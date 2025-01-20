# 复制文件夹内所有文件的文件名生成空文件。

# 导入模块
import os

def create_empty_files(source_folder, target_folder):
    """
    根据源文件夹内文件的文件名，在目标文件夹中生成对应的空文件。
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
    for file_name in os.listdir(source_folder):
        source_file = os.path.join(source_folder, file_name)
        
        # 判断是否是文件
        if os.path.isfile(source_file):
            # 拼接目标文件的完整路径
            target_file = os.path.join(target_folder, file_name)
            
            # 创建一个空文件
            try:
                open(target_file, "w").close()
                print(f"已复制文件名 '{file_name}' 到目标文件夹中。")
            except Exception as e:
                print(f"创建文件 '{file_name}' 时发生错误：{e}")
        else:
            print(f"跳过非文件项：'{file_name}'")

def main():
    # 询问用户源文件夹路径
    source_folder = input("请输入源文件夹路径（按回车则为“T:\\Temps\\”）：").strip() or "T:\\Temps\\"
    # 询问用户目标文件夹路径
    target_folder = input("请输入目标文件夹路径（按回车则为“T:\\XXX\\”）：").strip() or "T:\\XXX\\"

    if not source_folder or not target_folder:
        print("源文件夹和目标文件夹路径不能为空！")
        return

    # 调用函数创建空文件
    create_empty_files(source_folder, target_folder)
    print("操作完成！")

if __name__ == "__main__":
    main()
    input("按回车键退出...")