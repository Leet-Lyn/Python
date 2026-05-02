# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件夹位置（默认为“d:\Works\Ins\”）与目标文件夹位置（默认为“d:\Works\Outs\”）。
# 依次读取源文件夹下的所有 htm、html、mhtml、mht 文件，进行下列操作，放在目标文件夹位置，保持文件夹及子文件结构。转换成功后删除源文件。
# 1. 通过 mhtml-to-html，将 mhtml、mht 文件转成 单文件 html。mhtml-to-html.exe（d:\ProApps\MhtmlToHtml\mhtml-to-html.exe），命令：mhtml-to-html file.mht --output output_file.html。htm、html 则不处理。
# 2. 通过 Leanify 进行压缩。Leanify.exe（d:\ProApps\Leanify\Leanify.exe）。命令：leanify [options] paths。
# 3. Html 文件内嵌的图片是（base64 格式）。我希望将它批量转成 html（zip）格式（要求生成的 html 还能被浏览器打开）。然后压缩图片。如果图片格式为 bmp、jpg、jpeg、png 或静态 webp 格式、或静态 avif 格式、静态 heic 格式、静态 heif 格式，则使用 magick 压缩成 avif 格式，使用类似命令：magick convert input.jpg -quality 50 output.avif。如果图片文件格式为 gif 或动态 webp 格式或 mp4 格式，则使用 magick 压缩成 gif 格式，类似命令：magick convert input.webp -fuzz 5% -quality 75 -layers Optimize output.gif。

# 导入模块
import os
import re
import base64
import subprocess
import mimetypes
import shutil
import tempfile
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

# ==================== 外部工具路径（请根据实际安装位置修改）====================
MHTML_TO_HTML_EXE = r"d:\ProApps\MhtmlToHtml\mhtml-to-html.exe"
LEANIFY_EXE = r"d:\ProApps\Leanify\Leanify.exe"
# ===========================================================================

def check_exe(exe_path, name):
    """检查可执行文件是否存在"""
    if not os.path.isfile(exe_path):
        print(f"错误：未找到 {name}，路径为：{exe_path}")
        return False
    return True

def check_ffmpeg_installed():
    """检查 ffmpeg 是否可用（用于动态图转换）"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        return result.returncode == 0 and 'ffmpeg version' in result.stdout
    except:
        return False

def check_magick_installed():
    """检查 ImageMagick (magick) 是否可用"""
    try:
        result = subprocess.run(['magick', '--version'], capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

def get_valid_directory(prompt, default_path):
    """获取有效的目录路径，支持创建"""
    while True:
        path = input(prompt).strip() or default_path
        path = os.path.normpath(path)
        if os.path.isdir(path):
            return path
        else:
            print(f"路径不存在: {path}")
            create = input("是否要创建此目录? (y/n): ").lower()
            if create == 'y':
                try:
                    os.makedirs(path, exist_ok=True)
                    print(f"已创建目录: {path}")
                    return path
                except Exception as e:
                    print(f"创建目录失败: {str(e)}")
            else:
                print("请重新输入有效路径")

def convert_mhtml_to_html(mht_path, html_path):
    """调用 mhtml-to-html 将 MHTML/MHT 转换为 HTML"""
    print(f"  步骤1：转换 MHTML -> {os.path.basename(html_path)}")
    os.makedirs(os.path.dirname(html_path), exist_ok=True)
    cmd = [MHTML_TO_HTML_EXE, mht_path, "--output", html_path]
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"  mhtml-to-html 转换失败: {e.stderr}")
        return False

def leanify_file(file_path):
    """调用 Leanify 压缩 HTML 文件（原地优化）"""
    print(f"  步骤2：Leanify 压缩 -> {os.path.basename(file_path)}")
    # 使用 -i 1 表示最高压缩级别
    cmd = [LEANIFY_EXE, "-i", "1", file_path]
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"  Leanify 压缩完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  Leanify 压缩失败: {e.stderr}")
        return False

# ==================== 图片处理函数（源自您的参考脚本）====================
def is_animated_webp(image_data):
    """检测 WebP 图片是否为动态图"""
    try:
        with Image.open(BytesIO(image_data)) as img:
            return getattr(img, "is_animated", False)
    except Exception as e:
        print(f"WebP 动图检测失败: {str(e)}")
        return False

def is_animated_gif(image_data):
    """检测 GIF 图片是否为动态图"""
    try:
        with Image.open(BytesIO(image_data)) as img:
            return img.is_animated
    except Exception as e:
        print(f"GIF 动图检测失败: {str(e)}")
        return False

def convert_to_avif(image_data, quality=50):
    """将静态图片转换为 AVIF 格式"""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.avif') as tmp_out:
            with tempfile.NamedTemporaryFile(delete=False) as tmp_in:
                tmp_in.write(image_data)
                tmp_in.flush()
                result = subprocess.run(
                    ['magick', tmp_in.name, '-quality', str(quality), tmp_out.name],
                    capture_output=True, text=True
                )
                if result.returncode != 0:
                    print(f"ImageMagick 转换失败: {result.stderr}")
                    return image_data
                with open(tmp_out.name, 'rb') as f:
                    return f.read()
    except Exception as e:
        print(f"AVIF 转换异常: {str(e)}")
        return image_data
    finally:
        if 'tmp_in' in locals() and os.path.exists(tmp_in.name):
            os.unlink(tmp_in.name)
        if 'tmp_out' in locals() and os.path.exists(tmp_out.name):
            os.unlink(tmp_out.name)

def convert_to_avifs(image_data):
    """将动态图片转换为 AVIFS 格式（AVIF 动图）"""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.gif') as tmp_in:
            tmp_in.write(image_data)
            tmp_in.flush()
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_mp4:
                ffmpeg_cmd1 = [
                    'ffmpeg', '-i', tmp_in.name, '-map', '0:v',
                    '-c:v', 'libsvtav1', '-crf', '32', '-preset', '5',
                    '-an', '-y', tmp_mp4.name
                ]
                result1 = subprocess.run(ffmpeg_cmd1, capture_output=True, text=True)
                if result1.returncode != 0:
                    print(f"ffmpeg GIF转MP4失败: {result1.stderr}")
                    return image_data
                with tempfile.NamedTemporaryFile(delete=False, suffix='.avif') as tmp_avif:
                    ffmpeg_cmd2 = [
                        'ffmpeg', '-i', tmp_mp4.name, '-c:v', 'copy', '-y', tmp_avif.name
                    ]
                    result2 = subprocess.run(ffmpeg_cmd2, capture_output=True, text=True)
                    if result2.returncode != 0:
                        print(f"ffmpeg MP4转AVIF失败: {result2.stderr}")
                        return image_data
                    with open(tmp_avif.name, 'rb') as f:
                        return f.read()
    except Exception as e:
        print(f"AVIFS 转换异常: {str(e)}")
        return image_data
    finally:
        for f in ['tmp_in', 'tmp_mp4', 'tmp_avif']:
            if f in locals() and os.path.exists(locals()[f].name):
                os.unlink(locals()[f].name)

def process_html_file(html_path, avif_quality=50):
    """
    处理 HTML 文件中的内嵌 Base64 图片（转换格式、压缩），原地修改文件。
    这是步骤3。
    """
    print(f"  步骤3：转换内嵌图片 -> {os.path.basename(html_path)}")
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
        
        total_original_size = 0
        total_compressed_size = 0
        processed_images = 0
        
        for img in soup.find_all('img'):
            src = img.get('src', '')
            if src.startswith('data:image'):
                match = re.match(r'data:(image\/[a-z\+]+);base64,(.*)', src)
                if not match:
                    continue
                mime_type, base64_data = match.groups()
                try:
                    image_data = base64.b64decode(base64_data)
                except Exception as e:
                    print(f"  Base64 解码失败: {str(e)}")
                    continue
                
                original_size = len(image_data)
                total_original_size += original_size
                ext = mimetypes.guess_extension(mime_type)
                if not ext:
                    continue
                
                processed = False
                optimized_data = None
                new_mime = mime_type
                is_animated = False
                
                # 静态图片格式
                static_formats = ['.bmp', '.jpg', '.jpeg', '.png', '.avif', '.heic', '.heif']
                if ext.lower() in static_formats:
                    optimized_data = convert_to_avif(image_data, avif_quality)
                    new_mime = 'image/avif'
                    processed = True
                elif ext.lower() == '.webp':
                    if is_animated_webp(image_data):
                        is_animated = True
                        optimized_data = convert_to_avifs(image_data)
                        new_mime = 'image/avif'
                        processed = True
                    else:
                        optimized_data = convert_to_avif(image_data, avif_quality)
                        new_mime = 'image/avif'
                        processed = True
                elif ext.lower() == '.gif':
                    if is_animated_gif(image_data):
                        is_animated = True
                        optimized_data = convert_to_avifs(image_data)
                        new_mime = 'image/avif'
                        processed = True
                    else:
                        optimized_data = convert_to_avif(image_data, avif_quality)
                        new_mime = 'image/avif'
                        processed = True
                
                if processed and optimized_data is not None:
                    compressed_size = len(optimized_data)
                    total_compressed_size += compressed_size
                    processed_images += 1
                    new_base64 = base64.b64encode(optimized_data).decode('utf-8')
                    img['src'] = f'data:{new_mime};base64,{new_base64}'
                    img_type = "AVIFS" if is_animated else "AVIF"
                    print(f"    图片: {ext} -> {img_type}, "
                          f"{original_size/1024:.1f}KB -> {compressed_size/1024:.1f}KB "
                          f"(压缩率 {1 - compressed_size/original_size:.1%})")
        
        # 写回文件
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        
        print(f"  图片处理汇总: 处理了 {processed_images} 张图片")
        if processed_images > 0:
            print(f"  总大小: {total_original_size/1024:.1f}KB -> {total_compressed_size/1024:.1f}KB "
                  f"(总体压缩率 {1 - total_compressed_size/total_original_size:.1%})")
        return True
    except Exception as e:
        print(f"  图片处理失败: {str(e)}")
        return False

def copy_non_html_files(src_folder, dst_folder):
    """复制非 HTML/MHTML 文件（保持目录结构）"""
    for root, dirs, files in os.walk(src_folder):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in ('.html', '.htm', '.mhtml', '.mht'):
                continue
            src_path = os.path.join(root, file)
            rel_path = os.path.relpath(src_path, src_folder)
            dst_path = os.path.join(dst_folder, rel_path)
            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
            shutil.copy2(src_path, dst_path)

# ==================== 主程序 ====================
def main():
    print("=== HTML/MHTML 综合处理工具（指定顺序版） ===")
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
        input("按 Enter 键退出...")
        return
    
    # 获取源和目标文件夹（默认值按题目要求）
    default_src = r"d:\Works\Ins"
    default_dst = r"d:\Works\Outs"
    src_folder = get_valid_directory(f"请输入源文件夹路径（默认为 {default_src}）: ", default_src)
    dst_folder = get_valid_directory(f"请输入目标文件夹路径（默认为 {default_dst}）: ", default_dst)
    
    avif_quality = 50  # AVIF 质量 (1-100)
    
    print(f"\n源文件夹: {src_folder}")
    print(f"目标文件夹: {dst_folder}")
    print(f"AVIF 质量: {avif_quality}")
    
    same_folder = os.path.abspath(src_folder) == os.path.abspath(dst_folder)
    if same_folder:
        print("警告：源文件夹和目标文件夹相同，将不会删除源文件！")
    else:
        print("注意：处理成功后源文件将被删除")
    
    # 第一步：复制所有非 HTML/MHTML 文件到目标文件夹
    print("\n正在复制非 HTML/MHTML 文件...")
    copy_non_html_files(src_folder, dst_folder)
    
    # 第二步：收集所有需要处理的 HTML/MHTML 文件
    all_files = []
    for root, dirs, files in os.walk(src_folder):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in ('.htm', '.html', '.mhtml', '.mht'):
                src_path = os.path.join(root, file)
                rel_path = os.path.relpath(src_path, src_folder)
                # 目标路径：对于 MHTML，扩展名改为 .html；对于 HTML 保持不变
                if ext in ('.mhtml', '.mht'):
                    base = os.path.splitext(rel_path)[0]
                    dst_path = os.path.join(dst_folder, base + '.html')
                else:
                    dst_path = os.path.join(dst_folder, rel_path)
                all_files.append((src_path, dst_path, ext))
    
    total_files = len(all_files)
    print(f"\n共找到 {total_files} 个文件需要处理")
    
    success_count = 0
    error_count = 0
    deleted_count = 0
    
    for i, (src_path, dst_path, ext) in enumerate(all_files, 1):
        print(f"\n[{i}/{total_files}] 处理: {os.path.relpath(src_path, src_folder)}")
        
        # ---------- 步骤1：生成 HTML（如果是 MHTML） ----------
        if ext in ('.mhtml', '.mht'):
            if not convert_mhtml_to_html(src_path, dst_path):
                error_count += 1
                continue
            # 转换成功后，dst_path 即为 HTML 文件，继续后续步骤
        else:  # .htm / .html
            # 直接复制源文件到目标位置（尚未处理）
            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
            shutil.copy2(src_path, dst_path)
        
        # ---------- 步骤2：Leanify 压缩 HTML ----------
        if not leanify_file(dst_path):
            # Leanify 失败不影响继续（但记录警告）
            print("  警告：Leanify 压缩失败，继续执行步骤3")
        
        # ---------- 步骤3：图片转换（原地修改 HTML） ----------
        if not process_html_file(dst_path, avif_quality):
            print("  图片转换失败，此文件处理异常")
            error_count += 1
            # 即使失败也尝试删除源文件？为安全起见，不删除
            continue
        
        # ---------- 删除源文件（如果不同文件夹） ----------
        if not same_folder:
            try:
                os.remove(src_path)
                deleted_count += 1
                print(f"  已删除源文件: {src_path}")
            except Exception as e:
                print(f"  删除源文件失败: {str(e)}")
        
        success_count += 1
    
    print("\n所有文件处理完成！")
    print(f"成功: {success_count}, 失败: {error_count}, 删除源文件: {deleted_count}")
    input("按 Enter 键退出...")

if __name__ == "__main__":
    main()