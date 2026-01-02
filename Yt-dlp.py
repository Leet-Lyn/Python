# 请帮我写个中文的 Python 脚本，批注也是中文，但是变量参数不要是中文：
# 用 yt-dlp（"d:\ProApps\Youtube-dl\yt-dlp.exe"）下载视频。
# 首先询问下载的链接？（如果输入的是网络链接，则下载该链接（可以是多行。不是多次输入而是输入一次，往往是从剪贴板粘贴，可以包含多行）。按回车则为默认地址“e:\Documents\Creations\Scripts\Attachment\Yt-dlpLists.txt”；如果输入的是本地链接，则下载该地址列表文件中的链接。）
# 引入本地 cookies：“e:\Documents\Creations\Scripts\Attachment\Yt-dlpCookies.txt”
# 每一个链接都尝试 2 次。第一次尝试不使用代理，如果未成功下载，则再次使用代理下载。。代理地址：“http://127.0.0.1:10808”
# 再询问我下载后文件存放的位置？（按回车则为默认地址“d:\Works\Downloads\Yt-dlp”；如果输入的是本地链接，则将该地址作为下载后文件存放的位置。）
# 询问我 excel 文件位置（默认为：“e:\Documents\Creations\Scripts\Attachment\视频.xlsx”）。
# 进行下载，类似命令：
# 
# 读取 excel 文件，第一行为表头（字段名）。此后每一行为一条记录。每下载一个视频，每一条记录新开一行。
# "Index"字段值为上一行 "Index"字段值+1（如上一行为空或为表头，则"Index"字段值为 1）。
# 将下载的文件名写入"名字"与"原文件名"字段值。
# 下载的链接写入"引用页"。
# 计算并生成下载的视频文件（仅仅是视频文件）的 Ed2K 链接。安装了 RHash，位置“d:\ProApps\RHash\rhash.exe”。生成 ed2k 的命令类似：rhash.exe --uppercase --ed2k-link "文件地址"。生成的 ed2k 链接，写入"主链接"字段值。
# 通过"主链接"字段值。分别生成"大小"、"散列"字段值。大小请转成 B、KB、MB、GB 形式，并精确到小数点后 4 位，hash 转全部大写。
# 所有结束后，再从最开始询问我下载的链接，循环进行。
# 输入“q”退出。

# 导入模块
# =========================
# 导入模块
# =========================
import os
import re
import subprocess
import urllib.parse
import pandas as pd

# =========================
# 配置路径
# =========================

YTDLP_PATH = r"d:\ProApps\Youtube-dl\yt-dlp.exe"
COOKIES_PATH = r"e:\Documents\Creations\Scripts\Attachment\Yt-dlpCookies.txt"
PROXY_URL = "http://127.0.0.1:10808"

DEFAULT_URL_LIST = r"e:\Documents\Creations\Scripts\Attachment\Yt-dlpLists.txt"
DEFAULT_OUTPUT_DIR = r"d:\Works\Downloads\Yt-dlp"
DEFAULT_EXCEL_PATH = r"e:\Documents\Creations\Scripts\Attachment\视频.xlsx"

RHASH_PATH = r"d:\ProApps\RHash\rhash.exe"

VIDEO_EXTENSIONS = {".mp4", ".mkv", ".webm", ".flv", ".avi", ".mov"}

# =========================
# 代理白名单（命中则直接用代理）
# =========================

PROXY_WHITELIST = [
    "youtube.com",
    "youtu.be"
]

# =========================
# 工具函数
# =========================

def format_size(size_bytes):
    """字节数 → B / KB / MB / GB（4 位小数）"""
    size = float(size_bytes)
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:.4f} {unit}"
        size /= 1024
    return f"{size:.4f} TB"

def extract_urls(text):
    """从文本中提取所有 http/https 链接"""
    urls = re.findall(r"https?://[^\s]+", text)
    return [u.rstrip(";,") for u in urls]

def read_url_input(user_input):
    """读取用户输入的链接或链接列表文件"""
    if not user_input:
        if os.path.exists(DEFAULT_URL_LIST):
            with open(DEFAULT_URL_LIST, "r", encoding="utf-8") as f:
                return extract_urls(f.read())
        return []

    if os.path.exists(user_input):
        with open(user_input, "r", encoding="utf-8") as f:
            return extract_urls(f.read())

    return extract_urls(user_input)

def need_proxy_first(url):
    """判断是否需要直接使用代理"""
    url_lower = url.lower()
    for domain in PROXY_WHITELIST:
        if domain in url_lower:
            return True
    return False

def run_ytdlp(url, output_dir, use_proxy):
    """执行 yt-dlp 下载，并实时输出信息"""
    cmd = [
        YTDLP_PATH,
        "--cookies", COOKIES_PATH,
        "-P", output_dir,
        "--write-thumbnail",
        "--convert-thumbnails", "jpg",
        "--write-subs",
        "--write-auto-subs",
        "--sub-langs", "all",
        "--sub-format", "srt",
        "--write-info-json",
        url
    ]

    if use_proxy:
        cmd.extend(["--proxy", PROXY_URL])

    print(f"{'='*10} 下载 {'代理' if use_proxy else '直连'}: {url} {'='*10}")
    result = subprocess.run(cmd)
    return result.returncode == 0

def find_latest_video(output_dir):
    """查找最新下载的视频文件"""
    videos = []
    for name in os.listdir(output_dir):
        path = os.path.join(output_dir, name)
        if os.path.isfile(path) and os.path.splitext(name)[1].lower() in VIDEO_EXTENSIONS:
            videos.append(path)
    return max(videos, key=os.path.getmtime) if videos else None

def generate_ed2k(file_path):
    """生成 ED2K 链接"""
    cmd = [RHASH_PATH, "--uppercase", "--ed2k-link", file_path]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
    return result.stdout.strip()

def parse_ed2k(ed2k_link):
    """解析 ED2K 链接"""
    decoded = urllib.parse.unquote(ed2k_link)
    parts = decoded.split("|")
    return parts[2], parts[3], parts[4].upper()

# =========================
# Excel 处理
# =========================

def load_or_create_excel(path):
    if os.path.exists(path):
        return pd.read_excel(path, engine="openpyxl")
    df = pd.DataFrame(columns=[
        "Index", "名字", "原文件名", "引用页",
        "大小", "散列", "主链接"
    ])
    df.to_excel(path, index=False, engine="openpyxl")
    return df

def get_next_index(df):
    if "Index" in df.columns and not df.empty:
        return int(df["Index"].dropna().iloc[-1]) + 1
    return 1

# =========================
# 主程序
# =========================

def main():
    df = load_or_create_excel(DEFAULT_EXCEL_PATH)

    while True:
        print("\n==============================")
        user_input = input(
            "请输入下载链接（可粘贴多行，回车用默认列表，q 退出）：\n"
        ).strip()

        if user_input.lower() == "q":
            print("程序已退出。")
            break

        urls = read_url_input(user_input)
        if not urls:
            print("未识别到有效链接。")
            continue

        output_dir = input(
            f"请输入下载目录（回车默认 {DEFAULT_OUTPUT_DIR}）："
        ).strip() or DEFAULT_OUTPUT_DIR
        os.makedirs(output_dir, exist_ok=True)

        for url in urls:
            print(f"\n处理链接: {url}")

            # 是否直接使用代理
            if need_proxy_first(url):
                print("命中代理白名单，直接使用代理下载。")
                success = run_ytdlp(url, output_dir, True)
            else:
                success = run_ytdlp(url, output_dir, False)
                if not success:
                    print("直连失败，切换代理重试。")
                    success = run_ytdlp(url, output_dir, True)

            if not success:
                print("下载失败，跳过该链接。")
                continue

            video_path = find_latest_video(output_dir)
            if not video_path:
                print("未找到视频文件。")
                continue

            ed2k = generate_ed2k(video_path)
            name, size, hash_value = parse_ed2k(ed2k)

            new_row = {
                "Index": get_next_index(df),
                "名字": name,
                "原文件名": os.path.basename(video_path),
                "引用页": url,
                "大小": format_size(size),
                "散列": hash_value,
                "主链接": ed2k
            }

            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_excel(DEFAULT_EXCEL_PATH, index=False, engine="openpyxl")

            print("已写入 Excel。")

        print("本轮完成。")

if __name__ == "__main__":
    main()
