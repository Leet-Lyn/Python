# 请帮我写个中文的 Python 脚本，批注也是中文，但是变量参数不要是中文：
# 用 yt-dlp 下载媒体。
# 首先询问下载的链接（可粘贴多行，按回车则从默认列表文件读取“e:\Documents\Softwares\Codes\Python\Yt-dlpLists.txt”；输入本地文件路径则读取该文件）。
# 引入本地 cookies（Firefox 配置）。每个链接尝试 2 次：先直连，失败则走代理。
# 再询问下载后文件存放位置、Excel 记录文件位置。
# 每下载一个媒体，生成 Ed2K 链接，解析大小/散列，追加写入 Excel 一行。
# 反复循环，输入 Q 退出。

import signal
import os
import re
import subprocess
import sys
import urllib.parse
from pathlib import Path

import pandas as pd

# =========================
# 配置路径
# =========================

YTDLP_PATH = Path(r"D:\ProApps\yt-dlp\current\yt-dlp.exe")
FIREFOX_PROFILE = r"D:\ProApps\Firefox\current\profile"
BROWSER_COOKIES = f"firefox:{FIREFOX_PROFILE}" if FIREFOX_PROFILE else "firefox"
PROXY_URL = "http://127.0.0.1:10808"

DEFAULT_URL_LIST = Path(r"e:\Documents\Softwares\Codes\Python\Yt-dlpLists.txt")
DEFAULT_OUTPUT_DIR = Path(r"d:\Studios\Folders\Downloads\Yt-dlp")
DEFAULT_EXCEL_PATH = Path(r"d:\Studios\Folders\Downloads\Yt-dlp\Yt-dlp.xlsx")

RHASH_PATH = Path(r"d:\ProApps\rhash\current\rhash.exe")

VIDEO_EXTS = {
    ".mkv", ".avi", ".f4v", ".flv", ".ts", ".mpeg", ".mpg",
    ".rm", ".rmvb", ".asf", ".wmv", ".mov", ".webm", ".mp4",
}

_quit_requested = False  # Ctrl+Q 中断标志

# --- 消息常量 ---
MSG_INTERRUPTED = "\n\n用户中断程序，已退出。"
MSG_ERROR = "\n程序运行出错: {}"
MSG_EXIT = "\n按回车键退出..."
MSG_DOWNLOAD_MODE = "下载"
MSG_PROXY_MODE = "代理"
MSG_DIRECT_MODE = "直连"
MSG_ASK_URL = "请输入下载链接（可粘贴多行，回车用默认列表，Q 退出）：\n"
MSG_PROGRAM_EXIT = "程序已退出。"
MSG_NO_VALID_URL = "未识别到有效链接。"
MSG_ASK_DOWNLOAD_DIR = "请输入下载目录（回车默认 {}）："
MSG_PROCESSING_URL = "\n处理链接：{}"
MSG_PROXY_WHITELIST_HIT = "命中代理白名单，直接使用代理下载。"
MSG_DIRECT_FAILED_RETRY_PROXY = "直连失败，切换代理重试。"
MSG_DOWNLOAD_FAILED = "下载失败，跳过该链接。"
MSG_NO_MEDIA_FOUND = "未找到媒体文件。"
MSG_EXCEL_WRITTEN = "已写入 Excel。"
MSG_ROUND_COMPLETE = "本轮完成。"
MSG_ASK_EXCEL_PATH = "请输入Excel记录文件位置（回车默认 {}）："

# =========================
# 代理白名单（命中则直接用代理）
# =========================

PROXY_WHITELIST = ["youtube.com", "youtu.be"]


# =========================
# 工具函数
# =========================

def format_size(size_bytes: int) -> str:
    """字节数 → B / KB / MB / GB（4 位小数）。"""
    size = float(size_bytes)
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024:
            return f"{size:.4f} {unit}"
        size /= 1024
    return f"{size:.4f} TB"


def extract_urls(text: str) -> list[str]:
    """从文本中提取所有 http/https 链接。"""
    urls = re.findall(r"https?://[^\s]+", text)
    return [u.rstrip(";,") for u in urls]


def read_url_input(user_input: str) -> list[str]:
    """读取用户输入的链接或链接列表文件。"""
    if not user_input:
        if DEFAULT_URL_LIST.is_file():
            return extract_urls(DEFAULT_URL_LIST.read_text(encoding="utf-8"))
        return []

    path = Path(user_input.strip("\"'"))
    if path.is_file():
        return extract_urls(path.read_text(encoding="utf-8"))

    return extract_urls(user_input)


def need_proxy_first(url: str) -> bool:
    """判断是否需要直接使用代理（命中白名单）。"""
    url_lower = url.lower()
    return any(domain in url_lower for domain in PROXY_WHITELIST)


def run_ytdlp(url: str, output_dir: Path, use_proxy: bool) -> bool:
    """执行 yt-dlp 下载，返回是否成功。"""
    cmd = [
        str(YTDLP_PATH),
        "--cookies-from-browser", BROWSER_COOKIES,
        "-P", str(output_dir),
        "--write-thumbnail",
        "--convert-thumbnails", "jpg",
        "--write-subs",
        "--write-auto-subs",
        "--sub-langs", "all",
        "--sub-format", "srt",
        "--write-info-json",
        url,
    ]

    if use_proxy:
        cmd.extend(["--proxy", PROXY_URL])

    mode = MSG_PROXY_MODE if use_proxy else MSG_DIRECT_MODE
    print(f"{'=' * 10} {MSG_DOWNLOAD_MODE} {mode}: {url} {'=' * 10}")
    result = subprocess.run(cmd)
    return result.returncode == 0


def find_latest_video(output_dir: Path) -> Path | None:
    """查找 output_dir 下最近修改的媒体文件。"""
    videos = [
        p for p in output_dir.iterdir()
        if p.is_file() and p.suffix.lower() in VIDEO_EXTS
    ]
    return max(videos, key=lambda p: p.stat().st_mtime) if videos else None


def generate_ed2k(file_path: Path) -> str:
    """使用 RHash 生成 ED2K 链接。"""
    cmd = [str(RHASH_PATH), "--uppercase", "--ed2k-link", str(file_path)]
    result = subprocess.run(
        cmd,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    return result.stdout.strip()


def parse_ed2k(ed2k_link: str) -> tuple[str, str, str]:
    """解析 ED2K 链接，返回 (文件名, 大小, 散列)。"""
    decoded = urllib.parse.unquote(ed2k_link)
    parts = decoded.split("|")
    return parts[2], parts[3], parts[4].upper()


# =========================
# Excel 处理
# =========================

def load_or_create_excel(path: Path) -> pd.DataFrame:
    """加载现有 Excel，不存在则创建含表头的新文件。"""
    if path.is_file():
        return pd.read_excel(path, engine="openpyxl")
    df = pd.DataFrame(columns=[
        "Index", "名字", "原文件名", "引用页",
        "大小", "散列", "主链接",
    ])
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(path, index=False, engine="openpyxl")
    return df


def get_next_index(df: pd.DataFrame) -> int:
    """获取下一条记录的 Index 值。"""
    if "Index" in df.columns and not df.empty:
        last = df["Index"].dropna()
        return int(last.iloc[-1]) + 1 if not last.empty else 1
    return 1


# =========================
# 主程序
# =========================
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
    """主循环：输入链接 → 下载 → Ed2K → 写入 Excel。"""
    while True:
        print("\n" + "=" * 30)
        user_input = input(MSG_ASK_URL).strip()

        if user_input.lower() == "q":
            print(MSG_PROGRAM_EXIT)
            break

        urls = read_url_input(user_input)
        if not urls:
            print(MSG_NO_VALID_URL)
            continue

        raw_dir = input(
            MSG_ASK_DOWNLOAD_DIR.format(DEFAULT_OUTPUT_DIR)
        ).strip()
        output_dir = Path(raw_dir) if raw_dir else DEFAULT_OUTPUT_DIR
        output_dir.mkdir(parents=True, exist_ok=True)

        raw_excel = input(
            MSG_ASK_EXCEL_PATH.format(DEFAULT_EXCEL_PATH)
        ).strip()
        excel_path = Path(raw_excel) if raw_excel else DEFAULT_EXCEL_PATH

        df = load_or_create_excel(excel_path)

        for url in urls:
            print(MSG_PROCESSING_URL.format(url))

            # 下载（白名单直接代理，否则先直连再代理重试）
            if need_proxy_first(url):
                print(MSG_PROXY_WHITELIST_HIT)
                success = run_ytdlp(url, output_dir, True)
            else:
                success = run_ytdlp(url, output_dir, False)
                if not success:
                    print(MSG_DIRECT_FAILED_RETRY_PROXY)
                    success = run_ytdlp(url, output_dir, True)

            if not success:
                print(MSG_DOWNLOAD_FAILED)
                continue

            video_path = find_latest_video(output_dir)
            if video_path is None:
                print(MSG_NO_MEDIA_FOUND)
                continue

            ed2k = generate_ed2k(video_path)
            name, size_bytes, hash_value = parse_ed2k(ed2k)

            new_row = {
                "Index": get_next_index(df),
                "名字": name,
                "原文件名": video_path.name,
                "引用页": url,
                "大小": format_size(int(size_bytes)),
                "散列": hash_value,
                "主链接": ed2k,
            }

            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_excel(excel_path, index=False, engine="openpyxl")
            print(MSG_EXCEL_WRITTEN)

        print(MSG_ROUND_COMPLETE)


# =========================
# 程序入口
# =========================

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
