# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件位置，默认为“d:\Downloads\”。
# 将文件夹下的所有文件夹内（包括子文件夹）的文件上移到文件的父文件夹中。

# 导入模块。
import os
import shutil

def move_files_to_parent_directory(source_dir):
    """
    将文件夹内（包括子文件夹）的所有文件移动到其父文件夹。
    """
    for root, dirs, files in os.walk(source_dir, topdown=False):  # 使用 topdown=False，从子目录向父目录遍历
        for file in files:
            file_path = os.path.join(root, file)  # 文件的完整路径
            parent_dir = os.path.dirname(root)  # 当前目录的父文件夹路径
            new_path = os.path.join(parent_dir, file)  # 文件移动后的新路径

            # 如果目标文件已经存在，避免覆盖，调整文件名
            while os.path.exists(new_path):
                base, ext = os.path.splitext(file)
                file = f"{base}_moved{ext}"  # 重命名，避免文件名冲突
                new_path = os.path.join(parent_dir, file)

            try:
                shutil.move(file_path, new_path)  # 移动文件
                print(f"文件已移动: {file_path} -> {new_path}")
            except Exception as e:
                print(f"无法移动文件: {file_path} -> {new_path}. 错误: {e}")

        # 如果当前文件夹为空，尝试删除
        try:
            if not os.listdir(root):  # 检查文件夹是否为空
                os.rmdir(root)
                print(f"已删除空文件夹: {root}")
        except Exception as e:
            print(f"无法删除文件夹: {root}. 错误: {e}")

def main():
    """
    主函数：处理用户输入并调用文件移动函数。
    """
    source_dir = input("请输入源文件夹位置（默认为'd:\\Downloads\\'）：").strip('"') or "d:\\Downloads\\"

    if not os.path.isdir(source_dir):
        print("提供的路径不是有效的文件夹路径，请检查后重试。")
        return

    move_files_to_parent_directory(source_dir)
    print("所有文件已移动完成。")

if __name__ == "__main__":
    main()

# 按下回车键退出。
input("按回车键退出...")
