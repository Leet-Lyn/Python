# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我是否采用正则表达式？默认不选择。
# 不选择正则表达式，则询问我源文件夹位置（默认为：d:\Studios\Folders\Downloads\）。依次在屏幕中询问我查找内容及替换内容。遍历源文件夹位置中所有的文件及子文件夹内文件（多种格式：txt、md、py、ahk等），读取每一文件，找到存放查找内容，用替换内容进行替换。
# 选择正则表达式，则询问我源文件夹位置（默认为：d:\Studios\Folders\Downloads\）。询问我存放查找内容的正则表达式文本位置（默认为：e:\Documents\Softwares\Codes\Python\RegexFind.txt）与存放替换内容的文本位置（默认为：e:\Documents\Softwares\Codes\Python\RegexReplace.txt）。遍历源文件夹位置中所有的文件及子文件夹内文件（多种格式：txt、md、py、ahk等），读取每一文件，找到存放查找内容，用替换内容进行替换。

import signal
import re
import sys
from pathlib import Path

# ==================== 全局配置 ====================

DEFAULT_SOURCE = Path(r"D:\Studios\Folders\Downloads")
DEFAULT_REGEX_FIND = Path(r"E:\Documents\Softwares\Codes\Python\RegexFind.txt")
DEFAULT_REGEX_REPLACE = Path(r"E:\Documents\Softwares\Codes\Python\RegexReplace.txt")
_quit_requested = False  # Ctrl+Q 中断标志

# 支持处理的文件扩展名
TEXT_EXTS = {
    ".txt", ".md", ".py", ".ahk", ".csv", ".json", ".xml", ".html", ".htm",
    ".css", ".js", ".ts", ".yaml", ".yml", ".ini", ".cfg", ".log", ".bat",
    ".cmd", ".ps1", ".sh", ".rb", ".lua", ".sql", ".tex", ".rst",
}

# --- 消息常量 ---
MSG_TITLE_BAR = "=" * 50
MSG_TITLE = "查找与替换工具"
MSG_PROMPT_USE_REGEX = "是否使用正则表达式？（回车默认 N，输入 Y 使用正则）："
MSG_PROMPT_SOURCE_DIR = "请输入源文件夹（回车默认 {}）："
MSG_ERROR_DIR_NOT_FOUND = "错误：文件夹 '{}' 不存在"
MSG_PROMPT_FIND = "请输入要查找的内容："
MSG_FIND_EMPTY = "查找内容为空，操作取消"
MSG_PROMPT_REPLACE = "请输入要替换的内容："
MSG_CONFIRM_PLAIN = "将在 {} 中查找 '{}' 并替换为 '{}'"
MSG_CONFIRM_PROMPT = "确认执行替换操作？(y/N)："
MSG_CANCELLED = "操作已取消"
MSG_PROCESS_OK = "  ✅ {}"
MSG_PLAIN_DONE = "普通查找与替换完成：修改 {} 个，扫描 {} 个。"
MSG_REGEX_DONE = "正则查找与替换完成：修改 {} 个，扫描 {} 个。"
MSG_PROMPT_REGEX_FILE = "请输入正则表达式文件（回车默认 {}）："
MSG_PROMPT_REPLACE_FILE = "请输入替换内容文件（回车默认 {}）："
MSG_ERROR_REGEX_FILE_NOT_FOUND = "查找正则表达式文件不存在：{}"
MSG_ERROR_REPLACE_FILE_NOT_FOUND = "替换内容文件不存在：{}"
MSG_ERROR_REGEX_INVALID = "正则表达式错误：{}"
MSG_REGEX_PREVIEW = "正则表达式：{}{}"
MSG_REGEX_ELLIPSIS = "..."
MSG_PROCESS_ERROR = "  处理文件 {} 时出错：{}"
MSG_INTERRUPTED = "\n\n用户中断程序，已退出。"
MSG_ERROR = "\n程序运行出错: {}"
MSG_EXIT = "\n按回车键退出..."


def process_plain(file_path: Path, find_content: str, replace_content: str) -> bool:
    """普通文本替换，有改动返回 True。"""
    try:
        content = file_path.read_text(encoding="utf-8")
        new_content = content.replace(find_content, replace_content)
        if new_content == content:
            return False
        file_path.write_text(new_content, encoding="utf-8")
        return True
    except Exception as e:
        print(MSG_PROCESS_ERROR.format(file_path, e))
        return False


def process_regex(file_path: Path, regex: re.Pattern, replace_content: str) -> bool:
    """正则表达式替换，有改动返回 True。"""
    try:
        content = file_path.read_text(encoding="utf-8")
        new_content = regex.sub(replace_content, content)
        if new_content == content:
            return False
        file_path.write_text(new_content, encoding="utf-8")
        return True
    except Exception as e:
        print(MSG_PROCESS_ERROR.format(file_path, e))
        return False


def run_plain_mode() -> None:
    """普通文本查找与替换。"""
    raw = input(MSG_PROMPT_SOURCE_DIR.format(DEFAULT_SOURCE)).strip()
    source_dir = Path(raw) if raw else DEFAULT_SOURCE

    if not source_dir.is_dir():
        print(MSG_ERROR_DIR_NOT_FOUND.format(source_dir))
        return

    find_content = input(MSG_PROMPT_FIND)
    if not find_content:
        print(MSG_FIND_EMPTY)
        return
    replace_content = input(MSG_PROMPT_REPLACE)

    print(MSG_CONFIRM_PLAIN.format(source_dir, find_content, replace_content))
    confirm = input(MSG_CONFIRM_PROMPT).strip().lower()
    if confirm != "y":
        print(MSG_CANCELLED)
        return

    ok = 0
    total = 0
    for file_path in source_dir.rglob("*"):
        if not file_path.is_file():
            continue
        if file_path.suffix.lower() not in TEXT_EXTS:
            continue
        total += 1
        if process_plain(file_path, find_content, replace_content):
            ok += 1
            print(MSG_PROCESS_OK.format(file_path))

    print(MSG_PLAIN_DONE.format(ok, total))


def run_regex_mode() -> None:
    """正则表达式查找与替换。"""
    raw = input(MSG_PROMPT_SOURCE_DIR.format(DEFAULT_SOURCE)).strip()
    source_dir = Path(raw) if raw else DEFAULT_SOURCE

    if not source_dir.is_dir():
        print(MSG_ERROR_DIR_NOT_FOUND.format(source_dir))
        return

    raw = input(MSG_PROMPT_REGEX_FILE.format(DEFAULT_REGEX_FIND)).strip()
    find_file = Path(raw) if raw else DEFAULT_REGEX_FIND
    raw = input(MSG_PROMPT_REPLACE_FILE.format(DEFAULT_REGEX_REPLACE)).strip()
    replace_file = Path(raw) if raw else DEFAULT_REGEX_REPLACE

    try:
        find_pattern = find_file.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        print(MSG_ERROR_REGEX_FILE_NOT_FOUND.format(find_file))
        return

    try:
        replace_content = replace_file.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(MSG_ERROR_REPLACE_FILE_NOT_FOUND.format(replace_file))
        return

    try:
        regex = re.compile(find_pattern, flags=re.MULTILINE)
    except re.error as e:
        print(MSG_ERROR_REGEX_INVALID.format(e))
        return

    ellipsis = MSG_REGEX_ELLIPSIS if len(find_pattern) > 80 else ""
    print(MSG_REGEX_PREVIEW.format(find_pattern[:80], ellipsis))
    confirm = input(MSG_CONFIRM_PROMPT).strip().lower()
    if confirm != "y":
        print(MSG_CANCELLED)
        return

    ok = 0
    total = 0
    for file_path in source_dir.rglob("*"):
        if not file_path.is_file():
            continue
        if file_path.suffix.lower() not in TEXT_EXTS:
            continue
        total += 1
        if process_regex(file_path, regex, replace_content):
            ok += 1
            print(MSG_PROCESS_OK.format(file_path))

    print(MSG_REGEX_DONE.format(ok, total))
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
    """主流程：选择模式 → 执行查找与替换。"""
    print(MSG_TITLE_BAR)
    print(MSG_TITLE)
    print(MSG_TITLE_BAR)

    choice = input(MSG_PROMPT_USE_REGEX).strip().lower()

    if choice == "y":
        run_regex_mode()
    else:
        run_plain_mode()



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