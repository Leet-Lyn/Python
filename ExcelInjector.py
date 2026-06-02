# 请帮我写个中文的 Python 脚本，批注也是中文，但是变量参数是英文的：
# 在脚本开始前询问我主 excel 文件位置（默认为：d:\Works\Attachments\main.xlsx）与客 excel 文件位置（默认为：d:\Works\Attachments\secondary.xlsx）。
# 主 excel 与 客 excel，第一行为表头（字段名）。此后每一行为一条记录。二者字段名多少与记录多少并不一致。
# 从主 excel 找到字段“现文件名”，枚举每一条记录，根据每一条记录的“现文件名”字段，在客 excel 中找到该记录，将该记录的“加密文件名”字段读取，写入主 excel 的“加密文件名”字段去。将该记录的“矫正文件名”字段读取，写入主 excel 的“矫正文件名”字段去。如果成功则在客 excel 中“确定”字段中赋值“yes”。
# 如果出错，给出详细信息。
# 完成后，反复循环我主 excel 文件位置与客 excel 文件位置。

# 导入模块
# -*- coding: utf-8 -*-
"""
Excel 字段匹配工具
功能：根据主表中的“现文件名”字段，在客表中查找匹配记录，
      将客表的“加密文件名”和“矫正文件名”写入主表的对应字段，
      并在客表的“确定”字段标记“yes”。
支持循环处理多组文件，并给出详细的错误信息。
"""

import pandas as pd
import os
import traceback

def get_file_path(prompt, default_path):
    """
    获取文件路径，若用户直接回车则使用默认值。
    
    参数:
        prompt (str): 提示信息
        default_path (str): 默认路径
    
    返回:
        str: 有效的文件路径，若文件不存在则返回 None
    """
    user_input = input(f"{prompt} (默认: {default_path}): ").strip()
    path = user_input if user_input != "" else default_path
    
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
        print("正在读取主文件...")
        main_df = pd.read_excel(main_path)
        print("正在读取客文件...")
        secondary_df = pd.read_excel(secondary_path)
        
        # 确保主表包含必要的列
        required_main_cols = ["现文件名", "加密文件名", "矫正文件名"]
        for col in required_main_cols:
            if col not in main_df.columns:
                main_df[col] = None  # 若列不存在则新增，默认填充 None
                print(f"提示：主表缺少列 '{col}'，已自动添加。")
        
        # 确保客表包含必要的列
        required_secondary_cols = ["现文件名", "加密文件名", "矫正文件名", "确定"]
        for col in required_secondary_cols:
            if col not in secondary_df.columns:
                secondary_df[col] = None
                print(f"提示：客表缺少列 '{col}'，已自动添加。")
        
        # 记录匹配成功的次数
        match_count = 0
        
        # 遍历主表每一行
        for idx, main_row in main_df.iterrows():
            current_name = main_row["现文件名"]
            if pd.isna(current_name):
                print(f"警告：主表第 {idx+2} 行（Excel行号）的“现文件名”为空，已跳过。")
                continue
            
            # 在客表中查找匹配的记录（第一个匹配项）
            # 注意：使用 .copy() 避免链式赋值警告，但这里直接使用布尔索引即可
            match_idx = secondary_df[secondary_df["现文件名"] == current_name].index
            if len(match_idx) > 0:
                matched_index = match_idx[0]
                encrypted_name = secondary_df.at[matched_index, "加密文件名"]
                corrected_name = secondary_df.at[matched_index, "矫正文件名"]
                
                # 写入主表的“加密文件名”和“矫正文件名”
                main_df.at[idx, "加密文件名"] = encrypted_name
                main_df.at[idx, "矫正文件名"] = corrected_name
                # 在客表的“确定”字段标记为 "yes"
                secondary_df.at[matched_index, "确定"] = "yes"
                match_count += 1
                print(f"匹配成功: {current_name} -> 加密文件: {encrypted_name}, 矫正文件: {corrected_name}")
            else:
                print(f"未找到匹配: {current_name}")
        
        # 保存修改后的主表和客表（覆盖原文件）
        print("正在保存主文件...")
        main_df.to_excel(main_path, index=False)
        print("正在保存客文件...")
        secondary_df.to_excel(secondary_path, index=False)
        
        print(f"\n处理完成！共匹配 {match_count} 条记录。")
        print(f"主文件已保存: {main_path}")
        print(f"客文件已保存: {secondary_path}")
    
    except Exception as e:
        # 输出详细错误信息，包括异常类型和堆栈跟踪
        print(f"处理过程中发生错误: {type(e).__name__}: {e}")
        print("详细堆栈信息：")
        traceback.print_exc()

def main():
    """
    主函数：循环处理多组 Excel 文件对。
    """
    print("=== Excel 字段匹配工具（现文件名 → 加密文件名 + 矫正文件名）===")
    print("说明：主表需要包含“现文件名”字段，客表需要包含“现文件名”、“加密文件名”、“矫正文件名”字段。\n")
    
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