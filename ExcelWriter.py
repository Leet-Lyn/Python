# 请帮我写个中文的 Python 脚本，批注也是中文，但是变量参数不要是中文：
# 在脚本开始前让我选择：1. 文件夹写入 excel 并写入数据库；2. 多行 ed2k 链接写入数据库；3. 单文件链接写入数据库；4. 多行ed2k链接从数据库删除；多行SizeMD4值从数据库删除；6. 整理数据库；0. 退出。
# 1. 文件夹写入 excel 并写入数据库：
# 询问我 excel 文件位置（默认为：d:\Studios\Attachments\标准.xlsx）、源文件夹位置（默认为：d:\Studios\Folders\Downloads\），写入文件夹位置（默认为：d:\Studios\Folders\Ins\），上传文件夹位置（默认为：d:\Studios\Folders\Uploads\）, 删除文件夹位置（默认为：d:\Studios\Folders\Deletes\）。SizeMD4 数据库文件位置（默认为：e:\Documents\Softwares\Codes\Attachments\Databases\SizeMD4\SizeMD4.txt）。
# 读取 excel 文件，第一行为表头（字段名）。此后每一行为一条记录。分别询问我"引用页"、"属于"、"主链接"的值（按回车则为空）。
# 遍历源文件夹内所有文件及子文件夹中的文件，顺序完成。
# 首先计算并生成该文件的 ed2k 链接。我安装了 RHash，位置“d:\ProApps\rhash\current\rhash.exe”。生成 ed2k 的命令类似：rhash.exe --uppercase --ed2k-link "\\TS-464C\Temps\rustdesk-1.4.3-x86_64.exe"。生成如“ed2k://|file|rustdesk-1.4.3-x86_64.exe|23369352|DF952EEB0438E288409858E6C960E261|h=T7BJKLDRQ7VDCDKOO525FO7YHJCZVKDK|/”的ed2k链接。生成的 ed2k 链接转换成 SizeMD4 值（格式：文件大小|MD4哈希，不需要文件名及其他）。比对 SizeMD4 数据库文件（SizeMD4 数据库文件，每一行为一个文件的 SizeMD4 值（文件大小|MD4哈希））。
# 如果当前文件的 SizeMD4 值在原来 SizeMD4 数据库文件里存在，则将该文件移动到删除文件夹，选择下一个文件。
# 如果当前文件的 SizeMD4 值不在原来 SizeMD4 数据库文件里存在，则添加该文件的 SizeMD4 值到 SizeMD4 数据库文件末尾（另起一行），保存SizeMD4 数据库文件。进行后续操作：
# 将该文件（SizeMD4 值不在原来 SizeMD4 数据库文件里存在的）的信息写入 excel 文件, 每一条记录新开一行。1. "Index"字段值为上一行 "Index"字段值+1（如上一行为空或为表头，则"Index"字段值为 1）。2. 将源文件夹内文件名写入"名字"与"原文件名"字段值。3. 将该文件移动到写入文件夹下的子文件夹（子文件夹名字为源文件夹名，保持原来文件夹结构），并移动到"z:\"中，如果无法完成写入"z:\"中，则重命名原文件（从后删除1个字符（不包括扩展名）），再次尝试将原文件向目标文件夹移动。反复循环，直至能将原文件向目标文件夹移动。如果有重命名过文件，将修改过的文件名写入"矫正文件名"字段值中。写入"z:\"后，系统会自动生成一个对应文件（自动加密的）。读取"d:\Xyz\"新生成的文件名，将其文件名（无扩展名）写入"加密文件名"字段值。将"d:\Xyz\"新生成的文件移动到上传文件夹下的子文件夹（子文件夹名字为源文件夹名，保持原来文件夹结构，在"d:\Xyz\"中不保留）。5. 将原来询问我的"引用页"、"属于"、"主链接"的值写入"引用页"、"属于"、"主链接"字段值。6. 将该文件的 ed2k 链接，写入"标准链接"字段值。7. 通过"标准链接"字段值，分别生成"大小"、"散列"字段值。大小请转成 B、KB、MB、GB 形式，并精确到小数点后 4 位，hash 转全部大写。选择下一个文件。
# 直至源文件夹内所有文件及子文件夹中的文件都处理好结束。最后整理哪些文件 SizeMD4 值原数据库存在，移动到删除文件夹里。并将这些文件列表打印在屏幕上并复制到剪贴板上去。
# 2. 多行 ed2k 链接写入数据库：
# 询问我SizeMD4 数据库文件位置（默认为：e:\Documents\Softwares\Codes\Attachments\Databases\SizeMD4\SizeMD4.txt）。读取剪贴板数据，其为多行 ed2k 链接（每行一个 ed2k 链接），顺序读取每一行 ed2k 链接，转换成 SizeMD4 值（格式：文件大小|MD4哈希，不需要文件名及其他）。比对 SizeMD4 数据库文件（SizeMD4 数据库文件，每一行为一个文件的 SizeMD4 值（文件大小|MD4哈希））。
# 如果当前 SizeMD4 值在原来 SizeMD4 数据库文件里存在，报告我。
# 如果当前 SizeMD4 值不在原来 SizeMD4 数据库文件里存在，则添加该 SizeMD4 值到 SizeMD4 数据库文件末尾（另起一行），保存SizeMD4 数据库文件。
# 最后整理哪些 ed2k 链接的 SizeMD4 值原数据库存在。并将这些文件列表打印在屏幕上并复制到剪贴板上去。
# 3. 单文件链接写入数据库：
# 询问我文件链接（默认为：d:\Studios\Attachments\标准.zip），SizeMD4 数据库文件位置（默认为：e:\Documents\Softwares\Codes\Attachments\Databases\SizeMD4\SizeMD4.txt）。通过 rhash.exe --uppercase --ed2k-link 命令生成 ed2k 链接，转换成 SizeMD4 值（格式：文件大小|MD4哈希，不需要文件名及其他）。比对 SizeMD4 数据库文件（SizeMD4 数据库文件，每一行为一个文件的 SizeMD4 值（文件大小|MD4哈希））。
# 如果当前文件 SizeMD4 值在原来 SizeMD4 数据库文件里存在，报告我。
# 如果当前文件 SizeMD4 值不在原来 SizeMD4 数据库文件里存在，则添加该 SizeMD4 值到 SizeMD4 数据库文件末尾（另起一行），保存SizeMD4 数据库文件。
# 最后告诉我该文件 ed2k 链接的 SizeMD4 值原数据库是否存在。
# 4. 整理数据库：
# 询问我 SizeMD4 数据库文件位置（默认为：e:\Documents\Softwares\Codes\Attachments\Databases\SizeMD4\SizeMD4.txt）。对 SizeMD4 数据库，先备份，再对文件里的 SizeMD4 值（字符串）从小到大排序。
# 5. 多行 ed2k 链接从数据库删除：
# 询问我 SizeMD4 数据库文件位置（默认为：e:\Documents\Softwares\Codes\Attachments\Databases\SizeMD4\SizeMD4.txt）。读取剪贴板数据，其为多行 ed2k 链接（每行一个 ed2k 链接），顺序读取每一行 ed2k 链接，转换成 SizeMD4 值（格式：文件大小|MD4哈希，不需要文件名及其他）。比对 SizeMD4 数据库文件（SizeMD4 数据库文件，每一行为一个文件的 SizeMD4 值（文件大小|MD4哈希））。
# 如果当前 SizeMD4 值在原来 SizeMD4 数据库文件里存在，则将该 SizeMD4 值从原来 SizeMD4 数据库文件里删除。
# 如果当前 SizeMD4 值不在原来 SizeMD4 数据库文件里存在，则报告我。
# 6. 多行 SizeMD4 值从数据库删除：
# 询问我 SizeMD4 数据库文件位置（默认为：e:\Documents\Softwares\Codes\Attachments\Databases\SizeMD4\SizeMD4.txt）。读取剪贴板数据，其为多行 SizeMD4 值（每行一个 多行 SizeMD4 值），顺序读取每一行 多行 SizeMD4 值。比对 SizeMD4 数据库文件（SizeMD4 数据库文件，每一行为一个文件的 SizeMD4 值（文件大小|MD4哈希））。
# 如果当前 SizeMD4 值在原来 SizeMD4 数据库文件里存在，则将该 SizeMD4 值从原来 SizeMD4 数据库文件里删除。
# 如果当前 SizeMD4 值不在原来 SizeMD4 数据库文件里存在，则报告我。
# 完成后，反复循环至最开始。

import shutil
import signal
import subprocess
import sys
import time
import urllib.parse
from datetime import datetime
from pathlib import Path

import pandas as pd

# ==================== 剪贴板 ====================

def copy_to_clipboard(text: str) -> None:
    """复制文本到 Windows 剪贴板。"""
    try:
        subprocess.run(
            ["clip.exe"],
            input=text,
            encoding="utf-16-le",
            errors="ignore",
            check=True,
        )
        print("已复制到剪贴板。")
    except Exception as e:
        print(f"复制到剪贴板失败: {e}")


def get_clipboard_text() -> str:
    """从剪贴板获取文本。"""
    try:
        result = subprocess.run(
            ["powershell", "-NonInteractive", "-Command", "Get-Clipboard -Raw"],
            capture_output=True,
            encoding="utf-8",
            check=True,
        )
        return result.stdout
    except Exception:
        print("无法读取剪贴板。")
        return ""


# ==================== 全局配置 ====================

DEFAULT_EXCEL_PATH = Path(r"d:\Studios\Attachments\标准.xlsx")
DEFAULT_SOURCE_DIR = Path(r"d:\Studios\Folders\Downloads")
DEFAULT_WRITE_DIR = Path(r"d:\Studios\Folders\Ins")
DEFAULT_UPLOAD_DIR = Path(r"d:\Studios\Folders\Uploads")
DEFAULT_DELETE_DIR = Path(r"d:\Studios\Folders\Deletes")
DEFAULT_SIZE_MD4_DB = Path(r"e:\Documents\Softwares\Codes\Attachments\Databases\SizeMD4\SizeMD4.txt")
DEFAULT_RHASH_PATH = Path(r"d:\ProApps\rhash\current\rhash.exe")
DEFAULT_XYZ_DIR = Path(r"D:\Xyz")
Z_DRIVE_PATH = Path(r"Z:/")

HIDDEN_FILE_PATTERNS = [
    "desktop.ini", "descript.ion", ".encfs6.xml", "Thumbs.db",
    ".DS_Store", "._*",
]

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
        print("提示：处理中可按 Ctrl+Q 中断。\n")


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
    user_input = input(f"{prompt_text} (默认: {default_value}): ").strip()
    return user_input if user_input else str(default_value)


def ensure_directory_exists(directory_path: str) -> str:
    """确保目录存在。"""
    p = Path(directory_path)
    if not p.is_dir():
        p.mkdir(parents=True, exist_ok=True)
        print(f"已创建目录: {directory_path}")
    return directory_path


def format_file_size(size_bytes: int) -> str:
    """格式化文件大小为 B/KB/MB/GB，保留 4 位小数。"""
    if size_bytes == 0:
        return "0 B"
    units = ["B", "KB", "MB", "GB"]
    unit_index = 0
    size = float(size_bytes)
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024.0
        unit_index += 1
    if unit_index == 0:
        return f"{size_bytes} B"
    return f"{size:.4f} {units[unit_index]}"


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
                                     upload_str: str, delete_str: str) -> tuple[bool, str]:
    """校验源文件夹与写入/上传/删除文件夹相互独立。"""
    src = Path(src_str).resolve()
    entries = [
        ("写入文件夹", Path(write_str).resolve()),
        ("上传文件夹", Path(upload_str).resolve()),
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


def get_all_files(source_dir: str) -> list[str]:
    """获取源目录下所有非隐藏文件（跳过隐藏文件夹）。"""
    src = Path(source_dir)
    result: list[str] = []
    for p in src.rglob("*"):
        if not p.is_file():
            continue
        if is_hidden_file(p.name):
            continue
        # 跳过隐藏文件夹内的文件（匹配原 os.walk 的 dirs[:] 过滤逻辑）
        try:
            rel = p.parent.relative_to(src)
        except ValueError:
            rel = Path()
        if any(part.startswith(".") for part in rel.parts):
            continue
        result.append(str(p))
    return result


def generate_ed2k_link(file_path: str) -> str:
    """生成文件的 ED2K 链接。"""
    try:
        fp = Path(file_path)
        if DEFAULT_RHASH_PATH.is_file() and fp.is_file():
            result = subprocess.run(
                [str(DEFAULT_RHASH_PATH), "--uppercase", "--ed2k-link", str(fp)],
                capture_output=True, encoding="utf-8",
            )
            if result.returncode == 0:
                return result.stdout.strip()
        return ""
    except Exception as e:
        print(f"生成ED2K链接失败 {file_path}: {e}")
        return ""


def parse_ed2k_link(ed2k_link: str) -> tuple[str, str]:
    """解析 ED2K 链接，返回 (格式化大小, 大写哈希)。"""
    if not ed2k_link or not ed2k_link.startswith("ed2k://|file|"):
        return "", ""
    try:
        decoded_link = urllib.parse.unquote(ed2k_link)
        parts = decoded_link.split("|")
        if len(parts) >= 5:
            size_str = parts[3]
            filehash = parts[4].upper()
            try:
                size_bytes = int(size_str)
                formatted_size = format_file_size(size_bytes)
            except ValueError:
                formatted_size = ""
            return formatted_size, filehash
        return "", ""
    except Exception as e:
        print(f"解析ED2K链接失败: {e}")
        return "", ""


def extract_size_md4(ed2k_link: str) -> str:
    """从 ED2K 链接提取 SizeMD4 字符串（文件大小|MD4哈希）。"""
    if not ed2k_link or not ed2k_link.startswith("ed2k://|file|"):
        return ""
    try:
        decoded_link = urllib.parse.unquote(ed2k_link)
        parts = decoded_link.split("|")
        if len(parts) >= 5:
            return f"{parts[3]}|{parts[4].upper()}"
        return ""
    except Exception as e:
        print(f"提取SizeMD4失败: {e}")
        return ""


def load_size_md4_database(db_path: str) -> set[str]:
    """从 TXT 文件读取所有 SizeMD4 值。"""
    p = Path(db_path)
    if not p.is_file():
        return set()
    try:
        lines = p.read_text(encoding="utf-8").splitlines()
        return {line.strip() for line in lines if line.strip()}
    except Exception as e:
        print(f"读取SizeMD4数据库失败: {e}")
        return set()


def add_to_size_md4_database(db_path: str, size_md4: str) -> None:
    """向 SizeMD4 数据库文件末尾追加一行。"""
    try:
        with Path(db_path).open("a", encoding="utf-8") as f:
            f.write(size_md4 + "\n")
    except Exception as e:
        print(f"写入SizeMD4数据库失败: {e}")


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
        print(f"目标已存在，重命名为: {dst.name}")

    for attempt in range(max_retries):
        try:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dst))
            print(f"移动成功: {src.name} -> {dst}")
            return True
        except (PermissionError, OSError) as e:
            print(f"文件被占用，重试 {attempt+1}/{max_retries}: {e}")
            time.sleep(retry_delay)
        except Exception as e:
            print(f"移动文件失败（不可恢复）: {e}")
            return False
    print(f"移动失败，已达最大重试次数: {src}")
    return False


def wait_for_file_ready(file_path: str, timeout_seconds: int = 30,
                        check_interval: float = 0.5) -> bool:
    """等待文件完全释放。"""
    p = Path(file_path)
    start_time = time.time()
    while time.time() - start_time < timeout_seconds:
        if not p.exists():
            time.sleep(check_interval)
            continue
        try:
            with p.open("r+b"):
                pass
            return True
        except (PermissionError, OSError):
            time.sleep(check_interval)
    print(f"文件就绪等待超时: {file_path}")
    return False


def copy_to_z_drive_with_retry(source_file: str):
    """
    复制文件到 Z 盘，失败则缩短文件名重试。
    返回 (成功路径, 修改后文件名或 None)。
    """
    FILENAME_ERROR_CODES = {3, 123, 161, 206}
    FATAL_ERROR_CODES = {5, 112}

    src = Path(source_file)
    stem = src.stem
    ext = src.suffix
    current_stem = stem
    attempt_count = 0
    max_attempts = 50

    while attempt_count < max_attempts:
        try:
            target_name = f"{current_stem}{ext}"
            target_path = Z_DRIVE_PATH / target_name
            shutil.copy2(str(src), str(target_path))
            if current_stem != stem:
                return str(target_path), target_name
            return str(target_path), None
        except OSError as e:
            winerr = getattr(e, "winerror", None)
            if winerr in FATAL_ERROR_CODES:
                print(f"复制到Z盘失败 ({e})，无法通过缩短文件名解决，跳过。")
                return None, None
            attempt_count += 1
            if winerr is not None and winerr not in FILENAME_ERROR_CODES:
                print(f"复制到Z盘出错 (winerror={winerr})，尝试缩短文件名: {e}")
            if len(current_stem) > 1:
                current_stem = current_stem[:-1]
            else:
                print(f"无法继续缩短文件名: {src.name}，错误: {e}")
                return None, None
        except Exception as e:
            print(f"复制到Z盘失败: {e}")
            return None, None
    print(f"达到最大尝试次数 {max_attempts}: {src.name}")
    return None, None


def wait_for_encrypted_file(xyz_dir_str: str | None = None,
                            timeout_seconds: int = 60) -> str | None:
    """等待加密文件生成并返回其完整路径。"""
    xyz_dir = Path(xyz_dir_str) if xyz_dir_str else DEFAULT_XYZ_DIR
    start_time = time.time()
    check_interval = 1.0
    warned_missing_dir = False

    while time.time() - start_time < timeout_seconds:
        if xyz_dir.is_dir():
            files = [p for p in xyz_dir.iterdir()
                     if p.is_file() and not is_hidden_file(p.name)]
            if files:
                newest = max(files, key=lambda p: p.stat().st_mtime)
                if wait_for_file_ready(str(newest), timeout_seconds=5):
                    return str(newest)
        else:
            if not warned_missing_dir:
                print(f"警告: XYZ目录不存在 ({xyz_dir})，等待中...")
                warned_missing_dir = True
        # Ctrl+Q 中断检查
        if check_quit_key():
            print("⚠ 用户中断（Ctrl+Q），停止等待加密文件。")
            return None
        time.sleep(check_interval)
    print(f"等待加密文件超时 ({timeout_seconds}秒)")
    return None


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

        rel_path = Path(rel)
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
        print(f"移动文件失败 {source_file}: {e}")
        return None


def get_last_index_from_excel(df: pd.DataFrame) -> int:
    """从 DataFrame 获取最后一个 Index 值。"""
    if "Index" in df.columns and not df.empty:
        index_values = df["Index"].dropna()
        if not index_values.empty:
            try:
                return int(index_values.max())
            except Exception:
                return 0
    return 0


# ==================== 功能 1：文件夹处理 ====================

def process_folder_to_excel_and_db(
    excel_path: str, source_dir: str, write_dir: str,
    upload_dir: str, delete_dir: str, size_md4_db_path: str,
    reference_page: str, belongs_to: str, main_link: str,
) -> tuple[bool, list[str]]:
    """处理文件夹：比对 SizeMD4 → 新文件写入 Excel → 移动 → Z盘 → 加密。"""
    print("\n=== 开始文件夹处理 ===")
    try:
        df = pd.read_excel(excel_path, engine="openpyxl")
    except Exception as e:
        print(f"读取Excel文件失败: {e}")
        return False, []

    size_md4_set = load_size_md4_database(size_md4_db_path)
    print(f"已加载 {len(size_md4_set)} 条 SizeMD4 记录")

    last_index = get_last_index_from_excel(df)
    all_files = get_all_files(source_dir)
    if not all_files:
        print("源文件夹中没有找到任何非隐藏文件")
        return True, []

    source_folder_name = Path(source_dir).name
    new_records: list[dict] = []
    duplicated_files: list[str] = []
    pending_size_md4_list: list[str] = []

    total = len(all_files)
    for idx, file_path in enumerate(all_files, 1):
        # Ctrl+Q 中断检查
        if check_quit_key():
            print("\n⚠ 用户中断（Ctrl+Q），已处理部分不会丢失。")
            break

        # 每文件头部信息
        now_str = datetime.now().strftime("%H:%M:%S")
        print(f"\n[{idx}/{total}] {now_str} | {Path(file_path).name}")

        try:
            ed2k_for_check = generate_ed2k_link(file_path)
            if not ed2k_for_check:
                print(f"无法生成ED2K链接，跳过文件: {file_path}")
                continue
            size_md4 = extract_size_md4(ed2k_for_check)
            if not size_md4:
                print(f"无法提取SizeMD4，跳过文件: {file_path}")
                continue

            if size_md4 in size_md4_set:
                fp_name = Path(file_path).name
                print(f"SizeMD4 已存在，将文件移动到删除文件夹: {fp_name}")
                moved = move_file_with_structure(file_path, delete_dir, source_dir)
                if moved:
                    duplicated_files.append(moved)
                    print(f"已移动到: {moved}")
                else:
                    print(f"移动失败，保留在源位置: {file_path}")
                    duplicated_files.append(file_path)
                continue

            pending_size_md4_list.append(size_md4)
            size_md4_set.add(size_md4)
            print(f"SizeMD4 已记入待写入列表: {size_md4}")

            new_record: dict = {}
            last_index += 1
            new_record["Index"] = last_index

            fp = Path(file_path)
            new_record["名字"] = fp.stem
            new_record["原文件名"] = fp.name

            moved_to_write = move_file_with_structure(
                file_path, write_dir, source_dir, source_folder_name
            )
            if not moved_to_write:
                print(f"移动到写入目录失败，跳过: {fp.name}")
                continue

            z_result = copy_to_z_drive_with_retry(moved_to_write)
            if z_result[0]:
                print(f"已复制到Z盘: {Path(z_result[0]).name}")
                new_record["矫正文件名"] = z_result[1] if z_result[1] else ""

                encrypted_file_path = wait_for_encrypted_file()
                if encrypted_file_path:
                    enc_fp = Path(encrypted_file_path)
                    new_record["加密文件名"] = enc_fp.stem

                    upload_target_dir = Path(upload_dir) / source_folder_name
                    upload_target_dir.mkdir(parents=True, exist_ok=True)
                    target_enc = upload_target_dir / enc_fp.name
                    if safe_move_file(encrypted_file_path, str(target_enc)):
                        print(f"已移动加密文件到上传目录: {enc_fp.name}")
                    else:
                        print("移动加密文件失败")
                else:
                    new_record["加密文件名"] = ""
            else:
                new_record["矫正文件名"] = ""
                new_record["加密文件名"] = ""

            new_record["引用页"] = reference_page
            new_record["属于"] = belongs_to
            new_record["主链接"] = main_link

            ed2k_link = generate_ed2k_link(moved_to_write)
            new_record["标准链接"] = ed2k_link
            if ed2k_link:
                size, filehash = parse_ed2k_link(ed2k_link)
                new_record["大小"] = size
                new_record["散列"] = filehash
            else:
                new_record["大小"] = ""
                new_record["散列"] = ""

            new_records.append(new_record)
            print(f"已处理: {fp.name} (Index: {last_index})")
        except Exception as e:
            print(f"处理文件失败 {file_path}: {e}")
            continue

    if new_records:
        try:
            new_df = pd.DataFrame(new_records)
            df = pd.concat([df, new_df], ignore_index=True)
            df.to_excel(excel_path, index=False, engine="openpyxl")
            print(f"\n成功添加 {len(new_records)} 条记录到Excel")
            if pending_size_md4_list:
                for smd4 in pending_size_md4_list:
                    add_to_size_md4_database(size_md4_db_path, smd4)
                print(f"已将 {len(pending_size_md4_list)} 条 SizeMD4 写入数据库")
        except Exception as e:
            print(f"保存Excel文件失败: {e}")
            print(f"注意: {len(pending_size_md4_list)} 条 SizeMD4 未写入数据库")
            return False, duplicated_files
    else:
        print("没有新记录需要写入Excel")

    return True, duplicated_files


# ==================== 功能 2：多行 ed2k 链接入库 ====================

def process_ed2k_links_from_clipboard(size_md4_db_path: str) -> None:
    """从剪贴板读取多行 ed2k 链接，提取 SizeMD4 更新数据库。"""
    print("\n=== 多行ed2k链接写入数据库 ===")
    clipboard_text = get_clipboard_text()
    if not clipboard_text.strip():
        print("剪贴板为空，无法处理。")
        return

    lines = [line.strip() for line in clipboard_text.splitlines() if line.strip()]
    if not lines:
        print("剪贴板中没有有效行。")
        return

    size_md4_set = load_size_md4_database(size_md4_db_path)
    print(f"已加载 {len(size_md4_set)} 条 SizeMD4 记录")

    existed_links: list[str] = []
    new_count = 0

    for line in lines:
        ed2k_link = line
        if not ed2k_link.startswith("ed2k://|file|"):
            print(f"跳过非ed2k链接行: {line}")
            continue

        size_md4 = extract_size_md4(ed2k_link)
        if not size_md4:
            print(f"无法提取SizeMD4: {line}")
            continue

        if size_md4 in size_md4_set:
            existed_links.append(ed2k_link)
            print(f"SizeMD4已存在: {size_md4}")
        else:
            add_to_size_md4_database(size_md4_db_path, size_md4)
            size_md4_set.add(size_md4)
            new_count += 1
            print(f"已添加新SizeMD4: {size_md4}")

    print(f"\n处理完成：新增 {new_count} 条，已存在 {len(existed_links)} 条。")

    if existed_links:
        print("\n===== 已存在的ed2k链接列表 =====")
        list_text = "\n".join(existed_links)
        print(list_text)
        copy_to_clipboard(list_text)
    else:
        print("没有重复的链接。")


# ==================== 功能 3：单文件链接入库 ====================

def process_single_file_link(file_path: str, size_md4_db_path: str) -> None:
    """对单个本地文件生成 ed2k，更新数据库并报告。"""
    print(f"\n=== 处理单个文件: {file_path} ===")
    if not Path(file_path).is_file():
        print(f"错误：文件不存在 - {file_path}")
        return

    ed2k_link = generate_ed2k_link(file_path)
    if not ed2k_link:
        print("无法生成ed2k链接。")
        return
    print(f"生成的ed2k链接: {ed2k_link}")

    size_md4 = extract_size_md4(ed2k_link)
    if not size_md4:
        print("无法提取SizeMD4。")
        return

    size_md4_set = load_size_md4_database(size_md4_db_path)
    if size_md4 in size_md4_set:
        print(f"该文件的SizeMD4已存在于数据库中: {size_md4}")
        print("文件未新增入数据库。")
    else:
        add_to_size_md4_database(size_md4_db_path, size_md4)
        print(f"该文件的SizeMD4已添加到数据库: {size_md4}")
    print(f"SizeMD4值: {size_md4}")


# ==================== 功能 4：整理数据库 ====================

def sort_and_dedup_size_md4_db(db_path: str) -> None:
    """对 SizeMD4 数据库排序去重，先备份。"""
    print(f"\n=== 整理SizeMD4数据库 ===")
    p = Path(db_path)
    if not p.is_file():
        print(f"数据库文件不存在: {db_path}")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = Path(str(db_path) + f".bak_{timestamp}")
    try:
        shutil.copy2(str(p), str(backup_path))
        print(f"已创建备份: {backup_path}")
    except Exception as e:
        print(f"备份失败: {e}")
        return

    try:
        lines = [line.strip() for line in p.read_text(encoding="utf-8").splitlines()
                 if line.strip()]
        original_count = len(lines)
        unique_sorted = sorted(set(lines))
        new_count = len(unique_sorted)
        p.write_text("\n".join(unique_sorted) + "\n", encoding="utf-8")
        print(f"整理完成。原始: {original_count}，去重后: {new_count}。")
    except Exception as e:
        print(f"整理过程中出错: {e}")
        try:
            shutil.copy2(str(backup_path), str(p))
            print("已从备份恢复原文件。")
        except Exception:
            pass


def delete_from_size_md4_database(db_path: str, size_md4: str) -> bool:
    """从 SizeMD4 数据库文件中删除匹配的一行，返回是否找到并删除。"""
    p = Path(db_path)
    if not p.is_file():
        return False
    lines = [line.strip() for line in p.read_text(encoding="utf-8").splitlines()
             if line.strip()]
    new_lines = [l for l in lines if l != size_md4]
    if len(new_lines) != len(lines):
        p.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
        return True
    return False


# ==================== 功能 5：多行 ed2k 链接从数据库删除 ====================

def delete_ed2k_links_from_db(size_md4_db_path: str) -> None:
    """从剪贴板读取多行 ed2k 链接，提取 SizeMD4 并从数据库删除。"""
    print("\n=== 多行ed2k链接从数据库删除 ===")
    clipboard_text = get_clipboard_text()
    if not clipboard_text.strip():
        print("剪贴板为空，无法处理。")
        return

    lines = [line.strip() for line in clipboard_text.splitlines() if line.strip()]
    if not lines:
        print("剪贴板中没有有效行。")
        return

    print(f"已加载 {len(load_size_md4_database(size_md4_db_path))} 条 SizeMD4 记录")

    deleted_count = 0
    not_found_count = 0

    for line in lines:
        if not line.startswith("ed2k://|file|"):
            print(f"跳过非ed2k链接行: {line}")
            continue

        size_md4 = extract_size_md4(line)
        if not size_md4:
            print(f"无法提取SizeMD4: {line}")
            continue

        if delete_from_size_md4_database(size_md4_db_path, size_md4):
            deleted_count += 1
            print(f"已删除: {size_md4}")
        else:
            not_found_count += 1
            print(f"未找到: {size_md4}")

    print(f"\n处理完成：删除 {deleted_count} 条，未找到 {not_found_count} 条。")


# ==================== 功能 6：多行 SizeMD4 值从数据库删除 ====================

def delete_size_md4_from_db(size_md4_db_path: str) -> None:
    """从剪贴板读取多行 SizeMD4 值并从数据库删除。"""
    print("\n=== 多行SizeMD4值从数据库删除 ===")
    clipboard_text = get_clipboard_text()
    if not clipboard_text.strip():
        print("剪贴板为空，无法处理。")
        return

    lines = [line.strip() for line in clipboard_text.splitlines() if line.strip()]
    if not lines:
        print("剪贴板中没有有效行。")
        return

    print(f"已加载 {len(load_size_md4_database(size_md4_db_path))} 条 SizeMD4 记录")

    deleted_count = 0
    not_found_count = 0

    for line in lines:
        size_md4 = line.strip()
        if not size_md4:
            continue

        if delete_from_size_md4_database(size_md4_db_path, size_md4):
            deleted_count += 1
            print(f"已删除: {size_md4}")
        else:
            not_found_count += 1
            print(f"未找到: {size_md4}")

    print(f"\n处理完成：删除 {deleted_count} 条，未找到 {not_found_count} 条。")


# ==================== 主菜单 ====================

def main() -> None:
    print("=" * 60)
    print("文件处理与SizeMD4数据库管理工具")
    print("=" * 60)

    while True:
        print("\n请选择功能：")
        print("1. 文件夹写入Excel并写入数据库")
        print("2. 多行ed2k链接写入数据库")
        print("3. 单文件链接写入数据库")
        print("4. 多行ed2k链接从数据库删除")
        print("5. 多行SizeMD4值从数据库删除")
        print("6. 整理数据库（排序去重）")
        print("0. 退出")
        choice = input("请输入选项 (0-6): ").strip()

        if choice == "1":
            excel_path = get_input_with_default("Excel文件位置", str(DEFAULT_EXCEL_PATH))
            source_dir = get_input_with_default("源文件夹位置", str(DEFAULT_SOURCE_DIR))
            write_dir = get_input_with_default("写入文件夹位置", str(DEFAULT_WRITE_DIR))
            upload_dir = get_input_with_default("上传文件夹位置", str(DEFAULT_UPLOAD_DIR))
            delete_dir = get_input_with_default("删除文件夹位置", str(DEFAULT_DELETE_DIR))
            size_md4_db_path = get_input_with_default(
                "SizeMD4数据库文件位置", str(DEFAULT_SIZE_MD4_DB)
            )

            ensure_directory_exists(write_dir)
            ensure_directory_exists(upload_dir)
            ensure_directory_exists(delete_dir)
            ensure_directory_exists(str(Path(size_md4_db_path).parent))

            if not Path(excel_path).is_file():
                print(f"错误: Excel文件不存在 - {excel_path}，返回主菜单。")
                continue
            if not Path(source_dir).is_dir():
                print(f"错误: 源文件夹不存在 - {source_dir}，返回主菜单。")
                continue

            is_valid, err_msg = validate_directory_independence(
                source_dir, write_dir, upload_dir, delete_dir
            )
            if not is_valid:
                print(f"目录冲突错误: {err_msg}")
                print("已返回主菜单，请重新选择目录。")
                continue

            print("\n请输入以下字段值（直接回车则为空）：")
            reference_page = input("引用页: ").strip()
            belongs_to = input("属于: ").strip()
            main_link = input("主链接: ").strip()

            init_quit_handler()
            success, duplicated_files = process_folder_to_excel_and_db(
                excel_path, source_dir, write_dir, upload_dir, delete_dir,
                size_md4_db_path, reference_page, belongs_to, main_link,
            )

            print("\n文件夹处理完成！" if success else "\n文件夹处理中出现错误。")

            if duplicated_files:
                print("\n===== 以下文件因SizeMD4重复被移至删除文件夹 =====")
                dup_list = "\n".join(duplicated_files)
                print(dup_list)
                copy_to_clipboard(dup_list)
            else:
                print("没有重复文件。")

        elif choice == "2":
            size_md4_db_path = get_input_with_default(
                "SizeMD4数据库文件位置", str(DEFAULT_SIZE_MD4_DB)
            )
            ensure_directory_exists(str(Path(size_md4_db_path).parent))
            process_ed2k_links_from_clipboard(size_md4_db_path)

        elif choice == "3":
            file_path = get_input_with_default(
                "请输入文件路径", str(Path(r"d:\Studios\Attachments\标准.zip"))
            )
            size_md4_db_path = get_input_with_default(
                "SizeMD4数据库文件位置", str(DEFAULT_SIZE_MD4_DB)
            )
            ensure_directory_exists(str(Path(size_md4_db_path).parent))
            process_single_file_link(file_path, size_md4_db_path)

        elif choice == "4":
            size_md4_db_path = get_input_with_default(
                "SizeMD4数据库文件位置", str(DEFAULT_SIZE_MD4_DB)
            )
            ensure_directory_exists(str(Path(size_md4_db_path).parent))
            delete_ed2k_links_from_db(size_md4_db_path)

        elif choice == "5":
            size_md4_db_path = get_input_with_default(
                "SizeMD4数据库文件位置", str(DEFAULT_SIZE_MD4_DB)
            )
            ensure_directory_exists(str(Path(size_md4_db_path).parent))
            delete_size_md4_from_db(size_md4_db_path)

        elif choice == "6":
            size_md4_db_path = get_input_with_default(
                "SizeMD4数据库文件位置", str(DEFAULT_SIZE_MD4_DB)
            )
            sort_and_dedup_size_md4_db(size_md4_db_path)

        elif choice == "0":
            print("程序退出。")
            break
        else:
            print("无效选项，请重新输入。")

        input("\n按回车键继续...")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n用户中断程序，已退出。")
    except Exception as e:
        print(f"\n程序运行出错: {e}")
    finally:
        input("\n按回车键退出...")
