# 请帮我写个中文的 Python 脚本，批注也是中文：
# 询问我复制还是删除。
# 选择复制，询问源文件夹（默认：d:\Studios\Folders\Ins\）与目标文件夹（默认：d:\Studios\Folders\Outs\）。根据源文件名（不包括扩展名），找出源文件夹里所有同名文件（扩展名可以不同），连同其父文件夹复制到目标文件夹中。
# 选择删除，询问源文件夹（默认：d:\Studios\Folders\Ins\）。删除源文件，同时 根据源文件名（不包括扩展名），找出源文件夹里所有同名文件（扩展名可以不同），一并删除。
# 完成后，再次循环。

import signal
import shutil
import sys
from pathlib import Path

# ==================== 全局配置 ====================

DEFAULT_SOURCE_DIR = Path(r"d:\Studios\Folders\Ins")
DEFAULT_TARGET_DIR = Path(r"d:\Studios\Folders\Outs")

_quit_requested = False  # Ctrl+Q 中断标志

# --- 消息常量 ---
MSG_INTERRUPTED = "\n\n用户中断程序，已退出。"
MSG_ERROR = "\n程序运行出错: {}"
MSG_EXIT = "\n按回车键退出..."
MSG_COPIED = "  已复制: {} -> {}"
MSG_COPY_FAILED = "  复制失败: {}\n    错误: {}"
MSG_NO_FILES_TO_DELETE = "  没有需要删除的文件。"
MSG_DELETE_PREVIEW_HEADER = "即将删除以下文件："
MSG_CONFIRM_DELETE_ALL = "确认删除以上所有文件吗？(y/n)："
MSG_DELETE_CANCELLED = "已取消删除操作。"
MSG_DELETED = "  已删除: {}"
MSG_DELETE_FAILED = "  删除失败: {}\n    错误: {}"
MSG_TOOL_TITLE = "=== 同名文件（不同扩展名）批量处理工具 ==="
MSG_SELECT_OPERATION = "请选择操作："
MSG_OPT_COPY = "  1 - 复制"
MSG_OPT_DELETE = "  2 - 删除"
MSG_OPT_EXIT = "  0 或 q - 退出"
MSG_ASK_CHOICE = "请输入数字 (1/2/0)："
MSG_PROGRAM_END = "程序结束。"
MSG_ASK_SRC_FILE = "请输入源文件路径（用于提取主文件名）："
MSG_ASK_SRC_FILE_DEL = "请输入源文件路径（用于提取主文件名，该文件本身也会被删除）："
MSG_ERR_NO_PATH = "错误：未输入文件路径，操作取消。"
MSG_ERR_FILE_NOT_FOUND = "错误：文件不存在 -> {}，操作取消。"
MSG_STEM_EXTRACTED = "提取的文件主名：{}"
MSG_ASK_SRC_DIR = "请输入源文件夹："
MSG_ASK_DST_DIR = "请输入目标文件夹："
MSG_ERR_SRC_DIR_NOT_EXIST = "错误：源文件夹不存在 -> {}，操作取消。"
MSG_NO_MATCH_IN_DIR = "在源文件夹 {} 中没有找到主名为 {} 的文件。"
MSG_FOUND_MATCHES = "找到 {} 个匹配的文件："
MSG_CONFIRM_COPY = "确认复制这些文件到目标文件夹吗？(y/n)："
MSG_COPY_CANCELLED = "复制操作已取消。"
MSG_COPY_COMPLETE = "复制完成：成功 {} / 总数 {}"
MSG_NO_FILES_TO_DELETE_STEM = "没有找到任何需要删除的文件（主名 {}）。"
MSG_WILL_DELETE_COUNT = "将要删除的文件（共 {} 个）："
MSG_CONFIRM_DELETE_PERMANENT = "确认永久删除以上所有文件吗？(y/n)："
MSG_DELETE_OP_CANCELLED = "删除操作已取消。"
MSG_DELETE_DONE = "删除操作执行完毕。"
MSG_INVALID_INPUT = "无效输入，请输入 1、2 或 0 退出。"
MSG_LIST_ITEM = "  {}"
MSG_DEFAULT_PROMPT_SUFFIX = " (默认: {}): "


# ==================== 辅助函数 ====================


def get_input_with_default(prompt_text: str, default_value: str) -> str:
    """获取带默认值的用户输入。"""
    user_input = input(f"{prompt_text}{MSG_DEFAULT_PROMPT_SUFFIX.format(default_value)}").strip()
    return user_input if user_input else str(default_value)


# ==================== 处理函数 ====================


def find_files_by_stem(root_dir: Path, stem: str) -> list[Path]:
    """
    在 root_dir 目录下递归查找所有主文件名等于 stem 的文件。
    """
    return [p for p in root_dir.rglob("*") if p.is_file() and p.stem == stem]


def copy_file_with_parents(src: Path, dst_root: Path, src_root: Path) -> bool:
    """
    将 src 复制到 dst_root，保留相对于 src_root 的目录结构。
    """
    try:
        rel = src.relative_to(src_root)
        dst = dst_root / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(src), str(dst))
        print(MSG_COPIED.format(src, dst))
        return True
    except OSError as e:
        print(MSG_COPY_FAILED.format(src, e))
        return False


def delete_files(file_paths: list[Path], confirm: bool = True) -> None:
    """删除给定的文件列表，可选确认。"""
    if not file_paths:
        print(MSG_NO_FILES_TO_DELETE)
        return

    print(MSG_DELETE_PREVIEW_HEADER)
    for f in file_paths:
        print(MSG_LIST_ITEM.format(f))

    if confirm:
        answer = input(MSG_CONFIRM_DELETE_ALL).strip().lower()
        if answer != "y":
            print(MSG_DELETE_CANCELLED)
            return

    for f in file_paths:
        try:
            f.unlink()
            print(MSG_DELETED.format(f))
        except OSError as e:
            print(MSG_DELETE_FAILED.format(f, e))


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
    print(MSG_TOOL_TITLE)

    while True:
        print("\n" + MSG_SELECT_OPERATION)
        print(MSG_OPT_COPY)
        print(MSG_OPT_DELETE)
        print(MSG_OPT_EXIT)
        choice = input(MSG_ASK_CHOICE).strip().lower()

        if choice in ("0", "q", "quit", "exit"):
            print(MSG_PROGRAM_END)
            break

        if choice == "1":
            # ---------- 复制模式 ----------
            src_input = get_input_with_default(MSG_ASK_SRC_FILE, "")
            if not src_input:
                print(MSG_ERR_NO_PATH)
                continue

            src_file = Path(src_input)
            if not src_file.is_file():
                print(MSG_ERR_FILE_NOT_FOUND.format(src_file))
                continue

            stem = src_file.stem
            print(MSG_STEM_EXTRACTED.format(stem))

            src_root_str = get_input_with_default(MSG_ASK_SRC_DIR, str(DEFAULT_SOURCE_DIR))
            src_root = Path(src_root_str)
            if not src_root.is_dir():
                print(MSG_ERR_SRC_DIR_NOT_EXIST.format(src_root))
                continue

            dst_root_str = get_input_with_default(MSG_ASK_DST_DIR, str(DEFAULT_TARGET_DIR))
            dst_root = Path(dst_root_str)
            dst_root.mkdir(parents=True, exist_ok=True)

            matched = find_files_by_stem(src_root, stem)
            if not matched:
                print(MSG_NO_MATCH_IN_DIR.format(src_root, stem))
                continue

            print(MSG_FOUND_MATCHES.format(len(matched)))
            for f in matched:
                print(MSG_LIST_ITEM.format(f))

            confirm = input(MSG_CONFIRM_COPY).strip().lower()
            if confirm != "y":
                print(MSG_COPY_CANCELLED)
                continue

            ok = sum(1 for f in matched if copy_file_with_parents(f, dst_root, src_root))
            print(MSG_COPY_COMPLETE.format(ok, len(matched)))

        elif choice == "2":
            # ---------- 删除模式 ----------
            src_input = get_input_with_default(MSG_ASK_SRC_FILE_DEL, "")
            if not src_input:
                print(MSG_ERR_NO_PATH)
                continue

            src_file = Path(src_input)
            if not src_file.is_file():
                print(MSG_ERR_FILE_NOT_FOUND.format(src_file))
                continue

            stem = src_file.stem
            print(MSG_STEM_EXTRACTED.format(stem))

            src_root_str = get_input_with_default(MSG_ASK_SRC_DIR, str(DEFAULT_SOURCE_DIR))
            src_root = Path(src_root_str)
            if not src_root.is_dir():
                print(MSG_ERR_SRC_DIR_NOT_EXIST.format(src_root))
                continue

            matched = find_files_by_stem(src_root, stem)
            if src_file not in matched:
                matched.append(src_file)

            # 去重（保持顺序）
            seen: set[str] = set()
            unique: list[Path] = []
            for f in matched:
                key = str(f.resolve())
                if key not in seen:
                    seen.add(key)
                    unique.append(f)
            matched = unique

            if not matched:
                print(MSG_NO_FILES_TO_DELETE_STEM.format(stem))
                continue

            print(MSG_WILL_DELETE_COUNT.format(len(matched)))
            for f in matched:
                print(MSG_LIST_ITEM.format(f))

            confirm = input(MSG_CONFIRM_DELETE_PERMANENT).strip().lower()
            if confirm != "y":
                print(MSG_DELETE_OP_CANCELLED)
                continue

            delete_files(matched, confirm=False)
            print(MSG_DELETE_DONE)

        else:
            print(MSG_INVALID_INPUT)


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
