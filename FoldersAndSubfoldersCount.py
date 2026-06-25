# 请帮我写个中文的 Python 脚本，批注也是中文：
# 询问我询问源文件夹位置（默认：d:\Studios\Folders\Downloads\）。
# 1. 检索该文件夹下，所有一级子文件夹（不包括其下子文件夹）。列出子文件夹数量。
# 2. 分别检索该文件夹下，所有一级子文件夹（不包括其下子文件夹），枚举出所有一级子文件夹下所拥有的文件数量。最后汇总：有1个文件的子文件夹子文件夹有几个，分别是：……有2个文件的子文件夹子文件夹有几个，分别是：……有3个文件的子文件夹子文件夹有几个，分别是：……以此类推。
# 完成后，跳到开始询问我源文件夹位置。反复循环。

import signal
import sys
from pathlib import Path

# ==================== 全局配置 ====================

DEFAULT_SOURCE_DIR = Path(r"d:\Studios\Folders\Downloads")

_quit_requested = False  # Ctrl+Q 中断标志

# --- 消息常量 ---

MSG_INPUT_SOURCE_DIR = "请输入源文件夹位置（输入 exit 退出）"
MSG_EXIT_PROGRAM = "程序已退出。"
MSG_DIR_NOT_FOUND = "错误：文件夹不存在或路径无效，请重新输入。\n"
MSG_PERMISSION_ERROR = "错误：没有权限访问文件夹 {}，请检查权限后重试。\n"
MSG_SUBDIR_COUNT = "\n一级子文件夹数量：{}"
MSG_NO_SUBDIRS = "没有找到任何一级子文件夹。\n"
MSG_SUB_PERMISSION_WARN = "警告：无法访问子文件夹 {}，已跳过该文件夹的统计。"
MSG_FILE_COUNT_GROUP = "有 {} 个文件的子文件夹有 {} 个，分别是：{}"
MSG_SEPARATOR = "\n--------------------------------------------------\n"
MSG_INTERRUPTED = "\n\n用户中断程序，已退出。"
MSG_ERROR = "\n程序运行出错: {}"
MSG_EXIT = "\n按回车键退出..."

# ==================== 辅助函数 ====================


def get_input_with_default(prompt_text: str, default_value: str) -> str:
    """获取带默认值的用户输入。"""
    user_input = input(f"{prompt_text} (默认: {default_value}): ").strip()
    return user_input if user_input else str(default_value)


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
    """
    主循环：反复询问源文件夹路径，执行统计并输出结果。
    """

    default_str = str(DEFAULT_SOURCE_DIR)

    while True:
        user_input = get_input_with_default(MSG_INPUT_SOURCE_DIR, default_str)

        if user_input.lower() in ("exit", "quit"):
            print(MSG_EXIT_PROGRAM)
            break

        source_dir = Path(user_input)

        if not source_dir.is_dir():
            print(MSG_DIR_NOT_FOUND)
            continue

        # ----------------------------------------------------------------
        # 1. 获取一级子文件夹（不递归）
        # ----------------------------------------------------------------
        try:
            subdirs = [p for p in source_dir.iterdir() if p.is_dir()]
        except PermissionError:
            print(MSG_PERMISSION_ERROR.format(source_dir))
            continue

        print(MSG_SUBDIR_COUNT.format(len(subdirs)))
        if not subdirs:
            print(MSG_NO_SUBDIRS)
            continue

        # ----------------------------------------------------------------
        # 2. 统计每个一级子文件夹下的文件数量（不递归）
        # ----------------------------------------------------------------
        file_count_map: dict[str, int] = {}
        for sub in subdirs:
            try:
                file_count_map[sub.name] = sum(
                    1 for e in sub.iterdir() if e.is_file()
                )
            except PermissionError:
                print(MSG_SUB_PERMISSION_WARN.format(sub.name))
                continue

        # ----------------------------------------------------------------
        # 3. 按文件数量分组输出
        # ----------------------------------------------------------------
        groups: dict[int, list[str]] = {}
        for name, cnt in file_count_map.items():
            groups.setdefault(cnt, []).append(name)

        for cnt in sorted(groups):
            folder_list = groups[cnt]
            print(MSG_FILE_COUNT_GROUP.format(cnt, len(folder_list), ", ".join(folder_list)))

        print(MSG_SEPARATOR)


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
