# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我文件夹位置（默认"d:\Studios\Folders\Downloads\"）与想要删除的字段（默认"（Via："）。
# 将文件夹及其子文件夹内所有文件以文件内容读出重命名为文件名（不包括扩展名，最长 20 个字符）。
# 再文件夹及其子文件夹内所有文件重命名，从某一字段开始至末尾删除（不包括扩展名）。

import signal
import sys
from pathlib import Path

# ==================== 全局配置 ====================

DEFAULT_SOURCE_DIR = Path(r"d:\Studios\Folders\Downloads")
DEFAULT_FIELD = "（Via："
MAX_CONTENT_LENGTH = 20
_quit_requested = False  # Ctrl+Q 中断标志

# --- 消息常量 ---
MSG_WELCOME = "欢迎使用文件批量重命名工具！"
MSG_PROMPT_SOURCE_DIR = "请输入文件夹路径："
MSG_PROMPT_FIELD = "请输入想要删除的字段："
MSG_DIR_NOT_EXIST = "错误：文件夹 '{}' 不存在或不是有效的文件夹。"
MSG_WILL_PROCESS_DIR = "\n即将处理文件夹：{}"
MSG_WILL_EXECUTE = "将执行以下操作："
MSG_OP1_DESC = "1. 根据文件内容重命名文件（文件名最长20个字符）"
MSG_OP2_DESC = "2. 删除文件名中 '{}' 及其后面的内容"
MSG_CONFIRM_EXEC = "确认执行操作？(y/n): "
MSG_CANCELLED = "操作已取消。"
MSG_STEP1_HEADER = "\n=== 第一步：根据文件内容重命名 ==="
MSG_STEP2_HEADER = "\n=== 第二步：删除指定字段后的内容 ==="
MSG_OPERATION_DONE = "\n操作完成！"
MSG_CONTENT_RENAME_COUNT = "内容重命名：{} 个文件"
MSG_FIELD_DELETE_COUNT = "字段删除：{} 个文件"
MSG_CANNOT_READ_CONTENT = "无法读取文件内容 {}：{}"
MSG_SKIP_NO_CONTENT = "跳过文件（无法读取内容）：{}"
MSG_WARN_TARGET_EXISTS_SKIP = "警告：目标文件 '{}' 已存在，跳过 '{}'"
MSG_RENAMED = "已将 '{}' 重命名为 '{}'"
MSG_CANNOT_RENAME = "错误：无法重命名文件 '{}'，{}"
MSG_SKIP_NO_FIELD = "跳过文件：'{}'（不包含字段 '{}'）"
MSG_INPUT_DEFAULT_HINT = " (默认: {}): "
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


def get_input_with_default(prompt_text: str, default_value: str) -> str:
    """获取带默认值的用户输入。"""
    user_input = input(f"{prompt_text}{MSG_INPUT_DEFAULT_HINT.format(default_value)}").strip()
    return user_input if user_input else str(default_value)


def read_file_content(file_path: Path, max_length: int = MAX_CONTENT_LENGTH) -> str | None:
    """
    读取文件内容作为新文件名（不含扩展名）。
    返回新文件名，失败时返回 None。
    """
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore").strip()
        content = " ".join(content.split())
        if len(content) > max_length:
            content = content[:max_length]
        return content if content else None
    except OSError as e:
        print(MSG_CANNOT_READ_CONTENT.format(file_path.name, e))
        return None


# ==================== 处理函数 ====================


def rename_by_content(source_dir: Path) -> tuple[int, int]:
    """根据文件内容重命名所有文件。返回 (重命名数, 跳过数)。"""
    renamed = 0
    skipped = 0

    for file_path in source_dir.rglob("*"):
        if not file_path.is_file():
            continue

        new_name = read_file_content(file_path)
        if not new_name:
            print(MSG_SKIP_NO_CONTENT.format(file_path.name))
            skipped += 1
            continue

        new_path = file_path.parent / (new_name + file_path.suffix)
        if new_path.exists():
            print(MSG_WARN_TARGET_EXISTS_SKIP.format(new_path.name, file_path.name))
            skipped += 1
            continue

        try:
            file_path.rename(new_path)
            print(MSG_RENAMED.format(file_path.name, new_path.name))
            renamed += 1
        except OSError as e:
            print(MSG_CANNOT_RENAME.format(file_path.name, e))
            skipped += 1

    return renamed, skipped


def remove_field_from_filenames(source_dir: Path, field: str) -> tuple[int, int]:
    """删除文件名中指定字段及其后内容。返回 (重命名数, 跳过数)。"""
    renamed = 0
    skipped = 0

    for file_path in source_dir.rglob("*"):
        if not file_path.is_file():
            continue

        if field not in file_path.stem:
            print(MSG_SKIP_NO_FIELD.format(file_path.name, field))
            skipped += 1
            continue

        try:
            index = file_path.stem.index(field)
            prefix = file_path.stem[:index]
            new_name = prefix + file_path.suffix
            new_path = file_path.parent / new_name

            if new_path.exists():
                print(MSG_WARN_TARGET_EXISTS_SKIP.format(new_name, file_path.name))
                skipped += 1
                continue

            file_path.rename(new_path)
            print(MSG_RENAMED.format(file_path.name, new_name))
            renamed += 1
        except OSError as e:
            print(MSG_CANNOT_RENAME.format(file_path.name, e))
            skipped += 1

    return renamed, skipped


# ==================== 主程序 ====================


def main() -> None:
    """主函数：获取用户输入并调用重命名函数。"""
    _init_quit_handler()
    print(MSG_WELCOME)

    source_str = get_input_with_default(MSG_PROMPT_SOURCE_DIR, str(DEFAULT_SOURCE_DIR))
    field = get_input_with_default(MSG_PROMPT_FIELD, DEFAULT_FIELD)

    source_dir = Path(source_str)
    if not source_dir.is_dir():
        print(MSG_DIR_NOT_EXIST.format(source_dir))
        return

    print(MSG_WILL_PROCESS_DIR.format(source_dir))
    print(MSG_WILL_EXECUTE)
    print(MSG_OP1_DESC)
    print(MSG_OP2_DESC.format(field))
    confirm = input(MSG_CONFIRM_EXEC).strip().lower()
    if confirm != "y":
        print(MSG_CANCELLED)
        return

    print(MSG_STEP1_HEADER)
    content_renamed, _ = rename_by_content(source_dir)

    print(MSG_STEP2_HEADER)
    field_renamed, _ = remove_field_from_filenames(source_dir, field)

    print(MSG_OPERATION_DONE)
    print(MSG_CONTENT_RENAME_COUNT.format(content_renamed))
    print(MSG_FIELD_DELETE_COUNT.format(field_renamed))


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