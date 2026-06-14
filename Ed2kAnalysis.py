# 将脚本改写下：请帮我写个中文的 Python 脚本，批注也是中文：
# 询问我 ed2k 链接，分析是不是单一 ed2k 链接，不是的话就提示："未包含 ed2k 链接。"
# 如果是单一 ed2k 链接，每个链接都是有百分号编码（Percent-encoding），请将其转回原来链接，生成新的链接。
# 根据新的拆分链接的文件名、后缀名、大小、hash。大小请转成 B、KB、MB、GB 形式，并精确到小数点后 4 位，hash 转全部大写。
# 打印内容：文件名、大小、hash，之间用回车间隔。
# 将大小、hash 写入剪贴板，之间用回车间隔。
# 最后询问我是否继续，默认（y，或回车），返回开头，询问我 ed2k 链接。按"n"，择退出。

# 导入模块
import subprocess
import sys
import urllib.parse


def copy_to_clipboard(text: str) -> None:
    """将文本复制到 Windows 剪贴板（使用系统自带 clip.exe）。"""
    try:
        subprocess.run(
            ["clip.exe"],
            input=text,
            encoding="utf-16-le",
            errors="ignore",
            check=True,
        )
    except Exception as e:
        print(f"复制到剪贴板失败：{e}")


def format_size(size_str: str) -> str:
    """
    将文件大小从字节数转换为 B、KB、MB、GB 形式，精确到小数点后 4 位。
    字节数应为整数字符串。
    """
    size = int(size_str)
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024:
            return f"{size:.4f} {unit}"
        size /= 1024
    return f"{size:.4f} TB"


def main() -> None:
    """主循环：输入 ed2k 链接 → 解码 → 打印信息 → 复制到剪贴板 → 询问是否继续。"""
    while True:
        # 提示用户输入 ed2k 链接
        ed2k_link = input("请输入 ed2k 链接（或按 N 退出程序）：").strip()

        # 判断用户是否选择退出
        if ed2k_link.lower() == "n":
            print("程序已退出。")
            break

        # 检查是否为有效的 ed2k 链接
        if not ed2k_link.startswith("ed2k://|file|"):
            print("未包含有效的 ed2k 链接。")
            continue

        try:
            # 对链接进行百分号解码
            decoded_link = urllib.parse.unquote(ed2k_link)
            parts = decoded_link.split("|")

            # 检查链接结构是否完整
            if len(parts) >= 5:
                filename = parts[2]   # 文件名
                filesize = parts[3]   # 文件大小（字节）
                filehash = parts[4].upper()  # 哈希值，转为大写

                # 格式化文件大小
                formatted_size = format_size(filesize)

                # 打印文件信息
                print(f"文件名：{filename}")
                print(f"大小：{formatted_size}")
                print(f"哈希：{filehash}")

                # 将大小和哈希复制到剪贴板
                copy_to_clipboard(f"{formatted_size}\n{filehash}")
                print("文件大小和哈希已复制到剪贴板。")
            else:
                print("ed2k 链接格式不完整。")
        except Exception as e:
            print(f"处理链接时发生错误：{e}")

        # 询问是否继续
        choice = input("是否继续？（回车继续，N 退出）：").strip().lower()
        if choice == "n":
            print("程序已退出。")
            break


# 程序入口
if __name__ == "__main__":
    # 强制 stdout 使用 UTF-8，避免中文/特殊字符打印报错
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()

# 按下回车键退出。
input("按回车键退出...")
