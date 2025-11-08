# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件夹位置（默认为“d:\\Works\\X\\”）。获取文件夹下所有文件名（包括扩展名），写到到一个文件内（默认为“d:\Works\0\files.txt”）。

# 导入模块
import os

def get_all_filenames(folder, output_file):
    """
    获取文件夹下所有文件的完整路径并保存到文件中。
    :param folder: 要遍历的文件夹路径
    :param output_file: 输出文件路径
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
    folder = input("请输入要获取文件名的文件夹路径（默认为'd:\\Works\\X\\'）：").strip() or "d:\\Works\\X\\"
    
    # 用户输入输出文件路径
    output_file = input("请输入保存文件名的文件路径（默认为'd:\\Works\\0\\files.txt'）：").strip() or "d:\\Works\\0\\files.txt"

    # 调用函数处理
    get_all_filenames(folder, output_file)

    # 提示完成
    input("操作完成！按回车键退出...")

if __name__ == "__main__":
    main()