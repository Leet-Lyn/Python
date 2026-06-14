# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我是否采用正则表达式？默认不选择。
# 不选择正则表达式，则询问我源文件夹位置（默认为：d:\Studios\Folders\Downloads\）。依次在屏幕中询问我查找内容及替换内容。遍历源文件夹位置中所有的文件及子文件夹内文件（多种格式：txt、md、py、ahk等），读取每一文件，找到存放查找内容，用替换内容进行替换。
# 选择正则表达式，则询问我源文件夹位置（默认为：d:\Studios\Folders\Downloads\）。询问我存放查找内容的正则表达式文本位置（默认为：e:\Documents\Softwares\Codes\Python\RegexFind.txt）与存放替换内容的文本位置（默认为：e:\Documents\Softwares\Codes\Python\RegexReplace.txt）。遍历源文件夹位置中所有的文件及子文件夹内文件（多种格式：txt、md、py、ahk等），读取每一文件，找到存放查找内容，用替换内容进行替换。

import re
import sys
from pathlib import Path

# --- 常量 ---
DEFAULT_SOURCE = Path(r"D:\Studios\Folders\Downloads")
DEFAULT_REGEX_FIND = Path(r"E:\Documents\Softwares\Codes\Python\RegexFind.txt")
DEFAULT_REGEX_REPLACE = Path(r"E:\Documents\Softwares\Codes\Python\RegexReplace.txt")

# 支持处理的文件扩展名
TEXT_EXTS = {
    ".txt", ".md", ".py", ".ahk", ".csv", ".json", ".xml", ".html", ".htm",
    ".css", ".js", ".ts", ".yaml", ".yml", ".ini", ".cfg", ".log", ".bat",
    ".cmd", ".ps1", ".sh", ".rb", ".lua", ".sql", ".tex", ".rst",
}


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
        print(f"  处理文件 {file_path} 时出错：{e}")
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
        print(f"  处理文件 {file_path} 时出错：{e}")
        return False


def run_plain_mode() -> None:
    """普通文本查找与替换。"""
    raw = input(f"请输入源文件夹（回车默认 {DEFAULT_SOURCE}）：").strip()
    source_dir = Path(raw) if raw else DEFAULT_SOURCE

    if not source_dir.is_dir():
        print(f"错误：文件夹 '{source_dir}' 不存在")
        return

    find_content = input("请输入要查找的内容：")
    if not find_content:
        print("查找内容为空，操作取消")
        return
    replace_content = input("请输入要替换的内容：")

    print(f"\n将在 {source_dir} 中查找 '{find_content}' 并替换为 '{replace_content}'")
    confirm = input("确认执行替换操作？(y/N)：").strip().lower()
    if confirm != "y":
        print("操作已取消")
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
            print(f"  ✅ {file_path}")

    print(f"\n普通查找与替换完成：修改 {ok} 个，扫描 {total} 个。")


def run_regex_mode() -> None:
    """正则表达式查找与替换。"""
    raw = input(f"请输入源文件夹（回车默认 {DEFAULT_SOURCE}）：").strip()
    source_dir = Path(raw) if raw else DEFAULT_SOURCE

    if not source_dir.is_dir():
        print(f"错误：文件夹 '{source_dir}' 不存在")
        return

    raw = input(f"请输入正则表达式文件（回车默认 {DEFAULT_REGEX_FIND}）：").strip()
    find_file = Path(raw) if raw else DEFAULT_REGEX_FIND
    raw = input(f"请输入替换内容文件（回车默认 {DEFAULT_REGEX_REPLACE}）：").strip()
    replace_file = Path(raw) if raw else DEFAULT_REGEX_REPLACE

    try:
        find_pattern = find_file.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        print(f"查找正则表达式文件不存在：{find_file}")
        return

    try:
        replace_content = replace_file.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"替换内容文件不存在：{replace_file}")
        return

    try:
        regex = re.compile(find_pattern, flags=re.MULTILINE)
    except re.error as e:
        print(f"正则表达式错误：{e}")
        return

    print(f"\n正则表达式：{find_pattern[:80]}{'...' if len(find_pattern) > 80 else ''}")
    confirm = input("确认执行替换操作？(y/N)：").strip().lower()
    if confirm != "y":
        print("操作已取消")
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
            print(f"  ✅ {file_path}")

    print(f"\n正则查找与替换完成：修改 {ok} 个，扫描 {total} 个。")


def main() -> None:
    """主流程：选择模式 → 执行查找与替换。"""
    print("=" * 50)
    print("查找与替换工具")
    print("=" * 50)

    choice = input("是否使用正则表达式？（回车默认 N，输入 Y 使用正则）：").strip().lower()

    if choice == "y":
        run_regex_mode()
    else:
        run_plain_mode()


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
    input("按回车键退出...")
