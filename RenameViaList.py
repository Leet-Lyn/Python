# 请帮我写个中文的 Python 脚本，批注也是中文：
# 询问为源文件夹路径（默认“d:\\Works\\Targets\\”）与列表路径（默认“d:\\Works\\0\\Lists.txt”）。
# 根据 List 文件里的文件名（包含扩展名），重命名文件夹里的路径（按名称排序）。

# 导入模块
import os
import chardet  # 用于检测文件编码

def detect_encoding(file_path):
    """
    检测文件的编码格式。
    :param file_path: 文件路径
    :return: 检测到的编码格式
    """
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result.get('encoding', 'utf-8')  # 默认返回 'utf-8'

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
        # 检测并读取文件的实际编码
        encoding = detect_encoding(list_file)
        print(f"检测到 List 文件编码为: {encoding}")

        # 读取新文件名列表
        with open(list_file, 'r', encoding=encoding) as file:
            new_names = file.read().splitlines()

        # 获取源文件夹中的所有文件，并按文件名排序
        files = sorted(
            [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]
        )

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

            # 检查新旧路径是否相同
            if old_path == new_path:
                print(f"文件 {old_name} 名称无需更改。")
                continue

            try:
                os.rename(old_path, new_path)
                print(f"文件 {old_name} 已成功重命名为 {sanitized_name}")
            except FileExistsError:
                print(f"文件 {sanitized_name} 已存在，跳过重命名 {old_name}。")
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
    # 设置默认路径
    default_source_folder = "d:\\Works\\Targets\\"
    default_list_file = "d:\\Works\\0\\Lists.txt"
    
    # 获取用户输入，使用默认值如果用户直接按回车
    source_folder = input(f"请输入源文件夹的路径（按回车使用默认值：{default_source_folder}）: ").strip()
    if not source_folder:
        source_folder = default_source_folder
    
    list_file = input(f"请输入包含文件名列表的 List 文件路径（按回车使用默认值：{default_list_file}）: ").strip()
    if not list_file:
        list_file = default_list_file

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

# 提示用户按下回车键退出程序
input("按回车键退出...")