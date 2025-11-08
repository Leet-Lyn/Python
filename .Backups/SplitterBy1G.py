# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件夹位置（默认为“d:\Works\In\”）与目标文件夹位置（默认为“d:\Works\Out\”）。
# 遍历源文件夹位置中所有文件。
# 对每一个文件进行分割，大小为 1 GB，放在目标文件夹中以文件名命名的子文件夹。如文件小于 1 GB 则将该文件复制到目标文件夹中以文件名命名的子文件夹。

# 导入模块
import os
import shutil
import zlib

def calculate_crc(file_path):
    """
    计算文件的 CRC32 校验和
    :param file_path: 文件路径
    :return: CRC32 校验值（十六进制字符串）
    """
    crc = 0
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                crc = zlib.crc32(chunk, crc)
        return f"{crc & 0xFFFFFFFF:08x}"
    except Exception as e:
        print(f"无法计算文件 {file_path} 的 CRC32 校验和: {e}")
        return None

def split_file(source_file, target_dir, chunk_size=1073741824):
    """
    分割大文件
    :param source_file: 源文件路径
    :param target_dir: 目标文件夹路径
    :param chunk_size: 分割块大小（字节，默认为1 GB）
    """
    try:
        with open(source_file, 'rb') as f:
            chunk_num = 1
            while chunk := f.read(chunk_size):
                chunk_filename = f"{os.path.basename(source_file)}.{chunk_num:03d}"
                chunk_path = os.path.join(target_dir, chunk_filename)
                with open(chunk_path, 'wb') as chunk_file:
                    chunk_file.write(chunk)
                print(f"已生成分割文件: {chunk_filename}")
                chunk_num += 1
    except Exception as e:
        print(f"分割文件 {source_file} 时发生错误: {e}")

def process_files(source_dir, target_dir):
    """
    遍历源文件夹中的所有文件并处理
    :param source_dir: 源文件夹路径
    :param target_dir: 目标文件夹路径
    """
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    chunk_size = 1073741824  # 1 GB

    for filename in os.listdir(source_dir):
        source_file_path = os.path.join(source_dir, filename)
        if not os.path.isfile(source_file_path):
            print(f"跳过非文件: {source_file_path}")
            continue

        file_size = os.path.getsize(source_file_path)
        file_target_dir = os.path.join(target_dir, os.path.splitext(filename)[0])
        os.makedirs(file_target_dir, exist_ok=True)

        if file_size < 1 * chunk_size:
            # 文件小于 1 GB，直接复制
            try:
                shutil.copy2(source_file_path, file_target_dir)
                print(f"文件 {filename} 小于 1 GB，已复制到 {file_target_dir}")
            except Exception as e:
                print(f"复制文件 {filename} 时出错: {e}")
        else:
            # 文件大于等于 1 GB，进行分割
            print(f"开始分割大文件: {filename}")
            split_file(source_file_path, file_target_dir, chunk_size)

        # 生成 CRC 校验文件
        crc = calculate_crc(source_file_path)
        if crc:
            crc_file_path = os.path.join(file_target_dir, f"{filename}.crc")
            try:
                with open(crc_file_path, 'w') as crc_file:
                    crc_file.write(f"filename={filename}\n")
                    crc_file.write(f"size={file_size}\n")
                    crc_file.write(f"crc32={crc}\n")
                print(f"已生成 CRC 校验文件: {crc_file_path}")
            except Exception as e:
                print(f"生成 CRC 校验文件时出错: {e}")

if __name__ == "__main__":
    # 获取用户输入的文件夹路径
    source_dir = input("请输入源文件夹路径（默认为 d:\\Works\\In\\）: ").strip() or "d:\\Works\\In\\"
    target_dir = input("请输入目标文件夹路径（默认为 d:\\Works\\Out\\）: ").strip() or "d:\\Works\\Out\\"

    if not os.path.isdir(source_dir):
        print(f"无效的源文件夹路径: {source_dir}")
    else:
        process_files(source_dir, target_dir)
        print("所有文件处理完成！")

    input("按回车键退出...")