# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件位置，默认为"d:\Studios\Folders\Downloads\"。
# 将文件夹下的所有文件夹内（包括子文件夹）的文件上移到文件的父文件夹中。

import shutil
import sys
from pathlib import Path

# ==================== 全局配置 ====================

DEFAULT_SOURCE_DIR = Path(r"d:\Studios\Folders\Downloads")

# ==================== 辅助函数 ====================


def get_input_with_default(prompt_text: str, default_value: str) -> str:
    """获取带默认值的用户输入。"""
    user_input = input(f"{prompt_text} (默认: {default_value}): ").strip()
    return user_input if user_input else str(default_value)


def move_files_to_parent_directory(source_dir: Path) -> int:
    """
    将文件夹内（包括子文件夹）的所有文件上移到其父文件夹。
    从最深子目录向浅层处理，处理完后删除空文件夹。
    返回移动的文件数量。
    """
    # 收集所有子目录，按深度降序（最深优先）
    all_dirs = [p for p in source_dir.rglob("*") if p.is_dir()]
    all_dirs.sort(key=lambda p: len(p.parts), reverse=True)

    moved_count = 0

    for dir_path in all_dirs:
        for entry in dir_path.iterdir():
            if not entry.is_file():
                continue

            parent_dir = dir_path.parent
            file_stem = entry.stem
            file_suffix = entry.suffix

            # 目标路径（父文件夹下同名文件）
            new_path = parent_dir / entry.name

            # 如果目标已存在，加 _moved 后缀避免冲突
            while new_path.exists():
                file_stem = f"{file_stem}_moved"
                new_path = parent_dir / f"{file_stem}{file_suffix}"

            try:
                shutil.move(str(entry), str(new_path))
                print(f"文件已移动: {entry} -> {new_path}")
                moved_count += 1
            except OSError as e:
                print(f"无法移动文件: {entry} -> {new_path}. 错误: {e}")

        # 如果当前文件夹已空，删除
        try:
            remaining = list(dir_path.iterdir())
            if not remaining:
                dir_path.rmdir()
                print(f"已删除空文件夹: {dir_path}")
        except OSError as e:
            print(f"无法删除文件夹: {dir_path}. 错误: {e}")

    return moved_count


# ==================== 主程序 ====================


def main() -> None:
    """主函数：处理用户输入并调用文件移动函数。"""

    source_str = get_input_with_default(
        "请输入源文件夹位置：", str(DEFAULT_SOURCE_DIR))
    source_dir = Path(source_str)

    if not source_dir.is_dir():
        print("提供的路径不是有效的文件夹路径，请检查后重试。")
        return

    count = move_files_to_parent_directory(source_dir)
    print(f"所有文件已移动完成，共移动 {count} 个文件。")


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
