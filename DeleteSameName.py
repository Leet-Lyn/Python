# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件夹位置与目标文件夹位置。
# 删除目标文件夹内与源文件夹同名的文件。 

# 导入必要模块
import os

def remove_duplicates(source_folder, target_folder):
    """
    删除目标文件夹内与源文件夹同名的文件。
    :param source_folder: 源文件夹路径。
    :param target_folder: 目标文件夹路径。
    """
    # 检查源文件夹和目标文件夹是否存在
    if not os.path.isdir(source_folder):
        print(f"错误：源文件夹 '{source_folder}' 不存在或不是有效的文件夹。")
        return
    if not os.path.isdir(target_folder):
        print(f"错误：目标文件夹 '{target_folder}' 不存在或不是有效的文件夹。")
        return

    # 获取目标文件夹中的文件名集合
    try:
        target_files = set(os.listdir(target_folder))
    except PermissionError:
        print(f"错误：无法访问目标文件夹 '{target_folder}'，权限不足。")
        return

    # 遍历源文件夹中的文件
    for file in os.listdir(source_folder):
        source_file_path = os.path.join(source_folder, file)
        # 确保处理的仅是文件
        if os.path.isfile(source_file_path):
            if file in target_files:
                try:
                    os.remove(source_file_path)
                    print(f"已从源文件夹中删除文件: {file}")
                except OSError as e:
                    print(f"错误：无法删除文件 '{file}'，错误信息: {e}")
        else:
            print(f"跳过非文件项目: {file}")

def main():
    """
    主函数：获取用户输入并调用删除重复文件的函数。
    """
    print("欢迎使用重复文件删除工具！")
    source_folder = input("请输入源文件夹路径: ").strip()
    target_folder = input("请输入目标文件夹路径: ").strip()

    if not source_folder or not target_folder:
        print("错误：输入路径不能为空，请重新运行程序并输入有效路径。")
        return

    # 调用删除重复文件的函数
    remove_duplicates(source_folder, target_folder)

if __name__ == "__main__":
    main()
    input("操作完成！按回车键退出...")