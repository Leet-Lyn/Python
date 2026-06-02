# 请帮我写个中文的 Python 脚本，批注也是中文，但是变量参数不要是中文：
# 在脚本开始前让我选择：1. 文件夹写入 excel 并写入数据库；2. 多行 ed2k 链接写入数据库；3. 单文件链接写入数据库；4. 整理数据库；0. 退出。
# 1. 文件夹写入 excel 并写入数据库：
# 询问我 excel 文件位置（默认为：d:\Works\Attachments\标准.xlsx）、源文件夹位置（默认为：d:\Works\Downloads\），写入文件夹位置（默认为：d:\Works\Ins\），上传文件夹位置（默认为：d:\Works\Uploads\）, 删除文件夹位置（默认为：d:\Works\Deletes\）。SizeMD4 数据库文件位置（默认为：e:\Documents\Creations\Scripts\Attachments\Databases\SizeMD4.txt）。
# 读取 excel 文件，第一行为表头（字段名）。此后每一行为一条记录。分别询问我"引用页"、"属于"、"主链接"的值（按回车则为空）。
# 遍历源文件夹内所有文件及子文件夹中的文件，顺序完成。
# 首先计算并生成该文件的 ed2k 链接。我安装了 RHash，位置“d:\\ProApps\\RHash\\rhash.exe”。生成 ed2k 的命令类似：rhash.exe --uppercase --ed2k-link "\\TS-464C\Temps\rustdesk-1.4.3-x86_64.exe"。生成如“ed2k://|file|rustdesk-1.4.3-x86_64.exe|23369352|DF952EEB0438E288409858E6C960E261|h=T7BJKLDRQ7VDCDKOO525FO7YHJCZVKDK|/”的ed2k链接。生成的 ed2k 链接转换成 SizeMD4 值（格式：文件大小|MD4哈希，不需要文件名及其他）。比对 SizeMD4 数据库文件（SizeMD4 数据库文件，每一行为一个文件的 SizeMD4 值（文件大小|MD4哈希））。
# 如果当前文件的 SizeMD4 值在原来 SizeMD4 数据库文件里存在，则将该文件移动到删除文件夹，选择下一个文件。
# 如果当前文件的 SizeMD4 值不在原来 SizeMD4 数据库文件里存在，则添加该文件的 SizeMD4 值到 SizeMD4 数据库文件末尾（另起一行），保存SizeMD4 数据库文件。进行后续操作：
# 将该文件（SizeMD4 值不在原来 SizeMD4 数据库文件里存在的）的信息写入 excel 文件, 每一条记录新开一行。1. "Index"字段值为上一行 "Index"字段值+1（如上一行为空或为表头，则"Index"字段值为 1）。2. 将源文件夹内文件名写入"名字"与"原文件名"字段值。3. 将该文件移动到写入文件夹下的子文件夹（子文件夹名字为源文件夹名，保持原来文件夹结构），并移动到"z:\"中，如果无法完成写入"z:\"中，则重命名原文件（从后删除1个字符（不包括扩展名）），再次尝试将原文件向目标文件夹移动。反复循环，直至能将原文件向目标文件夹移动。如果有重命名过文件，将修改过的文件名写入"矫正文件名"字段值中。写入"z:\"后，系统会自动生成一个对应文件（自动加密的）。读取"d:\Xyz\"新生成的文件名，将其文件名（无扩展名）写入"加密文件名"字段值。将"d:\Xyz\"新生成的文件移动到上传文件夹下的子文件夹（子文件夹名字为源文件夹名，保持原来文件夹结构，在"d:\Xyz\"中不保留）。5. 将原来询问我的"引用页"、"属于"、"主链接"的值写入"引用页"、"属于"、"主链接"字段值。6. 将该文件的 ed2k 链接，写入"标准链接"字段值。7. 通过"标准链接"字段值，分别生成"大小"、"散列"字段值。大小请转成 B、KB、MB、GB 形式，并精确到小数点后 4 位，hash 转全部大写。选择下一个文件。
# 直至源文件夹内所有文件及子文件夹中的文件都处理好结束。最后整理哪些文件 SizeMD4 值原数据库存在，移动到删除文件夹里。并将这些文件列表打印在屏幕上并复制到剪贴板上去。
# 2. 多行 ed2k 链接写入数据库：
# 询问我SizeMD4 数据库文件位置（默认为：e:\Documents\Creations\Scripts\Attachments\Databases\SizeMD4.txt）。读取剪贴板数据，其为多行 ed2k 链接（每行一个 ed2k 链接），顺序读取每一行 ed2k 链接，转换成 SizeMD4 值（格式：文件大小|MD4哈希，不需要文件名及其他）。比对 SizeMD4 数据库文件（SizeMD4 数据库文件，每一行为一个文件的 SizeMD4 值（文件大小|MD4哈希））。
# 如果当前 SizeMD4 值在原来 SizeMD4 数据库文件里存在，报告我。
# 如果当前 SizeMD4 值不在原来 SizeMD4 数据库文件里存在，则添加该 SizeMD4 值到 SizeMD4 数据库文件末尾（另起一行），保存SizeMD4 数据库文件。
# 最后整理哪些 ed2k 链接的 SizeMD4 值原数据库存在。并将这些文件列表打印在屏幕上并复制到剪贴板上去。
# 3. 单文件链接写入数据库：
# 询问我文件链接（默认为：d:\Works\Attachments\标准.txt），SizeMD4 数据库文件位置（默认为：e:\Documents\Creations\Scripts\Attachments\Databases\SizeMD4.txt）。通过 rhash.exe --uppercase --ed2k-link 命令生成 ed2k 链接，转换成 SizeMD4 值（格式：文件大小|MD4哈希，不需要文件名及其他）。比对 SizeMD4 数据库文件（SizeMD4 数据库文件，每一行为一个文件的 SizeMD4 值（文件大小|MD4哈希））。
# 如果当前文件 SizeMD4 值在原来 SizeMD4 数据库文件里存在，报告我。
# 如果当前文件 SizeMD4 值不在原来 SizeMD4 数据库文件里存在，则添加该 SizeMD4 值到 SizeMD4 数据库文件末尾（另起一行），保存SizeMD4 数据库文件。
# 最后告诉我该文件 ed2k 链接的 SizeMD4 值原数据库是否存在。
# 4. 整理数据库：
# 询问我 SizeMD4 数据库文件位置（默认为：e:\Documents\Creations\Scripts\Attachments\Databases\SizeMD4.txt）。对 SizeMD4 数据库，先备份，再对文件里的 SizeMD4 值（字符串）从小到大排序。
# 完成后，反复循环至最开始。

# 导入模块

# -*- coding: utf-8 -*-
"""
文件处理与SizeMD4数据库管理工具
功能菜单：
1. 文件夹写入Excel并写入数据库
2. 多行ed2k链接写入数据库
3. 单文件链接写入数据库
4. 整理数据库（排序去重）
0. 退出
"""

import os
import shutil
import time
import urllib.parse
import subprocess
import pandas as pd
import sys
import io
from datetime import datetime

# -------------------- 剪贴板支持 --------------------
try:
    import pyperclip
    def copy_to_clipboard(text):
        pyperclip.copy(text)
        print("已复制到剪贴板。")
except ImportError:
    def copy_to_clipboard(text):
        # 使用Windows的clip命令
        try:
            process = subprocess.Popen(['clip'], stdin=subprocess.PIPE, text=True)
            process.communicate(input=text)
            print("已复制到剪贴板。")
        except Exception as e:
            print(f"复制到剪贴板失败: {e}")

def get_clipboard_text():
    """获取剪贴板文本，优先pyperclip，其次clip"""
    try:
        import pyperclip
        return pyperclip.paste()
    except ImportError:
        try:
            result = subprocess.run(['powershell', '-command', 'Get-Clipboard'], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.rstrip('\n')
        except:
            pass
        print("无法读取剪贴板，请安装pyperclip库或在Windows下运行。")
        return ""

# ==================== 全局配置 ====================
DEFAULT_EXCEL_PATH = r"d:\Works\Attachments\标准.xlsx"
DEFAULT_SOURCE_DIR = r"d:\Works\Downloads"
DEFAULT_WRITE_DIR = r"d:\Works\Ins"
DEFAULT_UPLOAD_DIR = r"d:\Works\Uploads"
DEFAULT_DELETE_DIR = r"d:\Works\Deletes"
DEFAULT_SIZE_MD4_DB = r"e:\Documents\Creations\Scripts\Attachments\Databases\SizeMD4.txt"
DEFAULT_TEMP_DIR = r"e:\Documents\Creations\Scripts\Attachments\Python"
DEFAULT_RHASH_PATH = r"d:\ProApps\RHash\rhash.exe"
DEFAULT_XYZ_DIR = r"d:\Xyz"
Z_DRIVE_PATH = r"z:"

# 隐藏文件过滤规则
HIDDEN_FILE_PATTERNS = [
    'desktop.ini', 'descript.ion', '.encfs6.xml', 'Thumbs.db',
    '.DS_Store', '._*'
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
                capture_output=True, text=True, encoding='utf-8'
            )
            if result.returncode == 0:
                return result.stdout.strip()
        return ""
    except Exception as e:
        print(f"生成ED2K链接失败 {file_path}: {e}")
        return ""

def parse_ed2k_link(ed2k_link):
    """解析ED2K链接，提取格式化后的大小和哈希值"""
    if not ed2k_link or not ed2k_link.startswith("ed2k://|file|"):
        return "", ""
    try:
        decoded_link = urllib.parse.unquote(ed2k_link)
        parts = decoded_link.split('|')
        if len(parts) >= 5:
            size_str = parts[3]
            filehash = parts[4].upper()
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

def extract_size_md4(ed2k_link):
    """
    从ED2K链接中提取 SizeMD4 字符串（格式：文件大小|MD4哈希）
    文件大小为原始字节数，MD4为大写
    """
    if not ed2k_link or not ed2k_link.startswith("ed2k://|file|"):
        return ""
    try:
        decoded_link = urllib.parse.unquote(ed2k_link)
        parts = decoded_link.split('|')
        if len(parts) >= 5:
            size_str = parts[3]
            filehash = parts[4].upper()
            size_bytes = int(size_str)
            return f"{size_bytes}|{filehash}"
        return ""
    except Exception as e:
        print(f"提取SizeMD4失败: {e}")
        return ""

def load_size_md4_database(db_path):
    """从TXT文件读取所有SizeMD4值，返回集合"""
    if not os.path.exists(db_path):
        return set()
    try:
        with open(db_path, 'r', encoding='utf-8') as f:
            lines = f.read().splitlines()
            return set(line.strip() for line in lines if line.strip())
    except Exception as e:
        print(f"读取SizeMD4数据库失败: {e}")
        return set()

def add_to_size_md4_database(db_path, size_md4):
    """向SizeMD4数据库文件末尾追加一行记录"""
    try:
        with open(db_path, 'a', encoding='utf-8') as f:
            f.write(size_md4 + '\n')
    except Exception as e:
        print(f"写入SizeMD4数据库失败: {e}")

def safe_move_file(src_path, dst_path, max_retries=10, retry_delay=1.0):
    """
    安全移动文件（带重试机制），解决文件被占用问题
    """
    for attempt in range(max_retries):
        try:
            dst_dir = os.path.dirname(dst_path)
            ensure_directory_exists(dst_dir)
            if os.path.exists(dst_path):
                try:
                    os.remove(dst_path)
                except:
                    pass
            shutil.move(src_path, dst_path)
            print(f"移动成功: {os.path.basename(src_path)} -> {dst_path}")
            return True
        except PermissionError as e:
            print(f"文件被占用，重试 {attempt+1}/{max_retries}: {e}")
            time.sleep(retry_delay)
        except Exception as e:
            print(f"移动文件失败（非权限）: {e}")
            return False
    print(f"移动失败，已达最大重试次数: {src_path}")
    return False

def wait_for_file_ready(file_path, timeout_seconds=30, check_interval=0.5):
    """等待文件完全释放（可读写）"""
    start_time = time.time()
    while time.time() - start_time < timeout_seconds:
        if not os.path.exists(file_path):
            time.sleep(check_interval)
            continue
        try:
            with open(file_path, 'r+b') as f:
                pass
            return True
        except (PermissionError, OSError):
            time.sleep(check_interval)
    print(f"文件就绪等待超时: {file_path}")
    return False

def copy_to_z_drive_with_retry(source_file, z_drive_path=Z_DRIVE_PATH):
    """
    复制文件到Z盘，如果失败则重试（缩短文件名）
    返回：(成功复制到的路径, 修改后的文件名或None)
    """
    original_file_name = os.path.basename(source_file)
    file_stem, file_extension = os.path.splitext(original_file_name)
    current_stem = file_stem
    attempt_count = 0
    max_attempts = 50
    while attempt_count < max_attempts:
        try:
            target_file_name = f"{current_stem}{file_extension}"
            target_path = os.path.join(z_drive_path, target_file_name)
            shutil.copy2(source_file, target_path)
            if current_stem != file_stem:
                return target_path, target_file_name
            else:
                return target_path, None
        except Exception as e:
            attempt_count += 1
            if len(current_stem) > 1:
                current_stem = current_stem[:-1]
            else:
                print(f"无法继续缩短文件名: {original_file_name}")
                return None, None
    print(f"达到最大尝试次数 {max_attempts}: {original_file_name}")
    return None, None

def wait_for_encrypted_file(xyz_dir=DEFAULT_XYZ_DIR, timeout_seconds=60):
    """等待加密文件生成并返回其完整路径"""
    start_time = time.time()
    check_interval = 1.0
    while time.time() - start_time < timeout_seconds:
        if os.path.exists(xyz_dir):
            files = [f for f in os.listdir(xyz_dir) 
                     if os.path.isfile(os.path.join(xyz_dir, f)) 
                     and not is_hidden_file(f)]
            if files:
                full_paths = [os.path.join(xyz_dir, f) for f in files]
                newest_file = max(full_paths, key=os.path.getmtime)
                if wait_for_file_ready(newest_file, timeout_seconds=5):
                    return newest_file
        time.sleep(check_interval)
    print(f"等待加密文件超时 ({timeout_seconds}秒)")
    return None

def move_file_with_structure(source_file, target_base_dir, source_base_dir, subfolder_name=None):
    """移动文件，保持文件夹结构（带重试）"""
    try:
        if source_base_dir in source_file:
            relative_path = os.path.relpath(source_file, source_base_dir)
        else:
            relative_path = os.path.basename(source_file)
        if subfolder_name:
            target_dir = os.path.join(target_base_dir, subfolder_name, os.path.dirname(relative_path))
        else:
            target_dir = os.path.join(target_base_dir, os.path.dirname(relative_path))
        ensure_directory_exists(target_dir)
        target_file = os.path.join(target_dir, os.path.basename(source_file))
        if safe_move_file(source_file, target_file):
            return target_file
        else:
            return None
    except Exception as e:
        print(f"移动文件失败 {source_file}: {e}")
        return None

def get_last_index_from_excel(df):
    """从DataFrame中获取最后一个Index值"""
    if 'Index' in df.columns and not df.empty:
        index_values = df['Index'].dropna()
        if not index_values.empty:
            try:
                return int(index_values.max())
            except:
                return 0
    return 0

# ==================== 功能1：文件夹处理 ====================
def process_folder_to_excel_and_db(excel_path, source_dir, write_dir, upload_dir, delete_dir, size_md4_db_path,
                                   reference_page, belongs_to, main_link):
    """
    处理文件夹中的所有文件：
    - 比对SizeMD4数据库，重复则移至删除文件夹
    - 新文件写入Excel，移动至写入目录，复制到Z盘，处理加密文件，记录信息
    返回：(处理是否成功, 被移动的重复文件路径列表)
    """
    print("\n=== 开始文件夹处理 ===")
    # 读取 Excel
    try:
        df = pd.read_excel(excel_path, engine='openpyxl')
    except Exception as e:
        print(f"读取Excel文件失败: {e}")
        return False, []

    # 加载 SizeMD4 数据库
    size_md4_set = load_size_md4_database(size_md4_db_path)
    print(f"已加载 {len(size_md4_set)} 条 SizeMD4 记录")

    last_index = get_last_index_from_excel(df)
    all_files = get_all_files(source_dir)
    if not all_files:
        print("源文件夹中没有找到任何非隐藏文件")
        return True, []

    source_folder_name = os.path.basename(source_dir.rstrip('\\/'))
    new_records = []
    duplicated_files = []  # 记录被移动的重复文件路径

    for file_path in all_files:
        try:
            # 生成ED2K链接并提取 SizeMD4
            ed2k_for_check = generate_ed2k_link(file_path)
            if not ed2k_for_check:
                print(f"无法生成ED2K链接，跳过文件: {file_path}")
                continue
            size_md4 = extract_size_md4(ed2k_for_check)
            if not size_md4:
                print(f"无法提取SizeMD4，跳过文件: {file_path}")
                continue

            # 检查是否已存在于数据库
            if size_md4 in size_md4_set:
                print(f"SizeMD4 已存在，将文件移动到删除文件夹: {os.path.basename(file_path)}")
                target_delete_path = os.path.join(delete_dir, os.path.basename(file_path))
                if safe_move_file(file_path, target_delete_path):
                    duplicated_files.append(target_delete_path)
                    print(f"已移动到: {target_delete_path}")
                else:
                    print(f"移动失败，保留在源位置: {file_path}")
                    duplicated_files.append(file_path)  # 移动失败也记录原路径
                continue  # 跳过后续处理

            # SizeMD4 不存在，先加入数据库
            add_to_size_md4_database(size_md4_db_path, size_md4)
            size_md4_set.add(size_md4)
            print(f"SizeMD4 已加入数据库: {size_md4}")

            # 开始处理新记录
            new_record = {}
            last_index += 1
            new_record['Index'] = last_index

            file_name = os.path.basename(file_path)
            file_name_without_ext = os.path.splitext(file_name)[0]
            new_record['名字'] = file_name_without_ext
            new_record['原文件名'] = file_name

            # 移动文件到写入目录（保持结构）
            moved_to_write = move_file_with_structure(file_path, write_dir, source_dir, source_folder_name)
            if not moved_to_write:
                print(f"移动到写入目录失败，跳过: {file_name}")
                continue

            # 复制到Z盘（带重命名重试）
            z_drive_result = copy_to_z_drive_with_retry(moved_to_write)
            corrected_filename = None
            if z_drive_result[0]:
                print(f"已复制到Z盘: {os.path.basename(z_drive_result[0])}")
                if z_drive_result[1]:
                    corrected_filename = z_drive_result[1]
                    new_record['矫正文件名'] = corrected_filename
                else:
                    new_record['矫正文件名'] = ""

                # 等待加密文件生成并解锁
                encrypted_file_path = wait_for_encrypted_file()
                if encrypted_file_path:
                    encrypted_filename = os.path.splitext(os.path.basename(encrypted_file_path))[0]
                    new_record['加密文件名'] = encrypted_filename

                    # 移动加密文件到上传目录
                    upload_target_dir = os.path.join(upload_dir, source_folder_name)
                    ensure_directory_exists(upload_target_dir)
                    target_encrypted_path = os.path.join(upload_target_dir, os.path.basename(encrypted_file_path))
                    if safe_move_file(encrypted_file_path, target_encrypted_path):
                        print(f"已移动加密文件到上传目录: {os.path.basename(encrypted_file_path)}")
                    else:
                        print("移动加密文件失败")
                else:
                    new_record['加密文件名'] = ""
            else:
                new_record['矫正文件名'] = ""
                new_record['加密文件名'] = ""

            # 填写固定字段
            new_record['引用页'] = reference_page
            new_record['属于'] = belongs_to
            new_record['主链接'] = main_link

            # 重新生成ED2K链接（基于移动后的位置）
            ed2k_link = generate_ed2k_link(moved_to_write)
            new_record['标准链接'] = ed2k_link
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

    # 保存 Excel
    if new_records:
        try:
            new_df = pd.DataFrame(new_records)
            df = pd.concat([df, new_df], ignore_index=True)
            df.to_excel(excel_path, index=False, engine='openpyxl')
            print(f"\n成功添加 {len(new_records)} 条记录到Excel")
        except Exception as e:
            print(f"保存Excel文件失败: {e}")
            return False, duplicated_files
    else:
        print("没有新记录需要写入Excel")

    return True, duplicated_files


# ==================== 功能2：多行ed2k链接入库 ====================
def process_ed2k_links_from_clipboard(size_md4_db_path):
    """
    从剪贴板读取多行ed2k链接，提取SizeMD4并更新数据库。
    打印并复制已存在的链接/SizeMD4列表。
    """
    print("\n=== 多行ed2k链接写入数据库 ===")
    clipboard_text = get_clipboard_text()
    if not clipboard_text.strip():
        print("剪贴板为空，无法处理。")
        return

    lines = [line.strip() for line in clipboard_text.splitlines() if line.strip()]
    if not lines:
        print("剪贴板中没有有效行。")
        return

    size_md4_set = load_size_md4_database(size_md4_db_path)
    print(f"已加载 {len(size_md4_set)} 条 SizeMD4 记录")

    existed_links = []   # 记录已存在的SizeMD4及对应链接
    new_count = 0

    for line in lines:
        # 提取ed2k链接（假设每行就是一个完整链接，或者包含在文本中，这里简单按行处理）
        ed2k_link = line
        if not ed2k_link.startswith("ed2k://|file|"):
            print(f"跳过非ed2k链接行: {line}")
            continue

        size_md4 = extract_size_md4(ed2k_link)
        if not size_md4:
            print(f"无法提取SizeMD4: {line}")
            continue

        if size_md4 in size_md4_set:
            existed_links.append(ed2k_link)   # 或者只记录size_md4
            print(f"SizeMD4已存在: {size_md4}")
        else:
            add_to_size_md4_database(size_md4_db_path, size_md4)
            size_md4_set.add(size_md4)
            new_count += 1
            print(f"已添加新SizeMD4: {size_md4}")

    print(f"\n处理完成：新增 {new_count} 条，已存在 {len(existed_links)} 条。")

    if existed_links:
        print("\n===== 已存在的ed2k链接列表 =====")
        list_text = "\n".join(existed_links)
        print(list_text)
        copy_to_clipboard(list_text)
    else:
        print("没有重复的链接。")

# ==================== 功能3：单文件链接入库 ====================
def process_single_file_link(file_path, size_md4_db_path):
    """
    对单个本地文件生成ed2k链接，提取SizeMD4，更新数据库并报告是否存在。
    """
    print(f"\n=== 处理单个文件: {file_path} ===")
    if not os.path.exists(file_path):
        print(f"错误：文件不存在 - {file_path}")
        return

    ed2k_link = generate_ed2k_link(file_path)
    if not ed2k_link:
        print("无法生成ed2k链接。")
        return
    print(f"生成的ed2k链接: {ed2k_link}")

    size_md4 = extract_size_md4(ed2k_link)
    if not size_md4:
        print("无法提取SizeMD4。")
        return

    size_md4_set = load_size_md4_database(size_md4_db_path)
    if size_md4 in size_md4_set:
        print(f"该文件的SizeMD4已存在于数据库中: {size_md4}")
        print("文件未新增入数据库。")
    else:
        add_to_size_md4_database(size_md4_db_path, size_md4)
        print(f"该文件的SizeMD4已添加到数据库: {size_md4}")
    print(f"SizeMD4值: {size_md4}")


# ==================== 功能4：整理数据库（排序去重） ====================
def sort_and_dedup_size_md4_db(db_path):
    """
    对SizeMD4数据库文件进行排序和去重，并创建备份。
    """
    print(f"\n=== 整理SizeMD4数据库 ===")
    if not os.path.exists(db_path):
        print(f"数据库文件不存在: {db_path}")
        return

    # 备份原文件
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = db_path + f".bak_{timestamp}"
    try:
        shutil.copy2(db_path, backup_path)
        print(f"已创建备份: {backup_path}")
    except Exception as e:
        print(f"备份失败: {e}")
        return

    # 读取所有行，去空，去重，排序（字符串排序）
    try:
        with open(db_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
        original_count = len(lines)
        unique_sorted = sorted(set(lines))  # set去重，sorted字符串排序
        new_count = len(unique_sorted)
        
        # 写回原文件
        with open(db_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(unique_sorted) + '\n')
        
        print(f"整理完成。")
        print(f"原始记录数: {original_count}")
        print(f"去重后记录数: {new_count}")
        print(f"已按字符串升序排列。")
    except Exception as e:
        print(f"整理过程中出错: {e}")
        # 失败时尝试恢复备份
        try:
            shutil.copy2(backup_path, db_path)
            print("已从备份恢复原文件。")
        except:
            pass


# ==================== 主菜单 ====================
def main():
    print("=" * 60)
    print("文件处理与SizeMD4数据库管理工具")
    print("=" * 60)

    while True:
        print("\n请选择功能：")
        print("1. 文件夹写入Excel并写入数据库")
        print("2. 多行ed2k链接写入数据库")
        print("3. 单文件链接写入数据库")
        print("4. 整理数据库（排序去重）")
        print("0. 退出")
        choice = input("请输入选项 (0-4): ").strip()

        if choice == '1':
            # 获取各项路径
            excel_path = get_input_with_default("Excel文件位置", DEFAULT_EXCEL_PATH)
            source_dir = get_input_with_default("源文件夹位置（不建议“d:\\Works\\Ins\\”、“d:\\Works\\Uploads\\”。）", DEFAULT_SOURCE_DIR)
            write_dir = get_input_with_default("写入文件夹位置", DEFAULT_WRITE_DIR)
            upload_dir = get_input_with_default("上传文件夹位置", DEFAULT_UPLOAD_DIR)
            delete_dir = get_input_with_default("删除文件夹位置", DEFAULT_DELETE_DIR)
            size_md4_db_path = get_input_with_default("SizeMD4数据库文件位置", DEFAULT_SIZE_MD4_DB)

            # 确保必要的目录存在
            ensure_directory_exists(write_dir)
            ensure_directory_exists(upload_dir)
            ensure_directory_exists(delete_dir)
            ensure_directory_exists(os.path.dirname(size_md4_db_path))

            # 检查Excel和源文件夹是否存在
            if not os.path.exists(excel_path):
                print(f"错误: Excel文件不存在 - {excel_path}，返回主菜单。")
                continue
            if not os.path.exists(source_dir):
                print(f"错误: 源文件夹不存在 - {source_dir}，返回主菜单。")
                continue

            # 询问固定字段
            print("\n请输入以下字段值（直接回车则为空）：")
            reference_page = input("引用页: ").strip()
            belongs_to = input("属于: ").strip()
            main_link = input("主链接: ").strip()

            # 执行处理
            success, duplicated_files = process_folder_to_excel_and_db(
                excel_path, source_dir, write_dir, upload_dir, delete_dir, size_md4_db_path,
                reference_page, belongs_to, main_link
            )

            if success:
                print("\n文件夹处理完成！")
            else:
                print("\n文件夹处理过程中出现错误，请检查日志。")

            # 汇总重复文件
            if duplicated_files:
                print("\n===== 以下文件因SizeMD4重复被移至删除文件夹 =====")
                dup_list = "\n".join(duplicated_files)
                print(dup_list)
                copy_to_clipboard(dup_list)
            else:
                print("没有重复文件。")

        elif choice == '2':
            size_md4_db_path = get_input_with_default("SizeMD4数据库文件位置", DEFAULT_SIZE_MD4_DB)
            ensure_directory_exists(os.path.dirname(size_md4_db_path))
            process_ed2k_links_from_clipboard(size_md4_db_path)

        elif choice == '3':
            file_path = get_input_with_default("请输入文件路径（或本地文件链接）", r"d:\Works\Attachments\标准.txt")
            size_md4_db_path = get_input_with_default("SizeMD4数据库文件位置", DEFAULT_SIZE_MD4_DB)
            ensure_directory_exists(os.path.dirname(size_md4_db_path))
            process_single_file_link(file_path, size_md4_db_path)

        elif choice == '4':
            size_md4_db_path = get_input_with_default("SizeMD4数据库文件位置", DEFAULT_SIZE_MD4_DB)
            sort_and_dedup_size_md4_db(size_md4_db_path)

        elif choice == '0':
            print("程序退出。")
            break
        else:
            print("无效选项，请重新输入。")

        # 返回菜单前暂停一下
        input("\n按回车键继续...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n用户中断程序，已退出。")
    except Exception as e:
        print(f"\n程序运行出错: {e}")
    finally:
        input("\n按回车键退出...")