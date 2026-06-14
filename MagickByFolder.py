# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件夹位置（默认：d:\Studios\Folders\Ins\）与目标文件夹位置（默认：d:\Studios\Folders\Outs\）。
# 1. 如果源文件格式为 bmp / jpg / jpeg / png / 静态 webp / 静态 avif / 静态 heic / 静态 heif，则使用 magick 压缩成 avif 格式，命令如：magick convert input.jpg -quality 50 output.avif。
# 2. 如果图片文件格式为 gif / 动态 webp / 动态 avif / 动态 heic / 动态 heif / mp4，则使用：ffmpeg -i input -map 0:v -c:v libsvtav1 -crf 32 -preset 5 temp.mp4，再 ffmpeg -i temp.mp4 -c:v copy output.avif 生成 avif 动图。
# 生成的文件放到目标文件夹中保持源文件夹的子目录结构。成功则删除源文件。

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
        if ext in {".webp", ".gif", ".avif", ".heic", ".heif"}:
            with Image.open(filepath) as img:
                return bool(getattr(img, "is_animated", False))

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


def convert_static(source: Path, dst_dir: Path) -> bool:
    """静态图 → AVIF，输出到 dst_dir，成功返回 True。"""
    output = dst_dir / f"{source.stem}.avif"
    try:
        subprocess.run(
            ["magick", str(source), "-quality", "50", str(output)],
            check=True,
            capture_output=True,
            creationflags=CREATION_FLAGS,
        )
        return output.is_file() and output.stat().st_size > 0
    except subprocess.CalledProcessError as e:
        print(f"  ❌ magick 失败：{e}")
        output.unlink(missing_ok=True)
        return False


def convert_animated(source: Path, dst_dir: Path) -> bool:
    """动态图 / 视频 → AV1 MP4 → AVIF 动图，输出到 dst_dir，成功返回 True。"""
    temp_id = uuid.uuid4().hex[:8]
    output = dst_dir / f"{source.stem}.avif"
    temp_mp4 = dst_dir / f"{source.stem}_temp_{temp_id}.mp4"
    temps: list[Path] = [temp_mp4]

    # 动态 WebP → 临时 GIF
    if source.suffix.lower() == ".webp" and is_animated(source):
        temp_gif = dst_dir / f"{source.stem}_temp_{temp_id}.gif"
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

    cleanup_temps(temps)
    return output.is_file() and output.stat().st_size > 0


def cleanup_temps(files: list[Path]) -> None:
    """删除临时文件列表。"""
    for f in files:
        f.unlink(missing_ok=True)


def main() -> None:
    """主流程：获取源/目标文件夹 → 遍历转换 → 统计。"""
    default_src = r"d:\Studios\Folders\Ins"
    default_dst = r"d:\Studios\Folders\Outs"

    raw = input(f"请输入源文件夹（回车使用默认 {default_src}）：").strip()
    src_root = Path(raw.strip("\"'")) if raw else Path(default_src)
    raw = input(f"请输入目标文件夹（回车使用默认 {default_dst}）：").strip()
    dst_root = Path(raw.strip("\"'")) if raw else Path(default_dst)

    if not src_root.is_dir():
        print(f"错误：源文件夹不存在 —— {src_root}")
        return

    dst_root.mkdir(parents=True, exist_ok=True)

    # 收集所有目标文件
    all_files = sorted(
        p for p in src_root.rglob("*")
        if p.is_file() and p.suffix.lower() in ALL_EXTS
    )
    total = len(all_files)

    if not total:
        print("未找到可处理的文件。")
        return

    print(f"\n找到 {total} 个文件，开始处理...\n")
    ok = 0
    fail = 0

    for idx, src in enumerate(all_files, 1):
        try:
            rel = src.parent.relative_to(src_root)
        except ValueError:
            rel = Path()
        dst_dir = dst_root / rel
        dst_dir.mkdir(parents=True, exist_ok=True)

        ext = src.suffix.lower()
        print(f"[{idx}/{total}] {src.relative_to(src_root)}")

        success = False
        if ext in STATIC_EXTS:
            if is_animated(src):
                success = convert_animated(src, dst_dir)
            else:
                success = convert_static(src, dst_dir)
        elif ext in ANIMATED_EXTS:
            success = convert_animated(src, dst_dir)

        if success:
            try:
                src.unlink()
            except OSError:
                pass
            ok += 1
            print(f"  ✅ 完成")
        else:
            fail += 1
            print(f"  ❌ 失败")

    print(f"\n处理完成：成功 {ok} 个，失败 {fail} 个，共 {total} 个。")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
    input("按回车键退出...")
