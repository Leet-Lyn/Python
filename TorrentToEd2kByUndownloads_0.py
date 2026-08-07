# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源 torrent 地址。与下载的文件夹位置（默认 d:\Studios\Folders\Downloads\）。
# 筛选 torrent 内文件夹，并且匹配“*.bc!”文件。
# 读取该 torrent 文件，生成同名的两个 txt 文件（分别后缀名为".txt"与".percent-encoding.txt"）。
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
DEFAULT_DOWNLOAD_DIR = Path(r"d:\Studios\Folders\Downloads")

# --- 消息常量 ---
MSG_PROMPT_TORRENT = "请输入 .torrent 文件路径: "
MSG_PROMPT_DOWNLOAD = "请输入下载文件夹路径 (默认: d:\\Studios\\Folders\\Downloads): "
MSG_READING = "\n读取 torrent: {}"
MSG_FILE_NOT_FOUND = "错误：文件不存在 —— {}"
MSG_FOLDER_NOT_FOUND = "错误：文件夹不存在 —— {}"
MSG_DONE = "\n已完成：总 {} 个文件，未下载 {} 个，共生成并复制 {} 条 ed2k 链接到剪贴板。"
MSG_NO_UNDOWNLOAD = "自定义文件夹内所有文件均已下载成功，无需导出。"
MSG_NO_ED2K = "未在 torrent 中找到任何 ed2k hash。"
MSG_SINGLE_FILE = "\n单文件 torrent，直接检查下载状态。"
MSG_CLIPBOARD_FAIL = "复制到剪贴板失败：{}"
MSG_TORRENT_ERROR = "解析 torrent 失败: {}"
MSG_BENCODER_MISSING = "缺少依赖库 bencodepy，请先执行: pip install bencodepy"
MSG_INTERRUPTED = "\n\n用户中断程序，已退出。"
MSG_ERROR = "\n程序运行出错: {}"
MSG_EXIT = "\n按回车键退出..."

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


# ==================== 树形结构 ====================

def build_file_tree(files_info: list):
    """将 torrent 的文件列表构建为嵌套字典树。
    每个节点形如 {"_files": [file_entries], "subdir": {...}}
    返回根节点 dict。"""
    root = {"_files": []}

    for f_entry in files_info:
        raw_parts = f_entry.get(b"path", [])
        if not raw_parts:
            if b"ed2k" in f_entry:
                root["_files"].append(f_entry)
            continue

        parts = [safe_decode_filename(p) for p in raw_parts]
        if not parts:
            root["_files"].append(f_entry)
            continue

        node = root
        for i, part in enumerate(parts):
            if i == len(parts) - 1:
                if b"ed2k" in f_entry:
                    node.setdefault("_files", []).append(f_entry)
            else:
                node = node.setdefault(part, {"_files": []})

    return root


def list_subfolders(tree_node):
    """列出当前节点的子文件夹名（排序）。"""
    return sorted(k for k in tree_node.keys() if not k.startswith("_"))


def file_count_in_subtree(tree_node):
    """递归统计子树中的文件数。"""
    count = len(tree_node.get("_files", []))
    for key in tree_node.keys():
        if not key.startswith("_"):
            count += file_count_in_subtree(tree_node[key])
    return count


# ==================== 下载状态检查 ====================

def is_file_downloaded(download_dir: Path, path_parts: list) -> bool:
    """检查文件是否已下载成功（无 .bc! 后缀）。
    path_parts 是已解码的路径分量列表 ["dir", "file.ext"]。
    返回 True 表示已下载成功，False 表示未下载或仅存在 .bc!。"""
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
    """递归遍历子树，收集未下载成功的文件条目。
    返回 [(decoded_parts, file_entry), ...] 列表。"""
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
    """递归统计子树中已下载和未下载的文件数。
    返回 (total, downloaded, undownloaded)。"""
    total = 0
    downloaded = 0

    for f_entry in tree_node.get("_files", []):
        decoded = [safe_decode_filename(p) for p in f_entry.get(b"path", [])]
        total += 1
        if is_file_downloaded(download_dir, decoded):
            downloaded += 1

    for key, child in tree_node.items():
        if key.startswith("_"):
            continue
        ct, cd, cu = count_status_in_subtree(child, download_dir)
        total += ct
        downloaded += cd

    return total, downloaded, total - downloaded


# ==================== 提取函数 ====================

def extract_ed2k_from_entries(entries):
    """从 [(decoded_parts, file_entry), ...] 提取 ed2k 链接。
    返回 (原始链接列表, Percent-encoding 链接列表)。"""
    links_raw = []
    links_encoded = []

    for decoded_parts, f_entry in entries:
        if b"ed2k" not in f_entry:
            continue
        size = f_entry.get(b"length", 0)
        md4_hex = bytes_to_hex_upper(f_entry[b"ed2k"])
        name = sanitize_filename(decoded_parts)
        links_raw.append(build_ed2k_link(name, size, md4_hex))
        links_encoded.append(build_ed2k_link_percent(name, size, md4_hex))

    return links_raw, links_encoded


# ==================== 导航交互 ====================

def navigate_tree(tree_root):
    """交互式逐层导航文件夹树，返回用户最终选定的子树节点和显示路径。
    返回 (selected_node, path_str)，用户退出时返回 (None, None)。"""
    node = tree_root
    path_stack = []  # [(display_name, tree_node), ...]

    while True:
        subdirs = list_subfolders(node)
        file_count = file_count_in_subtree(node)

        if path_stack:
            path_str = " / ".join(d for d, _ in path_stack)
        else:
            path_str = MSG_NAV_ROOT
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

        choice = input(
            MSG_NAV_PROMPT.format(len(subdirs))
        ).strip()

        if choice == "" or choice == "0":
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


# ==================== 主程序 ====================

def main() -> None:
    """主流程：输入 torrent → 输入下载文件夹 → 导航树 →
    检查下载状态 → 提取未下载文件的 ed2k → 生成 txt → 剪贴板。"""
    _init_quit_handler()

    # 输入 torrent 文件路径
    while True:
        raw = input(MSG_PROMPT_TORRENT).strip()
        if raw:
            break
        print("    请输入文件路径。")

    raw_path = Path(raw)
    if raw_path.is_dir():
        torrents = sorted(raw_path.glob("*.torrent"), key=lambda p: p.name)
        if not torrents:
            print(MSG_FILE_NOT_FOUND.format("该文件夹下无 .torrent 文件"))
            return
        if len(torrents) == 1:
            torrent_path = torrents[0]
        else:
            print("\n文件夹内有多个 .torrent 文件：")
            for j, tp in enumerate(torrents, 1):
                print("  {} - {}".format(j, tp.name))
            choice = input(
                "请选择 (1-{}, 默认 1): ".format(len(torrents))
            ).strip()
            try:
                idx = int(choice) - 1 if choice else 0
                torrent_path = torrents[idx]
            except (ValueError, IndexError):
                torrent_path = torrents[0]
    else:
        torrent_path = raw_path

    if not torrent_path.is_file():
        print(MSG_FILE_NOT_FOUND.format(torrent_path))
        return

    # 输入下载文件夹路径
    raw = input(MSG_PROMPT_DOWNLOAD).strip()
    download_dir = Path(raw) if raw else DEFAULT_DOWNLOAD_DIR
    if not download_dir.is_dir():
        print(MSG_FOLDER_NOT_FOUND.format(download_dir))
        return

    print(MSG_READING.format(torrent_path))

    try:
        torrent = bencodepy.decode(torrent_path.read_bytes())
    except Exception as e:
        print(MSG_TORRENT_ERROR.format(e))
        return

    info = torrent.get(b"info", {})

    # 单文件 torrent（BitComet 私有字段）
    if b"files" not in info:
        print(MSG_SINGLE_FILE)
        selected_path_str = ""

        name = safe_decode_filename(info.get(b"name", b""))
        target = download_dir / name
        bc_target = Path(str(target) + ".bc!")

        if target.is_file():
            print("  文件已下载成功: {}".format(name))
            print(MSG_NO_UNDOWNLOAD)
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
                    b"path": [info.get(b"name", b"")]
                }))
                break
        total = 1
        undownloaded = 1
    else:
        # 多文件 torrent：构建树并交互导航
        files_info = info[b"files"]
        tree_root = build_file_tree(files_info)
        selected_node, selected_path_str = navigate_tree(tree_root)
        if selected_node is None:
            return

        # 扫描下载状态（path_parts 已是 torrent 内完整相对路径，直接拼 download_dir）
        print(MSG_SCANNING)
        total, downloaded, undownloaded = count_status_in_subtree(
            selected_node, download_dir
        )
        print(MSG_SCAN_RESULT.format(total, downloaded, undownloaded))
        undownloaded_entries = collect_undownloaded(selected_node, download_dir)

    # 提取 ed2k 链接
    links_raw, links_encoded = extract_ed2k_from_entries(undownloaded_entries)

    if not links_raw:
        print(MSG_NO_UNDOWNLOAD)
        return

    # 生成输出文件名
    stem = torrent_path.stem
    safe_path = selected_path_str.replace(" / ", "_").replace(" ", "_")
    if safe_path:
        output_name = "{}_{}_undownload".format(stem, safe_path)
    else:
        output_name = "{}_undownload".format(stem)

    (torrent_path.parent / "{}.txt".format(output_name)).write_text(
        "\n".join(links_raw), encoding="utf-8"
    )
    (torrent_path.parent / "{}.percent-encoding.txt".format(output_name)).write_text(
        "\n".join(links_encoded), encoding="utf-8"
    )

    copy_to_clipboard("\n".join(links_raw))
    print(MSG_DONE.format(total, undownloaded, len(links_raw)))


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
