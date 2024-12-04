# 重命名为 List 文件里的文件名

# 导入模块。
import os

def sanitize_filename(name):
    """
    替换 Windows 系统中不允许使用的文件名字符。
    :param name: 原始文件名。
    :return: 替换后的文件名。
    """
    return name.replace('/', '／').replace('?', '？').replace('<', '＜')\
               .replace('>', '＞').replace(':', '：').replace('*', '＊')\
               .replace('"', '＂').replace('\\', '＼').replace('|', '｜')

def rename_files(source_folder, list_file):
    """
    根据 List 文件中的内容重命名文件夹中的文件（包括扩展名）。
    :param source_folder: 源文件夹路径。
    :param list_file: 包含新文件名（包括扩展名）的 List 文件路径。
    """
    try:
        # 读取新文件名列表
        with open(list_file, 'r', encoding='GB18030') as file:
            new_names = file.read().splitlines()

        # 获取源文件夹中的所有文件，并保持当前顺序
        files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]

        # 检查文件数量是否匹配
        if len(files) != len(new_names):
            print(f"错误：源文件夹中的文件数量 ({len(files)}) 与 List 文件中的名称数量 ({len(new_names)}) 不匹配。")
            return

        # 遍历文件并重命名
        for old_name, new_name in zip(files, new_names):
            sanitized_name = sanitize_filename(new_name.strip())  # 去除新名称两侧空格并替换非法字符
            
            # 获取完整路径
            old_path = os.path.join(source_folder, old_name)
            new_path = os.path.join(source_folder, sanitized_name)

            if old_path == new_path:
                print(f"文件 {old_name} 名称无需更改。")
                continue

            try:
                os.rename(old_path, new_path)
                print(f"文件 {old_name} 已成功重命名为 {sanitized_name}")
            except OSError as e:
                print(f"无法重命名文件 {old_name}，错误信息: {str(e)}")
    except FileNotFoundError as e:
        print(f"错误：文件未找到。{str(e)}")
    except Exception as e:
        print(f"发生未知错误：{str(e)}")

def main():
    """
    主函数：处理用户输入并执行文件重命名。
    """
    source_folder = input("请输入源文件夹的路径: ").strip()
    list_file = input("请输入包含文件名列表的 List 文件路径: ").strip()

    # 验证源文件夹路径是否有效
    if not os.path.isdir(source_folder):
        print(f"错误：提供的路径 {source_folder} 不是有效的文件夹路径。")
        return

    # 验证 List 文件路径是否有效
    if not os.path.isfile(list_file):
        print(f"错误：提供的路径 {list_file} 不是有效的文件路径。")
        return

    # 执行重命名操作
    rename_files(source_folder, list_file)

if __name__ == "__main__":
    main()

# 按下回车键退出。
input("按回车键退出...")