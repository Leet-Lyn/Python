# 请帮我写个中文的 Python 脚本，批注也是中文：
# 用 Tdl（"p:\\ProApps\\Tdl\\tdl.exe"）下载链接。
# 首先询问我想链接是什么（如果输入的是网络链接，则下载该链接；按回车则为默认地址“e:\\Documents\\Creations\\Scripts\\Python\\TdlLists.txt”；如果输入的是本地链接，则下载该地址列表文件中的链接（每行一条）。）
# 再询问我是否需要代理？（按回车或输入“y”则为代理，默认地址“socks5://127.0.0.1:10808”。）
# 再询问我下载后文件存放的位置？（按回车则为默认地址“q:\\Downloads\\Tdl\\”；如果输入的是本地链接，则将该地址作为下载后文件存放的位置。）

# 导入模块。
import subprocess
import os
import sys

TDL_EXE = r"p:\ProApps\Tdl\tdl.exe"
DEFAULT_LIST_FILE = r"e:\Documents\Creations\Scripts\Python\TdlLists.txt"
DEFAULT_PROXY = "socks5://127.0.0.1:10808"
DEFAULT_SAVE_PATH = r"q:\Downloads\Tdl"

def run_tdl(url, save_dir, proxy=None, group=True):
    """
    使用 tdl 执行下载命令，命令格式：
    tdl dl -u <url> -d <save_dir> --group --proxy <proxy>
    """
    cmd = [TDL_EXE, "dl", "-u", url, "-d", save_dir]
    if group:
        cmd.append("--group")
    if proxy:
        # tdl 需要完整协议前缀，例如 socks5://127.0.0.1:10808
        cmd.extend(["--proxy", proxy])

    # 打印将要执行的命令（便于调试）
    print("\n执行命令：", " ".join(cmd))
    try:
        # 使用 subprocess.run，直接传列表以避免 shell 解析问题
        res = subprocess.run(cmd, check=False)
        if res.returncode != 0:
            print(f"⚠️ tdl 返回非零退出码：{res.returncode}")
    except FileNotFoundError:
        print(f"❌ 找不到 tdl 可执行文件：{TDL_EXE}")
        sys.exit(1)
    except Exception as e:
        print("❌ 执行 tdl 时发生异常：", e)


def read_list_file(path):
    """读入列表文件，返回非空行的列表"""
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines


def main():
    # ---------------- 输入下载链接或列表文件 ----------------
    input_link = input(
        "请输入下载链接或列表文件路径（回车使用默认列表文件："
        f"\"{DEFAULT_LIST_FILE}\"）："
    ).strip()

    # 三种情况：空（使用默认列表文件）、http(s)（单条）、本地路径（列表文件）
    if not input_link:
        is_batch = True
        batch_file = DEFAULT_LIST_FILE
        default_save_dir = DEFAULT_SAVE_PATH
    elif input_link.startswith(("http://", "https://")):
        is_batch = False
        url = input_link
        default_save_dir = DEFAULT_SAVE_PATH
    else:
        # 用户输入本地路径：当作列表文件
        is_batch = True
        batch_file = input_link
        # 将该列表文件所在目录作为默认保存位置（符合你要求）
        default_save_dir = os.path.dirname(os.path.abspath(batch_file)) or DEFAULT_SAVE_PATH

    # ---------------- 代理交互 ----------------
    proxy_answer = input(
        f"是否使用代理？(回车或输入 y 使用默认：{DEFAULT_PROXY}；输入 n 不使用；输入自定义代理地址)："
    ).strip()

    if proxy_answer == "" or proxy_answer.lower() == "y":
        proxy = DEFAULT_PROXY
    elif proxy_answer.lower() == "n":
        proxy = None
    else:
        proxy = proxy_answer  # 用户自定义代理，例如 socks5://127.0.0.1:10808

    # ---------------- 保存路径交互 ----------------
    # 如果是本地列表文件，脚本把该列表目录作为默认保存路径（如你要求）
    save_path_prompt = (
        f"请输入保存路径（回车使用默认：\"{default_save_dir}\"）："
    )
    save_dir_input = input(save_path_prompt).strip()
    if save_dir_input:
        save_dir = save_dir_input
    else:
        save_dir = default_save_dir

    # 确保目录存在（若不能创建则提示并退出）
    try:
        os.makedirs(save_dir, exist_ok=True)
    except Exception as e:
        print("❌ 无法创建或访问保存路径：", save_dir, "\n错误：", e)
        return

    # ---------------- 执行 ----------------
    # 默认加上 --group（与你示例一致）
    use_group = True

    if is_batch:
        # 检查文件是否存在
        if not os.path.isfile(batch_file):
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
        # 单条 URL
        print(f"\n单条链接模式，开始下载（保存到：{save_dir}）...\n")
        run_tdl(url, save_dir, proxy=proxy, group=use_group)
        print("\n下载完成。")


if __name__ == "__main__":
    main()