# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件夹位置（默认为 d:\Studios\Folders\Ins\）。
# 依次将源文件夹下的所有文件，移动至以它们文件名（不包括扩展名）为文件夹名的文件夹中。

import shutil
import sys
from pathlib import Path

# ==================== 全局配置 ====================

DEFAULT_SOURCE_DIR = Path(r"d:\Studios\Folders\Ins")

# ==================== 辅助函数 ====================


def get_input_with_default(prompt_text: str, default_value: str) -> str:
    """获取带默认值的用户输入。"""
    user_input = input(f"{prompt_text} (默认: {default_value}): ").strip()
    return user_input if user_input else str(default_value)


# ==================== 处理函数 ====================


def move_files_to_stem_folders(source_dir: Path) -> tuple[int, int]:
    """
    将源文件夹下的每个文件，移动到以主文件名命名的子文件夹中。
    返回 (移动文件数, 创建文件夹数)。
    """
    if not source_dir.is_dir():
        print(f"错误：路径 '{source_dir}' 不存在！")
        return 0, 0

    moved = 0
    created = 0

    for file_path in source_dir.iterdir():
        if not file_path.is_file():
            continue

        # 以主文件名命名的目标文件夹
        target_dir = source_dir / file_path.stem
        if not target_dir.is_dir():
            target_dir.mkdir(parents=True, exist_ok=True)
            print(f"已创建文件夹: {target_dir}")
            created += 1

        # 移动文件
        target_path = target_dir / file_path.name
        shutil.move(str(file_path), str(target_path))
        print(f"移动文件: {file_path.name} -> {target_dir}")
        moved += 1

    return moved, created


# ==================== 主程序 ====================


def main() -> None:
    """主函数：获取用户输入并执行文件移动操作。"""

    source_str = get_input_with_default("请输入源文件夹路径：", str(DEFAULT_SOURCE_DIR))
    source_dir = Path(source_str)

    moved, created = move_files_to_stem_folders(source_dir)
    print(f"\n操作完成！移动 {moved} 个文件，创建 {created} 个文件夹。")


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
