# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件夹位置（默认是：d:\Studios\Folders\Downloads\）。
# 遍历源文件夹位置中所有子文件夹，如果子文件夹为空，则删除子文件夹。

import signal
import sys
from pathlib import Path

# ==================== 全局配置 ====================

DEFAULT_SOURCE_DIR = Path(r"d:\Studios\Folders\Downloads")
_quit_requested = False  # Ctrl+Q 中断标志

# --- 消息常量 ---
MSG_TOOL_TITLE = "=== 删除空子文件夹工具 ==="
MSG_PROMPT_SOURCE_DIR = "请输入源文件夹位置"
MSG_INPUT_DEFAULT_HINT = "（回车使用默认 {}）："
MSG_USING_SOURCE_DIR = "使用的源文件夹：{}"
MSG_INVALID_PATH = "输入的路径无效：{}，请重新输入。"
MSG_DELETED_EMPTY_FOLDER = "已删除空子文件夹: {}"
MSG_DELETE_FOLDER_ERROR = "删除子文件夹 {} 时出错: {}"
MSG_NO_EMPTY_FOLDER = "未找到空子文件夹。"
MSG_DELETE_COMPLETE = "操作完成！共删除了 {} 个空子文件夹。"
MSG_INTERRUPTED = "\n\n用户中断程序，已退出。"
MSG_ERROR = "\n程序运行出错: {}"
MSG_EXIT = "\n按回车键退出..."

# ==================== 中断处理 ====================


def _on_quit_signal(signum, frame):
    global _quit_requested
    _quit_requested = True
    raise KeyboardInterrupt()


def _init_quit_handler():
    if hasattr(signal, "SIGQUIT"):
        signal.signal(signal.SIGQUIT, _on_quit_signal)


def _check_quit() -> bool:
    global _quit_requested
    if sys.platform == "win32":
        try:
            import msvcrt
            while msvcrt.kbhit():
                if msvcrt.getch() == b"\x11":
                    _quit_requested = True
        except Exception:
            pass
    return _quit_requested


# ==================== 辅助函数 ====================


def ask_folder(prompt: str, default: Path) -> Path:
    """询问文件夹路径，回车使用默认值；输入无效则循环重试。"""
    while True:
        raw = input(f"{prompt}{MSG_INPUT_DEFAULT_HINT.format(default)}").strip().strip("'\"")
        folder = Path(raw) if raw else default
        if folder.is_dir():
            return folder
        print(MSG_INVALID_PATH.format(folder))


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
                print(MSG_DELETED_EMPTY_FOLDER.format(dir_path))
                removed_count += 1
        except OSError as e:
            print(MSG_DELETE_FOLDER_ERROR.format(dir_path, e))

    return removed_count


# ==================== 主程序 ====================


def main() -> None:
    """主程序入口。"""
    _init_quit_handler()
    print(MSG_TOOL_TITLE)

    source_dir = ask_folder(MSG_PROMPT_SOURCE_DIR, DEFAULT_SOURCE_DIR)
    print(MSG_USING_SOURCE_DIR.format(source_dir))

    count = remove_empty_subfolders(source_dir)
    if count == 0:
        print(MSG_NO_EMPTY_FOLDER)
    else:
        print(MSG_DELETE_COMPLETE.format(count))


# ==================== 程序入口 ====================

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    try:
        main()
    except KeyboardInterrupt:
        print(MSG_INTERRUPTED)
    except Exception as e:
        print(MSG_ERROR.format(e))
    finally:
        input(MSG_EXIT)