# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件位置（d:\\Works\\0\\files.txt）与目标文件夹位置（d:\\Works\\Targets\\）。
# 读取源文件每行，在目标文件夹位置生成空文件，文件名与读取的一致。

# 导入模块
import os

def get_valid_file_path(prompt, default_path):
    """
    获取有效的文件路径，支持默认值。
    """
    while True:
        path = input(prompt).strip()
        
        # 如果用户直接回车，使用默认值
        if not path:
            path = default_path
        
        # 去除可能的首尾引号
        path = path.strip('"\'')
        
        # 对于源文件，检查文件是否存在
        if "源文件" in prompt:
            if os.path.isfile(path):
                return path
            print(f"源文件不存在：{path}，请重新输入有效的文件路径。")
        else:  # 对于目标文件夹，不需要检查存在性，因为我们会创建它
            return path

def create_empty_files_from_source(source_file_path, target_folder_path):
    """
    根据源文件的每一行内容，在目标文件夹中创建同名的空文件。
    """
    try:
        # 确保目标文件夹存在，如果不存在则创建
        if not os.path.exists(target_folder_path):
            os.makedirs(target_folder_path)
            print(f"目标文件夹不存在，已创建新文件夹：{target_folder_path}")

        # 读取源文件每行内容
        encodings = ['utf-8', 'gbk', 'gb2312', 'latin-1']
        lines = None
        
        for encoding in encodings:
            try:
                with open(source_file_path, 'r', encoding=encoding) as source_file:
                    lines = source_file.readlines()
                print(f"成功使用 {encoding} 编码读取源文件")
                break
            except UnicodeDecodeError:
                continue
        
        if lines is None:
            print("无法使用常见编码读取源文件，请检查文件编码")
            return

        files_created = 0  # 记录创建的文件数量

        # 遍历每行生成空文件
        for line in lines:
            # 去除行首尾空白字符，包括换行符
            file_name = line.strip()

            # 跳过空行
            if not file_name:
                continue

            # 构建目标文件路径
            file_path = os.path.join(target_folder_path, file_name)

            # 检查文件名是否有效，处理可能包含非法字符的情况
            try:
                # 创建空文件
                with open(file_path, 'w', encoding='utf-8'):
                    pass
                
                print(f"已生成空文件：{file_name}")
                files_created += 1
            except Exception as e:
                print(f"创建文件失败：{file_name}，错误：{e}")

        print(f"文件生成完成，共创建了 {files_created} 个空文件。")

    except Exception as e:
        print(f"处理过程中发生错误：{e}")

def main():
    """
    主函数：处理用户输入并调用文件生成函数。
    """
    print("=== 批量创建空文件工具 ===")
    
    # 设置默认路径
    default_source = "d:\\Works\\0\\files.txt"
    default_target = "d:\\Works\\Targets\\"
    
    # 询问源文件路径
    source_file_path = get_valid_file_path(
        f"请输入源文件位置（默认是：{default_source}，直接回车使用默认值）：", 
        default_source
    )
    
    # 询问目标文件夹路径
    target_folder_path = get_valid_file_path(
        f"请输入目标文件夹位置（默认是：{default_target}，直接回车使用默认值）：", 
        default_target
    )
    
    print(f"使用的源文件：{source_file_path}")
    print(f"使用的目标文件夹：{target_folder_path}")
    
    # 调用创建文件函数
    create_empty_files_from_source(source_file_path, target_folder_path)

    # 等待用户按回车键退出
    input("按回车键退出...")

if __name__ == "__main__":
    main()