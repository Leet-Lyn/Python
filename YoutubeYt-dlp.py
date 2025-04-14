# 请帮我写个中文的 Python 脚本，批注也是中文：
# 用 yt-dlp（"d:\\ProApps\\Youtube-dl\\yt-dlp.exe"）下载视频。
# 首先询问我想下载单个链接还是列表文件中的链接？（如果输入的是网络链接，则下载该链接；按回车则为默认地址“e:\\Documents\\Creations\\Scripts\\Python\\YoutubeYt-dlpLists.txt”；如果输入的是本地链接，则下载该地址列表文件中的链接。）
# 再询问我是否需要引入 cookies 文件？（按回车或输入“y”则为引入 cookies 文件，默认地址为"d:\\ProApps\\Youtube-dl\\YoutubeYt-dlpCookies.txt"；如果输入的是本地链接，则将该地址作为 cookies 文件地址；输入“n”则不引入 cookies 文件。）
# 再询问我是否需要代理？（按回车或输入“y”则为代理，默认地址“127.0.0.1:10809”；输入“n”则不引入 cookies 文件。）
# 再询问我下载后文件存放的位置？（按回车则为默认地址“d:\\Downloads\\”；如果输入的是本地链接，则将该地址作为下载后文件存放的位置。）

# 导入模块。
import subprocess
import os

# 定义默认路径
YT_DLP_PATH = r"d:\\ProApps\\Youtube-dl\\yt-dlp.exe"
DEFAULT_LIST_FILE = r"e:\\Documents\\Creations\\Scripts\\Python\\YoutubeYt-dlpLists.txt"
DEFAULT_COOKIES_FILE = r"d:\\ProApps\\Youtube-dl\\YoutubeYt-dlpCookies.txt"
DEFAULT_PROXY = "127.0.0.1:10809"
DEFAULT_SAVE_PATH = r"d:\\Downloads\\"

def main():
    # 询问下载方式
    input_link = input("请输入视频链接或列表文件路径（直接回车使用默认列表文件“e:\\Documents\\Creations\\Scripts\\Python\\YoutubeYt-dlpLists.txt”）：").strip()
    if not input_link:
        # 使用默认列表文件
        batch_file = DEFAULT_LIST_FILE
        is_batch = True
    elif input_link.startswith(("http://", "https://")):
        # 单个链接
        url = input_link
        is_batch = False
    else:
        # 本地列表文件
        batch_file = input_link
        is_batch = True

    # 询问Cookies
    cookies_answer = input("是否使用Cookies文件？(Y/n, 默认“d:\\ProApps\\Youtube-dl\\YoutubeYt-dlpCookies.txt”): ").strip().lower()
    if cookies_answer == "n":
        cookies = None
    else:
        if cookies_answer in ("", "y"):
            cookies = DEFAULT_COOKIES_FILE
        else:
            cookies = cookies_answer  # 用户自定义路径

    # 询问代理
    proxy_answer = input("是否使用代理？(Y/n, 默认为“127.0.0.1:10809”): ").strip().lower()
    proxy = DEFAULT_PROXY if proxy_answer in ("", "y") else None

    # 询问保存路径
    save_path = input(f"请输入保存路径（直接回车使用默认路径“d:\\Downloads\\”）：").strip()
    if not save_path:
        save_path = DEFAULT_SAVE_PATH
    os.makedirs(save_path, exist_ok=True)  # 自动创建目录

    # 构建命令
    command = [YT_DLP_PATH]
    
    # 核心新增功能：封面+字幕
    command += [
        "--write-thumbnail",    # 下载封面图
        "--write-subs",        # 下载字幕
        "--sub-langs", "all",  # 所有可用语言
        "--convert-subs", "srt"# 转换为通用字幕格式
    ]
    
    # 添加代理
    if proxy:
        command.extend(["--proxy", proxy])
    
    # 添加Cookies
    if cookies:
        command.extend(["--cookies", cookies])
    
    # 添加下载链接/列表文件
    if is_batch:
        command.extend(["--batch-file", batch_file])
    else:
        command.append(url)
    
    # 添加输出模板
    command.extend(["-o", os.path.join(save_path, "%(title)s.%(ext)s")])

    # 执行下载
    print("\\n执行命令：", " ".join(command))
    subprocess.run(command)

if __name__ == "__main__":
    main()