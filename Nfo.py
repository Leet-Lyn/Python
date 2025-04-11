# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件夹位置。
# 遍历源文件夹位置中所有的视频文件（mkv、avi、f4v、flv、ts、mpeg、mpg、rm、rmvb、asf、wmv、mov、webm、mp4）。在该文件夹下生成同名 nfo 文件。
# 询问我 nfo 文件内写入的内容。UTF-8编码，默认为：<?xml version="1.0" encoding="UTF-8" standalone="yes"?><movie><title> </title></movie>
# 再次枚举源文件夹位置中所有 nfo 文件，读取其文件名（不包括后缀名），替换“<title> </title>”内的“ ”。   

# 导入模块
import os

def get_valid_directory(prompt, default_folder=None):
    """
    获取有效的文件夹路径，支持默认路径
    """
    while True:
        folder = input(prompt).strip()
        # 使用默认路径当用户输入为空时
        if not folder and default_folder is not None:
            folder = default_folder
        if os.path.isdir(folder):
            return folder
        print(f"路径 '{folder}' 无效，请重新输入。")

def create_nfo_files_for_videos(source_folder, xml_template):
    """
    遍历源文件夹中的所有视频文件，生成对应的XML文件
    """
    # 支持的视频文件扩展名集合（小写）
    video_extensions = {
        '.mkv', '.avi', '.f4v', '.flv', '.ts',
        '.mpeg', '.mpg', '.rm', '.rmvb', '.asf',
        '.wmv', '.mov', '.webm', '.mp4'
    }

    for file_name in os.listdir(source_folder):
        # 获取文件扩展名并转为小写
        file_ext = os.path.splitext(file_name)[1].lower()
        
        if file_ext in video_extensions:
            base_name = os.path.splitext(file_name)[0]  # 去除扩展名
            nfo_file_path = os.path.join(source_folder, f"{base_name}.nfo")

            # 写入XML模板内容
            with open(nfo_file_path, 'w', encoding='utf-8') as nfo_file:
                nfo_file.write(xml_template)
            print(f"已生成：{nfo_file_path}")

def update_nfo_with_filenames(source_folder):
    """
    更新所有XML文件中的标题信息
    """
    for file_name in os.listdir(source_folder):
        if file_name.endswith('.nfo'):
            base_name = os.path.splitext(file_name)[0]  # 获取基础文件名
            nfo_path = os.path.join(source_folder, file_name)

            # 读取并替换文件内容
            with open(nfo_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 替换标题标签内容
            new_content = content.replace(
                "<title> </title>", 
                f"<title>{base_name}</title>"
            )

            # 写回更新后的内容
            with open(nfo_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"已更新：{nfo_path}")

def main():
    """
    主程序流程控制
    """
    # 默认路径设置
    default_source = r"D:\Works\Out"
    
    # 获取用户输入的源文件夹路径
    prompt = f"请输入视频文件夹路径（默认：{default_source}）："
    source_folder = get_valid_directory(prompt, default_source)

    # 获取XML模板内容
    custom_title = input("请输入<title>内容（留空使用默认模板）：").strip()
    xml_template = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<movie>
  <title>{}</title>
</movie>""".format(custom_title if custom_title else " ")

    # 创建XML文件
    create_nfo_files_for_videos(source_folder, xml_template)
    
    # 更新标题信息
    update_nfo_with_filenames(source_folder)

    print("\n所有操作已完成！")
    input("按回车键退出程序...")

if __name__ == "__main__":
    main()