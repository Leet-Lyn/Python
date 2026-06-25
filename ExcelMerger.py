# 请帮我写个中文的 Python 脚本，批注也是中文，但是变量参数不要是中文：
# 在脚本开始前询问我 excel 文件夹位置（默认为：d:\Studios\Attachments\）。
# 读取文件夹内所有 excel 文件，读取每一个 excel 文件，第一行为表头（字段名）。此后每一行为一条记录。
# 将所有 excel 文件，根据每一个 excel 文件的表头（字段名）进行合并（数据跟着表头（字段名）走），生成一个新的 excel 文件，文件名为父文件夹名。

import signal
import sys
from pathlib import Path

import pandas as pd

# ==================== 全局配置 ====================

DEFAULT_FOLDER = r"d:\Studios\Attachments"

_quit_requested = False  # Ctrl+Q 中断标志

# --- 消息常量 ---
MSG_INTERRUPTED = "\n\n用户中断程序，已退出。"
MSG_ERROR = "\n程序运行出错: {}"
MSG_EXIT = "\n按回车键退出..."
MSG_PROMPT_FOLDER = "请输入 Excel 文件夹路径（默认 {}）："
MSG_READ_FILE = "已读取：{}，共 {} 行"
MSG_READ_ERROR = "读取文件 {} 时出错：{}"
MSG_NO_DATA = "没有读取到任何有效数据，程序退出。"
MSG_FOLDER_NOT_EXIST = "错误：文件夹 '{}' 不存在。"
MSG_NO_EXCEL_FOUND = "在文件夹 '{}' 中未找到任何 Excel 文件。"
MSG_FOUND_FILES = "找到 {} 个 Excel 文件。"
MSG_MERGE_DONE = "合并完成，文件已保存为：{}"
MSG_SUMMARY = "总记录数：{}，总字段数：{}"
MSG_SAVE_ERROR = "保存文件时出错：{}"

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


def get_folder_path(default: str) -> Path:
    """获取文件夹路径，回车使用默认。"""
    raw = input(MSG_PROMPT_FOLDER.format(default)).strip()
    return Path(raw).resolve() if raw else Path(default).resolve()


def find_excel_files(folder: Path) -> list[Path]:
    """查找文件夹内所有 Excel 文件（.xlsx / .xls / .xlsm）。"""
    excel_exts = {".xlsx", ".xls", ".xlsm"}
    return sorted(p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in excel_exts)


def merge_excel_files(file_list: list[Path]) -> pd.DataFrame | None:
    """读取所有 Excel 文件，按列名合并数据。"""
    data_frames: list[pd.DataFrame] = []
    for file in file_list:
        try:
            df = pd.read_excel(file, header=0)
            data_frames.append(df)
            print(MSG_READ_FILE.format(file.name, len(df)))
        except Exception as e:
            print(MSG_READ_ERROR.format(file, e))
            continue

    if not data_frames:
        print(MSG_NO_DATA)
        return None

    return pd.concat(data_frames, axis=0, join="outer", ignore_index=True)


def main() -> None:
    _init_quit_handler()
    folder = get_folder_path(DEFAULT_FOLDER)
    if not folder.is_dir():
        print(MSG_FOLDER_NOT_EXIST.format(folder))
        return

    excel_files = find_excel_files(folder)
    if not excel_files:
        print(MSG_NO_EXCEL_FOUND.format(folder))
        return

    print(MSG_FOUND_FILES.format(len(excel_files)))

    merged = merge_excel_files(excel_files)
    if merged is None:
        return

    output_file = folder / f"{folder.name}.xlsx"
    try:
        merged.to_excel(output_file, index=False)
        print(MSG_MERGE_DONE.format(output_file))
        print(MSG_SUMMARY.format(len(merged), len(merged.columns)))
    except Exception as e:
        print(MSG_SAVE_ERROR.format(e))



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