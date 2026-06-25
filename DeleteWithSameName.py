# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件夹位置（默认为 d:\Studios\Folders\Ins\）与目标文件夹位置（默认为 d:\Studios\Folders\Outs\）。
# 询问我是否排除扩展名（扩展名可以不同，大小写敏感）。
# 依次读取目标文件夹的所有文件的文件名，如果源文件夹内存在名字相同的文件（大小写敏感），则删除源文件的文件。
# 要求如果文件夹内有子文件夹，递归实现。

import signal
import sys
from pathlib import Path

# ==================== 全局配置 ====================

DEFAULT_SOURCE_DIR = Path(r"d:\Studios\Folders\Ins")
DEFAULT_TARGET_DIR = Path(r"d:\Studios\Folders\Outs")
_quit_requested = False  # Ctrl+Q 中断标志

# --- 消息常量 ---
MSG_PROMPT_SOURCE_DIR = "请输入源文件夹路径："
MSG_PROMPT_TARGET_DIR = "请输入目标文件夹路径："
MSG_ERR_SOURCE_NOT_FOUND = "错误: 源文件夹不存在 [{}]"
MSG_ERR_TARGET_NOT_FOUND = "错误: 目标文件夹不存在 [{}]"
MSG_ERR_SAME_DIR = "错误: 源文件夹与目标文件夹相同，操作将删除全部文件，已阻止。"
MSG_EXCLUDE_EXT_PROMPT = "是否排除扩展名（仅匹配主文件名）？(y/n，默认 n): "
MSG_START_CLEANUP = "\n开始清理: {}"
MSG_REFERENCE_DIR = "参照目录: {}"
MSG_MATCH_MODE = "\n匹配模式：{}（大小写敏感）"
MSG_LABEL_STEM = "主文件名"
MSG_LABEL_FULLNAME = "完整文件名"
MSG_DELETED = "已删除: {}"
MSG_DELETE_FAILED = "删除失败: {} - {}"
MSG_DELETE_COMPLETE = "操作完成！共删除 {} 个文件，失败 {} 个。"
MSG_TARGET_FILE_COUNT = "目标文件夹文件总数: {}"
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


# ==================== 处理函数 ====================


def delete_duplicate_files(
    source_dir: Path,
    target_dir: Path,
    exclude_extension: bool = False,
) -> tuple[int, int]:
    """
    递归遍历目标文件夹，删除源文件夹中同名文件（大小写敏感）。
    若 exclude_extension=True，仅匹配主文件名（忽略扩展名）；
    否则匹配完整文件名。
    返回 (删除成功数, 删除失败数)。
    """
    # 第一步：收集目标文件夹匹配键
    if exclude_extension:
        target_keys = {p.stem for p in target_dir.rglob("*") if p.is_file()}
        get_key = lambda p: p.stem
        label = MSG_LABEL_STEM
    else:
        target_keys = {p.name for p in target_dir.rglob("*") if p.is_file()}
        get_key = lambda p: p.name
        label = MSG_LABEL_FULLNAME

    print(MSG_MATCH_MODE.format(label))

    # 第二步：遍历源文件夹并删除匹配文件
    deleted = 0
    failed = 0

    for src_file in source_dir.rglob("*"):
        if not src_file.is_file():
            continue
        if get_key(src_file) not in target_keys:
            continue

        try:
            src_file.unlink()
            print(MSG_DELETED.format(src_file))
            deleted += 1
        except OSError as e:
            print(MSG_DELETE_FAILED.format(src_file, e))
            failed += 1

    return deleted, failed


# ==================== 主程序 ====================


def main() -> None:
    """主函数：获取用户输入并执行重复文件删除。"""
    _init_quit_handler()

    source_str = get_input_with_default(MSG_PROMPT_SOURCE_DIR, str(DEFAULT_SOURCE_DIR))
    target_str = get_input_with_default(MSG_PROMPT_TARGET_DIR, str(DEFAULT_TARGET_DIR))

    source_dir = Path(source_str)
    target_dir = Path(target_str)

    if not source_dir.is_dir():
        print(MSG_ERR_SOURCE_NOT_FOUND.format(source_dir))
        return
    if not target_dir.is_dir():
        print(MSG_ERR_TARGET_NOT_FOUND.format(target_dir))
        return
    if source_dir.resolve() == target_dir.resolve():
        print(MSG_ERR_SAME_DIR)
        return

    # 询问是否排除扩展名
    ext_choice = input(MSG_EXCLUDE_EXT_PROMPT).strip().lower()
    exclude_extension = ext_choice in ("y", "yes")

    print(MSG_START_CLEANUP.format(source_dir))
    print(MSG_REFERENCE_DIR.format(target_dir))

    deleted, failed = delete_duplicate_files(source_dir, target_dir, exclude_extension)

    print(f"\n{'=' * 50}")
    print(MSG_DELETE_COMPLETE.format(deleted, failed))
    print(MSG_TARGET_FILE_COUNT.format(sum(1 for p in target_dir.rglob('*') if p.is_file())))
    print(f"{'=' * 50}")


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