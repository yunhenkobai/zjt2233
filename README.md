密码字典生成器使用介绍
📖 工具简介
密码字典生成器是一个基于个人信息生成密码字典的Python工具，专门用于教育学习和授权的安全测试。该工具能够根据目标的姓名、生日、手机号等个人信息，智能生成可能的密码组合。

⚠️ 重要声明
本工具仅用于教育学习和授权的安全测试目的，请确保在使用前获得适当的授权。任何未经授权的使用都是违法行为。

🚀 功能特点
✅ 支持中文姓名自动转拼音
✅ 智能生成多种大小写组合
✅ 支持特殊符号组合（@、!、*、#等）
✅ 多种个人信息组合方式
✅ 自动去重和排序
✅ 密码长度控制（6-18位）
✅ 双语界面支持
📋 系统要求
Python 3.6+
可选：pypinyin库（用于中文姓名处理）


使用命令
G:\字典\Social-Engineering-dictionary-generator-master\Social-Engineering-dictionary-generator-master>python zd_scq.py -h
警告: 未安装pypinyin库，将使用内置简单拼音映射
建议安装: pip install pypinyin
Warning: pypinyin library not installed, using built-in simple mapping
Recommend installation: pip install pypinyin
密码字典生成器 / Password Dictionary Generator
仅用于教育和授权的安全测试目的 / For educational and authorized security testing purposes only
请确保在使用此工具前获得适当的授权 / Please ensure you have proper authorization before using this tool
密码长度限制: 6-18位 / Password length limit: 6-18 characters
--------------------------------------------------------------------------------

密码字典生成器 v3.0 / Password Dictionary Generator v3.0
用法 / Usage: python dict_generator.py [选项/options]

选项 / Options:
  -h              显示此帮助信息 / Show this help message
  -n <姓名>       目标姓名，支持格式 / Target name formats supported:
                  拼音格式 / Pinyin format: zhang,san 或 zhang.san
                  中文格式 / Chinese format: 张三 (需要pypinyin库 / requires pypinyin library)
  -b <生日>       目标生日 (8位数字，如: 20031205) / Target birthday (8 digits, e.g., 20031205)
  -c <身份证>     身份证号 (18位) / ID card number (18 digits)
  -m <邮箱>       邮箱地址 (如: user@example.com) / Email address (e.g., user@example.com)
  -d <域名>       域名地址 (如: www.example.com) / Domain address (e.g., www.example.com)
  -p <手机号>     手机号 (11位数字) / Phone number (11 digits)
  -q <QQ号>       QQ号 / QQ number
  -i <用户ID>     常用用户ID / Common user ID

姓名处理增强功能 / Enhanced Name Processing:
  - 支持拼音首字母组合 (如: zs) / Supports pinyin initial combinations (e.g., zs)
  - 支持大小写变化 (如: Zs, ZS, zs) / Supports case variations (e.g., Zs, ZS, zs)
  - 支持特殊符号组合 (如: @, !, *, #, $, %) / Supports special character combinations
  - 支持与生日的多种组合格式 / Supports various combinations with birthday

密码长度限制 / Password Length Restrictions:
  - 只生成6-18位长度的密码 / Only generates passwords with 6-18 characters
  - 自动过滤过短或过长的密码 / Automatically filters passwords that are too short or too long

使用示例 / Examples:
  python dict_generator.py -n zhang,san -b 20031205
  python dict_generator.py -n 张三 -b 20031205 -p 13912345678
  python dict_generator.py -n li.ming -b 19950316 -d www.example.com

生成密码示例 / Generated password examples:
  zs20031205, Zs@20031205, 20031205zs, ZS!20031205 等

注意事项 / Notes:
  - 中文姓名需要安装pypinyin库 / Chinese names require pypinyin library: pip install pypinyin
  - 运行后会提示输入文件名保存字典 / You will be prompted to enter a filename to save the dictionary
  - 此工具仅用于教育和授权测试目的 / This tool is for educational and authorized testing purposes only
  - 密码长度限制在6-18位之间 / Password length is limited to 6-18 characters



可以自己去改，没问题
