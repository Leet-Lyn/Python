# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件位置。
# 计算并生成文件的 Ed2K 链接。
# 我安装了 RHash，位置：“d:\ProApps\rhash\current\rhash.exe”。生成 ed2k 的命令类似：rhash.exe --uppercase --ed2k-link "file_path"。
# 生成如 "ed2k://|file|rustdesk-1.4.3-x86_64.exe|23369352|DF952...|/" 的 ed2k 链接，显示在屏幕，并写入剪贴板。
# 如此循环，再次询问我源文件位置。

# 导入模块
import signal
import subprocess
import sys
from pathlib import Path

# --- 常量 ---
RHASH = Path(r"d:\ProApps\rhash\current\rhash.exe")

_quit_requested = False  # Ctrl+Q 中断标志

# --- 消息常量 ---
MSG_INTERRUPTED = "\n\n用户中断程序，已退出。"
MSG_ERROR = "\n程序运行出错: {}"
MSG_EXIT = "\n按回车键退出..."
MSG_CLIPBOARD_FAIL = "复制到剪贴板失败：{}"
MSG_FILE_NOT_FOUND = "错误：文件 '{}' 不存在"
MSG_RHASH_MISSING = "错误：未找到 RHash —— {}"
MSG_RHASH_ERROR = "RHash 执行错误：{}"
MSG_PROMPT_FILE = "请输入源文件路径（输入 N 退出程序）："
MSG_EXIT_OK = "程序已退出"
MSG_PATH_EMPTY = "错误：文件路径不能为空"
MSG_GENERATING = "\n正在为文件生成 ed2k 链接：{}"
MSG_ED2K_RESULT = "生成的 ED2K 链接："
MSG_CLIPBOARD_OK = "✓ ED2K 链接已复制到剪贴板"
MSG_GENERATE_FAIL = "生成 ed2k 链接失败，请检查文件路径是否正确"
MSG_RHASH_WARN = "警告：未找到 RHash 程序，请确认路径：{}"


def copy_to_clipboard(text: str) -> None:
    """将文本复制到 Windows 剪贴板（使用系统自带 clip.exe）。"""
    try:
        subprocess.run(
            ["clip.exe"],
            input=text,
            encoding="utf-16-le",
            errors="ignore",
            check=True,
        )
    except Exception as e:
        print(MSG_CLIPBOARD_FAIL.format(e))


def get_ed2k_link(file_path: Path) -> str | None:
    """使用 RHash 生成文件的 ed2k 链接，失败返回 None。"""
    if not file_path.is_file():
        print(MSG_FILE_NOT_FOUND.format(file_path))
        return None

    command = [str(RHASH), "--uppercase", "--ed2k-link", str(file_path)]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            check=True,
        )
        return result.stdout.strip()
    except FileNotFoundError:
        print(MSG_RHASH_MISSING.format(RHASH))
        return None
    except subprocess.CalledProcessError as e:
        print(MSG_RHASH_ERROR.format(e))
        return None
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
    """主循环：输入文件路径 → 生成 ed2k 链接 → 复制到剪贴板。"""
    while True:
        try:
            raw = input(MSG_PROMPT_FILE).strip()

            if raw.lower() in ("quit", "exit", "n"):
                print(MSG_EXIT_OK)
                break

            # 移除路径两端的引号
            file_path = Path(raw.strip("\"'"))

            if raw == "" or str(file_path) == ".":
                print(MSG_PATH_EMPTY)
                continue

            print(MSG_GENERATING.format(file_path))
            ed2k_link = get_ed2k_link(file_path)

            if ed2k_link:
                print(MSG_ED2K_RESULT)
                print(ed2k_link)
                copy_to_clipboard(ed2k_link)
                print(MSG_CLIPBOARD_OK)
            else:
                print(MSG_GENERATE_FAIL)

        except KeyboardInterrupt:
            print(MSG_INTERRUPTED)
            break


# ==================== 程序入口 ====================

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if not RHASH.is_file():
        print(MSG_RHASH_WARN.format(RHASH))
    try:
        main()
    except KeyboardInterrupt:
        print(MSG_INTERRUPTED)
    except Exception as e:
        print(MSG_ERROR.format(e))
    finally:
        input(MSG_EXIT)
