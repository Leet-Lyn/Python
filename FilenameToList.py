# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我文件夹位置，默认为“d:\\Works\\X\\”；目标文件夹位置，默认为“d:\\Works\\T\\”；询问我目标文件文件名，默认为“Links.txt”
# 在源文件夹内按照文件名排序依次读取文件的文件名，写入目标文件夹中的目标文中，如无此文件就生成一个。

# 导入模块
import os

def ask_input(prompt, default_value):
    """
    提示用户输入内容，若未输入则使用默认值。
    """
    user_input = input(f"{prompt}（默认值: {default_value}）: ").strip()
    return user_input if user_input else default_value

def write_filenames_to_file(source_folder, target_folder, target_file):
    """
    遍历源文件夹，按文件名排序将文件名写入目标文件中。
    """
    try:
        # 确保目标文件夹存在
        os.makedirs(target_folder, exist_ok=True)
        
        # 获取文件名列表并排序
        filenames = sorted(
            [file for file in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, file))]
        )
        
        # 目标文件完整路径
        target_file_path = os.path.join(target_folder, target_file)
        
        # 写入文件名到目标文件
        with open(target_file_path, 'w', encoding='utf-8') as f:
            for filename in filenames:
                f.write(filename + '\n')
        
        print(f"文件名已成功写入到目标文件：{target_file_path}")
    except Exception as e:
        print(f"处理过程中发生错误：{e}")

def main():
    # 获取源文件夹和目标文件夹路径
    source_folder = ask_input("请输入源文件夹位置", "d:\\Works\\X\\")
    target_folder = ask_input("请输入目标文件夹位置", "d:\\Works\\T\\")
    target_file = ask_input("请输入目标文件的文件名", "Links.txt")

    # 验证源文件夹是否存在
    if not os.path.isdir(source_folder):
        print(f"源文件夹不存在：{source_folder}")
        return
    
    # 调用函数写入文件名
    write_filenames_to_file(source_folder, target_folder, target_file)

    print("操作完成！")

if __name__ == "__main__":
    main()