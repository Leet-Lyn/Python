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

import json
import shutil
import signal
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
# ============================================================
# 输出编码：强制 UTF-8，防止 GBK 控制台下 emoji/中文打印崩溃
# ============================================================
for _stream in (sys.stdout, sys.stderr):
    if _stream is not None and hasattr(_stream, "reconfigure"):
        try:
            _stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
# ============================================================
# 全局配置
# ============================================================
# 默认源文件夹
DEFAULT_SOURCE_DIR = Path(
    r"d:\Studios\Folders\Ins"
)
# 默认输出文件夹
DEFAULT_TARGET_DIR = Path(
    r"d:\Studios\Folders\Outs"
)
# 用户中断标记
_quit_requested = False
# 跳过已存在的输出文件（批量跑几天时不覆盖）
SKIP_EXISTING = True
# ============================================================
# 支持格式
# ============================================================
VIDEO_EXTS = (
    ".mkv",
    ".avi",
    ".f4v",
    ".flv",
    ".swf",
    ".ts",
    ".mpeg",
    ".mpg",
    ".rm",
    ".rmvb",
    ".asf",
    ".wmv",
    ".mov",
    ".webm",
    ".mp4",
    ".ogv",
    ".ogm",
    ".ogg",
    ".vob",
)
AUDIO_EXTS = (
    ".mp3",
    ".m4a",
    ".m4b",
    ".mka",
    ".wma",
    ".ogg",
    ".aac",
    ".ac3",
    ".rm",
    ".wav",
)
# ============================================================
# 转码预设
# ============================================================
PRESETS = {
    # --------------------------------------------------------
    # AV1 + AAC
    # --------------------------------------------------------
    "1":
    {
        "name":
        "AV1 + AAC → MKV",
        "extensions":
        VIDEO_EXTS,
        "output_ext":
        ".mkv",
        "ffmpeg":
        [
            # 保留全部 stream
            "-map",
            "0",
            # 排除 data stream
            "-map",
            "-0:d",
            # 视频
            "-c:v",
            "libsvtav1",
            "-preset",
            "5",
            "-crf",
            "32",
            # 音频
            "-c:a",
            "aac",
            "-q:a",
            "0.64",
            # 字幕
            "-c:s",
            "copy",
            "-y",
        ],
        # 转码后 mkvmerge
        "mkvmerge":
        True,
    },
    # --------------------------------------------------------
    # x264
    # --------------------------------------------------------
    "2":
    {
        "name":
        "H.264 x264 → MKV",
        "extensions":
        VIDEO_EXTS,
        "output_ext":
        ".mkv",
        "ffmpeg":
        [
            "-map",
            "0",
            "-map",
            "-0:d",
            "-c:v",
            "libx264",
            "-crf",
            "18",
            "-preset",
            "veryslow",
            "-c:a",
            "copy",
            "-c:s",
            "copy",
            "-y",
        ],
        "mkvmerge":
        True,
    },
    # --------------------------------------------------------
    # Xvid
    # --------------------------------------------------------
    "3":
    {
        "name":
        "Xvid MPEG4 → AVI",
        "extensions":
        VIDEO_EXTS,
        "output_ext":
        ".avi",
        "ffmpeg":
        [
            "-map",
            "0:v",
            "-map",
            "0:a?",
            "-c:v",
            "mpeg4",
            "-vtag",
            "xvid",
            "-qscale:v",
            "1",
            "-c:a",
            "copy",
            "-y",
        ],
        "mkvmerge":
        False,
    },
    # --------------------------------------------------------
    # OGG Vorbis
    # --------------------------------------------------------
    "4":
    {
        "name":
        "OGG Vorbis 音频",
        "extensions":
        AUDIO_EXTS,
        "output_ext":
        ".ogg",
        "ffmpeg":
        [
            "-map",
            "0:a",
            "-c:a",
            "libvorbis",
            "-q:a",
            "4",
            "-y",
        ],
        "mkvmerge":
        False,
    },
    # --------------------------------------------------------
    # AAC → .aac
    # --------------------------------------------------------
    "5":
    {
        "name":
        "AAC 音频 (.aac)",
        "extensions":
        AUDIO_EXTS,
        "output_ext":
        ".aac",
        "ffmpeg":
        [
            "-map",
            "0:a",
            "-c:a",
            "aac",
            "-q:a",
            "0.36",
            "-y",
        ],
        "mkvmerge":
        False,
    },
    # --------------------------------------------------------
    # AAC → .m4a
    # --------------------------------------------------------
    "6":
    {
        "name":
        "AAC 音频 (.m4a)",
        "extensions":
        AUDIO_EXTS,
        "output_ext":
        ".m4a",
        "ffmpeg":
        [
            "-map",
            "0:a",
            "-c:a",
            "aac",
            "-q:a",
            "0.36",
            "-y",
        ],
        "mkvmerge":
        False,
    },
    # --------------------------------------------------------
    # AAC → .m4b
    # --------------------------------------------------------
    "7":
    {
        "name":
        "AAC 音频 (.m4b)",
        "extensions":
        AUDIO_EXTS,
        "output_ext":
        ".m4b",
        "ffmpeg":
        [
            "-map",
            "0:a",
            "-c:a",
            "aac",
            "-q:a",
            "0.36",
            "-y",
        ],
        "mkvmerge":
        False,
    },
    # --------------------------------------------------------
    # AAC → .mka
    # --------------------------------------------------------
    "8":
    {
        "name":
        "AAC 音频 (.mka)",
        "extensions":
        AUDIO_EXTS,
        "output_ext":
        ".mka",
        "ffmpeg":
        [
            "-map",
            "0:a",
            "-c:a",
            "aac",
            "-q:a",
            "0.36",
            "-y",
        ],
        "mkvmerge":
        False,
    },
}
# ============================================================
# 输入文件夹
# ============================================================
def ask_folder(prompt, default):
    while True:
        value = input(
            f"{prompt}"
            f"（回车使用默认 {default}）："
        ).strip()
        folder = (
            Path(value)
            if value
            else default
        )
        if folder.exists() and folder.is_dir():
            return folder
        print(
            "文件夹不存在，请重新输入。"
        )
# ============================================================
# ffprobe
# ============================================================
def probe_streams(file_path):
    """
    获取媒体流信息
    返回:
        ffprobe JSON
    """
    cmd = [
        "ffprobe",
        "-v",
        "quiet",
        "-print_format",
        "json",
        "-show_streams",
        "-show_format",
        str(file_path),
    ]
    try:
        result = subprocess.check_output(
            cmd,
            text=True,
            encoding="utf-8",
            stderr=subprocess.DEVNULL
        )
        return json.loads(result)
    except Exception:
        return None
def get_duration(file_path):
    """
    获取媒体时长
    """
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        str(file_path),
    ]
    try:
        out = subprocess.check_output(
            cmd,
            text=True,
            encoding="utf-8",
            stderr=subprocess.DEVNULL
        )
        return float(
            out.strip()
        )
    except Exception:
        return None
# ============================================================
# 异常 FPS 检测
# ============================================================
def detect_bad_fps(probe):
    """
    检测老视频错误时间基
    例如：
        r_frame_rate=90000/1
    SVT-AV1 最大支持:
        240 fps
    返回:
        None
            正常
        "30000/1001"
            需要修复
    """
    if not probe:
        return None
    for stream in probe.get(
        "streams",
        []
    ):
        if stream.get(
            "codec_type"
        ) != "video":
            continue
        for key in (
            "avg_frame_rate",
            "r_frame_rate",
        ):
            value = stream.get(key)
            if not value:
                continue
            try:
                n, d = value.split("/")
                fps = (
                    float(n)
                    /
                    float(d)
                )
                if fps > 240:
                    return "30000/1001"
            except Exception:
                pass
    return None
# ============================================================
# Part 1 结束
# ============================================================
# ============================================================
# Part 2:
# ffmpeg 调用、进度显示、mkvmerge、单文件处理
# ============================================================
# ============================================================
# 中断处理
# ============================================================
def quit_signal(signum, frame):
    global _quit_requested
    _quit_requested = True
def init_quit_handler():
    """
    初始化 Ctrl+C
    """
    signal.signal(
        signal.SIGINT,
        quit_signal
    )
def check_quit():
    return _quit_requested
# ============================================================
# 时间转换
# ============================================================
def parse_ffmpeg_time(value):
    """
    ffmpeg:
        00:01:20.123
    转换为秒
    """
    try:
        h, m, s = value.split(":")
        return (
            int(h) * 3600
            +
            int(m) * 60
            +
            float(s)
        )
    except Exception:
        return -1
# ============================================================
# 进度条
# ============================================================
def progress_bar(
        current,
        total,
        width=40
):
    if not total:
        return ""
    ratio = min(
        current / total,
        1
    )
    done = int(
        ratio * width
    )
    return (
        "["
        +
        "█" * done
        +
        "░" * (width - done)
        +
        "] "
        +
        f"{ratio:6.2%}"
    )
# ============================================================
# ffmpeg 实时运行
# ============================================================
def run_ffmpeg_progress(
        cmd,
        duration
):
    """
    使用 ffmpeg -progress pipe:2
    Windows 下进度从 stderr 读取更稳定。
    返回:
        None
            成功
        错误文本
    """
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
        )
    except FileNotFoundError:
        return (
            "未找到 ffmpeg，请检查 PATH。"
        )
    start_time = time.time()
    last_time = 0
    while True:
        line = process.stderr.readline()
        if not line:
            if process.poll() is not None:
                break
            continue
        line = line.strip()
        # ffmpeg progress:
        if line.startswith(
            "out_time="
        ):
            value = line.split(
                "=",
                1
            )[1]
            seconds = parse_ffmpeg_time(
                value
            )
            if seconds >= 0:
                last_time = seconds
                text = (
                    "\r  🎬 转码 "
                    +
                    progress_bar(
                        seconds,
                        duration
                    )
                    +
                    f"  已运行 {time.time()-start_time:.0f}s"
                )
                print(
                    text,
                    end="",
                    flush=True
                )
        if check_quit():
            process.terminate()
            return (
                "用户中断"
            )
    process.wait()
    print()
    if process.returncode != 0:
        return (
            "ffmpeg 执行失败"
        )
    return None
# ============================================================
# mkvmerge
# ============================================================
def run_mkvmerge(
        source,
        target
):
    """
    mkvmerge 二次封装
    """
    cmd = [
        "mkvmerge",
        "--disable-track-statistics-tags",
        "-o",
        str(target),
        str(source),
    ]
    try:
        subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        return None
    except FileNotFoundError:
        return (
            "未找到 mkvmerge，请确认已安装。"
        )
    except subprocess.CalledProcessError as e:
        return e.stderr
# ============================================================
# 输出文件验证
# ============================================================
def validate_output(
        file_path,
        label="输出文件",
        require_video=True
):
    """
    使用 ffprobe 验证输出文件完整性。
    检查:
        - duration > 0
        - 至少有一个 stream
        - 视频流存在（require_video=True 时）
    返回:
        (True, None)      成功
        (False, 错误信息)  失败
    """
    probe = probe_streams(
        file_path
    )
    if not probe:
        return (
            False,
            "ffprobe 无法读取文件"
        )
    # 检查 streams
    streams = probe.get(
        "streams",
        []
    )
    if not streams:
        return (
            False,
            "ffprobe 报告无流"
        )
    # 检查 duration
    fmt = probe.get(
        "format",
        {}
    )
    dur_str = fmt.get(
        "duration"
    )
    if dur_str is None:
        return (
            False,
            "ffprobe 未返回时长"
        )
    try:
        dur = float(dur_str)
    except (ValueError, TypeError):
        return (
            False,
            f"无效的时长值: {dur_str}"
        )
    if dur <= 0:
        return (
            False,
            f"时长为 0: {dur_str}"
        )
    # 统计流类型
    stream_types = {}
    has_video = False
    for s in streams:
        ct = s.get(
            "codec_type",
            "unknown"
        )
        stream_types[ct] = (
            stream_types.get(ct, 0)
            + 1
        )
        if ct == "video":
            has_video = True
    type_summary = (
        ", ".join(
            f"{k}:{v}"
            for k, v
            in stream_types.items()
        )
    )
    # 视频流检查
    if require_video and not has_video:
        return (
            False,
            "输出文件没有视频流"
        )
    print(
        f"  🔍 {label}: "
        f"时长={dur:.1f}s, "
        f"流({type_summary}) → 验证通过"
    )
    return (True, None)
# ============================================================
# 单文件处理
# ============================================================
def process_file(
        source,
        target_base,
        relative_dir,
        preset,
        index,
        total
):
    """
    处理单个文件。

    三层验证流程:
        ffmpeg → ffprobe temp → mkvmerge → ffprobe final → 删除源文件
    任一步失败即保留源文件。
    """
    target_dir = (
        target_base
        /
        relative_dir
    )
    target_dir.mkdir(
        parents=True,
        exist_ok=True
    )
    output_file = (
        target_dir
        /
        f"{source.stem}{preset['output_ext']}"
    )
    temp_file = (
        target_dir
        /
        f"{source.stem}_temp{preset['output_ext']}"
    )
    print(
        f"\n[{index}/{total}] "
        f"{datetime.now().strftime('%H:%M:%S')} | "
        f"{relative_dir / source.name}"
    )
    duration = get_duration(
        source
    )
    if duration:
        print(
            f"  时长: {duration:.1f}s"
        )
    # --------------------------------------------------------
    # 跳过已存在文件
    # --------------------------------------------------------
    if SKIP_EXISTING and output_file.exists():
        print(
            "  ⏭ 输出文件已存在，跳过"
        )
        return True
    # --------------------------------------------------------
    # ffprobe 源文件
    # --------------------------------------------------------
    probe = probe_streams(
        source
    )
    # --------------------------------------------------------
    # 判断是否纯音频预设（跳过视频流检查）
    # --------------------------------------------------------
    is_audio = (
        preset["extensions"] == AUDIO_EXTS
    )
    # --------------------------------------------------------
    # ffmpeg 参数
    # --------------------------------------------------------
    ffmpeg_args = list(
        preset["ffmpeg"]
    )
    # --------------------------------------------------------
    # 异常 FPS 修复
    # --------------------------------------------------------
    fix_fps = detect_bad_fps(
        probe
    )
    if fix_fps:
        print(
            "  ⚠ 检测到异常帧率，修正:"
            f" {fix_fps}"
        )
        # 输出端修复
        ffmpeg_args.extend(
            [
                "-r",
                fix_fps
            ]
        )
    # ====================================================
    # 第 1 层：ffmpeg 转码
    # ====================================================
    cmd = [
        "ffmpeg",
        "-stats_period",
        "1",
        "-progress",
        "pipe:2",
        "-loglevel",
        "error",
        "-i",
        str(source),
    ]
    cmd.extend(
        ffmpeg_args
    )
    cmd.append(
        str(temp_file)
    )
    print(
        subprocess.list2cmdline(cmd)
    )
    error = run_ffmpeg_progress(
        cmd,
        duration
    )
    if error:
        print(
            f"  ❌ ffmpeg 失败: {error}"
        )
        temp_file.unlink(
            missing_ok=True
        )
        return False
    # ====================================================
    # 第 2 层：ffprobe 验证临时文件
    # ====================================================
    ok, err = validate_output(
        temp_file,
        "temp",
        require_video=not is_audio
    )
    if not ok:
        print(
            f"  ❌ temp 验证失败: {err}"
        )
        temp_file.unlink(
            missing_ok=True
        )
        return False
    # ====================================================
    # 第 3 层：mkvmerge（如需要）
    # ====================================================
    if preset["mkvmerge"]:
        print(
            "  📦 mkvmerge 重封装..."
        )
        error = run_mkvmerge(
            temp_file,
            output_file
        )
        if error:
            print(
                f"  ❌ mkvmerge 失败: {error}"
            )
            temp_file.unlink(
                missing_ok=True
            )
            return False
        temp_file.unlink(
            missing_ok=True
        )
        # ================================================
        # 第 4 层：ffprobe 验证最终文件
        # ================================================
        ok, err = validate_output(
            output_file,
            "final",
            require_video=not is_audio
        )
        if not ok:
            print(
                f"  ❌ final 验证失败: {err}"
            )
            # mkvmerge 失败但 ffmpeg 成功，保留 temp 也无意义
            return False
    else:
        # 无需 mkvmerge，temp 重命名为 final
        if output_file.exists():
            output_file.unlink()
        shutil.move(
            str(temp_file),
            str(output_file)
        )
        # ================================================
        # 第 4 层：ffprobe 验证最终文件
        # ================================================
        ok, err = validate_output(
            output_file,
            "final",
            require_video=not is_audio
        )
        if not ok:
            print(
                f"  ❌ final 验证失败: {err}"
            )
            return False
    # ====================================================
    # 全部验证通过 → 删除源文件
    # ====================================================
    try:
        # Windows 文件句柄释放有延迟
        time.sleep(1)
        source.unlink()
        print(
            f"  ✅ 完成 → {output_file}"
        )
        return True
    except OSError as e:
        print(
            "  ⚠ 输出成功但无法删除源文件:"
            f" {source.name} — {e}"
        )
        return True  # 输出成功，仍算通过
# ============================================================
# Part 2 结束
# ============================================================
# ============================================================
# Part 3:
# 主程序、扫描、运行入口
# ============================================================
# ============================================================
# 主程序
# ============================================================
def main():
    print(
        "=" * 60
    )
    print(
        "FFmpeg 批量转码工具"
    )
    print(
        "=" * 60
    )
    # --------------------------------------------------------
    # 选择模式
    # --------------------------------------------------------
    print()
    print(
        "请选择转码模式:"
    )
    for key, value in PRESETS.items():
        print(
            f"{key}. {value['name']}"
        )
    choice = input(
        "\n请输入编号（默认 1）: "
    ).strip()
    if choice not in PRESETS:
        choice = "1"
    preset = PRESETS[choice]
    print()
    print(
        "当前模式:"
        ,
        preset["name"]
    )
    # --------------------------------------------------------
    # 输入目录
    # --------------------------------------------------------
    source_folder = ask_folder(
        "请输入源文件夹",
        DEFAULT_SOURCE_DIR
    )
    target_folder = ask_folder(
        "请输入目标文件夹",
        DEFAULT_TARGET_DIR
    )
    print()
    print(
        "源目录:"
        ,
        source_folder
    )
    print(
        "目标目录:"
        ,
        target_folder
    )
    # --------------------------------------------------------
    # 扫描文件
    # --------------------------------------------------------
    files = []
    print()
    print(
        "正在扫描文件..."
    )
    for file in source_folder.rglob("*"):
        if not file.is_file():
            continue
        if (
            file.suffix.lower()
            in
            preset["extensions"]
        ):
            relative = file.parent.relative_to(
                source_folder
            )
            files.append(
                (
                    file,
                    relative
                )
            )
    if not files:
        print(
            "没有找到符合条件的文件。"
        )
        return
    print(
        f"找到 {len(files)} 个文件。"
    )
    # --------------------------------------------------------
    # 创建目标目录
    # --------------------------------------------------------
    target_folder.mkdir(
        parents=True,
        exist_ok=True
    )
    # --------------------------------------------------------
    # 初始化 Ctrl+C
    # --------------------------------------------------------
    init_quit_handler()
    success = 0
    failed = 0
    start_time = time.time()
    # --------------------------------------------------------
    # 执行
    # --------------------------------------------------------
    try:
        for index, item in enumerate(
            files,
            1
        ):
            if check_quit():
                print(
                    "\n用户中断。"
                )
                break
            file, relative = item
            result = process_file(
                file,
                target_folder,
                relative,
                preset,
                index,
                len(files)
            )
            if result:
                success += 1
            else:
                failed += 1
    except KeyboardInterrupt:
        print(
            "\n用户中断。"
        )
    # --------------------------------------------------------
    # 统计
    # --------------------------------------------------------
    elapsed = time.time() - start_time
    print()
    print(
        "=" * 60
    )
    print(
        "处理完成"
    )
    print(
        f"成功: {success}"
    )
    print(
        f"失败: {failed}"
    )
    print(
        f"总计: {len(files)}"
    )
    print(
        f"耗时: {elapsed/3600:.2f} 小时"
    )
    print(
        "=" * 60
    )
# ============================================================
# 程序入口
# ============================================================
if __name__ == "__main__":
    try:
        # Windows 中文输出
        if hasattr(
            sys.stdout,
            "reconfigure"
        ):
            sys.stdout.reconfigure(
                encoding="utf-8",
                errors="replace"
            )
        main()
    except Exception as e:
        print()
        print(
            "程序发生错误:"
        )
        print(e)
    finally:
        input(
            "\n按回车键退出..."
        )
# ============================================================
# 完成
# ============================================================