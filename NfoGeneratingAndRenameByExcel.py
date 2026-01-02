# 请帮我写个中文的 Python 脚本，批注也是中文，但是变量参数不要是中文：
# 在脚本开始前询问我 excel 文件位置（默认为：e:\Documents\Creations\Scripts\Attachment\标准.xlsx）、写入文件夹位置（默认为：d:\Works\In\）。
# 重命名即生成 nfo 文件：读取 excel 文件，第一行为表头（字段名）。此后每一行为一条记录。"原文件名"字段值对应着写入文件夹中到每一个文件名字。依次根据每一行到"原文件名"找到写入文件夹中到每一个文件，将其改名为同一行中的“现文件名”。根据“现文件名”生成同名“*.nfo”文件。nfo 文件内写入的内容：UTF-8编码，<?xml version="1.0" encoding="UTF-8" standalone="yes"?><movie>  <title> </title></movie>，将该行中的“名字”字段填入“<title> </title>”内的“ ”。
# 完成后，反复循环。

# 导入模块
import os
import pandas as pd
import xml.etree.ElementTree as ET
from pathlib import Path

# ==================== 全局配置 ====================
DEFAULT_EXCEL_PATH = r"e:\Documents\Creations\Scripts\Attachment\标准.xlsx"
DEFAULT_WRITE_DIR = r"d:\Works\In"

# ==================== 辅助函数 ====================

def get_input_with_default(prompt_text, default_value):
    """获取带默认值的用户输入"""
    user_input = input(f"{prompt_text} (默认: {default_value}): ").strip()
    return user_input if user_input else default_value

def ensure_directory_exists(directory_path):
    """确保目录存在，如果不存在则创建"""
    if not os.path.exists(directory_path):
        os.makedirs(directory_path, exist_ok=True)
        print(f"已创建目录: {directory_path}")
    return directory_path

def find_file_in_directory(directory_path, filename):
    """在目录中查找文件，支持子目录查找"""
    matches = []
    
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file == filename:
                matches.append(os.path.join(root, file))
    
    return matches

def create_nfo_file(filepath, title):
    """创建NFO文件"""
    try:
        # 创建XML结构
        movie_elem = ET.Element("movie")
        
        title_elem = ET.SubElement(movie_elem, "title")
        title_elem.text = title
        
        # 转换为XML字符串
        xml_str = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        
        # 手动格式化，因为ElementTree的tostring没有格式化选项
        xml_str += '<movie>\n'
        xml_str += f'  <title>{title}</title>\n'
        xml_str += '</movie>'
        
        # 写入文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(xml_str)
        
        return True
    except Exception as e:
        print(f"创建NFO文件失败 {filepath}: {e}")
        return False

# ==================== 主要功能 ====================

def rename_and_generate_nfo(excel_path, write_dir):
    """
    重命名文件并生成NFO文件
    参数:
        excel_path: Excel文件路径
        write_dir: 写入文件夹路径
    """
    print("\n=== 开始重命名并生成NFO文件 ===")
    
    # 检查Excel文件是否存在
    if not os.path.exists(excel_path):
        print(f"错误: Excel文件不存在 - {excel_path}")
        return False
    
    # 检查写入文件夹是否存在
    if not os.path.exists(write_dir):
        print(f"错误: 写入文件夹不存在 - {write_dir}")
        return False
    
    # 读取Excel文件
    try:
        df = pd.read_excel(excel_path, engine='openpyxl')
    except Exception as e:
        print(f"读取Excel文件失败: {e}")
        return False
    
    # 检查必要的字段是否存在
    required_columns = ["原文件名", "现文件名", "名字"]
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        print(f"错误: Excel文件中缺少以下必要字段: {', '.join(missing_columns)}")
        return False
    
    # 处理每一行
    processed_count = 0
    rename_failures = 0
    nfo_failures = 0
    
    for index, row in df.iterrows():
        try:
            # 获取字段值
            original_filename = row.get("原文件名", "")
            new_filename = row.get("现文件名", "")
            name_value = row.get("名字", "")
            
            # 跳过空值
            if (pd.isna(original_filename) or pd.isna(new_filename) or 
                pd.isna(name_value) or 
                not original_filename or not new_filename or not name_value):
                continue
            
            # 转换为字符串并去除空白
            original_filename = str(original_filename).strip()
            new_filename = str(new_filename).strip()
            name_value = str(name_value).strip()
            
            # 如果原文件名和现文件名相同，跳过重命名
            if original_filename == new_filename:
                print(f"跳过第 {index+1} 行: 原文件名和现文件名相同")
                # 仍然生成NFO文件
                target_file = None
                
                # 查找文件
                found_files = find_file_in_directory(write_dir, original_filename)
                
                if found_files:
                    target_file = found_files[0]
                    
                    # 生成NFO文件
                    nfo_filename = os.path.splitext(original_filename)[0] + ".nfo"
                    nfo_filepath = os.path.join(os.path.dirname(target_file), nfo_filename)
                    
                    if create_nfo_file(nfo_filepath, name_value):
                        print(f"已生成NFO文件: {nfo_filename}")
                        processed_count += 1
                    else:
                        nfo_failures += 1
                else:
                    print(f"未找到文件: {original_filename}")
                continue
            
            # 查找源文件
            found_files = find_file_in_directory(write_dir, original_filename)
            
            if not found_files:
                print(f"未找到文件: {original_filename}")
                continue
            
            if len(found_files) > 1:
                print(f"找到多个同名文件，使用第一个: {original_filename}")
            
            source_file = found_files[0]
            
            # 重命名文件
            try:
                # 获取源文件目录
                source_dir = os.path.dirname(source_file)
                
                # 构建新文件路径
                new_filepath = os.path.join(source_dir, new_filename)
                
                # 检查新文件是否已存在
                if os.path.exists(new_filepath):
                    print(f"目标文件已存在，跳过重命名: {new_filename}")
                    target_file = new_filepath
                else:
                    # 重命名文件
                    os.rename(source_file, new_filepath)
                    print(f"已重命名: {original_filename} -> {new_filename}")
                    target_file = new_filepath
                
                # 生成NFO文件
                nfo_filename = os.path.splitext(new_filename)[0] + ".nfo"
                nfo_filepath = os.path.join(source_dir, nfo_filename)
                
                if create_nfo_file(nfo_filepath, name_value):
                    print(f"已生成NFO文件: {nfo_filename}")
                    processed_count += 1
                else:
                    nfo_failures += 1
                
            except Exception as e:
                print(f"重命名文件失败 {original_filename}: {e}")
                rename_failures += 1
                
        except Exception as e:
            print(f"处理第 {index+1} 行时出错: {e}")
            continue
    
    # 输出处理结果
    print(f"\n处理完成!")
    print(f"成功处理: {processed_count} 个文件")
    print(f"重命名失败: {rename_failures} 个文件")
    print(f"NFO文件生成失败: {nfo_failures} 个文件")
    
    return processed_count > 0

# ==================== 主程序 ====================

def main():
    """主程序"""
    print("=" * 60)
    print("重命名并生成NFO文件脚本")
    print("功能: 根据Excel文件重命名文件并生成对应的NFO文件")
    print("=" * 60)
    
    while True:
        print("\n" + "=" * 60)
        print("[配置参数]")
        
        # 获取用户输入
        excel_path = get_input_with_default("请输入Excel文件位置", DEFAULT_EXCEL_PATH)
        write_dir = get_input_with_default("请输入写入文件夹位置", DEFAULT_WRITE_DIR)
        
        # 执行主要功能
        success = rename_and_generate_nfo(excel_path, write_dir)
        
        if success:
            print("操作成功完成!")
        else:
            print("操作失败或未处理任何文件!")
        
        # 询问是否继续
        print("\n" + "=" * 60)
        print("[操作选项]")
        print("1. 重新配置并执行")
        print("0. 退出程序")
        
        choice = input("\n请选择操作 (1/0): ").strip()
        
        if choice == '0':
            print("\n程序已退出")
            break
        elif choice != '1':
            print("无效选择，将重新配置并执行")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
    except Exception as e:
        print(f"\n程序运行出错: {e}")
    finally:
        input("\n按回车键退出程序...")