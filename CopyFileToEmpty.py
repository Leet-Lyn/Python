# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件夹位置（默认“d:\\Works\\In\\”）与目标文件夹位置（默认“d:\\Works\\Out\\”）。
# 复制源文件夹位置内所有文件的文件名生成空文件到目标文件夹。

# 导入模块
import os

def create_empty_files(source_folder, target_folder):
    """
    根据源文件夹内文件的文件名，在目标文件夹中生成对应的空文件。
    :param source_folder: 源文件夹路径
    :param target_folder: 目标文件夹路径
    """
    # 检查源文件夹是否存在
    if not os.path.exists(source_folder):
        print(f"源文件夹 '{source_folder}' 不存在。")
        return

    # 检查目标文件夹是否存在，不存在则创建
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
        print(f"目标文件夹 '{target_folder}' 不存在，已创建。")

    # 遍历源文件夹内所有文件
    file_count = 0
    for file_name in os.listdir(source_folder):
        source_file = os.path.join(source_folder, file_name)
        
        # 判断是否是文件
        if os.path.isfile(source_file):
            # 拼接目标文件的完整路径
            target_file = os.path.join(target_folder, file_name)
            
            # 创建一个空文件
            try:
                open(target_file, "w").close()
                print(f"已创建空文件：'{file_name}'")
                file_count += 1
            except Exception as e:
                print(f"创建文件 '{file_name}' 时发生错误：{e}")
        else:
            print(f"跳过非文件项：'{file_name}'")
    
    print(f"共创建 {file_count} 个空文件")

def main():
    """
    主函数：获取用户输入并执行空文件创建操作。
    """
    # 设置默认路径
    default_source = "d:\\Works\\In\\"
    default_target = "d:\\Works\\Out\\"
    
    # 获取用户输入
    source_folder = input(f"请输入源文件夹位置（按回车使用默认值：{default_source}）：").strip()
    if not source_folder:
        source_folder = default_source
        
    target_folder = input(f"请输入目标文件夹位置（按回车使用默认值：{default_target}）：").strip()
    if not target_folder:
        target_folder = default_target

    # 调用函数创建空文件
    create_empty_files(source_folder, target_folder)
    
    # 等待用户确认退出
    input("操作完成，按回车键退出...")

if __name__ == "__main__":
    main()