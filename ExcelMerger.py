# 请帮我写个中文的 Python 脚本，批注也是中文，但是变量参数不要是中文：
# 在脚本开始前询问我 excel 文件夹位置（默认为：d:\Works\Attachments\）。
# 读取文件夹内所有 excel 文件，读取每一个 excel 文件，第一行为表头（字段名）。此后每一行为一条记录。
# 将所有 excel 文件，根据每一个 excel 文件的表头（字段名）进行合并（数据跟着表头（字段名）走），生成一个新的 excel 文件，文件名为父文件夹名。

# 导入模块
import os
import pandas as pd

def get_folder_path():

    default_path = r"d:\Works\Attachments"   # 原始字符串，防止 \W 被误解释
    folder = input(f"请输入 Excel 文件夹路径（默认为 {default_path}）：").strip()
    if not folder:
        folder = default_path
    # 转换为绝对路径并规范化
    folder = os.path.abspath(folder)
    return folder

def find_excel_files(folder):
    """
    查找文件夹内所有 Excel 文件（支持 .xlsx, .xls, .xlsm）
    """
    excel_extensions = ('.xlsx', '.xls', '.xlsm')
    files = []
    for file in os.listdir(folder):
        if file.lower().endswith(excel_extensions):
            files.append(os.path.join(folder, file))
    return files

def merge_excel_files(file_list):
    """
    读取所有 Excel 文件，按列名合并数据（不同文件的列自动对齐）
    """
    data_frames = []
    for file in file_list:
        try:
            # 读取 Excel 文件，假设第一行为表头
            df = pd.read_excel(file, header=0)
            data_frames.append(df)
            print(f"已读取：{os.path.basename(file)}，共 {len(df)} 行")
        except Exception as e:
            print(f"读取文件 {file} 时出错：{e}")
            continue

    if not data_frames:
        print("没有读取到任何有效数据，程序退出。")
        return None

    # 合并所有 DataFrame，外连接保证所有列都存在
    merged_df = pd.concat(data_frames, axis=0, join='outer', ignore_index=True)
    return merged_df

def main():
    # 1. 获取文件夹路径
    folder_path = get_folder_path()
    if not os.path.isdir(folder_path):
        print(f"错误：文件夹 '{folder_path}' 不存在。")
        return

    # 2. 查找所有 Excel 文件
    excel_files = find_excel_files(folder_path)
    if not excel_files:
        print(f"在文件夹 '{folder_path}' 中未找到任何 Excel 文件。")
        return

    print(f"找到 {len(excel_files)} 个 Excel 文件。")

    # 3. 合并数据
    merged_data = merge_excel_files(excel_files)
    if merged_data is None:
        return

    # 4. 确定输出文件名（使用父文件夹名）
    parent_folder_name = os.path.basename(folder_path)  # 获取文件夹名
    output_file = os.path.join(folder_path, f"{parent_folder_name}.xlsx")

    # 5. 保存合并后的数据
    try:
        merged_data.to_excel(output_file, index=False)
        print(f"合并完成，文件已保存为：{output_file}")
        print(f"总记录数：{len(merged_data)}，总字段数：{len(merged_data.columns)}")
    except Exception as e:
        print(f"保存文件时出错：{e}")

if __name__ == "__main__":
    main()