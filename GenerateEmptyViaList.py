# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件位置与目标文件夹位置。
# 读取源文件每行，在目标文件夹位置生成空文件，文件名与读取的一致。

# 导入模块。
import os

def create_empty_files_from_source(source_file_path, target_folder_path):
    """
    根据源文件的每一行内容，在目标文件夹中创建同名的空文件。
    """
    try:
        # 检查源文件是否存在
        if not os.path.isfile(source_file_path):
            print("源文件不存在，请重新输入有效的文件路径。")
            return

        # 确保目标文件夹存在，如果不存在则创建
        if not os.path.exists(target_folder_path):
            os.makedirs(target_folder_path)
            print(f"目标文件夹不存在，已创建新文件夹：{target_folder_path}")

        # 读取源文件每行内容
        with open(source_file_path, 'r', encoding='utf-8') as source_file:
            lines = source_file.readlines()

        # 遍历每行生成空文件
        for line in lines:
            # 去除行首尾空白字符，包括换行符
            file_name = line.strip()

            # 跳过空行
            if not file_name:
                print("跳过空行。")
                continue

            # 构建目标文件路径
            file_path = os.path.join(target_folder_path, file_name)

            # 检查文件名是否有效
            if any(char in r'\/:*?"<>|' for char in file_name):
                print(f"无效文件名，已跳过：{file_name}")
                continue

            # 创建空文件
            with open(file_path, 'w', encoding='utf-8'):
                pass

            print(f"已生成空文件：{file_name}")

        print("所有文件已生成完成。")

    except Exception as e:
        print(f"处理过程中发生错误：{e}")

def main():
    """
    主函数：处理用户输入并调用文件生成函数。
    """
    # 询问源文件路径
    source_file_path = input("请输入源文件位置：").strip()

    # 询问目标文件夹路径
    target_folder_path = input("请输入目标文件夹位置：").strip()

    # 调用创建文件函数
    create_empty_files_from_source(source_file_path, target_folder_path)

    # 等待用户按回车键退出
    input("按回车键退出...")

if __name__ == "__main__":
    main()