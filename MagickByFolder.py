# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件夹位置（默认为 d:\\Works\\In\\）与目标文件夹位置（默认为 d:\\Works\\Out\\）。
# 1. 如果源文件格式为 bmp、jpg、jpeg、png 或静态 webp 格式、或静态 avif 格式、静态 heic 格式、静态 heif 格式，则使用 magick 压缩成 avif 格式，使用类似命令：magick convert input.jpg -quality 50 output.avif。
# 2. 如果图片文件格式为 gif 或动态 webp 格式、或动态 avif 格式、动态 heic 格式、动态 heif 格式或 mp4 格式，则使用似命令：ffmpeg -i input.gif -map 0:v -c:v libsvtav1 -crf 32 -preset 5 output.mp4，生成mp4，再生成 avif 动图（ffmpeg -i input-av1.mp4 -c:v copy animation.avif）。
# 生成的文件放到目标文件夹中以“源文件夹的子文件夹”中，保持文件夹及子文件结构。如果生成新文件成功，则删除原始文件。

# 导入模块
import os
import subprocess
import uuid
from PIL import Image

def is_animated_image(filepath):
    """改进版动态图检测（解决NoneType错误）"""
    ext = os.path.splitext(filepath)[1].lower()
    
    try:
        # WebP格式检测
        if ext == '.webp':
            with Image.open(filepath) as img:
                return getattr(img, "is_animated", False)
        
        # 使用Pillow检测其他格式的动画属性
        if ext in ('.gif', '.avif', '.heic', '.heif'):
            with Image.open(filepath) as img:
                return getattr(img, "is_animated", False)
        
        # 其他格式使用快速ImageMagick检测（禁用输出解码）
        result = subprocess.run(
            ['magick', 'identify', '-format', '%n\n', filepath],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,  # 禁用错误输出
            check=True
        )
        frame_count = int(result.stdout.split(b'\n')[0])
        return frame_count > 1
        
    except Exception as e:
        print(f"动态检测异常：{filepath} | 错误：{str(e)}")
        return False

def process_files(src_root, dst_root):
    """改进文件遍历处理"""
    for root, dirs, files in os.walk(src_root):
        for filename in files:
            src_path = os.path.join(root, filename)
            ext = os.path.splitext(filename)[1].lower()
            
            # 构建安全路径
            relative_path = os.path.relpath(root, src_root)
            dst_dir = os.path.normpath(os.path.join(dst_root, relative_path))
            os.makedirs(dst_dir, exist_ok=True)
            
            try:
                # 跳过非目标文件
                if ext not in {'.bmp', '.jpg', '.jpeg', '.png', '.webp', 
                              '.avif', '.heic', '.heif', '.gif', '.mp4'}:
                    continue
                
                # 处理流程
                success = False
                if ext in ('.bmp', '.jpg', '.jpeg', '.png', '.webp', 
                          '.avif', '.heic', '.heif'):
                    animated = is_animated_image(src_path)
                    success = handle_convert(src_path, dst_dir, 'av1' if animated else 'avif')
                elif ext in ('.gif', '.mp4'):
                    success = handle_convert(src_path, dst_dir, 'av1')
                
                # 成功后处理
                if success:
                    os.remove(src_path)
                    print(f"成功处理：{os.path.basename(src_path)}")
                    
            except Exception as e:
                print(f"处理失败：{filename} | 错误：{str(e)}")

def handle_convert(src_path, dst_dir, format_type):
    """改进转换函数（解决编码问题）"""
    base_name = os.path.splitext(os.path.basename(src_path))[0]
    dst_ext = '.avif'  # 最终输出都是avif格式
    dst_path = os.path.join(dst_dir, f"{base_name}{dst_ext}")
    temp_file = None
    temp_mp4 = None
    
    try:
        if format_type == 'avif':
            # 静态图像转换（禁用控制台输出）
            subprocess.run(
                ['magick', src_path, '-quality', '50', dst_path],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW  # Windows专用参数
            )
            return True
        else:
            # 动态内容处理 - 两步转换
            # 第一步：转换为MP4
            temp_mp4 = os.path.join(dst_dir, f"{base_name}_temp_{uuid.uuid4().hex[:8]}.mp4")
            
            # 处理动态WebP：转换为临时GIF
            if src_path.lower().endswith('.webp'):
                temp_file = os.path.join(dst_dir, f"temp_{uuid.uuid4().hex[:8]}.gif")
                subprocess.run(
                    ['magick', src_path, temp_file],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                input_file = temp_file
            else:
                input_file = src_path

            # FFmpeg转换为MP4
            subprocess.run(
                [
                    'ffmpeg', '-hide_banner', '-loglevel', 'error',
                    '-i', input_file, '-map', '0:v',
                    '-vf', 'scale=trunc(iw/2)*2:trunc(ih/2)*2',
                    '-c:v', 'libsvtav1', '-crf', '32', '-preset', '5',
                    '-movflags', '+faststart', '-an', '-sn', '-f', 'mp4', temp_mp4
                ],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            # 第二步：将MP4转换为动态AVIF
            subprocess.run(
                [
                    'ffmpeg', '-hide_banner', '-loglevel', 'error',
                    '-i', temp_mp4, '-c:v', 'copy', dst_path
                ],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            return True
    except subprocess.CalledProcessError as e:
        print(f"转换失败：{os.path.basename(src_path)} | 错误码：{e.returncode}")
        # 清理所有临时文件
        for f in [dst_path, temp_file, temp_mp4]:
            if f and os.path.exists(f):
                try:
                    os.remove(f)
                except:
                    pass
        return False
    finally:
        # 确保清理所有临时文件
        for f in [temp_file, temp_mp4]:
            if f and os.path.exists(f):
                try:
                    os.remove(f)
                except:
                    pass

def main():
    """改进输入处理"""
    default_in = os.path.normpath(r'd:\Works\In')
    default_out = os.path.normpath(r'd:\Works\Out')
    
    src_folder = input(f"请输入源文件夹路径（默认：{default_in}）: ") or default_in
    dst_folder = input(f"请输入目标文件夹路径（默认：{default_out}）: ") or default_out
    
    # 路径规范化
    src_folder = os.path.normpath(src_folder)
    dst_folder = os.path.normpath(dst_folder)
    
    # 检查路径是否存在
    if not os.path.exists(src_folder):
        print(f"错误：源文件夹不存在 - {src_folder}")
        return
    
    # 开始处理
    print("\n开始处理文件...")
    process_files(src_folder, dst_folder)
    print("\n全部文件处理完成")

if __name__ == "__main__":
    main()
    input("按回车键退出...")