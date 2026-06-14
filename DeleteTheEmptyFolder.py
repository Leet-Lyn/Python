# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件夹位置（默认是：d:\Studios\Folders\Downloads\）。
# 遍历源文件夹位置中所有子文件夹，如果子文件夹为空，则删除子文件夹。

import sys
from pathlib import Path

# ==================== 全局配置 ====================

DEFAULT_SOURCE_DIR = Path(r"d:\Studios\Folders\Downloads")

# ==================== 辅助函数 ====================


def ask_folder(prompt: str, default: Path) -> Path:
    """询问文件夹路径，回车使用默认值；输入无效则循环重试。"""
    while True:
        raw = input(f"{prompt}（回车使用默认 {default}）：").strip().strip("'\"")
        folder = Path(raw) if raw else default
        if folder.is_dir():
            return folder
        print(f"输入的路径无效：{folder}，请重新输入。")


# ==================== 处理函数 ====================


def remove_empty_subfolders(source_dir: Path) -> int:
    """
    遍历源文件夹中的所有子文件夹，删除空子文件夹。
    返回删除的文件夹数量。
    """
    removed_count = 0

    # 收集所有子目录，按深度降序（最深优先，确保子目录先被处理）
    all_dirs = [p for p in source_dir.rglob("*") if p.is_dir()]
    all_dirs.sort(key=lambda p: len(p.parts), reverse=True)

    for dir_path in all_dirs:
        try:
            # 检查目录是否为空（iterdir 为空即无任何内容）
            if not any(True for _ in dir_path.iterdir()):
                dir_path.rmdir()
                print(f"已删除空子文件夹: {dir_path}")
                removed_count += 1
        except OSError as e:
            print(f"删除子文件夹 {dir_path} 时出错: {e}")

    return removed_count


# ==================== 主程序 ====================


def main() -> None:
    """主程序入口。"""
    print("=== 删除空子文件夹工具 ===")

    source_dir = ask_folder("请输入源文件夹位置", DEFAULT_SOURCE_DIR)
    print(f"使用的源文件夹：{source_dir}")

    count = remove_empty_subfolders(source_dir)
    if count == 0:
        print("未找到空子文件夹。")
    else:
        print(f"操作完成！共删除了 {count} 个空子文件夹。")


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
