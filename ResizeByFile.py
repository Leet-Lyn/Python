# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件位置。
# 将该图片文件（bmp、jpg、jpeg、png、webp、avif、heic）调整大小。
# 让我选择：1.640*480：宽度640，高度根据宽度调整保持纵横比；2.800*600：宽度800，高度根据宽度调整保持纵横比；3.1024*768：宽度1024，高度根据宽度调整保持纵横比；4.1280*720：宽度1280，高度根据宽度调整保持纵横比；5.1920*1080：宽度1920，高度根据宽度调整保持纵横比；5.3840*2160：宽度3840，高度根据宽度调整保持纵横比；5.7680*4320：宽度7680，高度根据宽度调整保持纵横比；
# 选项 0：强制 640×640 正方形（不保持纵横比）。其余选项：宽度固定，高度按纵横比自动计算。
# 生成的文件替换源文件。
# 如此循环，再次前询问我源文件位置。

import signal
import sys
from pathlib import Path

from PIL import Image

# ==================== 全局配置 ====================

VALID_EXTS = {".bmp", ".jpg", ".jpeg", ".png", ".webp", ".avif", ".heic"}

SIZE_OPTIONS: dict[str, tuple[int | tuple[int, int], str]] = {
    "0": ((640, 640), "640×640  (正方) [默认]"),
    "1": (640,   "640×480  (标清)"),
    "2": (800,   "800×600  (SVGA)"),
    "3": (1024,  "1024×768 (XGA)"),
    "4": (1280,  "1280×720 (高清)"),
    "5": (1920,  "1920×1080 (全高清)"),
    "6": (3840,  "3840×2160 (4K)"),
    "7": (7680,  "7680×4320 (8K)"),
}

_quit_requested = False  # Ctrl+Q 中断标志

# --- 消息常量 ---
MSG_PROMPT_FILE = "请输入图片路径（输入 Q 退出）: "
MSG_PROGRAM_EXIT = "程序已退出"
MSG_ERROR_FILE_NOT_FOUND = "错误：文件不存在，请重新输入"
MSG_ERROR_UNSUPPORTED_EXT = "错误：不支持的格式 {}，支持: {}"
MSG_PROMPT_SIZE = "请选择目标尺寸（回车默认 640×640）:"
MSG_OPTION_LINE = "  {}. {}"
MSG_PROMPT_OPTION = "请输入选项数字 (0-7, 默认 0): "
MSG_INVALID_OPTION = "无效选择，将使用默认尺寸 640×640"
MSG_RESIZE_OK = "✓ 已调整尺寸: {}×{} | 覆盖保存: {}"
MSG_RESIZE_FAIL = "✗ 处理失败: {}"
MSG_INTERRUPTED = "\n\n用户中断程序，已退出。"
MSG_ERROR = "\n程序运行出错: {}"
MSG_EXIT = "\n按回车键退出..."


def resize_image(image_path: Path, target: int | tuple[int, int]) -> None:
    """调整图片大小并覆盖源文件。int=固定宽度保持纵横比；tuple=强制该尺寸。"""
    try:
        with Image.open(image_path) as img:
            if isinstance(target, tuple):
                size = target
            else:
                w_percent = target / float(img.size[0])
                new_height = int(float(img.size[1]) * w_percent)
                size = (target, new_height)
            resized_img = img.resize(size, Image.LANCZOS)
            resized_img.save(image_path, quality=95)
            print(MSG_RESIZE_OK.format(size[0], size[1], image_path))
    except Exception as e:
        print(MSG_RESIZE_FAIL.format(e))
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
    """主循环：输入文件 → 选择尺寸 → 调整 → 替换。"""
    while True:
        raw = input("\n" + MSG_PROMPT_FILE).strip()

        if raw.lower() in ("q", "quit", "exit"):
            print(MSG_PROGRAM_EXIT)
            break

        source = Path(raw.strip("\"'"))
        if not source.is_file():
            print(MSG_ERROR_FILE_NOT_FOUND)
            continue

        ext = source.suffix.lower()
        if ext not in VALID_EXTS:
            print(MSG_ERROR_UNSUPPORTED_EXT.format(ext, ", ".join(sorted(VALID_EXTS))))
            continue

        print(MSG_PROMPT_SIZE)
        for key in sorted(SIZE_OPTIONS, key=int):
            _, label = SIZE_OPTIONS[key]
            print(MSG_OPTION_LINE.format(key, label))

        choice = input(MSG_PROMPT_OPTION).strip() or "0"
        if choice in SIZE_OPTIONS:
            target, _ = SIZE_OPTIONS[choice]
        else:
            print(MSG_INVALID_OPTION)
            target, _ = SIZE_OPTIONS["0"]

        resize_image(source, target)



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
