import websocket
import json
import time
import MiraiHttpApi
import HttpRequests
import ConfigParser
import DoktaOffice
import DoVars

# 获取字符串中间的内容
def getMiddleString(content, start_str, end):
    start = content.find(start_str)
    if start >= 0:
        start += len(start_str)
        end = content.find(end, start)
        if end >= 0:
            return content[start:end].strip()
            
# 私聊消息处理（message：消息串，fromAccount：来自QQ号，msgId：消息ID，fromNickname：来自QQ昵称，content：这条消息数据）
def friendMessage(message, fromAccount, msgId, fromNickname, content):
    msg = str(message)

    # 分析用户发来的图片，且进入了公招模式
    if 'mirai:image' in msg:
        if (ConfigParser.getValueConfig(DoVars.userConfig, fromAccount, 'hr', DoVars.userConfigFile) == 'true'):
            url = getMiddleString(msg, "url=", ",")
            DoktaOffice.sendHumanResourceInfo('FriendMessage', fromAccount, -1, url, msgId)
            ConfigParser.setValueConfig(DoVars.userConfig, DoVars.userConfigFile, fromAccount, "hr", "false")
            return 0

    # /do 获取应用命令帮助
    if msg == '/do':
        DoktaOffice.sendAboutDoInfo('FriendMessage', fromAccount, -1, 'command', msgId)
        return 0

    # /do item <material> 获取材料矩阵信息
    if msg.startswith('/do item'):
        if msg == '/do item':
            loadingMessage = [{'type':'Plain','text':DoVars.TEXT_HELP_COMMAND_ITEM_MESSAGE}]
            MiraiHttpApi.sendFriendMessage(fromAccount, loadingMessage, msgId)
            return 0
        
        material = msg.replace('/do item ', '')
        fullMode = 'false'
        
        if msg.endswith('-m'):
            material = getMiddleString(msg, "item ", " -m")
            fullMode = 'true'
        
        DoktaOffice.sendMaterialInfo('FriendMessage', fromAccount, -1, material, msgId, fullMode)
        return 0

    # /do hr [image/tags...] 分析公招标签组合
    if msg.startswith('/do hr'):
        if msg == '/do hr':
            ConfigParser.setValueConfig(DoVars.userConfig, DoVars.userConfigFile, fromAccount, "hr", "true")
            loadingMessage = [{'type':'Plain','text':DoVars.TEXT_PLEASE_SEND_HR_IMAGE_MESSAGE}]
            MiraiHttpApi.sendFriendMessage(fromAccount, loadingMessage, msgId)
            return 0
        elif 'mirai:image' in msg:
            url = getMiddleString(msg, "url=", ",")
            DoktaOffice.sendHumanResourceInfo('FriendMessage', fromAccount, -1, url, msgId)
            return 0
        else:
            tags = msg.replace('/do hr ', '')
            DoktaOffice.sendHumanResourceInfo('FriendMessage', fromAccount, -1, tags, msgId)
            return 0

    # /do form <operator> 获取干员入职表图
    if msg.startswith('/do form'):
        if msg == '/do form':
            loadingMessage = [{'type':'Plain','text':DoVars.TEXT_HELP_COMMAND_FORM_MESSAGE}]
            MiraiHttpApi.sendFriendMessage(fromAccount, loadingMessage, msgId)
            return 0
        
        operator = msg.replace('/do form ', '')
        uncompressedMode = 'false'
        
        if msg.endswith('-u'):
            operator = getMiddleString(msg, "form ", " -u")
            uncompressedMode = 'true'
        
        DoktaOffice.sendOperatorResourceInfo('FriendMessage', fromAccount, -1, operator, msgId, uncompressedMode)
        return 0

    # /do range <x> <y> <basis> [exclude] 生成攻击范围图片
    if msg.startswith('/do range'):
        if msg == '/do range':
            loadingMessage = [{'type':'Plain','text':DoVars.TEXT_HELP_COMMAND_RANGE_MESSAGE}]
            MiraiHttpApi.sendFriendMessage(fromAccount, loadingMessage, msgId)
            return 0
        
        operator = msg.replace('/do range ', '')
        DoktaOffice.sendRangeInfo('FriendMessage', fromAccount, -1, operator, msgId)
        return 0

    # /do plot <Id> <Position> [Nickname] [Type] 生成剧情回忆图片
    if msg.startswith('/do plot'):
        if msg == '/do plot':
            loadingMessage = [{'type':'Plain','text':DoVars.TEXT_HELP_COMMAND_PLOT_MESSAGE}]
            MiraiHttpApi.sendFriendMessage(fromAccount, loadingMessage, msgId)
            return 0
        
        plot = msg.replace('/do plot ', '')
        DoktaOffice.sendPlotInfo('FriendMessage', fromAccount, -1, plot, msgId, fromNickname)
        return 0

    # /do bag[s] 干员寻访
    if msg.startswith('/do bag'):
        if msg == '/do bag':
            DoktaOffice.sendBagInfo('FriendMessage', fromAccount, -1, 'one', msgId)
            return 0
        
        DoktaOffice.sendBagInfo('FriendMessage', fromAccount, -1, 'ten', msgId)
        return 0

    # /do about [type] 获取应用信息
    if msg.startswith('/do about'):
        if msg == '/do about':
            DoktaOffice.sendAboutDoInfo('FriendMessage', fromAccount, -1, 'do', msgId)
            return 0
        
        about = msg.replace('/do about ', '')
        DoktaOffice.sendAboutDoInfo('FriendMessage', fromAccount, -1, about, msgId)
        return 0

    # /do news [count] 获取近期消息
    if msg.startswith('/do news'):
        if msg == '/do news':
            count = 1
        else:
            count = int(msg.replace('/do news ', ''))

        DoktaOffice.sendNewsInfo('FriendMessage', fromAccount, -1, count, msgId)
        return 0

    # /do set [<key> <value>] 获取或设定个人设定
    if msg.startswith('/do set'):
        key = ''
        value = ''
        array = msg.split(' ')

        if len(array) == 4:
            key = array[2]
            value = array[3]

        DoktaOffice.sendPersonalSettingsInfo(fromAccount, key, value)

    return 0

# 群消息处理（message：消息串，fromGroup：QQ群号，fromAccount：QQ号，msgId：消息ID，fromPermission：来自QQ群的权限，botPermission：机器人群权限，fromNickname：来自QQ昵称，content：这条消息数据）
def groupMessage(message, fromGroup, fromAccount, msgId, fromPermission, botPermission, fromNickname, content):
    msg = str(message)

    # 如果该群没有配置文件，则创建一个
    if(DoVars.groupConfig.has_section(str(fromGroup)) == False):
        DoVars.groupConfig.add_section(str(fromGroup))
        DoVars.groupConfig.write(open(DoVars.groupConfigFile, "w"))

    # 分析用户发来的图片，且进入了公招模式
    if 'mirai:image' in msg:
        if (ConfigParser.getValueConfig(DoVars.groupConfig, fromGroup, 'hr_' + str(fromAccount), DoVars.groupConfigFile) == 'true'):
            url = getMiddleString(msg, "url=", ",")
            DoktaOffice.sendHumanResourceInfo('GroupMessage', fromAccount, fromGroup, url, msgId)
            ConfigParser.setValueConfig(DoVars.groupConfig, DoVars.groupConfigFile, fromGroup, "hr_" + str(fromAccount), "false")
            return 0
    
    # /do 获取应用命令帮助
    if msg == '/do':
        DoktaOffice.sendAboutDoInfo('GroupMessage', fromAccount, fromGroup, 'command', msgId)
        return 0
    
    # /do item <material> 获取材料矩阵信息
    if msg.startswith('/do item'):
        if msg == '/do item':
            loadingMessage = [{'type':'Plain','text':DoVars.TEXT_HELP_COMMAND_ITEM_MESSAGE}]
            MiraiHttpApi.sendGroupMessage(fromGroup, fromAccount, loadingMessage, msgId)
            return 0
        
        material = msg.replace('/do item ', '')
        fullMode = 'false'
        
        if msg.endswith('-m'):
            material = getMiddleString(msg, "item ", " -m")
            fullMode = 'true'
        
        material = msg.replace('/do item ', '').replace(' -m', '')
        
        DoktaOffice.sendMaterialInfo('GroupMessage', fromAccount, fromGroup, material, msgId, fullMode)
        return 0

    # /do hr [image/tags...] 分析公招标签组合
    if msg.startswith('/do hr'):
        if msg == '/do hr':
            ConfigParser.setValueConfig(DoVars.groupConfig, DoVars.groupConfigFile, fromGroup, "hr_" + str(fromAccount), "true")
            loadingMessage = [{'type':'Plain','text':DoVars.TEXT_PLEASE_SEND_HR_IMAGE_MESSAGE}]
            MiraiHttpApi.sendGroupMessage(fromGroup, fromAccount, loadingMessage, msgId)
            return 0
        elif 'mirai:image' in msg:
            url = getMiddleString(msg, "url=", ",")
            DoktaOffice.sendHumanResourceInfo('GroupMessage', fromAccount, fromGroup, url, msgId)
            return 0
        else:
            tags = msg.replace('/do hr ', '')
            DoktaOffice.sendHumanResourceInfo('GroupMessage', fromAccount, fromGroup, tags, msgId)
            return 0

    # /do hr + quote 分析公招标签组合
    if '/do hr' in msg and 'mirai:quote' in msg:
        quoteId = getMiddleString(msg, "quote,id=", "]")
        quote = MiraiHttpApi.messageFromId(quoteId)

        if quote['code'] != 0:
            loadingMessage = [{'type':'Plain','text':"无法获取消息，原因：" + quote['msg'] + "。"}]
            MiraiHttpApi.sendGroupMessage(fromGroup, fromAccount, loadingMessage, msgId)
            return 0
            
        quoteMsg = MiraiHttpApi.chainToMiraiMsg(quote['data'])
        url = str(getMiddleString(quoteMsg, "url=", ","))
        DoktaOffice.sendHumanResourceInfo('GroupMessage', fromAccount, fromGroup, url, msgId)
        return 0

    # /do form <operator> 获取干员入职表图
    if msg.startswith('/do form'):
        if msg == '/do form':
            loadingMessage = [{'type':'Plain','text':DoVars.TEXT_HELP_COMMAND_FORM_MESSAGE}]
            MiraiHttpApi.sendGroupMessage(fromGroup, fromAccount, loadingMessage, msgId)
            return 0
        
        operator = msg.replace('/do form ', '')
        uncompressedMode = 'false'
        
        if msg.endswith('-u'):
            operator = getMiddleString(msg, "form ", " -u")
            uncompressedMode = 'true'
        
        DoktaOffice.sendOperatorResourceInfo('GroupMessage', fromAccount, fromGroup, operator, msgId, uncompressedMode)
        return 0

    # /do range <x> <y> <basis> [exclude] 生成攻击范围图片
    if msg.startswith('/do range'):
        if msg == '/do range':
            loadingMessage = [{'type':'Plain','text':DoVars.TEXT_HELP_COMMAND_RANGE_MESSAGE}]
            MiraiHttpApi.sendGroupMessage(fromGroup, fromAccount, loadingMessage, msgId)
            return 0
        
        operator = msg.replace('/do range ', '')
        DoktaOffice.sendRangeInfo('GroupMessage', fromAccount, fromGroup, operator, msgId)
        return 0

    # /do plot <Id> <Position> [Nickname] [Type] 生成剧情回忆图片
    if msg.startswith('/do plot'):
        if msg == '/do plot':
            loadingMessage = [{'type':'Plain','text':DoVars.TEXT_HELP_COMMAND_PLOT_MESSAGE}]
            MiraiHttpApi.sendGroupMessage(fromGroup, fromAccount, loadingMessage, msgId)
            return 0
        
        plot = msg.replace('/do plot ', '')
        DoktaOffice.sendPlotInfo('GroupMessage', fromAccount, fromGroup, plot, msgId, fromNickname)
        return 0

    # /do bag[s] 干员寻访
    if msg.startswith('/do bag'):
        if msg == '/do bag':
            DoktaOffice.sendBagInfo('GroupMessage', fromAccount, fromGroup, 'one', msgId)
            return 0
        
        DoktaOffice.sendBagInfo('GroupMessage', fromAccount, fromGroup, 'ten', msgId)
        return 0

    # /do about [type] 获取应用信息
    if msg.startswith('/do about'):
        if msg == '/do about':
            DoktaOffice.sendAboutDoInfo('GroupMessage', fromAccount, fromGroup, 'do', msgId)
            return 0
        
        about = msg.replace('/do about ', '')
        DoktaOffice.sendAboutDoInfo('GroupMessage', fromAccount, fromGroup, about, msgId)
        return 0

    # /do news [count] 获取近期消息
    if msg.startswith('/do news'):
        if msg == '/do news':
            count = 1
        else:
            count = int(msg.replace('/do news ', ''))

        DoktaOffice.sendNewsInfo('GroupMessage', fromAccount, fromGroup, count, msgId)
        return 0

    # /do set [<key> <value>] 获取或设定群属性
    if msg.startswith('/do set'):
        if fromPermission == 'MEMBER':
            permissionMessage = [{'type':'Plain','text':DoVars.TEXT_PERMISSION_DENIED_MESSAGE}]
            MiraiHttpApi.sendGroupMessage(fromGroup, fromAccount, permissionMessage, msgId)
            return 0

        key = ''
        value = ''
        array = msg.split(' ')

        if len(array) == 4:
            key = array[2]
            value = array[3]

        DoktaOffice.sendGlobalSettingsInfo(fromGroup, key, value, msgId)

    return 0

def on_message(ws, message):
    data = json.loads(message)
    msgType = data['type']

    # 转到处理群、私聊消息函数
    if 'Message' in msgType:
        message = MiraiHttpApi.chainToMiraiMsg(data)
        msgId = data['messageChain'][0]['id']
        fromAccount = data['sender']['id']
        localTime = time.localtime(data['messageChain'][0]['time'])
        timedate = time.strftime("%Y-%m-%d %H:%M:%S", localTime)
        
        if(msgType == 'FriendMessage'):
            fromNickname = data['sender']['nickname']
            print("[" + timedate + "][" + msgType + "]" + fromNickname + "(" + str(fromAccount) + "):\n\t" + message)
            friendMessage(message, fromAccount, msgId, fromNickname, data)
        else:
            fromGroup = data['sender']['group']['id']
            fromNickname = data['sender']['memberName']
            fromPermission = data['sender']['permission']
            botPermission = data['sender']['group']['permission']
            print("[" + timedate + "][" + msgType + "][" + str(fromGroup) + "]" + fromNickname + "(" + str(fromAccount) + "):\n\t" + message)
            groupMessage(message, fromGroup, fromAccount, msgId, fromPermission, botPermission, fromNickname, data)
        
        return

ConfigParser.initConfig()

websocket.enableTrace(True)
ws = websocket.WebSocketApp("ws://" + MiraiHttpApi.host + "all?sessionKey=" + MiraiHttpApi.getSession(),on_message=on_message)
ws.run_forever()
