# 从一个文件夹复制文件夹结构到另一个文件夹，但不复制文件。

# 导入模块
import os

def copy_folder_structure(source, target):
    """
    从源文件夹复制文件夹结构到目标文件夹，但不复制文件。
    """
    # 检查源文件夹是否存在
    if not os.path.exists(source):
        print(f"源文件夹 '{source}' 不存在。")
        return

    # 如果目标文件夹不存在，则创建
    if not os.path.exists(target):
        os.makedirs(target)
        print(f"目标文件夹 '{target}' 不存在，已创建。")

    # 遍历源文件夹结构
    for root, dirs, _ in os.walk(source):
        # 获取相对路径
        relative_path = os.path.relpath(root, source)
        # 创建相同的子文件夹在目标文件夹
        for dir_name in dirs:
            target_dir = os.path.join(target, relative_path, dir_name)
            os.makedirs(target_dir, exist_ok=True)
            print(f"已创建文件夹：'{target_dir}'")

def main():
    # 询问用户输入源文件夹和目标文件夹路径
    source = input("请输入源文件夹的位置：").strip()
    target = input("请输入目标文件夹的位置：").strip()

    if not source or not target:
        print("源文件夹和目标文件夹路径不能为空！")
        return

    # 调用函数复制文件夹结构
    copy_folder_structure(source, target)
    print("操作完成！")

if __name__ == "__main__":
    main()
    input("按回车键退出...")