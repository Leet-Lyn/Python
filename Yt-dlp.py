# 请帮我写个中文的 Python 脚本，批注也是中文：
# 用 yt-dlp（"d:\\ProApps\\Youtube-dl\\yt-dlp.exe"）下载视频。
# 首先询问我想下载单个链接还是列表文件中的链接？（如果输入的是网络链接，则下载该链接；按回车则为默认地址“d:\\ProApps\\Youtube-dl\\Cookies.txt”；如果输入的是本地链接，则下载该地址列表文件中的链接。）
# 再询问我是否需要引入 cookies 文件？（按回车或输入“y”则为引入 cookies 文件，默认地址为"d:\\ProApps\\Youtube-dl\\Cookies.txt"；如果输入的是本地链接，则将该地址作为 cookies 文件地址；输入“n”则不引入 cookies 文件。）
# 再询问我是否需要代理？（按回车或输入“y”则为代理，默认地址“127.0.0.1:10809”；输入“n”则不引入 cookies 文件。）
# 再询问我下载后文件存放的位置？（按回车则为默认地址“d:\\Downloads\\”；如果输入的是本地链接，则将该地址作为下载后文件存放的位置。）

# 导入模块。
# 导入必要模块
import subprocess
import os

# 默认路径设置
DEFAULT_COOKIES_PATH = "d:\\ProApps\\Youtube-dl\\Cookies.txt"
DEFAULT_LIST_FILE = "d:\\ProApps\\Youtube-dl\\Links.txt"
DEFAULT_OUTPUT_DIR = "d:\\Downloads\\"
DEFAULT_PROXY = "127.0.0.1:10809"
YT_DLP_PATH = "d:\\ProApps\\Youtube-dl\\yt-dlp.exe"

def get_user_choice(prompt, default=None):
    """
    获取用户输入，如果为空则返回默认值。
    """
    choice = input(prompt).strip()
    return choice if choice else default

def validate_file_path(path):
    """
    验证文件路径是否存在。
    """
    if not os.path.exists(path):
        print(f"路径无效：{path}")
        return False
    return True

def download_videos(urls, output_dir, cookies_file=None, proxy=None):
    """
    使用 yt-dlp 下载视频。
    """
    # 构建基本命令
    base_command = [YT_DLP_PATH, "-o", os.path.join(output_dir, "%(title)s.%(ext)s")]

    # 如果启用 cookies 文件，添加参数
    if cookies_file:
        base_command.extend(["--cookies", cookies_file])

    # 如果启用代理，添加参数
    if proxy:
        base_command.extend(["--proxy", proxy])

    # 下载每个链接
    for url in urls:
        print(f"开始下载：{url}")
        command = base_command + [url]
        try:
            result = subprocess.run(command, check=True)
            print(f"成功下载：{url}")
        except subprocess.CalledProcessError as e:
            print(f"下载失败：{url}，错误代码：{e.returncode}")
        except Exception as e:
            print(f"下载过程中发生未知错误：{e}")

def main():
    while True:
        # 用户选择链接来源
        download_choice = get_user_choice(
            "请输入要下载的链接（按回车默认使用地址列表文件）：", default=None
        )
        if download_choice:  # 用户输入了单个链接
            urls = [download_choice]
        else:  # 使用地址列表文件
            list_file = get_user_choice(
                f"请输入地址列表文件路径（按回车默认使用 '{DEFAULT_LIST_FILE}'）：", default=DEFAULT_LIST_FILE
            )
            if not validate_file_path(list_file):
                continue
            with open(list_file, "r") as file:
                urls = file.read().splitlines()

        # 用户选择是否引入 cookies 文件
        cookies_choice = get_user_choice(
            f"是否使用 cookies 文件？（按回车默认 '{DEFAULT_COOKIES_PATH}'，输入 'n' 不使用）：", default=None
        )
        if cookies_choice and cookies_choice.lower() != "n":
            cookies_file = cookies_choice
            if not validate_file_path(cookies_file):
                continue
        else:
            cookies_file = None

        # 用户选择是否使用代理
        proxy_choice = get_user_choice(
            f"是否使用代理？（按回车默认 '{DEFAULT_PROXY}'，输入 'n' 不使用）：", default=None
        )
        if proxy_choice and proxy_choice.lower() != "n":
            proxy = proxy_choice
        else:
            proxy = None

        # 用户选择下载后文件保存位置
        output_dir = get_user_choice(
            f"请输入下载文件保存的位置（按回车默认使用 '{DEFAULT_OUTPUT_DIR}'）：", default=DEFAULT_OUTPUT_DIR
        )
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
                print(f"下载目录已创建：{output_dir}")
            except Exception as e:
                print(f"创建下载目录失败：{e}")
                continue

        # 调用下载函数
        download_videos(urls, output_dir, cookies_file=cookies_file, proxy=proxy)

        # 询问是否继续
        continue_choice = get_user_choice("是否继续下载？（输入 'n' 退出，回车继续）：", default="y").lower()
        if continue_choice == "n":
            print("程序结束。")
            break

# 程序入口
if __name__ == "__main__":
    main()

# 按回车键退出程序
input("按回车键退出...")