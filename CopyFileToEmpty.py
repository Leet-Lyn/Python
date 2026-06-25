# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件夹位置（默认"d:\Studios\Folders\Ins\"）与目标文件夹位置（默认"d:\Studios\Folders\Outs\"）。
# 复制源文件夹位置内所有文件的文件名生成空文件到目标文件夹。

import signal
import sys
from pathlib import Path

# ==================== 全局配置 ====================

# 中断标志：Ctrl+Q（Windows msvcrt）或 SIGQUIT（Unix）设置
_quit_requested = False

DEFAULT_SOURCE_DIR = Path(r"d:\Studios\Folders\Ins")
DEFAULT_TARGET_DIR = Path(r"d:\Studios\Folders\Outs")

# --- 消息常量 ---
MSG_PROMPT_SOURCE_DIR = "请输入源文件夹位置："
MSG_PROMPT_TARGET_DIR = "请输入目标文件夹位置："
MSG_SOURCE_DIR_NOT_FOUND = "源文件夹 '{}' 不存在。"
MSG_SKIP_NON_FILE = "跳过非文件项：'{}'"
MSG_CREATED_EMPTY_FILE = "已创建空文件：'{}'"
MSG_CREATE_FILE_ERROR = "创建文件 '{}' 时发生错误：{}"
MSG_TOTAL_CREATED = "共创建 {} 个空文件"
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
    """注册中断处理：Unix SIGQUIT + Windows msvcrt 兼容。"""
    if hasattr(signal, "SIGQUIT"):
        signal.signal(signal.SIGQUIT, _on_quit_signal)


def _check_quit() -> bool:
    """检测是否请求退出（Windows Ctrl+Q 或 Unix SIGQUIT）。"""
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


def create_empty_files(source_dir: Path, target_dir: Path) -> int:
    """
    根据源文件夹内文件的文件名，在目标文件夹中生成对应的空文件。
    返回创建的空文件数量。
    """
    # 检查源文件夹是否存在
    if not source_dir.is_dir():
        print(MSG_SOURCE_DIR_NOT_FOUND.format(source_dir))
        return 0

    # 确保目标文件夹存在
    target_dir.mkdir(parents=True, exist_ok=True)

    # 遍历源文件夹内所有文件（仅顶层，不递归子文件夹）
    file_count = 0
    for p in source_dir.iterdir():
        if not p.is_file():
            print(MSG_SKIP_NON_FILE.format(p.name))
            continue

        target_file = target_dir / p.name
        try:
            target_file.write_text("", encoding="utf-8")
            print(MSG_CREATED_EMPTY_FILE.format(p.name))
            file_count += 1
        except OSError as e:
            print(MSG_CREATE_FILE_ERROR.format(p.name, e))

    return file_count


# ==================== 主程序 ====================


def main() -> None:
    """主函数：获取用户输入并执行空文件创建操作。"""

    # 获取用户输入
    _init_quit_handler()
    source_str = get_input_with_default(MSG_PROMPT_SOURCE_DIR, str(DEFAULT_SOURCE_DIR))
    target_str = get_input_with_default(MSG_PROMPT_TARGET_DIR, str(DEFAULT_TARGET_DIR))

    source_dir = Path(source_str)
    target_dir = Path(target_str)

    # 执行
    count = create_empty_files(source_dir, target_dir)
    print(MSG_TOTAL_CREATED.format(count))


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