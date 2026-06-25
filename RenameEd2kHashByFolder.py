# 请帮我写个中文的 Python 脚本，批注也是中文：
# 请输入源文件夹位置（默认"d:\Studios\Folders\Downloads\"）
# 我安装了 RHash，位置"d:\ProApps\rhash\current\rhash.exe"。生成 ed2k 的命令类似：rhash.exe --uppercase --ed2k-link "\\TS-464C\Temps\rustdesk-1.4.3-x86_64.exe"。生成如"ed2k://|file|rustdesk-1.4.3-x86_64.exe|23369352|DF952EEB0438E288409858E6C960E261|h=T7BJKLDRQ7VDCDKOO525FO7YHJCZVKDK|/"的ed2k链接。
# 用文件名大小与 ed2k hash 对文件夹及其子文件夹下所有文件重命名。如 rustdesk-1.4.3-x86_64.exe 重命名为 [23369352][DF952EEB0438E288409858E6C960E261].exe（用方括号包绕，扩展名不变）。

import signal
import subprocess
import sys
from pathlib import Path

# ==================== 全局配置 ====================

DEFAULT_SOURCE_DIR = Path(r"d:\Studios\Folders\Downloads")
DEFAULT_RHASH_PATH = Path(r"d:\ProApps\rhash\current\rhash.exe")

_quit_requested = False  # Ctrl+Q 中断标志

# --- 消息常量 ---
MSG_PROMPT_SOURCE_DIR = "请输入源文件夹位置："
MSG_ERROR_RHASH_NOT_FOUND = "错误：找不到 RHash 工具 —— {}"
MSG_ERROR_PARSE_RHASH = "无法解析 RHash 输出：{}"
MSG_ERROR_RHASH_EXEC = "RHash 执行错误：{}"
MSG_ERROR_ED2K_HASH = "计算文件 {} 的 ED2K 哈希时出错：{}"
MSG_ERROR_INVALID_DIR = "指定的路径无效，请确保它是一个文件夹。"
MSG_SKIP_EMPTY = "{} 是空文件，已跳过。"
MSG_SKIP_NO_HASH = "无法计算文件 {} 的 ED2K 哈希，已跳过。"
MSG_SKIP_EXISTS = "目标文件已存在，跳过重命名：{}"
MSG_RENAME_OK = "成功重命名：{} -> {}"
MSG_RENAME_FAIL = "无法重命名文件 {}: {}"
MSG_DONE = "完成！共重命名了 {} 个文件。"
MSG_INTERRUPTED = "\n\n用户中断程序，已退出。"
MSG_ERROR = "\n程序运行出错: {}"
MSG_EXIT = "\n按回车键退出..."

# ==================== 辅助函数 ====================


def get_input_with_default(prompt_text: str, default_value: str) -> str:
    """获取带默认值的用户输入。"""
    user_input = input(f"{prompt_text} (默认: {default_value}): ").strip()
    return user_input if user_input else str(default_value)


def ed2k_hash(file_path: Path) -> str:
    """
    使用 RHash 计算文件的 ED2K 哈希值。
    返回哈希值字符串，失败时返回空字符串。
    """
    if not DEFAULT_RHASH_PATH.is_file():
        print(MSG_ERROR_RHASH_NOT_FOUND.format(DEFAULT_RHASH_PATH))
        return ""

    try:
        cmd = [str(DEFAULT_RHASH_PATH), "--uppercase", "--ed2k-link", str(file_path)]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

        # 输出格式：ed2k://|file|filename|filesize|HASH|...|/
        parts = result.stdout.strip().split("|")
        if len(parts) >= 5:
            return parts[4]  # 哈希值在第五个位置
        else:
            print(MSG_ERROR_PARSE_RHASH.format(result.stdout.strip()))
            return ""
    except subprocess.CalledProcessError as e:
        print(MSG_ERROR_RHASH_EXEC.format(e))
        return ""
    except OSError as e:
        print(MSG_ERROR_ED2K_HASH.format(file_path.name, e))
        return ""


# ==================== 处理函数 ====================


def rename_files_by_ed2k(source_dir: Path) -> int:
    """
    遍历文件夹及其子文件夹，将文件重命名为 [大小][ED2K哈希].扩展名 格式。
    返回重命名的文件数量。
    """
    if not source_dir.is_dir():
        print(MSG_ERROR_INVALID_DIR)
        return 0

    renamed_count = 0

    for file_path in source_dir.rglob("*"):
        if not file_path.is_file():
            continue

        file_size = file_path.stat().st_size
        if file_size == 0:
            print(MSG_SKIP_EMPTY.format(file_path.name))
            continue

        file_hash = ed2k_hash(file_path)
        if not file_hash:
            print(MSG_SKIP_NO_HASH.format(file_path.name))
            continue

        new_name = f"[{file_size}][{file_hash}]{file_path.suffix.lower()}"
        new_path = file_path.parent / new_name

        if new_path.exists():
            print(MSG_SKIP_EXISTS.format(new_name))
            continue

        try:
            file_path.rename(new_path)
            print(MSG_RENAME_OK.format(file_path.name, new_name))
            renamed_count += 1
        except OSError as e:
            print(MSG_RENAME_FAIL.format(file_path, e))

    return renamed_count


# ==================== 主程序 ====================
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
    """主函数：获取用户输入并执行文件重命名操作。"""

    source_str = get_input_with_default(
        MSG_PROMPT_SOURCE_DIR, str(DEFAULT_SOURCE_DIR))
    source_dir = Path(source_str)

    count = rename_files_by_ed2k(source_dir)
    print(MSG_DONE.format(count))


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
