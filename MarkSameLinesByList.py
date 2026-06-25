# 请帮我写个中文的 Python 脚本，批注也是中文：
# 询问我文件位置（可以是任何格式，默认是：d:\Studios\Attachments\Lists.txt）。以文本方式读取该文件。
# 遍历该 txt 文件所有行。每发现有某个行与前面的行相同就在行首打上"# "。

import signal
import sys
from pathlib import Path

# ==================== 全局配置 ====================

DEFAULT_FILE_PATH = Path(r"d:\Studios\Attachments\Lists.txt")

_quit_requested = False  # Ctrl+Q 中断标志

# --- 消息常量 ---

MSG_TITLE = "=== 文件重复行标记工具 ==="
MSG_INPUT_FILE_PATH = "请输入文件位置"
MSG_ENCODING_SUCCESS = "成功使用 {} 编码读取文件"
MSG_FILE_NOT_FOUND = "错误：文件不存在 —— {}"
MSG_ENCODING_FAIL = "无法使用常见编码读取文件，请检查文件编码"
MSG_DONE_MARKED = "文件处理完成，标记了 {} 行重复内容。"
MSG_NO_DUPLICATES = "未发现重复行，或文件不存在。"
MSG_INTERRUPTED = "\n\n用户中断程序，已退出。"
MSG_ERROR = "\n程序运行出错: {}"
MSG_EXIT = "\n按回车键退出..."

# ==================== 辅助函数 ====================


def get_input_with_default(prompt_text: str, default_value: str) -> str:
    """获取带默认值的用户输入。"""
    user_input = input(f"{prompt_text} (默认: {default_value}): ").strip()
    return user_input if user_input else str(default_value)


def read_text_with_fallback(file_path: Path) -> str | None:
    """
    尝试多种编码读取文本文件，全部失败返回 None。
    """
    for encoding in ("utf-8", "gbk", "gb2312", "latin-1"):
        try:
            text = file_path.read_text(encoding=encoding)
            print(MSG_ENCODING_SUCCESS.format(encoding))
            return text
        except (UnicodeDecodeError, OSError):
            continue
    return None


# ==================== 处理函数 ====================


def mark_duplicate_lines(file_path: Path) -> int:
    """
    读取文件，对重复出现的行添加 "# " 前缀后写回。
    返回标记的重复行数。
    """
    if not file_path.is_file():
        print(MSG_FILE_NOT_FOUND.format(file_path))
        return 0

    text = read_text_with_fallback(file_path)
    if text is None:
        print(MSG_ENCODING_FAIL)
        return 0

    seen: set[str] = set()
    result: list[str] = []
    marked = 0

    for line in text.splitlines(keepends=True):
        stripped = line.rstrip("\n\r")
        if stripped in seen:
            result.append(f"# {line}")
            marked += 1
        else:
            seen.add(stripped)
            result.append(line)

    file_path.write_text("".join(result), encoding="utf-8")
    return marked


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
    """主函数：获取文件路径并执行重复行标记。"""
    print(MSG_TITLE)

    raw = get_input_with_default(MSG_INPUT_FILE_PATH, str(DEFAULT_FILE_PATH))
    raw = raw.strip("\"'")

    file_path = Path(raw) if raw else DEFAULT_FILE_PATH

    count = mark_duplicate_lines(file_path)
    if count:
        print(MSG_DONE_MARKED.format(count))
    else:
        print(MSG_NO_DUPLICATES)


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
