# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件夹位置。
# 遍历源文件夹位置中所有子文件夹，如果子文件夹为空，则删除子文件夹。

# 导入模块
import os
import shutil

def get_valid_directory(prompt):
    """
    获取有效的文件夹路径，确保路径存在且有效。
    """
    while True:
        folder = input(prompt).strip()
        if os.path.isdir(folder):
            return folder
        print("输入的路径无效，请重新输入有效的文件夹路径。")

def remove_empty_subfolders(source_folder):
    """
    遍历源文件夹中的所有子文件夹，删除空子文件夹。
    """
    for root, dirs, _ in os.walk(source_folder, topdown=False):  # 逆序遍历，优先处理最深层的子文件夹
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            # 检查子文件夹是否为空
            if not os.listdir(dir_path):
                try:
                    shutil.rmtree(dir_path)  # 删除空子文件夹
                    print(f"已删除空子文件夹: {dir_path}")
                except Exception as e:
                    print(f"删除子文件夹 {dir_path} 时出错: {e}")

def main():
    """
    主程序入口。
    """
    # 获取源文件夹路径
    source_folder = get_valid_directory("请输入源文件夹路径：")
    
    # 删除空子文件夹
    remove_empty_subfolders(source_folder)

    print("操作完成！")
    input("按回车键退出...")

if __name__ == "__main__":
    main()