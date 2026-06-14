# 请帮我写个中文的 Python 脚本，批注也是中文：
# 询问我想要做什么：
# 1. 根据文件夹生成 excel 文件：在脚本开始前询问我源文件夹位置（默认为：d:\Studios\Attachments\Android\）。在其父文件夹中生成同名 xlsx 格式文件。第一行为字段名。第二行开始为数据内容，依次读取源文件夹位置内每一个 markdown 文件（markdown 格式文件，数据以 yaml 属性格式呈现如上文），将 markdown 中"---"包绕的属性根据每一字段名写入 xlsx 格式文件。写入 xlsx 文件中，每一行对应一个文件。
# 2. 根据 excel 文件生成相应 markdown 文件：在脚本开始前询问我源 xlsx 文件位置（默认为：d:\Studios\Attachments\Android\标准.xlsx）。在其父文件夹中生成同名文件夹。将字段名字设置为 markdown 文件名。每一行生成一个文件，并依次写入相应的 yaml 属性呈现如上文，在 markdown 中用"---"包绕。
# 3. CSV 生成文件：在脚本开始前询问我源 CSV 文件位置（默认为：d:\Downloads\CSV.csv）与目标文件夹位置（默认为：d:\Studios\Attachments\Android\）。这个 CSV 格式，第一行为所有字段名，字段名用""包绕。不同字段名之间用,隔开。第二行开始每一以"开头的为每一条记录。每一个""包绕的为相应的字段数据（可包含数行）为每一条字段。独立的一条记录和字段内多行区别在于行首有无"。每一记录内字段名与字段内容一一对应。请生成每一条记录（markdown 格式 文件，数据以 yaml 属性格式呈现如上文，markdown 文件名为字段"名字"对应字段内容，）。在目标文件夹下生成子文件夹，子文件夹名为CSV格式的文件名（不包括后缀名），将生成的记录放在该子文件夹下。生成的文件名为字段"名字"对应字段内容，当字段"名字"对应字段内容出现不能成为文件名的内容如半角冒号":"，请用空格破折号空格" -"代替。其他的如半角问号"?"、半角反斜杠"\"、正斜杠"/"，用全角问号"？"、全角反斜杠"＼"、正斜杠"／"代替。半角双引号"""用半角波浪号"~"代替。竖线"|"用反单引号"`"代替。星号"*"用乘号"×"代替。<（小于）、>（大于）用书名号"《 》"代替。
# 4. 删除字段：在脚本开始前询问我源文件夹位置，文件夹内储存着上述结构的数据（默认为：d:\Studios\Attachments\Android\）。询问我需要删除某一字段名。遍历源文件夹位置中所有的文件及子文件夹内文件（md 格式），读取每一文件，找到这个字段后删除该字段即其配套的字段内容。
# 5. 添加字段：在脚本开始前询问我源文件夹位置，文件夹内储存着上述结构的数据（默认为：d:\Studios\Attachments\Android\）。询问我需要添加某一字段名，及添加在哪一个字段前。遍历源文件夹位置中所有的文件及子文件夹内文件（md 格式），读取每一文件，找到这个字段，在这行之前，添加要求的字段。
# 6. 查找与替换：在脚本开始前询问我源文件夹位置，文件夹内储存着上述结构的数据（默认为：d:\Studios\Attachments\Android\）。依次在屏幕中询问我查找内容及替换内容。遍历源文件夹位置中所有的文件及子文件夹内文件（md 格式），读取每一文件，找到存放查找内容，用替换内容进行替换。
# 7. 查找与替换（正则表达式）：在脚本开始前询问我源文件夹位置，文件夹内储存着上述结构的数据（默认为：d:\Studios\Attachments\Android\）。询问我存放查找内容的正则表达式文本位置（默认为：e:\Documents\Softwares\Codes\Python\RegexFind.txt）与存放替换内容的文本位置（默认为：e:\Documents\Softwares\Codes\Python\RegexReplace.txt）。遍历源文件夹位置中所有的文件及子文件夹内文件（md 格式），读取每一文件，找到存放查找内容，用替换内容进行替换。
# 8. 元替换：在脚本开始前询问我源文件夹位置，文件夹内储存着上述结构的数据（默认为：d:\Studios\Attachments\Android\）。遍历源文件夹位置中所有的文件及子文件夹内文件（md 格式），读取每一文件，将文件里的元数据标实替换 md 文件的元数据。（比如[FileName]表示全文件名，[BaseName]表示不含扩展名的文件名，[Extension]表示扩展名，[FolderName]表示父文件夹名，[FolderPath]表示父文件夹路径，[FilePath]表示文件路径，[DateCreated]表示文件生成日期时间，[DateModified]表示文件修改日期时间，[DateAccessed]表示文件修改时间，[Size]表示文件大小（适配 B、KB、MB、GB 形式，并精确到小数点后 4 位），[SizeBytes]表示文件大小（Bytes）。
# 9. 生成数据结构文件：在脚本开始前询问我源文件夹位置，文件夹内储存着上述结构的数据（默认为：d:\Studios\Attachments\Android\）。在该文件夹下生成一个 md 文件，文件名为".DatabaseStructure.md"。读取该文件夹中的其他每一文件（排除 ".DatabaseStructure.md"），将第一个文件里每一个的字段名，依次写入".DatabaseStructure.md"中。字段名后接一个半角冒号和空格（": "），在此之后，写着这个字段的字段类型（文本、数值、布尔、日期、时间、日期时间、列表），每一行一个字段。这些字段名首尾由一组三个破折号（"---"）分隔符包围。此后依次读取每一个文件，如文件里的字段名已经被".DatabaseStructure.md"记录，则不做处理；如文件里的字段名未被".DatabaseStructure.md"记录，则添加该字段。
# 10. 结构化数据文件：在脚本开始前询问我源文件夹位置，文件夹内储存着上述结构的数据（默认为：d:\Studios\Attachments\Android\）。读取该文件夹下的".DatabaseStructure.md"。这个就是后续文件的字段的数据结构。依次读取该文件夹中的其他每一文件（排除 ".DatabaseStructure.md"），将它的字段按照".DatabaseStructure.md"中字段名顺序重新排序；如果".DatabaseStructure.md"里的某一字段名有，而该文件中没有，就按顺序添加到该文件中；如果该文件有，而".DatabaseStructure.md"里没有的字段名，就删除该字段及其数据。
# 11. 删除没有数据的字段名：在脚本开始前询问我源文件夹位置，文件夹内储存着上述结构的数据（默认为：d:\Studios\Attachments\Android\）。依次读取该文件夹中的其他每一文件（排除 ".DatabaseStructure.md"）。删除没有数据的字段行。
# 12. 双引号置换单引号：在脚本开始前询问我源文件夹位置，文件夹内储存着上述结构的数据（默认为：d:\Studios\Attachments\Android\）。打开每个 markdown 文件，顺序读取文件，将每一行中除了第一个和倒数第一个双引号（"），其他的双引号改为单引号（'）。
# 13. 属性内容处理：在脚本开始前询问我源文件夹位置，文件夹内储存着上述结构的数据（默认为：d:\Studios\Attachments\Android\），再询问我属性名称。打开每个 markdown 文件，顺序找到该属性。询问我下一步：1.将该属性内容设置为空（""）。2.将该属性内容设置为什么？（询问我属性内容，所有 markdown 文件的属性均设置为该属性内容）。3. 将该属性内容每个单词大写。4.将该属性内容每个单词小写。5. 将该属性内容每个单词首字母大写，其余小写。6.将该属性内容（汉字、英文、或数字）用空格隔开。7.将该属性内容的汉字繁体中文转为简体中文。8. 所有半角标点符号转为全角标点符号。
# 0. 退出程序。
# 完成后，反复循环我要做什么。

import csv
import datetime
import re
import subprocess
import sys
import time
import urllib.parse
from collections import OrderedDict
from pathlib import Path

import pandas as pd
import yaml

# 尝试导入 zhconv 用于简繁转换
try:
    import zhconv
    ZHCONV_AVAILABLE = True
except ImportError:
    ZHCONV_AVAILABLE = False


# =========================
# 工具函数
# =========================

def sanitize_filename(name: str) -> str:
    """净化文件名中的特殊字符。"""
    replacements = {
        ":": " -",
        "?": "？",
        "\\": "＼",
        "/": "／",
        '"': "~",
        "|": "`",
        "*": "×",
        "<": "《",
        ">": "》",
    }
    for char, replacement in replacements.items():
        name = name.replace(char, replacement)
    return name.strip()


def get_default_path(prompt: str, default: str) -> str:
    """获取带默认值的路径输入。"""
    path = input(f"{prompt} (默认：{default}): ").strip()
    return path if path else default


def escape_yaml_value(value) -> str:
    """转义 YAML 值——所有值都用双引号包绕。"""
    if value is None:
        return '""'
    return f'"{value!s}"'


def extract_yaml_block(content: str) -> str:
    """从文件内容中提取 YAML 块（--- 包绕部分）。"""
    match = re.search(r"^---\n(.*?)\n---", content, flags=re.DOTALL)
    return match.group(1) if match else ""


def infer_field_type(value) -> str:
    """根据字段值推断字段类型。"""
    if value is None:
        return "文本"
    if isinstance(value, bool):
        return "布尔"
    if isinstance(value, (int, float)):
        return "数值"
    if isinstance(value, list):
        return "列表"
    if isinstance(value, datetime.datetime):
        return "日期时间"
    if isinstance(value, datetime.date):
        return "日期"
    if isinstance(value, datetime.time):
        return "时间"
    if isinstance(value, str):
        try:
            datetime.datetime.fromisoformat(value)
            return "日期时间"
        except ValueError:
            pass
        try:
            datetime.date.fromisoformat(value)
            return "日期"
        except ValueError:
            pass
        try:
            datetime.time.fromisoformat(value)
            return "时间"
        except ValueError:
            pass
        if value.lower() in ("true", "false"):
            return "布尔"
        if re.match(r"^[-+]?\d+$", value):
            return "数值"
        if re.match(r"^[-+]?\d*\.\d+$", value):
            return "数值"
    return "文本"


def format_file_size(size_bytes: int) -> str:
    """格式化文件大小为 B / KB / MB / GB（4 位小数）。"""
    units = ["B", "KB", "MB", "GB"]
    unit_index = 0
    size = float(size_bytes)
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024.0
        unit_index += 1
    if unit_index == 0:
        return f"{size_bytes} B"
    return f"{size:.4f} {units[unit_index]}"


# =========================
# 选项 1：根据文件夹生成 Excel 文件
# =========================

def generate_excel_from_folder() -> None:
    """从文件夹生成 Excel 文件——增量更新模式。"""
    source_dir = Path(get_default_path("请输入源文件夹位置", r"d:\Studios\Attachments\Android"))
    if not source_dir.is_dir():
        print(f"错误：文件夹 '{source_dir}' 不存在")
        return

    output_path = source_dir.parent / f"{source_dir.name}.xlsx"
    print(f"Excel 文件位置: {output_path}")

    all_records = []
    field_order = OrderedDict()

    for filepath in sorted(source_dir.rglob("*.md")):
        record, fields_in_file = parse_markdown_yaml(filepath)
        if not record:
            continue

        processed_name = filepath.stem.replace(" - ", ": ")
        record["名字"] = processed_name
        record["文件名"] = filepath.name

        for field in fields_in_file:
            if field not in field_order:
                field_order[field] = True
        if "名字" not in field_order:
            field_order["名字"] = True
        if "文件名" not in field_order:
            field_order["文件名"] = True

        all_records.append(record)

    if not all_records:
        print("未找到任何 Markdown 文件或解析失败")
        return

    field_list = list(field_order.keys())
    data = []
    for record in all_records:
        row = []
        for field in field_list:
            value = record.get(field, "")
            if isinstance(value, (list, tuple)):
                value = ", ".join(str(item) for item in value)
            else:
                value = str(value) if value is not None else ""
            row.append(value)
        data.append(row)

    new_df = pd.DataFrame(data, columns=field_list)

    if output_path.is_file():
        try:
            existing_df = pd.read_excel(output_path, engine="openpyxl")
            if "名字" in existing_df.columns and "名字" in new_df.columns:
                final_df = existing_df.copy()
                for _, row in new_df.iterrows():
                    name = row["名字"]
                    if name in final_df["名字"].values:
                        mask = final_df["名字"] == name
                        for col in new_df.columns:
                            if col != "名字":
                                final_df.loc[mask, col] = row[col]
                    else:
                        final_df = pd.concat([final_df, pd.DataFrame([row])], ignore_index=True)
                for col in [c for c in new_df.columns if c not in existing_df.columns]:
                    final_df[col] = new_df[col]
                df = final_df
                print("已增量更新现有 Excel 文件")
            else:
                df = new_df
                print("无法找到'名字'字段，将创建新 Excel 文件")
        except Exception as e:
            print(f"读取现有 Excel 文件失败: {e}，将创建新 Excel 文件")
            df = new_df
    else:
        df = new_df
        print("将创建新 Excel 文件")

    try:
        df.to_excel(output_path, index=False, engine="openpyxl")
        print(f"成功导出 {len(df)} 条记录到: {output_path}")
        print(f"包含字段 ({len(df.columns)} 个): {', '.join(df.columns)}")
    except Exception as e:
        print(f"导出 Excel 失败: {e}")
        csv_path = output_path.with_suffix(".csv")
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")
        print(f"已备选导出为 CSV: {csv_path}")


def parse_markdown_yaml(filepath: Path):
    """解析 Markdown 文件中的 YAML 属性块，返回 (数据字典, 字段顺序列表)。"""
    try:
        content = filepath.read_text(encoding="utf-8")
        yaml_pattern = r"^---\s*\n(.*?)\n---\s*$"
        match = re.search(yaml_pattern, content, re.DOTALL | re.MULTILINE)
        if not match:
            print(f"警告：文件 {filepath} 中未找到 YAML 属性块")
            return None, []

        yaml_content = match.group(1)
        try:
            data = yaml.safe_load(yaml_content)
            if data:
                for key, value in data.items():
                    if isinstance(value, (list, tuple)):
                        data[key] = ", ".join(str(item) for item in value)
                    else:
                        data[key] = str(value) if value is not None else ""

            if data:
                field_order = []
                for line in yaml_content.strip().split("\n"):
                    line = line.strip()
                    if line and ":" in line and not line.startswith("#"):
                        field_name = line.split(":", 1)[0].strip()
                        if field_name in data:
                            field_order.append(field_name)
                return data, field_order
            return None, []
        except yaml.YAMLError as e:
            print(f"解析 YAML 失败 {filepath}: {e}")
            return None, []
    except Exception as e:
        print(f"读取文件失败 {filepath}: {e}")
        return None, []


# =========================
# 选项 2：根据 Excel 生成 Markdown 文件夹
# =========================

def generate_markdown_from_excel() -> None:
    """从 Excel 生成 Markdown 文件夹——增量更新模式。"""
    excel_path = Path(get_default_path("请输入 Excel 文件路径", r"d:\Studios\Attachments\Android\标准.xlsx"))
    if not excel_path.is_file():
        print(f"错误：Excel 文件 '{excel_path}' 不存在")
        return

    output_dir = excel_path.parent / excel_path.stem
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"将在以下位置生成/更新 Markdown 文件: {output_dir}")

    try:
        df = pd.read_excel(excel_path, engine="openpyxl")
    except Exception as e:
        print(f"读取 Excel 文件失败: {e}")
        return

    if df.empty:
        print("Excel 文件为空")
        return

    field_names = df.columns.tolist()
    if "名字" not in field_names:
        print("错误：Excel 文件中缺少'名字'字段，无法生成 Markdown 文件")
        return

    success_count = 0
    update_count = 0
    for _, row in df.iterrows():
        name_value = row.get("名字", "")
        if not name_value or pd.isna(name_value):
            print(f"跳过：'名字'字段为空")
            continue

        processed_name = name_value.replace(": ", " - ")
        filename = sanitize_filename(processed_name) + ".md"
        filepath = output_dir / filename

        yaml_data = OrderedDict()
        for field in field_names:
            value = row.get(field, "")
            if pd.isna(value) or value == "":
                yaml_data[field] = [""]
            elif isinstance(value, str) and ", " in value:
                values = [v.strip() for v in value.split(", ") if v.strip()]
                yaml_data[field] = values
            else:
                yaml_data[field] = [str(value)]

        if filepath.is_file():
            try:
                content = filepath.read_text(encoding="utf-8")
                match = re.search(r"(^---\n.*?\n---)(.*)", content, flags=re.DOTALL)
                if match:
                    existing_data = yaml.safe_load(extract_yaml_block(match.group(1)))
                    if existing_data:
                        standardized = OrderedDict()
                        for fld, val in existing_data.items():
                            standardized[fld] = val if isinstance(val, list) else [str(val)]
                        for fld, val in yaml_data.items():
                            standardized[fld] = val
                        yaml_data = standardized
                    update_count += 1
            except Exception as e:
                print(f"读取现有文件失败 {filename}: {e}")

        try:
            with filepath.open("w", encoding="utf-8") as f:
                f.write("---\n")
                for field, value_list in yaml_data.items():
                    f.write(f"{field}:\n")
                    for item in value_list:
                        f.write(f"  - {escape_yaml_value(item)}\n")
                f.write("---\n")
            success_count += 1
            label = "已更新" if update_count > 0 and filepath.is_file() else "已生成"
            print(f"{label}: {filename}")
        except Exception as e:
            print(f"生成文件失败 {filename}: {e}")

    print(f"成功处理 {success_count} 个 Markdown 文件到: {output_dir}")
    if update_count > 0:
        print(f"其中 {update_count} 个文件已更新")


# =========================
# 选项 3：从 CSV 生成 Markdown 文件
# =========================

def generate_from_csv() -> None:
    """从 CSV 生成 Markdown 文件——所有字段内容用双引号包绕并使用列表格式。"""
    csv_path = Path(input(r"请输入 CSV 文件路径（默认：d:\Studios\Attachments\Android\CSV.csv）：") or r"d:\Studios\Attachments\Android\CSV.csv")
    output_dir = Path(input(r"请输入目标文件夹（默认：d:\Studios\Attachments\Android\）：") or r"d:\Studios\Attachments\Android")

    output_subdir = output_dir / csv_path.stem
    output_subdir.mkdir(parents=True, exist_ok=True)

    try:
        with csv_path.open("r", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=",", quotechar='"')
            headers = next(reader)

            for row_idx, row in enumerate(reader, 1):
                try:
                    yaml_lines = ["---"]
                    for header, value in zip(headers, row):
                        yaml_lines.append(f"{header}:")
                        if not value.strip():
                            yaml_lines.append('  - ""')
                        else:
                            for line in value.split("\n"):
                                yaml_lines.append(f'  - "{line}"')
                    yaml_lines.append("---\n")

                    name_field = next((v for h, v in zip(headers, row) if h == "名字"), None)
                    if not name_field:
                        raise ValueError("CSV 中缺少'名字'字段")

                    safe_name = sanitize_filename(name_field)
                    if not safe_name:
                        raise ValueError("文件名经净化后为空")

                    (output_subdir / f"{safe_name}.md").write_text(
                        "\n".join(yaml_lines), encoding="utf-8"
                    )
                    print(f"已生成：{output_subdir / safe_name}.md")
                except Exception as e:
                    print(f"处理第 {row_idx} 行时出错：{e}")
        print("\nCSV 转换完成！")
    except Exception as e:
        print(f"处理 CSV 文件时出错：{e}")


# =========================
# 选项 4：删除字段
# =========================

def delete_field() -> None:
    """删除指定字段。"""
    source_dir = Path(input(r"请输入源文件夹（默认：d:\Studios\Attachments\Android\）：") or r"d:\Studios\Attachments\Android")
    field_name = input("请输入要删除的字段名称：")

    processed_count = 0
    for file_path in source_dir.rglob("*.md"):
        if process_delete_field(file_path, field_name):
            processed_count += 1
    print(f"\n字段删除完成！共处理 {processed_count} 个文件")


def process_delete_field(file_path: Path, field_name: str) -> bool:
    """处理单个文件的字段删除。"""
    try:
        content = file_path.read_text(encoding="utf-8")
        pattern = re.compile(
            r"^(" + re.escape(field_name) + r":.*?)(?=^\S|\Z)",
            flags=re.DOTALL | re.MULTILINE,
        )
        new_content = pattern.sub("", content)
        new_content = re.sub(r"\n\s*\n", "\n", new_content)

        if new_content != content:
            file_path.write_text(new_content, encoding="utf-8")
            print(f"已处理：{file_path}")
            return True
        return False
    except Exception as e:
        print(f"处理文件 {file_path} 时出错：{e}")
        return False


# =========================
# 选项 5：添加字段
# =========================

def add_field() -> None:
    """添加新字段。"""
    source_dir = Path(input(r"请输入源文件夹（默认：d:\Studios\Attachments\Android\）：") or r"d:\Studios\Attachments\Android")
    new_field = input("请输入要添加的字段名称：")
    target_field = input("请输入要插入在哪个字段之前：")

    processed_count = 0
    for file_path in source_dir.rglob("*.md"):
        if process_add_field(file_path, new_field, target_field):
            processed_count += 1
    print(f"\n字段添加完成！共处理 {processed_count} 个文件")


def process_add_field(file_path: Path, new_field: str, target_field: str) -> bool:
    """处理单个文件的字段添加。"""
    try:
        lines = file_path.read_text(encoding="utf-8").splitlines(keepends=True)
        try:
            yaml_start = lines.index("---\n")
            yaml_end = lines.index("---\n", yaml_start + 1)
        except ValueError:
            print(f"文件 {file_path} 缺少 YAML 分隔符，跳过处理")
            return False

        insert_pos = -1
        for i in range(yaml_start + 1, yaml_end):
            if lines[i].startswith(f"{target_field}:"):
                insert_pos = i
                break

        if insert_pos == -1:
            print(f"在 {file_path} 中未找到目标字段 {target_field}")
            return False

        lines.insert(insert_pos, f"{new_field}: \n")
        file_path.write_text("".join(lines), encoding="utf-8")
        print(f"已更新：{file_path}")
        return True
    except Exception as e:
        print(f"处理文件 {file_path} 时出错：{e}")
        return False


# =========================
# 选项 6：查找与替换（普通）
# =========================

def find_and_replace() -> None:
    """查找与替换功能（普通）。"""
    source_dir = Path(input(r"请输入源文件夹（默认：d:\Studios\Attachments\Android\）：") or r"d:\Studios\Attachments\Android")
    find_content = input("请输入要查找的内容：")
    replace_content = input("请输入要替换的内容：")

    if not find_content.strip():
        print("查找内容为空，操作取消")
        return

    print(f"将在文件夹 {source_dir} 中查找 '{find_content}' 并替换为 '{replace_content}'")
    confirm = input("确认执行替换操作？(y/N): ")
    if confirm.lower() != "y":
        print("操作已取消")
        return

    processed_count = 0
    for file_path in source_dir.rglob("*.md"):
        if process_find_replace(file_path, find_content, replace_content):
            processed_count += 1
    print(f"\n查找与替换完成！共处理 {processed_count} 个文件")


def process_find_replace(file_path: Path, find_content: str, replace_content: str) -> bool:
    """处理单个文件的查找与替换（普通）。"""
    try:
        content = file_path.read_text(encoding="utf-8")
        new_content = content.replace(find_content, replace_content)
        if new_content == content:
            return False
        file_path.write_text(new_content, encoding="utf-8")
        print(f"已更新：{file_path}")
        return True
    except Exception as e:
        print(f"处理文件 {file_path} 时出错：{e}")
        return False


# =========================
# 选项 7：查找与替换（正则表达式）
# =========================

def find_and_replace_regex() -> None:
    """查找与替换功能（正则表达式）。"""
    source_dir = Path(input(r"请输入源文件夹（默认：d:\Studios\Attachments\Android\）：") or r"d:\Studios\Attachments\Android")
    find_file = Path(input(
        r"请输入查找正则表达式文件位置（默认：e:\Documents\Softwares\Codes\Python\RegexFind.txt）："
    ) or r"e:\Documents\Softwares\Codes\Python\RegexFind.txt")
    replace_file = Path(input(
        r"请输入替换内容文件位置（默认：e:\Documents\Softwares\Codes\Python\RegexReplace.txt）："
    ) or r"e:\Documents\Softwares\Codes\Python\RegexReplace.txt")

    try:
        find_pattern = find_file.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        print(f"查找正则表达式文件不存在：{find_file}")
        return

    try:
        replace_content = replace_file.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"替换内容文件不存在：{replace_file}")
        return

    try:
        regex = re.compile(find_pattern, flags=re.MULTILINE)
    except re.error as e:
        print(f"正则表达式错误：{e}")
        return

    processed_count = 0
    for file_path in source_dir.rglob("*.md"):
        if process_regex_replace(file_path, regex, replace_content):
            processed_count += 1
    print(f"\n正则表达式查找与替换完成！共处理 {processed_count} 个文件")


def process_regex_replace(file_path: Path, regex: re.Pattern, replace_content: str) -> bool:
    """处理单个文件的正则表达式查找与替换。"""
    try:
        content = file_path.read_text(encoding="utf-8")
        new_content = regex.sub(replace_content, content)
        if new_content == content:
            return False
        file_path.write_text(new_content, encoding="utf-8")
        print(f"已更新：{file_path}")
        return True
    except Exception as e:
        print(f"处理文件 {file_path} 时出错：{e}")
        return False


# =========================
# 选项 8：元替换
# =========================

def meta_replacement() -> None:
    """元替换功能。"""
    source_dir = Path(input(r"请输入源文件夹（默认：d:\Studios\Attachments\Android\）：") or r"d:\Studios\Attachments\Android")

    processed_count = 0
    for file_path in source_dir.rglob("*.md"):
        if process_meta_replacement(file_path):
            processed_count += 1
    print(f"\n元替换完成！共处理 {processed_count} 个文件")


def process_meta_replacement(file_path: Path) -> bool:
    """处理单个文件的元替换。"""
    try:
        stat = file_path.stat()
        created_time = datetime.datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S")
        modified_time = datetime.datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        accessed_time = datetime.datetime.fromtimestamp(stat.st_atime).strftime("%Y-%m-%d %H:%M:%S")
        size_formatted = format_file_size(stat.st_size)

        parent = file_path.parent
        replacements = {
            "[FileName]": file_path.name,
            "[BaseName]": file_path.stem,
            "[Extension]": file_path.suffix[1:] if file_path.suffix else "",
            "[FolderName]": parent.name,
            "[FolderPath]": str(parent),
            "[FilePath]": str(file_path),
            "[DateCreated]": created_time,
            "[DateModified]": modified_time,
            "[DateAccessed]": accessed_time,
            "[Size]": size_formatted,
            "[SizeBytes]": str(stat.st_size),
        }

        content = file_path.read_text(encoding="utf-8")
        new_content = content
        for pattern, replacement in replacements.items():
            new_content = new_content.replace(pattern, replacement)

        if new_content == content:
            return False

        file_path.write_text(new_content, encoding="utf-8")
        print(f"已更新：{file_path}")
        return True
    except Exception as e:
        print(f"处理文件 {file_path} 时出错：{e}")
        return False


# =========================
# 选项 9：生成数据结构文件
# =========================

def generate_structure_file() -> None:
    """生成数据结构文件。"""
    source_dir = Path(input(r"请输入源文件夹（默认：d:\Studios\Attachments\Android\）：") or r"d:\Studios\Attachments\Android")
    output_file = source_dir / ".DatabaseStructure.md"

    field_types: dict[str, str] = {}
    field_order: list[str] = []
    processed_files = 0

    for file_path in source_dir.rglob("*.md"):
        if file_path.name == ".DatabaseStructure.md":
            continue

        try:
            content = file_path.read_text(encoding="utf-8")
            yaml_block = extract_yaml_block(content)
            if not yaml_block:
                print(f"跳过：{file_path}（未找到 YAML 块）")
                continue

            try:
                data = yaml.safe_load(yaml_block)
            except Exception as e:
                print(f"解析 YAML 失败：{file_path} - {e}")
                continue

            for field, value in data.items():
                if field not in field_types:
                    field_types[field] = infer_field_type(value)
                    field_order.append(field)
                    processed_files += 1
        except Exception as e:
            print(f"处理文件 {file_path} 时出错：{e}")

    try:
        with output_file.open("w", encoding="utf-8") as f:
            f.write("---\n")
            for field in field_order:
                f.write(f"{field}: {field_types[field]}\n")
            f.write("---\n")
        print(f"\n数据结构文件已生成：{output_file}")
        print(f"共处理 {processed_files} 个文件，发现 {len(field_order)} 个唯一字段")
    except Exception as e:
        print(f"写入数据结构文件时出错：{e}")


# =========================
# 选项 10：结构化数据文件
# =========================

def restructure_files() -> None:
    """根据数据结构文件重新组织数据文件。"""
    source_dir = Path(input(r"请输入源文件夹（默认：d:\Studios\Attachments\Android\）：") or r"d:\Studios\Attachments\Android")
    structure_file = source_dir / ".DatabaseStructure.md"

    try:
        content = structure_file.read_text(encoding="utf-8")
        yaml_block = extract_yaml_block(content)
        if not yaml_block:
            print(f"数据结构文件格式错误：{structure_file}")
            return

        structure_data = yaml.safe_load(yaml_block)
        if not structure_data:
            print(f"数据结构文件内容为空：{structure_file}")
            return

        field_order = list(structure_data.keys())
    except Exception as e:
        print(f"读取数据结构文件时出错：{e}")
        return

    processed_count = 0
    for file_path in source_dir.rglob("*.md"):
        if file_path.name == ".DatabaseStructure.md":
            continue
        if process_restructure_file(file_path, field_order):
            processed_count += 1
    print(f"\n文件结构化完成！共处理 {processed_count} 个文件")


def process_restructure_file(file_path: Path, field_order: list[str]) -> bool:
    """处理单个文件的结构化。"""
    try:
        content = file_path.read_text(encoding="utf-8")
        match = re.search(r"(^---\n.*?\n---)(.*)", content, flags=re.DOTALL)
        if not match:
            print(f"跳过：{file_path}（未找到 YAML 块）")
            return False

        yaml_block = match.group(1)
        rest_content = match.group(2)

        try:
            data = yaml.safe_load(extract_yaml_block(yaml_block))
        except Exception as e:
            print(f"解析 YAML 失败：{file_path} - {e}")
            return False

        new_yaml_lines = ["---"]
        for field in field_order:
            if field in data:
                value = data[field]
                if isinstance(value, list):
                    new_yaml_lines.append(f"{field}: ")
                    for item in value:
                        new_yaml_lines.append(f"  - {item}")
                elif isinstance(value, bool):
                    new_yaml_lines.append(f"{field}: {str(value).lower()}")
                elif value is None:
                    new_yaml_lines.append(f"{field}: ")
                else:
                    new_yaml_lines.append(f"{field}: {value}")
            else:
                new_yaml_lines.append(f"{field}: ")

        new_yaml_lines.append("---")
        new_content = "\n".join(new_yaml_lines) + rest_content

        file_path.write_text(new_content, encoding="utf-8")
        print(f"已结构化：{file_path}")
        return True
    except Exception as e:
        print(f"处理文件 {file_path} 时出错：{e}")
        return False


# =========================
# 选项 11：删除没有数据的字段名
# =========================

def delete_empty_fields() -> None:
    """删除没有数据的字段名。"""
    source_dir = Path(input(r"请输入源文件夹（默认：d:\Studios\Attachments\Android\）：") or r"d:\Studios\Attachments\Android")

    processed_count = 0
    for file_path in source_dir.rglob("*.md"):
        if file_path.name == ".DatabaseStructure.md":
            continue
        if process_delete_empty_fields(file_path):
            processed_count += 1
    print(f"\n空字段删除完成！共处理 {processed_count} 个文件")


def process_delete_empty_fields(file_path: Path) -> bool:
    """处理单个文件的空字段删除。"""
    try:
        content = file_path.read_text(encoding="utf-8")
        match = re.search(r"(^---\n.*?\n---)(.*)", content, flags=re.DOTALL)
        if not match:
            print(f"跳过：{file_path}（未找到 YAML 块）")
            return False

        yaml_block = match.group(1)
        rest_content = match.group(2)

        try:
            data = yaml.safe_load(extract_yaml_block(yaml_block))
        except Exception as e:
            print(f"解析 YAML 失败：{file_path} - {e}")
            return False

        new_yaml_lines = ["---"]
        has_changes = False

        for field, value in data.items():
            is_empty = (
                value is None
                or value == ""
                or (isinstance(value, list) and len(value) == 0)
            )
            if not is_empty:
                if isinstance(value, list):
                    new_yaml_lines.append(f"{field}: ")
                    for item in value:
                        new_yaml_lines.append(f"  - {item}")
                else:
                    new_yaml_lines.append(f"{field}: {value}")
            else:
                has_changes = True

        new_yaml_lines.append("---")
        new_content = "\n".join(new_yaml_lines) + rest_content

        if not has_changes:
            return False

        file_path.write_text(new_content, encoding="utf-8")
        print(f"已清理空字段：{file_path}")
        return True
    except Exception as e:
        print(f"处理文件 {file_path} 时出错：{e}")
        return False


# =========================
# 选项 12：双引号置换单引号
# =========================

def replace_double_quotes() -> None:
    """双引号置换单引号功能。"""
    source_dir = Path(input(r"请输入源文件夹（默认：d:\Studios\Attachments\Android\）：") or r"d:\Studios\Attachments\Android")

    processed_count = 0
    for file_path in source_dir.rglob("*.md"):
        if process_replace_double_quotes(file_path):
            processed_count += 1
    print(f"\n双引号置换单引号完成！共处理 {processed_count} 个文件")


def process_replace_double_quotes(file_path: Path) -> bool:
    """处理单个文件的双引号置换单引号。"""
    try:
        lines = file_path.read_text(encoding="utf-8").splitlines(keepends=True)
        has_changes = False
        new_lines = []

        for line in lines:
            double_quote_count = line.count('"')
            if double_quote_count <= 2:
                new_lines.append(line)
            else:
                first_quote_pos = line.find('"')
                last_quote_pos = line.rfind('"')
                new_line = ""
                for i, char in enumerate(line):
                    if char == '"':
                        if i == first_quote_pos or i == last_quote_pos:
                            new_line += '"'
                        else:
                            new_line += "'"
                            has_changes = True
                    else:
                        new_line += char
                new_lines.append(new_line)

        if not has_changes:
            return False

        file_path.write_text("".join(new_lines), encoding="utf-8")
        print(f"已处理：{file_path}")
        return True
    except Exception as e:
        print(f"处理文件 {file_path} 时出错：{e}")
        return False


# =========================
# 选项 13：属性内容处理
# =========================

def process_attribute_content() -> None:
    """属性内容处理功能。"""
    source_dir = Path(input(r"请输入源文件夹（默认：d:\Studios\Attachments\Android\）：") or r"d:\Studios\Attachments\Android")
    attribute_name = input("请输入要处理的属性名称：")

    print("\n请选择处理方式：")
    print('1. 将该属性内容设置为空（""）')
    print("2. 将该属性内容设置为指定内容")
    print("3. 将该属性内容每个单词大写")
    print("4. 将该属性内容每个单词小写")
    print("5. 将该属性内容每个单词首字母大写，其余小写")
    print("6. 将该属性内容（汉字、英文、或数字）用空格隔开")
    print("7. 将该属性内容的汉字繁体中文转为简体中文")
    print("8. 所有半角标点符号转为全角标点符号")

    choice = input("请输入数字选择操作（1/2/3/4/5/6/7/8）：")
    new_content = input("请输入要设置的属性内容：") if choice == "2" else None

    processed_count = 0
    for file_path in source_dir.rglob("*.md"):
        if process_attribute_content_file(file_path, attribute_name, choice, new_content):
            processed_count += 1
    print(f"\n属性内容处理完成！共处理 {processed_count} 个文件")


def process_attribute_content_file(
    file_path: Path, attribute_name: str, operation: str, new_content: str | None = None
) -> bool:
    """处理单个文件的属性内容。"""
    try:
        content = file_path.read_text(encoding="utf-8")
        match = re.search(r"(^---\n.*?\n---)(.*)", content, flags=re.DOTALL)
        if not match:
            print(f"跳过：{file_path}（未找到 YAML 块）")
            return False

        yaml_block = match.group(1)
        rest_content = match.group(2)

        try:
            data = yaml.safe_load(extract_yaml_block(yaml_block))
        except Exception as e:
            print(f"解析 YAML 失败：{file_path} - {e}")
            return False

        if attribute_name not in data:
            return False

        original_value = data[attribute_name]

        if operation == "1":
            processed_value = ""
        elif operation == "2":
            processed_value = new_content
        elif operation == "3":
            processed_value = (
                [item.upper() for item in original_value]
                if isinstance(original_value, list)
                else original_value.upper()
            )
        elif operation == "4":
            processed_value = (
                [item.lower() for item in original_value]
                if isinstance(original_value, list)
                else original_value.lower()
            )
        elif operation == "5":
            processed_value = (
                [item.title() for item in original_value]
                if isinstance(original_value, list)
                else original_value.title()
            )
        elif operation == "6":
            processed_value = (
                [separate_chinese_english_numbers(item) for item in original_value]
                if isinstance(original_value, list)
                else separate_chinese_english_numbers(original_value)
            )
        elif operation == "7":
            if not ZHCONV_AVAILABLE:
                print("警告：zhconv 库未安装，无法进行简繁转换。请使用 pip install zhconv 安装。")
                return False
            processed_value = (
                [zhconv.convert(item, "zh-cn") for item in original_value]
                if isinstance(original_value, list)
                else zhconv.convert(original_value, "zh-cn")
            )
        elif operation == "8":
            processed_value = (
                [half_to_full_width(item) for item in original_value]
                if isinstance(original_value, list)
                else half_to_full_width(original_value)
            )
        else:
            print(f"无效的操作选择：{operation}")
            return False

        data[attribute_name] = processed_value

        new_yaml_lines = ["---"]
        for field, value in data.items():
            if isinstance(value, list):
                new_yaml_lines.append(f"{field}:")
                for item in value:
                    new_yaml_lines.append(f"  - {escape_yaml_value(item)}")
            elif isinstance(value, bool):
                new_yaml_lines.append(f"{field}: {str(value).lower()}")
            elif value is None:
                new_yaml_lines.append(f"{field}: ")
            else:
                new_yaml_lines.append(f"{field}: {escape_yaml_value(value)}")

        new_yaml_lines.append("---")
        file_path.write_text("\n".join(new_yaml_lines) + rest_content, encoding="utf-8")
        print(f"已处理：{file_path}")
        return True
    except Exception as e:
        print(f"处理文件 {file_path} 时出错：{e}")
        return False


def separate_chinese_english_numbers(text: str) -> str:
    """将汉字、英文、数字用空格隔开。"""
    if not text:
        return text
    result = re.sub(r"([一-鿿])(?=[a-zA-Z0-9])", r"\1 ", str(text))
    result = re.sub(r"(?<=[a-zA-Z0-9])([一-鿿])", r" \1", result)
    result = re.sub(r"([a-zA-Z])(?=\d)", r"\1 ", result)
    result = re.sub(r"(?<=\d)([a-zA-Z])", r" \1", result)
    result = re.sub(r"\s+", " ", result)
    return result.strip()


def half_to_full_width(text: str) -> str:
    """半角标点符号转为全角标点符号。"""
    if not text:
        return text

    half_to_full_map = {
        " ": "　", ",": "，", "~": "～", ":": "：", ";": "；",
        "!": "！", "?": "？", "%": "％", "+": "＋", "-": "－",
        "=": "＝", "/": "／", "\\": "＼", "(": "（", ")": "）",
        "<": "〈", ">": "〉",
    }

    result = str(text)

    # 智能双引号替换
    quote_count = 0
    pos = 0
    while pos < len(result):
        if result[pos] == '"':
            quote_count += 1
            replacement = "「" if quote_count % 2 == 1 else "」"
            result = result[:pos] + replacement + result[pos + 1 :]
            pos += len(replacement)
        else:
            pos += 1

    for half, full in half_to_full_map.items():
        result = result.replace(half, full)

    return result


# =========================
# 主菜单
# =========================

def main() -> None:
    """主循环：显示菜单 → 选择功能 → 执行。"""
    while True:
        print("\n" + "=" * 50)
        print("请选择操作：")
        print("1. 根据文件夹生成 Excel 文件")
        print("2. 根据 Excel 生成 Markdown 文件夹")
        print("3. 从 CSV 生成 Markdown 文件")
        print("4. 删除字段")
        print("5. 添加字段")
        print("6. 查找与替换（普通）")
        print("7. 查找与替换（正则表达式）")
        print("8. 元替换")
        print("9. 生成数据结构文件")
        print("10. 结构化数据文件")
        print("11. 删除没有数据的字段名")
        print("12. 双引号置换单引号")
        print("13. 属性内容处理")
        print("0. 退出程序")
        choice = input("请输入数字选择操作（1-13,0）：")

        if choice == "1":
            generate_excel_from_folder()
        elif choice == "2":
            generate_markdown_from_excel()
        elif choice == "3":
            generate_from_csv()
        elif choice == "4":
            delete_field()
        elif choice == "5":
            add_field()
        elif choice == "6":
            find_and_replace()
        elif choice == "7":
            find_and_replace_regex()
        elif choice == "8":
            meta_replacement()
        elif choice == "9":
            generate_structure_file()
        elif choice == "10":
            restructure_files()
        elif choice == "11":
            delete_empty_fields()
        elif choice == "12":
            replace_double_quotes()
        elif choice == "13":
            process_attribute_content()
        elif choice == "0":
            print("程序已退出")
            break
        else:
            print("无效选择，请重新输入")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
    input("按回车键退出程序...")
