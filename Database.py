# 请帮我写个中文的 Python 脚本，批注也是中文：
# 询问我想要做什么：
# 1. 生成文件：在脚本开始前询问我源 CSV 文件位置（默认为：d:\\Downloads\\CSV.csv）与目标文件夹位置（默认为：e:\\Documents\\Creations\\Articles\\Database\\）。这个 CSV 格式，第一行为所有字段名，字段名用""包绕。不同字段名之间用,隔开。第二行开始每一以"开头的为每一条记录。每一个""包绕的为相应的字段数据（可包含数行）为每一条字段。独立的一条记录和字段内多行区别在于行首有无"。每一记录内字段名与字段内容一一对应。请生成每一条记录（markdown 格式 文件，数据以 yaml 属性格式呈现如上文，markdown 文件名为字段"名字"对应字段内容，）。在目标文件夹下生成子文件夹，子文件夹名为CSV格式的文件名（不包括后缀名），将生成的记录放在该子文件夹下。生成的文件名为字段"名字"对应字段内容，当字段"名字"对应字段内容出现不能成为文件名的内容如半角冒号“:”，请用空格破折号空格“ -”代替。其他的如半角问号“?”、半角反斜杠“\”、正斜杠“/”，用全角问号“？”、全角反斜杠“＼”、正斜杠“／”代替。半角双引号“"”用半角波浪号“~”代替。竖线“|”用反单引号“`”代替。星号“*”用乘号“×”代替。<（小于）、>（大于）用书名号“《 》”代替。
# 2. 删除字段：在脚本开始前询问我源文件夹位置，文件夹内储存着上述结构的数据（默认为：e:\\Documents\\Creations\\Articles\\Database\\）。询问我需要删除某一字段名。遍历源文件夹位置中所有的文件及子文件夹内文件（md 格式），读取每一文件，找到这个字段后删除该字段即其配套的字段内容。
# 3. 添加字段：在脚本开始前询问我源文件夹位置，文件夹内储存着上述结构的数据（默认为：e:\\Documents\\Creations\\Articles\\Database\\）。询问我需要添加某一字段名，及添加在哪一个字段前。遍历源文件夹位置中所有的文件及子文件夹内文件（md 格式），读取每一文件，找到这个字段，在这行之前，添加要求的字段。
# 4. 查找与替换：在脚本开始前询问我源文件夹位置，文件夹内储存着上述结构的数据（默认为：e:\\Documents\\Creations\\Articles\\Database\\）。询问我存放查找内容的文本位置（默认为：e:\\Documents\\Creations\\Scripts\\Python\\DatabaseFind.txt）与存放替换内容的文本位置（默认为：e:\\Documents\\Creations\\Scripts\\Python\\DatabaseReplace.txt）。遍历源文件夹位置中所有的文件及子文件夹内文件（md 格式），读取每一文件，找到存放查找内容，用替换内容进行替换。
# 5. 查找与替换（正则表达式）：在脚本开始前询问我源文件夹位置，文件夹内储存着上述结构的数据（默认为：e:\\Documents\\Creations\\Articles\\Database\\）。询问我存放查找内容的正则表达式文本位置（默认为：e:\\Documents\\Creations\\Scripts\\Python\\DatabaseFindRegex.txt）与存放替换内容的文本位置（默认为：e:\\Documents\\Creations\\Scripts\\Python\\DatabaseReplaceRegex.txt）。遍历源文件夹位置中所有的文件及子文件夹内文件（md 格式），读取每一文件，找到存放查找内容，用替换内容进行替换。
# 6. 元替换：在脚本开始前询问我源文件夹位置，文件夹内储存着上述结构的数据（默认为：e:\\Documents\\Creations\\Articles\\Database\\）。遍历源文件夹位置中所有的文件及子文件夹内文件（md 格式），读取每一文件，将文件里的元数据标实替换 md 文件的元数据。（比如[FileName]表示全文件名，[BaseName]表示不含扩展名的文件名，[Extension]表示扩展名，[FolderName]表示父文件夹名，[FolderPath]表示父文件夹路径，[FilePath]表示文件路径，[DateCreated]表示文件生成日期时间，[DateModified]表示文件修改日期时间，[DateAccessed]表示文件修改时间，[Size]表示文件大小（适配 B、KB、MB、GB 形式，并精确到小数点后 4 位），[SizeBytes]表示文件大小（Bytes）。
# 7. 生成数据结构文件：在脚本开始前询问我源文件夹位置，文件夹内储存着上述结构的数据（默认为：e:\\Documents\\Creations\\Articles\\Database\\）。在该文件夹下生成一个 md 文件，文件名为“.DatabaseStructure.md”。读取该文件夹中的其他每一文件（排除 “.DatabaseStructure.md”），将第一个文件里每一个的字段名，依次写入“.DatabaseStructure.md”中。字段名后接一个半角冒号和空格（“: ”），在此之后，写着这个字段的字段类型（文本、数值、布尔、日期、时间、日期时间、列表），每一行一个字段。这些字段名首尾由一组三个破折号（“---”）分隔符包围。此后依次读取每一个文件，如文件里的字段名已经被“.DatabaseStructure.md”记录，则不做处理；如文件里的字段名未被“.DatabaseStructure.md”记录，则添加该字段。
# 8. 结构化数据文件：在脚本开始前询问我源文件夹位置，文件夹内储存着上述结构的数据（默认为：e:\\Documents\\Creations\\Articles\\Database\\）。读取该文件夹下的“.DatabaseStructure.md”。这个就是后续文件的字段的数据结构。依次读取该文件夹中的其他每一文件（排除 “.DatabaseStructure.md”），将它的字段按照“.DatabaseStructure.md”中字段名顺序重新排序；如果“.DatabaseStructure.md”里的某一字段名有，而该文件中没有，就按顺序添加到该文件中；如果该文件有，而“.DatabaseStructure.md”里没有的字段名，就删除该字段及其数据。
# 9. 删除没有数据的字段名：在脚本开始前询问我源文件夹位置，文件夹内储存着上述结构的数据（默认为：e:\\Documents\\Creations\\Articles\\Database\\）。依次读取该文件夹中的其他每一文件（排除 “.DatabaseStructure.md”）。删除没有数据的字段行。
# 0. 退出程序。

# 导入模块
import os
import csv
import re
import shutil
from pathlib import Path
import yaml
import datetime
import time  # 添加time模块用于元替换功能

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
        print("1. 从 CSV 生成 Markdown 文件")
        print("2. 删除字段")
        print("3. 添加字段")
        print("4. 查找与替换（普通）")
        print("5. 查找与替换（正则表达式）")
        print("6. 元替换")
        print("7. 生成数据结构文件")
        print("8. 结构化数据文件")
        print("9. 删除没有数据的字段名")
        print("0. 退出程序")
        choice = input("请输入数字选择操作（1/2/3/4/5/6/7/8/9/0）：")
        
        if choice == '1':
            generate_from_csv()
        elif choice == '2':
            delete_field()
        elif choice == '3':
            add_field()
        elif choice == '4':
            find_and_replace()
        elif choice == '5':
            find_and_replace_regex()
        elif choice == '6':
            meta_replacement()
        elif choice == '7':
            generate_structure_file()
        elif choice == '8':
            restructure_files()
        elif choice == '9':
            delete_empty_fields()
        elif choice == '0':
            print("程序已退出")
            break
        else:
            print("无效选择，请重新输入")

def generate_from_csv():
    """从CSV生成Markdown文件"""
    # 获取用户输入路径
    csv_path = input(f"请输入 CSV 文件路径（默认：D:\\Downloads\\CSV.csv）：") or "D:\\Downloads\\CSV.csv"
    output_dir = input(f"请输入目标文件夹（默认：E:\\Documents\\Creations\\Articles\\Database\\）：") or "E:\\Documents\\Creations\\Articles\\Database\\"

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
                        # 处理多行内容
                        if '\n' in value:
                            yaml_lines.append(f"{header}: ")
                            for line in value.split('\n'):
                                yaml_lines.append(f"  - {line.strip()}")
                        else:
                            yaml_lines.append(f"{header}: {value}")
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

def delete_field():
    """删除指定字段"""
    source_dir = input(f"请输入源文件夹（默认：E:\\Documents\\Creations\\Articles\\Database\\）：") or "E:\\Documents\\Creations\\Articles\\Database\\"
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

def add_field():
    """添加新字段"""
    source_dir = input(f"请输入源文件夹（默认：E:\\Documents\\Creations\\Articles\\Database\\）：") or "E:\\Documents\\Creations\\Articles\\Database\\"
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

def find_and_replace():
    """查找与替换功能（普通）"""
    source_dir = input(f"请输入源文件夹（默认：E:\\Documents\\Creations\\Articles\\Database\\）：") or "E:\\Documents\\Creations\\Articles\\Database\\"
    find_file = input(f"请输入查找内容文件位置（默认：E:\\Documents\\Creations\\Scripts\\Python\\DatabaseFind.txt）：") or "E:\\Documents\\Creations\\Scripts\\Python\\DatabaseFind.txt"
    replace_file = input(f"请输入替换内容文件位置（默认：E:\\Documents\\Creations\\Scripts\\Python\\DatabaseReplace.txt）：") or "E:\\Documents\\Creations\\Scripts\\Python\\DatabaseReplace.txt"
    
    # 读取查找内容
    try:
        with open(find_file, 'r', encoding='utf-8') as f:
            find_content = f.read()
    except FileNotFoundError:
        print(f"查找文件不存在：{find_file}")
        return
    
    # 读取替换内容
    try:
        with open(replace_file, 'r', encoding='utf-8') as f:
            replace_content = f.read()
    except FileNotFoundError:
        print(f"替换文件不存在：{replace_file}")
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

def find_and_replace_regex():
    """查找与替换功能（正则表达式）"""
    source_dir = input(f"请输入源文件夹（默认：E:\\Documents\\Creations\\Articles\\Database\\）：") or "E:\\Documents\\Creations\\Articles\\Database\\"
    find_file = input(f"请输入查找正则表达式文件位置（默认：E:\\Documents\\Creations\\Scripts\\Python\\DatabaseFindRegex.txt）：") or "E:\\Documents\\Creations\\Scripts\\Python\\DatabaseFindRegex.txt"
    replace_file = input(f"请输入替换内容文件位置（默认：E:\\Documents\\Creations\\Scripts\\Python\\DatabaseReplaceRegex.txt）：") or "E:\\Documents\\Creations\\Scripts\\Python\\DatabaseReplaceRegex.txt"
    
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

def meta_replacement():
    """元替换功能"""
    source_dir = input(f"请输入源文件夹（默认：E:\\Documents\\Creations\\Articles\\Database\\）：") or "E:\\Documents\\Creations\\Articles\\Database\\"
    
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

def process_find_replace(file_path, find_content, replace_content):
    """处理单个文件的查找与替换（普通）"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 如果查找内容为空则跳过
        if not find_content.strip():
            print(f"跳过：{file_path}（查找内容为空）")
            return False
        
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

def generate_structure_file():
    """生成数据结构文件"""
    source_dir = input(f"请输入源文件夹（默认：E:\\Documents\\Creations\\Articles\\Database\\）：") or "E:\\Documents\\Creations\\Articles\\Database\\"
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

def restructure_files():
    """根据数据结构文件重新组织数据文件"""
    source_dir = input(f"请输入源文件夹（默认：E:\\Documents\\Creations\\Articles\\Database\\）：") or "E:\\Documents\\Creations\\Articles\\Database\\"
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

def delete_empty_fields():
    """删除没有数据的字段名"""
    source_dir = input(f"请输入源文件夹（默认：E:\\Documents\\Creations\\Articles\\Database\\）：") or "E:\\Documents\\Creations\\Articles\\Database\\"
    
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

if __name__ == "__main__":
    main()
    input("按回车键退出程序...")