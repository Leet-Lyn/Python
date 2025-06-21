# 请帮我写个中文的 Python 脚本，批注也是中文：
# 询问我想要做什么：
# 1. 生成文件：在脚本开始前询问我源 CSV 文件位置（默认为：d:\\Downloads\\CSV.csv）与目标文件夹位置（默认为：e:\\Documents\\Creations\\Articles\\Database\\）。这个 CSV 格式，第一行为所有字段名，字段名用""包绕。不同字段名之间用,隔开。第二行开始每一以"开头的为每一条记录。每一个""包绕的为相应的字段数据（可包含数行）为每一条字段。独立的一条记录和字段内多行区别在于行首有无"。每一记录内字段名与字段内容一一对应。请生成每一条记录（markdown 格式 文件，数据以 yaml 属性格式呈现如上文，markdown 文件名为字段"名字"对应字段内容，）。在目标文件夹下生成子文件夹，子文件夹名为CSV格式的文件名（不包括后缀名），将生成的记录放在该子文件夹下。生成的文件名为字段"名字"对应字段内容，当字段"名字"对应字段内容出现不能成为文件名的内容如半角冒号“:”，请用空格破折号空格“ -”代替。其他的如半角问号“?”、半角反斜杠“\”、正斜杠“/”，用全角问号“？”、全角反斜杠“＼”、正斜杠“／”代替。半角双引号“"”用半角波浪号“~”代替。竖线“|”用反单引号“`”代替。星号“*”用乘号“×”代替。<（小于）、>（大于）用书名号“《 》”代替。
# 2. 删除字段：在脚本开始前询问我源文件夹位置，文件夹内储存着上述结构的数据（默认为：e:\\Documents\\Creations\\Articles\\Database\\）。询问我需要删除某一字段名。遍历源文件夹位置中所有的文件及子文件夹内文件（md 格式），读取每一文件，找到这个字段后删除该字段即其配套的字段内容。
# 3. 添加字段：在脚本开始前询问我源文件夹位置，文件夹内储存着上述结构的数据（默认为：e:\\Documents\\Creations\\Articles\\Database\\）。询问我需要添加某一字段名，及添加在哪一个字段前。遍历源文件夹位置中所有的文件及子文件夹内文件（md 格式），读取每一文件，找到这个字段，在这行之前，添加要求的字段。
# 4. 查找与替换：在脚本开始前询问我源文件夹位置，文件夹内储存着上述结构的数据（默认为：e:\\Documents\\Creations\\Articles\\Database\\）。询问我存放查找内容的文本位置（默认为：e:\\Documents\\Creations\\Scripts\\Python\\DatabaseFind.txt）与存放替换内容的文本位置（默认为：e:\\Documents\\Creations\\Scripts\\Python\\DatabaseReplace.txt）。遍历源文件夹位置中所有的文件及子文件夹内文件（md 格式），读取每一文件，找到存放查找内容，用替换内容进行替换。
# 5. 退出程序。

# 导入模块
import os
import csv
import re
import shutil
from pathlib import Path

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

def main():
    while True:  # 添加循环，使程序能持续运行
        print("\n" + "="*50)
        print("请选择操作：")
        print("1. 从 CSV 生成 Markdown 文件")
        print("2. 删除字段")
        print("3. 添加字段")
        print("4. 查找与替换")
        print("5. 退出程序")
        choice = input("请输入数字选择操作（1/2/3/4/5）：")
        
        if choice == '1':
            generate_from_csv()
        elif choice == '2':
            delete_field()
        elif choice == '3':
            add_field()
        elif choice == '4':
            find_and_replace()
        elif choice == '5':
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
                            yaml_lines.append(f"{header}: |")
                            for line in value.split('\n'):
                                yaml_lines.append(f"  {line.strip()}")
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
    """查找与替换功能"""
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

def process_find_replace(file_path, find_content, replace_content):
    """处理单个文件的查找与替换"""
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

if __name__ == "__main__":
    main()
    input("按回车键退出程序...")