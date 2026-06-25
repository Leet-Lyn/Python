# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问原文件位置与目标文件夹（默认为 "Z:\"）位置。
# 尝试将原文件向目标文件夹移动。
# 如果无法移动，则重命名原文件（从后删除1个字符（不包括扩展名）），再次尝试将原文件向目标文件夹移动。
# 反复循环，直至能将原文件向目标文件夹移动。
# 将生成的文件名，写入剪贴板。
# 最后询问我是否继续，默认（"y"，或回车），返回开头，询问原文件位置与目标文件夹（默认为 "Z:\"）位置。按"n"，择退出。

# 导入模块
import signal
import shutil
import subprocess
import sys
from pathlib import Path

# ==================== 全局配置 ====================

DEFAULT_TARGET_DIR = Path("Z:\\")
_quit_requested = False  # Ctrl+Q 中断标志

MSG_PROMPT_SOURCE = "请输入原文件的完整路径"
MSG_PROMPT_TARGET = "请输入目标文件夹位置"
MSG_SOURCE_INVALID = "输入的原文件路径无效，请重新输入。"
MSG_TARGET_CREATED = "目标文件夹已创建：{}"
MSG_TARGET_CREATE_FAILED = "创建目标文件夹失败：{}"
MSG_MOVE_FAILED = "文件移动失败：{}"
MSG_STEM_EXHAUSTED = "文件名已无法缩短，无法移动文件。"
MSG_FILE_RENAMED = "文件已重命名为：{}"
MSG_RENAME_FAILED = "文件重命名失败：{}"
MSG_CLIPBOARD_FAILED = "复制到剪贴板失败：{}"
MSG_SUCCESS = "文件已成功移动至：{}"
MSG_CLIPBOARD_COPIED = "文件路径已复制到剪贴板：{}"
MSG_OPERATION_FAILED = "操作失败。"
MSG_ASK_CONTINUE = "是否继续操作？（Y 继续，N 退出）"
MSG_PROGRAM_END = "程序结束。"
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
    user_input = input(f"{prompt_text} (默认: {default_value}): ").strip()
    return user_input if user_input else str(default_value)


def copy_to_clipboard(text: str) -> None:
    """将文本复制到 Windows 剪贴板（使用系统自带 clip.exe）。"""
    try:
        # Windows 自带 clip.exe，无需额外依赖
        subprocess.run(
            ["clip.exe"],
            input=text,
            encoding="utf-16-le",
            errors="ignore",
            check=True,
        )
    except Exception as e:
        print(MSG_CLIPBOARD_FAILED.format(e))


def try_move_file(source: Path, target_dir: Path, stem: str, suffix: str) -> Path | None:
    """
    尝试将文件移动到目标目录。
    若因文件名冲突失败，则逐次缩短文件名（每次从末尾去掉一个字符，
    不含扩展名）并重试，直到移动成功或文件名长度耗尽。
    """
    while True:
        new_name = f"{stem}{suffix}"
        target = target_dir / new_name

        try:
            # 跨盘移动使用 shutil.move；同盘时它会用 os.rename（高效）
            shutil.move(str(source), str(target))
            return target  # 成功，返回目标 Path
        except shutil.Error as e:
            print(MSG_MOVE_FAILED.format(e))
        except OSError as e:
            print(MSG_MOVE_FAILED.format(e))

        if len(stem) <= 1:
            print(MSG_STEM_EXHAUSTED)
            return None

        stem = stem[:-1]
        new_source = source.with_stem(stem)

        try:
            source.rename(new_source)
            source = new_source
            print(MSG_FILE_RENAMED.format(source))
        except OSError as rename_error:
            print(MSG_RENAME_FAILED.format(rename_error))
            return None


# ==================== 主程序 ====================


def main() -> None:
    """主循环：获取输入 → 移动文件 → 复制路径到剪贴板 → 询问是否继续。"""
    _init_quit_handler()
    while True:
        if _check_quit():
            print(MSG_INTERRUPTED)
            break
        # --- 获取原文件路径 ---
        raw = get_input_with_default(MSG_PROMPT_SOURCE, "")
        source = Path(raw)

        if not source.is_file():
            print(MSG_SOURCE_INVALID)
            continue

        # --- 获取目标文件夹 ---
        raw_target = get_input_with_default(MSG_PROMPT_TARGET, str(DEFAULT_TARGET_DIR))
        target_dir = Path(raw_target)

        # 确保目标文件夹存在
        if not target_dir.exists():
            try:
                target_dir.mkdir(parents=True)
                print(MSG_TARGET_CREATED.format(target_dir))
            except OSError as e:
                print(MSG_TARGET_CREATE_FAILED.format(e))
                continue

        # --- 执行移动 ---
        stem = source.stem
        suffix = source.suffix
        result = try_move_file(source, target_dir, stem, suffix)

        if result is not None:
            target_str = str(result)
            copy_to_clipboard(target_str)
            print(MSG_SUCCESS.format(target_str))
            print(MSG_CLIPBOARD_COPIED.format(target_str))
        else:
            print(MSG_OPERATION_FAILED)
            break

        # --- 询问是否继续 ---
        cont = get_input_with_default(MSG_ASK_CONTINUE, "y").strip().lower()
        if cont == "n":
            print(MSG_PROGRAM_END)
            break



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