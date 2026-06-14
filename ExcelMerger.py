# 请帮我写个中文的 Python 脚本，批注也是中文，但是变量参数不要是中文：
# 在脚本开始前询问我 excel 文件夹位置（默认为：d:\Studios\Attachments\）。
# 读取文件夹内所有 excel 文件，读取每一个 excel 文件，第一行为表头（字段名）。此后每一行为一条记录。
# 将所有 excel 文件，根据每一个 excel 文件的表头（字段名）进行合并（数据跟着表头（字段名）走），生成一个新的 excel 文件，文件名为父文件夹名。

import sys
from pathlib import Path

import pandas as pd


def get_folder_path(default: str) -> Path:
    """获取文件夹路径，回车使用默认。"""
    raw = input(f"请输入 Excel 文件夹路径（默认 {default}）：").strip()
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
            print(f"已读取：{file.name}，共 {len(df)} 行")
        except Exception as e:
            print(f"读取文件 {file} 时出错：{e}")
            continue

    if not data_frames:
        print("没有读取到任何有效数据，程序退出。")
        return None

    return pd.concat(data_frames, axis=0, join="outer", ignore_index=True)


def main() -> None:
    folder = get_folder_path(r"d:\Studios\Attachments")
    if not folder.is_dir():
        print(f"错误：文件夹 '{folder}' 不存在。")
        return

    excel_files = find_excel_files(folder)
    if not excel_files:
        print(f"在文件夹 '{folder}' 中未找到任何 Excel 文件。")
        return

    print(f"找到 {len(excel_files)} 个 Excel 文件。")

    merged = merge_excel_files(excel_files)
    if merged is None:
        return

    output_file = folder / f"{folder.name}.xlsx"
    try:
        merged.to_excel(output_file, index=False)
        print(f"合并完成，文件已保存为：{output_file}")
        print(f"总记录数：{len(merged)}，总字段数：{len(merged.columns)}")
    except Exception as e:
        print(f"保存文件时出错：{e}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
