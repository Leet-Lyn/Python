# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我文件夹位置，默认为“d:\\Works\\X\\”；目标文件位置，默认为“d:\\Works\\0\\Lists.txt”。
# 将源文件夹及其子文件夹内所有文件夹，按照相对路径排序。依次将绝对路径（仅仅针对文件夹），写入目标列表文件中，如无这列表文件就生成一个。

# 导入模块
import os

def save_folder_paths(source_folder, output_file):
    """
    获取指定文件夹下所有子文件夹的绝对路径，并按相对路径排序后写入文件。
    :param source_folder: 源文件夹路径
    :param output_file: 输出文件路径
    """
    try:
        # 确保输出文件的目录存在
        output_dir = os.path.dirname(output_file)
        if output_dir:  # 如果输出文件路径包含目录
            os.makedirs(output_dir, exist_ok=True)

        # 收集所有文件夹的绝对路径和相对路径
        folder_paths = []
        
        # 遍历所有子文件夹
        for root, dirs, files in os.walk(source_folder):
            # 添加当前目录（如果它不是源文件夹本身）
            if root != source_folder:
                folder_paths.append(root)
            
            # 添加当前目录下的所有子文件夹
            for dir_name in dirs:
                folder_path = os.path.join(root, dir_name)
                folder_paths.append(folder_path)
        
        # 去除重复项（因为某些文件夹可能会被多次添加）
        folder_paths = list(set(folder_paths))
        
        # 按相对路径排序（相对于源文件夹）
        folder_paths.sort(key=lambda x: os.path.relpath(x, source_folder).lower())
        
        # 写入文件夹绝对路径到输出文件
        with open(output_file, 'w', encoding='utf-8') as f:
            for folder_path in folder_paths:
                f.write(folder_path + '\n')
        
        print(f"文件夹绝对路径已成功保存到：{output_file}")
        print(f"共保存 {len(folder_paths)} 个文件夹路径")
        
    except Exception as e:
        print(f"错误：无法保存文件夹路径，错误信息: {e}")

def main():
    """
    主函数：获取用户输入并调用保存文件夹路径的函数。
    """
    print("欢迎使用文件夹路径提取工具！")

    # 设置默认路径
    default_source_folder = "d:\\Works\\X\\"
    default_output_file = "d:\\Works\\0\\Lists.txt"
    
    # 获取源文件夹路径
    source_folder = input(f"请输入源文件夹位置（按回车使用默认值：{default_source_folder}）：").strip()
    if not source_folder:
        source_folder = default_source_folder

    # 获取输出文件路径
    output_file = input(f"请输入目标文件位置（按回车使用默认值：{default_output_file}）：").strip()
    if not output_file:
        output_file = default_output_file

    # 验证源文件夹路径
    if not os.path.isdir(source_folder):
        print(f"错误：源文件夹 '{source_folder}' 不存在或不是有效的文件夹。")
        return

    # 调用保存文件夹路径的函数
    save_folder_paths(source_folder, output_file)
    
    # 等待用户确认退出
    input("操作完成，按回车键退出...")

if __name__ == "__main__":
    main()