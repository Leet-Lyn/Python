# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件夹位置与目标文件夹位置（默认均为"d:\Studios\Folders\Outs\"）。
# 遍历源文件夹位置中所有视频文件（mkv、avi、f4v、flv、ts、mpeg、mpg、rm、rmvb、asf、wmv、mov、webm、mp4）。
# 使用 ffmpeg 压缩，类似命令：ffmpeg -i input.mp4 -ss 00:00:01 -vframes 1 output.jpg。
# 分别截取第 1 秒、第 10 秒以及一半时间的视频的图片，后缀名为-s01.jpg、-s10.jpg、-ss.jpg。

import shutil
import subprocess
import sys
from pathlib import Path

# ==================== 全局配置 ====================

DEFAULT_SOURCE_DIR = Path(r"d:\Works\Out")
DEFAULT_TARGET_DIR = Path(r"d:\Works\Out")

VIDEO_EXTENSIONS = {".mkv", ".avi", ".f4v", ".flv", ".ts", ".mpeg", ".mpg",
                    ".rm", ".rmvb", ".asf", ".wmv", ".mov", ".webm", ".mp4"}

# ==================== 辅助函数 ====================


def get_input_with_default(prompt_text: str, default_value: str) -> str:
    """获取带默认值的用户输入。"""
    user_input = input(f"{prompt_text} (默认: {default_value}): ").strip()
    return user_input if user_input else str(default_value)


def is_video_file(file_path: Path) -> bool:
    """检查文件是否为支持的视频格式（大小写不敏感）。"""
    return file_path.suffix.lower() in VIDEO_EXTENSIONS


def get_video_duration(video_path: Path) -> float | None:
    """
    使用 ffprobe 获取视频时长（秒），失败返回 None。
    ffprobe -show_entries format=duration 输出为单行浮点数（如 "123.456"）。
    """
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(video_path),
    ]
    try:
        output = subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL).strip()
        return float(output)
    except Exception as e:
        print(f"    获取视频时长失败：{video_path.name}，{e}")
        return None


def extract_thumbnails(video_path: Path, output_dir: Path) -> int:
    """
    使用 ffmpeg 从视频中截取第 1 秒、第 10 秒及视频中间位置的图片。
    返回成功截取的图片数量。

    -ss 放在 -i 前面使用 keyframe seeking，速度远优于放在 -i 之后。
    -y 自动覆盖已存在的输出文件，避免交互式卡死。
    自动跳过超出视频时长的截图时间点（如短视频 < 10s 则跳过 10s 截图）。
    """
    video_name = video_path.stem

    duration = get_video_duration(video_path)
    if duration is None or duration <= 0:
        return 0

    # 截图时间点：(秒数, 后缀标签)
    timestamps: list[tuple[float, str]] = [
        (1.0, "-s01"),
        (10.0, "-s10"),
        (duration / 2, "-ss"),
    ]

    success_count = 0
    for timestamp, suffix in timestamps:
        # 跳过超出视频时长的时间点
        if timestamp >= duration:
            print(f"    跳过 {video_name}{suffix}.jpg（{timestamp:.1f}s >= 时长 {duration:.1f}s）")
            continue

        output_file = output_dir / f"{video_name}{suffix}.jpg"
        cmd = [
            "ffmpeg",
            "-ss", f"{timestamp:.2f}",   # 放在 -i 前面：快速 keyframe seeking
            "-i", str(video_path),
            "-vframes", "1",
            "-y",                         # 自动覆盖已存在文件
            str(output_file),
        ]
        try:
            subprocess.run(cmd, check=True,
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
            print(f"    截图成功：{output_file.name}")
            success_count += 1
        except subprocess.CalledProcessError as e:
            print(f"    截图失败：{output_file.name}，{e}")

    return success_count


# ==================== 主程序 ====================


def main() -> None:
    """主程序入口：获取用户输入的文件夹，遍历文件并处理。"""

    # 检查 ffmpeg 是否可用
    if shutil.which("ffmpeg") is None:
        print("错误：找不到 ffmpeg，请安装后重试。")
        return

    # 获取源文件夹和目标文件夹路径
    source_str = get_input_with_default("请输入源文件夹路径：", str(DEFAULT_SOURCE_DIR))
    target_str = get_input_with_default("请输入目标文件夹路径：", str(DEFAULT_TARGET_DIR))

    source_root = Path(source_str)
    target_root = Path(target_str)

    if not source_root.is_dir():
        print(f"错误：源文件夹不存在 —— {source_root}")
        return

    # 确保目标文件夹存在
    target_root.mkdir(parents=True, exist_ok=True)

    # 收集所有视频文件
    video_files = [p for p in source_root.rglob("*") if p.is_file() and is_video_file(p)]

    if not video_files:
        print("未找到任何视频文件。")
        return

    print(f"\n找到 {len(video_files)} 个视频文件，开始处理…\n")

    total_screenshots = 0
    for idx, video_path in enumerate(video_files, 1):
        # 保持源文件夹的相对目录结构
        relative_dir = video_path.parent.relative_to(source_root)
        output_dir = target_root / relative_dir
        output_dir.mkdir(parents=True, exist_ok=True)

        print(f"[{idx}/{len(video_files)}] {video_path.relative_to(source_root)}")
        count = extract_thumbnails(video_path, output_dir)
        total_screenshots += count

    print(f"\n所有视频处理完成！共处理 {len(video_files)} 个视频，成功截图 {total_screenshots} 张。")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n用户中断程序，已退出。")
    except Exception as e:
        print(f"\n程序运行出错: {e}")
    finally:
        input("\n按回车键退出...")
