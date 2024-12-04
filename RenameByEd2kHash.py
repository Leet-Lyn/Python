# 用 ed2k hash 对文件夹下所有文件重命名为生成的 ed2k hash。

# 导入模块
import os
from Crypto.Hash import MD4

def ed2k_hash(file_path):
    """
    计算文件的 ED2K 哈希值。
    :param file_path: 文件路径
    :return: ED2K 哈希值字符串，失败时返回空字符串
    """
    CHUNK_SIZE = 9728000  # ED2K 每个块的大小
    md4 = MD4.new()
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(CHUNK_SIZE):  # 逐块读取文件
                md4.update(chunk)
        return md4.hexdigest()
    except Exception as e:
        print(f"无法读取文件 {file_path}：{e}")
        return ''

def rename_files_in_folder(source_folder):
    """
    遍历指定文件夹中的所有文件，并将其重命名为 ED2K 哈希格式。
    :param source_folder: 源文件夹路径
    """
    if not os.path.isdir(source_folder):
        print("指定的路径无效，请确保它是一个文件夹。")
        return

    for root, _, files in os.walk(source_folder):
        for file in files:
            file_path = os.path.join(root, file)
            
            # 检查是否为文件
            if not os.path.isfile(file_path):
                print(f"跳过非文件项：{file_path}")
                continue

            file_size = os.path.getsize(file_path)
            if file_size == 0:
                print(f"{file} 是空文件，已跳过。")
                continue

            # 计算文件哈希
            file_hash = ed2k_hash(file_path)
            if not file_hash:
                continue

            # 生成新的文件名
            file_ext = os.path.splitext(file)[1].lower()
            new_file_name = f"[{file_size}][{file_hash}]{file_ext}"
            new_file_path = os.path.join(root, new_file_name)

            try:
                os.rename(file_path, new_file_path)
                print(f"成功重命名：{file} -> {new_file_name}")
            except Exception as e:
                print(f"无法重命名文件 {file_path}：{e}")

def main():
    """
    主程序入口，处理用户输入并执行文件重命名操作。
    """
    # 获取源文件夹路径
    source_folder = input("请输入源文件夹位置（按回车键使用默认地址：t:\\XXX\\）：").strip() or "t:\\XXX\\"
    
    # 调用重命名函数
    rename_files_in_folder(source_folder)

    # 退出提示
    input("操作完成，按回车键退出...")

if __name__ == "__main__":
    main()