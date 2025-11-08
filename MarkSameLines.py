# 请帮我写个中文的 Python 脚本，批注也是中文：
# 询问我文件位置（可以是如何格式，默认是：d:\\Works\\0\\txt.txt）。以文本方式读取该文件。
# 遍历该 txt 文件所有行。每发现有某个行与前面的行相同就在行首打上“# ”。

# 导入模块
import os

def get_valid_file_path():
    """
    获取有效的文件路径，支持默认值。
    """
    default_file = "d:\\Works\\0\\txt.txt"
    prompt = f"请输入文件位置（默认是：{default_file}，直接回车使用默认值）："
    
    while True:
        file_path = input(prompt).strip()
        
        # 如果用户直接回车，使用默认值
        if not file_path:
            file_path = default_file
        
        # 去除可能的首尾引号
        file_path = file_path.strip('"\'')
        
        if os.path.isfile(file_path):
            return file_path
        print(f"文件不存在：{file_path}，请重新输入有效的文件路径。")

def process_file(file_path):
    """
    处理给定的文件，为重复行添加注释。
    """
    try:
        # 尝试多种编码方式读取文件
        encodings = ['utf-8', 'gbk', 'gb2312', 'latin-1']
        lines = None
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as file:
                    lines = file.readlines()
                print(f"成功使用 {encoding} 编码读取文件")
                break
            except UnicodeDecodeError:
                continue
        
        if lines is None:
            print("无法使用常见编码读取文件，请检查文件编码")
            return

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

        # 将处理后的内容写回文件，使用UTF-8编码保存
        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(processed_lines)

        print("文件处理完成，重复的行已添加注释。")

    except Exception as e:
        print(f"处理文件时出错：{e}")

def main():
    """
    主程序入口，处理用户输入。
    """
    print("=== 文件重复行标记工具 ===")
    
    # 获取文件路径
    file_path = get_valid_file_path()
    print(f"使用的文件：{file_path}")
    
    # 处理文件
    process_file(file_path)
    
    input("按回车键退出...")

if __name__ == "__main__":
    main()