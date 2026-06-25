# 将脚本改写下：请帮我写个中文的 Python 脚本，批注也是中文：
# 询问我 ed2k 链接，分析是不是单一 ed2k 链接，不是的话就提示："未包含 ed2k 链接。"
# 如果是单一 ed2k 链接，每个链接都是有百分号编码（Percent-encoding），请将其转回原来链接，生成新的链接。
# 根据新的拆分链接的文件名、后缀名、大小、hash。大小请转成 B、KB、MB、GB 形式，并精确到小数点后 4 位，hash 转全部大写。
# 打印内容：文件名、大小、hash，之间用回车间隔。
# 将大小、hash 写入剪贴板，之间用回车间隔。
# 最后询问我是否继续，默认（y，或回车），返回开头，询问我 ed2k 链接。按"n"，择退出。

# 导入模块
import signal
import subprocess
import sys
import urllib.parse

# --- 常量 ---
_quit_requested = False  # Ctrl+Q 中断标志

# --- 消息常量 ---
MSG_INTERRUPTED = "\n\n用户中断程序，已退出。"
MSG_ERROR = "\n程序运行出错: {}"
MSG_EXIT = "\n按回车键退出..."
MSG_CLIPBOARD_FAIL = "复制到剪贴板失败：{}"
MSG_PROMPT_ED2K = "请输入 ed2k 链接（或按 N 退出程序）："
MSG_EXIT_OK = "程序已退出。"
MSG_INVALID_ED2K = "未包含有效的 ed2k 链接。"
MSG_FILENAME = "文件名：{}"
MSG_FILESIZE = "大小：{}"
MSG_FILEHASH = "哈希：{}"
MSG_CLIPBOARD_OK = "文件大小和哈希已复制到剪贴板。"
MSG_INCOMPLETE_ED2K = "ed2k 链接格式不完整。"
MSG_PROCESS_ERROR = "处理链接时发生错误：{}"
MSG_CONTINUE = "是否继续？（回车继续，N 退出）："


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
        print(MSG_CLIPBOARD_FAIL.format(e))


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


# ==================== 中断处理 ====================


def _on_quit_signal(signum, frame):
    global _quit_requested
    _quit_requested = True
    raise KeyboardInterrupt()


def _init_quit_handler():
    if hasattr(signal, "SIGQUIT"):
        signal.signal(signal.SIGQUIT, _on_quit_signal)


def _check_quit() -> bool:
    global _quit_requested
    if sys.platform == "win32":
        try:
            import msvcrt
            while msvcrt.kbhit():
                if msvcrt.getch() == b"\x11":
                    _quit_requested = True
        except Exception:
            pass
    return _quit_requested


def main() -> None:
    """主循环：输入 ed2k 链接 → 解码 → 打印信息 → 复制到剪贴板 → 询问是否继续。"""
    _init_quit_handler()
    while True:
        # 提示用户输入 ed2k 链接
        ed2k_link = input(MSG_PROMPT_ED2K).strip()

        # 判断用户是否选择退出
        if ed2k_link.lower() == "n":
            print(MSG_EXIT_OK)
            break

        # 检查是否为有效的 ed2k 链接
        if not ed2k_link.lower().startswith("ed2k://|file|"):
            print(MSG_INVALID_ED2K)
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
                print(MSG_FILENAME.format(filename))
                print(MSG_FILESIZE.format(formatted_size))
                print(MSG_FILEHASH.format(filehash))

                # 将大小和哈希复制到剪贴板
                copy_to_clipboard(f"{formatted_size}\n{filehash}")
                print(MSG_CLIPBOARD_OK)
            else:
                print(MSG_INCOMPLETE_ED2K)
        except Exception as e:
            print(MSG_PROCESS_ERROR.format(e))

        print()  # 空行分隔，让输出更清晰


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