# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件夹位置（默认 d:\Studios\Folders\Ins\）与目标文件夹位置（默认 d:\Studios\Folders\Outs\）。
# 依次读取源文件夹下所有 htm / html / mhtml / mht 文件，进行下列操作，
# 放到目标文件夹保持子目录结构。转换成功后删除源文件。
# 1. 通过 mhtml-to-html 将 mhtml / mht 转成单文件 html。
# 2. 通过 Leanify 进行压缩。
# 3. Html 内嵌 base64 图片 → 解出后压缩（静态→AVIF，动态→AVIFS），重新 base64 嵌入。

import signal
import base64
import mimetypes
import re
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from io import BytesIO
from pathlib import Path

from bs4 import BeautifulSoup
from PIL import Image

# ==================== 外部工具路径 ====================
MHTML_TO_HTML_EXE = Path(r"d:\ProApps\MhtmlToHtml\mhtml-to-html.exe")
LEANIFY_EXE = Path(r"d:\ProApps\leanify\current\Leanify.exe")

HTML_EXTS = {".htm", ".html", ".mhtml", ".mht"}
MHTML_EXTS = {".mhtml", ".mht"}

_quit_requested = False  # Ctrl+Q 中断标志

# --- 消息常量 ---
MSG_INTERRUPTED = "\n\n用户中断程序，已退出。"
MSG_ERROR = "\n程序运行出错: {}"
MSG_EXIT = "\n按回车键退出..."
MSG_PRESS_ENTER = "按 Enter 键退出..."
MSG_ERR_TOOL_NOT_FOUND = "错误：未找到 {name}，路径为：{exe_path}"
MSG_ERR_FFMPEG_NOT_INSTALLED = "错误：ffmpeg 未安装或未添加到系统 PATH（用于动态图转换）"
MSG_ERR_MAGICK_NOT_INSTALLED = "错误：ImageMagick (magick) 未安装或未添加到系统 PATH"
MSG_ERR_MISSING_TOOLS = "\n请安装缺失的工具后重试。"
MSG_PATH_NOT_EXIST = "路径不存在: {}"
MSG_ASK_CREATE_DIR = "是否要创建此目录? (y/n): "
MSG_DIR_CREATED = "已创建目录: {}"
MSG_DIR_CREATE_FAILED = "创建目录失败: {}"
MSG_REENTER_PATH = "请重新输入有效路径"
MSG_STEP1_MHTML = "  步骤1：转换 MHTML → {}"
MSG_MHTML_CONVERT_FAILED = "  mhtml-to-html 转换失败: {}"
MSG_STEP2_LEANIFY = "  步骤2：Leanify 压缩 → {}"
MSG_LEANIFY_DONE = "  Leanify 压缩完成"
MSG_LEANIFY_FAILED = "  Leanify 压缩失败: {}"
MSG_STEP3_MEDIA = "  步骤3：转换内嵌媒体 → {}"
MSG_WEBP_DETECT_FAILED = "WebP 动图检测失败: {}"
MSG_GIF_DETECT_FAILED = "GIF 动图检测失败: {}"
MSG_MAGICK_CONVERT_FAILED = "ImageMagick 转换失败: {}"
MSG_AVIF_CONVERT_ERROR = "AVIF 转换异常: {}"
MSG_FFMPEG_GIF_TO_MP4_FAILED = "ffmpeg GIF转MP4失败: {}"
MSG_FFMPEG_MP4_TO_AVIF_FAILED = "ffmpeg MP4转AVIF失败: {}"
MSG_AVIFS_CONVERT_ERROR = "AVIFS 转换异常: {}"
MSG_FFMPEG_MP4_TO_AVIFS_FAILED = "ffmpeg MP4转AVIFS失败: {}"
MSG_MP4_TO_AVIFS_ERROR = "MP4转AVIFS异常: {}"
MSG_BASE64_DECODE_FAILED = "  Base64 解码失败: {}"
MSG_MEDIA_ITEM = "    媒体: {ext} → {label}, {orig_kb:.1f}KB → {comp_kb:.1f}KB (压缩率 {ratio:.1%})"
MSG_MEDIA_SUMMARY = "  媒体处理汇总: 处理了 {count} 个"
MSG_MEDIA_TOTAL = "  总大小: {orig_kb:.1f}KB → {comp_kb:.1f}KB (总体压缩率 {ratio:.1%})"
MSG_MEDIA_PROCESS_FAILED = "  媒体处理失败: {}"
MSG_TOOL_TITLE = "=== HTML/MHTML 综合处理工具 ==="
MSG_PROCESS_ORDER = "处理顺序："
MSG_ORDER_1 = "1. 将 .mhtml/.mht 转换为 .html"
MSG_ORDER_2 = "2. 对 HTML 执行 Leanify 压缩"
MSG_ORDER_3 = "3. 将 HTML 内嵌图片转为 AVIF/AVIFS"
MSG_ORDER_NOTE = "处理后的文件将保持原文件夹结构存放于目标文件夹，成功后删除源文件。\n"
MSG_ASK_SRC_DIR = "请输入源文件夹路径（默认 {}）: "
MSG_ASK_DST_DIR = "请输入目标文件夹路径（默认 {}）: "
MSG_INFO_SRC = "\n源文件夹: {}"
MSG_INFO_DST = "目标文件夹: {}"
MSG_INFO_AVIF_Q = "AVIF 质量: {}"
MSG_WARN_SAME_FOLDER = "警告：源文件夹和目标文件夹相同，将不会删除源文件！"
MSG_NOTE_DELETE = "注意：处理成功后源文件将被删除"
MSG_COPYING_NON_HTML = "\n正在复制非 HTML/MHTML 文件..."
MSG_FOUND_TOTAL = "\n共找到 {} 个文件需要处理"
MSG_START_TIME = "[{i}/{total}] {time_str} 开始: {rel_path}"
MSG_PROGRESS = "[{i}/{total}] {bar} {pct:5.1%} | ⏱ {elapsed:.0f}s | ✅{ok} ❌{fail} 🗑{deleted}"
MSG_LEANIFY_WARN = "  警告：Leanify 压缩失败，继续执行步骤3"
MSG_IMG_CONVERT_FAILED = "  图片转换失败，此文件处理异常"
MSG_SRC_DELETED = "  已删除源文件: {}"
MSG_SRC_DELETE_FAILED = "  删除源文件失败: {}"
MSG_ALL_DONE = "\n所有文件处理完成：成功 {ok}，失败 {fail}，删除源文件 {deleted}，共 {total}。"


# ==================== 辅助函数 ====================


def _format_bar(current: int, total: int, width: int = 20) -> str:
    """生成文本进度条：[████░░░░]"""
    if total <= 0:
        return "[" + " " * width + "]"
    filled = int(width * current / total)
    return "[" + "█" * filled + "░" * (width - filled) + "]"


# ==================== 工具检查 ====================

def check_exe(exe_path: Path, name: str) -> bool:
    """检查可执行文件是否存在。"""
    if not exe_path.is_file():
        print(MSG_ERR_TOOL_NOT_FOUND.format(name=name, exe_path=exe_path))
        return False
    return True


def check_ffmpeg_installed() -> bool:
    """检查 ffmpeg 是否可用。"""
    try:
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
        return result.returncode == 0 and "ffmpeg version" in result.stdout
    except Exception:
        return False


def check_magick_installed() -> bool:
    """检查 ImageMagick (magick) 是否可用。"""
    try:
        result = subprocess.run(["magick", "--version"], capture_output=True, text=True)
        return result.returncode == 0
    except Exception:
        return False


def get_valid_directory(prompt: str, default_path: str) -> str:
    """获取有效的目录路径，支持创建。"""
    while True:
        path = input(prompt).strip() or default_path
        path = str(Path(path))
        if Path(path).is_dir():
            return path
        print(MSG_PATH_NOT_EXIST.format(path))
        create = input(MSG_ASK_CREATE_DIR).lower()
        if create == "y":
            try:
                Path(path).mkdir(parents=True, exist_ok=True)
                print(MSG_DIR_CREATED.format(path))
                return path
            except OSError as e:
                print(MSG_DIR_CREATE_FAILED.format(e))
        else:
            print(MSG_REENTER_PATH)


# ==================== 步骤 1：MHTML → HTML ====================

def convert_mhtml_to_html(mht_path: str, html_path: str) -> bool:
    """调用 mhtml-to-html 将 MHTML/MHT 转换为 HTML。"""
    print(MSG_STEP1_MHTML.format(Path(html_path).name))
    Path(html_path).parent.mkdir(parents=True, exist_ok=True)
    cmd = [str(MHTML_TO_HTML_EXE), mht_path, "--output", html_path]
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(MSG_MHTML_CONVERT_FAILED.format(e.stderr))
        return False


# ==================== 步骤 2：Leanify 压缩 ====================

def leanify_file(file_path: str) -> bool:
    """调用 Leanify 压缩 HTML 文件（原地优化）。"""
    print(MSG_STEP2_LEANIFY.format(Path(file_path).name))
    cmd = [str(LEANIFY_EXE), "-i", "1", file_path]
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(MSG_LEANIFY_DONE)
        return True
    except subprocess.CalledProcessError as e:
        print(MSG_LEANIFY_FAILED.format(e.stderr))
        return False


# ==================== 图片处理函数 ====================


def _safe_unlink(f) -> None:
    """安全删除 NamedTemporaryFile，Windows 下等待文件锁释放后重试。"""
    if f is None:
        return
    import time
    for _ in range(3):
        try:
            Path(f.name).unlink(missing_ok=True)
            return
        except OSError:
            time.sleep(0.1)
    # 最后再试一次，失败就算了
    try:
        Path(f.name).unlink(missing_ok=True)
    except OSError:
        pass

def is_animated_webp(image_data: bytes) -> bool:
    """检测 WebP 图片是否为动态图。"""
    try:
        with Image.open(BytesIO(image_data)) as img:
            return bool(getattr(img, "is_animated", False))
    except Exception as e:
        print(MSG_WEBP_DETECT_FAILED.format(e))
        return False


def is_animated_gif(image_data: bytes) -> bool:
    """检测 GIF 图片是否为动态图。"""
    try:
        with Image.open(BytesIO(image_data)) as img:
            return img.is_animated
    except Exception as e:
        print(MSG_GIF_DETECT_FAILED.format(e))
        return False


def convert_to_avif(image_data: bytes, quality: int = 50) -> bytes:
    """将静态图片转换为 AVIF 格式。"""
    tmp_in = None
    tmp_out = None
    try:
        tmp_in = tempfile.NamedTemporaryFile(delete=False)
        tmp_out = tempfile.NamedTemporaryFile(delete=False, suffix=".avif")
        tmp_in.write(image_data)
        tmp_in.flush()
        tmp_in.close()  # 关闭句柄，释放 Windows 文件锁
        tmp_out.close()
        result = subprocess.run(
            ["magick", tmp_in.name, "-quality", str(quality), tmp_out.name],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            print(MSG_MAGICK_CONVERT_FAILED.format(result.stderr))
            return image_data
        return Path(tmp_out.name).read_bytes()
    except Exception as e:
        print(MSG_AVIF_CONVERT_ERROR.format(e))
        return image_data
    finally:
        if not _quit_requested:
            _safe_unlink(tmp_in)
            _safe_unlink(tmp_out)


def convert_to_avifs(image_data: bytes) -> bytes:
    """将动态图片转换为 AVIFS 格式（AVIF 动图）。"""
    tmp_in = None
    tmp_mp4 = None
    tmp_avif = None
    try:
        tmp_in = tempfile.NamedTemporaryFile(delete=False, suffix=".gif")
        tmp_in.write(image_data)
        tmp_in.flush()
        tmp_in.close()  # 关闭句柄，释放 Windows 文件锁

        tmp_mp4 = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        tmp_mp4.close()
        ffmpeg_cmd1 = [
            "ffmpeg", "-i", tmp_in.name, "-map", "0:v",
            "-c:v", "libsvtav1", "-crf", "32", "-preset", "5",
            "-an", "-y", tmp_mp4.name,
        ]
        result1 = subprocess.run(ffmpeg_cmd1, capture_output=True, text=True)
        if result1.returncode != 0:
            print(MSG_FFMPEG_GIF_TO_MP4_FAILED.format(result1.stderr))
            return image_data

        tmp_avif = tempfile.NamedTemporaryFile(delete=False, suffix=".avif")
        tmp_avif.close()
        ffmpeg_cmd2 = [
            "ffmpeg", "-i", tmp_mp4.name, "-c:v", "copy", "-y", tmp_avif.name,
        ]
        result2 = subprocess.run(ffmpeg_cmd2, capture_output=True, text=True)
        if result2.returncode != 0:
            print(MSG_FFMPEG_MP4_TO_AVIF_FAILED.format(result2.stderr))
            return image_data
        return Path(tmp_avif.name).read_bytes()
    except Exception as e:
        print(MSG_AVIFS_CONVERT_ERROR.format(e))
        return image_data
    finally:
        _safe_unlink(tmp_in)
        _safe_unlink(tmp_mp4)
        _safe_unlink(tmp_avif)


def convert_mp4_to_avifs(image_data: bytes) -> bytes:
    """将 MP4 视频直接转换为 AVIFS 格式。"""
    tmp_in = None
    tmp_avif = None
    try:
        tmp_in = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        tmp_in.write(image_data)
        tmp_in.flush()
        tmp_in.close()  # 关闭句柄，释放 Windows 文件锁

        tmp_avif = tempfile.NamedTemporaryFile(delete=False, suffix=".avif")
        tmp_avif.close()
        ffmpeg_cmd = [
            "ffmpeg", "-i", tmp_in.name, "-map", "0:v",
            "-c:v", "libsvtav1", "-crf", "32", "-preset", "5",
            "-an", "-y", tmp_avif.name,
        ]
        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(MSG_FFMPEG_MP4_TO_AVIFS_FAILED.format(result.stderr))
            return image_data
        return Path(tmp_avif.name).read_bytes()
    except Exception as e:
        print(MSG_MP4_TO_AVIFS_ERROR.format(e))
        return image_data
    finally:
        _safe_unlink(tmp_in)
        _safe_unlink(tmp_avif)


# ==================== 步骤 3：HTML 内嵌媒体处理 ====================

def process_html_file(html_path: str, avif_quality: int = 50) -> bool:
    """处理 HTML 文件中的内嵌 Base64 图片/视频，原地修改。"""
    print(MSG_STEP3_MEDIA.format(Path(html_path).name))
    try:
        soup = BeautifulSoup(Path(html_path).read_text(encoding="utf-8"), "html.parser")

        total_original_size = 0
        total_compressed_size = 0
        processed_media = 0

        media_tags = soup.find_all(["img", "video", "source"])

        for tag in media_tags:
            src = tag.get("src", "")
            if not src.startswith("data:"):
                continue

            match = re.match(r"data:((?:image|video)\/[a-z\+]+);base64,(.*)", src)
            if not match:
                continue
            mime_type, base64_data = match.groups()

            try:
                media_data = base64.b64decode(base64_data)
            except Exception as e:
                print(MSG_BASE64_DECODE_FAILED.format(e))
                continue

            original_size = len(media_data)
            total_original_size += original_size

            ext = mimetypes.guess_extension(mime_type)
            if not ext:
                continue

            optimized_data = None
            new_mime = "image/avif"
            is_animated = False

            if ext.lower() == ".mp4":
                is_animated = True
                optimized_data = convert_mp4_to_avifs(media_data)
            elif ext.lower() in {".bmp", ".jpg", ".jpeg", ".png", ".avif", ".heic", ".heif"}:
                optimized_data = convert_to_avif(media_data, avif_quality)
            elif ext.lower() == ".webp":
                if is_animated_webp(media_data):
                    is_animated = True
                    optimized_data = convert_to_avifs(media_data)
                else:
                    optimized_data = convert_to_avif(media_data, avif_quality)
            elif ext.lower() == ".gif":
                if is_animated_gif(media_data):
                    is_animated = True
                    optimized_data = convert_to_avifs(media_data)
                else:
                    optimized_data = convert_to_avif(media_data, avif_quality)
            else:
                continue

            if optimized_data is None:
                continue

            compressed_size = len(optimized_data)
            total_compressed_size += compressed_size
            processed_media += 1
            new_base64 = base64.b64encode(optimized_data).decode()
            tag["src"] = f"data:{new_mime};base64,{new_base64}"

            label = "AVIFS" if is_animated else "AVIF"
            print(MSG_MEDIA_ITEM.format(
                ext=ext, label=label,
                orig_kb=original_size/1024, comp_kb=compressed_size/1024,
                ratio=1 - compressed_size/original_size,
            ))

        Path(html_path).write_text(str(soup), encoding="utf-8")

        print(MSG_MEDIA_SUMMARY.format(count=processed_media))
        if processed_media > 0:
            print(MSG_MEDIA_TOTAL.format(
                orig_kb=total_original_size/1024, comp_kb=total_compressed_size/1024,
                ratio=1 - total_compressed_size/total_original_size,
            ))
        return True
    except Exception as e:
        print(MSG_MEDIA_PROCESS_FAILED.format(e))
        return False


# ==================== 文件复制 ====================

def copy_non_html_files(src_folder: str, dst_folder: str) -> None:
    """复制非 HTML/MHTML 文件到目标，保持目录结构。"""
    for src_path in Path(src_folder).rglob("*"):
        if not src_path.is_file():
            continue
        if src_path.suffix.lower() in HTML_EXTS:
            continue
        rel = src_path.relative_to(src_folder)
        dst = Path(dst_folder) / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(src_path), str(dst))


# ==================== 主程序 ====================
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
    _init_quit_handler()
    print(MSG_TOOL_TITLE)
    print(MSG_PROCESS_ORDER)
    print(MSG_ORDER_1)
    print(MSG_ORDER_2)
    print(MSG_ORDER_3)
    print(MSG_ORDER_NOTE)

    # 检查必需工具
    tools_ok = True
    if not check_exe(MHTML_TO_HTML_EXE, "mhtml-to-html"):
        tools_ok = False
    if not check_exe(LEANIFY_EXE, "Leanify"):
        tools_ok = False
    if not check_ffmpeg_installed():
        print(MSG_ERR_FFMPEG_NOT_INSTALLED)
        tools_ok = False
    if not check_magick_installed():
        print(MSG_ERR_MAGICK_NOT_INSTALLED)
        tools_ok = False

    if not tools_ok:
        print(MSG_ERR_MISSING_TOOLS)
        return

    default_src = r"d:\Studios\Folders\Ins"
    default_dst = r"d:\Studios\Folders\Outs"
    src_folder = get_valid_directory(MSG_ASK_SRC_DIR.format(default_src), default_src)
    dst_folder = get_valid_directory(MSG_ASK_DST_DIR.format(default_dst), default_dst)

    avif_quality = 50

    print(MSG_INFO_SRC.format(src_folder))
    print(MSG_INFO_DST.format(dst_folder))
    print(MSG_INFO_AVIF_Q.format(avif_quality))

    same_folder = Path(src_folder).resolve() == Path(dst_folder).resolve()
    if same_folder:
        print(MSG_WARN_SAME_FOLDER)
    else:
        print(MSG_NOTE_DELETE)

    # 第一步：复制非 HTML/MHTML 文件
    print(MSG_COPYING_NON_HTML)
    copy_non_html_files(src_folder, dst_folder)

    # 第二步：收集所有 HTML/MHTML 文件
    all_files: list[tuple[str, str, str]] = []
    for src_path in Path(src_folder).rglob("*"):
        if not src_path.is_file():
            continue
        ext = src_path.suffix.lower()
        if ext not in HTML_EXTS:
            continue

        rel = str(src_path.relative_to(src_folder))
        if ext in MHTML_EXTS:
            dst = str(Path(dst_folder) / Path(rel).with_suffix(".html"))
        else:
            dst = str(Path(dst_folder) / rel)
        all_files.append((str(src_path), dst, ext))

    total = len(all_files)
    print(MSG_FOUND_TOTAL.format(total))

    ok = 0
    fail = 0
    deleted = 0
    start_all = time.time()

    for i, (src_path, dst_path, ext) in enumerate(all_files, 1):
        if _check_quit():
            print(MSG_INTERRUPTED)
            break

        rel_path = Path(src_path).relative_to(src_folder)
        now_str = datetime.now().strftime("%H:%M:%S")
        print(MSG_START_TIME.format(i=i, total=total, time_str=now_str, rel_path=rel_path))

        # 步骤 1：MHTML → HTML
        if ext in MHTML_EXTS:
            if not convert_mhtml_to_html(src_path, dst_path):
                fail += 1
                print(MSG_PROGRESS.format(i=i, total=total, bar=_format_bar(i, total), pct=i/total, elapsed=time.time()-start_all, ok=ok, fail=fail, deleted=deleted))
                continue
        else:
            Path(dst_path).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_path, dst_path)

        # 步骤 2：Leanify
        if not leanify_file(dst_path):
            print(MSG_LEANIFY_WARN)

        # 步骤 3：内嵌媒体处理
        if not process_html_file(dst_path, avif_quality):
            print(MSG_IMG_CONVERT_FAILED)
            fail += 1
            print(MSG_PROGRESS.format(i=i, total=total, bar=_format_bar(i, total), pct=i/total, elapsed=time.time()-start_all, ok=ok, fail=fail, deleted=deleted))
            continue

        # 删除源文件（如果不同文件夹，用户中断时保留）
        if not same_folder and not _quit_requested:
            try:
                Path(src_path).unlink()
                deleted += 1
                print(MSG_SRC_DELETED.format(src_path))
            except OSError as e:
                print(MSG_SRC_DELETE_FAILED.format(e))

        ok += 1
        print(MSG_PROGRESS.format(i=i, total=total, bar=_format_bar(i, total), pct=i/total, elapsed=time.time()-start_all, ok=ok, fail=fail, deleted=deleted))

    elapsed_all = time.time() - start_all
    print(MSG_ALL_DONE.format(ok=ok, fail=fail, deleted=deleted, total=total))
    print(f"总耗时: {elapsed_all:.0f}s ({elapsed_all/60:.1f}min)")



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
