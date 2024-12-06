# 遍历源文件夹下所有文件，将所有文件移动到以该文件修改时间命名的子文件中。

# 导入模块。
import os
import shutil
from datetime import datetime

def organize_files(source_folder):
    """
    遍历源文件夹下的所有文件，将所有文件移动到以修改时间命名的子文件夹中。
    :param source_folder: 源文件夹路径
    """
    # 检查源文件夹是否存在且为有效文件夹
    if not os.path.isdir(source_folder):
        print(f"错误：指定的源文件夹 '{source_folder}' 不存在或不是有效的文件夹。")
        return

    # 遍历源文件夹中的所有文件和文件夹
    for filename in os.listdir(source_folder):
        file_path = os.path.join(source_folder, filename)

        # 跳过非文件（如子文件夹或隐藏文件）
        if not os.path.isfile(file_path) or filename.startswith('.'):
            print(f"跳过非文件或隐藏文件: {filename}")
            continue

        try:
            # 获取文件的修改时间并格式化为目标文件夹名称
            modified_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            target_folder = os.path.join(source_folder, modified_time.strftime("[%Y-%m-%d]"))

            # 创建目标文件夹（如果不存在）
            os.makedirs(target_folder, exist_ok=True)

            # 移动文件到目标文件夹
            shutil.move(file_path, os.path.join(target_folder, filename))
            print(f"已移动文件 '{filename}' 到 '{target_folder}'。")

        except Exception as e:
            print(f"错误：无法移动文件 '{filename}'，错误信息: {e}")

def main():
    """
    主函数：获取用户输入并调用文件整理功能。
    """
    print("欢迎使用文件整理工具！")
    source_folder = input("请输入源文件夹路径: ").strip()

    if not source_folder:
        print("错误：输入路径不能为空，请重新运行程序并输入有效路径。")
        return

    # 调用整理文件的函数
    organize_files(source_folder)
    print("文件整理完成！")

if __name__ == "__main__":
    main()
    input("按回车键退出...")