# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我文件夹位置（默认“d:\\Works\\Targets\\”）与想要删除的字段（默认“（Via：”）。
# 将文件夹及其子文件夹内所有文件以文件内容读出重命名为文件名（不包括扩展名，最长 20 个字符）。
# 再文件夹及其子文件夹内所有文件重命名，从某一字段开始至末尾删除（不包括扩展名）。

# 导入模块
import os

def read_file_content(file_path, max_length=20):
    """
    读取文件内容作为新文件名（不包括扩展名）。
    :param file_path: 文件路径
    :param max_length: 文件名最大长度
    :return: 新文件名（不含扩展名），失败时返回None
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read().strip()
        
        # 移除换行符和多余空格
        content = ' '.join(content.split())
        
        # 截取指定长度
        if len(content) > max_length:
            content = content[:max_length]
        
        return content if content else None
    except Exception as e:
        print(f"无法读取文件内容 {file_path}：{e}")
        return None

def rename_by_content(folder):
    """
    遍历文件夹及其子文件夹内所有文件，根据文件内容重命名文件。
    :param folder: 文件夹路径
    """
    renamed_count = 0
    skipped_count = 0
    
    # 递归遍历所有文件
    for root, _, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            
            # 获取文件扩展名
            file_ext = os.path.splitext(file)[1]
            
            # 读取文件内容作为新文件名
            new_name = read_file_content(file_path)
            if not new_name:
                print(f"跳过文件（无法读取内容）：{file}")
                skipped_count += 1
                continue
            
            # 生成新文件名（保留原扩展名）
            new_file = new_name + file_ext
            new_file_path = os.path.join(root, new_file)
            
            # 检查是否存在同名文件，避免覆盖
            if os.path.exists(new_file_path):
                print(f"警告：目标文件 '{new_file}' 已存在，跳过重命名 '{file}'")
                skipped_count += 1
                continue
            
            try:
                os.rename(file_path, new_file_path)
                print(f"已将 '{file}' 重命名为 '{new_file}'")
                renamed_count += 1
            except Exception as e:
                print(f"错误：无法重命名文件 '{file}'，错误信息: {e}")
                skipped_count += 1
    
    print(f"\n内容重命名完成！共重命名 {renamed_count} 个文件，跳过 {skipped_count} 个文件。")
    return renamed_count

def remove_field_from_filenames(folder, field):
    """
    遍历文件夹及其子文件夹内所有文件，删除文件名中指定字段后的部分。
    :param folder: 文件夹路径
    :param field: 要删除的字段
    """
    renamed_count = 0
    skipped_count = 0
    
    # 递归遍历所有文件
    for root, _, files in os.walk(folder):
        for file in files:
            file_path = os.path.join(root, file)
            
            # 检查文件名是否包含指定字段
            if field in file:
                try:
                    # 获取字段在文件名中的位置
                    index = file.index(field)
                    # 获取文件名的前缀和后缀
                    prefix = file[:index]
                    suffix = os.path.splitext(file)[1]
                    # 生成新的文件名
                    new_file = prefix + suffix
                    new_file_path = os.path.join(root, new_file)

                    # 检查是否存在同名文件，避免覆盖
                    if os.path.exists(new_file_path):
                        print(f"警告：目标文件 '{new_file}' 已存在，跳过重命名 '{file}'")
                        skipped_count += 1
                        continue

                    # 重命名文件
                    os.rename(file_path, new_file_path)
                    print(f"已将 '{file}' 重命名为 '{new_file}'")
                    renamed_count += 1

                except Exception as e:
                    print(f"错误：无法重命名文件 '{file}'，错误信息: {e}")
                    skipped_count += 1
            else:
                print(f"跳过文件：'{file}'（不包含字段 '{field}'）")
                skipped_count += 1
    
    print(f"\n字段删除完成！共重命名 {renamed_count} 个文件，跳过 {skipped_count} 个文件。")
    return renamed_count

def main():
    """
    主函数：获取用户输入并调用重命名函数。
    """
    print("欢迎使用文件批量重命名工具！")
    
    # 设置默认值
    default_folder = "d:\\Works\\Targets\\"
    default_field = "（Via："
    
    # 获取文件夹路径
    folder = input(f"请输入文件夹路径（按回车使用默认值：{default_folder}）：").strip()
    if not folder:
        folder = default_folder
    
    # 获取要删除的字段
    field = input(f"请输入想要删除的字段（按回车使用默认值：{default_field}）：").strip()
    if not field:
        field = default_field

    # 验证文件夹是否存在
    if not os.path.isdir(folder):
        print(f"错误：文件夹 '{folder}' 不存在或不是有效的文件夹。")
        return
    
    # 确认操作
    print(f"\n即将处理文件夹：{folder}")
    print("将执行以下操作：")
    print("1. 根据文件内容重命名文件（文件名最长20个字符）")
    print(f"2. 删除文件名中 '{field}' 及其后面的内容")
    confirm = input("确认执行操作？(y/n): ").strip().lower()
    
    if confirm != 'y':
        print("操作已取消。")
        return
    
    # 第一步：根据文件内容重命名
    print("\n=== 第一步：根据文件内容重命名 ===")
    content_renamed = rename_by_content(folder)
    
    # 第二步：删除指定字段后的内容
    print("\n=== 第二步：删除指定字段后的内容 ===")
    field_renamed = remove_field_from_filenames(folder, field)
    
    print(f"\n操作完成！")
    print(f"内容重命名：{content_renamed} 个文件")
    print(f"字段删除：{field_renamed} 个文件")

if __name__ == "__main__":
    main()
    input("按回车键退出...")