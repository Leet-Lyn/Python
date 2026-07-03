# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源 torrent 文件所在文件夹（默认 d:\Studios\Folders\Downloads\）。
# 依次读取该文件夹下所有 torrent 文件，生成同名的两个 txt 文件（分别后缀名为".txt"与".percent-encoding.txt"）。
# 读取每个 torrent 文件，提取每一个 ed2k hash 生成 ed2k 链接。要求 Hash 大写，分别写入这两个 txt 文件。
# ".txt" 里的链接不转为 Percent-encoding，".percent-encoding.txt" 里的链接转为 Percent-encoding。二者链接数量相同。
# 同时将不转为 Percent-encoding 的 ed2k 链接写入剪贴板。

# 导入模块
import signal
import binascii
import subprocess
import sys
from pathlib import Path
from urllib.parse import quote

# ==================== 全局配置 ====================

# --- 默认路径 ---
DEFAULT_SOURCE_DIR = Path(r"d:\Studios\Folders\Downloads")

# --- 消息常量 ---
MSG_PROMPT_FOLDER = "请输入 torrent 文件所在文件夹 (默认: d:\\Studios\\Folders\\Downloads): "
MSG_PROGRESS = "[{}/{}] 处理: {}"
MSG_DONE = "已完成：共生成并复制 {} 条 ed2k 链接到剪贴板。"
MSG_NO_ED2K = "未在任何 torrent 中找到 ed2k hash。"
MSG_NO_TORRENT = "在文件夹中未找到 .torrent 文件。"
MSG_BENCODER_MISSING = "缺少依赖库 bencodepy，请先执行: pip install bencodepy"
MSG_CLIPBOARD_FAIL = "复制到剪贴板失败：{}"
MSG_TORRENT_SKIP = "    跳过（解析失败）: {} —— {}"
MSG_INTERRUPTED = "\n\n用户中断程序，已退出。"
MSG_ERROR = "\n程序运行出错: {}"
MSG_EXIT = "\n按回车键退出..."

# ==================== 中断处理 ====================

_quit_requested = False


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


# ==================== 辅助函数 ====================

def safe_decode_filename(raw_bytes: bytes) -> str:
    """解码 torrent 中的文件名字段。先尝试 UTF-8，失败则回退 GBK。"""
    try:
        return raw_bytes.decode("utf-8")
    except UnicodeDecodeError:
        try:
            return raw_bytes.decode("gbk", errors="replace")
        except Exception:
            return raw_bytes.decode("utf-8", errors="replace")


def bytes_to_hex_upper(data: bytes) -> str:
    """二进制 MD4 hash → 大写 HEX 字符串。"""
    return binascii.hexlify(data).decode().upper()


def build_ed2k_link(name: str, size: int, md4_hex: str) -> str:
    """生成不做 Percent-encoding 的 ed2k 链接。"""
    return "ed2k://|file|{}|{}|{}|/".format(name, size, md4_hex)


def build_ed2k_link_percent(name: str, size: int, md4_hex: str) -> str:
    """生成做 Percent-encoding 的 ed2k 链接。"""
    return "ed2k://|file|{}|{}|{}|/".format(quote(name, safe=""), size, md4_hex)


def sanitize_filename(path_parts: list) -> str:
    """路径拼接，替换 ed2k 和 Windows 非法字符为下划线。"""
    _ILLEGAL = str.maketrans({
        '|': '_', '/': '_', '\\': '_',
        ':': '_', '<': '_', '>': '_',
        '"': '_', '?': '_', '*': '_',
    })
    return "_".join(str(p).translate(_ILLEGAL) for p in path_parts)


def copy_to_clipboard(text: str) -> None:
    """文本 → Windows 剪贴板。优先 .NET Clipboard，静默回退 clip.exe。"""
    try:
        subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "Add-Type -AssemblyName System.Windows.Forms;"
             "[System.Windows.Forms.Clipboard]::SetText($Input)"],
            input=text,
            encoding="utf-8",
            capture_output=True,
            check=True,
        )
    except Exception:
        try:
            subprocess.run(
                ["clip.exe"],
                input=text,
                encoding="utf-8",
                errors="ignore",
                check=True,
            )
        except Exception as e:
            print(MSG_CLIPBOARD_FAIL.format(e))


# ==================== 处理函数 ====================

def extract_ed2k_from_torrent(torrent_path: Path) -> tuple:
    """从单个 torrent 提取 ed2k 链接。
    返回 (原始链接列表, Percent-encoding 链接列表)。"""
    torrent = bencodepy.decode(torrent_path.read_bytes())
    info = torrent.get(b"info", {})
    links_raw = []
    links_encoded = []

    # 多文件 torrent
    if b"files" in info:
        for f in info[b"files"]:
            if b"ed2k" not in f:
                continue
            size = f.get(b"length", 0)
            md4_hex = bytes_to_hex_upper(f[b"ed2k"])
            raw_parts = f.get(b"path", [])
            name = sanitize_filename(
                safe_decode_filename(p) for p in raw_parts
            )
            links_raw.append(build_ed2k_link(name, size, md4_hex))
            links_encoded.append(build_ed2k_link_percent(name, size, md4_hex))

    # 单文件 torrent（BitComet 私有字段 ed2k / emulehash / filehash）
    else:
        for key in (b"ed2k", b"emulehash", b"filehash"):
            if key in info:
                size = info.get(b"length", 0)
                md4_hex = bytes_to_hex_upper(info[key])
                name = safe_decode_filename(info.get(b"name", b""))
                filename = sanitize_filename([name])
                links_raw.append(build_ed2k_link(filename, size, md4_hex))
                links_encoded.append(
                    build_ed2k_link_percent(filename, size, md4_hex)
                )
                break

    return links_raw, links_encoded


# ==================== 主程序 ====================

def main() -> None:
    """主流程：输入文件夹 → 遍历 torrent → 生成 txt → 写入剪贴板。"""
    _init_quit_handler()

    raw = input(MSG_PROMPT_FOLDER).strip()
    base_path = Path(raw) if raw else DEFAULT_SOURCE_DIR

    torrent_list = sorted(base_path.glob("**/*.torrent"), key=lambda p: p.name)
    if not torrent_list:
        print(MSG_NO_TORRENT)
        return

    total = len(torrent_list)
    all_clipboard_links = []

    for i, torrent_path in enumerate(torrent_list, 1):
        if _check_quit():
            print(MSG_INTERRUPTED)
            break

        print(MSG_PROGRESS.format(i, total, torrent_path.name))

        try:
            raw_links, encoded_links = extract_ed2k_from_torrent(torrent_path)
        except Exception as e:
            print(MSG_TORRENT_SKIP.format(torrent_path.name, e))
            continue

        if not raw_links:
            continue

        stem = torrent_path.stem
        (torrent_path.parent / "{}.txt".format(stem)).write_text(
            "\n".join(raw_links), encoding="utf-8"
        )
        (torrent_path.parent / "{}.percent-encoding.txt".format(stem)).write_text(
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
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    try:
        import bencodepy  # noqa: F401
    except ImportError:
        print(MSG_BENCODER_MISSING)
        input(MSG_EXIT)
        sys.exit(1)
    try:
        main()
    except KeyboardInterrupt:
        print(MSG_INTERRUPTED)
    except Exception as e:
        print(MSG_ERROR.format(e))
    finally:
        input(MSG_EXIT)
