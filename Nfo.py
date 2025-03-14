# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件夹位置。
# 遍历源文件夹位置中所有 mkv 文件。在该文件夹下生成同名 txt 文件。
# 询问我 txt 文件内写入的内容。UTF-8编码，默认为：<?xml version="1.0" encoding="UTF-8" standalone="yes"?><movie><title> </title></movie>
# 再次枚举源文件夹位置中所有 txt 文件，读取其文件名（不包括后缀名），替换“<title> </title>”内的“ ”。   

# 导入模块
import os

def get_valid_directory(prompt, default_folder=None):
    """
    获取有效的文件夹路径，支持默认路径。
    """
    while True:
        folder = input(prompt).strip()
        # 如果用户输入为空且存在默认路径，则使用默认路径
        if not folder and default_folder is not None:
            folder = default_folder
        if os.path.isdir(folder):
            return folder
        print(f"路径 '{folder}' 无效，请重新输入。")

def create_txt_files_for_mkv(source_folder, xml_template):
    """
    遍历源文件夹中的所有 .mkv 文件，生成对应的 .txt 文件。
    """
    for file_name in os.listdir(source_folder):
        if file_name.endswith('.mkv'):
            base_name = os.path.splitext(file_name)[0]  # 获取文件名，不包括扩展名
            txt_file_path = os.path.join(source_folder, f"{base_name}.txt")  # 构建 txt 文件路径

            # 写入 XML 模板到 txt 文件
            with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write(xml_template)

            print(f"已生成 {txt_file_path} 文件")

def update_txt_with_filenames(source_folder):
    """
    遍历源文件夹中的所有 .txt 文件，读取文件名并替换 XML 中的 <title> 内容。
    """
    for file_name in os.listdir(source_folder):
        if file_name.endswith('.txt'):
            base_name = os.path.splitext(file_name)[0]  # 获取文件名，不包括扩展名
            txt_file_path = os.path.join(source_folder, file_name)

            # 读取 txt 文件内容
            with open(txt_file_path, 'r', encoding='utf-8') as txt_file:
                content = txt_file.read()

            # 替换 <title> 标签中的内容为文件名
            new_content = content.replace("<title> </title>", f"<title>{base_name}</title>")

            # 写回修改后的内容
            with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write(new_content)

            print(f"已更新 {txt_file_path} 文件中的 <title> 标签")

def main():
    """
    主程序入口。
    """
    # 设置默认路径
    default_source = r"D:\Works\Out"
    
    # 获取源文件夹路径（带默认值）
    prompt = f"请输入源文件夹路径（默认为 {default_source}）："
    source_folder = get_valid_directory(prompt, default_folder=default_source)

    # 询问用户 txt 文件内容
    custom_title = input("请输入txt文件中<title>标签的内容（按回车使用默认内容）：").strip()
    if not custom_title:
        custom_title = " "  # 默认内容

    # XML 模板（包括用户自定义的内容）
    xml_template = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<movie>
  <title>{custom_title}</title>
</movie>"""

    # 创建 mkv 文件对应的 txt 文件
    create_txt_files_for_mkv(source_folder, xml_template)

    # 更新所有 txt 文件中的 <title> 内容
    update_txt_with_filenames(source_folder)

    print("处理完成！")
    input("按回车键退出...")

if __name__ == "__main__":
    main()