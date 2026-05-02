# 请帮我写个中文的 Python 脚本，批注也是中文，但是变量参数是英文的：
# 在脚本开始前询问我主 excel 文件位置（默认为：d:\Works\Attachments\main.xlsx）与客 excel 文件位置（默认为：d:\Works\Attachments\secondary.xlsx）。
# 主 excel 与 客 excel，第一行为表头（字段名）。此后每一行为一条记录。二者字段名多少与记录多少并不一致。
# 从主 excel 找到字段“原文件名”，枚举每一条记录，根据每一条记录的“原文件名”字段，在客 excel 中找到该记录，将该记录的“加密文件名”字段读取，写入主 excel 的“加密文件名”字段去。如果成功则在客 excel 中“确定”字段中赋值“yes”。
# 完成后，反复循环我主 excel 文件位置与客 excel 文件位置。

# 导入模块
import pandas as pd
import os

def get_file_path(prompt, default_path):
    """
    获取文件路径，若用户直接回车则使用默认值。
    
    参数:
        prompt (str): 提示信息
        default_path (str): 默认路径
    
    返回:
        str: 有效的文件路径
    """
    user_input = input(f"{prompt} (默认: {default_path}): ").strip()
    if user_input == "":
        path = default_path
    else:
        path = user_input
    
    # 检查文件是否存在
    if not os.path.exists(path):
        print(f"错误：文件不存在 -> {path}")
        return None
    return path

def process_excel(main_path, secondary_path):
    """
    处理主 Excel 和客 Excel 的匹配与更新。
    
    参数:
        main_path (str): 主 Excel 文件路径
        secondary_path (str): 客 Excel 文件路径
    """
    try:
        # 读取 Excel 文件
        main_df = pd.read_excel(main_path)
        secondary_df = pd.read_excel(secondary_path)
        
        # 确保必要字段存在
        required_main_cols = ["原文件名", "加密文件名"]
        required_secondary_cols = ["原文件名", "加密文件名", "确定"]
        
        for col in required_main_cols:
            if col not in main_df.columns:
                main_df[col] = None  # 若“加密文件名”不存在则新增列
        for col in required_secondary_cols:
            if col not in secondary_df.columns:
                secondary_df[col] = None  # 若“确定”列不存在则新增列
        
        # 记录匹配成功的次数
        match_count = 0
        
        # 遍历主表每一行
        for idx, main_row in main_df.iterrows():
            original_name = main_row["原文件名"]
            if pd.isna(original_name):
                continue  # 跳过空的原文件名
            
            # 在客表中查找匹配的记录（第一个匹配项）
            match_idx = secondary_df[secondary_df["原文件名"] == original_name].index
            if len(match_idx) > 0:
                matched_index = match_idx[0]
                encrypted_name = secondary_df.at[matched_index, "加密文件名"]
                
                # 写入主表的“加密文件名”
                main_df.at[idx, "加密文件名"] = encrypted_name
                # 在客表的“确定”字段标记为 "yes"
                secondary_df.at[matched_index, "确定"] = "yes"
                match_count += 1
                print(f"匹配成功: {original_name} -> {encrypted_name}")
            else:
                print(f"未找到匹配: {original_name}")
        
        # 保存修改后的主表和客表（覆盖原文件）
        main_df.to_excel(main_path, index=False)
        secondary_df.to_excel(secondary_path, index=False)
        
        print(f"\n处理完成！共匹配 {match_count} 条记录。")
        print(f"主文件已保存: {main_path}")
        print(f"客文件已保存: {secondary_path}")
    
    except Exception as e:
        print(f"处理过程中发生错误: {e}")

def main():
    """
    主函数：循环处理多组 Excel 文件对。
    """
    print("=== Excel 字段匹配工具 ===\n")
    
    while True:
        print("\n--- 请指定本次要处理的文件 ---")
        main_path = get_file_path("请输入主 Excel 文件位置", r"d:\Works\Attachments\main.xlsx")
        if main_path is None:
            print("主文件无效，请重新输入。")
            continue
        
        secondary_path = get_file_path("请输入客 Excel 文件位置", r"d:\Works\Attachments\secondary.xlsx")
        if secondary_path is None:
            print("客文件无效，请重新输入。")
            continue
        
        # 执行处理
        process_excel(main_path, secondary_path)
        
        # 询问是否继续处理其他文件对
        again = input("\n是否继续处理其他文件？(y/n): ").strip().lower()
        if again != 'y':
            print("程序结束。")
            break

if __name__ == "__main__":
    main()