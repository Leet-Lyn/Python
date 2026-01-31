# 请帮我写个中文的 Python 脚本，批注也是中文，但是变量参数不要是中文：
# 在脚本开始前询问我 excel 文件位置（默认为：d:\Works\Attachment\标准.xlsx）、源文件夹位置（默认为：d:\Works\Downloads\），写入文件夹位置（默认为：d:\Works\In\），上传文件夹位置（默认为：d:\Works\Uploads\）。
# 询问我想要做什么：
# 1. 单文件写入：读取 excel 文件，第一行为表头（字段名）。此后每一行为一条记录。分别询问我"引用页"、"属于"、"主链接"的值（按回车则为空）。遍历源文件夹内所有文件及子文件夹中的文件，顺序完成。1. 每一条记录新开一行。2. "Index"字段值为上一行 "Index"字段值+1（如上一行为空或为表头，则"Index"字段值为 1）。3. 将源文件夹内文件名写入"名字"与"原文件名"字段值。4. 将该文件移动到写入文件夹下的子文件夹（子文件夹名字为源文件夹名，保持原来文件夹结构）。5. 将原来询问我的"引用页"、"属于"、"主链接"的值写入"引用页"、"属于"、"主链接"字段值。6. 计算并生成该文件的 Ed2K 链接。生成的 ed2k 链接，写入"标准链接"字段值。7. 通过"标准链接"字段值，分别生成"大小"、"散列"字段值。大小请转成 B、KB、MB、GB 形式，并精确到小数点后 4 位，hash 转全部大写。
# 2. 多文件写入：读取 excel 文件，第一行为表头（字段名）。此后每一行为一条记录。分别询问我"引用页"、"属于"、"主链接"的值（按回车则为空）。遍历源文件夹内所有文件及子文件夹中的文件，顺序完成。1. 新开一行。2. "Index"字段值为上一行 "Index"字段值+1（如上一行为空或为表头，则"Index"字段值为 1）。3. 将源文件夹名写入"名字"。将源文件夹内每个文件名写入临时文件“e:\Documents\Creations\Scripts\Attachment\SourceName.txt”中（内容先清空，每行一个），最合合并写入"原文件名"字段值。4. 将该文件移动到写入文件夹下的子文件夹（子文件夹名字为源文件夹名，保持原来文件夹结构）。5. 将原来询问我的"引用页"、"属于"、"主链接"的值写入"引用页"、"属于"、"主链接"字段值。6. 计算并生成该文件的 Ed2K 链接。生成的 ed2k 链接，写入临时文件“e:\Documents\Creations\Scripts\Attachment\Ed2kList.txt”中（内容先清空，每行一个），最合合并写入"标准链接"字段值。7. 通过每个"标准链接"字段值，分别将分解出的"大小"、"散列"值，大小请转成 B、KB、MB、GB 形式，并精确到小数点后 4 位，hash 转全部大写。写入临时文件“e:\Documents\Creations\Scripts\Attachment\Ed2kList.size.txt”、“e:\Documents\Creations\Scripts\Attachment\Ed2kList.hash.txt”中（内容先清空，每行一个），最合合并写入"大小"、"散列"字段值。
# 3. 读取 excel 文件，第一行为表头（字段名）。此后每一行为一条记录。分别询问我"引用页"、"属于"、"主链接"的值（按回车则为空）。遍历源文件夹内所有文件及子文件夹中的文件，顺序完成。1. 每一条记录新开一行。2. "Index"字段值为上一行 "Index"字段值+1（如上一行为空或为表头，则"Index"字段值为 1）。3. 将源文件夹内文件名写入"名字"与"原文件名"字段值。4. 将该文件移动到写入文件夹下的子文件夹（子文件夹名字为源文件夹名，保持原来文件夹结构），并移动到"z:\"中，如果无法完成写入"z:\"中，则重命名原文件（从后删除1个字符（不包括扩展名）），再次尝试将原文件向目标文件夹移动。反复循环，直至能将原文件向目标文件夹移动。如果有重命名过文件，将修改过的文件名写入"矫正文件名"字段值中。写入"z:\"后，系统会自动生成一个对应文件（自动加密的）。读取"d:\Xyz\"新生成的文件名，将其文件名（无扩展名）写入"加密文件名"字段值。将"d:\Xyz\"新生成的文件移动到上传文件夹下的子文件夹（子文件夹名字为源文件夹名，保持原来文件夹结构，在"d:\Xyz\"中不保留）。5. 将原来询问我的"引用页"、"属于"、"主链接"的值写入"引用页"、"属于"、"主链接"字段值。6. 计算并生成该文件的 Ed2K 链接。生成的 ed2k 链接，写入"标准链接"字段值。7. 通过"标准链接"字段值，分别生成"大小"、"散列"字段值。大小请转成 B、KB、MB、GB 形式，并精确到小数点后 4 位，hash 转全部大写。
# 4. 多文件复杂写入：读取 excel 文件，第一行为表头（字段名）。此后每一行为一条记录。分别询问我"引用页"、"属于"、"主链接"的值（按回车则为空）。遍历源文件夹内所有文件及子文件夹中的文件，顺序完成。1. 每一条记录新开一行。2. "Index"字段值为上一行 "Index"字段值+1（如上一行为空或为表头，则"Index"字段值为 1）。3. 将源文件夹名写入"名字"。将源文件夹内每个文件名写入临时文件“e:\Documents\Creations\Scripts\Attachment\SourceName.txt”中（内容先清空，每行一个），最合合并写入"原文件名"字段值。4. 将该文件移动到写入文件夹下的子文件夹（子文件夹名字为源文件夹名，保持原来文件夹结构），并移动到"z:\"中，如果无法完成写入"z:\"中，则重命名原文件（从后删除1个字符（不包括扩展名）），再次尝试将原文件向目标文件夹移动。反复循环，直至能将原文件向目标文件夹移动。如果有重命名过文件，将修改过的文件名写入临时文件“e:\Documents\Creations\Scripts\Attachment\ChangeName.txt”中（内容先清空，每行一个），最合合并写入"矫正文件名"字段值中。写入"z:\"后，系统会自动生成一个对应文件（自动加密的）。读取"d:\Xyz\"新生成的文件名，将其文件名（无扩展名）写入临时文件“e:\Documents\Creations\Scripts\Attachment\EncryptedName.txt”中（内容先清空，每行一个），最合合并写入"加密文件名"字段值中。将"d:\Xyz\"新生成的文件移动到上传文件夹下的子文件夹（子文件夹名字为源文件夹名，保持原来文件夹结构，在"d:\Xyz\"中不保留）。5. 将原来询问我的"引用页"、"属于"、"主链接"的值写入"引用页"、"属于"、"主链接"字段值。6. 计算并生成该文件的 Ed2K 链接。生成的 ed2k 链接，写入临时文件“e:\Documents\Creations\Scripts\Attachment\Ed2kList.txt”中（内容先清空，每行一个），最合合并写入"标准链接"字段值。7. 通过每个"标准链接"字段值，分别将分解出的"大小"、"散列"值，大小请转成 B、KB、MB、GB 形式，并精确到小数点后 4 位，hash 转全部大写。写入临时文件“e:\Documents\Creations\Scripts\Attachment\Ed2kList.size.txt”、“e:\Documents\Creations\Scripts\Attachment\Ed2kList.hash.txt”中（内容先清空，每行一个），最合合并写入"大小"、"散列"字段值。
# 0. 退出程序。
# 完成后，反复循环我要做什么。

# 导入模块
import os
import re
import shutil
import time
import urllib.parse
import subprocess
import pandas as pd
from pathlib import Path
import datetime

# ==================== 全局配置 ====================
# 使用原始字符串来处理Windows路径
DEFAULT_EXCEL_PATH = r"d:\Works\Attachment\标准.xlsx"
DEFAULT_SOURCE_DIR = r"d:\Works\Downloads"
DEFAULT_WRITE_DIR = r"d:\Works\In"
DEFAULT_UPLOAD_DIR = r"d:\Works\Uploads"
DEFAULT_TEMP_DIR = r"e:\Documents\Creations\Scripts\Attachment"
DEFAULT_RHASH_PATH = r"d:\ProApps\RHash\rhash.exe"
DEFAULT_XYZ_DIR = r"d:\Xyz"
Z_DRIVE_PATH = r"z:"

# 隐藏文件模式
HIDDEN_FILE_PATTERNS = [
    'desktop.ini',
    'descript.ion',
    '.encfs6.xml',
    'Thumbs.db',
    '.DS_Store',
    '._*'
]

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

def format_file_size(size_bytes):
    """格式化文件大小为B/KB/MB/GB，保留4位小数"""
    if size_bytes == 0:
        return "0 B"
    
    units = ["B", "KB", "MB", "GB"]
    unit_index = 0
    size = float(size_bytes)
    
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024.0
        unit_index += 1
    
    if unit_index == 0:
        return f"{size_bytes} B"
    else:
        return f"{size:.4f} {units[unit_index]}"

def is_hidden_file(file_name):
    """检查是否为隐藏文件"""
    file_name_lower = file_name.lower()
    
    # 检查常见隐藏文件
    for pattern in HIDDEN_FILE_PATTERNS:
        if pattern.startswith('.') and file_name.startswith('.'):
            return True
        if file_name_lower == pattern.lower():
            return True
    
    return False

def get_all_files(source_dir):
    """获取源目录下所有非隐藏文件"""
    all_files = []
    
    for root, dirs, files in os.walk(source_dir):
        # 跳过隐藏文件夹
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            if not is_hidden_file(file):
                file_path = os.path.join(root, file)
                all_files.append(file_path)
    
    return all_files

def generate_ed2k_link(file_path):
    """生成文件的ED2K链接"""
    try:
        if os.path.exists(DEFAULT_RHASH_PATH) and os.path.exists(file_path):
            result = subprocess.run(
                [DEFAULT_RHASH_PATH, "--uppercase", "--ed2k-link", file_path],
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            if result.returncode == 0:
                return result.stdout.strip()
        
        return ""
    except Exception as e:
        print(f"生成ED2K链接失败 {file_path}: {e}")
        return ""

def parse_ed2k_link(ed2k_link):
    """解析ED2K链接，提取文件大小和哈希值"""
    if not ed2k_link or not ed2k_link.startswith("ed2k://|file|"):
        return "", ""
    
    try:
        # 解码URL编码
        decoded_link = urllib.parse.unquote(ed2k_link)
        parts = decoded_link.split('|')
        
        if len(parts) >= 5:
            # 文件大小（字节）
            size_str = parts[3]
            # 哈希值
            filehash = parts[4].upper()
            
            # 格式化文件大小
            try:
                size_bytes = int(size_str)
                formatted_size = format_file_size(size_bytes)
            except ValueError:
                formatted_size = ""
            
            return formatted_size, filehash
        
        return "", ""
    except Exception as e:
        print(f"解析ED2K链接失败: {e}")
        return "", ""

def copy_to_z_drive_with_retry(source_file, z_drive_path=Z_DRIVE_PATH):
    """
    复制文件到Z盘，如果失败则重试（缩短文件名）
    返回：(成功复制到的路径, 修改后的文件名或None)
    """
    original_file_name = os.path.basename(source_file)
    file_stem, file_extension = os.path.splitext(original_file_name)
    current_stem = file_stem
    
    attempt_count = 0
    max_attempts = 50  # 最大尝试次数
    
    while attempt_count < max_attempts:
        try:
            target_file_name = f"{current_stem}{file_extension}"
            target_path = os.path.join(z_drive_path, target_file_name)
            
            # 复制文件
            shutil.copy2(source_file, target_path)
            
            # 如果文件名有修改，返回修改后的文件名
            if current_stem != file_stem:
                return target_path, target_file_name
            else:
                return target_path, None
                
        except Exception as e:
            attempt_count += 1
            
            # 如果文件名长度大于1，缩短文件名
            if len(current_stem) > 1:
                current_stem = current_stem[:-1]
            else:
                print(f"无法继续缩短文件名: {original_file_name}")
                return None, None
    
    print(f"达到最大尝试次数 {max_attempts}: {original_file_name}")
    return None, None

def wait_for_encrypted_file(xyz_dir=DEFAULT_XYZ_DIR, timeout_seconds=30):
    """
    等待加密文件生成
    返回：加密文件的文件名（不带扩展名）
    """
    start_time = time.time()
    check_interval = 1  # 检查间隔（秒）
    
    while time.time() - start_time < timeout_seconds:
        if os.path.exists(xyz_dir):
            # 获取所有非隐藏文件
            files = []
            for item in os.listdir(xyz_dir):
                item_path = os.path.join(xyz_dir, item)
                if os.path.isfile(item_path) and not is_hidden_file(item):
                    files.append(item)
            
            if files:
                # 返回第一个文件的文件名（不带扩展名）
                encrypted_file = files[0]
                return os.path.splitext(encrypted_file)[0]
        
        time.sleep(check_interval)
    
    print(f"等待加密文件超时 ({timeout_seconds}秒)")
    return ""

def move_file_with_structure(source_file, target_base_dir, source_base_dir, subfolder_name=None):
    """
    移动文件，保持文件夹结构
    返回：移动后的文件路径
    """
    try:
        # 计算相对路径
        if source_base_dir in source_file:
            relative_path = os.path.relpath(source_file, source_base_dir)
        else:
            # 如果不在源目录中，只使用文件名
            relative_path = os.path.basename(source_file)
        
        # 如果有子文件夹名，添加到目标路径
        if subfolder_name:
            target_dir = os.path.join(target_base_dir, subfolder_name, os.path.dirname(relative_path))
        else:
            target_dir = os.path.join(target_base_dir, os.path.dirname(relative_path))
        
        # 确保目标目录存在
        ensure_directory_exists(target_dir)
        
        # 构建目标文件路径
        target_file = os.path.join(target_dir, os.path.basename(source_file))
        
        # 移动文件
        shutil.move(source_file, target_file)
        return target_file
        
    except Exception as e:
        print(f"移动文件失败 {source_file}: {e}")
        return None

def get_last_index_from_excel(df):
    """从DataFrame中获取最后一个Index值"""
    if 'Index' in df.columns and not df.empty:
        # 找到所有非空Index值
        index_values = df['Index'].dropna()
        if not index_values.empty:
            try:
                # 获取最大值
                return int(index_values.max())
            except:
                return 0
    return 0

def clean_temp_files(temp_dir=DEFAULT_TEMP_DIR):
    """清理临时文件"""
    try:
        if os.path.exists(temp_dir):
            temp_files = [
                os.path.join(temp_dir, "SourceName.txt"),
                os.path.join(temp_dir, "ChangeName.txt"),
                os.path.join(temp_dir, "EncryptedName.txt"),
                os.path.join(temp_dir, "Ed2kList.txt"),
                os.path.join(temp_dir, "Ed2kList.size.txt"),
                os.path.join(temp_dir, "Ed2kList.hash.txt")
            ]
            
            for temp_file in temp_files:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                    print(f"已清理临时文件: {temp_file}")
    except Exception as e:
        print(f"清理临时文件失败: {e}")

# ==================== 主要功能 ====================

def single_file_write(excel_path, source_dir, write_dir, reference_page, belongs_to, main_link):
    """
    单文件写入功能
    每个文件对应Excel中的一行记录
    """
    print("\n=== 开始单文件写入 ===")
    
    # 读取Excel文件
    try:
        df = pd.read_excel(excel_path, engine='openpyxl')
    except Exception as e:
        print(f"读取Excel文件失败: {e}")
        return False
    
    # 获取最后一个Index值
    last_index = get_last_index_from_excel(df)
    
    # 获取所有文件
    all_files = get_all_files(source_dir)
    
    if not all_files:
        print("源文件夹中没有找到任何非隐藏文件")
        return False
    
    print(f"找到 {len(all_files)} 个文件")
    
    # 获取源文件夹名（用于子文件夹）
    source_folder_name = os.path.basename(source_dir.rstrip('\\/'))
    
    # 处理每个文件
    new_records = []
    
    for file_path in all_files:
        try:
            # 1. 新开一行
            new_record = {}
            
            # 2. Index字段值
            last_index += 1
            new_record['Index'] = last_index
            
            # 3. 写入文件名
            file_name = os.path.basename(file_path)
            file_name_without_ext = os.path.splitext(file_name)[0]
            
            new_record['名字'] = file_name_without_ext
            new_record['原文件名'] = file_name
            
            # 4. 移动文件
            moved_file = move_file_with_structure(file_path, write_dir, source_dir, source_folder_name)
            
            if moved_file:
                print(f"已移动文件: {file_name}")
                
                # 5. 写入引用页、属于、主链接
                new_record['引用页'] = reference_page
                new_record['属于'] = belongs_to
                new_record['主链接'] = main_link
                
                # 6. 生成ED2K链接
                ed2k_link = generate_ed2k_link(moved_file)
                new_record['标准链接'] = ed2k_link
                
                # 7. 解析大小和哈希
                if ed2k_link:
                    size, filehash = parse_ed2k_link(ed2k_link)
                    new_record['大小'] = size
                    new_record['散列'] = filehash
                else:
                    new_record['大小'] = ""
                    new_record['散列'] = ""
                
                new_records.append(new_record)
                print(f"已处理: {file_name} (Index: {last_index})")
                
        except Exception as e:
            print(f"处理文件失败 {file_path}: {e}")
            continue
    
    # 如果有新记录，添加到Excel
    if new_records:
        try:
            new_df = pd.DataFrame(new_records)
            df = pd.concat([df, new_df], ignore_index=True)
            df.to_excel(excel_path, index=False, engine='openpyxl')
            print(f"\n成功添加 {len(new_records)} 条记录到Excel")
            return True
            
        except Exception as e:
            print(f"保存Excel文件失败: {e}")
            return False
    
    return False

def multiple_file_write(excel_path, source_dir, write_dir, reference_page, belongs_to, main_link):
    """
    多文件写入功能
    整个源文件夹作为一个记录
    """
    print("\n=== 开始多文件写入 ===")
    
    # 读取Excel文件
    try:
        df = pd.read_excel(excel_path, engine='openpyxl')
    except Exception as e:
        print(f"读取Excel文件失败: {e}")
        return False
    
    # 获取最后一个Index值
    last_index = get_last_index_from_excel(df)
    
    # 获取所有文件
    all_files = get_all_files(source_dir)
    
    if not all_files:
        print("源文件夹中没有找到任何非隐藏文件")
        return False
    
    print(f"找到 {len(all_files)} 个文件")
    
    # 1. 新开一行
    new_record = {}
    
    # 2. Index字段值
    last_index += 1
    new_record['Index'] = last_index
    
    # 3. 写入源文件夹名到"名字"
    source_folder_name = os.path.basename(source_dir.rstrip('\\/'))
    new_record['名字'] = source_folder_name
    
    # 创建临时目录
    ensure_directory_exists(DEFAULT_TEMP_DIR)
    
    # 临时文件路径
    source_name_file = os.path.join(DEFAULT_TEMP_DIR, "SourceName.txt")
    ed2k_list_file = os.path.join(DEFAULT_TEMP_DIR, "Ed2kList.txt")
    size_list_file = os.path.join(DEFAULT_TEMP_DIR, "Ed2kList.size.txt")
    hash_list_file = os.path.join(DEFAULT_TEMP_DIR, "Ed2kList.hash.txt")
    
    # 清空临时文件
    clean_temp_files()
    
    # 准备数据
    source_names = []
    ed2k_links = []
    sizes = []
    hashes = []
    
    # 处理每个文件
    for file_path in all_files:
        file_name = os.path.basename(file_path)
        
        # 添加到源文件名列表
        source_names.append(file_name)
        
        # 移动文件
        moved_file = move_file_with_structure(file_path, write_dir, source_dir, source_folder_name)
        
        if moved_file:
            print(f"已移动文件: {file_name}")
            
            # 生成ED2K链接
            ed2k_link = generate_ed2k_link(moved_file)
            ed2k_links.append(ed2k_link if ed2k_link else "")
            
            # 解析大小和哈希
            if ed2k_link:
                size, filehash = parse_ed2k_link(ed2k_link)
                sizes.append(size if size else "")
                hashes.append(filehash if filehash else "")
            else:
                sizes.append("")
                hashes.append("")
        else:
            ed2k_links.append("")
            sizes.append("")
            hashes.append("")
    
    # 写入临时文件
    with open(source_name_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(source_names))
    
    with open(ed2k_list_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(ed2k_links))
    
    with open(size_list_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(sizes))
    
    with open(hash_list_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(hashes))
    
    # 读取并合并到记录中
    with open(source_name_file, 'r', encoding='utf-8') as f:
        new_record['原文件名'] = f.read().strip()
    
    with open(ed2k_list_file, 'r', encoding='utf-8') as f:
        new_record['标准链接'] = f.read().strip()
    
    with open(size_list_file, 'r', encoding='utf-8') as f:
        new_record['大小'] = f.read().strip()
    
    with open(hash_list_file, 'r', encoding='utf-8') as f:
        new_record['散列'] = f.read().strip()
    
    # 5. 写入引用页、属于、主链接
    new_record['引用页'] = reference_page
    new_record['属于'] = belongs_to
    new_record['主链接'] = main_link
    
    # 添加到Excel
    try:
        new_df = pd.DataFrame([new_record])
        df = pd.concat([df, new_df], ignore_index=True)
        df.to_excel(excel_path, index=False, engine='openpyxl')
        print(f"\n成功添加 1 条记录到Excel (包含 {len(all_files)} 个文件)")
        return True
        
    except Exception as e:
        print(f"保存Excel文件失败: {e}")
        return False

def complex_single_file_write(excel_path, source_dir, write_dir, upload_dir, reference_page, belongs_to, main_link):
    """
    复杂单文件写入功能
    包含复制到Z盘和加密文件处理
    """
    print("\n=== 开始复杂单文件写入 ===")
    
    # 读取Excel文件
    try:
        df = pd.read_excel(excel_path, engine='openpyxl')
    except Exception as e:
        print(f"读取Excel文件失败: {e}")
        return False
    
    # 获取最后一个Index值
    last_index = get_last_index_from_excel(df)
    
    # 获取所有文件
    all_files = get_all_files(source_dir)
    
    if not all_files:
        print("源文件夹中没有找到任何非隐藏文件")
        return False
    
    print(f"找到 {len(all_files)} 个文件")
    
    # 获取源文件夹名（用于子文件夹）
    source_folder_name = os.path.basename(source_dir.rstrip('\\/'))
    
    # 处理每个文件
    new_records = []
    
    for file_path in all_files:
        try:
            # 1. 新开一行
            new_record = {}
            
            # 2. Index字段值
            last_index += 1
            new_record['Index'] = last_index
            
            # 3. 写入文件名
            file_name = os.path.basename(file_path)
            file_name_without_ext = os.path.splitext(file_name)[0]
            
            new_record['名字'] = file_name_without_ext
            new_record['原文件名'] = file_name
            
            # 4. 移动文件到写入目录
            moved_to_write = move_file_with_structure(file_path, write_dir, source_dir, source_folder_name)
            
            if moved_to_write:
                print(f"已移动到写入目录: {file_name}")
                
                # 4. 复制到Z盘（带重试机制）
                z_drive_result = copy_to_z_drive_with_retry(moved_to_write)
                
                corrected_filename = None
                if z_drive_result[0]:
                    print(f"已复制到Z盘: {os.path.basename(z_drive_result[0])}")
                    
                    # 记录矫正文件名
                    if z_drive_result[1]:
                        corrected_filename = z_drive_result[1]
                        new_record['矫正文件名'] = corrected_filename
                    else:
                        new_record['矫正文件名'] = ""
                    
                    # 等待加密文件生成
                    encrypted_filename = wait_for_encrypted_file()
                    
                    if encrypted_filename:
                        new_record['加密文件名'] = encrypted_filename
                        
                        # 移动加密文件到上传目录
                        encrypted_source = None
                        
                        for item in os.listdir(DEFAULT_XYZ_DIR):
                            item_path = os.path.join(DEFAULT_XYZ_DIR, item)
                            if os.path.isfile(item_path) and not is_hidden_file(item):
                                encrypted_source = item_path
                                break
                        
                        if encrypted_source:
                            move_file_with_structure(encrypted_source, upload_dir, DEFAULT_XYZ_DIR, source_folder_name)
                            print(f"已移动加密文件到上传目录")
                    else:
                        new_record['加密文件名'] = ""
                else:
                    new_record['矫正文件名'] = ""
                    new_record['加密文件名'] = ""
                
                # 5. 写入引用页、属于、主链接
                new_record['引用页'] = reference_page
                new_record['属于'] = belongs_to
                new_record['主链接'] = main_link
                
                # 6. 生成ED2K链接
                ed2k_link = generate_ed2k_link(moved_to_write)
                new_record['标准链接'] = ed2k_link
                
                # 7. 解析大小和哈希
                if ed2k_link:
                    size, filehash = parse_ed2k_link(ed2k_link)
                    new_record['大小'] = size
                    new_record['散列'] = filehash
                else:
                    new_record['大小'] = ""
                    new_record['散列'] = ""
                
                new_records.append(new_record)
                print(f"已处理: {file_name} (Index: {last_index})")
                
        except Exception as e:
            print(f"处理文件失败 {file_path}: {e}")
            continue
    
    # 如果有新记录，添加到Excel
    if new_records:
        try:
            new_df = pd.DataFrame(new_records)
            df = pd.concat([df, new_df], ignore_index=True)
            df.to_excel(excel_path, index=False, engine='openpyxl')
            print(f"\n成功添加 {len(new_records)} 条记录到Excel")
            return True
            
        except Exception as e:
            print(f"保存Excel文件失败: {e}")
            return False
    
    return False

def complex_multiple_file_write(excel_path, source_dir, write_dir, upload_dir, reference_page, belongs_to, main_link):
    """
    复杂多文件写入功能
    整个源文件夹作为一个记录，包含复制到Z盘和加密文件处理
    """
    print("\n=== 开始复杂多文件写入 ===")
    
    # 读取Excel文件
    try:
        df = pd.read_excel(excel_path, engine='openpyxl')
    except Exception as e:
        print(f"读取Excel文件失败: {e}")
        return False
    
    # 获取最后一个Index值
    last_index = get_last_index_from_excel(df)
    
    # 获取所有文件
    all_files = get_all_files(source_dir)
    
    if not all_files:
        print("源文件夹中没有找到任何非隐藏文件")
        return False
    
    print(f"找到 {len(all_files)} 个文件")
    
    # 1. 新开一行
    new_record = {}
    
    # 2. Index字段值
    last_index += 1
    new_record['Index'] = last_index
    
    # 3. 写入源文件夹名到"名字"
    source_folder_name = os.path.basename(source_dir.rstrip('\\/'))
    new_record['名字'] = source_folder_name
    
    # 创建临时目录
    ensure_directory_exists(DEFAULT_TEMP_DIR)
    
    # 临时文件路径
    source_name_file = os.path.join(DEFAULT_TEMP_DIR, "SourceName.txt")
    change_name_file = os.path.join(DEFAULT_TEMP_DIR, "ChangeName.txt")
    encrypted_name_file = os.path.join(DEFAULT_TEMP_DIR, "EncryptedName.txt")
    ed2k_list_file = os.path.join(DEFAULT_TEMP_DIR, "Ed2kList.txt")
    size_list_file = os.path.join(DEFAULT_TEMP_DIR, "Ed2kList.size.txt")
    hash_list_file = os.path.join(DEFAULT_TEMP_DIR, "Ed2kList.hash.txt")
    
    # 清空临时文件
    clean_temp_files()
    
    # 准备数据
    source_names = []
    change_names = []
    encrypted_names = []
    ed2k_links = []
    sizes = []
    hashes = []
    
    # 处理每个文件
    for file_path in all_files:
        file_name = os.path.basename(file_path)
        
        # 添加到源文件名列表
        source_names.append(file_name)
        
        try:
            # 移动文件到写入目录
            moved_to_write = move_file_with_structure(file_path, write_dir, source_dir, source_folder_name)
            
            if moved_to_write:
                print(f"已移动到写入目录: {file_name}")
                
                # 复制到Z盘（带重试机制）
                z_drive_result = copy_to_z_drive_with_retry(moved_to_write)
                
                if z_drive_result[0]:
                    print(f"已复制到Z盘: {os.path.basename(z_drive_result[0])}")
                    
                    # 记录矫正文件名
                    if z_drive_result[1]:
                        change_names.append(z_drive_result[1])
                    else:
                        change_names.append(file_name)
                    
                    # 等待加密文件生成
                    encrypted_filename = wait_for_encrypted_file()
                    
                    if encrypted_filename:
                        encrypted_names.append(encrypted_filename)
                        
                        # 移动加密文件到上传目录
                        for item in os.listdir(DEFAULT_XYZ_DIR):
                            item_path = os.path.join(DEFAULT_XYZ_DIR, item)
                            if os.path.isfile(item_path) and not is_hidden_file(item):
                                move_file_with_structure(item_path, upload_dir, DEFAULT_XYZ_DIR, source_folder_name)
                                print(f"已移动加密文件: {item}")
                                break
                    else:
                        encrypted_names.append("")
                else:
                    change_names.append("")
                    encrypted_names.append("")
                
                # 生成ED2K链接
                ed2k_link = generate_ed2k_link(moved_to_write)
                ed2k_links.append(ed2k_link if ed2k_link else "")
                
                # 解析大小和哈希
                if ed2k_link:
                    size, filehash = parse_ed2k_link(ed2k_link)
                    sizes.append(size if size else "")
                    hashes.append(filehash if filehash else "")
                else:
                    sizes.append("")
                    hashes.append("")
                    
            else:
                change_names.append("")
                encrypted_names.append("")
                ed2k_links.append("")
                sizes.append("")
                hashes.append("")
                
        except Exception as e:
            print(f"处理文件失败 {file_path}: {e}")
            change_names.append("")
            encrypted_names.append("")
            ed2k_links.append("")
            sizes.append("")
            hashes.append("")
    
    # 写入临时文件
    with open(source_name_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(source_names))
    
    with open(change_name_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(change_names))
    
    with open(encrypted_name_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(encrypted_names))
    
    with open(ed2k_list_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(ed2k_links))
    
    with open(size_list_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(sizes))
    
    with open(hash_list_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(hashes))
    
    # 读取并合并到记录中
    with open(source_name_file, 'r', encoding='utf-8') as f:
        new_record['原文件名'] = f.read().strip()
    
    with open(change_name_file, 'r', encoding='utf-8') as f:
        new_record['矫正文件名'] = f.read().strip()
    
    with open(encrypted_name_file, 'r', encoding='utf-8') as f:
        new_record['加密文件名'] = f.read().strip()
    
    with open(ed2k_list_file, 'r', encoding='utf-8') as f:
        new_record['标准链接'] = f.read().strip()
    
    with open(size_list_file, 'r', encoding='utf-8') as f:
        new_record['大小'] = f.read().strip()
    
    with open(hash_list_file, 'r', encoding='utf-8') as f:
        new_record['散列'] = f.read().strip()
    
    # 5. 写入引用页、属于、主链接
    new_record['引用页'] = reference_page
    new_record['属于'] = belongs_to
    new_record['主链接'] = main_link
    
    # 添加到Excel
    try:
        new_df = pd.DataFrame([new_record])
        df = pd.concat([df, new_df], ignore_index=True)
        df.to_excel(excel_path, index=False, engine='openpyxl')
        print(f"\n成功添加 1 条记录到Excel (包含 {len(all_files)} 个文件)")
        return True
        
    except Exception as e:
        print(f"保存Excel文件失败: {e}")
        return False

# ==================== 主程序 ====================

def main():
    """主程序"""
    print("=" * 60)
    print("文件管理脚本")
    print("支持单文件/多文件写入Excel，包含ED2K链接生成")
    print("=" * 60)
    
    # 主循环
    while True:
        print("\n" + "=" * 60)
        print("[主菜单]")
        print("1. 单文件写入")
        print("2. 多文件写入")
        print("3. 复杂单文件写入")
        print("4. 复杂多文件写入")
        print("0. 退出程序")
        
        choice = input("\n请选择操作 (0-4): ").strip()
        
        if choice == '0':
            print("\n程序已退出")
            break
        
        # 获取路径配置（每次操作前都要重新询问）
        print("\n[配置路径]")
        excel_path = get_input_with_default("请输入Excel文件位置", DEFAULT_EXCEL_PATH)
        source_dir = get_input_with_default("请输入源文件夹位置", DEFAULT_SOURCE_DIR)
        write_dir = get_input_with_default("请输入写入文件夹位置", DEFAULT_WRITE_DIR)
        upload_dir = get_input_with_default("请输入上传文件夹位置", DEFAULT_UPLOAD_DIR)
        
        # 确保目录存在
        ensure_directory_exists(write_dir)
        ensure_directory_exists(upload_dir)
        ensure_directory_exists(DEFAULT_TEMP_DIR)
        
        # 检查Excel文件是否存在
        if not os.path.exists(excel_path):
            print(f"错误: Excel文件不存在 - {excel_path}")
            continue
        
        # 检查源文件夹是否存在
        if not os.path.exists(source_dir):
            print(f"错误: 源文件夹不存在 - {source_dir}")
            continue
        
        # 询问引用页、属于、主链接的值
        print("\n[输入字段值]")
        reference_page = input("请输入引用页的值 (按回车则为空): ").strip()
        belongs_to = input("请输入属于的值 (按回车则为空): ").strip()
        main_link = input("请输入主链接的值 (按回车则为空): ").strip()
        
        # 根据选择执行相应功能
        if choice == '1':
            # 单文件写入
            success = single_file_write(
                excel_path, source_dir, write_dir,
                reference_page, belongs_to, main_link
            )
            
            if success:
                print("单文件写入完成!")
            else:
                print("单文件写入失败!")
                
        elif choice == '2':
            # 多文件写入
            success = multiple_file_write(
                excel_path, source_dir, write_dir,
                reference_page, belongs_to, main_link
            )
            
            if success:
                print("多文件写入完成!")
            else:
                print("多文件写入失败!")
                
        elif choice == '3':
            # 复杂单文件写入
            success = complex_single_file_write(
                excel_path, source_dir, write_dir, upload_dir,
                reference_page, belongs_to, main_link
            )
            
            if success:
                print("复杂单文件写入完成!")
            else:
                print("复杂单文件写入失败!")
                
        elif choice == '4':
            # 复杂多文件写入
            success = complex_multiple_file_write(
                excel_path, source_dir, write_dir, upload_dir,
                reference_page, belongs_to, main_link
            )
            
            if success:
                print("复杂多文件写入完成!")
            else:
                print("复杂多文件写入失败!")
                
        else:
            print("无效选择，请重新输入!")
        
        # 操作完成后，直接返回主菜单开始新的循环
        print("\n操作完成，返回主菜单...")
        time.sleep(1)  # 暂停1秒，让用户看到结果

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
    except Exception as e:
        print(f"\n程序运行出错: {e}")
    finally:
        input("\n按回车键退出程序...")