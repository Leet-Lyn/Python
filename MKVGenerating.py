# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件夹位置（默认 d:\Studios\Folders\Ins\）与目标文件夹位置（默认 d:\Studios\Folders\Outs\）。
# 遍历源文件夹内所有子文件夹中的视频文件，使用 mkvmerge.exe 转换成 mkv 格式。
# 生成的文件放到目标文件夹中保持子目录结构。

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

VIDEO_EXTS = {
    ".mkv", ".avi", ".f4v", ".flv", ".ts", ".mpeg", ".mpg",
    ".rm", ".rmvb", ".asf", ".wmv", ".mov", ".webm", ".mp4",
    ".ogv", ".ogm", ".ogg",
}

MKVMERGE_CANDIDATES = [
    Path(r"D:\ProApps\MKVToolNix\mkvmerge.exe"),
    Path(r"C:\Program Files\MKVToolNix\mkvmerge.exe"),
]

# 中断标志：Ctrl+Q（Windows msvcrt）或 Ctrl+\（Unix SIGQUIT）设置
_quit_requested = False

# ============================================================
# 辅助函数
# ============================================================


def get_input_with_default(prompt_text: str, default_value: str) -> str:
    """获取带默认值的用户输入。"""
    user_input = input(f"{prompt_text} (默认: {default_value}): ").strip()
    return user_input if user_input else str(default_value)


def find_mkvmerge() -> Path | None:
    """查找 mkvmerge.exe，按候选路径 → PATH 顺序查找。"""
    for path in MKVMERGE_CANDIDATES:
        if path.is_file():
            return path
    # 尝试 PATH 中的 mkvmerge
    which = shutil.which("mkvmerge") or shutil.which("mkvmerge.exe")
    if which:
        return Path(which)
    # 最后尝试候选路径（可能通过 PATH 补全）
    for path in MKVMERGE_CANDIDATES:
        try:
            result = subprocess.run(
                [str(path), "--version"],
                capture_output=True,
                encoding="utf-8",
                errors="ignore",
            )
            if result.returncode == 0:
                return path
        except Exception:
            continue
    return None


def format_progress_bar(pct: float, width: int = 36) -> str:
    """生成文本进度条：[████░░░░] 百分比。"""
    if pct < 0:
        return " " * (width + 10)
    pct = min(pct / 100.0, 1.0)
    filled = int(width * pct)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}] {pct:5.1%}"


def print_progress(msg: str) -> None:
    """输出进度信息（\r 覆盖当前行），末尾不带换行。"""
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
    if hasattr(signal, "SIGQUIT"):
        signal.signal(signal.SIGQUIT, _on_quit_signal)
    if sys.platform == "win32":
        print("提示：封装中可按 Ctrl+Q 中断。\n")


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


def convert_video(
    source: Path,
    target: Path,
    mkvmerge: Path,
    file_index: int,
    total_files: int,
) -> bool:
    """
    使用 mkvmerge 转换单个视频文件（带实时进度条）。
    成功删除源文件返回 True，失败返回 False。
    """
    # 打印文件头部信息
    now_str = datetime.now().strftime("%H:%M:%S")
    print(f"\n[{file_index}/{total_files}] {now_str} | {source}")
    print(f"  📦 封装中…")

    cmd = [str(mkvmerge), "-o", str(target), str(source)]

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
        print(f"  ❌ 未找到 mkvmerge：{mkvmerge}")
        return False

    # 逐行读取 mkvmerge 进度输出（stdout: "Progress: XX%"）
    last_pct = -1.0
    for line in proc.stdout:
        if line.startswith("Progress:"):
            try:
                pct_str = line.split(":", 1)[1].strip().rstrip("%")
                pct = float(pct_str)
            except ValueError:
                continue

            # 限制刷新频率
            if abs(pct - last_pct) >= 1.0:
                bar = format_progress_bar(pct)
                print_progress(f"  📦 封装 {bar}")
                last_pct = pct

            # 检测 Ctrl+Q 中断
            if check_quit_key():
                proc.terminate()
                print(f"\n  ⚠ 用户中断（Ctrl+Q），保留源文件及不完整输出。")
                return False

    proc.wait()
    # 进度条完成后换行
    if last_pct >= 0:
        print()

    if proc.returncode != 0:
        stderr_output = proc.stderr.read().strip()
        print(f"  ❌ 封装失败：{source.name}")
        if stderr_output:
            print(f"      {stderr_output}")
        return False

    # 验证输出
    if target.is_file() and target.stat().st_size > 0:
        try:
            source.unlink()
            print(f"  ✅ 完成 → {target}")
        except OSError as e:
            print(f"  ⚠ 输出成功但无法删除源文件：{e}")
        return True
    else:
        print(f"  ⚠ 输出文件异常（缺失或为空），保留源文件：{source}")
        return False


# ============================================================
# 主流程
# ============================================================


def main() -> None:
    """主流程：获取源/目标文件夹 → 遍历视频 → mkvmerge 转换 → 统计。"""

    source_str = get_input_with_default(
        "请输入源文件夹位置：", str(DEFAULT_SOURCE_DIR))
    target_str = get_input_with_default(
        "请输入目标文件夹位置：", str(DEFAULT_TARGET_DIR))

    src_root = Path(source_str)
    dst_root = Path(target_str)

    if not src_root.is_dir():
        print(f"错误：源文件夹不存在 —— {src_root}")
        return

    mkvmerge = find_mkvmerge()
    if mkvmerge is None:
        print("错误：未找到 mkvmerge.exe")
        print("请确保已安装 MKVToolNix 或提供正确的路径")
        return
    print(f"使用 mkvmerge: {mkvmerge}")

    # 收集所有视频文件
    video_files = sorted(
        p for p in src_root.rglob("*")
        if p.is_file() and p.suffix.lower() in VIDEO_EXTS
    )
    total = len(video_files)

    if not total:
        print("未找到任何视频文件。")
        return

    print(f"\n找到 {total} 个视频文件。")
    init_quit_handler()

    ok = 0
    fail = 0
    deleted = 0

    try:
        for idx, src in enumerate(video_files, 1):
            # 检查中断标志
            if check_quit_key():
                print("\n⚠ 用户中断（Ctrl+Q），已处理部分不会丢失。")
                break

            try:
                rel = src.parent.relative_to(src_root)
            except ValueError:
                rel = Path()

            target_dir = dst_root / rel
            target_dir.mkdir(parents=True, exist_ok=True)
            dst = target_dir / (src.stem + ".mkv")

            if convert_video(src, dst, mkvmerge, idx, total):
                ok += 1
                if not src.is_file():
                    deleted += 1
            else:
                fail += 1
    except KeyboardInterrupt:
        print("\n⚠ 用户中断，已处理部分不会丢失。")

    print(f"\n处理完成：成功 {ok} 个，失败 {fail} 个，已删源 {deleted} 个，共 {total} 个。")


# ============================================================
# 入口
# ============================================================
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
