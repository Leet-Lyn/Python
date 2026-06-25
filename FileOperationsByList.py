# 请帮我写个中文的 Python 脚本，批注也是中文，但是变量参数不要是中文：
# 询问我需要的操作：
# 1. 移动：询问我列表路径（默认"d:\Studios\Attachments\Lists.txt"）。源文件夹路径（默认"d:\Studios\Folders\Ins\"）与目标文件夹路径（默认"d:\Studios\Folders\Outs\"）。列表里一行一个文件名（有扩展名）。请枚举每一行的文件名，找到源文件夹里匹配的文件，移动到目标文件夹。
# 2. 复制：询问我列表路径（默认"d:\Studios\Attachments\Lists.txt"）。源文件夹路径（默认"d:\Studios\Folders\Ins\"）与目标文件夹路径（默认"d:\Studios\Folders\Outs\"）。列表里一行一个文件名（有扩展名）。请枚举每一行的文件名，找到源文件夹里匹配的文件，复制到目标文件夹。
# 3. 重命名：询问我列表路径（默认"d:\Studios\Attachments\Lists.txt"）。源文件夹路径（默认"d:\Studios\Folders\Ins\"）。列表里一行一个文件名（有扩展名）。请枚举每一行的文件名，重命名文件夹里的路径（按名称排序）。不涉及文件夹。
# 4. 文件路径生成：询问我列表路径（默认"d:\Studios\Attachments\Lists.txt"）。源文件夹路径（默认"d:\Studios\Folders\Ins\"）。询问我是否匹配文件夹，询问我是否包含子文件夹里。将源文件夹路径里的所有文件的路径写入列表中。
# 5. 文件名生成列表（包含子文件夹里）：询问我列表路径（默认"d:\Studios\Attachments\Lists.txt"）。源文件夹路径（默认"d:\Studios\Folders\Ins\"）。询问我是否匹配文件夹，询问我是否包含子文件夹里。将源文件夹路径里的所有文件的名称写入列表中。
# 结束后重复询问。

import signal
import shutil
import sys
from pathlib import Path

# ==================== 全局配置 ====================

DEFAULT_LIST_PATH = Path(r"d:\Studios\Attachments\Lists.txt")
DEFAULT_SOURCE_DIR = Path(r"d:\Studios\Folders\Ins")
DEFAULT_TARGET_DIR = Path(r"d:\Studios\Folders\Outs")

_quit_requested = False  # Ctrl+Q 中断标志

# --- 消息常量 ---
MSG_INTERRUPTED = "\n\n用户中断程序，已退出。"
MSG_ERROR = "\n程序运行出错: {}"
MSG_EXIT = "\n按回车键退出..."
MSG_ERR_LIST_NOT_FOUND = "错误：列表文件不存在 -> {}"
MSG_ERR_SRC_DIR_NOT_EXIST = "错误：源文件夹不存在 -> {}"
MSG_WARN_FILE_NOT_FOUND = "警告：未找到文件，跳过 -> {}"
MSG_WARN_TARGET_EXISTS = "警告：目标已存在，跳过 -> {}"
MSG_MOVED = "已移动: {}"
MSG_MOVE_COMPLETE = "移动完成，共处理 {} 个文件。"
MSG_COPIED = "已复制: {}"
MSG_COPY_COMPLETE = "复制完成，共处理 {} 个文件。"
MSG_RENAME_COUNT_MISMATCH = "警告：源文件夹有 {} 个文件，列表提供 {} 个名称，数量不匹配。"
MSG_ASK_CONTINUE_RENAME = "是否仍要继续重命名？(y/n): "
MSG_OPERATION_CANCELLED = "操作已取消。"
MSG_SKIP_SAME_NAME = "跳过（名称未变）: {}"
MSG_WARN_NEW_NAME_EXISTS = "警告：目标名称已存在，跳过 -> {}"
MSG_RENAMED = "重命名: {} -> {}"
MSG_RENAME_COMPLETE = "重命名完成，共处理 {} 个文件。"
MSG_PATH_LIST_GENERATED = "已生成路径列表，共 {} 条，保存至: {}"
MSG_NAME_LIST_GENERATED = "已生成名称列表，共 {} 条，保存至: {}"
MSG_TOOL_TITLE = "===== 文件管理工具（列表驱动）====="
MSG_OPT_MOVE = "1. 移动"
MSG_OPT_COPY = "2. 复制"
MSG_OPT_RENAME = "3. 重命名"
MSG_OPT_PATH_LIST = "4. 文件路径生成"
MSG_OPT_NAME_LIST = "5. 文件名生成列表"
MSG_OPT_EXIT = "0. 退出"
MSG_ASK_CHOICE = "请输入数字(0-5): "
MSG_PROGRAM_EXIT = "程序已退出。"
MSG_ASK_LIST_PATH = "列表文件路径"
MSG_ASK_SRC_DIR = "源文件夹路径"
MSG_ASK_DST_DIR = "目标文件夹路径"
MSG_ASK_INCLUDE_FOLDERS = "是否包含文件夹路径？(y/n)"
MSG_ASK_INCLUDE_SUBDIRS = "是否包含子文件夹？(y/n)"
MSG_ASK_INCLUDE_FOLDER_NAMES = "是否包含文件夹名称？(y/n)"
MSG_INVALID_CHOICE = "无效的选择，请输入 0-5 之间的数字。"
MSG_PRESS_ENTER = "\n按回车键继续..."
MSG_SECTION_MOVE = "\n--- 移动文件 ---"
MSG_SECTION_COPY = "\n--- 复制文件 ---"
MSG_SECTION_RENAME = "\n--- 重命名文件 ---"
MSG_SECTION_PATH_LIST = "\n--- 生成文件路径列表 ---"
MSG_SECTION_NAME_LIST = "\n--- 生成文件名列表 ---"
MSG_DEFAULT_PROMPT_SUFFIX = " (默认: {}): "

# ==================== 辅助函数 ====================


def get_input_with_default(prompt_text: str, default_value: str) -> str:
    """获取用户输入，若直接回车则返回默认值。"""
    user_input = input(f"{prompt_text}{MSG_DEFAULT_PROMPT_SUFFIX.format(default_value)}").strip()
    return user_input if user_input else str(default_value)


def read_list_file(file_path: Path) -> list[str]:
    """读取列表文件，每行一个文件名，忽略空行。"""
    if not file_path.is_file():
        print(MSG_ERR_LIST_NOT_FOUND.format(file_path))
        return []
    text = file_path.read_text(encoding="utf-8-sig")
    return [line.strip() for line in text.splitlines() if line.strip()]


def collect_entries(
    src_dir: Path, include_folders: bool, include_subdirs: bool,
) -> list[str]:
    """收集源文件夹中的文件（及可选文件夹）路径。"""
    iterator = src_dir.rglob("*") if include_subdirs else src_dir.iterdir()
    entries: list[str] = []
    for p in iterator:
        if p.is_file():
            entries.append(str(p))
        elif p.is_dir() and include_folders:
            entries.append(str(p))
    entries.sort()
    return entries


# ==================== 核心操作 ====================


def move_files(list_path: Path, src_dir: Path, dst_dir: Path) -> None:
    """根据列表文件名，从源文件夹移动到目标文件夹。"""
    names = read_list_file(list_path)
    if not names:
        return
    if not src_dir.is_dir():
        print(MSG_ERR_SRC_DIR_NOT_EXIST.format(src_dir))
        return
    dst_dir.mkdir(parents=True, exist_ok=True)

    moved = 0
    for name in names:
        src_path = src_dir / name
        dst_path = dst_dir / name
        if not src_path.is_file():
            print(MSG_WARN_FILE_NOT_FOUND.format(src_path))
            continue
        if dst_path.exists():
            print(MSG_WARN_TARGET_EXISTS.format(dst_path))
            continue
        shutil.move(str(src_path), str(dst_path))
        print(MSG_MOVED.format(name))
        moved += 1
    print(MSG_MOVE_COMPLETE.format(moved))


def copy_files(list_path: Path, src_dir: Path, dst_dir: Path) -> None:
    """根据列表文件名，从源文件夹复制到目标文件夹。"""
    names = read_list_file(list_path)
    if not names:
        return
    if not src_dir.is_dir():
        print(MSG_ERR_SRC_DIR_NOT_EXIST.format(src_dir))
        return
    dst_dir.mkdir(parents=True, exist_ok=True)

    copied = 0
    for name in names:
        src_path = src_dir / name
        dst_path = dst_dir / name
        if not src_path.is_file():
            print(MSG_WARN_FILE_NOT_FOUND.format(src_path))
            continue
        if dst_path.exists():
            print(MSG_WARN_TARGET_EXISTS.format(dst_path))
            continue
        shutil.copy2(str(src_path), str(dst_path))
        print(MSG_COPIED.format(name))
        copied += 1
    print(MSG_COPY_COMPLETE.format(copied))


def rename_files(list_path: Path, src_dir: Path) -> None:
    """按名称排序后，依次重命名为列表中提供的新名称。"""
    new_names = read_list_file(list_path)
    if not new_names:
        return
    if not src_dir.is_dir():
        print(MSG_ERR_SRC_DIR_NOT_EXIST.format(src_dir))
        return

    old_names = sorted(p.name for p in src_dir.iterdir() if p.is_file())
    if len(old_names) != len(new_names):
        print(MSG_RENAME_COUNT_MISMATCH.format(len(old_names), len(new_names)))
        if input(MSG_ASK_CONTINUE_RENAME).strip().lower() != "y":
            print(MSG_OPERATION_CANCELLED)
            return

    renamed = 0
    for old_name, new_name in zip(old_names, new_names):
        if old_name == new_name:
            print(MSG_SKIP_SAME_NAME.format(old_name))
            continue
        new_path = src_dir / new_name
        if new_path.exists():
            print(MSG_WARN_NEW_NAME_EXISTS.format(new_name))
            continue
        (src_dir / old_name).rename(new_path)
        print(MSG_RENAMED.format(old_name, new_name))
        renamed += 1
    print(MSG_RENAME_COMPLETE.format(renamed))


def generate_path_list(
    list_path: Path, src_dir: Path, include_folders: bool, include_subdirs: bool,
) -> None:
    """生成文件（及可选文件夹）路径列表写入指定文件。"""
    if not src_dir.is_dir():
        print(MSG_ERR_SRC_DIR_NOT_EXIST.format(src_dir))
        return
    entries = collect_entries(src_dir, include_folders, include_subdirs)
    list_path.parent.mkdir(parents=True, exist_ok=True)
    list_path.write_text("\n".join(entries) + "\n", encoding="utf-8")
    print(MSG_PATH_LIST_GENERATED.format(len(entries), list_path))


def generate_name_list(
    list_path: Path, src_dir: Path, include_folders: bool, include_subdirs: bool,
) -> None:
    """生成文件名（及可选文件夹名）列表写入指定文件。"""
    if not src_dir.is_dir():
        print(MSG_ERR_SRC_DIR_NOT_EXIST.format(src_dir))
        return
    entries = collect_entries(src_dir, include_folders, include_subdirs)
    names = [Path(e).name for e in entries]
    list_path.parent.mkdir(parents=True, exist_ok=True)
    list_path.write_text("\n".join(names) + "\n", encoding="utf-8")
    print(MSG_NAME_LIST_GENERATED.format(len(names), list_path))


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
    while True:
        print("\n" + MSG_TOOL_TITLE)
        print(MSG_OPT_MOVE)
        print(MSG_OPT_COPY)
        print(MSG_OPT_RENAME)
        print(MSG_OPT_PATH_LIST)
        print(MSG_OPT_NAME_LIST)
        print(MSG_OPT_EXIT)
        choice = input(MSG_ASK_CHOICE).strip()

        if choice == "0":
            print(MSG_PROGRAM_EXIT)
            break

        elif choice == "1":
            print(MSG_SECTION_MOVE)
            lst = Path(get_input_with_default(MSG_ASK_LIST_PATH, str(DEFAULT_LIST_PATH)))
            src = Path(get_input_with_default(MSG_ASK_SRC_DIR, str(DEFAULT_SOURCE_DIR)))
            dst = Path(get_input_with_default(MSG_ASK_DST_DIR, str(DEFAULT_TARGET_DIR)))
            move_files(lst, src, dst)

        elif choice == "2":
            print(MSG_SECTION_COPY)
            lst = Path(get_input_with_default(MSG_ASK_LIST_PATH, str(DEFAULT_LIST_PATH)))
            src = Path(get_input_with_default(MSG_ASK_SRC_DIR, str(DEFAULT_SOURCE_DIR)))
            dst = Path(get_input_with_default(MSG_ASK_DST_DIR, str(DEFAULT_TARGET_DIR)))
            copy_files(lst, src, dst)

        elif choice == "3":
            print(MSG_SECTION_RENAME)
            lst = Path(get_input_with_default(MSG_ASK_LIST_PATH, str(DEFAULT_LIST_PATH)))
            src = Path(get_input_with_default(MSG_ASK_SRC_DIR, str(DEFAULT_SOURCE_DIR)))
            rename_files(lst, src)

        elif choice == "4":
            print(MSG_SECTION_PATH_LIST)
            lst = Path(get_input_with_default(MSG_ASK_LIST_PATH, str(DEFAULT_LIST_PATH)))
            src = Path(get_input_with_default(MSG_ASK_SRC_DIR, str(DEFAULT_SOURCE_DIR)))
            inc_folders = get_input_with_default(MSG_ASK_INCLUDE_FOLDERS, "n").lower() == "y"
            inc_sub = get_input_with_default(MSG_ASK_INCLUDE_SUBDIRS, "n").lower() == "y"
            generate_path_list(lst, src, inc_folders, inc_sub)

        elif choice == "5":
            print(MSG_SECTION_NAME_LIST)
            lst = Path(get_input_with_default(MSG_ASK_LIST_PATH, str(DEFAULT_LIST_PATH)))
            src = Path(get_input_with_default(MSG_ASK_SRC_DIR, str(DEFAULT_SOURCE_DIR)))
            inc_folders = get_input_with_default(MSG_ASK_INCLUDE_FOLDER_NAMES, "n").lower() == "y"
            inc_sub = get_input_with_default(MSG_ASK_INCLUDE_SUBDIRS, "n").lower() == "y"
            generate_name_list(lst, src, inc_folders, inc_sub)

        else:
            print(MSG_INVALID_CHOICE)

        input(MSG_PRESS_ENTER)


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
