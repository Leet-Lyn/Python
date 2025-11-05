# 请帮我写个中文的 Python 脚本，批注也是中文：
# 询问我想要做什么：
# 1. 根据文件夹生成 excel 文件：在脚本开始前询问我源文件夹位置（默认为：e:\\Documents\\Creations\\Databases\\标准\\）。在其父文件夹中生成同名 xlsx 格式文件。第一行为字段名。第二行开始为数据内容，依次读取源文件夹位置内每一个 markdown 文件（markdown 格式文件，数据以 yaml 属性格式呈现如上文），将 markdown 中"---"包绕的属性根据每一字段名写入 xlsx 格式文件。写入 xlsx 文件中，每一行对应一个文件。
# 2. 根据 excel 文件生成相应 markdown 文件：在脚本开始前询问我源 excel  文件位置（默认为：e:\\Documents\\Creations\\Databases\\标准.xlsx）。在其父文件夹中生成同名文件夹。将字段名字设置为 markdown 文件名。每一行生成一个文件，并依次写入相应的 yaml 属性呈现如上文，在 markdown 中用"---"包绕。
# 3. CSV 生成文件：在脚本开始前询问我源 CSV 文件位置（默认为：d:\\Downloads\\CSV.csv）与目标文件夹位置（默认为：e:\\Documents\\Creations\\Databases\\）。这个 CSV 格式，第一行为所有字段名，字段名用""包绕。不同字段名之间用,隔开。第二行开始每一以"开头的为每一条记录。每一个""包绕的为相应的字段数据（可包含数行）为每一条字段。独立的一条记录和字段内多行区别在于行首有无"。每一记录内字段名与字段内容一一对应。请生成每一条记录（markdown 格式 文件，数据以 yaml 属性格式呈现如上文，markdown 文件名为字段"名字"对应字段内容，）。在目标文件夹下生成子文件夹，子文件夹名为CSV格式的文件名（不包括后缀名），将生成的记录放在该子文件夹下。生成的文件名为字段"名字"对应字段内容，当字段"名字"对应字段内容出现不能成为文件名的内容如半角冒号":"，请用空格破折号空格" -"代替。其他的如半角问号"?"、半角反斜杠"\"、正斜杠"/"，用全角问号"？"、全角反斜杠"＼"、正斜杠"／"代替。半角双引号"""用半角波浪号"~"代替。竖线"|"用反单引号"`"代替。星号"*"用乘号"×"代替。<（小于）、>（大于）用书名号"《 》"代替。
# 4. 删除字段：在脚本开始前询问我源文件夹位置，文件夹内储存着上述结构的数据（默认为：e:\\Documents\\Creations\\Databases\\）。询问我需要删除某一字段名。遍历源文件夹位置中所有的文件及子文件夹内文件（md 格式），读取每一文件，找到这个字段后删除该字段即其配套的字段内容。
# 5. 添加字段：在脚本开始前询问我源文件夹位置，文件夹内储存着上述结构的数据（默认为：e:\\Documents\\Creations\\Databases\\）。询问我需要添加某一字段名，及添加在哪一个字段前。遍历源文件夹位置中所有的文件及子文件夹内文件（md 格式），读取每一文件，找到这个字段，在这行之前，添加要求的字段。
# 6. 查找与替换：在脚本开始前询问我源文件夹位置，文件夹内储存着上述结构的数据（默认为：e:\\Documents\\Creations\\Databases\\）。依次在屏幕中询问我查找内容及替换内容。遍历源文件夹位置中所有的文件及子文件夹内文件（md 格式），读取每一文件，找到存放查找内容，用替换内容进行替换。
# 7. 查找与替换（正则表达式）：在脚本开始前询问我源文件夹位置，文件夹内储存着上述结构的数据（默认为：e:\\Documents\\Creations\\Databases\\）。询问我存放查找内容的正则表达式文本位置（默认为：e:\\Documents\\Creations\\Scripts\\Python\\DatabaseRegexFind.txt）与存放替换内容的文本位置（默认为：e:\\Documents\\Creations\\Scripts\\Python\\DatabaseRegexReplace.txt）。遍历源文件夹位置中所有的文件及子文件夹内文件（md 格式），读取每一文件，找到存放查找内容，用替换内容进行替换。
# 8. 元替换：在脚本开始前询问我源文件夹位置，文件夹内储存着上述结构的数据（默认为：e:\\Documents\\Creations\\Databases\\）。遍历源文件夹位置中所有的文件及子文件夹内文件（md 格式），读取每一文件，将文件里的元数据标实替换 md 文件的元数据。（比如[FileName]表示全文件名，[BaseName]表示不含扩展名的文件名，[Extension]表示扩展名，[FolderName]表示父文件夹名，[FolderPath]表示父文件夹路径，[FilePath]表示文件路径，[DateCreated]表示文件生成日期时间，[DateModified]表示文件修改日期时间，[DateAccessed]表示文件修改时间，[Size]表示文件大小（适配 B、KB、MB、GB 形式，并精确到小数点后 4 位），[SizeBytes]表示文件大小（Bytes）。
# 9. 生成数据结构文件：在脚本开始前询问我源文件夹位置，文件夹内储存着上述结构的数据（默认为：e:\\Documents\\Creations\\Databases\\）。在该文件夹下生成一个 md 文件，文件名为".DatabaseStructure.md"。读取该文件夹中的其他每一文件（排除 ".DatabaseStructure.md"），将第一个文件里每一个的字段名，依次写入".DatabaseStructure.md"中。字段名后接一个半角冒号和空格（": "），在此之后，写着这个字段的字段类型（文本、数值、布尔、日期、时间、日期时间、列表），每一行一个字段。这些字段名首尾由一组三个破折号（"---"）分隔符包围。此后依次读取每一个文件，如文件里的字段名已经被".DatabaseStructure.md"记录，则不做处理；如文件里的字段名未被".DatabaseStructure.md"记录，则添加该字段。
# 10. 结构化数据文件：在脚本开始前询问我源文件夹位置，文件夹内储存着上述结构的数据（默认为：e:\\Documents\\Creations\\Databases\\）。读取该文件夹下的".DatabaseStructure.md"。这个就是后续文件的字段的数据结构。依次读取该文件夹中的其他每一文件（排除 ".DatabaseStructure.md"），将它的字段按照".DatabaseStructure.md"中字段名顺序重新排序；如果".DatabaseStructure.md"里的某一字段名有，而该文件中没有，就按顺序添加到该文件中；如果该文件有，而".DatabaseStructure.md"里没有的字段名，就删除该字段及其数据。
# 11. 删除没有数据的字段名：在脚本开始前询问我源文件夹位置，文件夹内储存着上述结构的数据（默认为：e:\\Documents\\Creations\\Databases\\）。依次读取该文件夹中的其他每一文件（排除 ".DatabaseStructure.md"）。删除没有数据的字段行。
# 12. 双引号置换单引号：在脚本开始前询问我源文件夹位置，文件夹内储存着上述结构的数据（默认为：e:\\Documents\\Creations\\Databases\\标准\\）。打开每个 markdown 文件，顺序读取文件，将每一行中除了第一个和倒数第一个双引号（"），其他的双引号改为单引号（'）。
# 13. 属性内容处理：在脚本开始前询问我源文件夹位置，文件夹内储存着上述结构的数据（默认为：e:\\Documents\\Creations\\Databases\\标准\\），再询问我属性名称。打开每个 markdown 文件，顺序找到该属性。询问我下一步：1.将该属性内容设置为空（""）。2.将该属性内容设置为什么？（询问我属性内容，所有 markdown 文件的属性均设置为该属性内容）。3. 将该属性内容每个单词大写。4.将该属性内容每个单词小写。5. 将该属性内容每个单词首字母大写，其余小写。6.将该属性内容（汉字、英文、或数字）用空格隔开。7.将该属性内容的汉字繁体中文转为简体中文。8. 所有半角标点符号转为全角标点符号。
# 14.写入 excel 文件：在脚本开始前询问我 excel 文件位置（默认为：e:\\Documents\\Creations\\Databases\\标准.xlsx）与源文件夹位置（默认为：d:\\Downloads\\）。读取 excel 文件，第一行为表头（字段名）。此后每一行为一条记录。分别询问我“引用页”、“属于”、“主链接”的值（按回车则为空）。遍历源文件夹内所有文件及子文件夹中的文件，顺序完成。1. 每一条记录新开一行。2. “Index”字段值为上一行 “Index”字段值+1（如上一行为空或为表头，则“Index”字段值为 1）。3. 将源文件夹内文件名写入“名字”与“原文件名”字段值。4. 将该文件复制到“d:\\Works\\In\\”与“z:\\”中，如果无法完成写入“z:\\”中，则提示我，并退出。写入“z:\\”后，系统会自动生成一个对应文件（自动加密的）。读取“d:\\Xyz\\”新生成的文件名，将其文件名（包括扩展名）写入“加密文件名”字段值。将“d:\\Xyz\\”新生成的文件移动到“d:\\Works\\Uploads\\”（在“d:\\Xyz\\”中不保留）。5. 将原来询问我的“引用页”、“属于”、“主链接”的值写入“引用页”、“属于”、“主链接”字段值。6. 计算并生成该文件的 Ed2K 链接。我安装了 RHash，位置“d:\\ProApps\\RHash\\hash.exe”。生成 ed2k 的命令类似：rhash.exe --uppercase --ed2k-link "\\TS-464C\Temps\rustdesk-1.4.3-x86_64.exe"。生成如“ed2k://|file|rustdesk-1.4.3-x86_64.exe|23369352|DF952EEB0438E288409858E6C960E261|h=T7BJKLDRQ7VDCDKOO525FO7YHJCZVKDK|/” 的 ed2k 链接，写入“标准链接”字段值。7. 通过“标准链接”字段值，分别生成“大小”、“散列”字段值。大小请转成 B、KB、MB、GB 形式，并精确到小数点后 4 位，hash 转全部大写。
# 0. 退出程序。

# 请帮我写个中文的 Python 脚本，批注也是中文：
# 询问我想要做什么：
# 1. 根据文件夹生成 excel 文件：在脚本开始前询问我源文件夹位置（默认为：e:\\Documents\\Creations\\Databases\\标准\\）。在其父文件夹中生成同名 xlsx 格式文件。第一行为字段名。第二行开始为数据内容，依次读取源文件夹位置内每一个 markdown 文件（markdown 格式文件，数据以 yaml 属性格式呈现如上文），将 markdown 中"---"包绕的属性根据每一字段名写入 xlsx 格式文件。写入 xlsx 文件中，每一行对应一个文件。
# 2. 根据 excel 文件生成相应 markdown 文件：在脚本开始前询问我源 xlsx 文件位置（默认为：e:\\Documents\\Creations\\Databases\\标准.xlsx）。在其父文件夹中生成同名文件夹。将字段名字设置为 markdown 文件名。每一行生成一个文件，并依次写入相应的 yaml 属性呈现如上文，在 markdown 中用"---"包绕。
# 3. CSV 生成文件：在脚本开始前询问我源 CSV 文件位置（默认为：d:\\Downloads\\CSV.csv）与目标文件夹位置（默认为：e:\\Documents\\Creations\\Databases\\）。这个 CSV 格式，第一行为所有字段名，字段名用""包绕。不同字段名之间用,隔开。第二行开始每一以"开头的为每一条记录。每一个""包绕的为相应的字段数据（可包含数行）为每一条字段。独立的一条记录和字段内多行区别在于行首有无"。每一记录内字段名与字段内容一一对应。请生成每一条记录（markdown 格式 文件，数据以 yaml 属性格式呈现如上文，markdown 文件名为字段"名字"对应字段内容，）。在目标文件夹下生成子文件夹，子文件夹名为CSV格式的文件名（不包括后缀名），将生成的记录放在该子文件夹下。生成的文件名为字段"名字"对应字段内容，当字段"名字"对应字段内容出现不能成为文件名的内容如半角冒号":"，请用空格破折号空格" -"代替。其他的如半角问号"?"、半角反斜杠"\"、正斜杠"/"，用全角问号"？"、全角反斜杠"＼"、正斜杠"／"代替。半角双引号"""用半角波浪号"~"代替。竖线"|"用反单引号"`"代替。星号"*"用乘号"×"代替。<（小于）、>（大于）用书名号"《 》"代替。
# 4. 删除字段：在脚本开始前询问我源文件夹位置，文件夹内储存着上述结构的数据（默认为：e:\\Documents\\Creations\\Databases\\）。询问我需要删除某一字段名。遍历源文件夹位置中所有的文件及子文件夹内文件（md 格式），读取每一文件，找到这个字段后删除该字段即其配套的字段内容。
# 5. 添加字段：在脚本开始前询问我源文件夹位置，文件夹内储存着上述结构的数据（默认为：e:\\Documents\\Creations\\Databases\\）。询问我需要添加某一字段名，及添加在哪一个字段前。遍历源文件夹位置中所有的文件及子文件夹内文件（md 格式），读取每一文件，找到这个字段，在这行之前，添加要求的字段。
# 6. 查找与替换：在脚本开始前询问我源文件夹位置，文件夹内储存着上述结构的数据（默认为：e:\\Documents\\Creations\\Databases\\）。依次在屏幕中询问我查找内容及替换内容。遍历源文件夹位置中所有的文件及子文件夹内文件（md 格式），读取每一文件，找到存放查找内容，用替换内容进行替换。
# 7. 查找与替换（正则表达式）：在脚本开始前询问我源文件夹位置，文件夹内储存着上述结构的数据（默认为：e:\\Documents\\Creations\\Databases\\）。询问我存放查找内容的正则表达式文本位置（默认为：e:\\Documents\\Creations\\Scripts\\Python\\DatabaseRegexFind.txt）与存放替换内容的文本位置（默认为：e:\\Documents\\Creations\\Scripts\\Python\\DatabaseRegexReplace.txt）。遍历源文件夹位置中所有的文件及子文件夹内文件（md 格式），读取每一文件，找到存放查找内容，用替换内容进行替换。
# 8. 元替换：在脚本开始前询问我源文件夹位置，文件夹内储存着上述结构的数据（默认为：e:\\Documents\\Creations\\Databases\\）。遍历源文件夹位置中所有的文件及子文件夹内文件（md 格式），读取每一文件，将文件里的元数据标实替换 md 文件的元数据。（比如[FileName]表示全文件名，[BaseName]表示不含扩展名的文件名，[Extension]表示扩展名，[FolderName]表示父文件夹名，[FolderPath]表示父文件夹路径，[FilePath]表示文件路径，[DateCreated]表示文件生成日期时间，[DateModified]表示文件修改日期时间，[DateAccessed]表示文件修改时间，[Size]表示文件大小（适配 B、KB、MB、GB 形式，并精确到小数点后 4 位），[SizeBytes]表示文件大小（Bytes）。
# 9. 生成数据结构文件：在脚本开始前询问我源文件夹位置，文件夹内储存着上述结构的数据（默认为：e:\\Documents\\Creations\\Databases\\）。在该文件夹下生成一个 md 文件，文件名为".DatabaseStructure.md"。读取该文件夹中的其他每一文件（排除 ".DatabaseStructure.md"），将第一个文件里每一个的字段名，依次写入".DatabaseStructure.md"中。字段名后接一个半角冒号和空格（": "），在此之后，写着这个字段的字段类型（文本、数值、布尔、日期、时间、日期时间、列表），每一行一个字段。这些字段名首尾由一组三个破折号（"---"）分隔符包围。此后依次读取每一个文件，如文件里的字段名已经被".DatabaseStructure.md"记录，则不做处理；如文件里的字段名未被".DatabaseStructure.md"记录，则添加该字段。
# 10. 结构化数据文件：在脚本开始前询问我源文件夹位置，文件夹内储存着上述结构的数据（默认为：e:\\Documents\\Creations\\Databases\\）。读取该文件夹下的".DatabaseStructure.md"。这个就是后续文件的字段的数据结构。依次读取该文件夹中的其他每一文件（排除 ".DatabaseStructure.md"），将它的字段按照".DatabaseStructure.md"中字段名顺序重新排序；如果".DatabaseStructure.md"里的某一字段名有，而该文件中没有，就按顺序添加到该文件中；如果该文件有，而".DatabaseStructure.md"里没有的字段名，就删除该字段及其数据。
# 11. 删除没有数据的字段名：在脚本开始前询问我源文件夹位置，文件夹内储存着上述结构的数据（默认为：e:\\Documents\\Creations\\Databases\\）。依次读取该文件夹中的其他每一文件（排除 ".DatabaseStructure.md"）。删除没有数据的字段行。
# 12. 双引号置换单引号：在脚本开始前询问我源文件夹位置，文件夹内储存着上述结构的数据（默认为：e:\\Documents\\Creations\\Databases\\标准\\）。打开每个 markdown 文件，顺序读取文件，将每一行中除了第一个和倒数第一个双引号（"），其他的双引号改为单引号（'）。
# 13. 属性内容处理：在脚本开始前询问我源文件夹位置，文件夹内储存着上述结构的数据（默认为：e:\\Documents\\Creations\\Databases\\标准\\），再询问我属性名称。打开每个 markdown 文件，顺序找到该属性。询问我下一步：1.将该属性内容设置为空（""）。2.将该属性内容设置为什么？（询问我属性内容，所有 markdown 文件的属性均设置为该属性内容）。3. 将该属性内容每个单词大写。4.将该属性内容每个单词小写。5. 将该属性内容每个单词首字母大写，其余小写。6.将该属性内容（汉字、英文、或数字）用空格隔开。7.将该属性内容的汉字繁体中文转为简体中文。8. 所有半角标点符号转为全角标点符号。
# 14. 写入 excel 文件：在脚本开始前询问我 excel 文件位置（默认为：e:\\Documents\\Creations\\Databases\\标准.xlsx）与源文件夹位置（默认为：d:\\Downloads\\）。读取 excel 文件，第一行为表头（字段名）。此后每一行为一条记录。分别询问我"引用页"、"属于"、"主链接"的值（按回车则为空）。遍历源文件夹内所有文件及子文件夹中的文件，顺序完成。1. 每一条记录新开一行。2. "Index"字段值为上一行 "Index"字段值+1（如上一行为空或为表头，则"Index"字段值为 1）。3. 将源文件夹内文件名写入"名字"与"原文件名"字段值。4. 将该文件复制到"d:\\Works\\In\\"与"z:\\"中，如果无法完成写入"z:\\"中，则提示我，并退出。写入"z:\\"后，系统会自动生成一个对应文件（自动加密的）。读取"d:\\Xyz\\"新生成的文件名，将其文件名（包括扩展名）写入"加密文件名"字段值。将"d:\\Xyz\\"新生成的文件移动到"d:\\Works\\Uploads\\"（在"d:\\Xyz\\"中不保留）。5. 将原来询问我的"引用页"、"属于"、"主链接"的值写入"引用页"、"属于"、"主链接"字段值。6. 计算并生成该文件的 Ed2K 链接。我安装了 RHash，位置"d:\\ProApps\\RHash\\hash.exe"。生成 ed2k 的命令类似：rhash.exe --uppercase --ed2k-link "\\TS-464C\Temps\rustdesk-1.4.3-x86_64.exe"。生成如"ed2k://|file|rustdesk-1.4.3-x86_64.exe|23369352|DF952EEB0438E288409858E6C960E261|h=T7BJKLDRQ7VDCDKOO525FO7YHJCZVKDK|/" 的 ed2k 链接，写入"标准链接"字段值。7. 通过"标准链接"字段值，分别生成"大小"、"散列"字段值。大小请转成 B、KB、MB、GB 形式，并精确到小数点后 4 位，hash 转全部大写。
# 0. 退出程序。

# 导入模块
import os
import csv
import re
import shutil
from pathlib import Path
import yaml
import datetime
import time
import pandas as pd
from collections import OrderedDict
import urllib.parse  # 用于处理百分号编码
import subprocess    # 用于调用外部程序

# 尝试导入zhconv用于简繁转换，如果没有安装则跳过
try:
    import zhconv
    ZHCONV_AVAILABLE = True
except ImportError:
    ZHCONV_AVAILABLE = False

def sanitize_filename(name):
    """净化文件名中的特殊字符"""
    replacements = {
        ':': ' -',    # 冒号替换为空格破折号空格
        '?': '？',     # 半角问号转全角
        '\\': '＼',    # 半角反斜杠转全角
        '/': '／',     # 正斜杠转全角
        '"': '~',      # 双引号替换为波浪号
        '|': '`',      # 竖线替换为反单引号
        '*': '×',     # 星号替换为乘号
        '<': '《',     # 小于号替换为左书名号
        '>': '》',     # 大于号替换为右书名号
    }
    
    # 按顺序替换特殊字符
    for char, replacement in replacements.items():
        name = name.replace(char, replacement)
    
    # 移除首尾空白
    return name.strip()

def get_default_path(prompt, default):
    """获取带默认值的路径输入"""
    path = input(f"{prompt} (默认：{default}): ").strip()
    return path if path else default

def ensure_dir(path):
    """确保目录存在"""
    if not os.path.exists(path):
        os.makedirs(path)

def escape_yaml_value(value):
    """转义YAML值，确保特殊字符被正确处理 - 修改版：所有值都用双引号包绕"""
    if value is None:
        return '""'
    
    value_str = str(value)
    
    # 所有情况都用双引号包裹，包括数字
    return f'"{value_str}"'

def extract_yaml_block(content):
    """从文件内容中提取YAML块"""
    match = re.search(r'^---\n(.*?)\n---', content, flags=re.DOTALL)
    return match.group(1) if match else ""

def infer_field_type(value):
    """根据字段值推断字段类型 - 空值默认为文本"""
    if value is None:
        return "文本"  # 空值默认为文本
    
    if isinstance(value, bool):
        return "布尔"
    
    if isinstance(value, (int, float)):
        return "数值"
    
    if isinstance(value, list):
        return "列表"
    
    if isinstance(value, datetime.datetime):
        return "日期时间"
    
    if isinstance(value, datetime.date):
        return "日期"
    
    if isinstance(value, datetime.time):
        return "时间"
    
    # 尝试解析日期时间格式
    if isinstance(value, str):
        try:
            datetime.datetime.fromisoformat(value)
            return "日期时间"
        except ValueError:
            pass
        
        try:
            datetime.date.fromisoformat(value)
            return "日期"
        except ValueError:
            pass
        
        try:
            datetime.time.fromisoformat(value)
            return "时间"
        except ValueError:
            pass
        
        # 检查布尔字符串
        if value.lower() in ["true", "false"]:
            return "布尔"
        
        # 检查数值字符串
        if re.match(r"^[-+]?\d+$", value):
            return "数值"
        if re.match(r"^[-+]?\d*\.\d+$", value):
            return "数值"
    
    return "文本"

def format_file_size(size_bytes):
    """格式化文件大小为适配单位（B, KB, MB, GB）并保留4位小数"""
    units = ["B", "KB", "MB", "GB"]
    unit_index = 0
    size = float(size_bytes)
    
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024.0
        unit_index += 1
    
    # 保留4位小数
    if unit_index == 0:  # 字节
        return f"{size_bytes} B"
    else:
        return f"{size:.4f} {units[unit_index]}"

def main():
    while True:  # 添加循环，使程序能持续运行
        print("\n" + "="*50)
        print("请选择操作：")
        print("1. 根据文件夹生成Excel文件")
        print("2. 根据Excel生成Markdown文件夹")
        print("3. 从 CSV 生成 Markdown 文件")
        print("4. 删除字段")
        print("5. 添加字段")
        print("6. 查找与替换（普通）")
        print("7. 查找与替换（正则表达式）")
        print("8. 元替换")
        print("9. 生成数据结构文件")
        print("10. 结构化数据文件")
        print("11. 删除没有数据的字段名")
        print("12. 双引号置换单引号")
        print("13. 属性内容处理")
        print("14. 写入Excel文件（含ED2K链接生成）")
        print("0. 退出程序")
        choice = input("请输入数字选择操作（1/2/3/4/5/6/7/8/9/10/11/12/13/14/0）：")
        
        if choice == '1':
            generate_excel_from_folder()
        elif choice == '2':
            generate_markdown_from_excel()
        elif choice == '3':
            generate_from_csv()
        elif choice == '4':
            delete_field()
        elif choice == '5':
            add_field()
        elif choice == '6':
            find_and_replace()
        elif choice == '7':
            find_and_replace_regex()
        elif choice == '8':
            meta_replacement()
        elif choice == '9':
            generate_structure_file()
        elif choice == '10':
            restructure_files()
        elif choice == '11':
            delete_empty_fields()
        elif choice == '12':
            replace_double_quotes()
        elif choice == '13':
            process_attribute_content()
        elif choice == '14':
            write_to_excel_with_ed2k()
        elif choice == '0':
            print("程序已退出")
            break
        else:
            print("无效选择，请重新输入")

# 选项1：根据文件夹生成Excel文件 - 修改版：增量更新
def generate_excel_from_folder():
    """从文件夹生成Excel文件 - 增量更新模式"""
    # 获取源文件夹位置
    source_dir = get_default_path("请输入源文件夹位置", "e:\\Documents\\Creations\\Databases\\标准\\")
    
    # 检查文件夹是否存在
    if not os.path.exists(source_dir):
        print(f"错误：文件夹 '{source_dir}' 不存在")
        return
    
    # 确定输出Excel文件路径（在源文件夹的父文件夹中，与源文件夹同名）
    parent_dir = os.path.dirname(source_dir.rstrip(os.sep))
    folder_name = os.path.basename(source_dir.rstrip(os.sep))
    output_path = os.path.join(parent_dir, f"{folder_name}.xlsx")
    
    print(f"Excel文件位置: {output_path}")
    
    # 收集所有记录和字段名
    all_records = []
    field_order = OrderedDict()  # 使用有序字典记录字段顺序
    
    # 遍历源文件夹中的所有markdown文件
    for root, _, files in os.walk(source_dir):
        # 对文件进行排序，确保处理顺序一致
        files.sort()
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                record, fields_in_file = parse_markdown_yaml(filepath)
                
                if record:
                    # 获取文件名（不含扩展名）并处理" - "到": "的转换
                    base_filename = os.path.splitext(file)[0]
                    processed_name = base_filename.replace(" - ", ": ")
                    
                    # 确保记录中有"名字"字段，使用处理后的文件名
                    record['名字'] = processed_name
                    
                    # 添加原始文件名作为字段
                    record['文件名'] = file
                    
                    # 记录字段顺序（只记录第一次出现的顺序）
                    for field in fields_in_file:
                        if field not in field_order:
                            field_order[field] = True
                    
                    # 确保"名字"和"文件名"字段在字段顺序中
                    if '名字' not in field_order:
                        field_order['名字'] = True
                    if '文件名' not in field_order:
                        field_order['文件名'] = True
                    
                    all_records.append(record)
    
    if not all_records:
        print("未找到任何Markdown文件或解析失败")
        return
    
    # 转换为DataFrame，保持字段顺序
    field_list = list(field_order.keys())
    data = []
    
    for record in all_records:
        row = []
        for field in field_list:
            # 确保所有值都是字符串格式
            value = record.get(field, "")
            if isinstance(value, (list, tuple)):
                # 如果是列表或元组，转换为逗号分隔的字符串
                value = ", ".join(str(item) for item in value)
            else:
                # 其他类型直接转换为字符串
                value = str(value) if value is not None else ""
            row.append(value)
        data.append(row)
    
    new_df = pd.DataFrame(data, columns=field_list)
    
    # 如果Excel文件已存在，则进行增量更新
    if os.path.exists(output_path):
        try:
            # 读取现有Excel文件
            existing_df = pd.read_excel(output_path, engine='openpyxl')
            
            # 合并新旧数据
            # 使用"名字"字段作为合并键
            if '名字' in existing_df.columns and '名字' in new_df.columns:
                # 合并数据框，保留原有数据，只更新新数据中存在的记录
                merged_df = pd.merge(existing_df, new_df, on='名字', how='outer', suffixes=('_old', '_new'))
                
                # 处理合并后的列
                final_columns = list(existing_df.columns)
                new_columns = [col for col in new_df.columns if col not in existing_df.columns]
                
                # 创建最终数据框
                final_df = existing_df.copy()
                
                # 更新现有记录
                for idx, row in new_df.iterrows():
                    name = row['名字']
                    if name in final_df['名字'].values:
                        # 更新现有记录
                        mask = final_df['名字'] == name
                        for col in new_df.columns:
                            if col != '名字':
                                final_df.loc[mask, col] = row[col]
                    else:
                        # 添加新记录
                        final_df = pd.concat([final_df, pd.DataFrame([row])], ignore_index=True)
                
                # 添加新字段
                for col in new_columns:
                    final_df[col] = new_df[col]
                
                df = final_df
                print("已增量更新现有Excel文件")
            else:
                df = new_df
                print("无法找到'名字'字段，将创建新Excel文件")
        except Exception as e:
            print(f"读取现有Excel文件失败: {e}，将创建新Excel文件")
            df = new_df
    else:
        df = new_df
        print("将创建新Excel文件")
    
    # 保存为Excel
    try:
        df.to_excel(output_path, index=False, engine='openpyxl')
        print(f"成功导出 {len(df)} 条记录到: {output_path}")
        print(f"包含字段 ({len(df.columns)} 个): {', '.join(df.columns)}")
    except Exception as e:
        print(f"导出Excel失败: {e}")
        # 尝试保存为CSV作为备选方案
        csv_path = output_path.replace('.xlsx', '.csv')
        df.to_csv(csv_path, index=False, encoding='utf-8-sig')
        print(f"已备选导出为CSV: {csv_path}")

def parse_markdown_yaml(filepath):
    """解析Markdown文件中的YAML属性块，返回记录和字段顺序"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 使用正则表达式提取YAML属性块（---之间的内容）
        yaml_pattern = r'^---\s*\n(.*?)\n---\s*$'
        match = re.search(yaml_pattern, content, re.DOTALL | re.MULTILINE)
        
        if not match:
            print(f"警告：文件 {filepath} 中未找到YAML属性块")
            return None, []
        
        yaml_content = match.group(1)
        
        # 解析YAML内容
        try:
            # 使用OrderedDict保持YAML字段顺序
            data = yaml.safe_load(yaml_content)
            
            # 确保所有值都是字符串格式
            if data:
                for key, value in data.items():
                    if isinstance(value, (list, tuple)):
                        # 如果是列表或元组，转换为逗号分隔的字符串
                        data[key] = ", ".join(str(item) for item in value)
                    else:
                        # 其他类型直接转换为字符串
                        data[key] = str(value) if value is not None else ""
            
            # 提取字段顺序
            if data:
                # 获取YAML中的字段顺序
                field_order = []
                lines = yaml_content.strip().split('\n')
                for line in lines:
                    line = line.strip()
                    if line and ':' in line and not line.startswith('#'):
                        field_name = line.split(':', 1)[0].strip()
                        if field_name in data:  # 确保字段存在于解析后的数据中
                            field_order.append(field_name)
                
                return data, field_order
            return None, []
            
        except yaml.YAMLError as e:
            print(f"解析YAML失败 {filepath}: {e}")
            return None, []
            
    except Exception as e:
        print(f"读取文件失败 {filepath}: {e}")
        return None, []

# 选项2：根据Excel生成Markdown文件夹 - 修改版：增量更新且标准化属性格式
def generate_markdown_from_excel():
    """从Excel生成Markdown文件夹 - 增量更新模式"""
    # 获取Excel文件路径
    excel_path = get_default_path("请输入Excel文件路径", "e:\\Documents\\Creations\\Databases\\标准.xlsx")
    
    # 检查文件是否存在
    if not os.path.exists(excel_path):
        print(f"错误：Excel文件 '{excel_path}' 不存在")
        return
    
    # 确定目标文件夹路径（与Excel文件同名，不含扩展名）
    parent_dir = os.path.dirname(excel_path)
    excel_name = os.path.splitext(os.path.basename(excel_path))[0]
    output_dir = os.path.join(parent_dir, excel_name)
    
    # 创建目标文件夹
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print(f"将在以下位置生成/更新Markdown文件: {output_dir}")
    
    # 读取Excel文件
    try:
        df = pd.read_excel(excel_path, engine='openpyxl')
    except Exception as e:
        print(f"读取Excel文件失败: {e}")
        return
    
    if df.empty:
        print("Excel文件为空")
        return
    
    # 获取字段名
    field_names = df.columns.tolist()
    
    # 检查是否有"名字"字段
    if "名字" not in field_names:
        print("错误：Excel文件中缺少'名字'字段，无法生成Markdown文件")
        return
    
    # 处理每一行数据
    success_count = 0
    update_count = 0
    for index, row in df.iterrows():
        # 获取文件名 - 使用"名字"字段
        name_value = row.get("名字", "")
        if not name_value or pd.isna(name_value):
            print(f"跳过第 {index+1} 行：'名字'字段为空")
            continue
        
        # 处理"名字"字段中的": "到" - "的转换
        processed_name = name_value.replace(": ", " - ")
        
        # 净化文件名
        filename = sanitize_filename(processed_name) + ".md"
        filepath = os.path.join(output_dir, filename)
        
        # 构建YAML属性字典 - 包含所有字段，包括空值字段
        yaml_data = OrderedDict()
        for field in field_names:
            value = row.get(field, "")
            
            # 处理空值 - 即使是空值也包含该属性
            if pd.isna(value) or value == "":
                # 空值表示为包含一个空字符串的列表
                yaml_data[field] = [""]
            else:
                # 处理可能的多值字段（包含半角逗号和空格的字段）
                if isinstance(value, str) and ", " in value:
                    # 使用半角逗号和空格分割为列表
                    values = [v.strip() for v in value.split(", ")]
                    # 过滤空字符串
                    values = [v for v in values if v]
                    yaml_data[field] = values
                else:
                    # 单行属性也表示为列表
                    yaml_data[field] = [str(value)]
        
        # 如果文件已存在，则合并内容
        if os.path.exists(filepath):
            try:
                # 读取现有文件内容
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 提取YAML块和文件其余部分
                match = re.search(r'(^---\n.*?\n---)(.*)', content, flags=re.DOTALL)
                if match:
                    yaml_block = match.group(1)
                    rest_content = match.group(2)
                    
                    # 解析现有YAML内容
                    existing_data = yaml.safe_load(extract_yaml_block(yaml_block))
                    
                    # 合并数据：保留原有字段，只更新新数据中存在的字段
                    if existing_data:
                        # 将现有数据转换为标准格式（所有值都是列表）
                        standardized_existing_data = OrderedDict()
                        for field, value in existing_data.items():
                            if isinstance(value, list):
                                standardized_existing_data[field] = value
                            else:
                                standardized_existing_data[field] = [str(value)]
                        
                        # 更新数据
                        for field, value in yaml_data.items():
                            standardized_existing_data[field] = value
                        
                        yaml_data = standardized_existing_data
                    
                    update_count += 1
            except Exception as e:
                print(f"读取现有文件失败 {filename}: {e}")
        
        # 生成Markdown文件
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                # 写入YAML前置内容
                f.write("---\n")
                
                # 自定义YAML输出，确保所有属性都用列表格式表示
                for field, value_list in yaml_data.items():
                    # 写入字段名
                    f.write(f"{field}:\n")
                    
                    # 处理属性值列表 - 所有值都用双引号包绕，包括空值
                    for item in value_list:
                        escaped_item = escape_yaml_value(item)
                        f.write(f"  - {escaped_item}\n")
                
                f.write("---\n")
            
            success_count += 1
            if os.path.exists(filepath) and update_count > 0:
                print(f"已更新: {filename}")
            else:
                print(f"已生成: {filename}")
        except Exception as e:
            print(f"生成文件失败 {filename}: {e}")
    
    print(f"成功处理 {success_count} 个Markdown文件到: {output_dir}")
    if update_count > 0:
        print(f"其中 {update_count} 个文件已更新")

# 选项3：从CSV生成Markdown文件
def generate_from_csv():
    """从CSV生成Markdown文件 - 修改版：所有字段内容用双引号包绕并使用列表格式"""
    # 获取用户输入路径
    csv_path = input(f"请输入 CSV 文件路径（默认：D:\\Downloads\\CSV.csv）：") or "D:\\Downloads\\CSV.csv"
    output_dir = input(f"请输入目标文件夹（默认：e:\\Documents\\Creations\\Databases\\）：") or "e:\\Documents\\Creations\\Databases\\"

    # 创建输出子文件夹
    csv_stem = Path(csv_path).stem
    output_subdir = Path(output_dir) / csv_stem
    output_subdir.mkdir(parents=True, exist_ok=True)

    # 读取CSV文件
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=',', quotechar='"')
            headers = next(reader)  # 读取首行字段名
            
            for row_idx, row in enumerate(reader, 1):
                try:
                    # 构建YAML内容
                    yaml_lines = ["---"]
                    for header, value in zip(headers, row):
                        # 所有字段都使用列表格式，并用双引号包绕
                        yaml_lines.append(f"{header}:")
                        
                        # 处理空值
                        if not value.strip():
                            yaml_lines.append('  - ""')
                        else:
                            # 分割多行内容
                            lines = value.split('\n')
                            for line in lines:
                                yaml_lines.append(f'  - "{line}"')
                    
                    yaml_lines.append("---\n")
                    
                    # 获取并净化文件名
                    name_field = next((v for h, v in zip(headers, row) if h == "名字"), None)
                    if not name_field:
                        raise ValueError(" CSV 中缺少'名字'字段")
                    
                    safe_name = sanitize_filename(name_field)
                    if not safe_name:
                        raise ValueError("文件名经净化后为空")
                    
                    # 写入文件
                    output_path = output_subdir / f"{safe_name}.md"
                    with open(output_path, 'w', encoding='utf-8') as md_file:
                        md_file.write('\n'.join(yaml_lines))
                    
                    print(f"已生成：{output_path}")
                except Exception as e:
                    print(f"处理第{row_idx}行时出错：{str(e)}")
        print("\nCSV 转换完成！")
    except Exception as e:
        print(f"处理 CSV 文件时出错：{str(e)}")

# 选项4：删除字段
def delete_field():
    """删除指定字段"""
    source_dir = input(f"请输入源文件夹（默认：e:\\Documents\\Creations\\Databases\\）：") or "e:\\Documents\\Creations\\Databases\\"
    field_name = input("请输入要删除的字段名称：")

    processed_count = 0
    # 遍历所有Markdown文件
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = Path(root) / file
                if process_delete_field(file_path, field_name):
                    processed_count += 1
    print(f"\n字段删除完成！共处理 {processed_count} 个文件")

def process_delete_field(file_path, field_name):
    """处理单个文件的字段删除"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 使用正则表达式匹配字段块
        pattern = re.compile(
            r'^(' + re.escape(field_name) + r':.*?)(?=^\S|\Z)', 
            flags=re.DOTALL|re.MULTILINE
        )
        new_content = pattern.sub('', content)

        # 删除空行并保留其他内容
        new_content = re.sub(r'\n\s*\n', '\n', new_content)
        
        # 检查内容是否有变化
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"已处理：{file_path}")
            return True
        return False
    except Exception as e:
        print(f"处理文件 {file_path} 时出错：{str(e)}")
        return False

# 选项5：添加字段
def add_field():
    """添加新字段"""
    source_dir = input(f"请输入源文件夹（默认：e:\\Documents\\Creations\\Databases\\）：") or "e:\\Documents\\Creations\\Databases\\"
    new_field = input("请输入要添加的字段名称：")
    target_field = input("请输入要插入在哪个字段之前：")

    processed_count = 0
    # 遍历所有Markdown文件
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = Path(root) / file
                if process_add_field(file_path, new_field, target_field):
                    processed_count += 1
    print(f"\n字段添加完成！共处理 {processed_count} 个文件")

def process_add_field(file_path, new_field, target_field):
    """处理单个文件的字段添加"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        try:
            yaml_start = lines.index('---\n')
            yaml_end = lines.index('---\n', yaml_start+1)
        except ValueError:
            print(f"文件 {file_path} 缺少 YAML 分隔符，跳过处理")
            return False
        
        # 查找目标字段位置
        insert_pos = -1
        for i in range(yaml_start+1, yaml_end):
            if lines[i].startswith(f"{target_field}:"):
                insert_pos = i
                break
        
        if insert_pos == -1:
            print(f"在 {file_path} 中未找到目标字段 {target_field}")
            return False

        # 插入新字段
        lines.insert(insert_pos, f"{new_field}: \n")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print(f"已更新：{file_path}")
        return True
    except Exception as e:
        print(f"处理文件 {file_path} 时出错：{str(e)}")
        return False

# 选项6：查找与替换（普通）- 修改版：直接从屏幕输入
def find_and_replace():
    """查找与替换功能（普通）- 修改版：直接从屏幕输入查找和替换内容"""
    source_dir = input(f"请输入源文件夹（默认：e:\\Documents\\Creations\\Databases\\）：") or "e:\\Documents\\Creations\\Databases\\"
    
    # 直接从屏幕输入查找内容和替换内容
    find_content = input("请输入要查找的内容：")
    replace_content = input("请输入要替换的内容：")
    
    # 如果查找内容为空则退出
    if not find_content.strip():
        print("查找内容为空，操作取消")
        return
    
    print(f"将在文件夹 {source_dir} 中查找 '{find_content}' 并替换为 '{replace_content}'")
    confirm = input("确认执行替换操作？(y/N): ")
    if confirm.lower() != 'y':
        print("操作已取消")
        return
    
    # 遍历所有Markdown文件
    processed_count = 0
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = Path(root) / file
                if process_find_replace(file_path, find_content, replace_content):
                    processed_count += 1
    
    print(f"\n查找与替换完成！共处理 {processed_count} 个文件")

def process_find_replace(file_path, find_content, replace_content):
    """处理单个文件的查找与替换（普通）"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 执行替换操作
        new_content = content.replace(find_content, replace_content)
        
        # 如果没有变化则跳过
        if new_content == content:
            return False
        
        # 写入更新后的内容
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"已更新：{file_path}")
        return True
    except Exception as e:
        print(f"处理文件 {file_path} 时出错：{str(e)}")
        return False

# 选项7：查找与替换（正则表达式）
def find_and_replace_regex():
    """查找与替换功能（正则表达式）"""
    source_dir = input(f"请输入源文件夹（默认：e:\\Documents\\Creations\\Databases\\）：") or "e:\\Documents\\Creations\\Databases\\"
    find_file = input(f"请输入查找正则表达式文件位置（默认：E:\\Documents\\Creations\\Scripts\\Python\\DatabaseRegexFind.txt）：") or "E:\\Documents\\Creations\\Scripts\\Python\\DatabaseRegexFind.txt"
    replace_file = input(f"请输入替换内容文件位置（默认：E:\\Documents\\Creations\\Scripts\\Python\\DatabaseRegexReplace.txt）：") or "E:\\Documents\\Creations\\Scripts\\Python\\DatabaseRegexReplace.txt"
    
    # 读取查找正则表达式
    try:
        with open(find_file, 'r', encoding='utf-8') as f:
            find_pattern = f.read().strip()
    except FileNotFoundError:
        print(f"查找正则表达式文件不存在：{find_file}")
        return
    
    # 读取替换内容
    try:
        with open(replace_file, 'r', encoding='utf-8') as f:
            replace_content = f.read()
    except FileNotFoundError:
        print(f"替换内容文件不存在：{replace_file}")
        return
    
    # 编译正则表达式
    try:
        regex = re.compile(find_pattern, flags=re.MULTILINE)
    except re.error as e:
        print(f"正则表达式错误：{str(e)}")
        return
    
    # 遍历所有Markdown文件
    processed_count = 0
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = Path(root) / file
                if process_regex_replace(file_path, regex, replace_content):
                    processed_count += 1
    
    print(f"\n正则表达式查找与替换完成！共处理 {processed_count} 个文件")

def process_regex_replace(file_path, regex, replace_content):
    """处理单个文件的正则表达式查找与替换"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 执行正则表达式替换
        new_content = regex.sub(replace_content, content)
        
        # 如果没有变化则跳过
        if new_content == content:
            return False
        
        # 写入更新后的内容
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"已更新：{file_path}")
        return True
    except Exception as e:
        print(f"处理文件 {file_path} 时出错：{str(e)}")
        return False

# 选项8：元替换
def meta_replacement():
    """元替换功能"""
    source_dir = input(f"请输入源文件夹（默认：e:\\Documents\\Creations\\Databases\\）：") or "e:\\Documents\\Creations\\Databases\\"
    
    processed_count = 0
    # 遍历所有Markdown文件
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = Path(root) / file
                if process_meta_replacement(file_path):
                    processed_count += 1
    
    print(f"\n元替换完成！共处理 {processed_count} 个文件")

def process_meta_replacement(file_path):
    """处理单个文件的元替换"""
    try:
        # 获取文件元数据
        file_stat = file_path.stat()
        
        # 创建时间
        created_time = datetime.datetime.fromtimestamp(file_stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S")
        # 修改时间
        modified_time = datetime.datetime.fromtimestamp(file_stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        # 访问时间
        accessed_time = datetime.datetime.fromtimestamp(file_stat.st_atime).strftime("%Y-%m-%d %H:%M:%S")
        
        # 文件大小
        size_bytes = file_stat.st_size
        size_formatted = format_file_size(size_bytes)
        
        # 父文件夹信息
        parent_folder = file_path.parent
        folder_name = parent_folder.name
        folder_path = str(parent_folder)
        
        # 文件信息
        file_name = file_path.name
        base_name = file_path.stem
        extension = file_path.suffix[1:] if file_path.suffix else ""
        full_path = str(file_path)
        
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 创建替换映射
        replacements = {
            "[FileName]": file_name,
            "[BaseName]": base_name,
            "[Extension]": extension,
            "[FolderName]": folder_name,
            "[FolderPath]": folder_path,
            "[FilePath]": full_path,
            "[DateCreated]": created_time,
            "[DateModified]": modified_time,
            "[DateAccessed]": accessed_time,
            "[Size]": size_formatted,
            "[SizeBytes]": str(size_bytes)
        }
        
        # 执行替换
        new_content = content
        for pattern, replacement in replacements.items():
            new_content = new_content.replace(pattern, replacement)
        
        # 检查是否有变化
        if new_content == content:
            return False
        
        # 写入更新后的内容
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"已更新：{file_path}")
        return True
    except Exception as e:
        print(f"处理文件 {file_path} 时出错：{str(e)}")
        return False

# 选项9：生成数据结构文件
def generate_structure_file():
    """生成数据结构文件"""
    source_dir = input(f"请输入源文件夹（默认：e:\\Documents\\Creations\\Databases\\）：") or "e:\\Documents\\Creations\\Databases\\"
    output_file = Path(source_dir) / ".DatabaseStructure.md"
    
    # 存储所有字段及其类型
    field_types = {}
    # 存储字段顺序
    field_order = []
    
    # 遍历所有Markdown文件
    processed_files = 0
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file == ".DatabaseStructure.md" or not file.endswith('.md'):
                continue
                
            file_path = Path(root) / file
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 提取YAML块
                yaml_block = extract_yaml_block(content)
                if not yaml_block:
                    print(f"跳过：{file_path}（未找到YAML块）")
                    continue
                
                # 解析YAML内容
                try:
                    data = yaml.safe_load(yaml_block)
                except Exception as e:
                    print(f"解析YAML失败：{file_path} - {str(e)}")
                    continue
                
                # 处理字段
                for field, value in data.items():
                    if field not in field_types:
                        # 新字段，添加到字典和顺序列表
                        field_types[field] = infer_field_type(value)
                        field_order.append(field)
                        processed_files += 1
                
            except Exception as e:
                print(f"处理文件 {file_path} 时出错：{str(e)}")
    
    # 写入数据结构文件
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("---\n")
            for field in field_order:
                f.write(f"{field}: {field_types[field]}\n")
            f.write("---\n")
        print(f"\n数据结构文件已生成：{output_file}")
        print(f"共处理 {processed_files} 个文件，发现 {len(field_order)} 个唯一字段")
    except Exception as e:
        print(f"写入数据结构文件时出错：{str(e)}")

# 选项10：结构化数据文件
def restructure_files():
    """根据数据结构文件重新组织数据文件"""
    source_dir = input(f"请输入源文件夹（默认：e:\\Documents\\Creations\\Databases\\）：") or "e:\\Documents\\Creations\\Databases\\"
    structure_file = Path(source_dir) / ".DatabaseStructure.md"
    
    # 读取数据结构文件
    try:
        with open(structure_file, 'r', encoding='utf-8') as f:
            content = f.read()
        yaml_block = extract_yaml_block(content)
        if not yaml_block:
            print(f"数据结构文件格式错误：{structure_file}")
            return
        
        structure_data = yaml.safe_load(yaml_block)
        if not structure_data:
            print(f"数据结构文件内容为空：{structure_file}")
            return
        
        # 获取字段顺序
        field_order = list(structure_data.keys())
    except Exception as e:
        print(f"读取数据结构文件时出错：{str(e)}")
        return
    
    # 处理所有数据文件
    processed_count = 0
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file == ".DatabaseStructure.md" or not file.endswith('.md'):
                continue
                
            file_path = Path(root) / file
            if process_restructure_file(file_path, field_order):
                processed_count += 1
    
    print(f"\n文件结构化完成！共处理 {processed_count} 个文件")

def process_restructure_file(file_path, field_order):
    """处理单个文件的结构化 - 修复了添加缺失字段的问题"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取YAML块和文件其余部分
        match = re.search(r'(^---\n.*?\n---)(.*)', content, flags=re.DOTALL)
        if not match:
            print(f"跳过：{file_path}（未找到YAML块）")
            return False
            
        yaml_block = match.group(1)
        rest_content = match.group(2)
        
        # 解析YAML内容
        try:
            data = yaml.safe_load(extract_yaml_block(yaml_block))
        except Exception as e:
            print(f"解析YAML失败：{file_path} - {str(e)}")
            return False
        
        # 创建新YAML内容
        new_yaml_lines = ["---"]
        
        # 按数据结构文件中的顺序添加字段
        for field in field_order:
            if field in data:
                value = data[field]
                
                # 处理列表值
                if isinstance(value, list):
                    new_yaml_lines.append(f"{field}: ")
                    for item in value:
                        new_yaml_lines.append(f"  - {item}")
                else:
                    # 处理布尔值 - 保持原始大小写 (true/false)
                    if isinstance(value, bool):
                        # 保持小写形式
                        new_yaml_lines.append(f"{field}: {str(value).lower()}")
                    else:
                        # 处理空值 - 留空
                        if value is None:
                            new_yaml_lines.append(f"{field}: ")
                        else:
                            new_yaml_lines.append(f"{field}: {value}")
            else:
                # 添加缺失字段
                new_yaml_lines.append(f"{field}: ")
        
        new_yaml_lines.append("---")
        new_content = "\n".join(new_yaml_lines) + rest_content
        
        # 写入文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"已结构化：{file_path}")
        return True
    except Exception as e:
        print(f"处理文件 {file_path} 时出错：{str(e)}")
        return False

# 选项11：删除没有数据的字段名
def delete_empty_fields():
    """删除没有数据的字段名"""
    source_dir = input(f"请输入源文件夹（默认：e:\\Documents\\Creations\\Databases\\）：") or "e:\\Documents\\Creations\\Databases\\"
    
    processed_count = 0
    # 遍历所有Markdown文件
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file == ".DatabaseStructure.md" or not file.endswith('.md'):
                continue
                
            file_path = Path(root) / file
            if process_delete_empty_fields(file_path):
                processed_count += 1
    print(f"\n空字段删除完成！共处理 {processed_count} 个文件")

def process_delete_empty_fields(file_path):
    """处理单个文件的空字段删除"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取YAML块和文件其余部分
        match = re.search(r'(^---\n.*?\n---)(.*)', content, flags=re.DOTALL)
        if not match:
            print(f"跳过：{file_path}（未找到YAML块）")
            return False
            
        yaml_block = match.group(1)
        rest_content = match.group(2)
        
        # 解析YAML内容
        try:
            data = yaml.safe_load(extract_yaml_block(yaml_block))
        except Exception as e:
            print(f"解析YAML失败：{file_path} - {str(e)}")
            return False
        
        # 创建新YAML内容
        new_yaml_lines = ["---"]
        has_changes = False
        
        for field, value in data.items():
            # 检查字段是否为空
            is_empty = (
                value is None or 
                value == "" or 
                (isinstance(value, list) and len(value) == 0)
            )
            
            if not is_empty:
                # 处理列表值
                if isinstance(value, list):
                    new_yaml_lines.append(f"{field}: ")
                    for item in value:
                        new_yaml_lines.append(f"  - {item}")
                else:
                    new_yaml_lines.append(f"{field}: {value}")
            else:
                has_changes = True
        
        new_yaml_lines.append("---")
        new_content = "\n".join(new_yaml_lines) + rest_content
        
        # 如果没有变化则跳过
        if not has_changes:
            return False
        
        # 写入文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"已清理空字段：{file_path}")
        return True
    except Exception as e:
        print(f"处理文件 {file_path} 时出错：{str(e)}")
        return False

# 选项12：双引号置换单引号
def replace_double_quotes():
    """双引号置换单引号功能"""
    source_dir = input(f"请输入源文件夹（默认：e:\\Documents\\Creations\\Databases\\标准\\）：") or "e:\\Documents\\Creations\\Databases\\标准\\"
    
    processed_count = 0
    # 遍历所有Markdown文件
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = Path(root) / file
                if process_replace_double_quotes(file_path):
                    processed_count += 1
    print(f"\n双引号置换单引号完成！共处理 {processed_count} 个文件")

def process_replace_double_quotes(file_path):
    """处理单个文件的双引号置换单引号"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        has_changes = False
        new_lines = []
        
        for line in lines:
            # 统计当前行中双引号的数量
            double_quote_count = line.count('"')
            
            if double_quote_count <= 2:
                # 如果双引号数量小于等于2，不需要替换
                new_lines.append(line)
            else:
                # 找到第一个和最后一个双引号的位置
                first_quote_pos = line.find('"')
                last_quote_pos = line.rfind('"')
                
                # 构建新行
                new_line = ""
                for i, char in enumerate(line):
                    if char == '"':
                        if i == first_quote_pos or i == last_quote_pos:
                            # 保留第一个和最后一个双引号
                            new_line += '"'
                        else:
                            # 其他双引号替换为单引号
                            new_line += "'"
                            has_changes = True
                    else:
                        new_line += char
                
                new_lines.append(new_line)
        
        # 如果没有变化则跳过
        if not has_changes:
            return False
        
        # 写入更新后的内容
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        
        print(f"已处理：{file_path}")
        return True
    except Exception as e:
        print(f"处理文件 {file_path} 时出错：{str(e)}")
        return False

# 选项13：属性内容处理
def process_attribute_content():
    """属性内容处理功能"""
    source_dir = input(f"请输入源文件夹（默认：e:\\Documents\\Creations\\Databases\\标准\\）：") or "e:\\Documents\\Creations\\Databases\\标准\\"
    attribute_name = input("请输入要处理的属性名称：")
    
    print("\n请选择处理方式：")
    print("1. 将该属性内容设置为空（\"\"）")
    print("2. 将该属性内容设置为指定内容")
    print("3. 将该属性内容每个单词大写")
    print("4. 将该属性内容每个单词小写")
    print("5. 将该属性内容每个单词首字母大写，其余小写")
    print("6. 将该属性内容（汉字、英文、或数字）用空格隔开")
    print("7. 将该属性内容的汉字繁体中文转为简体中文")
    print("8. 所有半角标点符号转为全角标点符号")
    
    choice = input("请输入数字选择操作（1/2/3/4/5/6/7/8）：")
    
    if choice == '2':
        new_content = input("请输入要设置的属性内容：")
    else:
        new_content = None
    
    processed_count = 0
    # 遍历所有Markdown文件
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = Path(root) / file
                if process_attribute_content_file(file_path, attribute_name, choice, new_content):
                    processed_count += 1
    
    print(f"\n属性内容处理完成！共处理 {processed_count} 个文件")

def process_attribute_content_file(file_path, attribute_name, operation, new_content=None):
    """处理单个文件的属性内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取YAML块和文件其余部分
        match = re.search(r'(^---\n.*?\n---)(.*)', content, flags=re.DOTALL)
        if not match:
            print(f"跳过：{file_path}（未找到YAML块）")
            return False
            
        yaml_block = match.group(1)
        rest_content = match.group(2)
        
        # 解析YAML内容
        try:
            data = yaml.safe_load(extract_yaml_block(yaml_block))
        except Exception as e:
            print(f"解析YAML失败：{file_path} - {str(e)}")
            return False
        
        # 检查属性是否存在
        if attribute_name not in data:
            return False
        
        # 获取原始值
        original_value = data[attribute_name]
        
        # 处理属性值
        if operation == '1':
            # 设置为空
            processed_value = ""
        elif operation == '2':
            # 设置为指定内容
            processed_value = new_content
        elif operation == '3':
            # 每个单词大写
            if isinstance(original_value, list):
                processed_value = [item.upper() for item in original_value]
            else:
                processed_value = original_value.upper()
        elif operation == '4':
            # 每个单词小写
            if isinstance(original_value, list):
                processed_value = [item.lower() for item in original_value]
            else:
                processed_value = original_value.lower()
        elif operation == '5':
            # 每个单词首字母大写
            if isinstance(original_value, list):
                processed_value = [item.title() for item in original_value]
            else:
                processed_value = original_value.title()
        elif operation == '6':
            # 中英数分隔
            if isinstance(original_value, list):
                processed_value = [separate_chinese_english_numbers(item) for item in original_value]
            else:
                processed_value = separate_chinese_english_numbers(original_value)
        elif operation == '7':
            # 繁体转简体
            if not ZHCONV_AVAILABLE:
                print("警告：zhconv库未安装，无法进行简繁转换。请使用 pip install zhconv 安装。")
                return False
            if isinstance(original_value, list):
                processed_value = [zhconv.convert(item, 'zh-cn') for item in original_value]
            else:
                processed_value = zhconv.convert(original_value, 'zh-cn')
        elif operation == '8':
            # 半角转全角标点
            if isinstance(original_value, list):
                processed_value = [half_to_full_width(item) for item in original_value]
            else:
                processed_value = half_to_full_width(original_value)
        else:
            print(f"无效的操作选择：{operation}")
            return False
        
        # 更新数据
        data[attribute_name] = processed_value
        
        # 创建新YAML内容
        new_yaml_lines = ["---"]
        
        for field, value in data.items():
            # 处理列表值
            if isinstance(value, list):
                new_yaml_lines.append(f"{field}:")
                for item in value:
                    escaped_item = escape_yaml_value(item)
                    new_yaml_lines.append(f"  - {escaped_item}")
            else:
                # 处理布尔值
                if isinstance(value, bool):
                    new_yaml_lines.append(f"{field}: {str(value).lower()}")
                else:
                    # 处理空值
                    if value is None:
                        new_yaml_lines.append(f"{field}: ")
                    else:
                        escaped_value = escape_yaml_value(value)
                        new_yaml_lines.append(f"{field}: {escaped_value}")
        
        new_yaml_lines.append("---")
        new_content = "\n".join(new_yaml_lines) + rest_content
        
        # 写入文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"已处理：{file_path}")
        return True
    except Exception as e:
        print(f"处理文件 {file_path} 时出错：{str(e)}")
        return False

def separate_chinese_english_numbers(text):
    """将汉字、英文、数字用空格隔开"""
    if not text:
        return text
    
    # 定义标点符号模式（半角和全角）
    punctuation = ".,!?;:""'`~@#$%^&*()[]{}<>/\\|_-+= 　，。！？；：""'～＠＃＄％＾＆＊（）【】｛｝〈〉／＼｜－—＋＝"
    
    # 汉字与英文/数字之间加空格（忽略标点）
    result = re.sub(r"([\u4e00-\u9fff])(?=[a-zA-Z0-9])", r"\1 ", str(text))
    result = re.sub(r"(?<=[a-zA-Z0-9])([\u4e00-\u9fff])", r" \1", result)
    
    # 英文与数字之间加空格（忽略标点）
    result = re.sub(r"([a-zA-Z])(?=\d)", r"\1 ", result)
    result = re.sub(r"(?<=\d)([a-zA-Z])", r" \1", result)
    
    # 清理多余空格
    result = re.sub(r"\s+", " ", result)
    return result.strip()

def half_to_full_width(text):
    """半角标点符号转为全角标点符号"""
    if not text:
        return text
    
    # 半角到全角的映射
    half_to_full_map = {
        ' ': '　',
        ',': '，',
        '~': '～',
        ':': '：',
        ';': '；',
        '!': '！',
        '?': '？',
        '%': '％',
        '+': '＋',
        '-': '－',
        '=': '＝',
        '/': '／',
        '\\': '＼',
        '(': '（',
        ')': '）',
        '<': '〈',
        '>': '〉'
    }
    
    result = str(text)
    
    # 智能双引号替换
    quote_count = 0
    pos = 0
    while pos < len(result):
        if result[pos] == '"':
            quote_count += 1
            replacement = "「" if quote_count % 2 == 1 else "」"
            result = result[:pos] + replacement + result[pos+1:]
            pos += len(replacement)
        else:
            pos += 1
    
    # 处理其他符号
    for half, full in half_to_full_map.items():
        result = result.replace(half, full)
    
    return result

# 选项14：写入Excel文件（含ED2K链接生成）
def write_to_excel_with_ed2k():
    """写入Excel文件并生成ED2K链接"""
    # 获取Excel文件位置和源文件夹位置
    excel_path = get_default_path("请输入Excel文件位置", "e:\\Documents\\Creations\\Databases\\标准.xlsx")
    source_dir = get_default_path("请输入源文件夹位置", "d:\\Downloads\\")
    
    # 询问引用页、属于、主链接的值
    reference_page = input("请输入引用页的值（按回车则为空）：").strip()
    belongs_to = input("请输入属于的值（按回车则为空）：").strip()
    main_link = input("请输入主链接的值（按回车则为空）：").strip()
    
    # 检查Excel文件是否存在
    if not os.path.exists(excel_path):
        print(f"错误：Excel文件 '{excel_path}' 不存在")
        return
    
    # 检查源文件夹是否存在
    if not os.path.exists(source_dir):
        print(f"错误：源文件夹 '{source_dir}' 不存在")
        return
    
    # 读取Excel文件
    try:
        df = pd.read_excel(excel_path, engine='openpyxl')
    except Exception as e:
        print(f"读取Excel文件失败: {e}")
        return
    
    # 获取最后一个Index值
    last_index = 0
    if 'Index' in df.columns and not df.empty:
        last_index_values = df['Index'].dropna()
        if not last_index_values.empty:
            last_index = int(last_index_values.iloc[-1])
    
    # 收集所有文件
    all_files = []
    for root, _, files in os.walk(source_dir):
        for file in files:
            file_path = os.path.join(root, file)
            all_files.append(file_path)
    
    if not all_files:
        print("源文件夹中没有找到任何文件")
        return
    
    print(f"找到 {len(all_files)} 个文件，开始处理...")
    
    # 处理每个文件
    for file_path in all_files:
        try:
            # 1. 每一条记录新开一行
            new_row = {}
            
            # 2. Index字段值为上一行Index字段值+1
            last_index += 1
            new_row['Index'] = last_index
            
            # 3. 将源文件夹内文件名写入"名字"与"原文件名"字段值
            file_name = os.path.basename(file_path)
            base_name = os.path.splitext(file_name)[0]
            new_row['名字'] = base_name
            new_row['原文件名'] = file_name
            
            # 4. 文件复制操作
            try:
                # 复制到 d:\Works\In\
                dest_in = "d:\\Works\\In\\" + file_name
                shutil.copy2(file_path, dest_in)
                print(f"已复制到: {dest_in}")
                
                # 复制到 z:\
                dest_z = "z:\\" + file_name
                try:
                    shutil.copy2(file_path, dest_z)
                    print(f"已复制到: {dest_z}")
                except Exception as e:
                    print(f"无法复制到 z:\\: {e}")
                    print("操作已退出")
                    return
                
                # 等待系统生成加密文件（假设在d:\Xyz\目录下）
                time.sleep(2)  # 等待2秒让系统处理
                
                # 查找d:\Xyz\目录中的新文件
                xyz_dir = "d:\\Xyz\\"
                if os.path.exists(xyz_dir):
                    # 获取所有文件
                    xyz_files = [f for f in os.listdir(xyz_dir) if os.path.isfile(os.path.join(xyz_dir, f))]
                    
                    # 过滤出可能是加密文件的文件（无扩展名的文件）
                    encrypted_files = [f for f in xyz_files if '.' not in f]
                    
                    # 如果找不到无扩展名的文件，考虑其他可能的加密文件命名规则
                    if not encrypted_files:
                        # 这里可以根据实际情况添加其他识别加密文件的逻辑
                        # 例如：文件名长度、字符组成等
                        encrypted_files = xyz_files
                
                if encrypted_files:
                    encrypted_filename = encrypted_files[0]  # 取第一个文件作为加密文件
                    new_row['加密文件名'] = encrypted_filename
                    
                    # 移动加密文件到d:\Works\Uploads\
                    source_encrypted = os.path.join(xyz_dir, encrypted_filename)
                    dest_upload = "d:\\Works\\Uploads\\" + encrypted_filename
                    shutil.move(source_encrypted, dest_upload)
                    print(f"已移动加密文件到: {dest_upload}")
                else:
                    print("警告：未在d:\\Xyz\\目录中找到加密文件")
                    new_row['加密文件名'] = ""
                    
            except Exception as e:
                print(f"文件复制/移动操作失败: {e}")
                new_row['加密文件名'] = ""
            
            # 5. 将询问的值写入相应字段
            new_row['引用页'] = reference_page
            new_row['属于'] = belongs_to
            new_row['主链接'] = main_link
            
            # 6. 计算并生成ED2K链接
            try:
                rhash_path = "d:\\ProApps\\RHash\\rhash.exe"
                if os.path.exists(rhash_path):
                    # 使用RHash生成ED2K链接
                    result = subprocess.run([
                        rhash_path, 
                        "--uppercase", 
                        "--ed2k-link", 
                        file_path
                    ], capture_output=True, text=True, encoding='utf-8')
                    
                    if result.returncode == 0:
                        ed2k_link = result.stdout.strip()
                        new_row['标准链接'] = ed2k_link
                        
                        # 7. 通过ED2K链接解析大小和散列
                        if ed2k_link.startswith("ed2k://|file|"):
                            # 对链接进行百分号解码
                            decoded_link = urllib.parse.unquote(ed2k_link)
                            parts = decoded_link.split('|')
                            
                            if len(parts) >= 5:
                                # 文件大小（字节）
                                filesize = parts[3]
                                # 哈希值
                                filehash = parts[4].upper()
                                
                                # 格式化文件大小
                                formatted_size = format_file_size(filesize)
                                
                                new_row['大小'] = formatted_size
                                new_row['散列'] = filehash
                            else:
                                new_row['大小'] = ""
                                new_row['散列'] = ""
                        else:
                            new_row['大小'] = ""
                            new_row['散列'] = ""
                    else:
                        print(f"生成ED2K链接失败: {result.stderr}")
                        new_row['标准链接'] = ""
                        new_row['大小'] = ""
                        new_row['散列'] = ""
                else:
                    print(f"RHash未找到于: {rhash_path}")
                    new_row['标准链接'] = ""
                    new_row['大小'] = ""
                    new_row['散列'] = ""
            except Exception as e:
                print(f"计算ED2K链接时出错: {e}")
                new_row['标准链接'] = ""
                new_row['大小'] = ""
                new_row['散列'] = ""
            
            # 将新行添加到DataFrame
            new_df = pd.DataFrame([new_row])
            df = pd.concat([df, new_df], ignore_index=True)
            
            print(f"已处理文件: {file_name} (Index: {last_index})")
            
        except Exception as e:
            print(f"处理文件 {file_path} 时出错: {e}")
            continue
    
    # 保存更新后的Excel文件
    try:
        df.to_excel(excel_path, index=False, engine='openpyxl')
        print(f"成功更新Excel文件: {excel_path}")
        print(f"新增 {len(all_files)} 条记录")
    except Exception as e:
        print(f"保存Excel文件失败: {e}")

if __name__ == "__main__":
    main()
    input("按回车键退出程序...")