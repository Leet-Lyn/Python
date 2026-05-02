# 请帮我写个中文的 Python 脚本，批注也是中文：
# 询问我询问源文件夹位置（默认：d:\Works\Downloads\）。
# 1. 检索该文件夹下，所有子文件夹下再有无子文件夹。如有请标明。
# 2. 检索该文件夹下（包括子文件夹）所有文件的扩展名。请全部列出来。
# 完成后，跳到开始询问我源文件夹位置。反复循环。

# 导入模块
import os
from pathlib import Path

def get_user_folder() -> Path:
    """
    询问用户源文件夹路径，支持默认路径。
    返回 Path 对象。如果用户输入 q/quit 则返回 None 表示退出。
    """
    default = r"d:\Works\Downloads"
    user_input = input(f"请输入源文件夹路径（默认：{default}，输入 q 退出）：").strip()
    if user_input.lower() in ('q', 'quit', 'exit'):
        return None
    if not user_input:
        folder = Path(default)
    else:
        folder = Path(user_input)
    # 验证路径是否存在且为目录
    if not folder.exists():
        raise FileNotFoundError(f"路径不存在：{folder}")
    if not folder.is_dir():
        raise NotADirectoryError(f"路径不是文件夹：{folder}")
    return folder

def find_subfolders_with_children(root: Path):
    """
    检索 root 下的所有子文件夹，判断每个子文件夹内是否还包含子文件夹。
    返回一个字典：{子文件夹路径: 布尔值(是否有更深子文件夹)}
    """
    result = {}
    for item in root.iterdir():
        if item.is_dir():
            has_children = any(sub.is_dir() for sub in item.iterdir())
            result[item] = has_children
    return result

def collect_extensions(root: Path):
    """
    递归遍历 root 下的所有文件，收集扩展名（不包含点号），
    无扩展名的文件标记为 '(无扩展名)'。
    返回去重后的扩展名集合。
    """
    extensions = set()
    for file_path in root.rglob("*"):
        if file_path.is_file():
            ext = file_path.suffix
            if ext:
                extensions.add(ext[1:].lower())
            else:
                extensions.add("(无扩展名)")
    return extensions

def main():
    while True:
        try:
            # 1. 获取源文件夹
            source = get_user_folder()
            if source is None:
                print("用户退出。")
                break

            print(f"\n正在扫描：{source}\n")

            # 2. 查找所有子文件夹及其是否含有更深子文件夹
            subfolders_status = find_subfolders_with_children(source)
            print("子文件夹状态")
            if not subfolders_status:
                print("源文件夹下没有子文件夹。")
            else:
                for sub, has_child in subfolders_status.items():
                    status = "\n包含子文件夹。" if has_child else "\n无子文件夹。"
                    print(f"  {sub} -> {status}")

            # 3. 收集所有文件的扩展名（包括子文件夹内）
            exts = collect_extensions(source)
            print("\n所有文件扩展名（去重）")
            if not exts:
                print("  未找到任何文件。")
            else:
                sorted_exts = sorted(exts, key=lambda x: (x == "(无扩展名)", x))
                for ext in sorted_exts:
                    print(f"  {ext}")

            print("\n" + "="*50 + "\n")  # 分隔线

        except (FileNotFoundError, NotADirectoryError) as e:
            print(f"输入错误：{e}，请重新输入。\n")
            continue
        except Exception as e:
            print(f"发生未知错误：{e}，程序将退出。")
            break

if __name__ == "__main__":
    main()