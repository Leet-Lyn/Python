# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我文件夹位置，默认为“d:\\Works\\X\\”；目标文件位置，默认为“d:\\Works\\0\\Lists.txt”。
# 将源文件夹及其子文件夹内所有文件，按照绝对路径排序。依次将绝对路径（包括文件名、扩展名），写入目标列表文件中，如无这列表文件就生成一个。

# 导入模块
import os

def write_absolute_filepaths_to_file(source_folder, target_file):
    """
    递归遍历源文件夹及其子文件夹，按绝对路径排序将文件绝对路径（包括文件名、扩展名）写入目标文件中。
    :param source_folder: 源文件夹路径
    :param target_file: 目标文件完整路径
    """
    try:
        # 确保目标文件的目录存在
        target_dir = os.path.dirname(target_file)
        if target_dir:  # 如果目标文件路径包含目录
            os.makedirs(target_dir, exist_ok=True)
        
        # 收集所有文件的绝对路径
        absolute_paths = []
        
        # 递归遍历源文件夹及其所有子文件夹
        for root, dirs, files in os.walk(source_folder):
            for file in files:
                # 获取文件的绝对路径
                absolute_path = os.path.abspath(os.path.join(root, file))
                absolute_paths.append(absolute_path)
        
        # 按绝对路径排序
        absolute_paths.sort()
        
        # 写入文件绝对路径到目标文件
        with open(target_file, 'w', encoding='utf-8') as f:
            for absolute_path in absolute_paths:
                f.write(absolute_path + '\n')
        
        print(f"文件绝对路径已成功写入到目标文件：{target_file}")
        print(f"共写入 {len(absolute_paths)} 个文件路径")
        
    except Exception as e:
        print(f"处理过程中发生错误：{e}")

def main():
    """
    主函数：获取用户输入并执行文件绝对路径导出操作。
    """
    # 设置默认路径
    default_source_folder = "d:\\Works\\X\\"
    default_target_file = "d:\\Works\\0\\Lists.txt"
    
    # 获取用户输入
    source_folder = input(f"请输入源文件夹位置（按回车使用默认值：{default_source_folder}）：").strip()
    if not source_folder:
        source_folder = default_source_folder
    
    target_file = input(f"请输入目标文件位置（按回车使用默认值：{default_target_file}）：").strip()
    if not target_file:
        target_file = default_target_file

    # 验证源文件夹是否存在
    if not os.path.isdir(source_folder):
        print(f"错误：源文件夹不存在：{source_folder}")
        return
    
    # 调用函数写入文件绝对路径
    write_absolute_filepaths_to_file(source_folder, target_file)

    # 等待用户确认退出
    input("操作完成，按回车键退出...")

if __name__ == "__main__":
    main()