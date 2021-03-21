## 抱歉，因为刀客塔的办公室的后端程序出现了一些问题，所以该应用目前暂时无法使用。

## 刀客塔的办公室 Dokta's Office
> 明日方舟小助手。可以进行公招标签、材料掉落、干员养成分析及干员应聘表生成等功能。

**该版本为 Mirai 版，请确保您机器人使用的是 Mirai(https://github.com/mamoe/mirai) 平台。**  

### 须知
本应用遵循 **Apache License**，也请您遵守此协议。  
*开发者承诺本应用永久免费，请勿用于出售、转卖等商业行为。*

### 程序使用表
 - 本体源程序由 **Python** 编写，并调用了 **websocket-client** 客户端。
 - 基于 **Mirai**，并使用其 **mirai-http-api**(https://github.com/project-mirai/mirai-api-http) 应用。
 
### 安装并使用
 1. 下载 dokta-office-mirai 并将其解压到任意文件夹下内；
 2. 安装 Python3.X 和其 websocket-client、configparser、json、requests 库；
 3. 安装 Mirai-http-api 应用并进行配置；
 4. 修改 DoVars.py 文件中的 configFolder 变量，指向你 Mirai 程序中 /config/DoktaOffice/ 文件夹（可能需要创建文件夹）；
 5. 修改 MiraiHttpApi.py 文件中的 host、authKey 和 qq 变量，分别为你的 mirai-http-api 设定的地址、authKey 和你机器人的 QQ 号；
 6. *(可选)* 如果需要定时检测新闻，请使用 crontab 设定脚本，指向 DoktaOfficeBash.sh 文件。
 7. 运行 Mirai 后启动 session.py 和 do.py，然后开始使用吧！

### 使用帮助
https://www.wsm.ink/781

### 捐助开发者
https://afdian.net/@rominwolf
