# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件夹位置（默认"d:\Studios\Folders\Ins\"）与目标文件夹位置（默认"d:\Studios\Folders\Outs\"）。
# 复制源文件夹结构到目标文件夹中，但不复制文件。

import signal
import sys
from pathlib import Path

# ==================== 全局配置 ====================

DEFAULT_SOURCE_DIR = Path(r"d:\Studios\Folders\Ins")
DEFAULT_TARGET_DIR = Path(r"d:\Studios\Folders\Outs")
_quit_requested = False  # Ctrl+Q 中断标志

# --- 消息常量 ---
MSG_PROMPT_SOURCE_DIR = "请输入源文件夹位置："
MSG_PROMPT_TARGET_DIR = "请输入目标文件夹位置："
MSG_SOURCE_DIR_NOT_FOUND = "源文件夹 '{}' 不存在。"
MSG_CREATED_FOLDER = "已创建文件夹：'{}'"
MSG_COPY_COMPLETE = "文件夹结构复制完成！共创建 {} 个文件夹。"
MSG_INPUT_DEFAULT_HINT = " (默认: {}): "
MSG_INTERRUPTED = "\n\n用户中断程序，已退出。"
MSG_ERROR = "\n程序运行出错: {}"
MSG_EXIT = "\n按回车键退出..."

# ==================== 中断处理 ====================


def _on_quit_signal(signum, frame):
    r"""Ctrl+Q / Ctrl+\ 中断处理：标记退出，保留临时文件。"""
    global _quit_requested
    _quit_requested = True
    raise KeyboardInterrupt()


def _init_quit_handler():
    """注册中断处理。"""
    if hasattr(signal, "SIGQUIT"):
        signal.signal(signal.SIGQUIT, _on_quit_signal)


def _check_quit() -> bool:
    """检测 Windows Ctrl+Q 或 Unix SIGQUIT 是否触发。"""
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


def copy_folder_structure(source_dir: Path, target_dir: Path) -> int:
    """
    从源文件夹复制文件夹结构到目标文件夹，但不复制文件。
    返回创建的文件夹数量。
    """
    # 检查源文件夹是否存在
    if not source_dir.is_dir():
        print(MSG_SOURCE_DIR_NOT_FOUND.format(source_dir))
        return 0

    # 确保目标根文件夹存在
    target_dir.mkdir(parents=True, exist_ok=True)

    # 收集源文件夹下所有子目录（递归），排除根目录自身
    # 按路径深度排序，确保父目录先于子目录处理
    all_dirs = sorted(
        (p for p in source_dir.rglob("*") if p.is_dir()),
        key=lambda p: len(p.parts),
    )

    count = 0
    for sub_dir in all_dirs:
        rel = sub_dir.relative_to(source_dir)
        new_dir = target_dir / rel
        if not new_dir.is_dir():
            new_dir.mkdir(parents=True, exist_ok=True)
            print(MSG_CREATED_FOLDER.format(new_dir))
            count += 1

    return count


# ==================== 主程序 ====================


def main() -> None:
    """主函数：获取用户输入并执行文件夹结构复制操作。"""

    _init_quit_handler()
    source_str = get_input_with_default(MSG_PROMPT_SOURCE_DIR, str(DEFAULT_SOURCE_DIR))
    target_str = get_input_with_default(MSG_PROMPT_TARGET_DIR, str(DEFAULT_TARGET_DIR))

    source_dir = Path(source_str)
    target_dir = Path(target_str)

    count = copy_folder_structure(source_dir, target_dir)
    print(MSG_COPY_COMPLETE.format(count))


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