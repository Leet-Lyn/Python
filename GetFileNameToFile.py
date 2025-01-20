# 获取文件夹下所有文件名，到一个文件内。

# 导入模块
import os

def get_all_filenames(folder, output_file):
    """
    获取文件夹下所有文件的完整路径并保存到文件中。
    """
    # 检查文件夹是否存在
    if not os.path.exists(folder):
        print(f"文件夹 '{folder}' 不存在。")
        return
    
    # 确保输出文件所在目录存在
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"输出文件夹 '{output_dir}' 不存在，已创建。")

    # 打开输出文件并写入所有文件路径
    with open(output_file, "w", encoding="utf-8") as f:
        for root, _, files in os.walk(folder):
            for name in files:
                file_path = os.path.join(root, name)
                f.write(file_path + "\n")
        print(f"已将文件夹 '{folder}' 中的所有文件名保存到 '{output_file}' 中。")

def main():
    # 用户输入文件夹路径
    folder = input("请输入要获取文件名的文件夹路径（默认当前文件夹）：").strip() or os.getcwd()
    # 用户输入输出文件名
    filename = input("请输入保存文件名的文件名（默认 'files.txt'）：").strip() or "files.txt"
    # 用户输入输出文件路径
    path = input("请输入保存文件的路径（默认 't:\\X\\'）：").strip() or "t:\\X\\"
    # 拼接完整输出文件路径
    output_file = os.path.join(path, filename)

    # 调用函数处理
    get_all_filenames(folder, output_file)

    # 提示完成
    input("操作完成！按回车键退出...")

if __name__ == "__main__":
    main()