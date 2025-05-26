# 请帮我写个中文的 Python 脚本，批注也是中文：
# 询问我想要做什么：
# 1. 生成文件：在脚本开始前询问我源 CSV 文件位置（默认为：d:\\Downloads\\CSV.csv）与目标文件夹位置（默认为：e:\\Documents\\Creations\\Articles\\Database\\）。这个 CSV 格式，第一行为所有字段名，字段名用""包绕。不同字段名之间用,隔开。第二行开始每一以"开头的为每一条记录。每一个""包绕的为相应的字段数据（可包含数行）为每一条字段。独立的一条记录和字段内多行区别在于行首有无"。每一记录内字段名与字段内容一一对应。请生成每一条记录（markdown格式文件，文件名为字段"名字"对应字段内容）。在目标文件夹下生成子文件夹，子文件夹名为CSV格式的文件名（不包括后缀名），将生成的记录放在该子文件夹下。
# 2. 删除字段：在脚本开始前询问我源文件夹位置，文件夹内储存着上述结构的数据（默认为：e:\\Documents\\Creations\\Articles\\Database\\）。询问我需要删除某一字段名。遍历源文件夹位置中所有的文件（md 格式），读取每一文件，找到这个字段后删除该字段即其配套的字段内容。
# 3. 添加字段：在脚本开始前询问我源文件夹位置，文件夹内储存着上述结构的数据（默认为：e:\\Documents\\Creations\\Articles\\Database\\）。询问我需要添加某一字段名，及添加在哪一个字段前。遍历源文件夹位置中所有的文件（md 格式），读取每一文件，找到这个字段，在这行之前，添加要求的字段。

# 导入模块
import os
import csv
import re

def main():
    """主交互函数"""
    print("请选择需要执行的操作：")
    print("1. 从CSV生成Markdown文件")
    print("2. 删除指定字段")
    print("3. 添加新字段")
    choice = input("请输入数字选择操作 (1/2/3): ").strip()

    if choice == '1':
        generate_from_csv()
    elif choice == '2':
        delete_field()
    elif choice == '3':
        add_field()
    else:
        print("无效的输入，程序退出")
    input("按回车键退出...")

# 通用工具函数
def get_default_path(prompt, default):
    """获取带默认值的路径输入"""
    path = input(f"{prompt} (默认：{default}): ").strip()
    return path if path else default

def ensure_dir(path):
    """确保目录存在"""
    if not os.path.exists(path):
        os.makedirs(path)

def sanitize_filename(name):
    """文件名净化处理"""
    # 替换Windows系统非法字符
    name = name.replace(':', ' -')        # 半角冒号转减号
    name = name.replace('!', '！')       # 半角感叹号转全角
    name = name.replace('?', '？')       # 半角问号转全角
    # 可选：处理其他特殊字符
    # name = re.sub(r'[\\/*"<>|]', '-', name)
    return name

# 功能 1：CSV转Markdown
def generate_from_csv():
    """从CSV生成Markdown文件"""
    csv_path = get_default_path("请输入CSV文件路径", "d:\\Downloads\\CSV.csv")
    target_dir = get_default_path("请输入目标文件夹路径", "e:\\Documents\\Creations\\Articles\\Database\\")

    # 创建子文件夹
    csv_name = os.path.splitext(os.path.basename(csv_path))[0]
    output_dir = os.path.join(target_dir, csv_name)
    ensure_dir(output_dir)

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, quotechar='"', delimiter=',')
        headers = next(reader)  # 读取首行字段名
        
        for row_idx, row in enumerate(reader, 1):
            process_row(row, headers, output_dir)

def process_row(row, headers, output_dir):
    """处理单行数据并生成Markdown文件"""
    record = {}
    for header, value in zip(headers, row):
        record[header] = value.strip()

    # 生成安全文件名
    raw_name = record.get('名字', '未命名')
    clean_name = sanitize_filename(raw_name)
    filename = f"{clean_name}.md"
    filepath = os.path.join(output_dir, filename)

    # 处理重名文件（可选）
    counter = 1
    while os.path.exists(filepath):
        filename = f"{clean_name}_{counter}.md"
        filepath = os.path.join(output_dir, filename)
        counter += 1

    # 写入Markdown内容
    with open(filepath, 'w', encoding='utf-8') as f:
        for header in headers:
            content = record.get(header, "")
            if '\n' in content:
                f.write(f"{header}：\n")
                for line in content.split('\n'):
                    f.write(f"    {line}\n")
            else:
                f.write(f"{header}：{content}\n")

# 功能 2：删除字段（保持不变）
def delete_field():
    source_dir = get_default_path("请输入源文件夹路径", "e:\\Documents\\Creations\\Articles\\Database\\")
    field_to_delete = input("请输入要删除的字段名（需包含全角冒号，示例：作者：）: ").strip()

    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.md'):
                process_delete(os.path.join(root, file), field_to_delete)

def process_delete(filepath, target_field):
    new_lines = []
    skip_mode = False

    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith(target_field):
                skip_mode = True
                continue
            if skip_mode:
                if line.startswith('    '):
                    continue
                else:
                    skip_mode = False
            new_lines.append(line)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

# 功能 3：添加字段（保持不变）
def add_field():
    source_dir = get_default_path("请输入源文件夹路径", "e:\\Documents\\Creations\\Articles\\Database\\")
    new_field = input("请输入要添加的新字段名（需包含全角冒号，示例：摘要：）: ").strip()
    before_field = input("请输入要插入在哪个字段之前（需包含全角冒号）: ").strip()

    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.md'):
                process_add(os.path.join(root, file), new_field, before_field)

def process_add(filepath, new_field, before_field):
    new_lines = []
    added = False

    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if not added and line.startswith(before_field):
                new_lines.append(f"{new_field}\n")
                added = True
            new_lines.append(line)
    
    if not added:
        new_lines.append(f"\n{new_field}\n")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    main()