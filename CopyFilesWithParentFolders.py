# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始，询问我文件名（不包括扩展名），源文件夹（默认：d:\Works\In\）与目标文件夹（默认：d:\Works\Out\）。
# 找到源文件夹及其子文件夹下所有同名文件（扩展名可以不同），连同其父文件夹（仅仅为文件夹，不包括其他文件）一同复制到目标文件夹。
# 完成后，反复循环我询问我文件名、源文件夹与目标文件夹。

# 导入模块
import os
import shutil

def main():
    # 默认路径
    DEFAULT_SRC = r'd:\Works\In'
    DEFAULT_DST = r'd:\Works\Out'

    print("脚本功能：查找源文件夹中所有指定文件名（不含扩展名）的文件，"
          "并连同其相对路径一同复制到目标文件夹。\n"
          "输入空文件名可退出程序。\n")

    while True:
        # 询问文件名（不含扩展名）
        file_name = input("请输入文件名（不含扩展名，直接回车退出）：").strip()
        if not file_name:
            print("未输入文件名，程序结束。")
            break

        # 询问源文件夹
        src_input = input(f"请输入源文件夹路径（默认：{DEFAULT_SRC}）：").strip()
        src_folder = src_input if src_input else DEFAULT_SRC
        # 规范化路径（去除末尾可能的斜杠）
        src_folder = os.path.normpath(src_folder)

        # 检查源文件夹是否存在
        if not os.path.isdir(src_folder):
            print(f"错误：源文件夹 '{src_folder}' 不存在，请重新输入。\n")
            continue

        # 询问目标文件夹
        dst_input = input(f"请输入目标文件夹路径（默认：{DEFAULT_DST}）：").strip()
        dst_folder = dst_input if dst_input else DEFAULT_DST
        dst_folder = os.path.normpath(dst_folder)

        # 如果目标文件夹不存在，则创建
        os.makedirs(dst_folder, exist_ok=True)

        print(f"\n正在搜索源文件夹 '{src_folder}' 及其子文件夹中所有以 '{file_name}' 为名的文件（任何扩展名）...")

        found_count = 0
        # 遍历源文件夹
        for root, dirs, files in os.walk(src_folder):
            for file in files:
                # 分离文件名和扩展名
                base_name, ext = os.path.splitext(file)
                # 比较时忽略大小写（Windows 习惯）
                if base_name.lower() == file_name.lower():
                    # 找到了匹配的文件
                    full_path = os.path.join(root, file)
                    # 计算相对于源文件夹的路径
                    rel_path = os.path.relpath(root, src_folder)
                    # 目标文件夹中的对应子目录
                    dest_dir = os.path.join(dst_folder, rel_path)
                    # 确保目标子目录存在
                    os.makedirs(dest_dir, exist_ok=True)
                    # 目标文件完整路径
                    dest_file = os.path.join(dest_dir, file)

                    # 复制文件（保留元数据）
                    shutil.copy2(full_path, dest_file)
                    print(f"已复制: {full_path} -> {dest_file}")
                    found_count += 1

        if found_count == 0:
            print("未找到任何匹配的文件。")
        else:
            print(f"总共复制了 {found_count} 个文件。\n")

        print("-" * 50)  # 分隔线，准备下一轮

if __name__ == "__main__":
    main()