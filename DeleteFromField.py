# 对文件夹内所有文件名重命名。从某一字段开始至末尾删除。

# 导入模块
import os

def rename_files(folder, field):
    """
    遍历指定文件夹内的所有文件，将文件名中指定字段后的部分删除。
    :param folder: 文件夹路径
    :param field: 要删除的字段
    """
    try:
        # 验证文件夹是否存在
        if not os.path.isdir(folder):
            print(f"错误：文件夹 '{folder}' 不存在或不是有效的文件夹。")
            return

        # 遍历文件夹内所有文件
        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)

            # 跳过文件夹，仅处理文件
            if os.path.isfile(file_path) and field in file:
                try:
                    # 获取字段在文件名中的位置
                    index = file.index(field)
                    # 获取文件名的前缀和后缀
                    prefix = file[:index]
                    suffix = os.path.splitext(file)[1]
                    # 生成新的文件名
                    new_file = prefix + suffix
                    new_file_path = os.path.join(folder, new_file)

                    # 检查是否存在同名文件，避免覆盖
                    if os.path.exists(new_file_path):
                        print(f"警告：目标文件 '{new_file}' 已存在，跳过重命名。")
                        continue

                    # 重命名文件
                    os.rename(file_path, new_file_path)
                    print(f"已将 '{file}' 重命名为 '{new_file}'")

                except Exception as e:
                    print(f"错误：无法重命名文件 '{file}'，错误信息: {e}")
            else:
                print(f"跳过文件：'{file}'（不包含字段 '{field}' 或不是文件）。")

    except Exception as e:
        print(f"错误：操作失败，错误信息: {e}")

def main():
    """
    主函数：获取用户输入并调用重命名函数。
    """
    print("欢迎使用文件批量重命名工具！")

    # 获取文件夹路径
    folder = input("请输入文件夹路径（默认当前文件夹）：").strip() or os.getcwd()

    # 获取要删除的字段
    field = input("请输入想要删除的字段（默认“（Via：”）：").strip() or "（Via："

    # 调用重命名函数
    rename_files(folder, field)

    print("文件重命名操作完成！")

if __name__ == "__main__":
    main()
    input("按回车键退出...")