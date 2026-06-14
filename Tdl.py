# 请帮我写个中文的 Python 脚本，批注也是中文：
# 用 Tdl（P:\ProApps\Tdl\tdl.exe）下载链接。
# 首先询问下载链接：网络链接则直接下载；回车则读取默认列表文件；本地路径则读取该列表文件。
# 再询问是否需要代理（默认 socks5://127.0.0.1:10808）。
# 再询问下载后文件存放位置（默认 Q:\Downloads\Tdl）。

import subprocess
import sys
from pathlib import Path

# --- 常量 ---
TDL_EXE = Path(r"P:\ProApps\Tdl\tdl.exe")
DEFAULT_LIST_FILE = Path(r"e:\Documents\Softwares\Codes\Python\TdlLists.txt")
DEFAULT_PROXY = "socks5://127.0.0.1:10808"
DEFAULT_SAVE_PATH = Path(r"Q:\Downloads\Tdl")


def run_tdl(url: str, save_dir: str, proxy: str | None = None, group: bool = True) -> None:
    """使用 tdl 执行下载：tdl dl -u <url> -d <save_dir> --group --proxy <proxy>。"""
    cmd = [str(TDL_EXE), "dl", "-u", url, "-d", save_dir]
    if group:
        cmd.append("--group")
    if proxy:
        cmd.extend(["--proxy", proxy])

    print("\n执行命令：", " ".join(cmd))
    try:
        res = subprocess.run(cmd, check=False)
        if res.returncode != 0:
            print(f"⚠ tdl 返回非零退出码：{res.returncode}")
    except FileNotFoundError:
        print(f"❌ 找不到 tdl 可执行文件：{TDL_EXE}")
        sys.exit(1)
    except Exception as e:
        print("❌ 执行 tdl 时发生异常：", e)


def read_list_file(path: Path) -> list[str]:
    """读入列表文件，返回非空行列表。"""
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> None:
    """主流程：获取链接 → 代理 → 保存路径 → 下载。"""
    # --- 输入下载链接或列表文件 ---
    input_link = input(
        f"请输入下载链接或列表文件路径（回车使用默认列表文件：{DEFAULT_LIST_FILE}）："
    ).strip()

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
    proxy_answer = input(
        f"是否使用代理？(回车或输入 y 使用默认：{DEFAULT_PROXY}；输入 n 不使用；输入自定义代理地址)："
    ).strip()

    if proxy_answer == "" or proxy_answer.lower() == "y":
        proxy = DEFAULT_PROXY
    elif proxy_answer.lower() == "n":
        proxy = None
    else:
        proxy = proxy_answer

    # --- 保存路径交互 ---
    save_dir_input = input(
        f"请输入保存路径（回车使用默认：{default_save_dir}）："
    ).strip()
    save_dir = save_dir_input if save_dir_input else str(default_save_dir)

    try:
        Path(save_dir).mkdir(parents=True, exist_ok=True)
    except OSError as e:
        print("❌ 无法创建或访问保存路径：", save_dir, "\n错误：", e)
        return

    # --- 执行 ---
    use_group = True

    if is_batch:
        if not batch_file.is_file():
            print("❌ 列表文件不存在：", batch_file)
            return

        try:
            links = read_list_file(batch_file)
        except Exception as e:
            print("❌ 读取列表文件失败：", e)
            return

        if not links:
            print("❌ 列表文件为空：", batch_file)
            return

        print(f"\n发现 {len(links)} 条链接，开始逐条下载（保存到：{save_dir}）...\n")
        for idx, link in enumerate(links, start=1):
            print(f"----- 正在下载 {idx}/{len(links)} -----")
            run_tdl(link, save_dir, proxy=proxy, group=use_group)

        print("\n全部处理完成。")
    else:
        print(f"\n单条链接模式，开始下载（保存到：{save_dir}）...\n")
        run_tdl(url, save_dir, proxy=proxy, group=use_group)
        print("\n下载完成。")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
