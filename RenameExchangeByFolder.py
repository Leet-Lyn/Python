# 请帮我写个中文的 Python 脚本，批注也是中文：
# 请输入源文件夹位置（默认"d:\Studios\Folders\Downloads\"），同时询问分隔符是什么（分隔符可以是字符串，默认是" - "）。
# 重命名源文件夹下所有文件及子文件夹下文件。
# 将文件名（不包括扩展名）中分隔符两端交换。如果有多个相同的分隔符，则只交换一次。

import sys
from pathlib import Path

# ==================== 全局配置 ====================

DEFAULT_SOURCE_DIR = Path(r"d:\Studios\Folders\Downloads")
DEFAULT_SEPARATOR = " - "

# ==================== 辅助函数 ====================


def get_input_with_default(prompt_text: str, default_value: str) -> str:
    """获取带默认值的用户输入。"""
    user_input = input(f"{prompt_text} (默认: {default_value}): ").strip()
    return user_input if user_input else str(default_value)


def swap_separator_sides(filename: str, separator: str) -> str:
    """
    将文件名中分隔符两侧的内容交换位置，只处理第一个出现的分隔符。
    """
    if separator not in filename:
        return filename
    pos = filename.find(separator)
    left = filename[:pos]
    right = filename[pos + len(separator):]
    return right + separator + left


# ==================== 处理函数 ====================


def traverse_and_rename(source_dir: Path, separator: str) -> tuple[int, int, int]:
    """
    递归遍历文件夹及其子文件夹，重命名所有文件（交换分隔符两端）。
    返回 (已重命名, 已跳过, 错误)。
    """
    renamed = 0
    skipped = 0
    errors = 0

    for file_path in source_dir.rglob("*"):
        if not file_path.is_file():
            continue

        stem = file_path.stem
        suffix = file_path.suffix
        new_stem = swap_separator_sides(stem, separator)

        if new_stem == stem:
            skipped += 1
            continue

        new_path = file_path.parent / f"{new_stem}{suffix}"

        # 避免文件名冲突
        counter = 1
        while new_path.exists():
            new_path = file_path.parent / f"{new_stem}_{counter}{suffix}"
            counter += 1

        try:
            file_path.rename(new_path)
            print(f"✓ 重命名: {file_path.name} -> {new_path.name}")
            renamed += 1
        except OSError as e:
            errors += 1
            print(f"✗ 处理文件失败 {file_path.name}: {e}")

    return renamed, skipped, errors


# ==================== 主程序 ====================


def main() -> None:
    """主函数：获取用户输入并执行重命名操作。"""

    source_str = get_input_with_default("请输入源文件夹位置：", str(DEFAULT_SOURCE_DIR))
    source_dir = Path(source_str)

    if not source_dir.is_dir():
        print(f"错误：文件夹 '{source_dir}' 不存在！")
        return

    separator = get_input_with_default("请输入分隔符：", DEFAULT_SEPARATOR)

    print(f"\n开始处理文件夹: {source_dir}")
    print(f"使用分隔符: '{separator}'")
    print("=" * 50)

    renamed, skipped, errors = traverse_and_rename(source_dir, separator)

    print("=" * 50)
    print("处理完成！")
    print(f"已重命名: {renamed} 个文件")
    print(f"跳过: {skipped} 个文件")
    print(f"错误: {errors} 个文件")


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
