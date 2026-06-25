# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件位置（可以是任何格式，默认是：d:\Studios\Attachments\Lists.txt）。
# 将文件按行读取，按字母顺序排序重新排序，再次写入文件。

import signal
import sys
from pathlib import Path

# ==================== 全局配置 ====================

DEFAULT_FILE_PATH = Path(r"d:\Studios\Attachments\Lists.txt")

_quit_requested = False  # Ctrl+Q 中断标志

# --- 消息常量 ---
MSG_INTERRUPTED = "\n\n用户中断程序，已退出。"
MSG_ERROR = "\n程序运行出错: {}"
MSG_EXIT = "\n按回车键退出..."
MSG_ASK_FILE_PATH = "请输入要处理的文件路径："
MSG_FILE_NOT_FOUND = "错误：'{}' 不是有效的文件路径！"
MSG_UNSUPPORTED_ENCODING = "错误：文件编码不支持，请使用 UTF-8 编码的文本文件"
MSG_FILE_EMPTY = "文件内容为空，无需处理！"
MSG_NO_WRITE_PERMISSION = "错误：没有写入权限，请关闭文件后重试 - {}"
MSG_WRITE_ERROR = "写入文件时发生错误：{}"
MSG_SORT_SUCCESS = "文件内容已成功排序并保存！"
MSG_DEFAULT_PROMPT_SUFFIX = " (默认: {}): "

# ==================== 辅助函数 ====================


def get_input_with_default(prompt_text: str, default_value: str) -> str:
    """获取带默认值的用户输入。"""
    user_input = input(f"{prompt_text}{MSG_DEFAULT_PROMPT_SUFFIX.format(default_value)}").strip()
    return user_input if user_input else str(default_value)


# ==================== 处理函数 ====================


def sort_file_lines(file_path: Path) -> bool:
    """
    读取文件 → 按字母排序行 → 覆盖写回。
    返回 True 表示成功。
    """
    # 读取
    try:
        text = file_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(MSG_FILE_NOT_FOUND.format(file_path))
        return False
    except UnicodeDecodeError:
        print(MSG_UNSUPPORTED_ENCODING)
        return False

    lines = text.splitlines()
    if not lines:
        print(MSG_FILE_EMPTY)
        return True  # 空文件不算失败

    # 排序
    sorted_lines = sorted(lines, key=str.lower)

    # 写回
    try:
        file_path.write_text("\n".join(sorted_lines), encoding="utf-8")
    except PermissionError:
        print(MSG_NO_WRITE_PERMISSION.format(file_path))
        return False
    except OSError as e:
        print(MSG_WRITE_ERROR.format(e))
        return False

    print(MSG_SORT_SUCCESS)
    return True


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
    """主函数：获取用户输入并执行文件排序操作。"""

    file_str = get_input_with_default(
        MSG_ASK_FILE_PATH, str(DEFAULT_FILE_PATH))
    file_path = Path(file_str)

    sort_file_lines(file_path)


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
