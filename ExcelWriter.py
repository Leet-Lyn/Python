# 请帮我写个中文的 Python 脚本，批注也是中文，但是变量参数不要是中文：
# 在脚本开始前询问我 excel 文件位置（默认为：d:\Works\Attachments\标准.xlsx）、源文件夹位置（默认为：d:\Works\Downloads\），写入文件夹位置（默认为：d:\Works\Ins\），上传文件夹位置（默认为：d:\Works\Uploads\）。
# 读取 excel 文件，第一行为表头（字段名）。此后每一行为一条记录。分别询问我"引用页"、"属于"、"主链接"的值（按回车则为空）。遍历源文件夹内所有文件及子文件夹中的文件，顺序完成。1. 每一条记录新开一行。2. "Index"字段值为上一行 "Index"字段值+1（如上一行为空或为表头，则"Index"字段值为 1）。3. 将源文件夹内文件名写入"名字"与"原文件名"字段值。4. 将该文件移动到写入文件夹下的子文件夹（子文件夹名字为源文件夹名，保持原来文件夹结构），并移动到"z:\"中，如果无法完成写入"z:\"中，则重命名原文件（从后删除1个字符（不包括扩展名）），再次尝试将原文件向目标文件夹移动。反复循环，直至能将原文件向目标文件夹移动。如果有重命名过文件，将修改过的文件名写入"矫正文件名"字段值中。写入"z:\"后，系统会自动生成一个对应文件（自动加密的）。读取"d:\Xyz\"新生成的文件名，将其文件名（无扩展名）写入"加密文件名"字段值。将"d:\Xyz\"新生成的文件移动到上传文件夹下的子文件夹（子文件夹名字为源文件夹名，保持原来文件夹结构，在"d:\Xyz\"中不保留）。5. 将原来询问我的"引用页"、"属于"、"主链接"的值写入"引用页"、"属于"、"主链接"字段值。6. 计算并生成该文件的 Ed2K 链接。生成的 ed2k 链接，写入"标准链接"字段值。7. 通过"标准链接"字段值，分别生成"大小"、"散列"字段值。大小请转成 B、KB、MB、GB 形式，并精确到小数点后 4 位，hash 转全部大写。
# 完成后，反复循环。

# 导入模块
# -*- coding: utf-8 -*-
"""
文件管理脚本 - 复杂单文件写入版
功能：将源文件夹中的每个文件移动到写入文件夹并复制到Z盘，等待加密文件生成后移动到上传文件夹，
      同时生成ED2K链接及大小、哈希，记录到Excel中。
支持反复循环，每次可更换路径。
"""

import os
import shutil
import time
import urllib.parse
import subprocess
import pandas as pd

# ==================== 全局配置 ====================
DEFAULT_EXCEL_PATH = r"d:\Works\Attachments\标准.xlsx"
DEFAULT_SOURCE_DIR = r"d:\Works\Downloads"
DEFAULT_WRITE_DIR = r"d:\Works\Ins"
DEFAULT_UPLOAD_DIR = r"d:\Works\Uploads"
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
    """解析ED2K链接，提取文件大小和哈希值"""
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

def complex_single_file_write(excel_path, source_dir, write_dir, upload_dir,
                              reference_page, belongs_to, main_link):
    """
    复杂单文件写入（核心功能）
    处理源文件夹中所有非隐藏文件，逐个生成Excel记录
    """
    print("\n=== 开始复杂单文件写入 ===")
    try:
        df = pd.read_excel(excel_path, engine='openpyxl')
    except Exception as e:
        print(f"读取Excel文件失败: {e}")
        return False

    last_index = get_last_index_from_excel(df)
    all_files = get_all_files(source_dir)
    if not all_files:
        print("源文件夹中没有找到任何非隐藏文件")
        return False

    source_folder_name = os.path.basename(source_dir.rstrip('\\/'))
    new_records = []

    for file_path in all_files:
        try:
            new_record = {}
            last_index += 1
            new_record['Index'] = last_index

            file_name = os.path.basename(file_path)
            file_name_without_ext = os.path.splitext(file_name)[0]
            new_record['名字'] = file_name_without_ext
            new_record['原文件名'] = file_name

            # 移动文件到写入目录
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

            # 生成ED2K链接并解析
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

# ==================== 主程序 ====================
def main():
    """主循环：反复询问路径并执行复杂单文件写入"""
    print("=" * 60)
    print("复杂单文件写入工具（支持反复循环）")
    print("每次执行完一轮后，可重新设置路径开始新一轮。")
    print("按 Ctrl+C 可随时退出程序。")
    print("=" * 60)

    loop_count = 0
    while True:
        loop_count += 1
        print(f"\n{'='*60}")
        print(f"第 {loop_count} 轮处理")
        print("请输入以下路径（直接回车使用默认值）：")

        # 获取四个路径
        excel_path = get_input_with_default("Excel文件位置", DEFAULT_EXCEL_PATH)
        source_dir = get_input_with_default("源文件夹位置", DEFAULT_SOURCE_DIR)
        write_dir = get_input_with_default("写入文件夹位置", DEFAULT_WRITE_DIR)
        upload_dir = get_input_with_default("上传文件夹位置", DEFAULT_UPLOAD_DIR)

        # 确保必要的目录存在（写入目录和上传目录）
        ensure_directory_exists(write_dir)
        ensure_directory_exists(upload_dir)

        # 检查Excel和源文件夹是否存在
        if not os.path.exists(excel_path):
            print(f"错误: Excel文件不存在 - {excel_path}，请重新输入路径。")
            continue
        if not os.path.exists(source_dir):
            print(f"错误: 源文件夹不存在 - {source_dir}，请重新输入路径。")
            continue

        # 询问三个固定字段值
        print("\n请输入以下字段值（直接回车则为空）：")
        reference_page = input("引用页: ").strip()
        belongs_to = input("属于: ").strip()
        main_link = input("主链接: ").strip()

        # 执行处理
        success = complex_single_file_write(
            excel_path, source_dir, write_dir, upload_dir,
            reference_page, belongs_to, main_link
        )
        if success:
            print("\n本轮处理完成！")
        else:
            print("\n本轮处理失败，请检查日志。")

        # 直接进入下一轮（无需选择，循环继续）
        print("\n准备开始下一轮...")
        time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n用户中断程序，已退出。")
    except Exception as e:
        print(f"\n程序运行出错: {e}")
    finally:
        input("\n按回车键退出...")