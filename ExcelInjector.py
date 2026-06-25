# 请帮我写个中文的 Python 脚本，批注也是中文，但是变量参数是英文的：
# 在脚本开始前询问我主 excel 文件位置（默认为：d:\Studios\Attachments\main.xlsx）与客 excel 文件位置（默认为：d:\Studios\Attachments\secondary.xlsx）。
# 主 excel 与 客 excel，第一行为表头（字段名）。此后每一行为一条记录。二者字段名多少与记录多少并不一致。
# 从主 excel 找到字段"现文件名"，枚举每一条记录，根据每一条记录的"现文件名"字段，在客 excel 中找到该记录，将该记录的"加密文件名"字段读取，写入主 excel 的"加密文件名"字段去。将该记录的"矫正文件名"字段读取，写入主 excel 的"矫正文件名"字段去。如果成功则在客 excel 中"确定"字段中赋值"yes"。
# 如果出错，给出详细信息。
# 完成后，反复循环我主 excel 文件位置与客 excel 文件位置。

import signal
import sys
import traceback
from pathlib import Path

import pandas as pd

# ==================== 全局配置 ====================

DEFAULT_MAIN_PATH = r"d:\Studios\Attachments\main.xlsx"
DEFAULT_SECONDARY_PATH = r"d:\Studios\Attachments\secondary.xlsx"

_quit_requested = False  # Ctrl+Q 中断标志

# --- 消息常量 ---
MSG_INTERRUPTED = "\n\n用户中断程序，已退出。"
MSG_ERROR = "\n程序运行出错: {}"
MSG_EXIT = "\n按回车键退出..."
MSG_PROMPT_FORMAT = "{} (默认: {}): "
MSG_FILE_NOT_EXIST = "错误：文件不存在 -> {}"
MSG_READING_MAIN = "正在读取主文件..."
MSG_READING_SECONDARY = "正在读取客文件..."
MSG_MAIN_MISSING_COL = "提示：主表缺少列 '{}'，已自动添加。"
MSG_SEC_MISSING_COL = "提示：客表缺少列 '{}'，已自动添加。"
MSG_EMPTY_FILENAME = '警告：主表第 {} 行的"现文件名"为空，已跳过。'
MSG_MATCH_SUCCESS = "匹配成功: {} -> 加密文件: {}, 矫正文件: {}"
MSG_NO_MATCH = "未找到匹配: {}"
MSG_SAVING_MAIN = "正在保存主文件..."
MSG_SAVING_SECONDARY = "正在保存客文件..."
MSG_DONE = "\n处理完成！共匹配 {} 条记录。"
MSG_MAIN_SAVED = "主文件已保存: {}"
MSG_SEC_SAVED = "客文件已保存: {}"
MSG_PROCESS_ERROR = "处理过程中发生错误: {}: {}"
MSG_DETAILED_TRACEBACK = "详细堆栈信息："
MSG_TITLE = "=== Excel 字段匹配工具（现文件名 → 加密文件名 + 矫正文件名）==="
MSG_DESC = '说明：主表需要包含"现文件名"字段，客表需要包含"现文件名"、"加密文件名"、"矫正文件名"字段。\n'
MSG_SPECIFY_FILES = "\n--- 请指定本次要处理的文件 ---"
MSG_PROMPT_MAIN = "请输入主 Excel 文件位置"
MSG_PROMPT_SEC = "请输入客 Excel 文件位置"
MSG_MAIN_INVALID = "主文件无效，请重新输入。"
MSG_SEC_INVALID = "客文件无效，请重新输入。"
MSG_AGAIN = "\n是否继续处理其他文件？(y/n): "
MSG_END = "程序结束。"


def get_file_path(prompt: str, default_path: str) -> str | None:
    """获取文件路径，回车用默认；文件不存在返回 None。"""
    user_input = input(MSG_PROMPT_FORMAT.format(prompt, default_path)).strip()
    path = user_input if user_input else default_path
    if not Path(path).is_file():
        print(MSG_FILE_NOT_EXIST.format(path))
        return None
    return path


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


def process_excel(main_path: str, secondary_path: str) -> None:
    """根据主表"现文件名"匹配客表，注入"加密文件名"和"矫正文件名"。"""
    try:
        print(MSG_READING_MAIN)
        main_df = pd.read_excel(main_path)
        print(MSG_READING_SECONDARY)
        secondary_df = pd.read_excel(secondary_path)

        required_main_cols = ["现文件名", "加密文件名", "矫正文件名"]
        for col in required_main_cols:
            if col not in main_df.columns:
                main_df[col] = None
                print(MSG_MAIN_MISSING_COL.format(col))

        required_secondary_cols = ["现文件名", "加密文件名", "矫正文件名", "确定"]
        for col in required_secondary_cols:
            if col not in secondary_df.columns:
                secondary_df[col] = None
                print(MSG_SEC_MISSING_COL.format(col))

        match_count = 0
        for idx, main_row in main_df.iterrows():
            current_name = main_row["现文件名"]
            if pd.isna(current_name):
                print(MSG_EMPTY_FILENAME.format(idx + 2))
                continue

            match_idx = secondary_df[secondary_df["现文件名"] == current_name].index
            if len(match_idx) > 0:
                matched_index = match_idx[0]
                encrypted_name = secondary_df.at[matched_index, "加密文件名"]
                corrected_name = secondary_df.at[matched_index, "矫正文件名"]

                main_df.at[idx, "加密文件名"] = encrypted_name
                main_df.at[idx, "矫正文件名"] = corrected_name
                secondary_df.at[matched_index, "确定"] = "yes"
                match_count += 1
                print(MSG_MATCH_SUCCESS.format(current_name, encrypted_name, corrected_name))
            else:
                print(MSG_NO_MATCH.format(current_name))

        print(MSG_SAVING_MAIN)
        # 先写入临时文件，成功后再替换原文件，防止写入失败损坏数据
        temp_main = Path(str(main_path) + '.tmp')
        main_df.to_excel(temp_main, index=False)
        temp_main.replace(main_path)

        print(MSG_SAVING_SECONDARY)
        temp_sec = Path(str(secondary_path) + '.tmp')
        secondary_df.to_excel(temp_sec, index=False)
        temp_sec.replace(secondary_path)

        print(MSG_DONE.format(match_count))
        print(MSG_MAIN_SAVED.format(main_path))
        print(MSG_SEC_SAVED.format(secondary_path))

    except Exception as e:
        print(MSG_PROCESS_ERROR.format(type(e).__name__, e))
        print(MSG_DETAILED_TRACEBACK)
        traceback.print_exc()


def main() -> None:
    """主循环：反复输入主/客 Excel 文件对。"""
    _init_quit_handler()
    print(MSG_TITLE)
    print(MSG_DESC)

    while True:
        print(MSG_SPECIFY_FILES)
        main_path = get_file_path(MSG_PROMPT_MAIN, DEFAULT_MAIN_PATH)
        if main_path is None:
            print(MSG_MAIN_INVALID)
            continue

        secondary_path = get_file_path(MSG_PROMPT_SEC, DEFAULT_SECONDARY_PATH)
        if secondary_path is None:
            print(MSG_SEC_INVALID)
            continue

        process_excel(main_path, secondary_path)

        again = input(MSG_AGAIN).strip().lower()
        if again == "n":
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