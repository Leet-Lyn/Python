# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件位置。
# 1. 如果源文件格式为 bmp、jpg、jpeg、png 或静态 webp 格式、或静态 avif 格式、静态 heic 格式、静态 heif 格式，则使用 magick 压缩成 avif 格式，使用类似命令：magick convert input.jpg -quality 50 output.avif。
# 2. 如果图片文件格式为 gif 或动态 webp 格式、或动态 avif 格式、动态 heic 格式、动态 heif 格式或 mp4 格式，则使用似命令：ffmpeg -i input.gif -map 0:v -c:v libsvtav1 -crf 32 -preset 5 output.mp4
# 生成的文件替换源文件。
# 如此循环，再次前询问我源文件位置。

# 导入模块
import os
import subprocess
from PIL import Image

def is_animated_image(filepath):
    """
    检测图像是否为动态图（支持 WebP/AVIF/HEIC/HEIF）
    返回：True=动态图 False=静态图
    """
    ext = os.path.splitext(filepath)[1].lower()
    
    try:
        # WebP格式检测
        if ext == '.webp':
            with Image.open(filepath) as img:
                return getattr(img, "is_animated", False)
        
        # 其他格式使用 ImageMagick 检测帧数
        result = subprocess.run(
            ['magick', 'identify', filepath],  # 使用列表参数避免路径问题
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        
        # 检查命令执行结果
        if result.returncode != 0:
            print(f"动态检测失败：{filepath} | 错误：{result.stderr}")
            return False
            
        # 计算输出的帧数
        frame_count = len(result.stdout.strip().split('\n'))
        return frame_count > 1
        
    except Exception as e:
        print(f"动态检测异常：{filepath} | 错误：{str(e)}")
        return False

def compress_file():
    """
    主函数：循环处理文件转换
    """
    # print("=== 现代化媒体压缩工具 ===")
    # print("支持格式：")
    # print("- 静态图：bmp/jpg/png/webp/avif/heic/heif → AVIF")
    # print("- 动态图：gif/webp/avif/heic/heif/mp4 → AV1 视频")
    
    while True:
        source_file = input("\n请输入文件路径（输入 n 退出）: ").strip()
        if source_file.lower() == 'n':
            break

        if not os.path.isfile(source_file):
            print("文件不存在，请重新输入。")
            continue

        ext = os.path.splitext(source_file)[1].lower()
        
        try:
            # 静态图像处理分支
            if ext in ('.bmp', '.jpg', '.jpeg', '.png', '.webp', '.avif', '.heic', '.heif'):
                if is_animated_image(source_file):
                    convert_to_av1(source_file)
                else:
                    convert_to_avif(source_file)
            
            # 视频/动态图处理分支
            elif ext in ('.gif', '.mp4'):
                convert_to_av1(source_file)
            
            else:
                print(f"不支持的格式：{ext}")

        except Exception as e:
            print(f"处理失败：{source_file} | 错误：{str(e)}")

    print("\n程序已退出。")

def convert_to_avif(source_file):
    """将静态图像转换为 AVIF 格式"""
    output_file = os.path.splitext(source_file)[0] + ".avif"
    
    try:
        # 使用 ImageMagick 转换
        subprocess.run(
            ['magick', source_file, '-quality', '50', output_file],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        # 替换原始文件
        os.remove(source_file)
        print(f"成功生成：{output_file}")
    except subprocess.CalledProcessError as e:
        print(f"AVIF 转换失败：{e}")
        if os.path.exists(output_file):
            os.remove(output_file)

def convert_to_av1(source_file):
    """将动态内容转换为AV1视频"""
    original_source = source_file  # 保存原始文件路径
    output_file = os.path.splitext(source_file)[0] + ".mp4"
    temp_file = None
    
    try:
        # 处理 WebP 文件时生成临时文件
        if original_source.lower().endswith('.webp'):
            temp_dir = os.path.dirname(original_source)
            base_name = os.path.basename(original_source).rsplit('.', 1)[0]
            
            import uuid
            temp_file = os.path.join(temp_dir, f"{base_name}_temp_{uuid.uuid4().hex[:6]}.gif")
            
            # 转换 WebP 到 GIF
            subprocess.run(
                ['magick', original_source, temp_file],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            source_file = temp_file  # 后续处理使用临时文件

        # 执行视频转换
        subprocess.run(
            [
                'ffmpeg', '-hide_banner', '-i', source_file,
                '-map', '0:v', '-vf', 'scale=trunc(iw/2)*2:trunc(ih/2)*2',
                '-c:v', 'libsvtav1', '-crf', '32', '-preset', '5',
                '-movflags', '+faststart', '-an', '-sn', '-f', 'mp4', output_file
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        # 清理文件
        if original_source != output_file and os.path.exists(original_source):
            os.remove(original_source)
        if temp_file and os.path.exists(temp_file):
            os.remove(temp_file)
        print(f"转换完成，原始文件已删除: {original_source}")

    except subprocess.CalledProcessError as e:
        print(f"转换失败: {str(e)}")
        # 异常时清理残留文件
        for f in [output_file, temp_file]:
            if f and os.path.exists(f):
                os.remove(f)

if __name__ == "__main__":
    compress_file()
    input("按回车键退出...")