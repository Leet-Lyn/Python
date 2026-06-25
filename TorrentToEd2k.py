# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源 torrent 文件所在文件夹（默认 d:\Studios\Folders\Downloads\）。
# 依次读取该文件夹下所有 torrent 文件，生成同名的两个 txt 文件（分别后缀名为".txt"与".percent-encoding.txt"）。
# 读取每个 torrent 文件，提取每一个 ed2k hash 生成 ed2k 链接。要求 Hash 大写，分别写入这两个 txt 文件。
# ".txt" 里的链接不转为 Percent-encoding，".percent-encoding.txt" 里的链接转为 Percent-encoding。二者链接数量相同。
# 同时将不转为 Percent-encoding 的 ed2k 链接写入剪贴板。

import signal
import binascii
import subprocess
import sys
from pathlib import Path
from urllib.parse import quote

import bencodepy

# --- 常量 ---

_quit_requested = False  # Ctrl+Q 中断标志

# --- 消息常量 ---
MSG_INTERRUPTED = "\n\n用户中断程序，已退出。"
MSG_ERROR = "\n程序运行出错: {}"
MSG_EXIT = "\n按回车键退出..."
MSG_CLIPBOARD_FAIL = "复制到剪贴板失败：{}"
MSG_PROMPT_FOLDER = (
    "请输入 torrent 文件所在文件夹（默认 d:\\Studios\\Folders\\Downloads\\）："
)
MSG_DONE = "已完成：共生成并复制 {} 条 ed2k 链接到剪贴板。"
MSG_NO_ED2K = "未在任何 torrent 中找到 ed2k hash。"


def bytes_to_hex_upper(data: bytes) -> str:
    """将二进制 MD4 hash 转为大写 HEX 字符串。"""
    return binascii.hexlify(data).decode().upper()


def build_ed2k_link(filename: str, size: int, md4_hex: str) -> str:
    """生成不做 Percent-encoding 的 ed2k 链接。"""
    return f"ed2k://|file|{filename}|{size}|{md4_hex}|/"


def build_ed2k_link_percent(filename: str, size: int, md4_hex: str) -> str:
    """生成做 Percent-encoding 的 ed2k 链接。"""
    return f"ed2k://|file|{quote(filename, safe='')}|{size}|{md4_hex}|/"


def sanitize_filename(path_parts: list[str]) -> str:
    """将文件路径拼接，并将所有路径分隔符替换为下划线。"""
    return "_".join(p.replace("/", "_").replace("\\", "_") for p in path_parts)


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


def extract_ed2k_from_torrent(torrent_path: Path) -> tuple[list[str], list[str]]:
    """
    从单个 torrent 文件中提取 ed2k 链接。
    返回 (原始链接列表, Percent-encoding 链接列表)。
    """
    torrent = bencodepy.decode(torrent_path.read_bytes())
    info = torrent.get(b"info", {})
    links_raw: list[str] = []
    links_encoded: list[str] = []

    # 多文件 torrent
    if b"files" in info:
        for f in info[b"files"]:
            if b"ed2k" not in f:
                continue
            size = f[b"length"]
            md4_hex = bytes_to_hex_upper(f[b"ed2k"])
            filename = sanitize_filename(
                [p.decode(errors="ignore") for p in f[b"path"]]
            )
            links_raw.append(build_ed2k_link(filename, size, md4_hex))
            links_encoded.append(build_ed2k_link_percent(filename, size, md4_hex))

    # 单文件 torrent（BitComet 私有字段）
    else:
        for key in (b"ed2k", b"emulehash", b"filehash"):
            if key in info:
                size = info.get(b"length", 0)
                md4_hex = bytes_to_hex_upper(info[key])
                name = info.get(b"name", b"").decode(errors="ignore")
                filename = sanitize_filename([name])
                links_raw.append(build_ed2k_link(filename, size, md4_hex))
                links_encoded.append(build_ed2k_link_percent(filename, size, md4_hex))
                break

    return links_raw, links_encoded
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
    """主流程：输入文件夹 → 遍历 torrent → 生成 txt → 写入剪贴板。"""
    raw = input(MSG_PROMPT_FOLDER).strip()
    base_path = Path(raw) if raw else Path(r"d:\Studios\Folders\Downloads")

    all_clipboard_links: list[str] = []

    for torrent_path in sorted(base_path.glob("*.torrent")):
        raw_links, encoded_links = extract_ed2k_from_torrent(torrent_path)
        if not raw_links:
            continue

        stem = torrent_path.stem
        (base_path / f"{stem}.txt").write_text(
            "\n".join(raw_links), encoding="utf-8"
        )
        (base_path / f"{stem}.percent-encoding.txt").write_text(
            "\n".join(encoded_links), encoding="utf-8"
        )
        all_clipboard_links.extend(raw_links)

    if all_clipboard_links:
        copy_to_clipboard("\n".join(all_clipboard_links))
        print(MSG_DONE.format(len(all_clipboard_links)))
    else:
        print(MSG_NO_ED2K)



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
