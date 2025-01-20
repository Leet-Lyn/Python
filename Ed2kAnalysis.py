# 将脚本改写下：请帮我写个中文的 Python 脚本，批注也是中文：
# 询问我 ed2k 链接，分析是不是单一 ed2k 链接，不是的话就提示：“未包含 ed2k 链接。”
# 如果是单一 ed2k 链接，每个链接都是有百分号编码（Percent-encoding），请将其转回原来链接，生成新的链接。
# 根据新的拆分链接的文件名、后缀名、大小、hash。大小请转成 B、KB、MB、GB 形式，并精确到小数点后 4 位，hash 转全部大写。
# 打印内容：文件名、大小、hash，之间用回车间隔。
# 将大小、hash 写入剪贴板，之间用回车间隔。
# 最后询问我是否继续，默认（y，或回车），返回开头，询问我 ed2k 链接。按“n”，择退出。

# 导入模块
import urllib.parse  # 用于处理百分号编码
import pyperclip     # 用于操作剪贴板

# 文件大小转换函数
def format_size(size_str):
    """
    将文件大小从字节数转换为 B、KB、MB、GB 形式，精确到小数点后 4 位。
    :param size_str: 文件大小（字节数）字符串
    :return: 格式化后的大小字符串
    """
    size = float(size_str)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.4f} {unit}"
        size /= 1024
    return f"{size:.4f} TB"

# 打印中文时避免编码错误
def print_gbk(text):
    """
    使用 GBK 编码输出文本，避免因特殊字符导致的编码错误。
    :param text: 需要打印的文本
    """
    print(text.encode('gbk', errors='replace').decode('gbk'))

# 主程序逻辑
def main():
    while True:
        # 提示用户输入 ed2k 链接
        ed2k_link = input("请输入 ed2k 链接（或按 'n' 退出程序）: ").strip()
        
        # 判断用户是否选择退出
        if ed2k_link.lower() == 'n':
            print_gbk("程序已退出。")
            break

        # 检查是否为有效的 ed2k 链接
        if not ed2k_link.startswith("ed2k://|file|"):
            print_gbk("未包含有效的 ed2k 链接。")
            continue

        try:
            # 对链接进行百分号解码
            decoded_link = urllib.parse.unquote(ed2k_link)
            parts = decoded_link.split('|')

            # 检查链接结构是否完整
            if len(parts) >= 5:
                filename = parts[2]  # 文件名
                filesize = parts[3]  # 文件大小（字节）
                filehash = parts[4].upper()  # 哈希值，转为大写

                # 格式化文件大小
                formatted_size = format_size(filesize)

                # 打印文件信息
                print_gbk(f"文件名：{filename}")
                print_gbk(f"大小：{formatted_size}")
                print_gbk(f"哈希：{filehash}")

                # 将大小和哈希复制到剪贴板
                clipboard_content = f"{formatted_size}\n{filehash}"
                pyperclip.copy(clipboard_content)
                print_gbk("文件大小和哈希已复制到剪贴板。")
            else:
                print_gbk("ed2k 链接格式不完整。")
        except Exception as e:
            print_gbk(f"处理链接时发生错误：{e}")

        # 提示用户是否继续
        # choice = input("是否继续？(按回车继续，输入 'n' 退出): ").strip().lower()
        # if choice == 'n':
        #     print_gbk("程序已退出。")
        #     break

# 程序入口
if __name__ == "__main__":
    main()

# 按下回车键退出。
input("按回车键退出...")