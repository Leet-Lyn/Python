# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件夹位置（默认为 d:\\Works\\In\\）与目标文件夹位置（默认为 d:\\Works\\Out\\）。
# 1. 如果源文件格式为 bmp、jpg、jpeg、png 或静态 webp 格式、或静态 avif 格式、静态 heic 格式、静态 heif 格式，则使用 magick 压缩成 avif 格式，使用类似命令：magick convert input.jpg -quality 75 output.avif。
# 2. 如果图片文件格式为 gif 或动态 webp 格式、或动态 avif 格式、动态 heic 格式、动态 heif 格式或 mp4 格式，则使用似命令：ffmpeg -i input.gif -map 0:v -c:v libsvtav1 -crf 32 -preset 5 output.mp4
# 生成的文件放到目标文件夹中以“源文件夹的子文件夹”中，保持文件夹及子文件结构。如果生成新文件成功，则删除原始文件。

# 导入模块
import os
import subprocess
from PIL import Image
import shutil

def is_animated_image(filepath):
    """检测图像是否为动态图（支持 WebP/AVIF/HEIC/HEIF）"""
    ext = os.path.splitext(filepath)[1].lower()
    
    try:
        # WebP格式检测
        if ext == '.webp':
            with Image.open(filepath) as img:
                return getattr(img, "is_animated", False)
        
        # 其他格式使用ImageMagick检测帧数（修复编码问题）
        result = subprocess.run(
            f'magick identify "{filepath}"',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            text=True,
            encoding='utf-8',
            errors='ignore'  # 忽略解码错误
        )
        
        # 检查命令执行是否成功
        if result.returncode != 0:
            print(f"动态检测失败：{filepath} | 错误：{result.stderr}")
            return False
            
        # 计算输出的帧数
        frame_count = len(result.stdout.strip().split('\n'))
        return frame_count > 1
    except Exception as e:
        print(f"动态检测失败：{filepath} | 错误：{str(e)}")
        return False

def process_files(src_root, dst_root):
    """遍历并处理所有文件"""
    for root, dirs, files in os.walk(src_root):
        for filename in files:
            src_path = os.path.join(root, filename)
            ext = os.path.splitext(filename)[1].lower()
            
            # 构建目标路径
            relative_path = os.path.relpath(root, src_root)
            dst_dir = os.path.join(dst_root, relative_path)
            os.makedirs(dst_dir, exist_ok=True)
            
            try:
                # 跳过非媒体文件
                if ext not in ('.bmp', '.jpg', '.jpeg', '.png', '.webp', 
                              '.avif', '.heic', '.heif', '.gif', '.mp4'):
                    continue
                
                # 静态图像处理分支
                if ext in ('.bmp', '.jpg', '.jpeg', '.png', '.webp', 
                          '.avif', '.heic', '.heif'):
                    if is_animated_image(src_path):
                        handle_convert(src_path, dst_dir, 'av1')
                    else:
                        handle_convert(src_path, dst_dir, 'avif')
                
                # 视频/动态图处理分支
                elif ext in ('.gif', '.mp4'):
                    handle_convert(src_path, dst_dir, 'av1')
                
                # 转换成功后删除源文件
                os.remove(src_path)
                print(f"成功处理并删除原始文件：{src_path}")

            except Exception as e:
                print(f"处理失败：{src_path} | 错误：{str(e)}")

def handle_convert(src_path, dst_dir, format_type):
    """根据类型执行转换（增加编码处理）"""
    filename = os.path.splitext(os.path.basename(src_path))[0]
    dst_path = os.path.join(dst_dir, f"{filename}.{'avif' if format_type == 'avif' else 'mp4'}")

    try:
        if format_type == 'avif':
            subprocess.run(
                f'magick "{src_path}" -quality 75 "{dst_path}"',
                check=True,
                shell=True,
                encoding='utf-8',
                errors='ignore'
            )
        else:
            temp_file = None
            try:
                # 处理动态WebP需要转换为GIF
                if src_path.lower().endswith('.webp'):
                    temp_file = os.path.join(dst_dir, f"temp_{os.urandom(4).hex()}.gif")
                    subprocess.run(
                        f'magick "{src_path}" "{temp_file}"',
                        check=True, 
                        shell=True,
                        encoding='utf-8',
                        errors='ignore'
                    )
                    src_path = temp_file

                # 执行视频转换
                subprocess.run(
                    f'ffmpeg -hide_banner -i "{src_path}" '
                    f'-map 0:v -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" '
                    f'-c:v libsvtav1 -crf 32 -preset 5 '
                    f'-movflags +faststart -an -sn -f mp4 "{dst_path}"',
                    check=True,
                    shell=True,
                    encoding='utf-8',
                    errors='ignore'
                )
            finally:
                if temp_file and os.path.exists(temp_file):
                    os.remove(temp_file)
                    
    except subprocess.CalledProcessError as e:
        print(f"转换失败：{src_path} | 错误码：{e.returncode} | 输出：{e.output}")
        if os.path.exists(dst_path):
            os.remove(dst_path)
        raise

def main():
    """主函数"""
    src_folder = input("请输入源文件夹路径（默认为d:\\Works\\In\\）: ") or "d:\\Works\\In\\"
    dst_folder = input("请输入目标文件夹路径（默认为d:\\Works\\Out\\）: ") or "d:\\Works\\Out\\"

    # 标准化路径格式
    src_folder = os.path.normpath(src_folder)
    dst_folder = os.path.normpath(dst_folder)
    
    # 创建目标根目录
    os.makedirs(dst_folder, exist_ok=True)
    
    # 开始处理文件
    process_files(src_folder, dst_folder)
    print("\n全部文件处理完成")

if __name__ == "__main__":
    main()
    input("按回车键退出...")