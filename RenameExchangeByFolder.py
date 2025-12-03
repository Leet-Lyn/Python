# 请帮我写个中文的 Python 脚本，批注也是中文：
# 请输入源文件夹位置（默认“d:\Downloads\”），同时询问分隔符是什么（分隔符可以是字符串，默认是“ - ”）。
# 重命名源文件夹下所有文件及子文件夹下文件。
# 将文件名（不包括扩展名）中分隔符两端交换。如果有多个相同的分隔符，则只交换一次。

# 导入模块
import os

def swap_separator_sides(filename, separator):
    """
    将文件名中分隔符两侧的内容交换位置
    只处理第一个出现的分隔符
    """
    if separator in filename:
        # 找到第一个分隔符的位置
        pos = filename.find(separator)
        
        # 分割成三部分：左侧、分隔符、右侧
        left_part = filename[:pos]
        right_part = filename[pos + len(separator):]
        
        # 交换左右两侧
        return right_part + separator + left_part
    return filename

def rename_file(file_path, separator):
    """
    处理单个文件的重命名
    """
    # 分离目录路径、文件名和扩展名
    directory, full_filename = os.path.split(file_path)
    filename, extension = os.path.splitext(full_filename)
    
    # 交换分隔符两侧内容（仅文件名部分，不包括扩展名）
    new_filename = swap_separator_sides(filename, separator)
    
    # 如果文件名没有变化，跳过
    if new_filename == filename:
        return None
    
    # 构建新的完整文件名（包含扩展名）
    new_full_filename = new_filename + extension
    new_file_path = os.path.join(directory, new_full_filename)
    
    # 避免文件名冲突
    counter = 1
    original_new_file_path = new_file_path
    while os.path.exists(new_file_path):
        new_full_filename = f"{new_filename}_{counter}{extension}"
        new_file_path = os.path.join(directory, new_full_filename)
        counter += 1
    
    return new_file_path

def traverse_and_rename(source_folder, separator):
    """
    递归遍历文件夹及其子文件夹，重命名所有文件
    """
    renamed_count = 0
    skipped_count = 0
    error_count = 0
    
    for root_dir, subfolders, files in os.walk(source_folder):
        for filename in files:
            original_path = os.path.join(root_dir, filename)
            
            try:
                new_path = rename_file(original_path, separator)
                
                if new_path:
                    # 执行重命名
                    os.rename(original_path, new_path)
                    renamed_count += 1
                    print(f"✓ 重命名: {filename} -> {os.path.basename(new_path)}")
                else:
                    skipped_count += 1
                    
            except Exception as e:
                error_count += 1
                print(f"✗ 处理文件失败 {filename}: {e}")
    
    return renamed_count, skipped_count, error_count

def main():
    """
    主函数：获取用户输入并执行重命名操作
    """
    # 获取源文件夹位置
    source_folder = input("请输入源文件夹位置（默认：d:\\Downloads\\）: ").strip()
    if not source_folder:
        source_folder = r"d:\Downloads"
    
    # 检查文件夹是否存在
    if not os.path.exists(source_folder):
        print(f"错误：文件夹 '{source_folder}' 不存在！")
        return
    
    if not os.path.isdir(source_folder):
        print(f"错误：'{source_folder}' 不是有效的文件夹！")
        return
    
    # 获取分隔符（设置默认值为" - "）
    separator_input = input("请输入分隔符（可以是任意字符串，默认是\" - \"）: ").strip()
    if not separator_input:
        separator = " - "
    else:
        separator = separator_input
    
    print(f"\n开始处理文件夹: {source_folder}")
    print(f"使用分隔符: '{separator}'")
    print("=" * 50)
    
    # 执行重命名操作（无需确认）
    renamed, skipped, errors = traverse_and_rename(source_folder, separator)
    
    print("=" * 50)
    print("处理完成！")
    print(f"已重命名: {renamed} 个文件")
    print(f"跳过: {skipped} 个文件")
    print(f"错误: {errors} 个文件")

if __name__ == "__main__":
    try:
        main()
        input("\n按 Enter 键退出...")
    except KeyboardInterrupt:
        print("\n\n操作被用户中断。")
    except Exception as e:
        print(f"\n程序发生错误: {e}")