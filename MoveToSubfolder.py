# 遍历源文件夹下所有文件，将所有文件移动到以该文件名字命名的子文件中。

# 导入模块。
import os
import shutil

def organize_files_by_name(source_folder):
    """
    遍历源文件夹下的所有文件，将所有文件移动到以文件名（不含扩展名）命名的子文件夹中。
    :param source_folder: 源文件夹路径
    """
    # 验证源文件夹是否存在
    if not os.path.isdir(source_folder):
        print(f"错误：源文件夹 '{source_folder}' 不存在或不是有效的文件夹。")
        return

    # 遍历源文件夹下的所有文件
    for root, dirs, files in os.walk(source_folder):
        for file_name in files:
            # 跳过隐藏文件（以 '.' 开头的文件）
            if file_name.startswith('.'):
                print(f"跳过隐藏文件: {file_name}")
                continue

            # 构建源文件的完整路径
            source_file_path = os.path.join(root, file_name)

            # 构建目标文件夹路径，以文件名（不含扩展名）命名
            file_base_name = os.path.splitext(file_name)[0]
            target_folder_path = os.path.join(source_folder, file_base_name)

            try:
                # 创建目标文件夹（如果不存在）
                os.makedirs(target_folder_path, exist_ok=True)

                # 构建目标文件路径
                target_file_path = os.path.join(target_folder_path, file_name)

                # 移动文件到目标位置
                shutil.move(source_file_path, target_file_path)
                print(f"文件 '{file_name}' 已移动到子文件夹 '{target_folder_path}'。")

            except Exception as e:
                print(f"错误：无法移动文件 '{file_name}'，错误信息: {e}")

def main():
    """
    主函数：获取用户输入并调用文件整理函数。
    """
    print("欢迎使用文件整理工具！")
    default_folder = "t:\\XXX\\"
    source_folder = input(f"请输入需整理的文件夹路径（按回车键使用默认地址：{default_folder}）: ").strip() or default_folder

    # 调用文件整理函数
    organize_files_by_name(source_folder)

    print("文件整理完成！")

if __name__ == "__main__":
    main()
    input("按回车键退出...")