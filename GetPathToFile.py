# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我文件夹位置，默认为"d:\Studios\Folders\Downloads\"；目标文件位置，默认为"d:\Studios\Attachments\Lists.txt"。
# 首先让我选择：当前文件夹还是包括子文件夹。
# 接下来让我选择：1. 仅仅文件夹；2. 仅仅文件；3. 文件夹与文件都要（文件夹在前）；4. 文件夹与文件都要（一起排序）。
# 将选中的路径排序后依次将绝对路径写入目标列表文件中，如无这列表文件就生成一个。同时写入剪贴板。

import signal
import subprocess
import sys
from pathlib import Path

# ==================== 全局配置 ====================

DEFAULT_SOURCE_DIR = Path(r"d:\Studios\Folders\Downloads")
DEFAULT_TARGET_FILE = Path(r"d:\Studios\Attachments\Lists.txt")

_quit_requested = False  # Ctrl+Q 中断标志

# --- 消息常量 ---
MSG_INTERRUPTED = "\n\n用户中断程序，已退出。"
MSG_ERROR = "\n程序运行出错: {}"
MSG_EXIT = "\n按回车键退出..."
MSG_CLIPBOARD_ERROR = "复制到剪贴板时发生错误：{}"
MSG_TITLE = "路径列表生成工具"
MSG_SCOPE_PROMPT = "\n请选择扫描范围："
MSG_SCOPE_CURRENT = "  1. 当前文件夹"
MSG_SCOPE_RECURSIVE = "  2. 包括子文件夹"
MSG_SCOPE_INPUT = "请输入选项 (默认 2): "
MSG_MODE_PROMPT = "\n请选择导出内容："
MSG_MODE_FOLDERS = "  1. 仅仅文件夹"
MSG_MODE_FILES = "  2. 仅仅文件"
MSG_MODE_BOTH_FOLDERS_FIRST = "  3. 文件夹与文件都要（文件夹在前）"
MSG_MODE_BOTH_SORTED = "  4. 文件夹与文件都要（一起排序）"
MSG_MODE_INPUT = "请输入选项 (默认 3): "
MSG_INVALID_OPTION = "无效选项：{}，使用默认 3。"
MSG_SCOPE_SUBDIR = "包括子文件夹"
MSG_SCOPE_CURRENT_ONLY = "仅当前文件夹"
MSG_PROMPT_SOURCE = "请输入源文件夹位置："
MSG_PROMPT_TARGET = "请输入目标文件位置："
MSG_SOURCE_NOT_EXIST = "错误：源文件夹不存在：{}"
MSG_CREATE_FOLDER_PROMPT = "是否要创建此文件夹？(y/n): "
MSG_FOLDER_CREATED = "已创建文件夹：{}"
MSG_FOLDER_CREATE_ERROR = "创建文件夹时发生错误：{}"
MSG_PROCESSING = "\n正在处理..."
MSG_SOURCE_LABEL = "源文件夹：{}"
MSG_TARGET_LABEL = "目标文件：{}"
MSG_PROCESS_FAILED = "✗ 处理失败，请检查错误信息"
MSG_WRITE_SUCCESS = "✓ 路径已成功写入到目标文件：{}"
MSG_FOUND_COUNT = "✓ 共找到 {} 个条目"
MSG_CLIPBOARD_SUCCESS = "✓ 路径列表已成功复制到剪贴板"
MSG_CLIPBOARD_WARN = "⚠ 路径列表已保存到文件，但未复制到剪贴板"
MSG_PREVIEW_HEADER = "\n前5个示例："
MSG_PREVIEW_MORE = "  ... 以及另外 {} 个条目"
MSG_WRITE_FILE_ERROR = "写入文件时发生错误：{}"
MSG_PROMPT_FORMAT = "{} (默认: {}): "

# ==================== 辅助函数 ====================


def get_input_with_default(prompt_text: str, default_value: str) -> str:
    """获取带默认值的用户输入。"""
    user_input = input(MSG_PROMPT_FORMAT.format(prompt_text, default_value)).strip()
    return user_input if user_input else str(default_value)


def copy_to_clipboard(text: str) -> bool:
    """将文本复制到 Windows 剪贴板（使用系统自带 clip.exe）。"""
    try:
        subprocess.run(
            ["clip.exe"],
            input=text,
            encoding="utf-16-le",
            errors="ignore",
            check=True,
        )
        return True
    except Exception as e:
        print(MSG_CLIPBOARD_ERROR.format(e))
        return False


# ==================== 处理函数 ====================


def collect_paths(
    source_dir: Path,
    include_subfolders: bool,
    mode: int,
) -> list[str]:
    """
    按条件收集路径。
      include_subfolders=False → 仅当前文件夹（iterdir，不递归）
      include_subfolders=True  → 递归所有子文件夹（rglob）
      mode=1: 仅文件夹
      mode=2: 仅文件
      mode=3: 文件夹 + 文件（文件夹在前，各自排序）
      mode=4: 文件夹 + 文件（混合排序）
    """
    iterator = source_dir.rglob("*") if include_subfolders else source_dir.iterdir()

    folders: list[str] = []
    files: list[str] = []

    for p in iterator:
        if p.is_dir():
            if p != source_dir:  # 排除源文件夹自身
                folders.append(str(p))
        elif p.is_file():
            files.append(str(p))

    if mode == 1:
        folders.sort(key=lambda x: str(Path(x).relative_to(source_dir)).lower())
        return folders
    elif mode == 2:
        files.sort()
        return files
    elif mode == 3:
        folders.sort(key=lambda x: str(Path(x).relative_to(source_dir)).lower())
        files.sort()
        return folders + files
    else:  # mode == 4
        all_paths = folders + files
        all_paths.sort()
        return all_paths


def write_paths_to_file(paths: list[str], target_file: Path) -> bool:
    """将路径列表写入目标文件，每行一个。返回是否成功。"""
    try:
        target_file.parent.mkdir(parents=True, exist_ok=True)
        target_file.write_text("\n".join(paths) + "\n", encoding="utf-8")
        return True
    except OSError as e:
        print(MSG_WRITE_FILE_ERROR.format(e))
        return False


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
    """主函数：获取用户输入，选择范围与模式，执行路径导出操作。"""
    print("=" * 60)
    print(MSG_TITLE)
    print("=" * 60)

    # —— 第一步：范围 ——
    print(MSG_SCOPE_PROMPT)
    print(MSG_SCOPE_CURRENT)
    print(MSG_SCOPE_RECURSIVE)
    scope_choice = input(MSG_SCOPE_INPUT).strip() or "2"
    include_subfolders = scope_choice == "2"

    # —— 第二步：内容 ——
    print(MSG_MODE_PROMPT)
    print(MSG_MODE_FOLDERS)
    print(MSG_MODE_FILES)
    print(MSG_MODE_BOTH_FOLDERS_FIRST)
    print(MSG_MODE_BOTH_SORTED)
    mode_choice = input(MSG_MODE_INPUT).strip() or "3"
    if mode_choice not in ("1", "2", "3", "4"):
        print(MSG_INVALID_OPTION.format(mode_choice))
        mode_choice = "3"
    mode = int(mode_choice)

    scope_label = MSG_SCOPE_SUBDIR if include_subfolders else MSG_SCOPE_CURRENT_ONLY
    mode_labels = {1: MSG_MODE_FOLDERS.strip(), 2: MSG_MODE_FILES.strip(), 3: MSG_MODE_BOTH_FOLDERS_FIRST.strip(), 4: MSG_MODE_BOTH_SORTED.strip()}
    print(f"\n{MSG_SCOPE_SUBDIR if include_subfolders else MSG_SCOPE_CURRENT_ONLY} | {mode_labels[mode]}")

    # —— 路径输入 ——
    source_str = get_input_with_default(MSG_PROMPT_SOURCE, str(DEFAULT_SOURCE_DIR))
    target_str = get_input_with_default(MSG_PROMPT_TARGET, str(DEFAULT_TARGET_FILE))

    source_dir = Path(source_str)
    target_file = Path(target_str)

    if not source_dir.is_dir():
        print(MSG_SOURCE_NOT_EXIST.format(source_dir))
        create = input(MSG_CREATE_FOLDER_PROMPT).strip().lower()
        if create == "y":
            try:
                source_dir.mkdir(parents=True, exist_ok=True)
                print(MSG_FOLDER_CREATED.format(source_dir))
            except OSError as e:
                print(MSG_FOLDER_CREATE_ERROR.format(e))
                return
        else:
            return

    print(MSG_PROCESSING)
    print(MSG_SOURCE_LABEL.format(source_dir))
    print(MSG_TARGET_LABEL.format(target_file))

    # —— 收集 & 写入 ——
    paths = collect_paths(source_dir, include_subfolders, mode)
    if not write_paths_to_file(paths, target_file):
        print(MSG_PROCESS_FAILED)
        return

    print(MSG_WRITE_SUCCESS.format(target_file))
    print(MSG_FOUND_COUNT.format(len(paths)))

    if paths:
        text = "\n".join(paths)
        if copy_to_clipboard(text):
            print(MSG_CLIPBOARD_SUCCESS)
        else:
            print(MSG_CLIPBOARD_WARN)

        print(MSG_PREVIEW_HEADER)
        for i, p in enumerate(paths[:5], 1):
            print(f"  {i}. {p}")
        if len(paths) > 5:
            print(MSG_PREVIEW_MORE.format(len(paths) - 5))


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
