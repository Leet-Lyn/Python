# 请帮我写个中文的 Python 脚本，批注也是中文：
# 请输入源文件夹位置（默认"d:\Studios\Folders\Downloads\"），重命名源文件夹下所有文件及子文件夹下文件。
# 遍历源文件夹位置中所有文件，对文件名（不包括后缀名）进行重命名，要求如下：
# 使中文、英文、数字之间用空格隔开。将 "-" 替换为 " "；将连续三个空格替换为 " - "。

import re
import sys
from pathlib import Path

# ==================== 全局配置 ====================

DEFAULT_SOURCE_DIR = Path(r"d:\Studios\Folders\Downloads")

# ==================== 辅助函数 ====================


def get_input_with_default(prompt_text: str, default_value: str) -> str:
    """获取带默认值的用户输入。"""
    user_input = input(f"{prompt_text} (默认: {default_value}): ").strip()
    return user_input if user_input else str(default_value)


def add_spaces_to_filename(filename: str) -> str:
    """
    处理文件名（不含扩展名）：
      1. 中文、英文、数字之间用空格隔开
      2. "-" 替换为 " "
      3. 连续三个空格替换为 " - "
    """
    stem, suffix = Path(filename).stem, Path(filename).suffix

    # 第一步：将 "-" 替换为 " "
    processed = stem.replace("-", " ")

    # 第二步：中文↔英文/数字边界插入空格
    pattern = r"([a-zA-Z0-9])([一-鿿])|([一-鿿])([a-zA-Z0-9])"

    def add_space(match):
        groups = match.groups()
        if groups[0] and groups[1]:
            return groups[0] + " " + groups[1]
        elif groups[2] and groups[3]:
            return groups[2] + " " + groups[3]
        return match.group()

    processed = re.sub(pattern, add_space, processed)

    # 第三步：连续三个空格替换为 " - "
    processed = processed.replace("   ", " - ")

    return processed + suffix


# ==================== 处理函数 ====================


def rename_files_in_directory(source_dir: Path) -> int:
    """
    遍历目录及其子目录，重命名所有文件（中英文数字间加空格）。
    返回重命名的文件数量。
    """
    if not source_dir.is_dir():
        print(f"错误：目录 '{source_dir}' 不存在")
        return 0

    rename_count = 0

    for file_path in source_dir.rglob("*"):
        if not file_path.is_file():
            continue

        new_name = add_spaces_to_filename(file_path.name)
        if new_name == file_path.name:
            continue

        new_path = file_path.parent / new_name
        if new_path.exists():
            print(f"警告：文件 '{new_name}' 已存在，跳过重命名 '{file_path.name}'")
            continue

        try:
            file_path.rename(new_path)
            print(f"重命名: '{file_path.name}' -> '{new_name}'")
            rename_count += 1
        except OSError as e:
            print(f"重命名文件 '{file_path.name}' 时出错: {e}")

    return rename_count


# ==================== 主程序 ====================


def main() -> None:
    """主函数：获取用户输入并执行重命名操作。"""
    source_str = get_input_with_default("请输入源文件夹位置：", str(DEFAULT_SOURCE_DIR))
    source_dir = Path(source_str)

    count = rename_files_in_directory(source_dir)
    print(f"\n完成！共重命名了 {count} 个文件")


# ==================== 程序入口 ====================

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n用户中断程序，已退出。")
    except Exception as e:
        print(f"\n程序运行出错: {e}")
    finally:
        input("\n按回车键退出...")
