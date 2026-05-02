# 请帮我写个中文的 Python 脚本，批注也是中文，但是变量参数不要是中文：
# 在脚本开始前询问我 excel 文件位置（默认为：d:\Works\Attachments\标准.xlsx）。
# Excel 第一行为表头（字段名）。此后每一行为一条记录。
# 从 excel 找到字段“加密文件名”，该字段内可能包含多个文件名，以“, ”（半角逗号与半角空格）隔开。请枚举每一条记录，根据每一条记录的“加密文件名”字段，如果该字段内可能包含包含多个文件名，请将该条记录，拆分成多条记录（其他字段不变）。生成新的 excel 文件。

# 导入模块
import os
import pandas as pd
from pathlib import Path

def main():
    # 1. 询问 Excel 文件位置，支持默认路径
    default_path = r"d:\Works\Attachments\标准.xlsx"
    user_input = input(f"请输入 Excel 文件路径（默认：{default_path}）: ").strip()
    if not user_input:
        excel_path = default_path
    else:
        excel_path = user_input

    # 检查文件是否存在
    if not os.path.exists(excel_path):
        print(f"错误：文件不存在 - {excel_path}")
        return

    # 2. 读取 Excel 文件
    try:
        df = pd.read_excel(excel_path, dtype=str)  # 将所有字段读为字符串，避免类型问题
        print(f"成功读取 Excel，共 {len(df)} 行。")
    except Exception as e:
        print(f"读取 Excel 失败：{e}")
        return

    # 检查必需字段
    target_col = "加密文件名"
    if target_col not in df.columns:
        print(f"错误：Excel 中找不到字段“{target_col}”，现有字段：{list(df.columns)}")
        return

    # 3. 拆分记录
    new_rows = []
    for idx, row in df.iterrows():
        # 获取加密文件名字段的值
        file_names_value = row[target_col]
        # 处理空值（None, NaN 或空字符串）
        if pd.isna(file_names_value) or str(file_names_value).strip() == "":
            # 没有文件名则保持原行
            new_rows.append(row.to_dict())
            continue

        # 按 ", " 分割文件名
        # 注意：必须严格按半角逗号+半角空格分割，如果实际文件中存在其他分隔符可能需要调整
        file_names = str(file_names_value).split(", ")
        # 去除可能的前后空格（分割后每个文件名可能包含首尾空格，但通常不会）
        file_names = [fname.strip() for fname in file_names if fname.strip()]

        if len(file_names) == 1:
            # 只有一个文件名，无需拆分
            new_rows.append(row.to_dict())
        else:
            # 拆分：为每个文件名生成一个新行，除“加密文件名”外其他字段相同
            for fname in file_names:
                new_row = row.to_dict()
                new_row[target_col] = fname   # 替换为单个文件名
                new_rows.append(new_row)

    # 4. 构建新的 DataFrame
    new_df = pd.DataFrame(new_rows)
    print(f"拆分完成，新数据共 {len(new_df)} 行。")

    # 5. 生成输出文件路径
    input_path = Path(excel_path)
    output_dir = input_path.parent
    output_name = input_path.stem + "_拆分" + input_path.suffix
    output_path = output_dir / output_name

    # 如果输出文件已存在，自动添加序号
    counter = 1
    while output_path.exists():
        output_name = f"{input_path.stem}_拆分_{counter}{input_path.suffix}"
        output_path = output_dir / output_name
        counter += 1

    # 6. 保存新 Excel
    try:
        new_df.to_excel(output_path, index=False, engine='openpyxl')
        print(f"新文件已保存至：{output_path}")
    except Exception as e:
        print(f"保存 Excel 失败：{e}")

if __name__ == "__main__":
    main()