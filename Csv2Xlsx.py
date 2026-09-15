# 请帮我写个中文的 Python 脚本，批注也是中文：
# 将 CVS 与 xls 文件相互转换，避免单元格内多行数据错误与编码错误。
# 完成后进行循环。

# 导入模块
# python -m pip install openpyxl
import csv
import sys
from pathlib import Path

import openpyxl

# CSV 字段长度上限调大：某些 CSV 单元格（如长文本、多行内容）超过
# Python csv 默认的 131072 字节（128KB）会报 field larger than field limit。
# 这里放宽到 1GB，覆盖绝大多数场景。
csv.field_size_limit(1024 * 1024 * 1024)

# ==================== 全局配置 ====================

# --- 消息常量 ---
MSG_TITLE = "CSV ↔ XLSX 互转工具"
MSG_DESC = "解决 Excel 打开 UTF-8 CSV 乱码、多行单元格被截断等问题。"
MSG_SELECT_MODE = "请选择转换方向："
MSG_MODE_CSV_TO_XLSX = "1. CSV → XLSX（解决编码和多行问题）"
MSG_MODE_XLSX_TO_CSV = "2. XLSX → CSV（输出 UTF-8 BOM，Excel 可直接打开）"
MSG_ASK_FILE = "请输入文件路径（支持拖拽，直接回车退出）："
MSG_FILE_NOT_FOUND = "文件不存在：{}"
MSG_UNSUPPORTED_FORMAT = "不支持的文件格式，仅支持 .csv / .xlsx。"
MSG_CONVERTING = "正在转换: {}"
MSG_CSV_DETECTED_ENCODING = "  检测编码: {}"
MSG_CSV_ROWS = "  读取: {} 行"
MSG_OUTPUT_WRITTEN = "  输出: {}"
MSG_XLSX_SHEETS = "  工作表: {}"
MSG_XLSX_ROWS = "  读取: {} 行（工作表: {}）"
MSG_DONE = "✅ 转换完成！"
MSG_INTERRUPTED = "\n\n用户中断程序，已退出。"
MSG_ERROR = "\n程序运行出错: {}"
MSG_EXIT = "\n按回车键退出..."

# ==================== 编码检测 ====================
def detect_encoding(file_path: Path) -> str:
    """检测 CSV 文件编码。先用 BOM 判断，再试常见编码。"""
    with open(file_path, "rb") as f:
        raw = f.read(4)

        # BOM 检测
        if raw[:3] == b"\xef\xbb\xbf":
            return "utf-8-sig"
        if raw[:2] == b"\xff\xfe":
            return "utf-16-le"
        if raw[:2] == b"\xfe\xff":
            return "utf-16-be"

        # 无 BOM，读取更多内容尝试解码
        rest = f.read(65536)
    sample = raw + rest

    encodings = ["utf-8", "gbk", "gb2312", "gb18030"]
    for enc in encodings:
        try:
            sample.decode(enc)
            return enc
        except (UnicodeDecodeError, LookupError):
            continue
    return "utf-8"  # 兜底，csv_to_xlsx 中以 errors="replace" 打开防止崩溃

# ==================== CSV → XLSX ====================
# Excel 单元格字符数硬上限为 32767，超长内容直接写入会导致 openpyxl
# 报错或生成的 xlsx 损坏。这里截断并追加标记，保证转换不失败。
EXCEL_CELL_LIMIT = 32767
TRUNC_MARK = " ...[已截断]"

def truncate_cell(value) -> str:
    """截断超过 Excel 上限的单元格内容。"""
    if len(value) > EXCEL_CELL_LIMIT:
        keep = EXCEL_CELL_LIMIT - len(TRUNC_MARK)
        return value[:keep] + TRUNC_MARK
    return value

def csv_to_xlsx(csv_path: Path) -> Path:
    """CSV 文件转 XLSX，处理 UTF-8 编码和多行单元格。"""
    encoding = detect_encoding(csv_path)
    print(MSG_CSV_DETECTED_ENCODING.format(encoding))

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = csv_path.stem[:31]  # Excel 工作表名最长 31 字符

    row_count = 0
    trunc_count = 0
    # errors="replace" 防止编码检测兜底时 UnicodeDecodeError 崩溃
    with open(csv_path, "r", encoding=encoding, errors="replace", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            row_count += 1
            safe_row = [truncate_cell(cell) for cell in row]
            if any(len(cell) > EXCEL_CELL_LIMIT for cell in row):
                trunc_count += 1
            ws.append(safe_row)

    print(MSG_CSV_ROWS.format(row_count))
    if trunc_count:
        print(f"  警告: {trunc_count} 行含超长单元格(>32767字符), 已截断")

    output_path = csv_path.with_suffix(".xlsx")
    wb.save(output_path)
    wb.close()
    return output_path

# ==================== XLSX → CSV ====================
def xlsx_to_csv(xlsx_path: Path) -> Path:
    """XLSX 文件转 UTF-8 BOM CSV，Excel 可直接打开。"""
    wb = openpyxl.load_workbook(xlsx_path, data_only=True)
    sheet_names = wb.sheetnames

    if len(sheet_names) == 1:
        sheet_name = sheet_names[0]
        ws = wb[sheet_name]
    else:
        # 多工作表：让用户选择
        print(MSG_XLSX_SHEETS.format(", ".join(sheet_names)))
        while True:
            choice = input(
                f"请选择工作表（1-{len(sheet_names)}，默认1）："
            ).strip()
            if choice == "":
                sheet_name = sheet_names[0]
                break
            if choice.isdigit() and 1 <= int(choice) <= len(sheet_names):
                sheet_name = sheet_names[int(choice) - 1]
                break
            print("输入错误，请重新输入。")
        ws = wb[sheet_name]

    row_count = 0
    output_path = xlsx_path.with_suffix(".csv")

    with open(output_path, "w", encoding="utf-8-sig", newline="") as f:
        # utf-8-sig 自动写入 UTF-8 BOM
        writer = csv.writer(f, lineterminator="\n")
        for row in ws.iter_rows(values_only=True):
            # 空单元格 → 空字符串，否则输出 "None" 文本
            safe_row = ["" if cell is None else cell for cell in row]
            writer.writerow(safe_row)
            row_count += 1

    print(MSG_XLSX_ROWS.format(row_count, sheet_name))
    wb.close()
    return output_path

# ==================== 主程序 ====================
def main() -> None:
    print("=" * 50)
    print(MSG_TITLE)
    print("=" * 50)
    print()
    print(MSG_DESC)
    print()
    print(MSG_SELECT_MODE)
    print(f"  {MSG_MODE_CSV_TO_XLSX}")
    print(f"  {MSG_MODE_XLSX_TO_CSV}")
    print()

    choice = ""
    while True:
        raw = input("请输入 (1/2，默认1)：").strip()
        if raw in ("", "1", "2"):
            choice = raw
            break
        print("输入错误，请重新输入。")

    # 持续循环转换
    while True:
        print()
        file_path_str = input(MSG_ASK_FILE).strip().strip("\"'")
        if not file_path_str:
            print("已退出。")
            break

        file_path = Path(file_path_str)
        if not file_path.is_file():
            print(MSG_FILE_NOT_FOUND.format(file_path))
            continue

        suffix = file_path.suffix.lower()
        if suffix == ".csv" and choice in ("", "1"):
            print(MSG_CONVERTING.format(file_path.name))
            output = csv_to_xlsx(file_path)
        elif suffix == ".xlsx" and choice == "2":
            print(MSG_CONVERTING.format(file_path.name))
            output = xlsx_to_csv(file_path)
        elif suffix == ".csv" and choice == "2":
            print(MSG_CONVERTING.format(file_path.name))
            output = csv_to_xlsx(file_path)
        elif suffix == ".xlsx" and choice in ("", "1"):
            print(MSG_CONVERTING.format(file_path.name))
            output = xlsx_to_csv(file_path)
        else:
            print(MSG_UNSUPPORTED_FORMAT)
            continue

        print(MSG_OUTPUT_WRITTEN.format(output))
        print(MSG_DONE)

# ==================== 程序入口 ====================
if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (OSError, AttributeError):
        pass
    try:
        main()
    except KeyboardInterrupt:
        print(MSG_INTERRUPTED)
    except Exception as e:
        print(MSG_ERROR.format(e))
    finally:
        input(MSG_EXIT)
