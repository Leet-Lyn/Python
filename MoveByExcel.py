# 请帮我写个中文的 Python 脚本，批注也是中文，但是变量参数不要是中文：
# 在脚本开始前询问我 excel 文件位置（默认为：d:\Studios\Attachments\标准.xlsx）、源文件夹位置（默认为：d:\Studios\Folders\Ins\），目标文件夹位置（默认为：d:\Studios\Folders\Outs\）。
# Excel 第一行为表头（字段名）。此后每一行为一条记录。
# 从 excel 找到字段“加密文件名”，枚举每一条记录，根据每一条记录的“加密文件名”字段，在源文件夹及其子文件夹位置找到相应文件，移动到目标文件夹。
# 如果成功则在 excel 中“确定”字段中赋值“yes”。
# 完成后，反复循环我 excel 文件位置与源文件夹位置、目标文件夹位置。

import shutil
import sys
from pathlib import Path

import pandas as pd


def get_path(prompt: str, default_path: str) -> str:
    """获取用户输入路径，回车使用默认。"""
    raw = input(f"{prompt}（默认为：{default_path}）: ").strip()
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
        print("正在读取 Excel 文件...")
        df = pd.read_excel(excel_path, dtype=str, engine="openpyxl")
    except Exception as e:
        print(f"读取 Excel 文件失败：{e}")
        return False

    if "加密文件名" not in df.columns:
        print("Excel 中缺少字段 '加密文件名'，请检查表头。")
        return False

    if "确定" not in df.columns:
        df["确定"] = ""

    src = Path(source_dir)
    dst = Path(target_dir)
    if not src.is_dir():
        print(f"源文件夹不存在：{source_dir}")
        return False
    if not dst.is_dir():
        print(f"目标文件夹不存在，正在创建：{target_dir}")
        dst.mkdir(parents=True)

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
                print(f"已移动：{encrypted_name} (原路径: {src_path})")
            except Exception as e:
                print(f"移动文件失败 {encrypted_name}：{e}")
        else:
            print(f"源文件中未找到：{encrypted_name}（搜索目录：{source_dir} 及其子文件夹）")

    try:
        print(f"正在保存 Excel 文件：{excel_path}")
        df.to_excel(excel_path, index=False, engine="openpyxl")
        print(f"处理完成！共成功移动 {moved_count} 个文件，并已在 Excel 中标记 'yes'。")
        return True
    except Exception as e:
        print(f"保存 Excel 文件失败：{e}")
        return False


def main() -> None:
    """主循环：反复询问路径并执行处理。"""
    print("=== 加密文件批量移动工具（支持源文件夹递归搜索）===\n")
    while True:
        print("\n--- 新一轮处理 ---")
        excel_file = get_path("请输入 Excel 文件位置", r"d:\Studios\Attachments\标准.xlsx")
        source_folder = get_path("请输入源文件夹位置", r"d:\Studios\Folders\Ins")
        target_folder = get_path("请输入目标文件夹位置", r"d:\Studios\Folders\Outs")

        if not Path(excel_file).is_file():
            print(f"错误：Excel 文件不存在 -> {excel_file}")
        else:
            process_excel(excel_file, source_folder, target_folder)

        again = input("\n是否继续处理其他文件/文件夹？(y/n，默认 n): ").strip().lower()
        if again != "y":
            print("程序结束。")
            break


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
