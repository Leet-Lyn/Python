# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件夹位置（默认 d:\Studios\Folders\Ins\）与目标文件夹位置（默认 d:\Studios\Folders\Outs\）。
# 遍历源文件夹内所有子文件夹中的文件（剔除隐藏文件）。
# 用 Leanify 进行压缩，生成的文件放到目标文件夹中保持子目录结构。

import signal
import shutil
import subprocess
import sys
from pathlib import Path

# ==================== 全局配置 ====================

DEFAULT_SOURCE_DIR = r"d:\Studios\Folders\Ins"
DEFAULT_TARGET_DIR = r"d:\Studios\Folders\Outs"
LEANIFY_EXE = Path(r"D:\ProApps\Leanify\Leanify.exe")

_quit_requested = False  # Ctrl+Q 中断标志

# --- 消息常量 ---
MSG_PROMPT_SOURCE_DIR = "请输入源文件夹位置（回车默认 d:\\Studios\\Folders\\Ins\\）："
MSG_PROMPT_TARGET_DIR = "请输入目标文件夹位置（回车默认 d:\\Studios\\Folders\\Outs\\）："
MSG_ERROR_INVALID_SOURCE = "源文件夹路径无效：{}"
MSG_COPY_FIRST = "📋 复制到目标…"
MSG_COMPRESS_OK = "✅ {} → {}"
MSG_COMPRESS_FAIL = "❌ 压缩失败：{}，错误码：{}"
MSG_LEANIFY_NOT_FOUND = "❌ 未找到 Leanify：{}"
MSG_PROCESS_ERROR = "❌ 处理文件 {} 时发生错误：{}"
MSG_DONE = "处理完成：成功 {}，失败 {}，跳过隐藏 {}，共扫描 {}。"
MSG_INTERRUPTED = "\n\n用户中断程序，已退出。"
MSG_ERROR = "\n程序运行出错: {}"
MSG_EXIT = "\n按回车键退出..."


def is_hidden_file(file_path: Path) -> bool:
    """判断文件是否为隐藏文件。"""
    # 文件名以点开头（Unix/Linux / 部分 Windows 场景）
    if file_path.name.startswith("."):
        return True

    # Windows 文件属性检查
    try:
        import win32con
        import win32file
        attributes = win32file.GetFileAttributes(str(file_path))
        return bool(attributes & (win32con.FILE_ATTRIBUTE_HIDDEN | win32con.FILE_ATTRIBUTE_SYSTEM))
    except Exception:
        pass

    try:
        return bool(file_path.stat().st_file_attributes & 0x2)
    except Exception:
        return False
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
    """主流程：获取源/目标文件夹 → 遍历文件 → Leanify 压缩 → 统计。"""
    raw = input(MSG_PROMPT_SOURCE_DIR).strip()
    input_path = Path(raw) if raw else Path(DEFAULT_SOURCE_DIR)
    raw = input(MSG_PROMPT_TARGET_DIR).strip()
    output_path = Path(raw) if raw else Path(DEFAULT_TARGET_DIR)

    if not input_path.is_dir():
        print(MSG_ERROR_INVALID_SOURCE.format(input_path))
        return

    output_path.mkdir(parents=True, exist_ok=True)

    total = 0
    ok = 0
    skipped = 0
    fail = 0

    for file_path in input_path.rglob("*"):
        if not file_path.is_file():
            continue

        if is_hidden_file(file_path):
            skipped += 1
            continue

        total += 1
        relative_dir = file_path.parent.relative_to(input_path)
        target_dir = output_path / relative_dir
        target_dir.mkdir(parents=True, exist_ok=True)
        target_file = target_dir / file_path.name

        try:
            # 先复制源文件到目标，再对副本运行 Leanify（原地压缩），保留源文件不变
            shutil.copy2(str(file_path), str(target_file))
            result = subprocess.run(
                [str(LEANIFY_EXE), str(target_file)],
                capture_output=True,
            )

            if result.returncode == 0:
                print(MSG_COMPRESS_OK.format(file_path, target_file))
                ok += 1
            else:
                print(MSG_COMPRESS_FAIL.format(file_path, result.returncode))
                target_file.unlink(missing_ok=True)
                fail += 1
        except FileNotFoundError:
            print(MSG_LEANIFY_NOT_FOUND.format(LEANIFY_EXE))
            return
        except Exception as e:
            print(MSG_PROCESS_ERROR.format(file_path, e))
            target_file.unlink(missing_ok=True)
            fail += 1

    print(MSG_DONE.format(ok, fail, skipped, total + skipped))



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
