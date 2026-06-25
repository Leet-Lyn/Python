# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件夹位置（默认 d:\Studios\Folders\Downloads\）与目标文件位置（默认 e:\Documents\Softwares\Codes\Python\Ed2kList.txt）。
# 遍历源文件夹内所有子文件夹中的文件，计算并生成该文件的 Ed2K 链接。
# 我安装了 RHash，位置：“d:\ProApps\rhash\current\rhash.exe”。生成 ed2k 的命令类似：rhash.exe --uppercase --ed2k-link "file_path"。
# 生成如 "ed2k://|file|rustdesk-1.4.3-x86_64.exe|23369352|DF952...|/" 的 ed2k 链接。
# 先清空目标文件，然后将生成的 ed2k 链接依次写入，一行一个。

# 导入模块
import signal
import subprocess
import sys
from pathlib import Path

# --- 常量 ---
RHASH = Path(r"d:\ProApps\rhash\current\rhash.exe")

_quit_requested = False  # Ctrl+Q 中断标志

# --- 消息常量 ---
MSG_INTERRUPTED = "\n\n用户中断程序，已退出。"
MSG_ERROR = "\n程序运行出错: {}"
MSG_EXIT = "\n按回车键退出..."
MSG_RHASH_MISSING = "错误：未找到 RHash —— {}"
MSG_RHASH_ERROR = "RHash 执行错误：{}"
MSG_NO_FILES = "源文件夹中没有文件。"
MSG_FOUND_FILES = "找到 {} 个文件，开始生成 ed2k 链接...\n"
MSG_SUCCESS = "  ✓ 成功"
MSG_FAIL = "  ✗ 失败"
MSG_DONE = "\n处理完成：成功 {} 个，失败 {} 个，共 {} 个。"
MSG_SAVED_TO = "ed2k 链接已保存到：{}"
MSG_PROMPT_SRC = "请输入源文件夹位置（回车使用默认 {}）："
MSG_SRC_NOT_FOUND = "错误：源文件夹 '{}' 不存在"
MSG_PROMPT_DST = "请输入目标文件位置（回车使用默认 {}）："
MSG_CONFIRM_INFO = "\n确认信息："
MSG_SRC_DIR = "  源文件夹：{}"
MSG_DST_FILE = "  目标文件：{}"
MSG_CONFIRM_START = "\n是否开始处理？（回车继续，N 取消）："
MSG_CANCELLED = "已取消操作"


def get_ed2k_link(file_path: Path) -> str | None:
    """使用 RHash 生成文件的 ed2k 链接，失败返回 None。"""
    command = [str(RHASH), "--uppercase", "--ed2k-link", str(file_path)]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            check=True,
        )
        return result.stdout.strip()
    except FileNotFoundError:
        print(MSG_RHASH_MISSING.format(RHASH))
        return None
    except subprocess.CalledProcessError as e:
        print(MSG_RHASH_ERROR.format(e))
        return None


def process_directory(source_dir: Path, target_file: Path) -> None:
    """遍历源文件夹，为所有文件生成 ed2k 链接并写入目标文件。"""
    # 收集所有文件
    all_files = sorted(
        p for p in source_dir.rglob("*")
        if p.is_file()
    )

    if not all_files:
        print(MSG_NO_FILES)
        return

    total = len(all_files)
    print(MSG_FOUND_FILES.format(total))

    # 清空目标文件
    target_file.parent.mkdir(parents=True, exist_ok=True)
    target_file.write_text("", encoding="utf-8")

    # 处理每个文件
    ok = 0
    fail = 0

    with target_file.open("a", encoding="utf-8") as fh:
        for idx, src in enumerate(all_files, 1):
            # 相对于源文件夹的路径，用于显示
            try:
                rel = src.relative_to(source_dir)
            except ValueError:
                rel = src

            print(f"[{idx}/{total}] {rel}")

            link = get_ed2k_link(src)
            if link:
                fh.write(link + "\n")
                ok += 1
                print(MSG_SUCCESS)
            else:
                fail += 1
                print(MSG_FAIL)

    print(MSG_DONE.format(ok, fail, total))
    print(MSG_SAVED_TO.format(target_file))
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
    """主流程：获取源文件夹与目标文件 → 批量生成 ed2k 链接。"""
    try:
        # --- 源文件夹 ---
        default_src = r"d:\Studios\Folders\Downloads"
        raw = input(MSG_PROMPT_SRC.format(default_src)).strip()
        source_dir = Path(raw.strip("\"'")) if raw else Path(default_src)

        if not source_dir.is_dir():
            print(MSG_SRC_NOT_FOUND.format(source_dir))
            return

        # --- 目标文件 ---
        default_dst = r"e:\Documents\Softwares\Codes\Python\Ed2kList.txt"
        raw = input(MSG_PROMPT_DST.format(default_dst)).strip()
        target_file = Path(raw.strip("\"'")) if raw else Path(default_dst)

        # --- 确认 ---
        print(MSG_CONFIRM_INFO)
        print(MSG_SRC_DIR.format(source_dir))
        print(MSG_DST_FILE.format(target_file))

        confirm = input(MSG_CONFIRM_START).strip().lower()
        if confirm in ("n", "no"):
            print(MSG_CANCELLED)
            return

        process_directory(source_dir, target_file)

    except KeyboardInterrupt:
        print(MSG_INTERRUPTED)


# ==================== 程序入口 ====================

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if not RHASH.is_file():
        print(MSG_RHASH_MISSING.format(RHASH))
        sys.exit(1)
    try:
        main()
    except KeyboardInterrupt:
        print(MSG_INTERRUPTED)
    except Exception as e:
        print(MSG_ERROR.format(e))
    finally:
        input(MSG_EXIT)
