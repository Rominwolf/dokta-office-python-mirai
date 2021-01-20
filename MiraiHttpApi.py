import HttpRequests
import configparser
import json

host = "localhost:25565/"
authKey = "authKey"
qq = 0

#messages = [{'type':'Plain','text':message}, {'type':'Image','url':''}]

# 发送一条消息给指定用户，返回消息ID
def sendFriendMessage(fromAccount, messages, fromId=-1):
    url = "http://" + host + "sendFriendMessage"
    data = json.dumps({'sessionKey':getSession(), 'target':fromAccount, 'messageChain':messages})

    response = HttpRequests.doPost(url, data, {'Content-Type':'application/json'})
    print(response)
    if 'code' not in response:
        print(response)
        print(data)
        return 0
    
    messageId = getMessageId(response)
    return messageId

# 发送一条临时消息给指定用户，返回消息ID
def sendTempMessage(fromAccount, fromGroup, messages):
    url = "http://" + host + "sendTempMessage"
    data = json.dumps({'sessionKey':getSession(), 'qq':fromAccount, 'group':fromGroup, 'messageChain':messages})

    response = HttpRequests.doPost(url, data, {'Content-Type':'application/json'})

    if 'code' not in response:
        print(response)
        print(data)
        return 0
    
    messageId = getMessageId(response)
    return messageId

# 发送一条消息到指定群里，返回消息ID
def sendGroupMessage(fromGroup, fromAccount, messages, fromId=-1):
    url = "http://" + host + "sendGroupMessage"
    data = json.dumps({'sessionKey':getSession(), 'target':fromGroup, 'quote':fromId, 'messageChain':messages})

    if(fromId == -1):
        data = data.replace('"quote": -1, ', '')

    response = HttpRequests.doPost(url, data, {'Content-Type':'application/json'})
    messageId = getMessageId(response)
    return messageId

# 撤回一条消息，返回 Code
def recall(fromId):
    url = "http://" + host + "recall"
    data = json.dumps({'sessionKey':getSession(), 'target':fromId})
    response = HttpRequests.doPost(url, data, {'Content-Type':'application/json'})
    array = json.loads(response)
    return array['code']

# 通过 messageId 获取一条被缓存的消息
def messageFromId(id):
    url = "http://" + host + "messageFromId?sessionKey=" + getSession() + "&id=" + id
    response = HttpRequests.doGet(url, {'Content-Type':'application/json'})
    response = json.loads(response)
    return response

# 上传一张图片，如果成功返回图片外链，失败返回错误信息
def uploadImage(type, img):
    url = "http://" + host + "uploadImage"
    data = "sessionKey=" + getSession() + "&type=" + type + "&img=" + img
    response = HttpRequests.doPost(url, data, {'Content-Type':'multipart/form-data'})
    if '.mirai' in response:
        array = json.loads(response)
        return array['url']
    else:
        return response

# 获取一个新的 Session 并进行绑定后开放 Websocket 接口（返回 Session ID）
def createSession():
    #创建新 Session
    url = "http://" + host + "auth"
    data = json.dumps({'authKey':authKey})
    response = HttpRequests.doPost(url, data, {'Content-Type':'application/json'})
    array = json.loads(response)
    
    session = array['session']

    #绑定 Session 到 Bot
    url = "http://" + host + "verify"
    data = json.dumps({'sessionKey':session, 'qq':qq})
    response = HttpRequests.doPost(url, data, {'Content-Type':'application/json'})

    #修改 Session 的权限
    url = "http://" + host + "config"
    data = json.dumps({'sessionKey':session, 'enableWebsocket':'true'})
    response = HttpRequests.doPost(url, data, {'Content-Type':'application/json'})
    
    return session

# 释放一个 Session
def releaseSession(session):
    #绑定 Session 到 Bot
    url = "http://" + host + "release"
    data = json.dumps({'sessionKey':session, 'qq':qq})
    response = HttpRequests.doPost(url, data, {'Content-Type':'application/json'})

# 获取最近的可用的 Session
def getSession():
    sessionConfigFile = "session.ini"
    sessionConfig = configparser.ConfigParser()
    sessionConfig.read(sessionConfigFile, encoding="utf-8")
    response = sessionConfig.get("session", "key")
    return response

# 获取一条消息的ID
def getMessageId(data):
    data = str(data)
    array = json.loads(data)
    if(array['code'] == 0):
        return(array['messageId'])
    else:
        return -1
    
def getFriendList():
    url = "http://" + host + "friendList?sessionKey=" + getSession()
    response = HttpRequests.doGet(url, {'Content-Type':'application/json'})
    response = json.loads(response)
    return response
     
# 获取所有群信息
def getGroupList():
    url = "http://" + host + "groupList?sessionKey=" + getSession()
    response = HttpRequests.doGet(url, {'Content-Type':'application/json'})
    response = json.loads(response)
    return response
   
# 处理申请添加好友请求（0：同意；1：拒绝；2：拉黑）
def newFriendRequest(eventId, fromAccount, operate, fromGroup=0, message=""):
    url = "http://" + host + "resp/newFriendRequestEvent"
    data = json.dumps({'sessionKey':getSession(), 'eventId': eventId, 'fromId': fromAccount, 'groupId': fromGroup, 'operate': operate, 'message': message})
    HttpRequests.doPost(url, data, {'Content-Type':'application/json'})

# 处理申请机器人邀请进群请求（0：同意；1：拒绝）
def newGroupRequest(eventId, fromAccount, fromGroup, operate, message=""):
    url = "http://" + host + "resp/botInvitedJoinGroupRequestEvent"
    data = json.dumps({'sessionKey':getSession(), 'eventId': eventId, 'fromId': fromAccount, 'groupId': fromGroup, 'operate': operate, 'message': message})
    HttpRequests.doPost(url, data, {'Content-Type':'application/json'})

# 将消息串转换成 Mirai 码组合的字符串
def chainToMiraiMsg(data):
    response = ""
    chain = data['messageChain']
    
    for message in chain:
        if message['type'] == "Quote":
            response += "[mirai:quote,id=" + str(message['id']) + "]"
        if message['type'] == "At":
            response += "[mirai:at,id=" + str(message['target']) + "]"
        if message['type'] == "Face":
            response += "[mirai:face,id=" + str(message['faceId']) + "]"
        if message['type'] == "Xml":
            response += "[mirai:xml,content=" + str(message['xml']) + "]"
        if message['type'] == "Json":
            response += "[mirai:json,content=" + str(message['json']) + "]"
        if message['type'] == "App":
            response += "[mirai:app,content=" + str(message['content']) + "]"
        if message['type'] == "Poke":
            response += "[mirai:poke,name=" + str(message['name']) + "]"
        if message['type'] == "Image":
            imageId = str(message['imageId'])
            imageUrl = str(message['url'])
            imagePath = str(message['path'])
            response += "[mirai:image,id=" + imageId + ",url=" + imageUrl + ",path=" + imagePath + ",]"
        if message['type'] == "FlashImage":
            imageId = str(message['imageId'])
            imageUrl = str(message['url'])
            imagePath = str(message['path'])
            response += "[mirai:flash,id=" + imageId + ",url=" + imageUrl + ",path=" + imagePath + ",]"
        if message['type'] == "Voice":
            voiceId = str(message['imageId'])
            voiceUrl = str(message['url'])
            voicePath = str(message['path'])
            response += "[mirai:voice,id=" + voiceId + ",url=" + voiceUrl + ",path=" + voicePath + ",]"
        if message['type'] == "Plain":
            response += message['text']
    
    return  response