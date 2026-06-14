# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件夹位置（默认 d:\Studios\Folders\Ins\）与目标文件夹位置（默认 d:\Studios\Folders\Outs\）。
# 依次读取源文件夹下所有 htm / html / mhtml / mht 文件，进行下列操作，
# 放到目标文件夹保持子目录结构。转换成功后删除源文件。
# 1. 通过 mhtml-to-html 将 mhtml / mht 转成单文件 html。
# 2. 通过 Leanify 进行压缩。
# 3. Html 内嵌 base64 图片 → 解出后压缩（静态→AVIF，动态→AVIFS），重新 base64 嵌入。

import base64
import mimetypes
import re
import shutil
import subprocess
import sys
import tempfile
from io import BytesIO
from pathlib import Path

from bs4 import BeautifulSoup
from PIL import Image

# ==================== 外部工具路径 ====================
MHTML_TO_HTML_EXE = Path(r"d:\ProApps\MhtmlToHtml\mhtml-to-html.exe")
LEANIFY_EXE = Path(r"d:\ProApps\Leanify\Leanify.exe")

HTML_EXTS = {".htm", ".html", ".mhtml", ".mht"}
MHTML_EXTS = {".mhtml", ".mht"}


# ==================== 工具检查 ====================

def check_exe(exe_path: Path, name: str) -> bool:
    """检查可执行文件是否存在。"""
    if not exe_path.is_file():
        print(f"错误：未找到 {name}，路径为：{exe_path}")
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
        print(f"路径不存在: {path}")
        create = input("是否要创建此目录? (y/n): ").lower()
        if create == "y":
            try:
                Path(path).mkdir(parents=True, exist_ok=True)
                print(f"已创建目录: {path}")
                return path
            except OSError as e:
                print(f"创建目录失败: {e}")
        else:
            print("请重新输入有效路径")


# ==================== 步骤 1：MHTML → HTML ====================

def convert_mhtml_to_html(mht_path: str, html_path: str) -> bool:
    """调用 mhtml-to-html 将 MHTML/MHT 转换为 HTML。"""
    print(f"  步骤1：转换 MHTML → {Path(html_path).name}")
    Path(html_path).parent.mkdir(parents=True, exist_ok=True)
    cmd = [str(MHTML_TO_HTML_EXE), mht_path, "--output", html_path]
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"  mhtml-to-html 转换失败: {e.stderr}")
        return False


# ==================== 步骤 2：Leanify 压缩 ====================

def leanify_file(file_path: str) -> bool:
    """调用 Leanify 压缩 HTML 文件（原地优化）。"""
    print(f"  步骤2：Leanify 压缩 → {Path(file_path).name}")
    cmd = [str(LEANIFY_EXE), "-i", "1", file_path]
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"  Leanify 压缩完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  Leanify 压缩失败: {e.stderr}")
        return False


# ==================== 图片处理函数 ====================

def is_animated_webp(image_data: bytes) -> bool:
    """检测 WebP 图片是否为动态图。"""
    try:
        with Image.open(BytesIO(image_data)) as img:
            return bool(getattr(img, "is_animated", False))
    except Exception as e:
        print(f"WebP 动图检测失败: {e}")
        return False


def is_animated_gif(image_data: bytes) -> bool:
    """检测 GIF 图片是否为动态图。"""
    try:
        with Image.open(BytesIO(image_data)) as img:
            return img.is_animated
    except Exception as e:
        print(f"GIF 动图检测失败: {e}")
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
        result = subprocess.run(
            ["magick", tmp_in.name, "-quality", str(quality), tmp_out.name],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            print(f"ImageMagick 转换失败: {result.stderr}")
            return image_data
        return Path(tmp_out.name).read_bytes()
    except Exception as e:
        print(f"AVIF 转换异常: {e}")
        return image_data
    finally:
        for f in (tmp_in, tmp_out):
            if f is not None:
                Path(f.name).unlink(missing_ok=True)


def convert_to_avifs(image_data: bytes) -> bytes:
    """将动态图片转换为 AVIFS 格式（AVIF 动图）。"""
    tmp_in = None
    tmp_mp4 = None
    tmp_avif = None
    try:
        tmp_in = tempfile.NamedTemporaryFile(delete=False, suffix=".gif")
        tmp_in.write(image_data)
        tmp_in.flush()

        tmp_mp4 = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        ffmpeg_cmd1 = [
            "ffmpeg", "-i", tmp_in.name, "-map", "0:v",
            "-c:v", "libsvtav1", "-crf", "32", "-preset", "5",
            "-an", "-y", tmp_mp4.name,
        ]
        result1 = subprocess.run(ffmpeg_cmd1, capture_output=True, text=True)
        if result1.returncode != 0:
            print(f"ffmpeg GIF转MP4失败: {result1.stderr}")
            return image_data

        tmp_avif = tempfile.NamedTemporaryFile(delete=False, suffix=".avif")
        ffmpeg_cmd2 = [
            "ffmpeg", "-i", tmp_mp4.name, "-c:v", "copy", "-y", tmp_avif.name,
        ]
        result2 = subprocess.run(ffmpeg_cmd2, capture_output=True, text=True)
        if result2.returncode != 0:
            print(f"ffmpeg MP4转AVIF失败: {result2.stderr}")
            return image_data
        return Path(tmp_avif.name).read_bytes()
    except Exception as e:
        print(f"AVIFS 转换异常: {e}")
        return image_data
    finally:
        for f in (tmp_in, tmp_mp4, tmp_avif):
            if f is not None:
                Path(f.name).unlink(missing_ok=True)


def convert_mp4_to_avifs(image_data: bytes) -> bytes:
    """将 MP4 视频直接转换为 AVIFS 格式。"""
    tmp_in = None
    tmp_avif = None
    try:
        tmp_in = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        tmp_in.write(image_data)
        tmp_in.flush()

        tmp_avif = tempfile.NamedTemporaryFile(delete=False, suffix=".avif")
        ffmpeg_cmd = [
            "ffmpeg", "-i", tmp_in.name, "-map", "0:v",
            "-c:v", "libsvtav1", "-crf", "32", "-preset", "5",
            "-an", "-y", tmp_avif.name,
        ]
        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"ffmpeg MP4转AVIFS失败: {result.stderr}")
            return image_data
        return Path(tmp_avif.name).read_bytes()
    except Exception as e:
        print(f"MP4转AVIFS异常: {e}")
        return image_data
    finally:
        for f in (tmp_in, tmp_avif):
            if f is not None:
                Path(f.name).unlink(missing_ok=True)


# ==================== 步骤 3：HTML 内嵌媒体处理 ====================

def process_html_file(html_path: str, avif_quality: int = 50) -> bool:
    """处理 HTML 文件中的内嵌 Base64 图片/视频，原地修改。"""
    print(f"  步骤3：转换内嵌媒体 → {Path(html_path).name}")
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
                print(f"  Base64 解码失败: {e}")
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
            print(
                f"    媒体: {ext} → {label}, "
                f"{original_size/1024:.1f}KB → {compressed_size/1024:.1f}KB "
                f"(压缩率 {1 - compressed_size/original_size:.1%})"
            )

        Path(html_path).write_text(str(soup), encoding="utf-8")

        print(f"  媒体处理汇总: 处理了 {processed_media} 个")
        if processed_media > 0:
            print(
                f"  总大小: {total_original_size/1024:.1f}KB → {total_compressed_size/1024:.1f}KB "
                f"(总体压缩率 {1 - total_compressed_size/total_original_size:.1%})"
            )
        return True
    except Exception as e:
        print(f"  媒体处理失败: {e}")
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

def main() -> None:
    print("=== HTML/MHTML 综合处理工具 ===")
    print("处理顺序：")
    print("1. 将 .mhtml/.mht 转换为 .html")
    print("2. 对 HTML 执行 Leanify 压缩")
    print("3. 将 HTML 内嵌图片转为 AVIF/AVIFS")
    print("处理后的文件将保持原文件夹结构存放于目标文件夹，成功后删除源文件。\n")

    # 检查必需工具
    tools_ok = True
    if not check_exe(MHTML_TO_HTML_EXE, "mhtml-to-html"):
        tools_ok = False
    if not check_exe(LEANIFY_EXE, "Leanify"):
        tools_ok = False
    if not check_ffmpeg_installed():
        print("错误：ffmpeg 未安装或未添加到系统 PATH（用于动态图转换）")
        tools_ok = False
    if not check_magick_installed():
        print("错误：ImageMagick (magick) 未安装或未添加到系统 PATH")
        tools_ok = False

    if not tools_ok:
        print("\n请安装缺失的工具后重试。")
        return

    default_src = r"d:\Studios\Folders\Ins"
    default_dst = r"d:\Studios\Folders\Outs"
    src_folder = get_valid_directory(f"请输入源文件夹路径（默认 {default_src}）: ", default_src)
    dst_folder = get_valid_directory(f"请输入目标文件夹路径（默认 {default_dst}）: ", default_dst)

    avif_quality = 50

    print(f"\n源文件夹: {src_folder}")
    print(f"目标文件夹: {dst_folder}")
    print(f"AVIF 质量: {avif_quality}")

    same_folder = Path(src_folder).resolve() == Path(dst_folder).resolve()
    if same_folder:
        print("警告：源文件夹和目标文件夹相同，将不会删除源文件！")
    else:
        print("注意：处理成功后源文件将被删除")

    # 第一步：复制非 HTML/MHTML 文件
    print("\n正在复制非 HTML/MHTML 文件...")
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
    print(f"\n共找到 {total} 个文件需要处理")

    ok = 0
    fail = 0
    deleted = 0

    for i, (src_path, dst_path, ext) in enumerate(all_files, 1):
        print(f"\n[{i}/{total}] 处理: {Path(src_path).relative_to(src_folder)}")

        # 步骤 1：MHTML → HTML
        if ext in MHTML_EXTS:
            if not convert_mhtml_to_html(src_path, dst_path):
                fail += 1
                continue
        else:
            Path(dst_path).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_path, dst_path)

        # 步骤 2：Leanify
        if not leanify_file(dst_path):
            print("  警告：Leanify 压缩失败，继续执行步骤3")

        # 步骤 3：内嵌媒体处理
        if not process_html_file(dst_path, avif_quality):
            print("  图片转换失败，此文件处理异常")
            fail += 1
            continue

        # 删除源文件（如果不同文件夹）
        if not same_folder:
            try:
                Path(src_path).unlink()
                deleted += 1
                print(f"  已删除源文件: {src_path}")
            except OSError as e:
                print(f"  删除源文件失败: {e}")

        ok += 1

    print(f"\n所有文件处理完成：成功 {ok}，失败 {fail}，删除源文件 {deleted}，共 {total}。")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
    input("按 Enter 键退出...")
