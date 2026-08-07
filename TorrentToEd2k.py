# Torrent → ed2k 链接导出工具（合并版）。
# 模式 1 — 文件夹批量：遍历文件夹内所有 torrent，导出全部文件的 ed2k。
# 模式 2 — 未下载筛选：单 torrent 交互式导航，仅导出未下载成功的文件 ed2k。

import binascii
import signal
import subprocess
import sys
from pathlib import Path
from urllib.parse import quote

# ==================== 全局配置 ====================

DEFAULT_DOWNLOAD_DIR = Path(r"d:\Studios\Folders\Downloads")

# --- 消息常量 ---
MSG_TITLE = "=" * 60 + "\nTorrent → ed2k 链接导出工具\n" + "=" * 60

MSG_MENU = (
    "\n请选择模式：\n"
    "  1. 文件夹批量导出 — 遍历文件夹内所有 torrent，导出全部文件 ed2k\n"
    "  2. 未下载文件导出 — 单 torrent 交互导航，仅导出未下载文件 ed2k\n"
    "  0. 退出"
)
MSG_MENU_PROMPT = "\n请输入 (0-2): "
MSG_MENU_INVALID = "无效选项，请重新输入。"

# 模式 1 消息
MSG_M1_PROMPT_FOLDER = "请输入 torrent 文件夹 (默认: d:\\Studios\\Folders\\Downloads): "
MSG_M1_PROGRESS = "[{}/{}] 处理: {}"
MSG_M1_DONE = "已完成：共生成并复制 {} 条 ed2k 链接到剪贴板。"
MSG_M1_NO_ED2K = "未在任何 torrent 中找到 ed2k hash。"
MSG_M1_NO_TORRENT = "在文件夹中未找到 .torrent 文件。"
MSG_M1_SKIP = "    跳过（解析失败）: {} —— {}"

# 模式 2 消息
MSG_M2_PROMPT_TORRENT = "请输入 .torrent 文件路径: "
MSG_M2_PROMPT_DOWNLOAD = "请输入下载文件夹 (默认: d:\\Studios\\Folders\\Downloads): "
MSG_M2_READING = "\n读取 torrent: {}"
MSG_M2_DONE = "\n已完成：总 {} 个文件，未下载 {} 个，共生成并复制 {} 条 ed2k 链接到剪贴板。"
MSG_M2_NO_UNDOWNLOAD = "所选范围内所有文件均已下载成功，无需导出。"
MSG_M2_NO_ED2K = "未在 torrent 中找到任何 ed2k hash。"
MSG_M2_SINGLE_FILE = "\n单文件 torrent，直接检查下载状态。"
MSG_M2_TORRENT_ERROR = "解析 torrent 失败: {}"
MSG_M2_FILE_NOT_FOUND = "错误：文件不存在 —— {}"
MSG_M2_FOLDER_NOT_FOUND = "错误：文件夹不存在 —— {}"

# 导航交互
MSG_NAV_PATH = "\n当前路径: {}"
MSG_NAV_FILE_COUNT = "  (含 {} 个文件)"
MSG_NAV_TITLE = "请选择操作："
MSG_NAV_EXTRACT = "  0 - 检查当前文件夹及子文件夹下所有文件"
MSG_NAV_BACK = "  b - 返回上一层"
MSG_NAV_QUIT = "  q - 退出"
MSG_NAV_PROMPT = "选择 (0/1-{}, 默认 0): "
MSG_NAV_INVALID = "无效输入，请重新选择。"
MSG_NAV_ROOT = "（根目录）"
MSG_NAV_AT_DEEPEST = "  已到达最深层，检查当前文件夹。"

# 扫描状态
MSG_SCANNING = "正在对照下载文件夹检查文件..."
MSG_SCAN_RESULT = "  总文件: {}  已下载: {}  未下载: {}"

# 通用
MSG_CLIPBOARD_FAIL = "复制到剪贴板失败：{}"
MSG_BENCODER_MISSING = "缺少依赖库 bencodepy，请先执行: pip install bencodepy"
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

# ==================== 共享辅助函数 ====================

def safe_decode_filename(raw_bytes: bytes) -> str:
    """解码 torrent 中的文件名字段。UTF-8 → GBK 回退。"""
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
            errors="replace",
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

# ==================== 共享提取函数 ====================

def extract_ed2k_from_file_entry(f_entry, path_parts: list):
    """从单个文件条目提取 ed2k 链接对。
    返回 (raw_link, encoded_link) 或 (None, None)。"""
    if b"ed2k" not in f_entry:
        return None, None
    size = f_entry.get(b"length", 0)
    md4_hex = bytes_to_hex_upper(f_entry[b"ed2k"])
    name = sanitize_filename(path_parts)
    return build_ed2k_link(name, size, md4_hex), build_ed2k_link_percent(name, size, md4_hex)

# ==================== 模式 1：文件夹批量导出 ====================

def extract_all_ed2k_from_torrent(torrent_path: Path) -> tuple:
    """从单个 torrent 提取全部 ed2k 链接（不关心下载状态）。
    返回 (raw_links, encoded_links)。"""
    torrent = bencodepy.decode(torrent_path.read_bytes())
    info = torrent.get(b"info", {})
    links_raw = []
    links_encoded = []

    if b"files" in info:
        for f in info[b"files"]:
            raw_parts = f.get(b"path", [])
            decoded = [safe_decode_filename(p) for p in raw_parts]
            r, e = extract_ed2k_from_file_entry(f, decoded)
            if r:
                links_raw.append(r)
                links_encoded.append(e)
    else:
        for key in (b"ed2k", b"emulehash", b"filehash"):
            if key in info:
                name = safe_decode_filename(info.get(b"name", b""))
                r, e = extract_ed2k_from_file_entry(
                    {b"ed2k": info[key], b"length": info.get(b"length", 0)},
                    [name],
                )
                if r:
                    links_raw.append(r)
                    links_encoded.append(e)
                break

    return links_raw, links_encoded

def mode_folder_export() -> None:
    """模式 1：遍历文件夹内所有 torrent，导出全部文件 ed2k。"""
    raw = input(MSG_M1_PROMPT_FOLDER).strip()
    base_path = Path(raw) if raw else DEFAULT_DOWNLOAD_DIR

    torrent_list = sorted(base_path.glob("**/*.torrent"), key=lambda p: p.name)
    if not torrent_list:
        print(MSG_M1_NO_TORRENT)
        return

    total = len(torrent_list)
    all_clipboard_links = []

    for i, torrent_path in enumerate(torrent_list, 1):
        if _check_quit():
            print(MSG_INTERRUPTED)
            break

        print(MSG_M1_PROGRESS.format(i, total, torrent_path.name))

        try:
            raw_links, encoded_links = extract_all_ed2k_from_torrent(torrent_path)
        except Exception as e:
            print(MSG_M1_SKIP.format(torrent_path.name, e))
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
        print(MSG_M1_DONE.format(len(all_clipboard_links)))
    else:
        print(MSG_M1_NO_ED2K)

# ==================== 模式 2：未下载文件导出 ====================

def build_file_tree(files_info: list):
    """将 torrent 的文件列表构建为嵌套字典树。"""
    root = {"_files": []}
    for f_entry in files_info:
        raw_parts = f_entry.get(b"path", [])
        if not raw_parts:
            if b"ed2k" in f_entry:
                root["_files"].append(f_entry)
            continue
        parts = [safe_decode_filename(p) for p in raw_parts]
        node = root
        for i, part in enumerate(parts):
            if i == len(parts) - 1:
                if b"ed2k" in f_entry:
                    node.setdefault("_files", []).append(f_entry)
            else:
                node = node.setdefault(part, {"_files": []})
    return root

def list_subfolders(tree_node):
    return sorted(k for k in tree_node.keys() if not k.startswith("_"))

def file_count_in_subtree(tree_node):
    count = len(tree_node.get("_files", []))
    for key in tree_node.keys():
        if not key.startswith("_"):
            count += file_count_in_subtree(tree_node[key])
    return count

def is_file_downloaded(download_dir: Path, path_parts: list) -> bool:
    """检查文件是否已下载成功（无 .bc! 后缀）。"""
    if not path_parts:
        return False
    full_path = download_dir / Path(*path_parts)
    if full_path.is_file():
        return True
    bc_path = Path(str(full_path) + ".bc!")
    if bc_path.is_file():
        return False
    return False

def collect_undownloaded(tree_node, download_dir: Path):
    """递归收集未下载成功的文件条目。"""
    results = []
    for f_entry in tree_node.get("_files", []):
        decoded = [safe_decode_filename(p) for p in f_entry.get(b"path", [])]
        if not is_file_downloaded(download_dir, decoded):
            results.append((decoded, f_entry))
    for key, child in tree_node.items():
        if key.startswith("_"):
            continue
        results.extend(collect_undownloaded(child, download_dir))
    return results

def count_status_in_subtree(tree_node, download_dir: Path) -> tuple:
    """递归统计已下载/未下载数。返回 (total, downloaded, undownloaded)。"""
    total = downloaded = 0
    for f_entry in tree_node.get("_files", []):
        decoded = [safe_decode_filename(p) for p in f_entry.get(b"path", [])]
        total += 1
        if is_file_downloaded(download_dir, decoded):
            downloaded += 1
    for key, child in tree_node.items():
        if key.startswith("_"):
            continue
        ct, cd, _ = count_status_in_subtree(child, download_dir)
        total += ct
        downloaded += cd
    return total, downloaded, total - downloaded

def navigate_tree(tree_root):
    """交互式逐层导航文件夹树，返回选定子树节点和路径字符串。"""
    node = tree_root
    path_stack = []

    while True:
        subdirs = list_subfolders(node)
        file_count = file_count_in_subtree(node)

        path_str = " / ".join(d for d, _ in path_stack) if path_stack else MSG_NAV_ROOT
        print(MSG_NAV_PATH.format(path_str))
        print(MSG_NAV_FILE_COUNT.format(file_count))

        if not subdirs:
            print(MSG_NAV_AT_DEEPEST)
            return node, path_str

        print(MSG_NAV_TITLE)
        print(MSG_NAV_EXTRACT)
        if path_stack:
            print(MSG_NAV_BACK)
        print(MSG_NAV_QUIT)
        for j, sub in enumerate(subdirs, 1):
            sub_count = file_count_in_subtree(node[sub])
            print("  {} - {} ({} 文件)".format(j, sub, sub_count))

        choice = input(MSG_NAV_PROMPT.format(len(subdirs))).strip()

        if choice in ("", "0"):
            return node, path_str
        elif choice.lower() == "b" and path_stack:
            path_stack.pop()
            node = tree_root
            for _, dir_name in path_stack:
                node = node[dir_name]
            continue
        elif choice.lower() == "q":
            print(MSG_INTERRUPTED)
            return None, None
        else:
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(subdirs):
                    selected = subdirs[idx]
                    path_stack.append((selected, node[selected]))
                    node = node[selected]
                    continue
            except (ValueError, IndexError):
                pass
            print(MSG_NAV_INVALID)

def mode_undownload_export() -> None:
    """模式 2：单 torrent 交互导航，仅导出未下载文件 ed2k。"""
    while True:
        raw = input(MSG_M2_PROMPT_TORRENT).strip()
        if raw:
            break
        print("    请输入文件路径。")

    raw_path = Path(raw)
    if raw_path.is_dir():
        torrents = sorted(raw_path.glob("*.torrent"), key=lambda p: p.name)
        if not torrents:
            print(MSG_M2_FILE_NOT_FOUND.format("该文件夹下无 .torrent 文件"))
            return
        if len(torrents) == 1:
            torrent_path = torrents[0]
        else:
            print("\n文件夹内有多个 .torrent 文件：")
            for j, tp in enumerate(torrents, 1):
                print("  {} - {}".format(j, tp.name))
            choice = input("请选择 (1-{}, 默认 1): ".format(len(torrents))).strip()
            try:
                idx = int(choice) - 1 if choice else 0
                torrent_path = torrents[idx]
            except (ValueError, IndexError):
                torrent_path = torrents[0]
    else:
        torrent_path = raw_path

    if not torrent_path.is_file():
        print(MSG_M2_FILE_NOT_FOUND.format(torrent_path))
        return

    raw = input(MSG_M2_PROMPT_DOWNLOAD).strip()
    download_dir = Path(raw) if raw else DEFAULT_DOWNLOAD_DIR
    if not download_dir.is_dir():
        print(MSG_M2_FOLDER_NOT_FOUND.format(download_dir))
        return

    print(MSG_M2_READING.format(torrent_path))

    try:
        torrent = bencodepy.decode(torrent_path.read_bytes())
    except Exception as e:
        print(MSG_M2_TORRENT_ERROR.format(e))
        return

    info = torrent.get(b"info", {})
    selected_path_str = ""

    if b"files" not in info:
        # 单文件 torrent
        print(MSG_M2_SINGLE_FILE)
        name = safe_decode_filename(info.get(b"name", b""))
        target = download_dir / name
        bc_target = Path(str(target) + ".bc!")

        if target.is_file():
            print("  文件已下载成功: {}".format(name))
            print(MSG_M2_NO_UNDOWNLOAD)
            return
        if bc_target.is_file():
            print("  文件未完成（.bc!）: {}".format(name))
        else:
            print("  文件尚未开始下载: {}".format(name))

        undownloaded_entries = []
        for key in (b"ed2k", b"emulehash", b"filehash"):
            if key in info:
                undownloaded_entries.append(([name], {
                    b"ed2k": info[key],
                    b"length": info.get(b"length", 0),
                    b"path": [info.get(b"name", b"")],
                }))
                break
        total = undownloaded = 1
    else:
        # 多文件 torrent
        files_info = info[b"files"]
        tree_root = build_file_tree(files_info)
        selected_node, selected_path_str = navigate_tree(tree_root)
        if selected_node is None:
            return

        print(MSG_SCANNING)
        total, downloaded, undownloaded = count_status_in_subtree(selected_node, download_dir)
        print(MSG_SCAN_RESULT.format(total, downloaded, undownloaded))
        undownloaded_entries = collect_undownloaded(selected_node, download_dir)

    # 提取 ed2k
    links_raw, links_encoded = [], []
    for decoded_parts, f_entry in undownloaded_entries:
        r, e = extract_ed2k_from_file_entry(f_entry, decoded_parts)
        if r:
            links_raw.append(r)
            links_encoded.append(e)

    if not links_raw:
        print(MSG_M2_NO_UNDOWNLOAD)
        return

    stem = torrent_path.stem
    safe_path = selected_path_str.replace(" / ", "_").replace(" ", "_")
    output_name = "{}_{}_undownload".format(stem, safe_path) if safe_path else "{}_undownload".format(stem)

    (torrent_path.parent / "{}.txt".format(output_name)).write_text(
        "\n".join(links_raw), encoding="utf-8"
    )
    (torrent_path.parent / "{}.percent-encoding.txt".format(output_name)).write_text(
        "\n".join(links_encoded), encoding="utf-8"
    )

    copy_to_clipboard("\n".join(links_raw))
    print(MSG_M2_DONE.format(total, undownloaded, len(links_raw)))

# ==================== 主菜单 ====================

def main() -> None:
    _init_quit_handler()
    print(MSG_TITLE)

    while True:
        print(MSG_MENU)
        choice = input(MSG_MENU_PROMPT).strip()

        if choice == "1":
            mode_folder_export()
        elif choice == "2":
            mode_undownload_export()
        elif choice == "0":
            print("程序退出。")
            break
        else:
            print(MSG_MENU_INVALID)

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
