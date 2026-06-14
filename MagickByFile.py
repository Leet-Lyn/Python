# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件位置。
# 1. 如果源文件格式为 bmp / jpg / jpeg / png / 静态 webp / 静态 avif / 静态 heic / 静态 heif，则使用 magick 压缩成 avif 格式，命令如：magick convert input.jpg -quality 50 output.avif。
# 2. 如果图片文件格式为 gif / 动态 webp / 动态 avif / 动态 heic / 动态 heif / mp4，则使用：ffmpeg -i input -map 0:v -c:v libsvtav1 -crf 32 -preset 5 temp.mp4，再 ffmpeg -i temp.mp4 -c:v copy output.avif 生成 avif 动图。
# 生成的文件替换源文件。
# 如此循环，再次询问我源文件位置。

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
        print(f"  动态检测异常：{filepath.name} | {e}")
        return False


def convert_static(source: Path) -> bool:
    """静态图 → AVIF，成功返回 True 并删除源文件。"""
    output = source.with_suffix(".avif")
    try:
        subprocess.run(
            ["magick", str(source), "-quality", "50", str(output)],
            check=True,
            capture_output=True,
            creationflags=CREATION_FLAGS,
        )
        if output.is_file() and output.stat().st_size > 0:
            source.unlink()
            print(f"  ✅ 已生成：{output}")
            return True
    except subprocess.CalledProcessError as e:
        print(f"  ❌ magick 失败：{e}")
        output.unlink(missing_ok=True)
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
            print(f"  ❌ WebP→GIF 失败：{e}")
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
        print(f"  ❌ ffmpeg（MP4）失败：{e}")
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
        print(f"  ❌ ffmpeg（AVIF）失败：{e}")
        output.unlink(missing_ok=True)
        cleanup_temps(temps)
        return False

    # 成功：删源文件、清临时
    source.unlink()
    cleanup_temps(temps)
    print(f"  ✅ 已生成：{output}")
    return True


def cleanup_temps(files: list[Path]) -> None:
    """删除临时文件列表。"""
    for f in files:
        f.unlink(missing_ok=True)


def main() -> None:
    """主循环：输入文件 → 判断静/动态 → 转换 → 替换。"""
    while True:
        raw = input("\n请输入文件路径（输入 N 退出）：").strip()
        if raw.lower() == "n":
            break

        source = Path(raw.strip("\"'"))
        if not source.is_file():
            print("文件不存在，请重新输入。")
            continue

        ext = source.suffix.lower()
        if ext not in ALL_EXTS:
            print(f"不支持的格式：{ext}")
            continue

        print(f"  处理中：{source}")

        try:
            if ext in STATIC_EXTS:
                if is_animated(source):
                    convert_animated(source)
                else:
                    convert_static(source)
            elif ext in ANIMATED_EXTS:
                convert_animated(source)
        except Exception as e:
            print(f"  ❌ 处理失败：{source} | {e}")

    print("\n程序已退出。")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
    input("按回车键退出...")
