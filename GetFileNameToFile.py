# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我文件夹位置，默认为“d:\Works\Downloads\”；目标文件位置，默认为“e:\Documents\Creations\Scripts\Attachments\Python\Lists.txt”。
# 将源文件夹及其子文件夹内所有文件，按照绝对路径排序。依次将绝对路径（包括文件名、扩展名），写入目标列表文件中，如无这列表文件就生成一个。同时写入剪贴板。

# 导入模块
# 导入必要的模块
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

def write_absolute_filepaths_to_file(source_folder, target_file):
    """
    递归遍历源文件夹及其子文件夹，按绝对路径排序将文件绝对路径（包括文件名、扩展名）写入目标文件中。
    
    :param source_folder: 源文件夹路径
    :param target_file: 目标文件完整路径
    :return: 包含所有文件路径的列表，以及是否成功写入文件
    """
    try:
        # 确保目标文件的目录存在
        target_dir = os.path.dirname(target_file)
        if target_dir:  # 如果目标文件路径包含目录
            os.makedirs(target_dir, exist_ok=True)
        
        # 收集所有文件的绝对路径
        absolute_paths = []
        
        print("正在扫描文件，请稍候...")
        
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
        
        # 构建要复制到剪贴板的文本（所有路径用换行符连接）
        clipboard_text = '\n'.join(absolute_paths)
        
        return absolute_paths, True, clipboard_text
        
    except Exception as e:
        print(f"处理过程中发生错误：{e}")
        return [], False, ""

def main():
    """
    主函数：获取用户输入并执行文件绝对路径导出操作。
    """
    # 设置默认路径
    default_source_folder = "d:\\Works\\Downloads\\"
    default_target_file = "e:\\Documents\\Creations\\Scripts\\Attachments\\Python\\Lists.txt"
    
    print("=" * 60)
    print("文件路径列表生成工具")
    print("=" * 60)
    
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
    print(f"目标文件：{target_file}")
    
    # 调用函数写入文件绝对路径
    file_paths, success, clipboard_text = write_absolute_filepaths_to_file(source_folder, target_file)
    
    if success:
        print(f"✓ 文件绝对路径已成功写入到目标文件：{target_file}")
        print(f"✓ 共找到 {len(file_paths)} 个文件")
        
        # 尝试复制到剪贴板
        if file_paths:
            print("\n正在尝试复制到剪贴板...")
            if copy_to_clipboard(clipboard_text):
                print("✓ 文件路径列表已成功复制到剪贴板")
                print("  您现在可以在任何文本编辑器中粘贴(Ctrl+V)使用")
            else:
                print("⚠ 文件路径列表已保存到文件，但未复制到剪贴板")
        
        # 显示前5个文件路径作为示例
        if file_paths:
            print(f"\n前5个文件路径示例：")
            for i, path in enumerate(file_paths[:5], 1):
                print(f"  {i}. {os.path.basename(path)}")
            if len(file_paths) > 5:
                print(f"  ... 以及另外 {len(file_paths) - 5} 个文件")
    
    else:
        print("✗ 处理失败，请检查错误信息")

    # 等待用户确认退出
    print("\n" + "=" * 60)
    input("操作完成，按回车键退出...")

if __name__ == "__main__":
    main()