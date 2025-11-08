# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件夹位置（默认“d:\\Works\\In\\”）与目标文件夹位置（默认“d:\\Works\\Out\\”）。
# 复制源文件夹结构到目标文件夹中，但不复制文件。

# 导入模块
import os

def copy_folder_structure(source, target):
    """
    从源文件夹复制文件夹结构到目标文件夹，但不复制文件。
    :param source: 源文件夹路径
    :param target: 目标文件夹路径
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
            if not os.path.exists(target_dir):
                os.makedirs(target_dir, exist_ok=True)
                print(f"已创建文件夹：'{target_dir}'")

    print("文件夹结构复制完成！")

def main():
    """
    主函数：获取用户输入并执行文件夹结构复制操作。
    """
    # 设置默认路径
    default_source = "d:\\Works\\In\\"
    default_target = "d:\\Works\\Out\\"
    
    # 获取用户输入，使用默认值如果用户直接按回车
    source = input(f"请输入源文件夹位置（按回车使用默认值：{default_source}）：").strip()
    if not source:
        source = default_source
    
    target = input(f"请输入目标文件夹位置（按回车使用默认值：{default_target}）：").strip()
    if not target:
        target = default_target

    # 调用函数复制文件夹结构
    copy_folder_structure(source, target)
    
    # 等待用户确认退出
    input("按回车键退出...")

if __name__ == "__main__":
    main()