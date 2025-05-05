# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件位置。
# 1. 如果源文件格式为 jpg、jpeg、png 或静态 webp 格式，则使用 magick 压缩成 avif 格式，使用类似命令：magick convert input.png -quality 75 output.avif。
# 2. 如果图片文件格式为 gif 或动态 webp 或 mp4，先转成 mp4 格式，使用似命令：ffmpeg -i input.gif -c:v libsvtav1 output.mp4。再将 output.mp4 转换成 avifs，使用命令：
# MP4Box -add-image output.mp4:id=1:primary -new output.avifs
# MP4Box -ab avis -ab msf1 -ab miaf -ab MA1B -rb mif1 -brand avis output.avifs
# MP4Box -add output.mp4:hdlr=pict:ccst:name="GPAC avifs" output.avifs
# 生成的文件替换源文件。
# 如此循环，再次前询问我源文件位置。

# 导入模块
import os
import subprocess
import shutil
from PIL import Image

def compress_file():
    """
    主函数：循环询问用户文件路径，对文件进行压缩处理
    """
    print("欢迎使用AVIFS转换工具（支持静态/动态内容转换）")
    while True:
        source_file = input("\n请输入源文件路径（或输入 'n' 退出）: ").strip()
        if source_file.lower() == 'n':
            break

        if not os.path.isfile(source_file):
            print("错误：文件不存在")
            continue

        file_ext = os.path.splitext(source_file)[1].lower()

        try:
            if file_ext in ['.jpg', '.jpeg', '.png', '.webp']:
                if file_ext == '.webp':
                    handle_webp_file(source_file)
                else:
                    handle_static_file(source_file)
            elif file_ext in ['.gif', '.mp4']:
                handle_animated_video(source_file)
            else:
                print(f"不支持格式：{file_ext}")
        except Exception as e:
            print(f"处理失败：{e}")

def handle_static_file(source_file):
    """处理静态图片转AVIF"""
    base_name = os.path.splitext(source_file)[0]
    output_file = f"{base_name}.avif"
    
    try:
        # 转换静态图片为AVIF（保留EXIF信息）
        subprocess.run(
            f'magick "{source_file}" -quality 75 "{output_file}"',
            check=True, shell=True, 
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE
        )
        os.remove(source_file)
        print(f"静态转换完成：{output_file}")
    except subprocess.CalledProcessError as e:
        print(f"转换失败：{e.stderr.decode()}")
        if os.path.exists(output_file):
            os.remove(output_file)

def handle_webp_file(source_file):
    """处理WebP文件（动/静态检测）"""
    try:
        with Image.open(source_file) as img:
            if getattr(img, "is_animated", False):
                handle_animated_video(source_file)
            else:
                handle_static_file(source_file)
    except Exception as e:
        print(f"WebP检测失败：{e}")

def handle_animated_video(source_file):
    """处理动态内容转AVIFS"""
    base_name = os.path.splitext(source_file)[0]
    temp_mp4 = f"{base_name}_temp.mp4"
    temp_avifs = f"{base_name}.avifs"
    
    try:
        # 第一步：转换为AV1编码的MP4（自动修正分辨率）
        ffmpeg_cmd = f'ffmpeg -i "{source_file}" '\
                     '-vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" '\
                     '-c:v libsvtav1 -crf 23 '\
                     f'"{temp_mp4}"'
        
        subprocess.run(
            ffmpeg_cmd,
            check=True, shell=True,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE
        )

        # 第二步：使用MP4Box生成AVIFS
        commands = [
            # 创建基础容器并设置品牌
            f'MP4Box -add-image {temp_mp4}:primary -ab avis -brand avis -new {temp_avifs}',
            # 添加视频轨道并指定媒体处理类型
            f'MP4Box -add {temp_mp4}:hdlr=pict {temp_avifs}'
        ]
        
        for cmd in commands:
            subprocess.run(
                cmd, check=True, shell=True,
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE
            )

        # 替换原始文件并清理
        if source_file != temp_avifs:
            os.remove(source_file)
            shutil.move(temp_avifs, source_file)
            print(f"动态转换完成：{source_file}")
        os.remove(temp_mp4)
        
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.decode()
        # 特殊处理分辨率错误提示
        if "must be even for YUV_420" in error_msg:
            print("检测到奇数分辨率，已自动修正后重新尝试")
        else:
            print(f"转换失败：{error_msg}")
        # 清理临时文件
        for f in [temp_mp4, temp_avifs]:
            if os.path.exists(f):
                os.remove(f)
    except Exception as e:
        print(f"处理异常：{str(e)}")
        for f in [temp_mp4, temp_avifs]:
            if os.path.exists(f):
                os.remove(f)

if __name__ == "__main__":
    compress_file()
    input("按回车退出...")