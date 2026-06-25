# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件夹位置（默认 D:\Studios\Folders\Ins\）与目标文件夹位置
# （默认 D:\Studios\Folders\Outs\）。
# 依次读取源文件夹下所有图片文件（bmp / jpg / jpeg / png / webp / avif / heic），
# 调整大小。强制 640×640 正方形（不保持纵横比）。
# 生成的文件放到目标文件夹中保持子目录结构。成功则删除源文件。

import signal
import sys
from pathlib import Path

from PIL import Image

# ==================== 全局配置 ====================

DEFAULT_SOURCE_DIR = r"D:\Studios\Folders\Ins"
DEFAULT_TARGET_DIR = r"D:\Studios\Folders\Outs"
VALID_EXTS = {".bmp", ".jpg", ".jpeg", ".png", ".webp", ".avif", ".heic"}
TARGET_SIZE = (640, 640)

_quit_requested = False  # Ctrl+Q 中断标志

# --- 消息常量 ---
MSG_PROMPT_SOURCE_DIR = "请输入源文件夹（回车默认 {}）："
MSG_PROMPT_TARGET_DIR = "请输入目标文件夹（回车默认 {}）："
MSG_ERROR_SOURCE_NOT_FOUND = "错误：源文件夹不存在 —— {}"
MSG_RESIZE_OK = "  ✅ {} → {}"
MSG_RESIZE_FAIL = "  ❌ 处理失败：{} | {}"
MSG_NO_FILES = "未找到可处理的图片文件。"
MSG_FOUND_FILES = "找到 {} 个文件，开始强制 640×640 调整...\n"
MSG_PROGRESS = "[{}/{}] {}"
MSG_DONE = "处理完成：成功 {} 个，失败 {} 个，共 {} 个。"
MSG_INTERRUPTED = "\n\n用户中断程序，已退出。"
MSG_ERROR = "\n程序运行出错: {}"
MSG_EXIT = "\n按回车键退出..."


def resize_image(source: Path, output: Path) -> bool:
    """强制调整为 640×640，保存到 output，成功返回 True 并删除 source。"""
    try:
        with Image.open(source) as img:
            resized = img.resize(TARGET_SIZE, Image.LANCZOS)
            output.parent.mkdir(parents=True, exist_ok=True)
            resized.save(output, quality=95)
        source.unlink()
        print(MSG_RESIZE_OK.format(source.name, output))
        return True
    except Exception as e:
        print(MSG_RESIZE_FAIL.format(source.name, e))
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
    """主流程：获取源/目标文件夹 → 遍历图片 → 强制 640×640 → 统计。"""
    raw = input(MSG_PROMPT_SOURCE_DIR.format(DEFAULT_SOURCE_DIR)).strip()
    src_root = Path(raw) if raw else Path(DEFAULT_SOURCE_DIR)
    raw = input(MSG_PROMPT_TARGET_DIR.format(DEFAULT_TARGET_DIR)).strip()
    dst_root = Path(raw) if raw else Path(DEFAULT_TARGET_DIR)

    if not src_root.is_dir():
        print(MSG_ERROR_SOURCE_NOT_FOUND.format(src_root))
        return

    # 收集所有图片文件
    all_files = sorted(
        p for p in src_root.rglob("*")
        if p.is_file() and p.suffix.lower() in VALID_EXTS
    )
    total = len(all_files)

    if not total:
        print(MSG_NO_FILES)
        return

    print(MSG_FOUND_FILES.format(total))
    ok = 0
    fail = 0

    for idx, src in enumerate(all_files, 1):
        try:
            rel = src.parent.relative_to(src_root)
        except ValueError:
            rel = Path()
        dst = dst_root / rel / src.name

        print(MSG_PROGRESS.format(idx, total, src.relative_to(src_root)))
        if resize_image(src, dst):
            ok += 1
        else:
            fail += 1

    print(MSG_DONE.format(ok, fail, total))



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
