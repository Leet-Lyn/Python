# 请帮我写个中文的 Python 脚本，批注也是中文，但是变量参数是英文的：
# 在脚本开始前询问我主 excel 文件位置（默认为：d:\Studios\Attachments\main.xlsx）与客 excel 文件位置（默认为：d:\Studios\Attachments\secondary.xlsx）。
# 主 excel 与 客 excel，第一行为表头（字段名）。此后每一行为一条记录。二者字段名多少与记录多少并不一致。
# 从主 excel 找到字段“现文件名”，枚举每一条记录，根据每一条记录的“现文件名”字段，在客 excel 中找到该记录，将该记录的“加密文件名”字段读取，写入主 excel 的“加密文件名”字段去。将该记录的“矫正文件名”字段读取，写入主 excel 的“矫正文件名”字段去。如果成功则在客 excel 中“确定”字段中赋值“yes”。
# 如果出错，给出详细信息。
# 完成后，反复循环我主 excel 文件位置与客 excel 文件位置。

import sys
import traceback
from pathlib import Path

import pandas as pd


def get_file_path(prompt: str, default_path: str) -> str | None:
    """获取文件路径，回车用默认；文件不存在返回 None。"""
    user_input = input(f"{prompt} (默认: {default_path}): ").strip()
    path = user_input if user_input else default_path
    if not Path(path).is_file():
        print(f"错误：文件不存在 -> {path}")
        return None
    return path


def process_excel(main_path: str, secondary_path: str) -> None:
    """根据主表"现文件名"匹配客表，注入"加密文件名"和"矫正文件名"。"""
    try:
        print("正在读取主文件...")
        main_df = pd.read_excel(main_path)
        print("正在读取客文件...")
        secondary_df = pd.read_excel(secondary_path)

        required_main_cols = ["现文件名", "加密文件名", "矫正文件名"]
        for col in required_main_cols:
            if col not in main_df.columns:
                main_df[col] = None
                print(f"提示：主表缺少列 '{col}'，已自动添加。")

        required_secondary_cols = ["现文件名", "加密文件名", "矫正文件名", "确定"]
        for col in required_secondary_cols:
            if col not in secondary_df.columns:
                secondary_df[col] = None
                print(f"提示：客表缺少列 '{col}'，已自动添加。")

        match_count = 0
        for idx, main_row in main_df.iterrows():
            current_name = main_row["现文件名"]
            if pd.isna(current_name):
                print(f'警告：主表第 {idx+2} 行的“现文件名”为空，已跳过。')
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
                print(f"匹配成功: {current_name} -> 加密文件: {encrypted_name}, 矫正文件: {corrected_name}")
            else:
                print(f"未找到匹配: {current_name}")

        print("正在保存主文件...")
        main_df.to_excel(main_path, index=False)
        print("正在保存客文件...")
        secondary_df.to_excel(secondary_path, index=False)

        print(f"\n处理完成！共匹配 {match_count} 条记录。")
        print(f"主文件已保存: {main_path}")
        print(f"客文件已保存: {secondary_path}")

    except Exception as e:
        print(f"处理过程中发生错误: {type(e).__name__}: {e}")
        print("详细堆栈信息：")
        traceback.print_exc()


def main() -> None:
    """主循环：反复输入主/客 Excel 文件对。"""
    print("=== Excel 字段匹配工具（现文件名 → 加密文件名 + 矫正文件名）===")
    print('说明：主表需要包含"现文件名"字段，客表需要包含"现文件名"、"加密文件名"、"矫正文件名"字段。\n')

    while True:
        print("\n--- 请指定本次要处理的文件 ---")
        main_path = get_file_path("请输入主 Excel 文件位置", r"d:\Studios\Attachments\main.xlsx")
        if main_path is None:
            print("主文件无效，请重新输入。")
            continue

        secondary_path = get_file_path("请输入客 Excel 文件位置", r"d:\Studios\Attachments\secondary.xlsx")
        if secondary_path is None:
            print("客文件无效，请重新输入。")
            continue

        process_excel(main_path, secondary_path)

        again = input("\n是否继续处理其他文件？(y/n): ").strip().lower()
        if again != "y":
            print("程序结束。")
            break


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
