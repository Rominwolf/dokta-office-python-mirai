import HttpRequests
import MiraiHttpApi
import json
import os
import requests
import ConfigParser
import base64
import random
import time
import DoVars
import urllib

DOKTA_OFFICE_SERVER = "https://api.do.wsm.ink/"

TEXT_ERROR_MESSAGE = "啊！数据库里没有该档案……\n可能是参数错误？\n您也可以申请加入该 群(854154822) 反馈问题。"
TEXT_ERROR_BAG_MESSAGE = "咦？这个背包里空空如也诶！\n您什么都没有抽到……"
TEXT_ERROR_PLOT_MESSAGE = "啊哦！生成这个关卡的剧情失败了！\n可能是关卡ID或位置无效…？"

TEXT_MSG_NEWS_ONLY_PRIVATE = "为防止刷屏，该条消息已经私信发送给你了。\n如果你和我不互为好友关系，那么你可能接收不到消息。"

TEXT_LOADING_MATERIAL_INFO = "正在获取该材料的掉落矩阵，请稍等片刻……\n受各方面因素影响，可能会在几分钟内发送。"
TEXT_LOADING_HR_INFO = "正在为您分析结果，请稍等片刻……\n受各方面因素影响，可能会在几分钟内发送。"
TEXT_LOADING_NEWS_INFO = "正在获取近期明日方舟发布的新闻，请稍等片刻……\n受各方面因素影响，可能会在几分钟内发送。"
TEXT_LOADING_FORM_INFO = "正在获取该干员的入职表，请稍等片刻……\n受各方面因素影响，可能会在几分钟内发送。"
TEXT_LOADING_RANGE_INFO = "正在生成该攻击范围的图片，请稍等片刻……\n受各方面因素影响，可能会在几秒内发送。"
TEXT_LOADING_PLOT_INFO = "正在生成关卡该的剧情图片，请稍等片刻……\n受剧情长度影响，将在几分钟至几十分钟内发送。"
TEXT_LOADING_BAG_INFO = "你的回合，开包！\n正在评估你的欧气，请稍等片刻……"
TEXT_LOADING_BAG_CLOSED_INFO = "本群已关闭干员寻访功能…该怎么办呢？\n▪ 联系管理员使用 命令(/do set) 开启本功能；\n▪ 添加我为好友并私聊相同的指令。"

TEXT_SET_INFO = "- 群设定 -\n干员寻访 => {1} (/do set bag <on/off>)\n新闻推送 => {2} (/do set news <on/off>)"
TEXT_SET_SUCCESSED_INFO = "好的！已将该群的“{1}”功能设置为{2}状态。"

TEXT_SET_PERSONAL_INFO = "- 个人设定 -\n新闻推送 => {1} (/do set news <on/off>)"
TEXT_SET_PERSONAL_SUCCESSED_INFO = "明白！已将你办公室的{1}功能设置为{2}状态。"

# 返回材料矩阵信息
def getMaterialInfo(material, fullMode):
    url = DOKTA_OFFICE_SERVER + "material/" + material
    data = "msgMode=true&fullMode=" + fullMode
    response = HttpRequests.doPost(url, data)
    return response

# 发送材料矩阵信息
def sendMaterialInfo(type, fromAccount, fromGroup, material, msgId, fullMode='false'):
    loadingMessage = TEXT_LOADING_MATERIAL_INFO.replace("{1}", material)
    loadingMessage = [{'type':'Plain','text':loadingMessage}]

    if(type == 'FriendMessage'):
        loadingMsgId = MiraiHttpApi.sendFriendMessage(fromAccount, loadingMessage)
    else:
        loadingMsgId = MiraiHttpApi.sendGroupMessage(fromGroup, fromAccount, loadingMessage, msgId)

    try:
        content = getMaterialInfo(material, fullMode)

        if '<html>' in content:
            content = TEXT_ERROR_MESSAGE

        message = [{'type':'Plain','text':content}]

        if(type == 'FriendMessage'):
            MiraiHttpApi.sendFriendMessage(fromAccount, message)
        else:
            MiraiHttpApi.sendGroupMessage(fromGroup, fromAccount, message, msgId)

    except:
        errorMessage = [{'type':'Plain','text':TEXT_ERROR_MESSAGE}]

        if(type == 'FriendMessage'):
            MiraiHttpApi.sendFriendMessage(fromAccount, errorMessage, msgId)
        else:
            MiraiHttpApi.sendGroupMessage(fromGroup, fromAccount, errorMessage, msgId)

    MiraiHttpApi.recall(loadingMsgId)

# 返回人力资源标签信息
def getHumanResourceInfo(type, hr):
    url = DOKTA_OFFICE_SERVER + "hr/"
    url = url + type

    if(type == 'tag'):
        data = "tags=" + hr.replace(' ', ',')
    else:
        data = hr

    url = url + "?fullMode=true"
    try:
        response = HttpRequests.doPost(url, data)
    except:
        response = TEXT_ERROR_MESSAGE

    return response
    
# 获取 OCR Token
def ocrBaiduCloudToken():
    url = DOKTA_OFFICE_SERVER + "hr/token"
    response = HttpRequests.doPost(url, "")
    return response
    
# OCR处理
def ocrBaiduCloudAnalyze(url):
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
    imageId = str(random.randint(0, 9999999)) + ".jpg"
    r = requests.get(url) 
    imageData = HttpRequests.doGet(url)

    with open(imageId,'wb') as f:
        f.write(r.content)
    
    f = open(imageId, 'rb')
    img = base64.encodebytes(f.read())

    os.remove(imageId)

    params = {"image":img}
    access_token = ocrBaiduCloudToken()
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        return response.text
    
# 发送人力资源标签信息
def sendHumanResourceInfo(type, fromAccount, fromGroup, hr, msgId):
    loadingMessage = TEXT_LOADING_HR_INFO
    loadingMessage = [{'type':'Plain','text':loadingMessage}]

    if(type == 'FriendMessage'):
        loadingMsgId = MiraiHttpApi.sendFriendMessage(fromAccount, loadingMessage)
    else:
        loadingMsgId = MiraiHttpApi.sendGroupMessage(fromGroup, fromAccount, loadingMessage, msgId)

    hrType = 'tag'
    if 'http' in hr:
        hrType = 'json'
        hr = ocrBaiduCloudAnalyze(hr)

    content = getHumanResourceInfo(hrType, hr)

    if '<html>' in content:
        content = TEXT_ERROR_MESSAGE

    message = [{'type':'Plain','text':content}]

    if(type == 'FriendMessage'):
        MiraiHttpApi.sendFriendMessage(fromAccount, message)
    else:
        MiraiHttpApi.sendGroupMessage(fromGroup, fromAccount, message, msgId)

    MiraiHttpApi.recall(loadingMsgId)

# 返回干员入职表信息
def getOperatorEntryInfo(operator):
    b64Type = base64.urlsafe_b64encode(operator.encode()).decode()
    response = DOKTA_OFFICE_SERVER + "entry/" + b64Type + "?base64=true"
    print(response)
    return response

# 发送干员入职表信息
def sendOperatorResourceInfo(type, fromAccount, fromGroup, operator, msgId, uncompressedMode='false'):
    msgType = 'Image'

    loadingMessage = TEXT_LOADING_FORM_INFO.replace("{1}", operator)
    loadingMessage = [{'type':'Plain','text':loadingMessage}]

    if(type == 'FriendMessage'):
        loadingMsgId = MiraiHttpApi.sendFriendMessage(fromAccount, loadingMessage)
    else:
        loadingMsgId = MiraiHttpApi.sendGroupMessage(fromGroup, fromAccount, loadingMessage, msgId)

    imageUrl = getOperatorEntryInfo(operator)

    message = [{'type':msgType,'url':imageUrl}]
    
    if(operator == "阿米娅"):
        casterAmiya = getOperatorEntryInfo("阿米娅")
        warriorAmiya = getOperatorEntryInfo("近卫阿米娅")
        message = [{'type':'Image','url':casterAmiya},{'type':'Image','url':warriorAmiya}]

    if operator == "霜星":
        randomTime = random.random() * 3
        strRandTime = str(int(randomTime * 1000))
        time.sleep(randomTime)
        message = [{'type':'Plain','text':DoVars.TEXT_FORM_FROSTNOVA.replace("{1}", strRandTime)}]

    if uncompressedMode == 'true':
        urlencode = urllib.parse.quote(operator)
        content = "请访问右侧链接获取未经压缩的干员入职表：https://do.wsm.ink/entry/" + urlencode
        message = [{'type':'Plain','text':content}]

    try:
        if(type == 'FriendMessage'):
            MiraiHttpApi.sendFriendMessage(fromAccount, message)
        else:
            MiraiHttpApi.sendGroupMessage(fromGroup, fromAccount, message, msgId)
    except:
        MiraiHttpApi.recall(loadingMsgId)
        content = TEXT_ERROR_MESSAGE
        message = [{'type':'Plain','text':content}]

        if(type == 'FriendMessage'):
            MiraiHttpApi.sendFriendMessage(fromAccount, message)
        else:
            MiraiHttpApi.sendGroupMessage(fromGroup, fromAccount, message, msgId)

    MiraiHttpApi.recall(loadingMsgId)

# 返回群数据信息
def getGlobalSettingsInfo(fromGroup):
    stateBag = ConfigParser.getValueConfig(DoVars.groupConfig, fromGroup, "state_bag", DoVars.groupConfigFile)

    if stateBag == "false":
        stateBag = "关闭"
    else:
        stateBag = "开启"
    
    response = TEXT_SET_INFO.replace("{1}", stateBag)

    newsPushList = ConfigParser.getValueConfig(DoVars.groupConfig, "global", "news_push", DoVars.groupConfigFile)
    newsPush = newsPushList.split(",")

    if str(fromGroup) in newsPush:
        stateNewsPush = "开启"
    else:
        stateNewsPush = "关闭"
    
    response = response.replace("{2}", stateNewsPush)

    return response

# 返回一项群数据信息
def getTheGlobalSettingInfo(fromGroup, key):
    response = ConfigParser.getValueConfig(DoVars.groupConfig, fromGroup, key, DoVars.groupConfigFile)
    return response

# 返回设置后的群数据信息
def setGlobalSettingsInfo(fromGroup, key, value):
    if key == 'bag':
        key = 'state_bag'
        name = '干员寻访'
        if value == 'on':
            state = 'true'
            stateChn = "开启"
        else:
            state = 'false'
            stateChn = "关闭"
    
    if key == 'news':
        groups = ConfigParser.getValueConfig(DoVars.groupConfig, "global", "news_push", DoVars.groupConfigFile)
        groupsList = groups.split(",")
        key = 'news_push'
        name = '新闻推送'
        
        if value == 'on':
            state = groups + "," + str(fromGroup)
            stateChn = "开启"
            
            if str(fromGroup) in groupsList:
                state = groups
        else:
            state = groups.replace("," + str(fromGroup), "")
            stateChn = "关闭"
            
        fromGroup = "global"
    
    ConfigParser.setValueConfig(DoVars.groupConfig, DoVars.groupConfigFile, fromGroup, key, state)

    response = TEXT_SET_SUCCESSED_INFO.replace("{1}", name).replace("{2}", stateChn)
    return response

# 发送群数据信息
def sendGlobalSettingsInfo(fromGroup, key, value, msgId):
    if key == '':
        content = getGlobalSettingsInfo(fromGroup)
        message = [{'type':'Plain','text':content}]
        MiraiHttpApi.sendGroupMessage(fromGroup, -1, message, msgId)
        return 0
    
    content = setGlobalSettingsInfo(fromGroup, key, value)
    message = [{'type':'Plain','text':content}]
    MiraiHttpApi.sendGroupMessage(fromGroup, -1, message, msgId)
    return 0

# 返回个人数据信息
def getPersonalSettingsInfo(fromAccount):
    newsPushList = ConfigParser.getValueConfig(DoVars.userConfig, "global", "news_push", DoVars.userConfigFile)
    newsPush = newsPushList.split(",")

    if str(fromAccount) in newsPush:
        stateNewsPush = "开启"
    else:
        stateNewsPush = "关闭"
    
    response = TEXT_SET_PERSONAL_INFO.replace("{1}", stateNewsPush)

    return response

# 返回一项个人数据信息
def getThePersonalSettingInfo(fromAccount, key):
    response = ConfigParser.getValueConfig(DoVars.userConfig, fromAccount, key, DoVars.userConfigFile)
    return response

# 返回设置后的个人数据信息
def setPersonalSettingsInfo(fromAccount, key, value):
    if key == 'news':
        users = ConfigParser.getValueConfig(DoVars.userConfig, "global", "news_push", DoVars.userConfigFile)
        usersList = users.split(",")
        key = 'news_push'
        name = '新闻推送'
        
        if value == 'on':
            state = users + "," + str(fromAccount)
            stateChn = "开启"
            
            if str(fromAccount) in usersList:
                state = users
        else:
            state = users.replace("," + str(fromAccount), "")
            stateChn = "关闭"
            
        fromAccount = "global"
    
    ConfigParser.setValueConfig(DoVars.userConfig, DoVars.userConfigFile, fromAccount, key, state)

    response = TEXT_SET_PERSONAL_SUCCESSED_INFO.replace("{1}", name).replace("{2}", stateChn)
    return response

# 发送个人数据信息
def sendPersonalSettingsInfo(fromAccount, key, value):
    if key == '':
        content = getPersonalSettingsInfo(fromAccount)
        message = [{'type':'Plain','text':content}]
        MiraiHttpApi.sendFriendMessage(fromAccount, message)
        return 0
    
    content = setPersonalSettingsInfo(fromAccount, key, value)
    message = [{'type':'Plain','text':content}]
    MiraiHttpApi.sendFriendMessage(fromAccount, message)
    return 0

# 返回干员寻访信息
def getBagInfo(type):
    if "one" in type:
        type = "gacha/" + type
    else:
        type = "bag/" + type
        
    response = DOKTA_OFFICE_SERVER + type
    return response

# 发送干员寻访信息
def sendBagInfo(type, fromAccount, fromGroup, bag, msgId):
    loadingMessage = TEXT_LOADING_BAG_INFO
    loadingMessage = [{'type':'Plain','text':loadingMessage}]

    if(type == 'FriendMessage'):
        loadingMsgId = MiraiHttpApi.sendFriendMessage(fromAccount, loadingMessage)
    else:
        loadingMsgId = MiraiHttpApi.sendGroupMessage(fromGroup, fromAccount, loadingMessage, msgId)

        if(getTheGlobalSettingInfo(fromGroup, "state_bag") == 'false'):
            bagClosedMessage = TEXT_LOADING_BAG_CLOSED_INFO
            bagClosedMessage = [{'type':'Plain','text':bagClosedMessage}]
            MiraiHttpApi.sendGroupMessage(fromGroup, fromAccount, bagClosedMessage, msgId)
            MiraiHttpApi.recall(loadingMsgId)
            return

    bag += "?qq=" + str(fromAccount)

    imageUrl = getBagInfo(bag)
    print(imageUrl)

    message = [{'type':'Image','url':imageUrl}]

    try:
        if(type == 'FriendMessage'):
            MiraiHttpApi.sendFriendMessage(fromAccount, message)
        else:
            MiraiHttpApi.sendGroupMessage(fromGroup, fromAccount, message, msgId)
    except:
        MiraiHttpApi.recall(loadingMsgId)
        content = TEXT_ERROR_BAG_MESSAGE
        message = [{'type':'Plain','text':content}]

        if(type == 'FriendMessage'):
            MiraiHttpApi.sendFriendMessage(fromAccount, message)
        else:
            MiraiHttpApi.sendGroupMessage(fromGroup, fromAccount, message, msgId)

    MiraiHttpApi.recall(loadingMsgId)

# 返回剧情回忆信息
def getPlotInfo(stageId, position, nickname, stageType):
    b64Nickname = base64.urlsafe_b64encode(nickname.encode()).decode()
    #stageType = "main"
    
    if position == "begin":
        position = "beg"

    plotRequest = "type=image&nickname={1}&stageId={2}&stageType={3}&position={4}"
    plotRequest = plotRequest.replace("{1}", b64Nickname)
    plotRequest = plotRequest.replace("{2}", stageId)
    plotRequest = plotRequest.replace("{3}", stageType)
    plotRequest = plotRequest.replace("{4}", position)
    
    response = DOKTA_OFFICE_SERVER + "plot?" + plotRequest
    return response

# 发送剧情回忆信息 /do plot <Id> <Position> [Nickname] [Type]
def sendPlotInfo(type, fromAccount, fromGroup, plot, msgId, accountName):
    loadingMessage = TEXT_LOADING_PLOT_INFO
    loadingMessage = [{'type':'Plain','text':loadingMessage}]

    if(type == 'FriendMessage'):
        loadingMsgId = MiraiHttpApi.sendFriendMessage(fromAccount, loadingMessage)
    else:
        loadingMsgId = MiraiHttpApi.sendGroupMessage(fromGroup, fromAccount, loadingMessage, msgId)

    plotData = plot.split(" ")
    if(len(plotData) < 2):
        content = TEXT_ERROR_PLOT_MESSAGE
        message = [{'type':'Plain','text':content}]
    else:
        stageId = plotData[0]
        position = plotData[1]
        stageType = ""
        nickname = ""
        
        if len(plotData) >= 3:
            nickname = plotData[2]

        if len(plotData) >= 4:
            stageType = plotData[3]

        content = getPlotInfo(stageId, position, nickname, stageType)
        print(content)
        
        message = [{'type':'Image','url':content}]
        if '<html>' in content:
            content = TEXT_ERROR_MESSAGE

    try:
        if(type == 'FriendMessage'):
            MiraiHttpApi.sendFriendMessage(fromAccount, message)
        else:
            MiraiHttpApi.sendGroupMessage(fromGroup, fromAccount, message, msgId)
    except:
        MiraiHttpApi.recall(loadingMsgId)
        content = TEXT_ERROR_MESSAGE
        message = [{'type':'Plain','text':content}]

        if(type == 'FriendMessage'):
            MiraiHttpApi.sendFriendMessage(fromAccount, message)
        else:
            MiraiHttpApi.sendGroupMessage(fromGroup, fromAccount, message, msgId)

    MiraiHttpApi.recall(loadingMsgId)

# 返回关于应用信息
def getAboutDoInfo(type):
    url = DOKTA_OFFICE_SERVER + "about/" + type
    response = HttpRequests.doGet(url)
    response = json.loads(response)
    return response['msg']

# 发送关于应用信息
def sendAboutDoInfo(type, fromAccount, fromGroup, about, msgId):
    aboutDo = getAboutDoInfo(about)

    message = [{'type':'Plain','text':aboutDo}]

    if(type == 'FriendMessage'):
        MiraiHttpApi.sendFriendMessage(fromAccount, message)
    else:
        MiraiHttpApi.sendGroupMessage(fromGroup, fromAccount, message, msgId)

# 返回攻击范围图片
def getRangeInfo(x, y, basis, exclude):
    url = DOKTA_OFFICE_SERVER + "range/"

    response = url + x + "/" + y + "/" + basis + "/" + exclude
    return response
    
# 发送攻击范围信息
def sendRangeInfo(type, fromAccount, fromGroup, rawRange, msgId):
    loadingMessage = TEXT_LOADING_RANGE_INFO
    loadingMessage = [{'type':'Plain','text':loadingMessage}]

    if(type == 'FriendMessage'):
        loadingMsgId = MiraiHttpApi.sendFriendMessage(fromAccount, loadingMessage)
    else:
        loadingMsgId = MiraiHttpApi.sendGroupMessage(fromGroup, fromAccount, loadingMessage, msgId)

    range = rawRange.split(" ")
    if(len(range) < 3):
        content = TEXT_ERROR_MESSAGE
        message = [{'type':'Plain','text':content}]
    else:
        x = range[0]
        y = range[1]
        basis = range[2]
        exclude = "0"
        
        if len(range) > 3:
            exclude = range[3]
        
        content = getRangeInfo(x, y, basis, exclude)
        message = [{'type':'Image','url':content}]
        if '<html>' in content:
            content = TEXT_ERROR_MESSAGE

    try:
        if(type == 'FriendMessage'):
            MiraiHttpApi.sendFriendMessage(fromAccount, message)
        else:
            MiraiHttpApi.sendGroupMessage(fromGroup, fromAccount, message, msgId)
    except:
        MiraiHttpApi.recall(loadingMsgId)
        content = TEXT_ERROR_MESSAGE
        message = [{'type':'Plain','text':content}]

        if(type == 'FriendMessage'):
            MiraiHttpApi.sendFriendMessage(fromAccount, message)
        else:
            MiraiHttpApi.sendGroupMessage(fromGroup, fromAccount, message, msgId)

    MiraiHttpApi.recall(loadingMsgId)

# 返回动态新闻信息
def getNewsInfo(type):
    url = DOKTA_OFFICE_SERVER + "news/" + type
    response = HttpRequests.doGet(url)
    return response

# 发送动态新闻信息
def sendNewsInfo(type, fromAccount, fromGroup, count, msgId):
    loadingMessage = TEXT_LOADING_NEWS_INFO
    loadingMessage = [{'type':'Plain','text':loadingMessage}]

    if(type == 'FriendMessage'):
        loadingMsgId = MiraiHttpApi.sendFriendMessage(fromAccount, loadingMessage)
    else:
        loadingMsgId = MiraiHttpApi.sendGroupMessage(fromGroup, fromAccount, loadingMessage, msgId)

    try:
        content = getNewsInfo('all?group=' + str(fromGroup) + '&qq=' + str(fromAccount))

        if '<html>' in content:
            content = TEXT_ERROR_MESSAGE
        else:
            dynamics = json.loads(content)
            
        if count < 1:
            count = 1
            
        if count > 10:
            count = 10
            
        for x in range(count):
            i = count - x - 1
            response = transformNewsDataToMsg(dynamics[i], 'all')
            MiraiHttpApi.sendFriendMessage(fromAccount, response, msgId)

        if(type == 'GroupMessage'):
            content = TEXT_MSG_NEWS_ONLY_PRIVATE
            message = [{'type':'Plain','text':content}]
            MiraiHttpApi.sendGroupMessage(fromGroup, fromAccount, message, msgId)

    except:
        errorMessage = [{'type':'Plain','text':TEXT_ERROR_MESSAGE}]

        if(type == 'FriendMessage'):
            MiraiHttpApi.sendFriendMessage(fromAccount, errorMessage, msgId)
        else:
            MiraiHttpApi.sendGroupMessage(fromGroup, fromAccount, errorMessage, msgId)

    MiraiHttpApi.recall(loadingMsgId)

# 将新闻数据转换成消息数据
def transformNewsDataToMsg(news, type, group=False):
    
    #注意注意注意啦！舟游官方发饼了！
    #时间：2020-12-15 16:30:56
    #链接：https://t.bilibili.com/468935936815296065
    #
    #【新增服饰】
    #//铁律 - 塞雷娅
    #忒斯特收藏系列/铁律。塞雷娅在进入曼斯菲尔德监狱时使用的狱警服，与女性狱警标准制服没有太大区别。
    #
    #_______________
    #服从即秩序，秩序即正义。 
    #[图片]
    #……等 8 张图片。
    
    msgNewActivity = "注意注意注意啦！舟游官方发饼了！"
    msgNewNoticeSmall = "海猫，手，两百合成玉——"
    msgNewNoticeBig = "海猫，手，五颗至纯源石——"
    
    if news['type'] == 'picture':#类型为带图动态
        
        content = "{1}\n时间：{2}\n链接：{3}\n{4}\n"
        
        if type == 'all':
            content = content.replace("{1}", "类型：带图动态")
        else:
            if '公告' in news['description']:
                if '10:00至16:00' in news['description']:
                    content = content.replace("{1}", msgNewNoticeBig)
                else:
                    content = content.replace("{1}", msgNewNoticeSmall)
            else:
                content = content.replace("{1}", msgNewActivity)
            
        if len(news['description']) > 160 and group != True:
            news['description'] = news['description'][0: 160] + "……"
            
        content = content.replace("{2}", news['datetime'])
        content = content.replace("{3}", news['url'])
        content = content.replace("{4}", news['description'].replace("#明日方舟#", ""))
        
        response = [{'type':'Plain','text': content}]
        
        if group != True:
            picturesCount = len(news['pictures'])
            response.append({'type': 'Image', 'url': news['pictures'][0]})
            response.append({'type': 'Plain', 'text': '\n……等 ' + str(picturesCount) + ' 张图片。'})
        else:
            for picture in news['pictures']:
                response.append({'type': 'Image', 'url': picture})

    if news['type'] == 'video':#类型为视频
        
        content = "{1}\n时间：{2}\n链接：{3}\n标题：{4}\n{5}\n"
        
        if type == 'all':
            content = content.replace("{1}", "类型：视频")
        else:
            content = content.replace("{1}", msgNewActivity)
            
        if len(news['dynamic']) > 160 and group != True:
            news['dynamic'] = news['dynamic'][0: 160] + "……"
            
        content = content.replace("{2}", news['datetime'])
        content = content.replace("{3}", news['videourl'])
        content = content.replace("{4}", news['title'])
        content = content.replace("{5}", news['dynamic'].replace("#明日方舟#", ""))
        
        response = [{'type':'Plain','text': content}]
        response.append({'type': 'Image', 'url': news['cover']})

    if news['type'] == 'plain':#类型为文字动态
        
        content = "{1}\n时间：{2}\n链接：{3}\n{4}\n"
        
        if type == 'all':
            content = content.replace("{1}", "类型：文字动态")
        else:
            if '公告' in news['description']:
                if '10:00至16:00' in news['description']:
                    content = content.replace("{1}", msgNewNoticeBig)
                else:
                    content = content.replace("{1}", msgNewNoticeSmall)
            else:
                content = content.replace("{1}", msgNewActivity)
            
        if len(news['content']) > 160 and group != True:
            news['content'] = news['content'][0: 160] + "……"
            
        content = content.replace("{2}", news['datetime'])
        content = content.replace("{3}", news['url'])
        content = content.replace("{4}", news['content'])
        
        response = [{'type':'Plain','text': content}]

    return response

# 每 3 分钟检测一次是否有新的未读消息
def timerCheckUnreadNews():
    ConfigParser.initConfig()

    #发送订阅新闻的群
    pushGroupRaw = ConfigParser.getValueConfig(DoVars.groupConfig, "global", "news_push", DoVars.groupConfigFile)
    pushGroup = pushGroupRaw.split(",")
    
    for group in pushGroup:
        news = getNewsInfo('unread?group=' + group + '&qq=-1')

        if news != 'null':
            news = json.loads(news)
            response = transformNewsDataToMsg(news, 'unread', True)
            MiraiHttpApi.sendGroupMessage(group, -1, response, -1)
            datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print("[" + datetime + "][Dokta Office] 新闻推送给 (群) " + group)
    
    #发送订阅新闻的用户
    pushUserRaw = ConfigParser.getValueConfig(DoVars.userConfig, "global", "news_push", DoVars.userConfigFile)
    pushUser = pushUserRaw.split(",")
    
    for user in pushUser:
        news = getNewsInfo('unread?qq=' + user + '&group=-1')

        if news != 'null':
            news = json.loads(news)
            response = transformNewsDataToMsg(news, 'unread', False)
            MiraiHttpApi.sendFriendMessage(user, response)
            datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print("[" + datetime + "][Dokta Office] 新闻推送给 (用户) " + user)
            
            
