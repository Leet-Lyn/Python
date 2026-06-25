# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件夹位置（默认为 d:\Studios\Folders\Ins\）。
# 依次将源文件夹下的所有文件，移动至以它们文件名（不包括扩展名）为文件夹名的文件夹中。

import signal
import shutil
import sys
from pathlib import Path

# ==================== 全局配置 ====================

DEFAULT_SOURCE_DIR = Path(r"d:\Studios\Folders\Ins")

_quit_requested = False  # Ctrl+Q 中断标志

# --- 消息常量 ---
MSG_PROMPT_SOURCE_DIR = "请输入源文件夹路径："
MSG_ERR_PATH_NOT_FOUND = "错误：路径 '{}' 不存在！"
MSG_CREATED_FOLDER = "已创建文件夹: {}"
MSG_MOVED_FILE = "移动文件: {} -> {}"
MSG_OPERATION_COMPLETE = "操作完成！移动 {} 个文件，创建 {} 个文件夹。"
MSG_INPUT_DEFAULT_HINT = " (默认: {}): "
MSG_INTERRUPTED = "\n\n用户中断程序，已退出。"
MSG_ERROR = "\n程序运行出错: {}"
MSG_EXIT = "\n按回车键退出..."

# ==================== 辅助函数 ====================


def get_input_with_default(prompt_text: str, default_value: str) -> str:
    """获取带默认值的用户输入。"""
    user_input = input(f"{prompt_text}{MSG_INPUT_DEFAULT_HINT.format(default_value)}").strip()
    return user_input if user_input else str(default_value)


# ==================== 处理函数 ====================


def move_files_to_stem_folders(source_dir: Path) -> tuple[int, int]:
    """
    将源文件夹下的每个文件，移动到以主文件名命名的子文件夹中。
    返回 (移动文件数, 创建文件夹数)。
    """
    if not source_dir.is_dir():
        print(MSG_ERR_PATH_NOT_FOUND.format(source_dir))
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
            print(MSG_CREATED_FOLDER.format(target_dir))
            created += 1

        # 移动文件
        target_path = target_dir / file_path.name
        shutil.move(str(file_path), str(target_path))
        print(MSG_MOVED_FILE.format(file_path.name, target_dir))
        moved += 1

    return moved, created


# ==================== 主程序 ====================
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


def main() -> None:
    """主函数：获取用户输入并执行文件移动操作。"""

    source_str = get_input_with_default(MSG_PROMPT_SOURCE_DIR, str(DEFAULT_SOURCE_DIR))
    source_dir = Path(source_str)

    moved, created = move_files_to_stem_folders(source_dir)
    print(MSG_OPERATION_COMPLETE.format(moved, created))


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
