userConfig = 0
groupConfig = 0
configFolder = "../config/DoktaOffice/"
userConfigFile = configFolder + "UserConfig.ini"
groupConfigFile = configFolder + "GroupConfig.ini"

TEXT_PRIVATE_SEND_MESSAGE = "[完成] 已将该消息的结果私聊发送，请注意查收。"
TEXT_PERMISSION_DENIED_MESSAGE = "[错误] 你无权使用基于此二级指令的相关命令，因为你不是管理员。"
TEXT_PLEASE_SEND_HR_IMAGE_MESSAGE = "现在发送一张公开招募界面的图片，我会为你选择最佳标签。\n或者你也可以使用 /do hr [标签…] 来自行查询指定标签的组合（不要包括括号）。"
TEXT_HELP_COMMAND_ITEM_MESSAGE = "分析获取某种材料的掉落概率，支持中文全名、部分易记词、首字母缩写及唯一识别码（不要包括括号）。\n（默认显示所需理智由低到高前三名的关卡，结尾增加 -m 获取前十名关卡）\n命令: /do item <名字> [-m]\n例如: /do item 固源岩组, /do item 星星, /do item nzc -m, /do item 30103 -m, etc."
TEXT_HELP_COMMAND_FORM_MESSAGE = "获取指定干员的入职表，支持中文全名、部分常见名及唯一识别码（不要包括括号）。\n（默认显示压缩后的图片，结尾增加 -u 获取未压缩的原图）\n命令: /do form <姓名> [-u]\n例如: /do form 艾雅法拉, /do form 阿能, /do form 洁哥 -u, /do form char_391_rosmon -u, etc."
TEXT_HELP_COMMAND_RANGE_MESSAGE = "生成一个自定义的攻击范围图片（不要包括括号）。\n<X>：宽度、<Y>：高度、<Basis>：干员位置、[Exclude]：被排除的格子（多个格子以英文逗号分隔）\n命令: /do range <X> <Y> <Basis> [Exclude]\n例如: /do range 4 3 5, /do range 4 3 5 4,12, etc."
TEXT_HELP_COMMAND_PLOT_MESSAGE = "获取一节剧情对话记录（不要包括括号）。\n<Chapter>：章（从第零章开始）、<Section>：节（从第一节开始）；<Id>：关卡编号、<Position>：剧情位置；[Nickname]：博士名字、[Type]：关卡类型\n命令: /do plot <Id/Chapter> <Position/Section> [Type] [Nickname]\n例如: /do plot 7 5, /do plot 07-07 end 田所浩二, etc."
TEXT_FORM_FROSTNOVA = "罗德岛干员〔霜星〕。\n…资料完整度61.6%…\n…正在解析资料…\n…资料解析完成，耗时{1}毫秒。\n❌  您现在无权查阅此干员的档案。"