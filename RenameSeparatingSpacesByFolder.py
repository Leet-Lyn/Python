# 请帮我写个中文的 Python 脚本，批注也是中文：
# 请输入源文件夹位置（默认“e:\\Documents\\Literatures\\Webpages\\”）
# 重命名源文件夹下所有文件及子文件夹下文件。
# 使中文、英文、数字之间用空格隔开。

# 导入模块
import os
import re

def process_filename(filename):
    """
    处理文件名，在中英文、数字之间添加空格
    
    参数:
        filename: 原始文件名（不含路径）
    
    返回:
        处理后的文件名
    """
    # 分离文件名和扩展名
    name, ext = os.path.splitext(filename)
    
    # 定义正则表达式模式
    # 匹配中文、英文、数字之间的边界
    pattern = r'([a-zA-Z0-9])([\u4e00-\u9fff])|([\u4e00-\u9fff])([a-zA-Z0-9])'
    
    # 替换函数：在匹配的位置添加空格
    def add_space(match):
        groups = match.groups()
        if groups[0] and groups[1]:  # 英文/数字在前，中文在后
            return groups[0] + ' ' + groups[1]
        elif groups[2] and groups[3]:  # 中文在前，英文/数字在后
            return groups[2] + ' ' + groups[3]
        return match.group()
    
    # 应用替换
    processed_name = re.sub(pattern, add_space, name)
    
    # 返回处理后的文件名（包含扩展名）
    return processed_name + ext

def rename_files_in_directory(directory_path):
    """
    遍历目录及其子目录，重命名所有文件
    
    参数:
        directory_path: 要处理的目录路径
    """
    # 检查目录是否存在
    if not os.path.exists(directory_path):
        print(f"错误：目录 '{directory_path}' 不存在")
        return
    
    # 统计重命名的文件数量
    rename_count = 0
    
    # 遍历目录及其所有子目录
    for root, dirs, files in os.walk(directory_path):
        for filename in files:
            # 获取文件的完整路径
            old_path = os.path.join(root, filename)
            
            # 处理文件名
            new_filename = process_filename(filename)
            
            # 如果文件名有变化，则进行重命名
            if new_filename != filename:
                new_path = os.path.join(root, new_filename)
                
                try:
                    # 检查新文件名是否已存在
                    if os.path.exists(new_path):
                        print(f"警告：文件 '{new_filename}' 已存在，跳过重命名 '{filename}'")
                        continue
                    
                    # 执行重命名
                    os.rename(old_path, new_path)
                    print(f"重命名: '{filename}' -> '{new_filename}'")
                    rename_count += 1
                    
                except Exception as e:
                    print(f"重命名文件 '{filename}' 时出错: {e}")
    
    print(f"\n完成！共重命名了 {rename_count} 个文件")

def main():
    """
    主函数：获取用户输入并执行重命名操作
    """
    # 获取用户输入的目录路径
    default_path = "e:\\Documents\\Literatures\\Webpages\\"
    user_input = input(f"请输入源文件夹位置（默认: {default_path}）: ").strip()
    
    # 使用用户输入或默认路径
    directory_path = user_input if user_input else default_path
    
    rename_files_in_directory(directory_path)

if __name__ == "__main__":
    main()