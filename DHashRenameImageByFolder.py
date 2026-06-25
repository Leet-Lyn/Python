# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件夹位置（默认 d:\Studios\Folders\Downloads\）与目标文件夹位置（默认 d:\Studios\Folders\Ins\）。
# 1. 如果源文件格式为 bmp / jpg / jpeg / png / 静态 webp / 静态 avif / 静态 heic / 静态 heif，则计算 imagehash.dhash，用哈希值重命名，前后用中括号包绕，如 [hash].jpg。
# 2. 如果图片文件格式为 gif / 动态 webp / 动态 avif / 动态 heic / 动态 heif / mp4，则取第一帧与最后一帧，分别计算 imagehash.dhash，用两个哈希值 + 帧数重命名，如 [hash1][24][hash2].gif。
# 生成的文件放到目标文件夹中保持源文件夹的子目录结构。成功则删除源文件。

import signal
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image
import imagehash

# ==================== 全局配置 ====================

DEFAULT_SOURCE_DIR = r"d:\Studios\Folders\Downloads"
DEFAULT_TARGET_DIR = r"d:\Studios\Folders\Ins"

STATIC_EXTS = {".bmp", ".jpg", ".jpeg", ".png"}
MAYBE_ANIMATED_EXTS = {".webp", ".avif", ".heic", ".heif"}
ANIMATED_EXTS = {".gif"}
VIDEO_EXTS = {".mp4"}
ALL_EXTS = STATIC_EXTS | MAYBE_ANIMATED_EXTS | ANIMATED_EXTS | VIDEO_EXTS

_quit_requested = False  # Ctrl+Q 中断标志

# --- 消息常量 ---
MSG_VIDEO_INFO_FAIL = "获取视频信息失败：{}，错误：{}"
MSG_EXTRACT_FRAME_FAIL_CODE = "提取视频帧失败：{}，时间：{}，错误码：{}"
MSG_FFMPEG_ERROR = "FFmpeg 错误信息：{}..."
MSG_EXTRACT_FRAME_FAIL = "提取视频帧失败：{}，时间：{}，错误：{}"
MSG_LAST_FRAME_FALLBACK = "无法提取最后一帧，使用第一帧替代：{}"
MSG_VIDEO_DURATION_FAIL = "获取视频时长失败：{}，错误：{}"
MSG_ANIMATION_DETECT_FAIL = "动态检测失败：{}，错误：{}"
MSG_FRAME_COUNT_FAIL = "获取图片帧数失败：{}，错误：{}"
MSG_HASH_FAIL = "计算哈希失败：{}，错误：{}"
MSG_STATIC_OK = "静态图片处理成功：{} → {}"
MSG_STATIC_FAIL = "静态图片处理失败：{}，错误：{}"
MSG_ANIMATED_OK = "动态图片处理成功：{} → {}"
MSG_ANIMATED_FAIL = "动态图片处理失败：{}，错误：{}"
MSG_VIDEO_EXTRACT_FRAME_FAIL = "无法提取视频帧：{}"
MSG_VIDEO_HASH_FAIL = "无法计算视频帧哈希：{}"
MSG_VIDEO_OK = "视频文件处理成功：{} → {}"
MSG_VIDEO_FAIL = "视频文件处理失败：{}，错误：{}"
MSG_ERROR_NO_FFMPEG = "错误：未找到 FFmpeg 或 FFprobe，请确保已正确安装并添加到系统 PATH"
MSG_FFMPEG_REFERENCE = "请参考：https://ffmpeg.org/download.html"
MSG_PROMPT_SOURCE_DIR = "请输入源文件夹路径（默认 {}）："
MSG_PROMPT_TARGET_DIR = "请输入目标文件夹路径（默认 {}）："
MSG_ERROR_SOURCE_NOT_FOUND = "错误：源文件夹不存在 —— {}"
MSG_START_PROCESS = "开始处理..."
MSG_SOURCE_DIR_LABEL = "源文件夹：{}"
MSG_TARGET_DIR_LABEL = "目标文件夹：{}"
MSG_SEPARATOR_LINE = "-" * 30
MSG_PROCESS_FAIL = "处理失败：{}"
MSG_PROCESS_ERROR = "处理文件时发生错误：{}，错误：{}"
MSG_DONE = "处理完成：成功 {} 个，失败 {} 个，共 {} 个。"
MSG_INTERRUPTED = "\n\n用户中断程序，已退出。"
MSG_ERROR = "\n程序运行出错: {}"
MSG_EXIT = "\n按回车键退出..."


# =========================
# 视频工具
# =========================

def get_video_info(filepath: Path) -> int:
    """使用 ffprobe 获取视频帧数，失败返回 100。"""
    try:
        cmd = [
            "ffprobe", "-v", "error", "-select_streams", "v:0",
            "-show_entries", "stream=nb_frames,r_frame_rate,duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(filepath),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output_lines = result.stdout.strip().split("\n")

        frame_rate = None
        duration = None
        frame_count = None

        for line in output_lines:
            if "/" in line:
                frame_rate = line
            elif line.replace(".", "").isdigit():
                if "." in line:
                    duration = float(line)
                else:
                    frame_count = int(line)

        if frame_count is None and duration and frame_rate:
            try:
                num, den = map(int, frame_rate.split("/"))
                frame_count = int(duration * num / den)
            except Exception:
                frame_count = 100

        return frame_count or 100
    except Exception as e:
        print(MSG_VIDEO_INFO_FAIL.format(filepath, e))
        return 100


def extract_video_frame(filepath: Path, frame_time: float, output_path: Path) -> bool:
    """使用 ffmpeg 提取视频指定时间点的帧。"""
    try:
        cmd = [
            "ffmpeg", "-i", str(filepath), "-ss", str(frame_time),
            "-vframes", "1", "-q:v", "2", "-y",
            "-avoid_negative_ts", "make_zero",
            "-fflags", "+genpts",
            str(output_path),
        ]
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(MSG_EXTRACT_FRAME_FAIL_CODE.format(filepath, frame_time, e.returncode))
        if e.stderr:
            print(MSG_FFMPEG_ERROR.format(e.stderr[:200]))
        return False
    except Exception as e:
        print(MSG_EXTRACT_FRAME_FAIL.format(filepath, frame_time, e))
        return False


def extract_first_and_last_frames(filepath: Path, temp_dir: str) -> tuple[Path | None, Path | None]:
    """提取视频的第一帧和最后一帧。"""
    temp = Path(temp_dir)
    first_frame = temp / "first_frame.jpg"
    last_frame = temp / "last_frame.jpg"

    if not extract_video_frame(filepath, 0, first_frame):
        return None, None

    try:
        cmd = [
            "ffprobe", "-v", "error", "-show_entries",
            "format=duration", "-of", "default=noprint_wrappers=1:nokey=1",
            str(filepath),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        duration = float(result.stdout.strip())

        last_frame_time = max(0, duration - 0.5)
        if not extract_video_frame(filepath, last_frame_time, last_frame):
            last_frame_time = max(0, duration - 1.0)
            if not extract_video_frame(filepath, last_frame_time, last_frame):
                print(MSG_LAST_FRAME_FALLBACK.format(filepath))
                shutil.copy2(str(first_frame), str(last_frame))
    except Exception as e:
        print(MSG_VIDEO_DURATION_FAIL.format(filepath, e))
        shutil.copy2(str(first_frame), str(last_frame))

    return first_frame, last_frame


# =========================
# 图像检测
# =========================

def is_animated_image(filepath: Path) -> bool:
    """检测图片是否为动态图。"""
    try:
        if filepath.suffix.lower() == ".mp4":
            return True
        with Image.open(filepath) as img:
            if hasattr(img, "is_animated"):
                return img.is_animated
            try:
                img.seek(1)
                return True
            except EOFError:
                return False
    except Exception as e:
        print(MSG_ANIMATION_DETECT_FAIL.format(filepath, e))
        return False


def get_image_frame_count(filepath: Path) -> int:
    """获取动态图片的帧数。"""
    try:
        frame_count = 1
        with Image.open(filepath) as img:
            if hasattr(img, "is_animated") and img.is_animated:
                while True:
                    try:
                        img.seek(frame_count)
                        frame_count += 1
                    except EOFError:
                        break
        return frame_count
    except Exception as e:
        print(MSG_FRAME_COUNT_FAIL.format(filepath, e))
        return 1


def calculate_image_hash(filepath: Path):
    """计算图片的 dhash 值。"""
    try:
        with Image.open(filepath) as img:
            return imagehash.dhash(img)
    except Exception as e:
        print(MSG_HASH_FAIL.format(filepath, e))
        return None


# =========================
# 处理函数
# =========================

def process_static_image(source: Path, dst_dir: Path, relative_dir: Path) -> bool:
    """处理静态图片：dhash 重命名 → 复制到目标。"""
    try:
        hash_value = calculate_image_hash(source)
        if hash_value is None:
            return False

        new_name = f"[{str(hash_value).upper()}]{source.suffix}"
        target_dir = dst_dir / relative_dir
        target_dir.mkdir(parents=True, exist_ok=True)
        dst = target_dir / new_name

        shutil.copy2(str(source), str(dst))
        print(MSG_STATIC_OK.format(source.name, new_name))
        return True
    except Exception as e:
        print(MSG_STATIC_FAIL.format(source, e))
        return False


def process_animated_image(source: Path, dst_dir: Path, relative_dir: Path) -> bool:
    """处理动态图片：首/末帧 dhash + 帧数重命名 → 复制到目标。"""
    try:
        frame_count = get_image_frame_count(source)

        with Image.open(source) as img:
            img.seek(0)
            first_hash = imagehash.dhash(img)
            try:
                last_idx = frame_count - 1 if frame_count > 1 else 0
                img.seek(last_idx)
                last_hash = imagehash.dhash(img)
            except Exception:
                last_hash = first_hash

        new_name = (
            f"[{str(first_hash).upper()}]"
            f"[{frame_count}]"
            f"[{str(last_hash).upper()}]"
            f"{source.suffix}"
        )
        target_dir = dst_dir / relative_dir
        target_dir.mkdir(parents=True, exist_ok=True)
        dst = target_dir / new_name

        shutil.copy2(str(source), str(dst))
        print(MSG_ANIMATED_OK.format(source.name, new_name))
        return True
    except Exception as e:
        print(MSG_ANIMATED_FAIL.format(source, e))
        return False


def process_video_file(source: Path, dst_dir: Path, relative_dir: Path) -> bool:
    """处理视频文件：提取首/末帧 → dhash + 帧数重命名 → 复制到目标。"""
    try:
        frame_count = get_video_info(source)

        with tempfile.TemporaryDirectory() as temp_dir:
            first_frame, last_frame = extract_first_and_last_frames(source, temp_dir)

            if first_frame is None or not first_frame.is_file():
                print(MSG_VIDEO_EXTRACT_FRAME_FAIL.format(source))
                return False

            first_hash = calculate_image_hash(first_frame)
            last_hash = calculate_image_hash(last_frame)

            if first_hash is None:
                print(MSG_VIDEO_HASH_FAIL.format(source))
                return False
            if last_hash is None:
                last_hash = first_hash

        new_name = (
            f"[{str(first_hash).upper()}]"
            f"[{frame_count}]"
            f"[{str(last_hash).upper()}]"
            f"{source.suffix}"
        )
        target_dir = dst_dir / relative_dir
        target_dir.mkdir(parents=True, exist_ok=True)
        dst = target_dir / new_name

        shutil.copy2(str(source), str(dst))
        print(MSG_VIDEO_OK.format(source.name, new_name))
        return True
    except Exception as e:
        print(MSG_VIDEO_FAIL.format(source, e))
        return False


# =========================
# 主流程
# =========================

def check_ffmpeg_available() -> bool:
    """检查 ffmpeg 和 ffprobe 是否可用。"""
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        subprocess.run(["ffprobe", "-version"], capture_output=True, check=True)
        return True
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
    """主流程：获取路径 → 遍历分类处理 → 统计。"""
    _init_quit_handler()

    if not check_ffmpeg_available():
        print(MSG_ERROR_NO_FFMPEG)
        print(MSG_FFMPEG_REFERENCE)
        return

    raw = input(MSG_PROMPT_SOURCE_DIR.format(DEFAULT_SOURCE_DIR)).strip()
    src_folder = Path(raw) if raw else Path(DEFAULT_SOURCE_DIR)
    raw = input(MSG_PROMPT_TARGET_DIR.format(DEFAULT_TARGET_DIR)).strip()
    dst_folder = Path(raw) if raw else Path(DEFAULT_TARGET_DIR)

    if not src_folder.is_dir():
        print(MSG_ERROR_SOURCE_NOT_FOUND.format(src_folder))
        return

    dst_folder.mkdir(parents=True, exist_ok=True)

    print(MSG_START_PROCESS)
    print(MSG_SOURCE_DIR_LABEL.format(src_folder))
    print(MSG_TARGET_DIR_LABEL.format(dst_folder))
    print(MSG_SEPARATOR_LINE)

    ok = 0
    fail = 0

    for src_path in src_folder.rglob("*"):
        if _check_quit():
            print("\n⚠ 用户中断（Ctrl+Q），已处理部分不会丢失。")
            break
        if not src_path.is_file():
            continue

        ext = src_path.suffix.lower()
        if ext not in ALL_EXTS:
            continue

        try:
            try:
                rel = src_path.parent.relative_to(src_folder)
            except ValueError:
                rel = Path()

            success = False

            if ext in STATIC_EXTS:
                success = process_static_image(src_path, dst_folder, rel)
            elif ext in MAYBE_ANIMATED_EXTS:
                if is_animated_image(src_path):
                    success = process_animated_image(src_path, dst_folder, rel)
                else:
                    success = process_static_image(src_path, dst_folder, rel)
            elif ext in ANIMATED_EXTS:
                success = process_animated_image(src_path, dst_folder, rel)
            elif ext in VIDEO_EXTS:
                success = process_video_file(src_path, dst_folder, rel)

            if success:
                if not _quit_requested:
                    src_path.unlink()
                ok += 1
            else:
                fail += 1
                print(MSG_PROCESS_FAIL.format(src_path))
        except Exception as e:
            print(MSG_PROCESS_ERROR.format(src_path, e))
            fail += 1

        if _check_quit():
            print("\n⚠ 用户中断（Ctrl+Q），已处理部分不会丢失。")
            break

    print(MSG_SEPARATOR_LINE)
    print(MSG_DONE.format(ok, fail, ok + fail))



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
