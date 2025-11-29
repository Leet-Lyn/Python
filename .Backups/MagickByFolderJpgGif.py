# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件夹位置（默认为 d:\\Works\\In\\）与目标文件夹位置（默认为 d:\\Works\\Out\\）。
# 遍历源文件夹内所有子文件夹中的图片或视频文件（jpg、jpeg、png、gif、webp、mp4 格式）。
# 1. 如果图片文件格式为 jpg、jpeg、png 或静态 webp 格式，则使用 magick 压缩成 jpg 格式，使用类似命令：magick convert input.png -quality 75 output.jpg。
# 2. 如果图片文件格式为 gif 或动态 webp 或 mp4，则使用 magick 压缩成 gif 格式，类似命令：magick convert input.webp -fuzz 5% -quality 75 -layers Optimize output.gif。
# 生成的文件放到目标文件夹中以“源文件夹的子文件夹”中，保持文件夹及子文件结构。

# 导入模块
import os
import subprocess
from PIL import Image  # 用于检测 WebP 文件是否为动态图

# 设置默认编码为 UTF-8
# import sys
# sys.stdout.reconfigure(encoding='utf-8')
# sys.stderr.reconfigure(encoding='utf-8')

def ask_folder_location(prompt, default_folder):
    """
    提示用户输入文件夹路径，若为空则返回默认路径。
    """
    folder_path = input(f"{prompt}（默认路径: {default_folder}）: ").strip() or default_folder
    while not os.path.isdir(folder_path):  # 验证路径是否存在
        print("输入的文件夹不存在，请重新输入。")
        folder_path = input(f"{prompt}（默认路径: {default_folder}）: ").strip() or default_folder
    return folder_path

def compress_to_jpg(input_path, output_path):
    """
    使用 magick 压缩图片为 JPG 格式。
    """
    try:
        subprocess.run(
            f'magick "{input_path}" -quality 75 "{output_path}"',
            check=True, shell=True
        )
        print(f"已成功压缩为 JPG: {input_path} -> {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"压缩失败: {input_path}，错误: {e}")

def compress_to_gif(input_path, output_path):
    """
    使用 magick 压缩动态图片或视频为 GIF 格式。
    """
    try:
        subprocess.run(
            f'magick "{input_path}" -fuzz 5% -quality 75 -layers Optimize "{output_path}"',
            check=True, shell=True
        )
        print(f"已成功压缩为 GIF: {input_path} -> {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"压缩失败: {input_path}，错误: {e}")

def is_animated_webp(file_path):
    """
    检测 WebP 文件是否为动态图。
    """
    try:
        with Image.open(file_path) as img:
            return getattr(img, "is_animated", False)
    except Exception as e:
        print(f"无法检查是否为动态图: {file_path}，错误: {e}")
        return False

# 主程序逻辑
def main():
    # 获取源文件夹和目标文件夹路径
    source_folder = ask_folder_location("请输入源文件夹位置", "d:\\Works\\In\\")
    target_folder = ask_folder_location("请输入目标文件夹位置", "d:\\Works\\Out\\")

    # 遍历源文件夹及其子文件夹
    for root, _, files in os.walk(source_folder):
        for file in files:
            file_path = os.path.normpath(os.path.join(root, file))  # 源文件路径
            relative_path = os.path.relpath(root, source_folder)  # 相对路径
            output_folder = os.path.normpath(os.path.join(target_folder, relative_path))  # 保持子文件夹结构
            os.makedirs(output_folder, exist_ok=True)  # 创建目标文件夹
            output_file_base = os.path.splitext(file)[0]  # 文件名（无后缀）

            try:
                # 处理不同格式的文件
                if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    # 压缩静态图片为 JPG
                    output_file = os.path.join(output_folder, f"{output_file_base}.jpg")
                    compress_to_jpg(file_path, output_file)
                
                elif file.lower().endswith('.webp'):
                    if is_animated_webp(file_path):
                        # 动态 WebP 转换为 GIF
                        output_file = os.path.join(output_folder, f"{output_file_base}.gif")
                        compress_to_gif(file_path, output_file)
                    else:
                        # 静态 WebP 压缩为 JPG
                        output_file = os.path.join(output_folder, f"{output_file_base}.jpg")
                        compress_to_jpg(file_path, output_file)
                
                elif file.lower().endswith(('.gif', '.mp4')):
                    # 压缩 GIF 或视频为 GIF
                    output_file = os.path.join(output_folder, f"{output_file_base}.gif")
                    compress_to_gif(file_path, output_file)
                
                # 删除原文件
                os.unlink(file_path)
                print(f"已删除源文件: {file_path}")
            
            except Exception as e:
                print(f"处理文件时出错: {file_path}，错误: {e}")

    print("所有文件处理完成！")
    input("按回车键退出...")

if __name__ == "__main__":
    main()