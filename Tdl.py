# 请帮我写个中文的 Python 脚本，批注也是中文：
# 用 Tdl（P:\ProApps\Tdl\tdl.exe）下载链接。
# 首先询问下载链接：网络链接则直接下载；回车则读取默认列表文件；本地路径则读取该列表文件。
# 再询问是否需要代理（默认 socks5://127.0.0.1:10808）。
# 再询问下载后文件存放位置（默认 Q:\Downloads\Tdl）。

import signal
import subprocess
import sys
from pathlib import Path

# ==================== 全局配置 ====================

# --- 默认路径 ---
TDL_EXE = Path(r"P:\ProApps\Tdl\tdl.exe")
DEFAULT_LIST_FILE = Path(r"e:\Documents\Softwares\Codes\Python\TdlLists.txt")
DEFAULT_PROXY = "socks5://127.0.0.1:10808"
DEFAULT_SAVE_PATH = Path(r"Q:\Downloads\Tdl")

_quit_requested = False  # Ctrl+Q 中断标志

# --- 消息常量 ---
MSG_PROMPT_LINK = "请输入下载链接或列表文件路径（回车使用默认列表文件：{}）"
MSG_PROMPT_PROXY = "是否使用代理？(回车或输入 y 使用默认：{}；输入 n 不使用；输入自定义代理地址）："
MSG_PROMPT_SAVE = "请输入保存路径（回车使用默认：{}）："
MSG_EXEC_CMD = "\n执行命令：{}"
MSG_TDL_EXIT_CODE = "⚠ tdl 返回非零退出码：{}"
MSG_TDL_NOT_FOUND = "❌ 找不到 tdl 可执行文件：{}"
MSG_TDL_EXCEPTION = "❌ 执行 tdl 时发生异常：{}"
MSG_DIR_ERROR = "❌ 无法创建或访问保存路径：{}\n错误：{}"
MSG_LIST_NOT_FOUND = "❌ 列表文件不存在：{}"
MSG_LIST_READ_FAIL = "❌ 读取列表文件失败：{}"
MSG_LIST_EMPTY = "❌ 列表文件为空：{}"
MSG_BATCH_START = "\n发现 {} 条链接，开始逐条下载（保存到：{}）...\n"
MSG_DOWNLOADING = "----- 正在下载 {}/{} -----"
MSG_ALL_DONE = "\n全部处理完成。"
MSG_SINGLE_START = "\n单条链接模式，开始下载（保存到：{}）...\n"
MSG_DOWNLOAD_DONE = "\n下载完成。"
MSG_INTERRUPTED = "\n用户中断，程序退出。"
MSG_ERROR = "❌ 发生未捕获的异常：{}"
MSG_EXIT = "\n按回车键退出..."


# ==================== 辅助函数 ====================

def get_input_with_default(prompt_msg: str, default: str) -> str:
    """显示带默认值的提示并读取用户输入，回车直接使用默认值。"""
    result = input(prompt_msg.format(default)).strip()
    return result if result else default


def run_tdl(url: str, save_dir: str, proxy: str | None = None, group: bool = True) -> None:
    """使用 tdl 执行下载：tdl dl -u <url> -d <save_dir> --group --proxy <proxy>。"""
    cmd = [str(TDL_EXE), "dl", "-u", url, "-d", save_dir]
    if group:
        cmd.append("--group")
    if proxy:
        cmd.extend(["--proxy", proxy])

    print(MSG_EXEC_CMD.format(" ".join(cmd)))
    try:
        res = subprocess.run(cmd, check=False)
        if res.returncode != 0:
            print(MSG_TDL_EXIT_CODE.format(res.returncode))
    except FileNotFoundError:
        print(MSG_TDL_NOT_FOUND.format(TDL_EXE))
        sys.exit(1)
    except Exception as e:
        print(MSG_TDL_EXCEPTION.format(e))


def read_list_file(path: Path) -> list[str]:
    """读入列表文件，返回非空行列表。"""
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
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
    """主流程：获取链接 → 代理 → 保存路径 → 下载。"""
    # --- 输入下载链接或列表文件 ---
    input_link = input(MSG_PROMPT_LINK.format(DEFAULT_LIST_FILE)).strip()

    if not input_link:
        is_batch = True
        batch_file = DEFAULT_LIST_FILE
        default_save_dir = DEFAULT_SAVE_PATH
    elif input_link.startswith(("http://", "https://")):
        is_batch = False
        url = input_link
        default_save_dir = DEFAULT_SAVE_PATH
    else:
        is_batch = True
        batch_file = Path(input_link)
        default_save_dir = batch_file.absolute().parent

    # --- 代理交互 ---
    proxy_answer = input(MSG_PROMPT_PROXY.format(DEFAULT_PROXY)).strip()

    if proxy_answer == "" or proxy_answer.lower() == "y":
        proxy = DEFAULT_PROXY
    elif proxy_answer.lower() == "n":
        proxy = None
    else:
        proxy = proxy_answer

    # --- 保存路径交互 ---
    save_dir = get_input_with_default(MSG_PROMPT_SAVE, str(default_save_dir))

    try:
        Path(save_dir).mkdir(parents=True, exist_ok=True)
    except OSError as e:
        print(MSG_DIR_ERROR.format(save_dir, e))
        return

    # --- 执行 ---
    use_group = True

    if is_batch:
        if not batch_file.is_file():
            print(MSG_LIST_NOT_FOUND.format(batch_file))
            return

        try:
            links = read_list_file(batch_file)
        except Exception as e:
            print(MSG_LIST_READ_FAIL.format(e))
            return

        if not links:
            print(MSG_LIST_EMPTY.format(batch_file))
            return

        print(MSG_BATCH_START.format(len(links), save_dir))
        for idx, link in enumerate(links, start=1):
            print(MSG_DOWNLOADING.format(idx, len(links)))
            run_tdl(link, save_dir, proxy=proxy, group=use_group)

        print(MSG_ALL_DONE)
    else:
        print(MSG_SINGLE_START.format(save_dir))
        run_tdl(url, save_dir, proxy=proxy, group=use_group)
        print(MSG_DOWNLOAD_DONE)



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
