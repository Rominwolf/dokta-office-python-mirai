import configparser
import DoVars

# 初始化配置文件
def initConfig():
    DoVars.userConfig = configparser.ConfigParser()
    DoVars.groupConfig = configparser.ConfigParser()

    DoVars.userConfig.read(DoVars.userConfigFile, encoding="utf-8")
    DoVars.groupConfig.read(DoVars.groupConfigFile, encoding="utf-8")

# 设置配置文件的值
def setValueConfig(config, fileName, section, key, value):
    response = config.set(str(section), key, value)
    config.write(open(fileName, "w"))
    return response

# 获取配置文件的值
def getValueConfig(config, section, key, fileName):
    try:
        response = config.get(str(section), key)
    except:
        setValueConfig(config, fileName, section, key, "false")
        response = "false"

    return response

