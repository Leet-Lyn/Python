# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件夹位置（默认为 d:\\Works\\In\\）与目标文件夹位置（默认为 d:\\Works\\Out\\）。
# 遍历源文件夹内所有子文件夹中的图片或视频文件（jpg、jpeg、png、gif、webp、mp4 格式）。
# 1. 如果图片文件格式为 jpg、jpeg、png 或静态 webp 格式，则使用 magick 压缩成 jpg 格式，使用类似命令：magick convert input.png -quality 75 output.jpg。
# 2. 如果图片文件格式为 gif 或动态 webp 或 mp4，则使用 magick 压缩成 gif 格式，类似命令：magick convert input.webp -fuzz 5% -quality 75 -layers Optimize output.gif。
# 生成的文件放到目标文件夹中以“源文件夹的子文件夹”中，保持文件夹及子文件结构。

# 导入模块
# 导入必要模块
import os
import subprocess
from PIL import Image  # 用于检测 WebP 文件是否为动态图

# 函数：获取文件夹路径
def ask_folder_location(prompt, default_folder):
    """
    提示用户输入文件夹路径，按回车使用默认路径。
    :param prompt: 提示信息
    :param default_folder: 默认路径
    :return: 文件夹路径
    """
    folder_path = input(f"{prompt}（默认路径: {default_folder}）: ").strip() or default_folder
    while not os.path.isdir(folder_path):
        print("输入的文件夹不存在，请重新输入。")
        folder_path = input(f"{prompt}（默认路径: {default_folder}）: ").strip() or default_folder
    return folder_path

# 函数：压缩静态图片为 JPG
def compress_to_jpg(input_path, output_path):
    """
    使用 magick 压缩静态图片为 JPG 格式。
    :param input_path: 输入文件路径
    :param output_path: 输出文件路径
    """
    try:
        subprocess.run(['magick', 'convert', input_path, '-quality', '75', output_path], check=True)
        print(f"已成功压缩为 JPG: {input_path} -> {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"压缩失败: {input_path}，错误: {e}")

# 函数：压缩动态图或视频为 GIF
def compress_to_gif(input_path, output_path):
    """
    使用 magick 压缩动态图或视频为 GIF 格式。
    :param input_path: 输入文件路径
    :param output_path: 输出文件路径
    """
    try:
        subprocess.run(['magick', 'convert', input_path, '-fuzz', '5%', '-quality', '75', '-layers', 'Optimize', output_path], check=True)
        print(f"已成功压缩为 GIF: {input_path} -> {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"压缩失败: {input_path}，错误: {e}")

# 函数：判断 WebP 文件是否为动态图
def is_animated_webp(file_path):
    """
    检查 WebP 文件是否为动态图。
    :param file_path: WebP 文件路径
    :return: 布尔值，True 表示是动态图
    """
    try:
        with Image.open(file_path) as img:
            return getattr(img, "is_animated", False)
    except Exception as e:
        print(f"无法检查是否为动态图: {file_path}，错误: {e}")
        return False

# 获取源文件夹和目标文件夹路径
source_folder = ask_folder_location("请输入源文件夹位置", "d:\\Works\\In\\")
target_folder = ask_folder_location("请输入目标文件夹位置", "d:\\Works\\Out\\")

# 遍历源文件夹及其子文件夹中的文件
for root, _, files in os.walk(source_folder):
    for file in files:
        # 获取文件路径和目标路径
        file_path = os.path.join(root, file)
        relative_path = os.path.relpath(root, source_folder)
        output_folder = os.path.join(target_folder, relative_path)
        os.makedirs(output_folder, exist_ok=True)
        output_file_base = os.path.splitext(file)[0]
        
        # 根据文件类型选择处理方式
        if file.lower().endswith(('.jpg', '.jpeg', '.png')):
            output_file = os.path.join(output_folder, f"{output_file_base}.jpg")
            compress_to_jpg(file_path, output_file)
        
        elif file.lower().endswith('.webp'):
            if is_animated_webp(file_path):
                output_file = os.path.join(output_folder, f"{output_file_base}.gif")
                compress_to_gif(file_path, output_file)
            else:
                output_file = os.path.join(output_folder, f"{output_file_base}.jpg")
                compress_to_jpg(file_path, output_file)
        
        elif file.lower().endswith(('.gif', '.mp4')):
            output_file = os.path.join(output_folder, f"{output_file_base}.gif")
            compress_to_gif(file_path, output_file)
        
        # 删除原文件
        try:
            os.remove(file_path)
            print(f"已删除源文件: {file_path}")
        except Exception as e:
            print(f"删除文件失败: {file_path}，错误: {e}")

print("所有文件处理完成！")
input("按回车键退出...")