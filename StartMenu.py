# 请帮我写个中文的 Python 脚本，批注也是中文。
# 开始询问我目标文件夹位置（默认为 E:\Backups\Windows\StartMenu\）。依次运行该文件夹下所有 *.lnk 指向的内容。

# 导入模块
import signal
import os
import sys
import time
from pathlib import Path

# ==================== 全局配置 ====================

DEFAULT_STARTMENU_DIR = Path(r"E:\Backups\Windows\StartMenu")

MSG_PROMPT_FOLDER = "请输入目标文件夹位置（默认 {default}）："
MSG_ERROR_DIR_NOT_FOUND = "错误：文件夹 '{folder}' 不存在。"
MSG_ERROR_RESOLVE = "错误：无法解析路径 '{path}' —— {error}"
MSG_NO_LNK_FOUND = "在文件夹 '{folder}' 中未找到任何快捷方式文件。"
MSG_FOUND_LNK = "找到 {count} 个快捷方式，开始依次启动...\n"
MSG_LAUNCH_OK = "✅ 已启动：{name}"
MSG_LAUNCH_FAIL = "❌ 启动失败：{name}\n    错误信息：{error}"
MSG_COMPLETE = "\n完成：成功 {ok} 个，失败 {fail} 个，共 {total} 个。"
MSG_INTERRUPTED = "\n\n用户中断程序，已退出。"
MSG_ERROR = "\n程序运行出错: {}"
MSG_EXIT = "\n按回车键退出..."

_quit_requested = False  # Ctrl+Q 中断标志

# ==================== 辅助函数 ====================


def get_folder_path(default: Path) -> Path:
    """获取文件夹路径，回车使用默认值。"""
    raw = input(MSG_PROMPT_FOLDER.format(default=default)).strip()
    return Path(raw) if raw else default


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
    """主流程：获取目标文件夹 → 扫描 .lnk → 依次启动 → 输出统计。"""
    # --- 获取目标文件夹路径 ---
    folder = get_folder_path(DEFAULT_STARTMENU_DIR)

    # 解析为绝对路径
    try:
        folder = folder.resolve()
    except OSError as e:
        print(MSG_ERROR_RESOLVE.format(path=folder, error=e))
        return

    # 检查目标文件夹是否存在
    if not folder.is_dir():
        print(MSG_ERROR_DIR_NOT_FOUND.format(folder=folder))
        return

    # --- 扫描目录下所有 .lnk 文件 ---
    lnk_files = sorted(
        p for p in folder.iterdir()
        if p.is_file() and p.suffix.lower() == ".lnk"
    )

    if not lnk_files:
        print(MSG_NO_LNK_FOUND.format(folder=folder))
        return

    print(MSG_FOUND_LNK.format(count=len(lnk_files)))

    # --- 依次启动 ---
    ok = 0
    fail = 0

    for lnk in lnk_files:
        try:
            os.startfile(str(lnk))
            print(MSG_LAUNCH_OK.format(name=lnk.name))
            ok += 1
        except Exception as e:
            print(MSG_LAUNCH_FAIL.format(name=lnk.name, error=e))
            fail += 1
        # 短暂间隔，避免瞬间打开大量应用导致系统卡顿
        time.sleep(0.3)

    # --- 输出统计 ---
    print(MSG_COMPLETE.format(ok=ok, fail=fail, total=len(lnk_files)))


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
