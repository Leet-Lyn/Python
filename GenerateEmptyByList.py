# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件位置（d:\Studios\Attachments\Lists.txt）与目标文件夹位置（d:\Studios\Folders\Downloads\）。
# 读取源文件每行，在目标文件夹位置生成空文件，文件名与读取的一致。

import signal
import sys
from pathlib import Path

# ==================== 全局配置 ====================

DEFAULT_SOURCE_FILE = Path(r"d:\Studios\Attachments\Lists.txt")
DEFAULT_TARGET_DIR = Path(r"d:\Studios\Folders\Downloads")

_quit_requested = False  # Ctrl+Q 中断标志

# --- 消息常量 ---
MSG_TOOL_TITLE = "=== 批量创建空文件工具 ==="
MSG_PROMPT_SOURCE_FILE = "请输入源文件位置："
MSG_PROMPT_TARGET_DIR = "请输入目标文件夹位置："
MSG_SOURCE_FILE_NOT_FOUND = "源文件不存在：{}"
MSG_ENCODING_SUCCESS = "成功使用 {} 编码读取源文件"
MSG_ENCODING_FAILED = "无法使用常见编码读取源文件，请检查文件编码"
MSG_CREATED_EMPTY_FILE = "已生成空文件：{}"
MSG_CREATE_FILE_FAILED = "创建文件失败：{}，错误：{}"
MSG_USING_SOURCE_FILE = "使用的源文件：{}"
MSG_USING_TARGET_DIR = "使用的目标文件夹：{}"
MSG_GENERATE_COMPLETE = "文件生成完成，共创建了 {} 个空文件。"
MSG_INPUT_DEFAULT_HINT = " (默认: {}): "
MSG_INTERRUPTED = "\n\n用户中断程序，已退出。"
MSG_ERROR = "\n程序运行出错: {}"
MSG_EXIT = "\n按回车键退出..."

# ==================== 辅助函数 ====================


def get_input_with_default(prompt_text: str, default_value: str) -> str:
    """获取带默认值的用户输入。"""
    user_input = input(f"{prompt_text}{MSG_INPUT_DEFAULT_HINT.format(default_value)}").strip()
    return user_input if user_input else str(default_value)


def read_lines_with_fallback(file_path: Path) -> list[str] | None:
    """
    尝试多种编码读取文件行，返回行列表；全部失败返回 None。
    """
    for encoding in ("utf-8", "gbk", "gb2312", "latin-1"):
        try:
            text = file_path.read_text(encoding=encoding)
            print(MSG_ENCODING_SUCCESS.format(encoding))
            return text.splitlines()
        except (UnicodeDecodeError, OSError):
            continue
    return None


# ==================== 处理函数 ====================


def create_empty_files_from_list(
    source_file: Path,
    target_dir: Path,
) -> int:
    """
    读取源文件每行作为文件名，在目标文件夹创建对应空文件。
    返回创建的文件数量。
    """
    # 检查源文件
    if not source_file.is_file():
        print(MSG_SOURCE_FILE_NOT_FOUND.format(source_file))
        return 0

    # 读取行
    lines = read_lines_with_fallback(source_file)
    if lines is None:
        print(MSG_ENCODING_FAILED)
        return 0

    # 确保目标文件夹存在
    target_dir.mkdir(parents=True, exist_ok=True)

    created = 0
    for line in lines:
        file_name = line.strip()
        if not file_name:
            continue

        target_path = target_dir / file_name
        try:
            target_path.write_text("", encoding="utf-8")
            print(MSG_CREATED_EMPTY_FILE.format(file_name))
            created += 1
        except OSError as e:
            print(MSG_CREATE_FILE_FAILED.format(file_name, e))

    return created


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
    """主函数：获取用户输入并调用文件生成函数，完成后循环回到开头。"""
    _init_quit_handler()
    while True:
        print(MSG_TOOL_TITLE)

        source_str = get_input_with_default(MSG_PROMPT_SOURCE_FILE, str(DEFAULT_SOURCE_FILE))
        if source_str.lower() == "q":
            print("程序已退出。")
            break

        target_str = get_input_with_default(MSG_PROMPT_TARGET_DIR, str(DEFAULT_TARGET_DIR))
        if target_str.lower() == "q":
            print("程序已退出。")
            break

        source_file = Path(source_str)
        target_dir = Path(target_str)

        print(MSG_USING_SOURCE_FILE.format(source_file))
        print(MSG_USING_TARGET_DIR.format(target_dir))

        count = create_empty_files_from_list(source_file, target_dir)
        print(MSG_GENERATE_COMPLETE.format(count))


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
