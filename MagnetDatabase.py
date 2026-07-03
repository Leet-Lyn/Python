# 请帮我写个中文的 Python 脚本，批注也是中文，但是变量参数不要是中文：
# 在脚本开始前让我选择：1. Torrents 文件夹写入 Magnet 数据库；2. 多行 Magnet 链接写入数据库；3. 多行 Magnet 链接从数据库删除；4. 多行 Magnet 值从数据库删除；5. 整理数据库；0. 退出。
# 1. Torrents 文件夹写入 Magnet 数据库：
# 询问我源文件夹位置（默认为：d:\Studios\Folders\Downloads\）。 写入文件夹位置（默认为：d:\Studios\Folders\Ins\）, 删除文件夹位置（默认为：d:\Studios\Folders\Deletes\）。Magnet 数据库文件位置（默认为：e:\Documents\Softwares\Codes\Attachments\Databases\Magnet\Magnet.txt）。
# 遍历源文件夹内所有 torrent 文件及子文件夹中的 torrent 文件，顺序完成。
# 将 torrent 提取出 Magnet 链接（Hex 格式），导出其 40 位十六进制（SHA-1 Hash），为 Magnet 值。
# 比对 Magnet 数据库文件（Magnet 数据库文件，每一行为一个文件的 Magnet 值。）如果当前文件的 Magnet 值在原来 Magnet 数据库文件里存在，则将该文件移动到删除文件夹，选择下一个文件。
# 如果当前文件的 Magnet 值不在原来 Magnet 数据库文件里存在，则添加该文件的 Magnet 值到 Magnet 数据库文件末尾（另起一行），保存 Magnet 数据库文件。将该torrent 文件安装文件夹子文件夹结构，移动到写入文件夹位置，
# 直至源文件夹内所有文件及子文件夹中的文件都处理好结束。最后整理哪些文件 Magnet 值原数据库存在，移动到删除文件夹里。并将这些文件列表打印在屏幕上并复制到剪贴板上去。
# 2. 多行 Magnet 链接写入数据库：
# 询问我 Magnet 数据库文件位置（默认为：e:\Documents\Softwares\Codes\Attachments\Databases\Magnet\Magnet.txt）。读取剪贴板数据，其为多行 Magnet 链接（每行一个 Magnet 链接），顺序读取每一行 Magnet 链接，（如非 Hex 格式的链接转成 Hex 格式的链接）。导出其 40 位十六进制（SHA-1 Hash），为 Magnet 值。
# 比对 Magnet 数据库文件（Magnet 数据库文件，每一行为一个文件的 Magnet 值。）
# 如果当前 Magnet 值在原来 Magnet 数据库文件里存在，报告我。
# 如果当前 Magnet 值不在原来 Magnet 数据库文件里存在，则添加该 Magnet 值到 Magnet 数据库文件末尾（另起一行），保存 Magnet 数据库文件。
# 最后整理哪些 Magnet 链接的 Magnet 值原数据库存在。并将这些文件列表打印在屏幕上并复制到剪贴板上去。
# 3. 多行 Magnet 链接从数据库删除：
# 询问我 Magnet 数据库文件位置（默认为：e:\Documents\Softwares\Codes\Attachments\Databases\Magnet\Magnet.txt）。读取剪贴板数据，其为多行 Magnet 链接（每行一个 Magnet 链接），顺序读取每一行 Magnet 链接，（如非 Hex 格式的链接转成 Hex 格式的链接）。导出其 40 位十六进制（SHA-1 Hash），为 Magnet 值。
# 比对 Magnet 数据库文件（Magnet 数据库文件，每一行为一个文件的 Magnet 值。）
# 如果当前 Magnet 值在原来 Magnet 数据库文件里存在，则将该 Magnet 值从原来 Magnet 数据库文件里删除。
# 如果当前 Magnet 值不在原来 Magnet 数据库文件里存在，则报告我。
# 4. 多行 Magnet 值从数据库删除：
# 询问我 Magnet 数据库文件位置（默认为：e:\Documents\Softwares\Codes\Attachments\Databases\Magnet\Magnet.txt）。读取剪贴板数据，其为多行 Magnet 值（每行一个 Magnet 值），顺序读取每一行 Magnet 链接。
# 比对 Magnet 数据库文件（Magnet 数据库文件，每一行为一个文件的 Magnet 值。）
# 如果当前 Magnet 值在原来 Magnet 数据库文件里存在，则将该 Magnet 值从原来 Magnet 数据库文件里删除。
# 如果当前 Magnet 值不在原来 Magnet 数据库文件里存在，则报告我。
# 5. 整理数据库：
# 询问我 Magnet 数据库文件位置（默认为：e:\Documents\Softwares\Codes\Attachments\Databases\Magnet\Magnet.txt）。对 Magnet 数据库，先备份，再对文件里的 Magnet 值（字符串）从小到大排序。
# 完成后，反复循环至最开始。

# 导入模块
import hashlib
import re
import signal
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

import bencodepy

# ==================== 剪贴板 ====================

def copy_to_clipboard(text: str) -> None:
    """复制文本到 Windows 剪贴板。优先 PowerShell，静默回退 clip.exe。"""
    try:
        # 优先使用 PowerShell 的 .NET Clipboard，避免 Set-Clipboard 对大文本限制
        subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "Add-Type -AssemblyName System.Windows.Forms;"
             "[System.Windows.Forms.Clipboard]::SetText($Input)"],
            input=text,
            encoding="utf-8",
            capture_output=True,
            check=True,
        )
        print(MSG_CLIPBOARD_COPIED)
    except Exception:
        # 静默回退到 clip.exe（UTF-8，现代 Windows 兼容）
        try:
            subprocess.run(
                ["clip.exe"],
                input=text,
                encoding="utf-8",
                errors="ignore",
                check=True,
            )
            print(MSG_CLIPBOARD_COPIED)
        except Exception as e:
            print(MSG_CLIPBOARD_COPY_FAIL.format(e))


def get_clipboard_text() -> str:
    """从剪贴板获取文本。强制 PowerShell 输出 UTF-8。"""
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "[Console]::OutputEncoding=[Text.Encoding]::UTF8;Get-Clipboard -Raw"],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            check=True,
        )
        return result.stdout or ""
    except Exception:
        print(MSG_CLIPBOARD_READ_FAIL)
        return ""


# ==================== 全局配置 ====================

DEFAULT_SOURCE_DIR = Path(r"d:\Studios\Folders\Downloads")
DEFAULT_WRITE_DIR = Path(r"d:\Studios\Folders\Ins")
DEFAULT_DELETE_DIR = Path(r"d:\Studios\Folders\Deletes")
DEFAULT_MAGNET_DB = Path(r"e:\Documents\Softwares\Codes\Attachments\Databases\Magnet\Magnet.txt")

HIDDEN_FILE_PATTERNS = [
    "desktop.ini", "descript.ion", ".encfs6.xml", "Thumbs.db",
    ".DS_Store", "._*",
]

# --- 消息常量 ---

# 程序退出相关
MSG_INTERRUPTED = "\n\n用户中断程序，已退出。"
MSG_ERROR = "\n程序运行出错: {}"
MSG_EXIT = "\n按回车键退出..."

# 剪贴板相关
MSG_CLIPBOARD_COPIED = "已复制到剪贴板。"
MSG_CLIPBOARD_COPY_FAIL = "复制到剪贴板失败: {}"
MSG_CLIPBOARD_READ_FAIL = "无法读取剪贴板。"

# 主菜单
MSG_MENU_TITLE = "Torrent/Magnet 数据库管理工具"
MSG_MENU_CHOICE_PROMPT = "请输入选项 (0-5): "
MSG_MENU_1 = "1. Torrents 文件夹写入 Magnet 数据库"
MSG_MENU_2 = "2. 多行 Magnet 链接写入数据库"
MSG_MENU_3 = "3. 多行 Magnet 链接从数据库删除"
MSG_MENU_4 = "4. 多行 Magnet 值从数据库删除"
MSG_MENU_5 = "5. 整理数据库（排序去重）"
MSG_MENU_0 = "0. 退出"
MSG_MENU_INVALID = "无效选项，请重新输入。"
MSG_MENU_EXIT = "程序退出。"
MSG_MENU_CONTINUE = "\n按回车键继续..."

# 输入提示
MSG_PROMPT_DEFAULT_FMT = "{} (默认: {}): "
MSG_PROMPT_SOURCE_DIR = "源文件夹位置"
MSG_PROMPT_WRITE_DIR = "写入文件夹位置"
MSG_PROMPT_DELETE_DIR = "删除文件夹位置"
MSG_PROMPT_MAGNET_DB = "Magnet 数据库文件位置"

# 中断提示
MSG_QUIT_HINT = "提示：处理中可按 Ctrl+Q 中断。\n"
MSG_QUIT_KEY = "\n⚠ 用户中断（Ctrl+Q），已处理部分不会丢失。"

# 错误消息
MSG_ERR_SOURCE_NOT_FOUND = "错误: 源文件夹不存在 - {}，返回主菜单。"
MSG_ERR_DIR_CONFLICT = "目录冲突错误: {}"
MSG_ERR_RETURN_MENU = "已返回主菜单，请重新选择目录。"
MSG_ERR_CANNOT_GENERATE_MAGNET = "无法生成 Magnet 链接。"
MSG_ERR_CANNOT_EXTRACT_HASH = "无法提取 Magnet 值。"

# 信息/状态消息
MSG_INFO_LOADED_DB = "已加载 {} 条 Magnet 记录"
MSG_INFO_NO_TORRENT_FILES = "源文件夹中没有找到任何 torrent 文件"
MSG_INFO_CREATED_DIR = "已创建目录: {}"
MSG_INFO_PROMPT_SELECT = "\n请选择功能："

# 选项 1 相关
MSG_OPT1_START = "\n=== 开始 Torrents 文件夹处理 ==="
MSG_OPT1_FILE_HEADER = "\n[{}/{}] {} | {}"
MSG_OPT1_NO_MAGNET = "无法生成 Magnet 链接，跳过文件: {}"
MSG_OPT1_NO_HASH = "无法提取 Magnet 值，跳过文件: {}"
MSG_OPT1_HASH_EXISTS = "Magnet 值已存在，将文件移动到删除文件夹: {}"
MSG_OPT1_MOVED_TO = "已移动到: {}"
MSG_OPT1_MOVE_FAIL_RETAIN = "移动失败，保留在源位置: {}"
MSG_OPT1_HASH_PENDING = "Magnet 值已记入待写入列表: {}"
MSG_OPT1_MOVE_WRITE_FAIL = "移动到写入目录失败，跳过: {}"
MSG_OPT1_PROCESSED = "已处理: {} (Hash: {})"
MSG_OPT1_PROCESS_FAIL = "处理文件失败 {}: {}"
MSG_OPT1_ADDED_HASHES = "已将 {} 条 Magnet 值写入数据库"
MSG_OPT1_COMPLETE = "\n文件夹处理完成！"
MSG_OPT1_ERROR = "\n文件夹处理中出现错误。"
MSG_OPT1_DUP_LIST_HEADER = "\n===== 以下文件因 Magnet 值重复被移至删除文件夹 ====="
MSG_OPT1_NO_DUP = "没有重复文件。"

# 选项 2 相关
MSG_OPT2_START = "\n=== 多行 Magnet 链接写入数据库 ==="
MSG_OPT2_CLIPBOARD_EMPTY = "剪贴板为空，无法处理。"
MSG_OPT2_NO_VALID_LINES = "剪贴板中没有有效行。"
MSG_OPT2_SKIP_NON_MAGNET = "跳过非 Magnet 链接行: {}"
MSG_OPT2_CANNOT_EXTRACT = "无法提取 Magnet 值: {}"
MSG_OPT2_HASH_EXISTS = "Magnet 值已存在: {}"
MSG_OPT2_ADDED = "已添加新 Magnet 值: {}"
MSG_OPT2_COMPLETE = "\n处理完成：新增 {} 条，已存在 {} 条。"
MSG_OPT2_EXISTED_HEADER = "\n===== 已存在的 Magnet 链接列表 ====="
MSG_OPT2_NO_DUP = "没有重复的链接。"

# 选项 3 相关
MSG_OPT3_DEL_MAGNET_START = "\n=== 多行 Magnet 链接从数据库删除 ==="
MSG_OPT3_DEL_MAGNET_DELETED = "已删除: {}"
MSG_OPT3_DEL_MAGNET_NOT_FOUND = "未找到: {}"
MSG_OPT3_DEL_MAGNET_COMPLETE = "\n处理完成：删除 {} 条，未找到 {} 条。"

# 选项 4 相关
MSG_OPT4_DEL_HASH_START = "\n=== 多行 Magnet 值从数据库删除 ==="
MSG_OPT4_DEL_HASH_DELETED = "已删除: {}"
MSG_OPT4_DEL_HASH_NOT_FOUND = "未找到: {}"
MSG_OPT4_DEL_HASH_COMPLETE = "\n处理完成：删除 {} 条，未找到 {} 条。"

# 选项 5 相关
MSG_OPT5_SORT_DB_START = "\n=== 整理 Magnet 数据库 ==="
MSG_OPT5_SORT_DB_NOT_FOUND = "数据库文件不存在: {}"
MSG_OPT5_SORT_DB_BACKUP_CREATED = "已创建备份: {}"
MSG_OPT5_SORT_DB_BACKUP_FAIL = "备份失败: {}"
MSG_OPT5_SORT_DB_COMPLETE = "整理完成。原始: {}，去重后: {}。"
MSG_OPT5_SORT_DB_PROCESS_ERROR = "整理过程中出错: {}"
MSG_OPT5_SORT_DB_RESTORED = "已从备份恢复原文件。"

# 通用
MSG_LOAD_DB_FAIL = "读取 Magnet 数据库失败: {}"
MSG_WRITE_DB_FAIL = "写入 Magnet 数据库失败: {}"
MSG_MOVE_FILE_FAIL = "移动文件失败（不可恢复）: {}"
MSG_MOVE_FILE_OCCUPIED = "文件被占用，重试 {}/{}: {}"
MSG_MOVE_FILE_MAX_RETRIES = "移动失败，已达最大重试次数: {}"
MSG_MOVE_SUCCESS = "移动成功: {} -> {}"
MSG_TARGET_EXISTS_RENAME = "目标已存在，重命名为: {}"
MSG_MAGNET_GEN_FAIL = "生成 Magnet 链接失败 {}: {}"
MSG_MAGNET_PARSE_FAIL = "解析 Magnet 链接失败: {}"
MSG_EXTRACT_HASH_FAIL = "提取 Magnet 值失败: {}"

# Ctrl+Q / Ctrl+\ 中断标志
_quit_requested = False


def _on_quit_signal(signum, frame):
    """Unix SIGQUIT 信号处理器（Ctrl+\）。"""
    global _quit_requested
    _quit_requested = True


def init_quit_handler() -> None:
    """注册中断处理：Windows 用 msvcrt，Unix 用 SIGQUIT（Ctrl+\）。"""
    if hasattr(signal, "SIGQUIT"):
        signal.signal(signal.SIGQUIT, _on_quit_signal)
    if sys.platform == "win32":
        print(MSG_QUIT_HINT)


def check_quit_key() -> bool:
    """
    非阻塞检测中断快捷键。
    Windows：检测 Ctrl+Q（msvcrt kbhit）。
    Unix：返回 _quit_requested 标志（由 SIGQUIT 设置）。
    """
    global _quit_requested
    if sys.platform == "win32":
        try:
            import msvcrt
            while msvcrt.kbhit():
                ch = msvcrt.getch()
                if ch == b"\x11":   # Ctrl+Q = ASCII 17
                    _quit_requested = True
        except Exception:
            pass
    return _quit_requested


# ==================== 辅助函数 ====================

def get_input_with_default(prompt_text: str, default_value: str) -> str:
    """获取带默认值的用户输入。"""
    user_input = input(MSG_PROMPT_DEFAULT_FMT.format(prompt_text, default_value)).strip()
    return user_input if user_input else str(default_value)


def ensure_directory_exists(directory_path: str) -> str:
    """确保目录存在。"""
    p = Path(directory_path)
    if not p.is_dir():
        p.mkdir(parents=True, exist_ok=True)
        print(MSG_INFO_CREATED_DIR.format(directory_path))
    return directory_path


def is_hidden_file(file_name: str) -> bool:
    """检查是否为隐藏文件，支持 * 通配符前缀匹配。"""
    lower = file_name.lower()
    for pattern in HIDDEN_FILE_PATTERNS:
        if pattern.endswith("*"):
            prefix = pattern[:-1].lower()
            if lower.startswith(prefix):
                return True
        elif lower == pattern.lower():
            return True
    return False


def validate_directory_independence(src_str: str, write_str: str,
                                     delete_str: str) -> tuple[bool, str]:
    """校验源文件夹与写入/删除文件夹相互独立。"""
    src = Path(src_str).resolve()
    entries = [
        ("写入文件夹", Path(write_str).resolve()),
        ("删除文件夹", Path(delete_str).resolve()),
    ]
    for label, dst in entries:
        if src == dst:
            return False, f"源文件夹与{label}路径相同，会导致文件丢失。"
        try:
            if dst.is_relative_to(src):
                return False, f"源文件夹包含{label}，会导致文件被重复处理或丢失。"
        except ValueError:
            pass
        try:
            if src.is_relative_to(dst):
                return False, f"{label}包含源文件夹，会导致文件丢失。"
        except ValueError:
            pass
    return True, ""


def get_all_torrent_files(source_dir: str) -> list[str]:
    """获取源目录下所有 .torrent 文件（非隐藏，跳过隐藏文件夹）。"""
    src = Path(source_dir)
    result: list[str] = []
    for p in src.rglob("*"):
        if not p.is_file():
            continue
        if p.suffix.lower() != ".torrent":
            continue
        if is_hidden_file(p.name):
            continue
        # 跳过隐藏文件夹内的文件
        try:
            rel = p.parent.relative_to(src)
        except ValueError:
            rel = Path()
        if any(part.startswith(".") for part in rel.parts):
            continue
        result.append(str(p))
    return result


def safe_move_file(src_path: str, dst_path_str: str,
                   max_retries: int = 10, retry_delay: float = 1.0) -> bool:
    """安全移动文件（带重试），目标已存在时自动加 _N 后缀。"""
    src = Path(src_path)
    dst = Path(dst_path_str)

    if dst.is_file():
        stem, ext = dst.stem, dst.suffix
        counter = 1
        while dst.is_file():
            dst = dst.parent / f"{stem}_{counter}{ext}"
            counter += 1
        print(MSG_TARGET_EXISTS_RENAME.format(dst.name))

    for attempt in range(max_retries):
        try:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dst))
            print(MSG_MOVE_SUCCESS.format(src.name, dst))
            return True
        except (PermissionError, OSError) as e:
            print(MSG_MOVE_FILE_OCCUPIED.format(attempt + 1, max_retries, e))
            time.sleep(retry_delay)
        except Exception as e:
            print(MSG_MOVE_FILE_FAIL.format(e))
            return False
    print(MSG_MOVE_FILE_MAX_RETRIES.format(src))
    return False


def move_file_with_structure(source_file: str, target_base_dir: str,
                             source_base_dir_str: str,
                             subfolder_name: str | None = None) -> str | None:
    """移动文件，保持文件夹结构。"""
    try:
        src = Path(source_file)
        base = Path(source_base_dir_str)
        if str(base) in str(src):
            rel = str(src.relative_to(base))
        else:
            rel = src.name

        # 路径遍历安全检查：拒绝包含 .. 组件的相对路径
        rel_path = Path(rel)
        if ".." in rel_path.parts:
            print(MSG_MOVE_FILE_FAIL.format(f"路径遍历被拒绝: {rel}"))
            return None

        if subfolder_name:
            target_dir = Path(target_base_dir) / subfolder_name / rel_path.parent
        else:
            target_dir = Path(target_base_dir) / rel_path.parent

        target_dir.mkdir(parents=True, exist_ok=True)
        target_file = target_dir / src.name
        if safe_move_file(str(src), str(target_file)):
            return str(target_file)
        return None
    except Exception as e:
        print(MSG_MOVE_FILE_FAIL.format(e))
        return None


# ==================== Magnet 核心函数 ====================

def extract_magnet_hash(magnet_link: str) -> str:
    """
    从 Magnet 链接提取 40 位十六进制 SHA-1 Hash（btih 值）。

    支持格式：
      - magnet:?xt=urn:btih:<40位hex>&dn=...
      - magnet:?xt=urn:btih:<40位hex>
      - 纯 40 位十六进制字符串
    """
    if not magnet_link or not magnet_link.strip():
        return ""

    link = magnet_link.strip()

    # 尝试匹配完整的 magnet 链接格式
    # urn:btih: 后面跟 40 位 hex，可能后跟 & 或直接结束
    match = re.search(r'btih:([0-9a-fA-F]{40})', link)
    if match:
        return match.group(1).lower()

    # 如果不是 magnet 链接格式，检查是否为纯 40 位 hex 字符串
    if re.match(r'^[0-9a-fA-F]{40}$', link):
        return link.lower()

    return ""


def generate_magnet_from_torrent(file_path: str) -> str:
    """
    从 torrent 文件生成 Magnet 链接。

    读取 torrent 文件，使用 bencodepy 解析出 info 字典，
    重新 bencode 后计算 SHA-1 Hash，返回 Magnet 链接。
    """
    try:
        fp = Path(file_path)
        if not fp.is_file():
            return ""

        with fp.open("rb") as f:
            raw_data = f.read()

        decoded = bencodepy.decode(raw_data)
        info = decoded[b"info"]
        # 将 info 字典重新 bencode 为原始字节
        info_bencoded = bencodepy.encode(info)
        info_hash = hashlib.sha1(info_bencoded).hexdigest().lower()

        return f"magnet:?xt=urn:btih:{info_hash}"
    except Exception as e:
        print(MSG_MAGNET_GEN_FAIL.format(file_path, e))
        return ""


# ==================== Magnet 数据库操作 ====================

def load_magnet_database(db_path: str) -> set[str]:
    """从 TXT 文件读取所有 Magnet 值（每行一个 40 位 hex hash）。"""
    p = Path(db_path)
    if not p.is_file():
        return set()
    try:
        lines = p.read_text(encoding="utf-8").splitlines()
        return {line.strip().lower() for line in lines if line.strip()}
    except Exception as e:
        print(MSG_LOAD_DB_FAIL.format(e))
        return set()


def add_to_magnet_database(db_path: str, magnet_value: str) -> None:
    """向 Magnet 数据库文件末尾追加一行 Magnet 值。"""
    try:
        with Path(db_path).open("a", encoding="utf-8") as f:
            f.write(magnet_value.lower() + "\n")
    except Exception as e:
        print(MSG_WRITE_DB_FAIL.format(e))


def batch_delete_from_magnet_database(db_path: str, magnet_values: set[str]) -> int:
    """从 Magnet 数据库文件中批量删除匹配的行，一次读写完成，返回删除数。"""
    p = Path(db_path)
    if not p.is_file():
        return 0
    lines = [line.strip().lower() for line in p.read_text(encoding="utf-8").splitlines()
             if line.strip()]
    values_lower = {v.lower() for v in magnet_values}
    new_lines = [l for l in lines if l not in values_lower]
    deleted = len(lines) - len(new_lines)
    if deleted > 0:
        p.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    return deleted


# ==================== 功能 1：Torrents 文件夹写入 Magnet 数据库 ====================

def process_torrent_folder_to_db(
    source_dir: str, write_dir: str, delete_dir: str, magnet_db_path: str,
) -> tuple[bool, list[str]]:
    """遍历 torrent 文件：比对 Magnet 值 → 新值入库 → 移动文件。"""
    print(MSG_OPT1_START)

    magnet_set = load_magnet_database(magnet_db_path)
    print(MSG_INFO_LOADED_DB.format(len(magnet_set)))

    all_files = get_all_torrent_files(source_dir)
    if not all_files:
        print(MSG_INFO_NO_TORRENT_FILES)
        return True, []

    source_folder_name = Path(source_dir).name
    duplicated_files: list[str] = []
    new_count = 0

    total = len(all_files)
    for idx, file_path in enumerate(all_files, 1):
        # Ctrl+Q 中断检查
        if check_quit_key():
            print(MSG_QUIT_KEY)
            break

        # 每文件头部信息
        now_str = datetime.now().strftime("%H:%M:%S")
        print(MSG_OPT1_FILE_HEADER.format(idx, total, now_str, Path(file_path).name))

        try:
            # 从 torrent 文件生成 Magnet 链接
            magnet_link = generate_magnet_from_torrent(file_path)
            if not magnet_link:
                print(MSG_OPT1_NO_MAGNET.format(file_path))
                continue

            # 提取 Magnet 值（40 位 hex hash）
            magnet_value = extract_magnet_hash(magnet_link)
            if not magnet_value:
                print(MSG_OPT1_NO_HASH.format(file_path))
                continue

            if magnet_value in magnet_set:
                fp_name = Path(file_path).name
                print(MSG_OPT1_HASH_EXISTS.format(fp_name))
                moved = move_file_with_structure(
                    file_path, delete_dir, source_dir, source_folder_name
                )
                if moved:
                    duplicated_files.append(moved)
                    print(MSG_OPT1_MOVED_TO.format(moved))
                else:
                    print(MSG_OPT1_MOVE_FAIL_RETAIN.format(file_path))
                    duplicated_files.append(file_path)
                continue

            # 新 Magnet 值：写入数据库并移动文件
            magnet_set.add(magnet_value)
            add_to_magnet_database(magnet_db_path, magnet_value)
            new_count += 1
            print(MSG_OPT1_HASH_PENDING.format(magnet_value))

            # 移动该 torrent 文件到写入文件夹（保持子文件夹结构）
            moved_to_write = move_file_with_structure(
                file_path, write_dir, source_dir, source_folder_name
            )
            if not moved_to_write:
                print(MSG_OPT1_MOVE_WRITE_FAIL.format(Path(file_path).name))
                continue

            print(MSG_OPT1_PROCESSED.format(Path(file_path).name, magnet_value))
        except Exception as e:
            print(MSG_OPT1_PROCESS_FAIL.format(file_path, e))
            continue

    if new_count > 0:
        print(MSG_OPT1_ADDED_HASHES.format(new_count))

    return True, duplicated_files


# ==================== 功能 2：多行 Magnet 链接写入数据库 ====================

def process_magnet_links_from_clipboard(magnet_db_path: str) -> None:
    """从剪贴板读取多行 Magnet 链接，提取 Magnet 值更新数据库。"""
    print(MSG_OPT2_START)
    clipboard_text = get_clipboard_text()
    if not clipboard_text.strip():
        print(MSG_OPT2_CLIPBOARD_EMPTY)
        return

    lines = [line.strip() for line in clipboard_text.splitlines() if line.strip()]
    if not lines:
        print(MSG_OPT2_NO_VALID_LINES)
        return

    magnet_set = load_magnet_database(magnet_db_path)
    print(MSG_INFO_LOADED_DB.format(len(magnet_set)))

    existed_links: list[str] = []
    new_count = 0

    for line in lines:
        magnet_value = extract_magnet_hash(line)
        if not magnet_value:
            print(MSG_OPT2_SKIP_NON_MAGNET.format(line))
            continue

        if magnet_value in magnet_set:
            existed_links.append(line)
            print(MSG_OPT2_HASH_EXISTS.format(magnet_value))
        else:
            add_to_magnet_database(magnet_db_path, magnet_value)
            magnet_set.add(magnet_value)
            new_count += 1
            print(MSG_OPT2_ADDED.format(magnet_value))

    print(MSG_OPT2_COMPLETE.format(new_count, len(existed_links)))

    if existed_links:
        print(MSG_OPT2_EXISTED_HEADER)
        list_text = "\n".join(existed_links)
        print(list_text)
        copy_to_clipboard(list_text)
    else:
        print(MSG_OPT2_NO_DUP)


# ==================== 功能 3：多行 Magnet 链接从数据库删除 ====================

def delete_magnet_links_from_db(magnet_db_path: str) -> None:
    """从剪贴板读取多行 Magnet 链接，提取 Magnet 值并批量从数据库删除。"""
    print(MSG_OPT3_DEL_MAGNET_START)
    clipboard_text = get_clipboard_text()
    if not clipboard_text.strip():
        print(MSG_OPT2_CLIPBOARD_EMPTY)
        return

    lines = [line.strip() for line in clipboard_text.splitlines() if line.strip()]
    if not lines:
        print(MSG_OPT2_NO_VALID_LINES)
        return

    magnet_set = load_magnet_database(magnet_db_path)
    print(MSG_INFO_LOADED_DB.format(len(magnet_set)))

    to_delete: set[str] = set()

    for line in lines:
        magnet_value = extract_magnet_hash(line)
        if not magnet_value:
            print(MSG_OPT2_SKIP_NON_MAGNET.format(line))
            continue

        to_delete.add(magnet_value)

    # 批量删除
    deleted_count = batch_delete_from_magnet_database(magnet_db_path, to_delete)

    # 逐条报告结果
    for mv in to_delete:
        if mv in magnet_set:
            print(MSG_OPT3_DEL_MAGNET_DELETED.format(mv))
        else:
            print(MSG_OPT3_DEL_MAGNET_NOT_FOUND.format(mv))

    not_found_count = len(to_delete) - deleted_count
    print(MSG_OPT3_DEL_MAGNET_COMPLETE.format(deleted_count, not_found_count))


# ==================== 功能 4：多行 Magnet 值从数据库删除 ====================

def delete_magnet_values_from_db(magnet_db_path: str) -> None:
    """从剪贴板读取多行 Magnet 值（40 位 hex hash）并批量从数据库删除。"""
    print(MSG_OPT4_DEL_HASH_START)
    clipboard_text = get_clipboard_text()
    if not clipboard_text.strip():
        print(MSG_OPT2_CLIPBOARD_EMPTY)
        return

    lines = [line.strip() for line in clipboard_text.splitlines() if line.strip()]
    if not lines:
        print(MSG_OPT2_NO_VALID_LINES)
        return

    magnet_set = load_magnet_database(magnet_db_path)
    print(MSG_INFO_LOADED_DB.format(len(magnet_set)))

    to_delete: set[str] = set()

    for line in lines:
        value = line.strip()
        if not value:
            continue
        # 规范化：如果输入的内容包含 magnet 链接格式，尝试提取 hash
        magnet_value = extract_magnet_hash(value)
        if not magnet_value:
            # 如果不是标准 magnet 链接，直接使用原始值（允许纯 hash 输入）
            if re.match(r'^[0-9a-fA-F]{40}$', value):
                magnet_value = value.lower()
            else:
                print(MSG_OPT2_SKIP_NON_MAGNET.format(value))
                continue
        to_delete.add(magnet_value)

    # 批量删除
    deleted_count = batch_delete_from_magnet_database(magnet_db_path, to_delete)

    # 逐条报告结果
    for mv in to_delete:
        if mv in magnet_set:
            print(MSG_OPT4_DEL_HASH_DELETED.format(mv))
        else:
            print(MSG_OPT4_DEL_HASH_NOT_FOUND.format(mv))

    not_found_count = len(to_delete) - deleted_count
    print(MSG_OPT4_DEL_HASH_COMPLETE.format(deleted_count, not_found_count))


# ==================== 功能 5：整理数据库 ====================

def sort_magnet_database(db_path: str) -> None:
    """对 Magnet 数据库排序去重，先备份。"""
    print(MSG_OPT5_SORT_DB_START)
    p = Path(db_path)
    if not p.is_file():
        print(MSG_OPT5_SORT_DB_NOT_FOUND.format(db_path))
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = Path(str(db_path) + f".bak_{timestamp}")
    try:
        shutil.copy2(str(p), str(backup_path))
        print(MSG_OPT5_SORT_DB_BACKUP_CREATED.format(backup_path))
    except Exception as e:
        print(MSG_OPT5_SORT_DB_BACKUP_FAIL.format(e))
        return

    try:
        lines = [line.strip().lower() for line in p.read_text(encoding="utf-8").splitlines()
                 if line.strip()]
        original_count = len(lines)
        unique_sorted = sorted(set(lines))
        new_count = len(unique_sorted)
        p.write_text("\n".join(unique_sorted) + "\n", encoding="utf-8")
        print(MSG_OPT5_SORT_DB_COMPLETE.format(original_count, new_count))
    except Exception as e:
        print(MSG_OPT5_SORT_DB_PROCESS_ERROR.format(e))
        try:
            shutil.copy2(str(backup_path), str(p))
            print(MSG_OPT5_SORT_DB_RESTORED)
        except Exception:
            pass


# ==================== 主菜单 ====================

def main() -> None:
    """主菜单循环。"""
    init_quit_handler()
    print("=" * 60)
    print(MSG_MENU_TITLE)
    print("=" * 60)

    while True:
        print(MSG_INFO_PROMPT_SELECT)
        print(MSG_MENU_1)
        print(MSG_MENU_2)
        print(MSG_MENU_3)
        print(MSG_MENU_4)
        print(MSG_MENU_5)
        print(MSG_MENU_0)
        choice = input(MSG_MENU_CHOICE_PROMPT).strip()

        if choice == "1":
            source_dir = get_input_with_default(
                MSG_PROMPT_SOURCE_DIR, str(DEFAULT_SOURCE_DIR)
            )
            write_dir = get_input_with_default(
                MSG_PROMPT_WRITE_DIR, str(DEFAULT_WRITE_DIR)
            )
            delete_dir = get_input_with_default(
                MSG_PROMPT_DELETE_DIR, str(DEFAULT_DELETE_DIR)
            )
            magnet_db_path = get_input_with_default(
                MSG_PROMPT_MAGNET_DB, str(DEFAULT_MAGNET_DB)
            )

            ensure_directory_exists(write_dir)
            ensure_directory_exists(delete_dir)
            ensure_directory_exists(str(Path(magnet_db_path).parent))

            if not Path(source_dir).is_dir():
                print(MSG_ERR_SOURCE_NOT_FOUND.format(source_dir))
                continue

            is_valid, err_msg = validate_directory_independence(
                source_dir, write_dir, delete_dir
            )
            if not is_valid:
                print(MSG_ERR_DIR_CONFLICT.format(err_msg))
                print(MSG_ERR_RETURN_MENU)
                continue

            success, duplicated_files = process_torrent_folder_to_db(
                source_dir, write_dir, delete_dir, magnet_db_path,
            )

            print(MSG_OPT1_COMPLETE if success else MSG_OPT1_ERROR)

            if duplicated_files:
                print(MSG_OPT1_DUP_LIST_HEADER)
                dup_list = "\n".join(duplicated_files)
                print(dup_list)
                copy_to_clipboard(dup_list)
            else:
                print(MSG_OPT1_NO_DUP)

        elif choice == "2":
            magnet_db_path = get_input_with_default(
                MSG_PROMPT_MAGNET_DB, str(DEFAULT_MAGNET_DB)
            )
            ensure_directory_exists(str(Path(magnet_db_path).parent))
            process_magnet_links_from_clipboard(magnet_db_path)

        elif choice == "3":
            magnet_db_path = get_input_with_default(
                MSG_PROMPT_MAGNET_DB, str(DEFAULT_MAGNET_DB)
            )
            ensure_directory_exists(str(Path(magnet_db_path).parent))
            delete_magnet_links_from_db(magnet_db_path)

        elif choice == "4":
            magnet_db_path = get_input_with_default(
                MSG_PROMPT_MAGNET_DB, str(DEFAULT_MAGNET_DB)
            )
            ensure_directory_exists(str(Path(magnet_db_path).parent))
            delete_magnet_values_from_db(magnet_db_path)

        elif choice == "5":
            magnet_db_path = get_input_with_default(
                MSG_PROMPT_MAGNET_DB, str(DEFAULT_MAGNET_DB)
            )
            sort_magnet_database(magnet_db_path)

        elif choice == "0":
            print(MSG_MENU_EXIT)
            break
        else:
            print(MSG_MENU_INVALID)

        input(MSG_MENU_CONTINUE)


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
