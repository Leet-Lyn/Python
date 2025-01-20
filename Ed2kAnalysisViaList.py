# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件位置，默认为“d:\\Works\\Ed2K\\”；询问我源文件文件名，默认为“Links.txt”
# 该文件内包含许多 ed2k 链接，每行一个。顺序读取每个 ed2k 链接。
# 每个链接都是百分号编码(Percent-encoding)，请将其转回原来链接。在源文件位置下生成新的文件，文件名相同，后缀名分别为“.new.txt”。
# 根据“.new.txt”文件，在源文件位置下生成新的文件，文件名相同，后缀名分别为“.name.txt”、“.suffix.txt”、“.size.txt”、“.hash.txt”。分别存放链接的文件名、后缀名、大小、hash。“.size.txt”文件中存放的文件大小请转成 B、KB、MB、GB 形式，并精确到小数点后 4 位，hash 转全部大写。

# 导入模块
import os            # 处理文件和路径
import urllib.parse  # 解码百分号编码的链接

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
    # 询问源文件位置，默认值为“d:\\Works\\Ed2K\\”
    source_folder = input("请输入源文件位置（默认为‘d:\\Works\\Ed2K\\’）：").strip()
    if not source_folder:
        source_folder = "d:\\Works\\Ed2K\\"

    # 询问源文件文件名，默认值为“Links.txt”
    source_filename = input("请输入源文件文件名（默认为‘Links.txt’）：").strip()
    if not source_filename:
        source_filename = "Links.txt"

    # 构建源文件路径
    source_file_path = os.path.join(source_folder, source_filename)

    # 检查源文件是否存在
    if not os.path.exists(source_file_path):
        print("源文件不存在，请检查路径或文件名！")
        return

    # 读取源文件中的所有 ed2k 链接
    with open(source_file_path, 'r', encoding='utf-8') as file:
        links = file.readlines()

    # 创建解码后的链接文件
    new_file_path = source_file_path + ".new.txt"
    with open(new_file_path, 'w', encoding='utf-8') as new_file:
        decoded_links = [urllib.parse.unquote(link.strip()) for link in links]
        new_file.write("\n".join(decoded_links))

    # 初始化要生成的文件路径
    name_file_path = source_file_path + ".name.txt"
    suffix_file_path = source_file_path + ".suffix.txt"
    size_file_path = source_file_path + ".size.txt"
    hash_file_path = source_file_path + ".hash.txt"

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

                    # 写入相应的文件
                    name_file.write(filename + "\n")
                    suffix_file.write(file_suffix + "\n")
                    size_file.write(formatted_size + "\n")
                    hash_file.write(filehash + "\n")

    print("处理完成，生成的新文件保存在：", source_folder)

# 程序入口
if __name__ == "__main__":
    main()

# 按下回车键退出程序
input("按回车键退出...")