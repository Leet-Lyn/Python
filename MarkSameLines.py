# 请帮我写个中文的 Python 脚本，批注也是中文：
# 询问我 txt 文件位置。读取该 txt 文件。
# 遍历该 txt 文件所有行。每发现有某个行与前面的行相同就在行首打上“# ”。

# 导入模块
import os

def process_file(file_path):
    """
    处理给定的 txt 文件，为重复行添加注释。
    """
    try:
        # 检查文件是否存在
        if not os.path.isfile(file_path):
            print("文件不存在，请检查路径是否正确。")
            return

        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # 记录已处理的行
        seen_lines = set()
        processed_lines = []

        # 遍历每一行
        for line in lines:
            stripped_line = line.strip()  # 去掉首尾空白字符，避免影响比较
            if stripped_line in seen_lines:
                # 如果该行已出现过，添加注释标记
                processed_lines.append(f"# {line}")
            else:
                # 如果是新行，加入已处理集合
                seen_lines.add(stripped_line)
                processed_lines.append(line)

        # 将处理后的内容写回文件
        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(processed_lines)

        print("文件处理完成，重复的行已添加注释。")

    except Exception as e:
        print(f"处理文件时出错：{e}")

def main():
    """
    主程序入口，处理用户输入。
    """
    # 询问用户输入文件路径
    file_path = input("请输入 txt 文件的路径：").strip()
    process_file(file_path)
    input("按回车键退出...")

if __name__ == "__main__":
    main()