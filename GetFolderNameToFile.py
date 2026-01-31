# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我文件夹位置，默认为“d:\\Works\\X\\”；目标文件位置，默认为“e:\Documents\Creations\Scripts\Attachment\Lists.txt”。
# 将源文件夹及其子文件夹内所有文件夹，按照相对路径排序。依次将绝对路径（仅仅针对文件夹），写入目标列表文件中，如无这列表文件就生成一个。同时写入剪贴板。

# 导入模块
import os
import sys

def copy_to_clipboard(text):
    """
    将文本复制到系统剪贴板
    
    :param text: 要复制的文本
    :return: 复制成功返回True，否则返回False
    """
    try:
        # 根据操作系统选择不同的剪贴板操作方法
        if sys.platform == 'win32':
            # Windows系统使用win32clipboard
            try:
                import win32clipboard
                import win32con
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardText(text, win32con.CF_UNICODETEXT)
                win32clipboard.CloseClipboard()
                return True
            except ImportError:
                # 如果没有安装win32clipboard模块，尝试使用其他方法
                print("警告：未安装win32clipboard模块，无法使用剪贴板功能")
                print("请使用以下命令安装：pip install pywin32")
                return False
        
        elif sys.platform == 'darwin':
            # macOS系统使用pbcopy命令
            import subprocess
            process = subprocess.Popen('pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
            process.communicate(text.encode('utf-8'))
            return True
        
        elif sys.platform.startswith('linux'):
            # Linux系统使用xclip或xsel命令
            try:
                import subprocess
                # 尝试使用xclip
                process = subprocess.Popen(['xclip', '-selection', 'clipboard'], stdin=subprocess.PIPE)
                process.communicate(text.encode('utf-8'))
                return True
            except (FileNotFoundError, subprocess.CalledProcessError):
                try:
                    # 如果xclip不可用，尝试xsel
                    process = subprocess.Popen(['xsel', '--clipboard', '--input'], stdin=subprocess.PIPE)
                    process.communicate(text.encode('utf-8'))
                    return True
                except (FileNotFoundError, subprocess.CalledProcessError):
                    print("警告：Linux系统需要安装xclip或xsel才能使用剪贴板功能")
                    print("请使用以下命令安装：sudo apt-get install xclip 或 sudo apt-get install xsel")
                    return False
        
        else:
            print(f"警告：不支持的操作系统 {sys.platform}，无法使用剪贴板功能")
            return False
    
    except Exception as e:
        print(f"复制到剪贴板时发生错误：{e}")
        return False

def get_all_subfolders(source_folder):
    """
    获取指定文件夹下所有子文件夹的绝对路径，并按相对路径排序
    
    :param source_folder: 源文件夹路径
    :return: 排序后的文件夹路径列表
    """
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
    
    return folder_paths

def save_folder_paths(source_folder, output_file):
    """
    获取指定文件夹下所有子文件夹的绝对路径，并按相对路径排序后写入文件。
    
    :param source_folder: 源文件夹路径
    :param output_file: 输出文件路径
    :return: 包含所有文件夹路径的列表，以及是否成功写入文件，以及剪贴板文本
    """
    try:
        # 确保输出文件的目录存在
        output_dir = os.path.dirname(output_file)
        if output_dir:  # 如果输出文件路径包含目录
            os.makedirs(output_dir, exist_ok=True)
        
        print("正在扫描文件夹，请稍候...")
        
        # 获取所有文件夹路径
        folder_paths = get_all_subfolders(source_folder)
        
        # 写入文件夹绝对路径到输出文件
        with open(output_file, 'w', encoding='utf-8') as f:
            for folder_path in folder_paths:
                f.write(folder_path + '\n')
        
        # 构建要复制到剪贴板的文本（所有路径用换行符连接）
        clipboard_text = '\n'.join(folder_paths)
        
        return folder_paths, True, clipboard_text
        
    except Exception as e:
        print(f"错误：无法保存文件夹路径，错误信息: {e}")
        return [], False, ""

def main():
    """
    主函数：获取用户输入并调用保存文件夹路径的函数。
    """
    print("=" * 60)
    print("文件夹路径提取工具")
    print("=" * 60)

    # 设置默认路径
    default_source_folder = "d:\\Works\\X\\"
    default_output_file = "e:\\Documents\\Creations\\Scripts\\Attachment\\Lists.txt"
    
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
        # 询问是否创建源文件夹
        create_folder = input("是否要创建此文件夹？(y/n): ").strip().lower()
        if create_folder == 'y':
            try:
                os.makedirs(source_folder, exist_ok=True)
                print(f"已创建文件夹：{source_folder}")
            except Exception as e:
                print(f"创建文件夹时发生错误：{e}")
                return
        else:
            return
    
    print(f"正在处理...")
    print(f"源文件夹：{source_folder}")
    print(f"目标文件：{output_file}")
    
    # 调用保存文件夹路径的函数
    folder_paths, success, clipboard_text = save_folder_paths(source_folder, output_file)
    
    if success:
        print(f"✓ 文件夹绝对路径已成功保存到：{output_file}")
        print(f"✓ 共找到 {len(folder_paths)} 个文件夹")
        
        # 尝试复制到剪贴板
        if folder_paths:
            print("\n正在尝试复制到剪贴板...")
            if copy_to_clipboard(clipboard_text):
                print("✓ 文件夹路径列表已成功复制到剪贴板")
                print("  您现在可以在任何文本编辑器中粘贴(Ctrl+V)使用")
            else:
                print("⚠ 文件夹路径列表已保存到文件，但未复制到剪贴板")
        
        # 显示前5个文件夹路径作为示例
        if folder_paths:
            print(f"\n前5个文件夹路径示例：")
            for i, path in enumerate(folder_paths[:5], 1):
                # 显示相对路径作为示例，更简洁
                rel_path = os.path.relpath(path, source_folder)
                print(f"  {i}. {rel_path}")
            if len(folder_paths) > 5:
                print(f"  ... 以及另外 {len(folder_paths) - 5} 个文件夹")
    
    else:
        print("✗ 处理失败，请检查错误信息")

    # 等待用户确认退出
    print("\n" + "=" * 60)
    input("操作完成，按回车键退出...")

if __name__ == "__main__":
    main()