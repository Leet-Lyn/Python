# 获取文件夹下所有文件夹名，到一个文件内。

# 导入模块
import os

def save_folder_names(folder, output_path):
    """
    获取指定文件夹下所有子文件夹名，并将结果写入指定文件中。
    :param folder: 要获取文件夹名的目标文件夹路径
    :param output_path: 保存文件夹名的目标文件路径
    """
    try:
        # 创建保存路径的文件夹（如果不存在）
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # 写入文件夹名称
        with open(output_path, 'w', encoding='utf-8') as f:
            for root, dirs, files in os.walk(folder):
                for dir_name in dirs:
                    folder_path = os.path.join(root, dir_name)
                    f.write(folder_path + '\n')
        print(f"文件夹名称已成功保存到 '{output_path}'。")

    except Exception as e:
        print(f"错误：无法保存文件夹名称，错误信息: {e}")

def main():
    """
    主函数：获取用户输入并调用保存文件夹名称的函数。
    """
    print("欢迎使用文件夹名称提取工具！")

    # 获取目标文件夹路径
    folder = input("请输入要获取文件夹名的文件夹路径（默认当前文件夹）：").strip()
    if not folder:
        folder = os.getcwd()

    # 获取输出文件名
    filename = input("请输入保存文件名的文件名（默认是“files.txt”）：").strip()
    if not filename:
        filename = "files.txt"

    # 获取输出文件存放路径
    path = input("请输入保存文件名的文件的存放位置（默认是“t:\\X\\”）：").strip()
    if not path:
        path = "t:\\X\\"

    # 构建完整的输出文件路径
    output_path = os.path.join(path, filename)

    # 验证目标文件夹路径
    if not os.path.isdir(folder):
        print(f"错误：指定的目标文件夹 '{folder}' 不存在或不是有效的文件夹。")
        return

    # 调用保存文件夹名称的函数
    save_folder_names(folder, output_path)

if __name__ == "__main__":
    main()
    input("操作完成！按回车键退出...")