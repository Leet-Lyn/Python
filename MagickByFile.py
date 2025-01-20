# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件位置。
# 1. 如果源文件格式为 jpg、jpeg、png 或静态 webp 格式，则使用 magick 压缩成 jpg 格式，使用类似命令：magick convert input.png -quality 75 output.jpg。
# 2. 如果图片文件格式为 gif 或动态 webp 或 mp4，则使用 magick 压缩成 gif 格式，类似命令：magick convert input.webp -fuzz 5% -quality 75 -layers Optimize output.gif。
# 生成的文件替换源文件。
# 如此循环，再次前询问我源文件位置。

# 导入模块
# 导入模块
import os
import subprocess
import shutil  # 用于替换文件
from PIL import Image  # 用于检测 WebP 文件是否为动态图

def compress_file():
    """
    主函数：循环询问用户文件路径，对文件进行压缩处理。
    """
    while True:
        # 提示用户输入文件路径
        source_file = input("请输入源文件路径（或输入 'n' 退出程序）: ").strip()
        if source_file.lower() == 'n':  # 用户选择退出
            break

        # 验证文件路径是否有效
        if not os.path.isfile(source_file):
            print("无效的文件路径，请重新输入。")
            continue

        # 获取文件扩展名
        file_ext = os.path.splitext(source_file)[1].lower()

        try:
            if file_ext in ['.jpg', '.jpeg', '.png']:  # 静态图片格式
                handle_static_image(source_file)

            elif file_ext == '.webp':  # WebP 文件
                handle_webp_file(source_file)

            elif file_ext in ['.gif', '.mp4']:  # 动态图片或视频格式
                handle_animated_or_video(source_file)

            else:
                print(f"不支持的文件格式：{file_ext}。请提供有效的图片或视频文件。")
        except Exception as e:
            print(f"处理文件时出错：{source_file}，错误信息：{e}")

    print("程序已退出。")

def handle_static_image(source_file):
    """
    处理静态图片，将其压缩为 JPG 格式。
    """
    output_file = f"{os.path.splitext(source_file)[0]}.jpg"
    try:
        # 使用 magick 命令压缩图片
        subprocess.run(f'magick "{source_file}" -quality 75 "{output_file}"', check=True, shell=True)
        
        # 替换源文件，并更新后缀名为 .jpg
        if source_file != output_file:
            os.remove(source_file)  # 删除原始文件
        shutil.move(output_file, source_file)  # 将新文件重命名为源文件
        print(f"{source_file} 已成功压缩为 JPG 格式并替换。")
    except subprocess.CalledProcessError as e:
        print(f"压缩文件 {source_file} 时失败，错误信息：{e}")

def handle_webp_file(source_file):
    """
    处理 WebP 文件，检测是否为动态图，动态 WebP 转换为 GIF，静态 WebP 压缩为 JPG。
    """
    try:
        # 使用 PIL 检测 WebP 文件是否为动态图
        with Image.open(source_file) as img:
            is_animated = getattr(img, "is_animated", False)

        if is_animated:  # 动态 WebP 转换为 GIF
            output_file = f"{os.path.splitext(source_file)[0]}.gif"
            subprocess.run(f'magick "{source_file}" -fuzz 5% -quality 75 -layers Optimize "{output_file}"', check=True, shell=True)
            
            # 替换源文件，并更新后缀名为 .gif
            if source_file != output_file:
                os.remove(source_file)  # 删除原始文件
            shutil.move(output_file, source_file)  # 将新文件重命名为源文件
            print(f"{source_file} 已成功转换为 GIF 格式并替换。")
        else:  # 静态 WebP 压缩为 JPG
            handle_static_image(source_file)
    except Exception as e:
        print(f"处理 WebP 文件 {source_file} 时出错，错误信息：{e}")

def handle_animated_or_video(source_file):
    """
    处理动态图片（GIF）或视频文件（MP4），压缩为 GIF 格式。
    """
    output_file = f"{os.path.splitext(source_file)[0]}.gif"
    try:
        # 使用 magick 命令处理 GIF 或视频
        subprocess.run(f'magick "{source_file}" -fuzz 5% -quality 75 -layers Optimize "{output_file}"', check=True, shell=True)
        
        # 替换源文件，并更新后缀名为 .gif
        if source_file != output_file:
            os.remove(source_file)  # 删除原始文件
        shutil.move(output_file, source_file)  # 将新文件重命名为源文件
        print(f"{source_file} 已成功转换为 GIF 格式并替换。")
    except subprocess.CalledProcessError as e:
        print(f"处理文件 {source_file} 时失败，错误信息：{e}")

if __name__ == "__main__":
    compress_file()
    print("所有文件处理完成！")
    input("按回车键退出...")