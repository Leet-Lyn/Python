# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件位置，默认为“e:\\Documents\\Creations\\Scripts\\Attachment\\Ed2kList.txt”（按回车表示默认，按“c”读取剪贴板，并写入“e:\\Documents\\Creations\\Scripts\\Attachment\\Ed2kList.txt”）。
# 该文件（或剪贴板）内包含许多 ed2k 链接，每行一个，顺序读取每个 ed2k 链接。
# 每个链接都是百分号编码(Percent-encoding)，请将其转回原来链接。在源文件位置下生成新的文件（读取剪贴板则在 “e:\\Documents\\Creations\\Scripts\\Attachment\\”下），文件名为“Ed2kList.new.txt”。
# 根据“Ed2kList.new.txt”文件，在源文件位置下生成新的文件，文件名分别为“Ed2kList.name.txt”、“Ed2kList.suffix.txt”、“Ed2kList.size.txt”、“Ed2kList.hash.txt”。分别存放链接的文件名、后缀名、大小、hash。“Ed2kList.size.txt”文件中存放的文件大小请转成 B、KB、MB、GB 形式，并精确到小数点后 4 位，hash 转全部大写。
# 将大小、hash 写入剪贴板，之间用回车间隔。

# 导入模块
import os            # 处理文件和路径
import urllib.parse  # 解码百分号编码的链接
import pyperclip     # 剪贴板操作

# 文件大小转换函数
def format_size(size_str):
    """
    将文件大小从字节数转换为 B、KB、MB、GB 的形式，精确到小数点后 4 位。
    :param size_str: 文件大小（以字节为单位）字符串
    :return: 格式化后的大小字符串
    """
    size = int(size_str)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.4f} {unit}"
        size /= 1024
    return f"{size:.4f} TB"

def main():
    # 询问源文件位置，默认值为"e:\\Documents\\Creations\\Scripts\\Attachment\\Ed2kList.txt"
    user_input = input("请输入源文件位置（默认为'e:\\Documents\\Creations\\Scripts\\Attachment\\Ed2kList.txt'，按回车使用默认，按'C'或'c'读取剪贴板）：").strip()
    
    if user_input.lower() == 'c':
        # 用户选择从剪贴板读取
        source_file_path = "e:\\Documents\\Creations\\Scripts\\Attachment\\Ed2kList.txt"
        source_folder = "e:\\Documents\\Creations\\Scripts\\Attachment\\"
        
        # 确保目录存在
        os.makedirs(source_folder, exist_ok=True)
        
        # 从剪贴板读取内容
        try:
            clipboard_content = pyperclip.paste()
            if not clipboard_content:
                print("剪贴板为空，请先复制ed2k链接到剪贴板！")
                return
                
            # 将剪贴板内容写入文件
            with open(source_file_path, 'w', encoding='utf-8') as file:
                file.write(clipboard_content)
            print(f"已从剪贴板读取内容并保存到: {source_file_path}")
        except Exception as e:
            print(f"读取剪贴板失败: {e}")
            return
    elif not user_input:
        # 用户直接按回车，使用默认路径
        source_file_path = "e:\\Documents\\Creations\\Scripts\\Attachment\\Ed2kList.txt"
        source_folder = "e:\\Documents\\Creations\\Scripts\\Attachment\\"
    else:
        # 用户输入了自定义路径
        source_file_path = user_input
        source_folder = os.path.dirname(source_file_path)
    
    # 检查源文件是否存在
    if not os.path.exists(source_file_path):
        print("源文件不存在，请检查路径或文件名！")
        return

    # 读取源文件中的所有 ed2k 链接
    with open(source_file_path, 'r', encoding='utf-8') as file:
        links = file.readlines()

    # 创建解码后的链接文件
    base_name = os.path.splitext(os.path.basename(source_file_path))[0]
    new_file_path = os.path.join(source_folder, f"{base_name}.new.txt")
    with open(new_file_path, 'w', encoding='utf-8') as new_file:
        decoded_links = [urllib.parse.unquote(link.strip()) for link in links]
        new_file.write("\n".join(decoded_links))

    # 初始化要生成的文件路径
    name_file_path = os.path.join(source_folder, f"{base_name}.name.txt")
    suffix_file_path = os.path.join(source_folder, f"{base_name}.suffix.txt")
    size_file_path = os.path.join(source_folder, f"{base_name}.size.txt")
    hash_file_path = os.path.join(source_folder, f"{base_name}.hash.txt")
    
    # 存储所有文件的大小和hash，用于写入剪贴板
    sizes = []
    hashes = []

    # 打开各目标文件进行写入
    with open(name_file_path, 'w', encoding='utf-8') as name_file, \
         open(suffix_file_path, 'w', encoding='utf-8') as suffix_file, \
         open(size_file_path, 'w', encoding='utf-8') as size_file, \
         open(hash_file_path, 'w', encoding='utf-8') as hash_file:

        # 逐行处理解码后的链接
        for link in decoded_links:
            if link.startswith("ed2k://|file|"):
                # 分割链接，获取文件信息
                parts = link.split('|')
                if len(parts) >= 5:
                    filename = parts[2]
                    filesize = parts[3]
                    filehash = parts[4].upper()  # 转换为大写形式
                    file_suffix = os.path.splitext(filename)[1]  # 提取文件后缀名

                    # 转换文件大小为可读格式
                    formatted_size = format_size(filesize)
                    
                    # 存储大小和hash
                    sizes.append(formatted_size)
                    hashes.append(filehash)

                    # 写入相应的文件
                    name_file.write(filename + "\n")
                    suffix_file.write(file_suffix + "\n")
                    size_file.write(formatted_size + "\n")
                    hash_file.write(filehash + "\n")

    # 读取生成的文件内容
    with open(size_file_path, 'r', encoding='utf-8') as size_file:
        size_content = size_file.read().strip()
    
    with open(hash_file_path, 'r', encoding='utf-8') as hash_file:
        hash_content = hash_file.read().strip()
    
    # 将大小和hash写入剪贴板，先写大小文件内容，再加2个回车，再写hash文件内容
    clipboard_content = size_content + "\n\n" + hash_content
    
    try:
        pyperclip.copy(clipboard_content)
        print("大小和hash已写入剪贴板")
    except Exception as e:
        print(f"写入剪贴板失败: {e}")

    print("处理完成，生成的新文件保存在：", source_folder)

# 程序入口
if __name__ == "__main__":
    main()

# 按下回车键退出程序
input("按回车键退出...")