import configparser
import ConfigParser
import MiraiHttpApi
import time
from threading import Timer

sessionConfigFile = "session.ini"
sessionConfig = configparser.ConfigParser()
sessionConfig.read(sessionConfigFile, encoding="utf-8")

# 更新 Session
def functionRebuildNewSession():
    oldSession = MiraiHttpApi.getSession()
    session = MiraiHttpApi.createSession()
    nowTime = time.asctime(time.localtime(time.time()))
    ConfigParser.setValueConfig(sessionConfig, sessionConfigFile, "session", "key", session)
    MiraiHttpApi.releaseSession(oldSession)
    print("[" + nowTime + "] Created new session:" + session + ", and released old session: " + oldSession)

# 每半小时调用一次该函数
def functionTimer(): 
    functionRebuildNewSession()
    Timer(1200, functionTimer).start()

functionTimer()