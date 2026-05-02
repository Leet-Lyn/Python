# 请帮我写个中文的 Python 脚本，批注也是中文，但是变量参数不要是中文：
# 在脚本开始前询问我 excel 文件位置（默认为：d:\Works\Attachments\标准.xlsx）、源文件夹位置（默认为：d:\Works\Ins\），目标文件夹位置（默认为：d:\Works\Outs\）。
# Excel 第一行为表头（字段名）。此后每一行为一条记录。
# 从 excel 找到字段“加密文件名”，枚举每一条记录，根据每一条记录的“加密文件名”字段，在源文件夹及其子文件夹位置找到相应文件，移动到目标文件夹。
# 如果成功则在 excel 中“确定”字段中赋值“yes”。
# 完成后，反复循环我 excel 文件位置与源文件夹位置、目标文件夹位置。

# 导入模块
import os
import shutil
import pandas as pd

def get_path(prompt, default_path):
    """
    获取用户输入的路径，若直接回车则使用默认值。
    :param prompt: 提示文字
    :param default_path: 默认路径
    :return: 用户输入或默认的路径字符串
    """
    user_input = input(f"{prompt}（默认为：{default_path}）: ").strip()
    if user_input == "":
        return default_path
    return user_input

def find_file_recursively(source_dir, filename):
    """
    在 source_dir 及其所有子文件夹中递归查找指定名称的文件。
    :param source_dir: 根目录路径
    :param filename: 要查找的文件名（不含路径）
    :return: 找到的完整文件路径，未找到则返回 None
    """
    for root, dirs, files in os.walk(source_dir):
        if filename in files:
            return os.path.join(root, filename)
    return None

def process_excel(excel_path, source_dir, target_dir):
    """
    处理单个 Excel 文件：根据“加密文件名”在源文件夹（含子文件夹）中查找并移动文件，更新“确定”列。
    :param excel_path: Excel 文件路径
    :param source_dir: 源文件夹路径（递归搜索）
    :param target_dir: 目标文件夹路径
    :return: 是否处理成功
    """
    try:
        # 读取 Excel 文件，所有列读为字符串以避免类型问题
        print("正在读取 Excel 文件...")
        df = pd.read_excel(excel_path, dtype=str, engine='openpyxl')
    except Exception as e:
        print(f"读取 Excel 文件失败：{e}")
        return False

    # 检查必需的列是否存在
    if '加密文件名' not in df.columns:
        print("Excel 中缺少字段 '加密文件名'，请检查表头。")
        return False

    # 如果“确定”列不存在，则新增该列，初始为空字符串
    if '确定' not in df.columns:
        df['确定'] = ""

    # 确保源文件夹和目标文件夹存在
    if not os.path.exists(source_dir):
        print(f"源文件夹不存在：{source_dir}")
        return False
    if not os.path.exists(target_dir):
        print(f"目标文件夹不存在，正在创建：{target_dir}")
        os.makedirs(target_dir)

    # 遍历每一行记录
    moved_count = 0
    for idx, row in df.iterrows():
        # 如果“确定”已经是 yes，跳过（避免重复移动）
        if row.get('确定') == 'yes':
            continue

        encrypted_name = row['加密文件名']
        # 跳过空值
        if pd.isna(encrypted_name) or encrypted_name == "":
            continue

        # 在源文件夹（含子文件夹）中递归查找文件
        src_path = find_file_recursively(source_dir, encrypted_name)

        if src_path is not None:
            dst_path = os.path.join(target_dir, encrypted_name)
            try:
                # 移动文件（如果目标已存在，shutil.move 会覆盖）
                shutil.move(src_path, dst_path)
                df.at[idx, '确定'] = 'yes'
                moved_count += 1
                print(f"已移动：{encrypted_name} (原路径: {src_path})")
            except Exception as e:
                print(f"移动文件失败 {encrypted_name}：{e}")
        else:
            print(f"源文件中未找到：{encrypted_name}（搜索目录：{source_dir} 及其子文件夹）")

    # 将更新后的 DataFrame 写回 Excel
    try:
        print(f"正在保存 Excel 文件：{excel_path}")
        df.to_excel(excel_path, index=False, engine='openpyxl')
        print(f"处理完成！共成功移动 {moved_count} 个文件，并已在 Excel 中标记 'yes'。")
        return True
    except Exception as e:
        print(f"保存 Excel 文件失败：{e}")
        return False

def main():
    """
    主循环：反复询问文件/文件夹路径并执行处理，直到用户选择退出。
    """
    print("=== 加密文件批量移动工具（支持源文件夹递归搜索）===\n")
    while True:
        print("\n--- 新一轮处理 ---")
        # 获取三个路径
        excel_file = get_path("请输入 Excel 文件位置", r"d:\Works\Attachments\标准.xlsx")
        source_folder = get_path("请输入源文件夹位置", r"d:\Works\Ins")
        target_folder = get_path("请输入目标文件夹位置", r"d:\Works\Outs")

        # 检查 Excel 文件是否存在
        if not os.path.exists(excel_file):
            print(f"错误：Excel 文件不存在 -> {excel_file}")
        else:
            process_excel(excel_file, source_folder, target_folder)

        # 询问是否继续
        again = input("\n是否继续处理其他文件/文件夹？(y/n，默认 n): ").strip().lower()
        if again != 'y':
            print("程序结束。")
            break

if __name__ == "__main__":
    main()