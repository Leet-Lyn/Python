# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件位置。
# 1. 如果源文件格式为 bmp / jpg / jpeg / png / 静态 webp / 静态 avif / 静态 heic / 静态 heif，则使用 magick 压缩成 avif 格式，命令如：magick convert input.jpg -quality 50 output.avif。
# 2. 如果图片文件格式为 gif / 动态 webp / 动态 avif / 动态 heic / 动态 heif / mp4，则使用：ffmpeg -i input -map 0:v -c:v libsvtav1 -crf 32 -preset 5 temp.mp4，再 ffmpeg -i temp.mp4 -c:v copy output.avif 生成 avif 动图。
# 生成的文件替换源文件。
# 如此循环，再次询问我源文件位置。

import signal
import subprocess
import sys
import uuid
from pathlib import Path

from PIL import Image

# --- 常量 ---
CREATION_FLAGS = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0

STATIC_EXTS = {".bmp", ".jpg", ".jpeg", ".png", ".webp", ".avif", ".heic", ".heif"}
ANIMATED_EXTS = {".gif", ".mp4"}
ALL_EXTS = STATIC_EXTS | ANIMATED_EXTS

_quit_requested = False  # Ctrl+Q 中断标志

# --- 消息常量 ---
MSG_INTERRUPTED = "\n\n用户中断程序，已退出。"
MSG_ERROR = "\n程序运行出错: {}"
MSG_EXIT = "\n按回车键退出..."
MSG_DETECT_ERROR = "  动态检测异常：{} | {}"
MSG_GENERATED = "  ✅ 已生成：{}"
MSG_MAGICK_FAIL = "  ❌ magick 失败：{}"
MSG_WEBP_FAIL = "  ❌ WebP→GIF 失败：{}"
MSG_FFMPEG_MP4_FAIL = "  ❌ ffmpeg（MP4）失败：{}"
MSG_FFMPEG_AVIF_FAIL = "  ❌ ffmpeg（AVIF）失败：{}"
MSG_PROMPT_FILE = "请输入文件路径（或输入 N 退出程序）："
MSG_FILE_NOT_FOUND = "文件不存在，请重新输入。"
MSG_UNSUPPORTED = "不支持的格式：{}"
MSG_PROCESSING = "  处理中：{}"
MSG_PROCESS_FAIL = "  ❌ 处理失败：{} | {}"
MSG_EXIT_OK = "\n程序已退出。"


def is_animated(filepath: Path) -> bool:
    """检测图像是否为动态图（多帧），Pillow 优先，Magick 兜底。"""
    ext = filepath.suffix.lower()
    try:
        # WebP / GIF / AVIF / HEIC / HEIF：Pillow 直接读帧数
        if ext in {".webp", ".gif", ".avif", ".heic", ".heif"}:
            with Image.open(filepath) as img:
                return bool(getattr(img, "is_animated", False))

        # 其余格式：Magick identify 读帧数
        result = subprocess.run(
            ["magick", "identify", "-format", "%n\n", str(filepath)],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            check=True,
        )
        return int(result.stdout.split("\n")[0]) > 1
    except Exception as e:
        print(MSG_DETECT_ERROR.format(filepath.name, e))
        return False


def convert_static(source: Path) -> bool:
    """静态图 → AVIF，成功返回 True 并删除源文件。"""
    output = source.with_suffix(".avif")
    # 用临时文件避免 input.avif 与 output.avif 同路径导致的读写冲突
    temp_output = source.with_name(f"{source.stem}_temp.avif")
    try:
        subprocess.run(
            ["magick", str(source), "-quality", "50", str(temp_output)],
            check=True,
            capture_output=True,
            creationflags=CREATION_FLAGS,
        )
        if temp_output.is_file() and temp_output.stat().st_size > 0:
            # 原子替换：先删旧文件，再将临时文件移入
            if output.exists():
                output.unlink()
            shutil.move(str(temp_output), str(output))
            if not _quit_requested:
                source.unlink()
            print(MSG_GENERATED.format(output))
            return True
    except subprocess.CalledProcessError as e:
        print(MSG_MAGICK_FAIL.format(e))
        if not _quit_requested:
            temp_output.unlink(missing_ok=True)
    return False


def convert_animated(source: Path) -> bool:
    """动态图 / 视频 → AV1 MP4 → AVIF 动图，成功返回 True 并删除源文件。"""
    temp_id = uuid.uuid4().hex[:8]
    base = source.with_suffix("")
    output = base.with_suffix(".avif")
    temp_mp4 = Path(f"{base}_temp_{temp_id}.mp4")
    temps: list[Path] = [temp_mp4]

    # 动态 WebP 需先转为临时 GIF
    if source.suffix.lower() == ".webp" and is_animated(source):
        temp_gif = Path(f"{base}_temp_{temp_id}.gif")
        temps.append(temp_gif)
        try:
            subprocess.run(
                ["magick", str(source), str(temp_gif)],
                check=True,
                capture_output=True,
                creationflags=CREATION_FLAGS,
            )
        except subprocess.CalledProcessError as e:
            print(MSG_WEBP_FAIL.format(e))
            cleanup_temps(temps)
            return False
        work_source = temp_gif
    else:
        work_source = source

    # 步骤 1：→ AV1 编码 MP4
    try:
        subprocess.run(
            [
                "ffmpeg", "-hide_banner", "-loglevel", "error",
                "-i", str(work_source), "-map", "0:v",
                "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2",
                "-c:v", "libsvtav1", "-crf", "32", "-preset", "5",
                "-movflags", "+faststart", "-an", "-sn", "-f", "mp4",
                str(temp_mp4),
            ],
            check=True,
            capture_output=True,
            creationflags=CREATION_FLAGS,
        )
    except subprocess.CalledProcessError as e:
        print(MSG_FFMPEG_MP4_FAIL.format(e))
        cleanup_temps(temps)
        return False

    # 步骤 2：MP4 → 动态 AVIF
    try:
        subprocess.run(
            [
                "ffmpeg", "-hide_banner", "-loglevel", "error",
                "-i", str(temp_mp4), "-map", "0:v", "-c:v", "copy", str(output),
            ],
            check=True,
            capture_output=True,
            creationflags=CREATION_FLAGS,
        )
    except subprocess.CalledProcessError as e:
        print(MSG_FFMPEG_AVIF_FAIL.format(e))
        if not _quit_requested:
            output.unlink(missing_ok=True)
        cleanup_temps(temps)
        return False

    # 成功：删源文件、清临时（保留临时残片当用户中断时）
    if not _quit_requested:
        source.unlink()
    cleanup_temps(temps)
    print(MSG_GENERATED.format(output))
    return True


def cleanup_temps(files: list[Path]) -> None:
    """删除临时文件列表。用户中断时保留临时残片。"""
    if _quit_requested:
        return
    for f in files:
        f.unlink(missing_ok=True)


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
    """主循环：输入文件 → 判断静/动态 → 转换 → 替换。"""
    _init_quit_handler()
    while True:
        if _check_quit():
            print(MSG_INTERRUPTED)
            break
        raw = input(MSG_PROMPT_FILE).strip()
        if raw.lower() == "n":
            break

        source = Path(raw.strip("\"'"))
        if not source.is_file():
            print(MSG_FILE_NOT_FOUND)
            continue

        ext = source.suffix.lower()
        if ext not in ALL_EXTS:
            print(MSG_UNSUPPORTED.format(ext))
            continue

        print(MSG_PROCESSING.format(source))

        try:
            if ext in STATIC_EXTS:
                if is_animated(source):
                    convert_animated(source)
                else:
                    convert_static(source)
            elif ext in ANIMATED_EXTS:
                convert_animated(source)
        except Exception as e:
            print(MSG_PROCESS_FAIL.format(source, e))

    print(MSG_EXIT_OK)



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
