# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件夹位置（默认是：d:\\Works\\Downloads\\）。
# 遍历源文件夹位置中所有文件，对文件名（不包括后缀名）进行重命名，要求如下：
# 中文字符与英文单词之间要有空格。将 "-" 替换为 " "；将连续三个空格替换为 " - "。

# 导入模块
import os
import re

def get_valid_directory():
    """
    获取有效的文件夹路径，支持默认值。
    """
    default_folder = "d:\\Works\\Downloads\\"
    prompt = f"请输入源文件夹位置（默认是：{default_folder}，直接回车使用默认值）："
    
    while True:
        folder = input(prompt).strip()
        
        # 如果用户直接回车，使用默认值
        if not folder:
            folder = default_folder
        
        # 去除可能的首尾引号
        folder = folder.strip('"\'')
        
        if os.path.isdir(folder):
            return folder
        print(f"输入的路径无效：{folder}，请重新输入。")

def add_space_between_chinese_and_english(filename):
    """
    在中文字符与英文/数字之间添加空格，处理文件名中的特殊格式。
    """
    # 中文字符与英文/数字之间添加空格
    filename = re.sub(r'([一-龥])([A-Za-z0-9])', r'\1 \2', filename)
    filename = re.sub(r'([A-Za-z0-9])([一-龥])', r'\1 \2', filename)
    
    # 将 "-" 替换为 " "
    filename = filename.replace("-", " ")
    
    # 将连续三个空格替换为 " - "
    filename = re.sub(r'\s{3,}', ' - ', filename)
    
    # 清除首尾多余的空格
    filename = filename.strip()
    return filename

def rename_files_in_directory(source_folder):
    """
    遍历源文件夹中的所有文件，并对文件名进行重命名。
    """
    files_processed = 0  # 记录处理的文件数量
    
    for root, _, files in os.walk(source_folder):
        for file in files:
            # 获取文件名和扩展名
            filename, extension = os.path.splitext(file)
            
            # 修改文件名
            new_filename = add_space_between_chinese_and_english(filename) + extension
            
            # 构建原文件和新文件的完整路径
            old_file_path = os.path.join(root, file)
            new_file_path = os.path.join(root, new_filename)
            
            # 如果新旧文件名不同，才进行重命名
            if old_file_path != new_file_path:
                try:
                    os.rename(old_file_path, new_file_path)
                    print(f"文件已重命名：\n  原文件名：{file}\n  新文件名：{new_filename}")
                    files_processed += 1
                except Exception as e:
                    print(f"重命名文件失败：{file}，错误：{e}")
    
    if files_processed == 0:
        print("没有需要处理的文件。")
    else:
        print(f"所有文件处理完成，共处理了 {files_processed} 个文件。")

def main():
    """
    主程序入口。
    """
    print("=== 文件名批量重命名工具 ===")
    source_folder = get_valid_directory()
    print(f"使用的源文件夹：{source_folder}")
    rename_files_in_directory(source_folder)
    input("按回车键退出程序...")

if __name__ == "__main__":
    main()