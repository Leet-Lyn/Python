# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件夹位置（默认"d:\Studios\Folders\Ins\"）与目标文件夹位置（默认"d:\Studios\Folders\Outs\"）。
# 遍历源文件夹及其子文件夹位置中所有视频文件（mkv、avi、f4v、flv、ts、mpeg、mpg、rm、rmvb、asf、wmv、mov、webm、mp4、ogv、ogm、ogg、vob）。
# 使用 ffmpeg 压缩，类似命令：
# 1. ffmpeg -i input.mkv -map 0 -c:v libsvtav1 -crf 32 -preset 5 -c:a aac -q:a 0.64 -c:s copy output.mkv。视频参数为：av1 格式，Const.Qualty: Quality=32，Preset=5。音频参数为：aac 格式，遍历每个音轨，质量模式。q=0.64。字幕保持不变。
# 2. ffmpeg -i input.mkv -c:v libx264 -crf 18 -preset veryslow -c:a copy output.mkv。
# 视频参数为：x264 格式，crf 18 -preset veryslow。音频、字幕保持不变。
# 3. ffmpeg -i input.mkv -c:v mpeg4 -vtag xvid -qscale:v 1 -c:a copy output.mkv。
# 视频参数为：xvid 格式，qscale:v 1。音频、字幕保持不变。
# 4. ffmpeg -i input.mp3 -c:a aac -q:a 0.36 -map 0:a -y output。音频参数为：aac 格式，遍历每个音轨，质量模式。q=0.36。
# 5. ffmpeg -i input -c:a libvorbis -q:a 4 -map 0:a -y output。音频参数为：ogg 格式，遍历每个音轨，质量模式。q=4。
# 生成的文件重新用 mkvmerge 再生成同名文件到目标文件夹位置，文件夹结构保持一致。

import shutil
import signal
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

# ============================================================
# 全局配置
# ============================================================

DEFAULT_SOURCE_DIR = Path(r"d:\Studios\Folders\Ins")
DEFAULT_TARGET_DIR = Path(r"d:\Studios\Folders\Outs")

# 中断标志：Ctrl+Q（Windows msvcrt）或 Ctrl+\（Unix SIGQUIT）设置
_quit_requested = False

VIDEO_EXTS = (
    ".mkv", ".avi", ".f4v", ".flv", ".ts", ".mpeg", ".mpg",
    ".rm", ".rmvb", ".asf", ".wmv", ".mov", ".webm", ".mp4",
    ".ogv", ".ogm", ".ogg", ".vob",
)
AUDIO_EXTS = (".mp3", ".m4a", ".wma", ".ogg", ".aac", ".ac3", ".rm", ".wav")

# --- 消息常量 ---
MSG_INTERRUPTED = "\n\n用户中断程序，已退出。"
MSG_ERROR = "\n程序运行出错: {}"
MSG_EXIT = "\n按回车键退出..."
MSG_ASK_FOLDER_SUFFIX = "（回车使用默认 {default}）："
MSG_FOLDER_NOT_EXIST = "文件夹不存在，请重新输入。"
MSG_TOOL_NOT_FOUND = "未找到 {description}，请确认已安装并添加到 PATH。"
MSG_QUIT_HINT = "提示：转码中可按 Ctrl+Q 中断。\n"
MSG_TOOL_TITLE = "FFmpeg 批量转码工具"
MSG_PRESET_LIST = "可选预设："
MSG_SELECT_PRESET = "请选择预设（默认 1 — AV1）："
MSG_INVALID_PRESET = "无效选择：{choice}，使用默认预设 AV1。"
MSG_CURRENT_PRESET = "\n当前预设：{name}\n"
MSG_ASK_SOURCE_DIR = "请输入源文件夹位置"
MSG_ASK_TARGET_DIR = "请输入目标文件夹位置"
MSG_NO_MATCH = "未找到匹配的文件。"
MSG_FOUND_FILES = "找到 {total} 个文件，开始转码…"
MSG_USER_INTERRUPT = "\n⚠ 用户中断（Ctrl+Q），已处理部分不会丢失。"
MSG_USER_INTERRUPT_KI = "\n⚠ 用户中断，已处理部分不会丢失。"
MSG_COMPLETE = "\n处理完成：成功 {ok} 个，失败 {fail} 个，共 {total} 个。"
MSG_DURATION = "  时长: {:.1f}s"
MSG_FFMPEG_FAILED = "\n  ❌ ffmpeg 失败：{}\n      {}"
MSG_REMUXING = "  📦 重封装中…"
MSG_MKVMERGE_FAILED = "  ❌ mkvmerge 失败：{}\n      {}"
MSG_DONE_OUTPUT = "  ✅ 完成 → {}"
MSG_OUTPUT_OK_CANT_DELETE = "  ⚠ 输出成功但无法删除源文件：{}\n      {}"
MSG_OUTPUT_ABNORMAL = "  ⚠ 输出文件异常（缺失或为空），保留源文件：{}"
MSG_FFMPEG_NOT_FOUND = "未找到 ffmpeg，请确认已安装并添加到 PATH。"
MSG_USER_INTERRUPT_FFMPEG = "用户中断（Ctrl+Q）"
MSG_TRANSCODING_PROGRESS = "  🎬 转码 {}  已耗时 {:.0f}s"

# ============================================================
# 预设定义
# ============================================================
# 每个预设包含：
#   name:       显示名称
#   extensions: 要扫描的扩展名元组
#   output_ext: 输出文件扩展名
#   ffmpeg:     转码参数（不含 -i input 和 output）
#   mkvmerge:   True = ffmpeg 后用 mkvmerge 再封装；False = 直接输出最终文件

PRESETS = {
    "1": {
        "name": "AV1 + AAC → MKV（视频）",
        "extensions": VIDEO_EXTS,
        "output_ext": ".mkv",
        # ffmpeg -i input -c:v libsvtav1 -preset 5 -crf 32 -c:a aac -q:a 0.64 -c:s copy -map 0 -y output
        "ffmpeg": ["-c:v", "libsvtav1", "-preset", "5", "-crf", "32",
                    "-c:a", "aac", "-q:a", "0.64",
                    "-c:s", "copy", "-map", "0", "-y"],
        "mkvmerge": True,
    },
    "2": {
        "name": "x264 → MP4（视频）",
        "extensions": VIDEO_EXTS,
        "output_ext": ".mp4",
        # ffmpeg -i input -c:v libx264 -preset veryslow -crf 18 -c:a copy -c:s copy -map 0 -y output
        "ffmpeg": ["-c:v", "libx264", "-preset", "veryslow", "-crf", "18",
                    "-c:a", "copy",
                    "-c:s", "copy", "-map", "0", "-y"],
        "mkvmerge": False,
    },
    "3": {
        "name": "Xvid → AVI（视频）",
        "extensions": VIDEO_EXTS,
        "output_ext": ".avi",
        # ffmpeg -i input -c:v mpeg4 -vtag xvid -qscale:v 1 -c:a copy -c:s copy -map 0 -y output
        "ffmpeg": ["-c:v", "mpeg4", "-vtag", "xvid", "-qscale:v", "1",
                    "-c:a", "copy",
                    "-c:s", "copy", "-map", "0", "-y"],
        "mkvmerge": False,
    },
    "4": {
        "name": "AAC（音频）",
        "extensions": AUDIO_EXTS,
        "output_ext": ".aac",
        # ffmpeg -i input -c:a aac -q:a 0.36 -map 0:a -y output
        "ffmpeg": ["-c:a", "aac", "-q:a", "0.36",
                    "-map", "0:a", "-y"],
        "mkvmerge": False,
    },
    "5": {
        "name": "OGG（音频）",
        "extensions": AUDIO_EXTS,
        "output_ext": ".ogg",
        # ffmpeg -i input -c:a libvorbis -q:a 4 -map 0:a -y output
        "ffmpeg": ["-c:a", "libvorbis", "-q:a", "4",
                    "-map", "0:a", "-y"],
        "mkvmerge": False,
    },
}

# ============================================================
# 辅助函数
# ============================================================


def ask_folder(prompt: str, default: Path) -> Path:
    """询问文件夹路径，回车使用默认值；输入无效则循环重试。"""
    while True:
        raw = input(f"{prompt}{MSG_ASK_FOLDER_SUFFIX.format(default=default)}").strip()
        folder = Path(raw) if raw else default
        if folder.is_dir():
            return folder
        print(MSG_FOLDER_NOT_EXIST)


def get_duration(file_path: Path) -> float | None:
    """使用 ffprobe 获取媒体文件时长（秒），失败返回 None。"""
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(file_path),
    ]
    try:
        output = subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL).strip()
        return float(output)
    except Exception:
        return None


def parse_ffmpeg_time(time_str: str) -> float:
    """解析 ffmpeg 时间字符串（HH:MM:SS.microseconds）为秒数。"""
    try:
        parts = time_str.strip().split(":")
        if len(parts) == 3:
            h, m, s = parts
            return int(h) * 3600 + int(m) * 60 + float(s)
    except (ValueError, AttributeError):
        pass
    return -1.0


def format_progress_bar(current: float, total: float, width: int = 36) -> str:
    """生成文本进度条：[████░░░░] 百分比。"""
    if total <= 0:
        return " " * (width + 10)
    pct = min(current / total, 1.0)
    filled = int(width * pct)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}] {pct:5.1%}"


def run_tool(cmd: list[str], description: str) -> str | None:
    """
    运行外部工具，抑制正常输出；失败时返回 stderr 内容供打印。
    """
    try:
        subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
        )
        return None  # 成功，无错误信息
    except FileNotFoundError:
        return MSG_TOOL_NOT_FOUND.format(description=description)
    except subprocess.CalledProcessError as e:
        return e.stderr.strip() or str(e)


def print_progress(msg: str) -> None:
    """输出进度信息（\r 覆盖当前行），末尾不带换行。"""
    # 先清空行尾残留字符
    print(f"\r{msg}", end="", flush=True)


# ============================================================
# Ctrl+Q / Ctrl+\ 中断支持
# ============================================================

def _on_quit_signal(signum, frame):
    """Unix SIGQUIT 信号处理器（Ctrl+\）。"""
    global _quit_requested
    _quit_requested = True


def init_quit_handler() -> None:
    """注册中断处理：Windows 用 msvcrt，Unix 用 SIGQUIT（Ctrl+\）。"""
    # Unix：注册 SIGQUIT 处理器（Ctrl+\）
    if hasattr(signal, "SIGQUIT"):
        signal.signal(signal.SIGQUIT, _on_quit_signal)
    # Windows：提示可用快捷键
    if sys.platform == "win32":
        print(MSG_QUIT_HINT)


def check_quit_key() -> bool:
    """
    非阻塞检测中断快捷键。
    Windows：检测 Ctrl+Q（msvcrt kbhit）。
    Unix：返回 _quit_requested 标志（由 SIGQUIT 设置）。
    """
    global _quit_requested
    if sys.platform == "win32":
        try:
            import msvcrt
            while msvcrt.kbhit():
                ch = msvcrt.getch()
                if ch == b"\x11":   # Ctrl+Q = ASCII 17
                    _quit_requested = True
        except Exception:
            pass
    return _quit_requested


# ============================================================
# 处理函数
# ============================================================


def process_file(
    source: Path,
    target_base: Path,
    relative_dir: Path,
    preset: dict,
    file_index: int,
    total_files: int,
) -> bool:
    """
    转码单个文件（带实时进度条）。成功删除源文件返回 True，失败返回 False。
    """
    stem = source.stem
    ext = preset["output_ext"]

    # 目标子目录，保持源文件夹结构
    target_dir = target_base / relative_dir
    target_dir.mkdir(parents=True, exist_ok=True)

    temp_output = target_dir / f"{stem}_temp{ext}"
    final_output = target_dir / f"{stem}{ext}"

    # 获取时长（供进度条计算百分比）
    duration = get_duration(source)

    # 打印文件头部信息
    now_str = datetime.now().strftime("%H:%M:%S")
    print(f"\n[{file_index}/{total_files}] {now_str} | {relative_dir / source.name}")
    if duration:
        print(MSG_DURATION.format(duration))

    # --- 步骤 1：ffmpeg 转码（带实时进度） ---
    ffmpeg_cmd = [
        "ffmpeg",
        "-progress", "pipe:1",     # 结构化进度写入 stdout
        "-loglevel", "error",       # 只输出错误到 stderr
        "-i", str(source),
        *preset["ffmpeg"],
        str(temp_output),
    ]

    err_msg = run_ffmpeg_with_progress(ffmpeg_cmd, duration)
    if err_msg:
        print(MSG_FFMPEG_FAILED.format(source.name, err_msg))
        if "Ctrl+Q" not in err_msg:
            temp_output.unlink(missing_ok=True)  # 非用户中断才清理临时文件
        return False
    # 进度条完成后换行
    print()

    # --- 步骤 2（可选）：mkvmerge 重封装 ---
    if preset["mkvmerge"]:
        print(MSG_REMUXING)
        mkvmerge_cmd = ["mkvmerge", "-o", str(final_output), str(temp_output)]

        err = run_tool(mkvmerge_cmd, "mkvmerge")
        if err:
            print(MSG_MKVMERGE_FAILED.format(temp_output, err))
            temp_output.unlink(missing_ok=True)
            return False

        temp_output.unlink(missing_ok=True)  # 删除临时文件
    else:
        # 无需 mkvmerge，临时文件即为最终文件
        if final_output.exists():
            final_output.unlink()
        shutil.move(str(temp_output), str(final_output))

    # --- 步骤 3：验证 & 清理 ---
    if final_output.is_file() and final_output.stat().st_size > 0:
        try:
            source.unlink()
            print(MSG_DONE_OUTPUT.format(final_output))
            return True
        except OSError as e:
            print(MSG_OUTPUT_OK_CANT_DELETE.format(source, e))
            return True  # 输出成功，算通过
    else:
        print(MSG_OUTPUT_ABNORMAL.format(source))
        return False


def run_ffmpeg_with_progress(cmd: list[str], duration: float | None) -> str | None:
    """
    运行 ffmpeg 并解析 -progress pipe:1 输出，实时显示进度条。
    返回 None 表示成功，否则返回错误信息字符串。
    """
    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except FileNotFoundError:
        return MSG_FFMPEG_NOT_FOUND

    # 逐行读取 ffmpeg 进度输出
    start_time = time.time()
    last_update = 0.0
    for line in proc.stdout:
        if line.startswith("out_time="):
            time_str = line.split("=", 1)[1].strip()
            seconds = parse_ffmpeg_time(time_str)
            if seconds >= 0 and duration and duration > 0:
                # 限制刷新频率：最多每秒更新 5 次
                now = time.time()
                if now - last_update >= 0.2:
                    bar = format_progress_bar(seconds, duration)
                    elapsed = now - start_time
                    print_progress(MSG_TRANSCODING_PROGRESS.format(bar, elapsed))
                    last_update = now
                    # 检测 Ctrl+Q 中断
                    if check_quit_key():
                        proc.terminate()
                        return MSG_USER_INTERRUPT_FFMPEG

    # 等待进程结束并读取 stderr
    proc.wait()
    if proc.returncode != 0:
        stderr_output = proc.stderr.read().strip()
        return stderr_output or f"ffmpeg 返回码 {proc.returncode}"

    # 最终显示 100%
    if duration and duration > 0:
        elapsed = time.time() - start_time
        print_progress(f"  🎬 转码 {format_progress_bar(duration, duration)}  已耗时 {elapsed:.0f}s")

    return None


# ============================================================
# 主流程
# ============================================================


def main() -> None:
    print("=" * 50)
    print(MSG_TOOL_TITLE)
    print("=" * 50)
    print("\n" + MSG_PRESET_LIST)
    # 视频预设在前，音频在后
    for key in ("1", "2", "3", "4", "5"):
        print(f"  {key}. {PRESETS[key]['name']}")
    print()

    choice = input(MSG_SELECT_PRESET).strip() or "1"
    preset = PRESETS.get(choice)
    if preset is None:
        print(MSG_INVALID_PRESET.format(choice=choice))
        preset = PRESETS["1"]

    print(MSG_CURRENT_PRESET.format(name=preset['name']))

    source_folder = ask_folder(MSG_ASK_SOURCE_DIR, DEFAULT_SOURCE_DIR)
    target_folder = ask_folder(MSG_ASK_TARGET_DIR, DEFAULT_TARGET_DIR)

    target_folder.mkdir(parents=True, exist_ok=True)
    exts = preset["extensions"]

    # 预先收集所有匹配文件（用于全局进度计数）
    all_files: list[tuple[Path, Path]] = []
    for src_path in source_folder.rglob("*"):
        if not src_path.is_file():
            continue
        if src_path.suffix.lower() not in exts:
            continue
        relative_dir = src_path.parent.relative_to(source_folder)
        all_files.append((src_path, relative_dir))

    total = len(all_files)
    if total == 0:
        print(MSG_NO_MATCH)
        return

    print(MSG_FOUND_FILES.format(total=total))
    init_quit_handler()

    ok = 0
    fail = 0

    try:
        for idx, (src_path, relative_dir) in enumerate(all_files, 1):
            # 检查中断标志
            if check_quit_key():
                print(MSG_USER_INTERRUPT)
                break

            if process_file(src_path, target_folder, relative_dir, preset, idx, total):
                ok += 1
            else:
                fail += 1
    except KeyboardInterrupt:
        print(MSG_USER_INTERRUPT_KI)

    print(MSG_COMPLETE.format(ok=ok, fail=fail, total=total))


# ============================================================
# 入口
# ============================================================

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