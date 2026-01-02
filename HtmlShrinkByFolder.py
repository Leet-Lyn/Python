# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件夹位置（默认为“d:\Works\Finisheds\”）与目标文件夹位置（默认为“d:\Works\Finishedx\”）。
# 依次读取源文件夹下的所有 html 文件，进行下列操作，放在目标文件夹位置，保持文件夹及子文件结构。
# Html 文件内嵌的图片是（base64 格式）。我希望将它批量转成 html（zip）格式（要求生成的 html 还能被浏览器打开）。然后压缩图片。如果图片格式为 bmp、jpg、jpeg、png 或静态 webp 格式、或静态 avif 格式、静态 heic 格式、静态 heif 格式，则使用 magick 压缩成 avif 格式，使用类似命令：magick convert input.jpg -quality 50 output.avif。如果图片文件格式为 gif 或动态 webp 格式或 mp4 格式，则使用 magick 压缩成 gif 格式，类似命令：magick convert input.webp -fuzz 5% -quality 75 -layers Optimize output.gif。

# 导入模块
import os
import re
import base64
import subprocess
import mimetypes
import shutil
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import tempfile

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
                
                # 使用 ImageMagick 进行转换
                result = subprocess.run(
                    ['magick', tmp_in.name, '-quality', str(quality), tmp_out.name],
                    capture_output=True,
                    text=True
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
        # 第一步：创建临时输入文件
        with tempfile.NamedTemporaryFile(delete=False, suffix='.gif') as tmp_in:
            tmp_in.write(image_data)
            tmp_in.flush()
            
            # 第二步：创建临时MP4文件
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_mp4:
                # 使用ffmpeg将GIF转为MP4 (SVT-AV1编码)
                ffmpeg_cmd1 = [
                    'ffmpeg', 
                    '-i', tmp_in.name,
                    '-map', '0:v',
                    '-c:v', 'libsvtav1',
                    '-crf', '32',
                    '-preset', '5',
                    '-an',  # 忽略音频
                    '-y',   # 覆盖输出文件
                    tmp_mp4.name
                ]
                
                result1 = subprocess.run(
                    ffmpeg_cmd1,
                    capture_output=True,
                    text=True
                )
                
                if result1.returncode != 0:
                    print(f"ffmpeg GIF转MP4失败: {result1.stderr}")
                    return image_data
                
                # 第三步：创建临时AVIF文件
                with tempfile.NamedTemporaryFile(delete=False, suffix='.avif') as tmp_avif:
                    # 使用ffmpeg将MP4转为AVIF动图
                    ffmpeg_cmd2 = [
                        'ffmpeg', 
                        '-i', tmp_mp4.name,
                        '-c:v', 'copy',
                        '-y',   # 覆盖输出文件
                        tmp_avif.name
                    ]
                    
                    result2 = subprocess.run(
                        ffmpeg_cmd2,
                        capture_output=True,
                        text=True
                    )
                    
                    if result2.returncode != 0:
                        print(f"ffmpeg MP4转AVIF失败: {result2.stderr}")
                        return image_data
                    
                    # 读取转换后的AVIF数据
                    with open(tmp_avif.name, 'rb') as f:
                        return f.read()
    except Exception as e:
        print(f"AVIFS 转换异常: {str(e)}")
        return image_data
    finally:
        # 清理临时文件
        if 'tmp_in' in locals() and os.path.exists(tmp_in.name):
            os.unlink(tmp_in.name)
        if 'tmp_mp4' in locals() and os.path.exists(tmp_mp4.name):
            os.unlink(tmp_mp4.name)
        if 'tmp_avif' in locals() and os.path.exists(tmp_avif.name):
            os.unlink(tmp_avif.name)

def process_html_file(input_path, output_path, avif_quality=50):
    """处理 HTML 文件中的图片"""
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
        
        total_original_size = 0
        total_compressed_size = 0
        processed_images = 0
        
        for img in soup.find_all('img'):
            src = img.get('src', '')
            
            # 检测 Base64 图片
            if src.startswith('data:image'):
                match = re.match(r'data:(image\/[a-z\+]+);base64,(.*)', src)
                if not match:
                    continue
                    
                mime_type, base64_data = match.groups()
                try:
                    image_data = base64.b64decode(base64_data)
                except Exception as e:
                    print(f"Base64 解码失败: {str(e)}")
                    continue
                
                original_size = len(image_data)
                total_original_size += original_size
                
                # 获取文件扩展名
                ext = mimetypes.guess_extension(mime_type)
                if not ext:
                    continue
                    
                processed = False
                optimized_data = None
                new_mime = mime_type
                is_animated = False
                
                # 处理静态图片
                static_formats = ['.bmp', '.jpg', '.jpeg', '.png', '.avif', '.heic', '.heif']
                if ext.lower() in static_formats:
                    # 静态图片处理
                    optimized_data = convert_to_avif(image_data, avif_quality)
                    new_mime = 'image/avif'
                    processed = True
                
                # 处理 WebP 图片（可能是静态或动态）
                elif ext.lower() == '.webp':
                    # 检测是否为动态 WebP
                    if is_animated_webp(image_data):
                        is_animated = True
                        optimized_data = convert_to_avifs(image_data)
                        new_mime = 'image/avif'
                        processed = True
                    else:
                        # 静态 WebP
                        optimized_data = convert_to_avif(image_data, avif_quality)
                        new_mime = 'image/avif'
                        processed = True
                
                # 处理 GIF 图片（动态）
                elif ext.lower() == '.gif':
                    # 检测是否为动态 GIF
                    if is_animated_gif(image_data):
                        is_animated = True
                        optimized_data = convert_to_avifs(image_data)
                        new_mime = 'image/avif'
                        processed = True
                    else:
                        # 静态 GIF
                        optimized_data = convert_to_avif(image_data, avif_quality)
                        new_mime = 'image/avif'
                        processed = True
                
                # 更新图片数据
                if processed and optimized_data is not None:
                    compressed_size = len(optimized_data)
                    total_compressed_size += compressed_size
                    processed_images += 1
                    
                    # 创建新的 Base64 字符串
                    new_base64 = base64.b64encode(optimized_data).decode('utf-8')
                    img['src'] = f'data:{new_mime};base64,{new_base64}'
                    
                    img_type = "AVIFS" if is_animated else "AVIF"
                    print(f"  Processed: {ext} => {img_type}, "
                          f"Size: {original_size/1024:.1f}KB → {compressed_size/1024:.1f}KB, "
                          f"Reduction: {1 - compressed_size/original_size:.1%}")
        
        # 保存处理后的 HTML
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        
        print(f"  Summary: 处理了 {processed_images} 张图片")
        if processed_images > 0:
            print(f"  总大小: {total_original_size/1024:.1f}KB → {total_compressed_size/1024:.1f}KB")
            print(f"  总体压缩率: {1 - total_compressed_size/total_original_size:.1%}")
        
        return True
    except Exception as e:
        print(f"处理文件 {input_path} 时出错: {str(e)}")
        return False

def copy_non_html_files(src_folder, dst_folder):
    """复制非HTML文件保持目录结构"""
    for root, dirs, files in os.walk(src_folder):
        for file in files:
            src_path = os.path.join(root, file)
            rel_path = os.path.relpath(src_path, src_folder)
            dst_path = os.path.join(dst_folder, rel_path)
            
            # 如果是HTML文件则跳过（后面单独处理）
            if file.lower().endswith(('.html', '.htm')):
                continue
                
            # 创建目标目录并复制文件
            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
            shutil.copy2(src_path, dst_path)

def process_html_folder(src_folder, dst_folder, avif_quality=50):
    """处理文件夹中的所有HTML文件"""
    # 先复制所有非HTML文件
    print("正在复制非HTML文件...")
    copy_non_html_files(src_folder, dst_folder)
    
    # 检查源和目标是否相同
    same_folder = os.path.abspath(src_folder) == os.path.abspath(dst_folder)
    if same_folder:
        print("警告：源文件夹和目标文件夹相同，将不会删除源文件！")
    else:
        print("注意：处理成功后源HTML文件将被删除")
    
    # 处理所有HTML文件
    print("\n开始处理HTML文件...")
    html_files = []
    for root, dirs, files in os.walk(src_folder):
        for file in files:
            if file.lower().endswith(('.html', '.htm')):
                src_path = os.path.join(root, file)
                rel_path = os.path.relpath(src_path, src_folder)
                dst_path = os.path.join(dst_folder, rel_path)
                html_files.append((src_path, dst_path))
    
    total_files = len(html_files)
    print(f"找到 {total_files} 个HTML文件需要处理")
    
    # 记录处理结果
    success_count = 0
    error_count = 0
    deleted_count = 0
    
    for i, (src_path, dst_path) in enumerate(html_files, 1):
        print(f"\n[{i}/{total_files}] 正在处理: {os.path.relpath(src_path, src_folder)}")
        success = process_html_file(src_path, dst_path, avif_quality)
        
        if success:
            success_count += 1
            # 检查目标文件是否存在且大小大于0
            if os.path.exists(dst_path) and os.path.getsize(dst_path) > 0:
                # 如果源和目标不同，则删除源文件
                if not same_folder:
                    try:
                        os.remove(src_path)
                        deleted_count += 1
                        print(f"  已删除源文件: {src_path}")
                    except Exception as e:
                        print(f"  删除源文件失败: {str(e)}")
                else:
                    print("  警告：源和目标相同，跳过删除操作")
            else:
                print(f"  警告：目标文件无效，跳过删除: {dst_path}")
        else:
            error_count += 1
            print(f"  处理失败，保留源文件: {src_path}")
    
    print("\n所有文件处理完成!")
    print(f"成功: {success_count}, 失败: {error_count}, 删除源文件: {deleted_count}")

def get_valid_directory(prompt, default_path):
    """获取有效的目录路径"""
    while True:
        path = input(prompt) or default_path
        path = os.path.normpath(path)  # 规范化路径
        
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

def check_ffmpeg_installed():
    """检查ffmpeg是否安装"""
    try:
        result = subprocess.run(
            ['ffmpeg', '-version'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0 and 'ffmpeg version' in result.stdout:
            return True
    except:
        return False
    return False

if __name__ == "__main__":
    print("=== HTML图片压缩工具 ===")
    print("此工具将处理HTML文件中的内嵌图片")
    print("静态图片转换为AVIF格式，动态图片转换为AVIFS格式（质量50）")
    print("处理成功后，源HTML文件将被删除（除非源和目标文件夹相同）")
    
    # 检查ffmpeg是否安装
    if not check_ffmpeg_installed():
        print("错误: ffmpeg未安装或未添加到系统PATH环境变量")
        print("请从 https://ffmpeg.org/download.html 下载并安装ffmpeg")
        exit(1)
    
    # 设置默认路径 - 已修改为新的默认路径
    default_input = r"d:\Works\B"
    default_output = r"e:\Documents\Literatures\Webpages"
    
    # 获取用户输入
    print(f"\n源文件夹位置 (默认: {default_input})")
    src_folder = get_valid_directory("请输入源文件夹路径（默认为“d:\\Works\\Finisheds\\”）: ", default_input)
    
    print(f"\n目标文件夹位置 (默认: {default_output})")
    dst_folder = get_valid_directory("请输入目标文件夹路径（默认为“d:\\Works\\Finishedx\\”）: ", default_output)
    
    # 使用固定压缩参数
    avif_quality = 50    # AVIF质量 (1-100, 默认50)
    
    # 开始处理
    print(f"\n开始处理: {src_folder} -> {dst_folder}")
    print(f"压缩参数: AVIF质量={avif_quality}")
    
    # 确保ImageMagick可用
    try:
        # 检查ImageMagick版本是否支持AVIF
        version_result = subprocess.run(
            ['magick', '--version'], 
            capture_output=True, 
            text=True,
            check=True
        )
        version_output = version_result.stdout.lower()
        
        # 检查是否支持AVIF
        if 'avif' not in version_output:
            print("警告: 当前ImageMagick版本可能不支持AVIF格式")
            print("建议安装ImageMagick 7.0.25或更高版本")
        
        print("ImageMagick 已安装，开始处理...")
        process_html_folder(src_folder, dst_folder, avif_quality)
    except Exception as e:
        print(f"错误: {str(e)}")
        print("请确保ImageMagick已安装并添加到系统PATH环境变量")
    
    print("处理完成！程序执行完毕，即将退出……")