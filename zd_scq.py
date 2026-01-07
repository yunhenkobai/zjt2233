#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Password Dictionary Generator / 密码字典生成器
# A tool for generating password dictionaries based on personal information
# 基于个人信息生成密码字典的工具
# For educational and authorized security testing purposes only
# 仅用于教育和授权的安全测试目的

import sys
import getopt
import os
import re

# Try to import pypinyin library for Chinese character support
# 尝试导入pypinyin库以支持中文字符处理
try:
    from pypinyin import lazy_pinyin, Style

    HAS_PYPINYIN = True
except ImportError:
    HAS_PYPINYIN = False
    print("警告: 未安装pypinyin库，将使用内置简单拼音映射")
    print("建议安装: pip install pypinyin")
    print("Warning: pypinyin library not installed, using built-in simple mapping")
    print("Recommend installation: pip install pypinyin")


def usage():
    """Display help menu / 显示帮助菜单"""
    print("""
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
""")


class PinyinConverter:
    """拼音转换器 / Pinyin converter for Chinese characters"""

    # 常用中文姓氏和名字映射 / Common Chinese surname and given name mappings
    SIMPLE_PINYIN_MAP = {
        # 常用姓氏 / Common surnames
        '张': 'zhang', '王': 'wang', '李': 'li', '赵': 'zhao', '刘': 'liu',
        '陈': 'chen', '杨': 'yang', '黄': 'huang', '周': 'zhou', '吴': 'wu',
        '徐': 'xu', '孙': 'sun', '马': 'ma', '朱': 'zhu', '胡': 'hu',
        '郭': 'guo', '何': 'he', '高': 'gao', '林': 'lin', '罗': 'luo',
        '郑': 'zheng', '梁': 'liang', '谢': 'xie', '宋': 'song', '唐': 'tang',
        '许': 'xu', '韩': 'han', '冯': 'feng', '邓': 'deng', '曹': 'cao',
        '彭': 'peng', '曾': 'zeng', '萧': 'xiao', '田': 'tian', '董': 'dong',
        '袁': 'yuan', '潘': 'pan', '于': 'yu', '蒋': 'jiang', '蔡': 'cai',
        '余': 'yu', '杜': 'du', '叶': 'ye', '程': 'cheng', '苏': 'su',
        '魏': 'wei', '吕': 'lv', '丁': 'ding', '任': 'ren', '沈': 'shen',
        '姚': 'yao', '卢': 'lu', '姜': 'jiang', '崔': 'cui', '钟': 'zhong',
        '谭': 'tan', '陆': 'lu', '汪': 'wang', '范': 'fan', '金': 'jin',
        '石': 'shi', '廖': 'liao', '贾': 'jia', '夏': 'xia', '韦': 'wei',
        '付': 'fu', '方': 'fang', '白': 'bai', '邹': 'zou', '孟': 'meng',
        '熊': 'xiong', '秦': 'qin', '邱': 'qiu', '江': 'jiang', '尹': 'yin',
        '薛': 'xue', '闫': 'yan', '段': 'duan', '雷': 'lei', '侯': 'hou',
        '龙': 'long', '史': 'shi', '陶': 'tao', '黎': 'li', '贺': 'he',
        '顾': 'gu', '毛': 'mao', '郝': 'hao', '龚': 'gong', '邵': 'shao',

        # 常用名字 / Common given names
        '伟': 'wei', '芳': 'fang', '娜': 'na', '敏': 'min', '静': 'jing',
        '丽': 'li', '强': 'qiang', '磊': 'lei', '军': 'jun', '洋': 'yang',
        '勇': 'yong', '艳': 'yan', '杰': 'jie', '娟': 'juan', '涛': 'tao',
        '明': 'ming', '超': 'chao', '秀': 'xiu', '英': 'ying', '华': 'hua',
        '慧': 'hui', '巧': 'qiao', '美': 'mei', '丹': 'dan', '红': 'hong',
        '玉': 'yu', '萍': 'ping', '婷': 'ting', '玲': 'ling', '雪': 'xue',
        '霞': 'xia', '飞': 'fei', '凯': 'kai', '浩': 'hao', '亮': 'liang',
        '政': 'zheng', '谦': 'qian', '亨': 'heng', '奇': 'qi', '固': 'gu',
        '之': 'zhi', '轮': 'lun', '翰': 'han', '朗': 'lang', '伯': 'bo',
        '宏': 'hong', '言': 'yan', '若': 'ruo', '鸣': 'ming', '朋': 'peng',
        '斌': 'bin', '栋': 'dong', '维': 'wei', '启': 'qi', '克': 'ke',
        '伦': 'lun', '翔': 'xiang', '旭': 'xu', '鹏': 'peng', '泽': 'ze',
        '晨': 'chen', '辰': 'chen', '士': 'shi', '以': 'yi', '建': 'jian',
        '家': 'jia', '致': 'zhi', '树': 'shu', '炎': 'yan', '德': 'de',
        '行': 'xing', '时': 'shi', '泰': 'tai', '盛': 'sheng', '雄': 'xiong',
        '琛': 'chen', '钧': 'jun', '冠': 'guan', '策': 'ce', '腾': 'teng',
        '楠': 'nan', '榕': 'rong', '风': 'feng', '航': 'hang', '弘': 'hong',
        '锦': 'jin', '恒': 'heng', '鸿': 'hong', '运': 'yun', '成': 'cheng',
        '康': 'kang', '星': 'xing', '光': 'guang', '天': 'tian', '达': 'da',
        '安': 'an', '岩': 'yan', '中': 'zhong', '茂': 'mao', '进': 'jin',
        '有': 'you', '坚': 'jian', '和': 'he', '彪': 'biao', '博': 'bo',
        '诚': 'cheng', '先': 'xian', '敬': 'jing', '震': 'zhen', '振': 'zhen',
        '壮': 'zhuang', '会': 'hui', '思': 'si', '群': 'qun', '豪': 'hao',
        '心': 'xin', '邦': 'bang', '承': 'cheng', '乐': 'le', '绍': 'shao',
        '功': 'gong', '松': 'song', '善': 'shan', '厚': 'hou', '庆': 'qing',
        '民': 'min', '友': 'you', '裕': 'yu', '河': 'he', '哲': 'zhe',
        '江': 'jiang', '三': 'san', '四': 'si', '五': 'wu', '六': 'liu',
        '七': 'qi', '八': 'ba', '九': 'jiu', '十': 'shi'
    }

    @classmethod
    def to_pinyin(cls, chinese_text):
        """将中文字符转换为拼音 / Convert Chinese characters to pinyin"""
        if HAS_PYPINYIN:
            return lazy_pinyin(chinese_text, style=Style.NORMAL)
        else:
            # 使用简单映射 / Use simple mapping
            result = []
            for char in chinese_text:
                if char in cls.SIMPLE_PINYIN_MAP:
                    result.append(cls.SIMPLE_PINYIN_MAP[char])
                else:
                    result.append(char)  # 如果找不到映射，保持原字符 / Keep original character if no mapping found
            return result


class DictGenerator:
    """密码字典生成器主类 / Main password dictionary generator class"""

    def __init__(self):
        # 默认参数 / Default parameters
        self.name = None
        self.birthday = None
        self.id_card = None
        self.mail = None
        self.domain = None
        self.phone_number = None
        self.qq_number = None
        self.name_ab = None
        self.user_id = None
        self.filename = None

        # 密码长度限制 / Password length restrictions
        self.min_length = 6  # 最小长度 / Minimum length
        self.max_length = 18  # 最大长度 / Maximum length

        # 姓名相关 / Name related
        self.name_pinyin_list = []  # 拼音列表 / Pinyin list
        self.name_initials = ""  # 首字母缩写 / Initial abbreviation
        self.name_combinations = []  # 各种姓名组合 / Various name combinations

        # 特殊符号 / Special characters
        self.special_chars = ["@", "!", "*", "#", "$", "%", "&", "+", "=", "?", "~"]

        # 数字组合 / Number combinations
        self.number_value_1 = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

        self.number_value_2 = ["00", "01", "02", "03", "04", "05", "06", "07",
                               "10", "11", "12", "13", "20", "22", "30", "33",
                               "08", "09", "40", "44", "50", "55", "60",
                               "66", "70", "77", "80", "88", "90", "99"]

        self.number_value_3 = ["000", "001", "101", "110", "111", "121", "123",
                               "212", "222", "250", "333", "444", "520", "555",
                               "666", "777", "888", "999"]

        self.number_value_4 = ["000000", "111111", "110120", "123321",
                               "123456", "123123", "222222", "333333",
                               "666666", "654321", "888888", "999999",
                               "1234", "1314", "5201314", "1212", "1111",
                               "0000", "123456789", "123123123"]

        # 常用弱密码 / Common weak passwords
        self.weak_password = ["qwerty", "qwert", "abc", "qazwsx",
                              "1q2w3e4r", "abcd", "qwer", "qwe", "love",
                              "asdf", "iloveyou", "admin", "password",
                              "pass", "test", "baby", "honey", "welcome",
                              "login", "master", "angel", "princess"]

    def is_valid_length(self, password):
        """检查密码长度是否有效 / Check if password length is valid"""
        return self.min_length <= len(password) <= self.max_length

    def parse_args(self):
        """解析命令行参数 / Parse command line arguments"""
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hn:b:c:m:d:p:q:i:")
        except getopt.GetoptError as err:
            print(f"错误 / Error: {err}")
            usage()
            sys.exit(2)

        for options, value in opts:
            if options == "-h":
                usage()
                sys.exit()
            elif options == "-n":
                self.name = value
            elif options == "-b":
                if len(value) == 8 and value.isdigit():
                    self.birthday = value
                else:
                    raise ValueError(
                        '生日格式错误，应为8位数字 (如: 20031205) / Birthday format error, should be 8 digits (e.g., 20031205)')
            elif options == "-c":
                if len(value) == 18:
                    self.id_card = value
                else:
                    raise ValueError('身份证号格式错误，应为18位 / ID card format error, should be 18 digits')
            elif options == "-m":
                if '@' in value:
                    self.mail = value
                else:
                    raise ValueError('邮箱格式错误 / Email format error')
            elif options == "-d":
                self.domain = value
            elif options == "-p":
                if len(value) == 11 and value.isdigit():
                    self.phone_number = value
                else:
                    raise ValueError('手机号格式错误，应为11位数字 / Phone number format error, should be 11 digits')
            elif options == "-q":
                if value.isdigit():
                    self.qq_number = value
                else:
                    raise ValueError('QQ号格式错误，应为纯数字 / QQ number format error, should be digits only')
            elif options == "-i":
                self.user_id = value

    def process_name(self):
        """处理姓名信息 - 增强版 / Process name information - Enhanced version"""
        if not self.name:
            return

        print(f"正在处理姓名 / Processing name: {self.name}")

        # 判断输入格式 / Determine input format
        if ',' in self.name or '.' in self.name:
            # 拼音格式输入 / Pinyin format input
            separator = ',' if ',' in self.name else '.'
            self.name_pinyin_list = [name.strip().lower() for name in self.name.split(separator)]
        else:
            # 检查是否包含中文字符 / Check if contains Chinese characters
            if re.search(r'[\u4e00-\u9fff]', self.name):
                # 中文格式输入 / Chinese format input
                chinese_chars = list(self.name)
                self.name_pinyin_list = [py.lower() for py in PinyinConverter.to_pinyin(self.name)]
                print(f"中文转拼音 / Chinese to Pinyin: {chinese_chars} -> {self.name_pinyin_list}")
            else:
                # 纯英文，按字符分割 / Pure English, split by character
                self.name_pinyin_list = list(self.name.lower())

        # 生成首字母缩写 / Generate initial abbreviation
        self.name_initials = ''.join([name[0] for name in self.name_pinyin_list if name])

        # 生成各种姓名组合 / Generate various name combinations
        self._generate_name_combinations()

        print(f"拼音列表 / Pinyin list: {self.name_pinyin_list}")
        print(f"首字母缩写 / Initial abbreviation: {self.name_initials}")
        print(f"姓名组合数量 / Name combinations count: {len(self.name_combinations)}")

    def _generate_name_combinations(self):
        """生成各种姓名组合 / Generate various name combinations"""
        if not self.name_pinyin_list:
            return

        combinations = []

        # 基本组合 / Basic combinations
        full_name = ''.join(self.name_pinyin_list)
        combinations.append(full_name)
        combinations.append(full_name.capitalize())
        combinations.append(full_name.upper())

        # 首字母组合 / Initial combinations
        initials = self.name_initials
        if len(initials) >= 2:  # 确保首字母缩写至少2位 / Ensure initials are at least 2 characters
            combinations.extend([
                initials,  # zs
                initials.capitalize(),  # Zs
                initials.upper(),  # ZS
                initials[0].upper() + initials[1:],  # Zs
            ])

        # 姓氏+名字首字母 / Surname + given name initials
        if len(self.name_pinyin_list) >= 2:
            surname = self.name_pinyin_list[0]
            name_initials = ''.join([name[0] for name in self.name_pinyin_list[1:]])
            combinations.extend([
                surname + name_initials,
                surname.capitalize() + name_initials,
                surname.capitalize() + name_initials.upper(),
                surname.upper() + name_initials,
            ])

        # 名字组合（去掉姓氏） / Given name combinations (without surname)
        if len(self.name_pinyin_list) > 1:
            given_name = ''.join(self.name_pinyin_list[1:])
            combinations.extend([
                given_name,
                given_name.capitalize(),
                given_name.upper(),
            ])

        # 单个字的组合（只保留长度>=3的） / Individual character combinations (keep only length>=3)
        for name_part in self.name_pinyin_list:
            if len(name_part) >= 3:  # 只保留长度>=3的单个拼音 / Only keep individual pinyin with length>=3
                combinations.extend([
                    name_part,
                    name_part.capitalize(),
                    name_part.upper(),
                ])

        # 过滤长度并去重 / Filter by length and remove duplicates
        valid_combinations = [combo for combo in combinations if self.is_valid_length(combo)]
        self.name_combinations = list(set(valid_combinations))

        # 为兼容性保留旧的name_ab / Keep old name_ab for compatibility
        self.name_ab = [initials, self.name_pinyin_list[0] if self.name_pinyin_list else ""]

    def process_birthday(self):
        """处理生日信息 / Process birthday information"""
        # 通过身份证号提取生日 / Extract birthday from ID card
        if self.id_card and not self.birthday:
            self.birthday = self.id_card[6:14]

        if self.birthday:
            self.birthday_list = [
                self.birthday,  # 20031205
                self.birthday[0:4],  # 2003
                self.birthday[2:],  # 031205
                self.birthday[4:],  # 1205
                self.birthday[2:4],  # 03 (太短，会被过滤)
                self.birthday[4:6],  # 12 (太短，会被过滤)
                self.birthday[6:8],  # 05 (太短，会被过滤)
                self.birthday[2:6],  # 0312 (太短，会被过滤)
                self.birthday[4:8],  # 1205 (太短，会被过滤)
            ]
            # 过滤掉长度不符合要求的生日组合 / Filter birthday combinations that don't meet length requirements
            self.birthday_list = [birth for birth in self.birthday_list if len(birth) >= 4]

    def process_domain(self):
        """处理域名信息 / Process domain information"""
        if self.domain:
            domain_split = self.domain.split('.')
            if len(domain_split) == 3:
                self.domain_list = [
                    self.domain,
                    domain_split[1],
                    domain_split[1] + '.' + domain_split[2],
                    domain_split[0] + domain_split[1] + domain_split[2],
                    domain_split[1] + domain_split[2]
                ]
            elif len(domain_split) == 4:
                self.domain_list = [
                    self.domain,
                    domain_split[1],
                    domain_split[1] + '.' + domain_split[2] + '.' + domain_split[3],
                    domain_split[0] + domain_split[1] + domain_split[2] + domain_split[3],
                    domain_split[1] + domain_split[2] + domain_split[3]
                ]
            else:
                self.domain_list = [self.domain]

            # 过滤域名组合长度 / Filter domain combination lengths
            self.domain_list = [domain for domain in self.domain_list if self.is_valid_length(domain)]

    def process_mail(self):
        """处理邮箱信息 / Process email information"""
        if self.mail:
            mail_parts = self.mail.split('@')
            self.mail_list = [
                self.mail,
                mail_parts[0],  # 用户名部分 / Username part
                mail_parts[1],  # 域名部分 / Domain part
                mail_parts[1].split('.')[0]  # 域名主体部分 / Domain main part
            ]
            # 过滤邮箱组合长度 / Filter email combination lengths
            self.mail_list = [mail for mail in self.mail_list if self.is_valid_length(mail)]

    def write_dict(self, dict_list):
        """写入字典文件 / Write to dictionary file"""
        if not self.filename:
            return

        valid_passwords = []
        for item in dict_list:
            # 只保留长度在6-18位之间的密码 / Only keep passwords with length between 6-18 characters
            if self.is_valid_length(item):
                valid_passwords.append(item)

        if valid_passwords:  # 只有当有有效密码时才写入 / Only write when there are valid passwords
            with open(self.filename, "a", encoding='utf-8') as f:
                for password in valid_passwords:
                    f.write(password + '\n')

    def name_and_weak(self):
        """姓名与弱口令字段、常用数字组合 - 增强版 / Name with weak passwords and common numbers - Enhanced version"""
        dict_list = []

        # 使用所有姓名组合 / Use all name combinations
        for name_combo in self.name_combinations:
            dict_list.append(name_combo)

            # 与弱密码组合 / Combine with weak passwords
            for weak in self.weak_password:
                dict_list.extend([
                    name_combo + weak,
                    weak + name_combo,
                ])

            # 与数字组合 / Combine with numbers
            for number_list in [self.number_value_1, self.number_value_2,
                                self.number_value_3, self.number_value_4]:
                for number in number_list:
                    dict_list.extend([
                        name_combo + number,
                        number + name_combo,
                    ])

        self.write_dict(dict_list)

    def name_and_birthday_enhanced(self):
        """姓名与生日的增强组合 / Enhanced name and birthday combinations"""
        if not (self.name_combinations and self.birthday):
            return

        dict_list = []

        for name_combo in self.name_combinations:
            for birth_combo in self.birthday_list:
                # 基本组合 / Basic combinations
                dict_list.extend([
                    name_combo + birth_combo,  # zs20031205
                    birth_combo + name_combo,  # 20031205zs
                ])

                # 带特殊符号的组合 / Combinations with special characters
                for char in self.special_chars:
                    dict_list.extend([
                        name_combo + char + birth_combo,  # zs@20031205
                        birth_combo + char + name_combo,  # 20031205@zs
                        name_combo + birth_combo + char,  # zs20031205@
                        char + name_combo + birth_combo,  # @zs20031205
                    ])

                # 与弱密码的三元组合 / Three-element combinations with weak passwords
                for weak in self.weak_password[:5]:  # 进一步限制数量 / Further limit quantity
                    dict_list.extend([
                        name_combo + birth_combo + weak,
                        name_combo + weak + birth_combo,
                        weak + name_combo + birth_combo,
                    ])

        self.write_dict(dict_list)

    def domain_and_weak(self):
        """域名与弱口令 / Domain with weak passwords"""
        if not hasattr(self, 'domain_list'):
            return

        dict_list = []
        for domain_i in self.domain_list:
            dict_list.append(domain_i)
            for weak in self.weak_password:
                dict_list.append(domain_i + weak)
                dict_list.append(weak + domain_i)

        self.write_dict(dict_list)

    def mail_and_weak(self):
        """邮箱与弱口令 / Email with weak passwords"""
        if not hasattr(self, 'mail_list'):
            return

        dict_list = []
        for mail_i in self.mail_list:
            dict_list.append(mail_i)
            for weak in self.weak_password:
                dict_list.append(mail_i + weak)
                dict_list.append(weak + mail_i)

        self.write_dict(dict_list)

    def name_and_domain(self):
        """域名与姓名结合 / Domain and name combinations"""
        if not (self.name_combinations and hasattr(self, 'domain_list')):
            return

        dict_list = []
        for domain_i in self.domain_list:
            for name_combo in self.name_combinations:
                dict_list.extend([name_combo + domain_i, domain_i + name_combo])

        self.write_dict(dict_list)

    def birthday_and_weak(self):
        """生日与弱口令字段组合 / Birthday with weak password combinations"""
        if not self.birthday:
            return

        dict_list = []

        for birth in self.birthday_list:
            dict_list.append(birth)
            for weak in self.weak_password:
                dict_list.append(birth + weak)
                dict_list.append(weak + birth)

        self.write_dict(dict_list)

    def name_and_birthday(self):
        """名称与生日组合 - 保持兼容性 / Name and birthday combinations - Keep compatibility"""
        if not (self.name and self.birthday):
            return

        dict_list = []
        full_name = ''.join(self.name_pinyin_list) if self.name_pinyin_list else self.name

        for birth in self.birthday_list:
            dict_list.append(full_name + birth)
            dict_list.append(birth + full_name)

            if self.name_ab:
                for i in self.name_ab:
                    if len(i) >= 2:  # 确保名字缩写至少2位 / Ensure name abbreviation is at least 2 characters
                        dict_list.append(i + birth)
                        dict_list.append(birth + i)

        self.write_dict(dict_list)

    def id_card_and_weak(self):
        """身份证与弱口令 / ID card with weak passwords"""
        if not self.id_card:
            return

        dict_list = []
        # 只保留长度符合要求的身份证片段 / Only keep ID card segments with valid length
        id_segments = [self.id_card[12:], self.id_card[-4:], self.id_card[-6:]]
        valid_segments = [seg for seg in id_segments if self.is_valid_length(seg)]

        dict_list.extend(valid_segments)

        for weak in self.weak_password:
            for seg in valid_segments:
                dict_list.append(seg + weak)
                dict_list.append(weak + seg)

        self.write_dict(dict_list)

    def id_card_and_name(self):
        """身份证与名称组合 / ID card and name combinations"""
        if not (self.id_card and self.name_combinations):
            return

        dict_list = []
        id_suffix = self.id_card[14:]

        for name_combo in self.name_combinations:
            dict_list.extend([name_combo + id_suffix, id_suffix + name_combo])

        self.write_dict(dict_list)

    def phone_number_and_weak(self):
        """手机号与弱口令组合 / Phone number with weak password combinations"""
        if not self.phone_number:
            return

        dict_list = []
        phone_parts = [self.phone_number, self.phone_number[3:], self.phone_number[7:]]

        for phone_part in phone_parts:
            dict_list.append(phone_part)
            for weak in self.weak_password:
                dict_list.append(phone_part + weak)
                dict_list.append(weak + phone_part)

        self.write_dict(dict_list)

    def phone_number_and_name(self):
        """手机号与名称组合 / Phone number and name combinations"""
        if not (self.phone_number and self.name_combinations):
            return

        dict_list = []
        phone_number_list = [self.phone_number, self.phone_number[7:], self.phone_number[3:]]

        for phone_part in phone_number_list:
            for name_combo in self.name_combinations:
                dict_list.extend([phone_part + name_combo, name_combo + phone_part])

        self.write_dict(dict_list)

    def user_id_and_weak(self):
        """用户ID与弱口令 / User ID with weak passwords"""
        if not self.user_id:
            return

        dict_list = []
        dict_list.append(self.user_id)

        for weak in self.weak_password:
            dict_list.append(self.user_id + weak)
            dict_list.append(weak + self.user_id)

        for number_list in [self.number_value_1, self.number_value_2,
                            self.number_value_3, self.number_value_4]:
            for number in number_list:
                dict_list.append(self.user_id + number)
                dict_list.append(number + self.user_id)

        self.write_dict(dict_list)

    def user_id_and_name(self):
        """用户ID与姓名组合 / User ID and name combinations"""
        if not (self.user_id and self.name_combinations):
            return

        dict_list = []

        for name_combo in self.name_combinations:
            dict_list.extend([name_combo + self.user_id, self.user_id + name_combo])

        for weak in self.weak_password:
            for name_combo in self.name_combinations:
                dict_list.append(name_combo + self.user_id + weak)

        self.write_dict(dict_list)

    def qq_and_weak(self):
        """QQ和弱密码组合 / QQ and weak password combinations"""
        if not self.qq_number:
            return

        dict_list = []
        dict_list.append(self.qq_number)

        for weak in self.weak_password:
            dict_list.append(self.qq_number + weak)
            dict_list.append(weak + self.qq_number)

        self.write_dict(dict_list)

    def qq_and_name(self):
        """名称与QQ组合 / Name and QQ combinations"""
        if not (self.qq_number and self.name_combinations):
            return

        dict_list = []

        for name_combo in self.name_combinations:
            dict_list.extend([name_combo + self.qq_number, self.qq_number + name_combo])

        for weak in self.weak_password:
            for name_combo in self.name_combinations:
                dict_list.append(name_combo + self.qq_number + weak)

        self.write_dict(dict_list)

    def generate_dict(self):
        """生成字典 / Generate dictionary"""
        # 获取文件名 / Get filename
        while not self.filename:
            self.filename = input(
                '请输入保存字典的文件名 (如: dict.txt) / Please enter filename to save dictionary (e.g., dict.txt): ').strip()
            if not self.filename:
                print("文件名不能为空！/ Filename cannot be empty!")

        # 检查文件是否存在 / Check if file exists
        if os.path.exists(self.filename):
            choice = input(
                f"文件 {self.filename} 已存在，是否覆盖？(y/n) / File {self.filename} already exists, overwrite? (y/n): ").lower()
            if choice != 'y':
                self.filename = None
                return self.generate_dict()

        # 清空文件 / Clear file
        with open(self.filename, "w", encoding='utf-8') as f:
            pass

        print(f"开始生成字典，保存到文件 / Starting dictionary generation, saving to file: {self.filename}")
        print(
            f"密码长度限制: {self.min_length}-{self.max_length} 位 / Password length limit: {self.min_length}-{self.max_length} characters")

        # 优先处理姓名相关的组合（放在前面） / Priority processing of name-related combinations (put at the front)
        if self.name:
            print("生成姓名相关密码... / Generating name-related passwords...")
            self.name_and_weak()

            if self.birthday:
                print("生成姓名+生日组合... / Generating name+birthday combinations...")
                self.name_and_birthday_enhanced()  # 使用增强版 / Use enhanced version
                self.name_and_birthday()  # 保持兼容性 / Keep compatibility

            if self.phone_number:
                print("生成姓名+手机号组合... / Generating name+phone combinations...")
                self.phone_number_and_name()

            if hasattr(self, 'domain_list'):
                print("生成姓名+域名组合... / Generating name+domain combinations...")
                self.name_and_domain()

            if self.id_card:
                print("生成姓名+身份证组合... / Generating name+ID card combinations...")
                self.id_card_and_name()

            if self.user_id:
                print("生成姓名+用户ID组合... / Generating name+user ID combinations...")
                self.user_id_and_name()

            if self.qq_number:
                print("生成姓名+QQ组合... / Generating name+QQ combinations...")
                self.qq_and_name()

        # 其他组合 / Other combinations
        if self.birthday:
            print("生成生日相关密码... / Generating birthday-related passwords...")
            self.birthday_and_weak()

        if self.id_card:
            print("生成身份证相关密码... / Generating ID card-related passwords...")
            self.id_card_and_weak()

        if self.phone_number:
            print("生成手机号相关密码... / Generating phone-related passwords...")
            self.phone_number_and_weak()

        if hasattr(self, 'domain_list'):
            print("生成域名相关密码... / Generating domain-related passwords...")
            self.domain_and_weak()

        if hasattr(self, 'mail_list'):
            print("生成邮箱相关密码... / Generating email-related passwords...")
            self.mail_and_weak()

        if self.user_id:
            print("生成用户ID相关密码... / Generating user ID-related passwords...")
            self.user_id_and_weak()

        if self.qq_number:
            print("生成QQ相关密码... / Generating QQ-related passwords...")
            self.qq_and_weak()

        # 去重和排序 / Remove duplicates and sort
        print("正在去重和排序... / Removing duplicates and sorting...")
        self.remove_duplicates()

        print(f"字典生成完成！文件保存为 / Dictionary generation completed! File saved as: {self.filename}")

        # 显示统计信息 / Display statistics
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                print(f"共生成 {len(lines)} 个密码组合 / Generated {len(lines)} password combinations")
                print(
                    f"所有密码长度均在 {self.min_length}-{self.max_length} 位之间 / All passwords are {self.min_length}-{self.max_length} characters long")

                # 显示一些示例 / Show some examples
                print("\n密码示例（前10个） / Password examples (first 10):")
                for i, line in enumerate(lines[:10]):
                    print(f"  {i + 1}. {line.strip()} (长度: {len(line.strip())})")

        except Exception as e:
            print(f"无法读取生成的文件 / Cannot read generated file: {e}")

    def remove_duplicates(self):
        """去除重复项并按长度和字母顺序排序 / Remove duplicates and sort by length and alphabetical order"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # 去重并再次验证长度 / Remove duplicates and verify length again
            unique_lines = []
            seen = set()
            for line in lines:
                password = line.strip()
                if password and self.is_valid_length(password) and password not in seen:
                    unique_lines.append(password)
                    seen.add(password)

            # 排序：先按长度，再按字母顺序 / Sort: first by length, then alphabetically
            unique_lines.sort(key=lambda x: (len(x), x.lower()))

            with open(self.filename, 'w', encoding='utf-8') as f:
                for line in unique_lines:
                    f.write(line + '\n')

        except Exception as e:
            print(f"去重时发生错误 / Error during deduplication: {e}")

    def run(self):
        """主运行函数 / Main run function"""
        try:
            self.parse_args()

            # 检查是否有输入参数 / Check if any parameters are provided
            if not any([self.name, self.birthday, self.id_card, self.mail,
                        self.domain, self.phone_number, self.qq_number, self.user_id]):
                print("错误: 请至少提供一个参数 / Error: Please provide at least one parameter")
                usage()
                sys.exit(1)

            # 处理各种信息 / Process various information
            self.process_name()
            self.process_birthday()
            self.process_domain()
            self.process_mail()

            # 生成字典 / Generate dictionary
            self.generate_dict()

        except Exception as e:
            print(f"错误 / Error: {e}")
            sys.exit(1)


if __name__ == "__main__":
    print("密码字典生成器 / Password Dictionary Generator")
    print("仅用于教育和授权的安全测试目的 / For educational and authorized security testing purposes only")
    print("请确保在使用此工具前获得适当的授权 / Please ensure you have proper authorization before using this tool")
    print("密码长度限制: 6-18位 / Password length limit: 6-18 characters")
    print("-" * 80)

    generator = DictGenerator()
    generator.run()
