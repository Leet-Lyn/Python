# 请帮我写个中文的 Python 脚本，批注也是中文，但是变量参数不要是中文：
# 在脚本开始前询问我 excel 文件位置（默认为：d:\Studios\Attachments\标准.xlsx）、写入文件夹位置（默认为：d:\Studios\Folders\Ins）。
# 重命名即生成 nfo 文件：读取 excel 文件，第一行为表头（字段名）。此后每一行为一条记录。"原文件名"字段值对应着写入文件夹中到每一个文件名字。依次根据每一行到"原文件名"找到写入文件夹中到每一个文件，将其改名为同一行中的“现文件名”。根据“现文件名”生成同名“*.nfo”文件。nfo 文件内写入的内容：UTF-8编码，<?xml version="1.0" encoding="UTF-8" standalone="yes"?><movie>  <title> </title></movie>，将该行中的“名字”字段填入“<title> </title>”内的“ ”。
# 完成后，反复循环。

# 导入模块
import os
import signal
import sys
import pandas as pd

# ==================== 全局配置 ====================
DEFAULT_EXCEL_PATH = r"d:\Studios\Attachments\标准.xlsx"
DEFAULT_WRITE_DIR = r"d:\Studios\Folders\Ins"

_quit_requested = False  # Ctrl+Q 中断标志

# --- 消息常量 ---
MSG_INTERRUPTED = "\n\n用户中断程序，已退出。"
MSG_ERROR = "\n程序运行出错: {}"
MSG_EXIT = "\n按回车键退出..."
MSG_PROMPT_FORMAT = "{} (默认: {}): "
MSG_NFO_CREATE_FAILED = "创建NFO文件失败 {}: {}"
MSG_START_RENAME_NFO = "\n=== 开始重命名并生成NFO文件 ==="
MSG_EXCEL_NOT_EXIST = "错误: Excel文件不存在 - {}"
MSG_WRITE_DIR_NOT_EXIST = "错误: 写入文件夹不存在 - {}"
MSG_READ_EXCEL_FAILED = "读取Excel文件失败: {}"
MSG_MISSING_COLUMNS = "错误: Excel文件中缺少以下必要字段: {}"
MSG_SKIP_SAME_NAME = "跳过第 {} 行: 原文件名和现文件名相同"
MSG_NFO_GENERATED = "已生成NFO文件: {}"
MSG_FILE_NOT_FOUND = "未找到文件: {}"
MSG_MULTIPLE_FOUND = "找到多个同名文件，使用第一个: {}"
MSG_TARGET_EXISTS = "目标文件已存在，跳过重命名: {}"
MSG_RENAMED = "已重命名: {} -> {}"
MSG_RENAME_FAILED = "重命名文件失败 {}: {}"
MSG_ROW_ERROR = "处理第 {} 行时出错: {}"
MSG_PROCESS_DONE = "\n处理完成!"
MSG_SUCCESS_COUNT = "成功处理: {} 个文件"
MSG_RENAME_FAIL_COUNT = "重命名失败: {} 个文件"
MSG_NFO_FAIL_COUNT = "NFO文件生成失败: {} 个文件"
MSG_TITLE = "重命名并生成NFO文件脚本"
MSG_DESC = "功能: 根据Excel文件重命名文件并生成对应的NFO文件"
MSG_EXIT_HINT = "提示: 如需退出程序，请按 Ctrl+C 或在Excel路径输入 'exit' 或 'quit' 后回车"
MSG_CONFIG_PARAMS = "\n[配置参数]"
MSG_PROMPT_EXCEL = "请输入Excel文件位置"
MSG_PROMPT_WRITE_DIR = "请输入写入文件夹位置"
MSG_EXIT_CMD = "程序退出。"
MSG_OP_SUCCESS = "操作成功完成!"
MSG_OP_FAILED = "操作失败或未处理任何文件!"

# ==================== 辅助函数 ====================

def get_input_with_default(prompt_text, default_value):
    """获取带默认值的用户输入"""
    user_input = input(MSG_PROMPT_FORMAT.format(prompt_text, default_value)).strip()
    return user_input if user_input else default_value

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
        # 构建XML字符串
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
        print(MSG_NFO_CREATE_FAILED.format(filepath, e))
        return False

# ==================== 主要功能 ====================

def rename_and_generate_nfo(excel_path, write_dir):
    """
    重命名文件并生成NFO文件
    参数:
        excel_path: Excel文件路径
        write_dir: 写入文件夹路径
    """
    print(MSG_START_RENAME_NFO)

    # 检查Excel文件是否存在
    if not os.path.exists(excel_path):
        print(MSG_EXCEL_NOT_EXIST.format(excel_path))
        return False

    # 检查写入文件夹是否存在
    if not os.path.exists(write_dir):
        print(MSG_WRITE_DIR_NOT_EXIST.format(write_dir))
        return False

    # 读取Excel文件
    try:
        df = pd.read_excel(excel_path, engine='openpyxl')
    except Exception as e:
        print(MSG_READ_EXCEL_FAILED.format(e))
        return False

    # 检查必要的字段是否存在
    required_columns = ["原文件名", "现文件名", "名字"]
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        print(MSG_MISSING_COLUMNS.format(', '.join(missing_columns)))
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
            
            # 转换为字符串并去除空白
            original_filename = str(original_filename).strip()
            new_filename = str(new_filename).strip()
            name_value = str(name_value).strip()

            # 跳过空值（包括 NaN 和空白字符串）
            if (not original_filename or original_filename == 'nan' or
                not new_filename or new_filename == 'nan' or
                not name_value or name_value == 'nan'):
                continue
            
            # 如果原文件名和现文件名相同，跳过重命名
            if original_filename == new_filename:
                print(MSG_SKIP_SAME_NAME.format(index + 1))
                # 仍然生成NFO文件

                # 查找文件
                found_files = find_file_in_directory(write_dir, original_filename)

                if found_files:
                    target_file = found_files[0]

                    # 生成NFO文件
                    nfo_filename = os.path.splitext(original_filename)[0] + ".nfo"
                    nfo_filepath = os.path.join(os.path.dirname(target_file), nfo_filename)

                    if create_nfo_file(nfo_filepath, name_value):
                        print(MSG_NFO_GENERATED.format(nfo_filename))
                        processed_count += 1
                    else:
                        nfo_failures += 1
                else:
                    print(MSG_FILE_NOT_FOUND.format(original_filename))
                continue

            # 查找源文件
            found_files = find_file_in_directory(write_dir, original_filename)

            if not found_files:
                print(MSG_FILE_NOT_FOUND.format(original_filename))
                continue

            if len(found_files) > 1:
                print(MSG_MULTIPLE_FOUND.format(original_filename))

            source_file = found_files[0]

            # 重命名文件
            try:
                # 获取源文件目录
                source_dir = os.path.dirname(source_file)

                # 构建新文件路径
                new_filepath = os.path.join(source_dir, new_filename)

                # 检查新文件是否已存在
                if os.path.exists(new_filepath):
                    print(MSG_TARGET_EXISTS.format(new_filename))
                    target_file = new_filepath
                else:
                    # 重命名文件
                    os.rename(source_file, new_filepath)
                    print(MSG_RENAMED.format(original_filename, new_filename))
                    target_file = new_filepath

                # 生成NFO文件
                nfo_filename = os.path.splitext(new_filename)[0] + ".nfo"
                nfo_filepath = os.path.join(source_dir, nfo_filename)

                if create_nfo_file(nfo_filepath, name_value):
                    print(MSG_NFO_GENERATED.format(nfo_filename))
                    processed_count += 1
                else:
                    nfo_failures += 1

            except Exception as e:
                print(MSG_RENAME_FAILED.format(original_filename, e))
                rename_failures += 1

        except Exception as e:
            print(MSG_ROW_ERROR.format(index + 1, e))
            continue

    # 输出处理结果
    print(MSG_PROCESS_DONE)
    print(MSG_SUCCESS_COUNT.format(processed_count))
    print(MSG_RENAME_FAIL_COUNT.format(rename_failures))
    print(MSG_NFO_FAIL_COUNT.format(nfo_failures))
    
    return processed_count > 0

# ==================== 主程序 ====================

def main():
    """主程序（循环执行，每次结束后自动回到配置输入，无需询问是否继续）"""
    print("=" * 60)
    print(MSG_TITLE)
    print(MSG_DESC)
    print(MSG_EXIT_HINT)
    print("=" * 60)

    while True:
        print("\n" + "=" * 60)
        print(MSG_CONFIG_PARAMS)

        # 获取用户输入
        excel_path = get_input_with_default(MSG_PROMPT_EXCEL, DEFAULT_EXCEL_PATH)
        # 检查退出指令
        if excel_path.lower() in ("exit", "quit"):
            print(MSG_EXIT_CMD)
            break

        write_dir = get_input_with_default(MSG_PROMPT_WRITE_DIR, DEFAULT_WRITE_DIR)
        if write_dir.lower() in ("exit", "quit"):
            print(MSG_EXIT_CMD)
            break

        # 执行主要功能
        success = rename_and_generate_nfo(excel_path, write_dir)

        if success:
            print(MSG_OP_SUCCESS)
        else:
            print(MSG_OP_FAILED)
        # 不询问是否继续，自动进入下一轮循环

# ==================== 程序入口 ====================

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    try:
        main()
    except KeyboardInterrupt:
        print(MSG_INTERRUPTED)
    except Exception as e:
        print(MSG_ERROR.format(e))
    finally:
        input(MSG_EXIT)