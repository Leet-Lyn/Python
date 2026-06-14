# 请帮我写个中文的 Python 脚本，批注也是中文，但是变量参数不要是中文：
# 询问我需要的操作：
# 1. 移动：询问我 excel 路径（默认"d:\Studios\Attachments\标准.xlsx"）。源文件夹路径（默认"d:\Studios\Folders\Ins\"）与目标文件夹路径（默认"d:\Studios\Folders\Outs\"）。读取 excel 文件，第一行为表头（字段名），此后每一行为一条记录。依次根据每一行的"原文件名"，在源文件夹路径找到后移动到目标文件夹。
# 2. 复制：询问我 excel 路径（默认"d:\Studios\Attachments\标准.xlsx"）。源文件夹路径（默认"d:\Studios\Folders\Ins\"）与目标文件夹路径（默认"d:\Studios\Folders\Outs\"）。读取 excel 文件，第一行为表头（字段名），此后每一行为一条记录。依次根据每一行的"原文件名"，在源文件夹路径找到后复制到目标文件夹。
# 3. 重命名：询问我 excel 路径（默认"d:\Studios\Attachments\标准.xlsx"）。源文件夹路径（默认"d:\Studios\Folders\Ins\"）。读取 excel 文件，第一行为表头（字段名），此后每一行为一条记录。依次根据每一行的"原文件名"，在源文件夹路径找到后改名为"现文件名"。
# 4. 记录写入：询问我 excel 路径（默认"d:\Studios\Attachments\标准.xlsx"）。源文件夹路径（默认"d:\Studios\Folders\Ins\"）。询问我是否包含子文件夹里的文件。读取 excel 文件，此后每一行为一条记录。根据源文件夹下文件写入该 excel 文件。要求只添加记录，不修改已经生成的记录。1. 每一条记录新开一行。2. "Index"字段值为上一行 "Index"字段值+1（如上一行为空或为表头，则"Index"字段值为 1）。3. 将源文件夹路径里的所有文件的文件名写入 excel 文件的"名字"与"原文件名"字段值"（名字字段不包括扩展名，原文件名包括扩展名）。
# 5. 记录删除：询问我 excel 路径（默认"d:\Studios\Attachments\标准.xlsx"）。源文件夹路径（默认"d:\Studios\Folders\Ins\"）。询问我是否包含子文件夹里的文件；询问我匹配的字段是"原文件名"还是"现文件名"。读取 excel 文件，此后每一行为一条记录。枚举源文件夹路径里的所有文件的文件名, 将匹配到 excel 文件的相应字段值的行（记录）进行删除。最后提示我在源文件夹里还有什么文件没有在原 excel 文件里，列出那些文件。
# 结束后重复询问。

import shutil
import sys
from pathlib import Path

from openpyxl import Workbook, load_workbook

# ==================== 全局配置 ====================

DEFAULT_EXCEL_PATH = Path(r"d:\Studios\Attachments\标准.xlsx")
DEFAULT_SOURCE_DIR = Path(r"d:\Studios\Folders\Ins")
DEFAULT_TARGET_DIR = Path(r"d:\Studios\Folders\Outs")

# ==================== 辅助函数 ====================


def get_input_with_default(prompt_text: str, default_value: str) -> str:
    """获取用户输入，直接回车则使用默认值。"""
    user_input = input(f"{prompt_text} (默认: {default_value}): ").strip()
    return user_input if user_input else str(default_value)


def get_column_index(ws, col_name: str) -> int | None:
    """在表头第一行中查找列名，返回 1-based 列索引；未找到返回 None。"""
    for cell in ws[1]:
        if cell.value and str(cell.value).strip() == col_name:
            return cell.column
    return None


def get_last_index_value(ws, index_col: int) -> int:
    """获取 Index 列最后一行的值。无数据行返回 0。"""
    for row in range(ws.max_row, 1, -1):
        cell = ws.cell(row=row, column=index_col)
        if cell.value is not None:
            return cell.value
    return 0


# ==================== 核心操作 ====================


def move_files_from_excel(excel_path: Path, src_dir: Path, dst_dir: Path) -> None:
    """根据 Excel 中的'原文件名'列移动文件。"""
    if not excel_path.is_file():
        print(f"错误：Excel 文件不存在 -> {excel_path}")
        return
    if not src_dir.is_dir():
        print(f"错误：源文件夹不存在 -> {src_dir}")
        return
    dst_dir.mkdir(parents=True, exist_ok=True)

    wb = load_workbook(str(excel_path))
    ws = wb.active
    col = get_column_index(ws, "原文件名")
    if col is None:
        print("错误：Excel 中缺少'原文件名'列。")
        wb.close()
        return

    moved = 0
    for row in ws.iter_rows(min_row=2, values_only=False):
        name = row[col - 1].value
        if not name:
            continue
        name = str(name).strip()
        src_path = src_dir / name
        dst_path = dst_dir / name
        if not src_path.is_file():
            print(f"警告：未找到文件，跳过 -> {src_path}")
            continue
        if dst_path.exists():
            print(f"警告：目标已存在，跳过 -> {dst_path}")
            continue
        shutil.move(str(src_path), str(dst_path))
        print(f"已移动: {name}")
        moved += 1

    wb.close()
    print(f"移动完成，共处理 {moved} 个文件。")


def copy_files_from_excel(excel_path: Path, src_dir: Path, dst_dir: Path) -> None:
    """根据 Excel 中的'原文件名'列复制文件。"""
    if not excel_path.is_file():
        print(f"错误：Excel 文件不存在 -> {excel_path}")
        return
    if not src_dir.is_dir():
        print(f"错误：源文件夹不存在 -> {src_dir}")
        return
    dst_dir.mkdir(parents=True, exist_ok=True)

    wb = load_workbook(str(excel_path))
    ws = wb.active
    col = get_column_index(ws, "原文件名")
    if col is None:
        print("错误：Excel 中缺少'原文件名'列。")
        wb.close()
        return

    copied = 0
    for row in ws.iter_rows(min_row=2, values_only=False):
        name = row[col - 1].value
        if not name:
            continue
        name = str(name).strip()
        src_path = src_dir / name
        dst_path = dst_dir / name
        if not src_path.is_file():
            print(f"警告：未找到文件，跳过 -> {src_path}")
            continue
        if dst_path.exists():
            print(f"警告：目标已存在，跳过 -> {dst_path}")
            continue
        shutil.copy2(str(src_path), str(dst_path))
        print(f"已复制: {name}")
        copied += 1

    wb.close()
    print(f"复制完成，共处理 {copied} 个文件。")


def rename_files_from_excel(excel_path: Path, src_dir: Path) -> None:
    """根据 Excel 中的'原文件名'和'现文件名'列重命名文件。"""
    if not excel_path.is_file():
        print(f"错误：Excel 文件不存在 -> {excel_path}")
        return
    if not src_dir.is_dir():
        print(f"错误：源文件夹不存在 -> {src_dir}")
        return

    wb = load_workbook(str(excel_path))
    ws = wb.active
    col_old = get_column_index(ws, "原文件名")
    col_new = get_column_index(ws, "现文件名")
    if col_old is None or col_new is None:
        print("错误：Excel 中缺少'原文件名'或'现文件名'列。")
        wb.close()
        return

    renamed = 0
    for row in ws.iter_rows(min_row=2, values_only=False):
        old_name = row[col_old - 1].value
        new_name = row[col_new - 1].value
        if not old_name or not new_name:
            continue
        old_name = str(old_name).strip()
        new_name = str(new_name).strip()
        old_path = src_dir / old_name
        new_path = src_dir / new_name
        if not old_path.is_file():
            print(f"警告：未找到文件，跳过 -> {old_path}")
            continue
        if new_path.exists():
            print(f"警告：目标名称已存在，跳过 -> {new_path}")
            continue
        old_path.rename(new_path)
        print(f"重命名: {old_name} -> {new_name}")
        renamed += 1

    wb.close()
    print(f"重命名完成，共处理 {renamed} 个文件。")


def write_filenames_to_excel(excel_path: Path, src_dir: Path, include_subdirs: bool) -> None:
    """将源文件夹中的文件名追加写入 Excel。"""
    if not src_dir.is_dir():
        print(f"错误：源文件夹不存在 -> {src_dir}")
        return

    if not excel_path.is_file():
        print(f"Excel 文件不存在，将创建新文件并添加表头 -> {excel_path}")
        wb = Workbook()
        ws = wb.active
        ws.append(["Index", "名字", "原文件名"])
        wb.save(str(excel_path))
        wb.close()

    wb = load_workbook(str(excel_path))
    ws = wb.active
    max_col = ws.max_column

    col_index = get_column_index(ws, "Index")
    col_name = get_column_index(ws, "名字")
    col_orig = get_column_index(ws, "原文件名")
    if col_index is None or col_name is None or col_orig is None:
        print("错误：Excel 表头必须包含'Index'、'名字'、'原文件名'列。")
        wb.close()
        return

    last_index = get_last_index_value(ws, col_index)
    next_index = last_index + 1

    # 收集文件
    iterator = src_dir.rglob("*") if include_subdirs else src_dir.iterdir()
    file_paths = [p for p in iterator if p.is_file()]

    added = 0
    for f in file_paths:
        new_row = [""] * max_col
        new_row[col_index - 1] = next_index
        new_row[col_name - 1] = f.stem
        new_row[col_orig - 1] = f.name
        ws.append(new_row)
        added += 1
        next_index += 1

    wb.save(str(excel_path))
    wb.close()
    print(f"已追加 {added} 条记录到 Excel，保存至: {excel_path}")


def delete_records_from_excel(
    excel_path: Path, src_dir: Path, include_subdirs: bool, match_field: str = "原文件名",
) -> None:
    """删除 Excel 中匹配源文件夹文件名的行，报告未匹配文件。"""
    if not excel_path.is_file():
        print(f"错误：Excel 文件不存在 -> {excel_path}")
        return
    if not src_dir.is_dir():
        print(f"错误：源文件夹不存在 -> {src_dir}")
        return

    # 收集源文件夹文件名
    iterator = src_dir.rglob("*") if include_subdirs else src_dir.iterdir()
    src_names = {p.name for p in iterator if p.is_file()}

    wb = load_workbook(str(excel_path))
    ws = wb.active

    col_match = get_column_index(ws, match_field)
    if col_match is None:
        print(f"错误：Excel 中缺少'{match_field}'列。")
        wb.close()
        return

    header = [cell.value for cell in ws[1]]
    rows_to_keep = [header]
    excel_names: set[str] = set()
    deleted = 0
    total_rows = 0

    for row in ws.iter_rows(min_row=2, values_only=True):
        total_rows += 1
        val = row[col_match - 1] if col_match - 1 < len(row) else None
        val = str(val).strip() if val else ""
        if val:
            excel_names.add(val)
        if val in src_names:
            deleted += 1
            continue
        rows_to_keep.append(list(row))

    ws.delete_rows(1, ws.max_row)
    for row_data in rows_to_keep:
        ws.append(row_data)
    wb.save(str(excel_path))
    wb.close()

    missing = src_names - excel_names
    print(f"已删除 {deleted} 条匹配'{match_field}'的记录（共 {total_rows} 行数据）。")
    if missing:
        print(f"\n源文件夹中以下文件未在 Excel 的'{match_field}'列中出现（共 {len(missing)} 个）：")
        for f in sorted(missing):
            print(f"  - {f}")
    else:
        print(f"源文件夹中的所有文件均在 Excel 的'{match_field}'列中有对应记录。")


# ==================== 主程序 ====================


def main() -> None:
    while True:
        print("\n===== 文件管理工具（Excel 驱动）=====")
        print("1. 移动")
        print("2. 复制")
        print("3. 重命名")
        print("4. 记录写入")
        print("5. 记录删除")
        print("0. 退出")
        choice = input("请输入数字(0-5): ").strip()

        if choice == "0":
            print("程序已退出。")
            break

        elif choice == "1":
            print("\n--- 移动文件 ---")
            excel = Path(get_input_with_default("Excel 文件路径", str(DEFAULT_EXCEL_PATH)))
            src = Path(get_input_with_default("源文件夹路径", str(DEFAULT_SOURCE_DIR)))
            dst = Path(get_input_with_default("目标文件夹路径", str(DEFAULT_TARGET_DIR)))
            move_files_from_excel(excel, src, dst)

        elif choice == "2":
            print("\n--- 复制文件 ---")
            excel = Path(get_input_with_default("Excel 文件路径", str(DEFAULT_EXCEL_PATH)))
            src = Path(get_input_with_default("源文件夹路径", str(DEFAULT_SOURCE_DIR)))
            dst = Path(get_input_with_default("目标文件夹路径", str(DEFAULT_TARGET_DIR)))
            copy_files_from_excel(excel, src, dst)

        elif choice == "3":
            print("\n--- 重命名文件 ---")
            excel = Path(get_input_with_default("Excel 文件路径", str(DEFAULT_EXCEL_PATH)))
            src = Path(get_input_with_default("源文件夹路径", str(DEFAULT_SOURCE_DIR)))
            rename_files_from_excel(excel, src)

        elif choice == "4":
            print("\n--- 记录写入 ---")
            excel = Path(get_input_with_default("Excel 文件路径", str(DEFAULT_EXCEL_PATH)))
            src = Path(get_input_with_default("源文件夹路径", str(DEFAULT_SOURCE_DIR)))
            inc = get_input_with_default("是否包含子文件夹？(y/n)", "n").strip().lower() == "y"
            write_filenames_to_excel(excel, src, inc)

        elif choice == "5":
            print("\n--- 记录删除 ---")
            excel = Path(get_input_with_default("Excel 文件路径", str(DEFAULT_EXCEL_PATH)))
            src = Path(get_input_with_default("源文件夹路径", str(DEFAULT_SOURCE_DIR)))
            inc = get_input_with_default("是否包含子文件夹？(y/n)", "n").strip().lower() == "y"
            field = get_input_with_default("匹配的字段名（原文件名/现文件名）", "原文件名")
            if field not in ("原文件名", "现文件名"):
                print(f"警告：未知字段'{field}'，将使用默认的'原文件名'。")
                field = "原文件名"
            delete_records_from_excel(excel, src, inc, field)

        else:
            print("无效的选择，请输入 0-5 之间的数字。")

        input("\n按回车键继续...")


# ==================== 程序入口 ====================

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n用户中断程序，已退出。")
    except Exception as e:
        print(f"\n程序运行出错: {e}")
    finally:
        input("\n按回车键退出...")
