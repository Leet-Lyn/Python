# 请帮我写个中文的 Python 脚本，批注也是中文，但是变量参数不要是中文：
# 在脚本开始前询问我 excel 文件位置（默认为：d:\Studios\Attachments\标准.xlsx）、源文件夹位置（默认为：d:\Studios\Folders\Ins\），目标文件夹位置（默认为：d:\Studios\Folders\Outs\）。
# Excel 第一行为表头（字段名）。此后每一行为一条记录。
# 从 excel 找到字段“加密文件名”，枚举每一条记录，根据每一条记录的“加密文件名”字段，在源文件夹及其子文件夹位置找到相应文件，移动到目标文件夹。
# 如果成功则在 excel 中“确定”字段中赋值“yes”。
# 完成后，反复循环我 excel 文件位置与源文件夹位置、目标文件夹位置。

import signal
import shutil
import sys
from pathlib import Path

import pandas as pd

# ==================== 全局配置 ====================

DEFAULT_EXCEL_PATH = r"d:\Studios\Attachments\标准.xlsx"
DEFAULT_SOURCE_DIR = r"d:\Studios\Folders\Ins"
DEFAULT_TARGET_DIR = r"d:\Studios\Folders\Outs"

_quit_requested = False  # Ctrl+Q 中断标志

# --- 消息常量 ---
MSG_INTERRUPTED = "\n\n用户中断程序，已退出。"
MSG_ERROR = "\n程序运行出错: {}"
MSG_EXIT = "\n按回车键退出..."
MSG_PROMPT_FORMAT = "{}（默认为：{}）: "
MSG_READING_EXCEL = "正在读取 Excel 文件..."
MSG_READ_EXCEL_FAILED = "读取 Excel 文件失败：{}"
MSG_MISSING_COLUMN = "Excel 中缺少字段 '加密文件名'，请检查表头。"
MSG_SOURCE_NOT_EXIST = "源文件夹不存在：{}"
MSG_TARGET_CREATING = "目标文件夹不存在，正在创建：{}"
MSG_MOVED = "已移动：{} (原路径: {})"
MSG_MOVE_FAILED = "移动文件失败 {}：{}"
MSG_NOT_FOUND = "源文件中未找到：{}（搜索目录：{} 及其子文件夹）"
MSG_SAVING_EXCEL = "正在保存 Excel 文件：{}"
MSG_DONE = "处理完成！共成功移动 {} 个文件，并已在 Excel 中标记 'yes'。"
MSG_SAVE_FAILED = "保存 Excel 文件失败：{}"
MSG_TITLE = "=== 加密文件批量移动工具（支持源文件夹递归搜索）===\n"
MSG_NEW_ROUND = "\n--- 新一轮处理 ---"
MSG_PROMPT_EXCEL = "请输入 Excel 文件位置"
MSG_PROMPT_SOURCE = "请输入源文件夹位置"
MSG_PROMPT_TARGET = "请输入目标文件夹位置"
MSG_FILE_NOT_EXIST = "错误：Excel 文件不存在 -> {}"
MSG_AGAIN = "\n是否继续处理其他文件/文件夹？(y/n，默认 n): "
MSG_END = "程序结束。"


def get_path(prompt: str, default_path: str) -> str:
    """获取用户输入路径，回车使用默认。"""
    raw = input(MSG_PROMPT_FORMAT.format(prompt, default_path)).strip()
    return raw if raw else default_path


def find_file_recursively(source_dir: str, filename: str) -> str | None:
    """在 source_dir 及其所有子文件夹中递归查找指定文件。"""
    for p in Path(source_dir).rglob(filename):
        if p.is_file():
            return str(p)
    return None


def process_excel(excel_path: str, source_dir: str, target_dir: str) -> bool:
    """根据"加密文件名"查找并移动文件，更新 Excel 中"确定"列。"""
    try:
        print(MSG_READING_EXCEL)
        df = pd.read_excel(excel_path, dtype=str, engine="openpyxl")
    except Exception as e:
        print(MSG_READ_EXCEL_FAILED.format(e))
        return False

    if "加密文件名" not in df.columns:
        print(MSG_MISSING_COLUMN)
        return False

    if "确定" not in df.columns:
        df["确定"] = ""

    src = Path(source_dir)
    dst = Path(target_dir)
    if not src.is_dir():
        print(MSG_SOURCE_NOT_EXIST.format(source_dir))
        return False
    if not dst.is_dir():
        print(MSG_TARGET_CREATING.format(target_dir))
        dst.mkdir(parents=True, exist_ok=True)

    moved_count = 0
    for idx, row in df.iterrows():
        if row.get("确定") == "yes":
            continue

        encrypted_name = row["加密文件名"]
        if pd.isna(encrypted_name) or encrypted_name == "":
            continue

        src_path = find_file_recursively(source_dir, encrypted_name)
        if src_path is not None:
            dst_path = dst / encrypted_name
            try:
                shutil.move(src_path, str(dst_path))
                df.at[idx, "确定"] = "yes"
                moved_count += 1
                print(MSG_MOVED.format(encrypted_name, src_path))
            except Exception as e:
                print(MSG_MOVE_FAILED.format(encrypted_name, e))
        else:
            print(MSG_NOT_FOUND.format(encrypted_name, source_dir))

    try:
        print(MSG_SAVING_EXCEL.format(excel_path))
        df.to_excel(excel_path, index=False, engine="openpyxl")
        print(MSG_DONE.format(moved_count))
        return True
    except Exception as e:
        print(MSG_SAVE_FAILED.format(e))
        return False
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
    """主循环：反复询问路径并执行处理。"""
    print(MSG_TITLE)
    while True:
        print(MSG_NEW_ROUND)
        excel_file = get_path(MSG_PROMPT_EXCEL, DEFAULT_EXCEL_PATH)
        source_folder = get_path(MSG_PROMPT_SOURCE, DEFAULT_SOURCE_DIR)
        target_folder = get_path(MSG_PROMPT_TARGET, DEFAULT_TARGET_DIR)

        if not Path(excel_file).is_file():
            print(MSG_FILE_NOT_EXIST.format(excel_file))
        else:
            process_excel(excel_file, source_folder, target_folder)

        again = input(MSG_AGAIN).strip().lower()
        if again != "y":
            print(MSG_END)
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
