# 请帮我写个中文的 Python 脚本，批注也是中文：
# 询问我询问源文件夹位置（默认：d:\Studios\Folders\Downloads\）。
# 1. 检索该文件夹下，所有子文件夹下再有无子文件夹。如有请标明。
# 2. 检索该文件夹下（包括子文件夹）所有文件的扩展名。请全部列出来。
# 完成后，跳到开始询问我源文件夹位置。反复循环。

import sys
from pathlib import Path

# ==================== 全局配置 ====================

DEFAULT_SOURCE_DIR = Path(r"d:\Studios\Folders\Downloads")

# ==================== 辅助函数 ====================


def get_user_folder() -> Path | None:
    """
    询问用户源文件夹路径，支持默认路径。
    返回 Path 对象；输入 q/quit/exit 返回 None 表示退出；无效路径打印提示并循环。
    """
    default_str = str(DEFAULT_SOURCE_DIR)
    while True:
        user_input = input(
            f"请输入源文件夹路径（默认：{default_str}，输入 q 退出）："
        ).strip()

        if user_input.lower() in ("q", "quit", "exit"):
            return None

        folder = Path(user_input) if user_input else DEFAULT_SOURCE_DIR
        if folder.is_dir():
            return folder
        print(f"输入错误：路径不存在或不是文件夹 —— {folder}，请重新输入。\n")


# ==================== 处理函数 ====================


def find_subfolders_with_children(root: Path) -> dict[Path, bool]:
    """
    递归检索 root 下所有子文件夹，判断每个是否还包含更深子文件夹。
    返回 {子文件夹路径: 是否包含更深子文件夹}。
    """
    result: dict[Path, bool] = {}
    all_subdirs = [p for p in root.rglob("*") if p.is_dir()]
    for sub in all_subdirs:
        has_children = any(e.is_dir() for e in sub.iterdir())
        result[sub] = has_children
    return result


def collect_extensions(root: Path) -> set[str]:
    """
    递归遍历 root 下所有文件，收集扩展名（小写，不含点号）。
    无扩展名的文件标记为 "(无扩展名)"。
    """
    extensions: set[str] = set()
    for file_path in root.rglob("*"):
        if not file_path.is_file():
            continue
        ext = file_path.suffix
        if ext:
            extensions.add(ext.lstrip(".").lower())
        else:
            extensions.add("(无扩展名)")
    return extensions


# ==================== 主程序 ====================


def main() -> None:
    """主循环：反复询问源文件夹路径，执行统计并输出结果。"""

    while True:
        source = get_user_folder()
        if source is None:
            print("用户退出。")
            break

        print(f"\n正在扫描：{source}\n")

        # 1. 查找所有子文件夹及其是否含有更深子文件夹
        subfolders_status = find_subfolders_with_children(source)
        print("=== 子文件夹状态 ===")
        if not subfolders_status:
            print("源文件夹下没有子文件夹。")
        else:
            for sub in sorted(subfolders_status, key=lambda p: str(p).lower()):
                status = "包含子文件夹" if subfolders_status[sub] else "无子文件夹"
                print(f"  {sub} -> {status}")

        # 2. 收集所有文件的扩展名
        exts = collect_extensions(source)
        print("\n=== 所有文件扩展名（去重） ===")
        if not exts:
            print("  未找到任何文件。")
        else:
            # "(无扩展名)" 排最前，其余字母序
            sorted_exts = sorted(exts, key=lambda x: (x != "(无扩展名)", x))
            for ext in sorted_exts:
                print(f"  .{ext}" if ext != "(无扩展名)" else f"  {ext}")

        print("\n" + "=" * 50 + "\n")


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
