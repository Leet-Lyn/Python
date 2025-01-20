# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件夹位置与目标文件夹位置。
# 遍历源文件夹位置中所有音频文件（mp3、m4a、wma、ogg、aac、ac3、rm、wav）。
# 使用 ffmpeg 压缩。
# 音频参数为：aac 格式，遍历每个音轨，质量模式。q=0.36。
# 生成的文件重新用 mkvmerge 再生成同名文件到 目标文件夹位置。   

# 导入模块
import os
import subprocess

# 函数用于询问用户文件夹位置
def ask_folder_location(prompt, default_folder):
    """
    提示用户输入文件夹路径，如果按回车则使用默认路径。
    :param prompt: 提示信息
    :param default_folder: 默认文件夹路径
    :return: 有效的文件夹路径
    """
    folder_path = input(f"{prompt}（按回车键使用默认位置 {default_folder}）: ").strip() or default_folder
    while not os.path.isdir(folder_path):
        print("文件夹不存在，请重新输入。")
        folder_path = input(f"{prompt}（按回车键使用默认位置 {default_folder}）: ").strip() or default_folder
    return folder_path

# 获取源文件夹和目标文件夹位置
source_folder = ask_folder_location("请输入源文件夹位置", "d:\\Works\\In\\")
target_folder = ask_folder_location("请输入目标文件夹位置", "d:\\Works\\Out\\")

# 支持的音频格式
audio_formats = (".mp3", ".m4a", ".wma", ".ogg", ".aac", ".ac3", ".rm", ".wav")

# 确保目标文件夹存在
os.makedirs(target_folder, exist_ok=True)

def compress_audio(source_path, target_folder):
    """
    压缩音频文件并保存到目标文件夹。
    :param source_path: 源音频文件路径
    :param target_folder: 目标文件夹路径
    """
    # 获取文件名（不含扩展名）和扩展名
    file_name, _ = os.path.splitext(os.path.basename(source_path))
    compressed_file_path = os.path.join(target_folder, f"{file_name}.aac")
    
    # 构建 ffmpeg 命令
    ffmpeg_command = [
        "ffmpeg", "-i", source_path,
        "-c:a", "aac", "-q:a", "0.36",
        "-map", "0:a",  # 仅保留音频流
        compressed_file_path
    ]
    
    print(f"正在压缩音频: {source_path}")
    try:
        subprocess.run(ffmpeg_command, check=True)
        print(f"压缩完成: {compressed_file_path}")
    except subprocess.CalledProcessError as e:
        print(f"音频压缩失败: {source_path}")
        print(f"错误信息: {e}")
        return

def remux_audio(compressed_file_path, final_file_path):
    """
    使用 mkvmerge 对音频进行封装。
    :param compressed_file_path: 已压缩的音频文件路径
    :param final_file_path: 最终封装的音频文件路径
    """
    # 构建 mkvmerge 命令
    mkvmerge_command = [
        "mkvmerge", "-o", final_file_path, compressed_file_path
    ]
    
    print(f"正在封装音频: {compressed_file_path}")
    try:
        subprocess.run(mkvmerge_command, check=True)
        print(f"封装完成: {final_file_path}")
        os.remove(compressed_file_path)  # 删除临时的压缩文件
    except subprocess.CalledProcessError as e:
        print(f"音频封装失败: {compressed_file_path}")
        print(f"错误信息: {e}")

# 遍历源文件夹中的所有音频文件
for root, dirs, files in os.walk(source_folder):
    for file in files:
        if file.lower().endswith(audio_formats):  # 忽略文件名大小写
            source_path = os.path.join(root, file)
            compressed_file_path = os.path.join(target_folder, f"{os.path.splitext(file)[0]}.aac")
            final_file_path = os.path.join(target_folder, f"{os.path.splitext(file)[0]}.mkv")
            
            # 压缩音频并重新封装
            compress_audio(source_path, target_folder)
            if os.path.exists(compressed_file_path):
                remux_audio(compressed_file_path, final_file_path)

print("所有音频处理完成！")
input("按回车键退出...")