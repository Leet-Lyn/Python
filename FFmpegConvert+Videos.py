# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件夹位置（默认“d:\\Works\\In\\”）与目标文件夹位置（默认“d:\\Works\\Out\\”）。
# 遍历源文件夹及其子文件夹位置中所有视频文件（mkv、avi、f4v、flv、ts、mpeg、mpg、rm、rmvb、asf、wmv、mov、webm、mp4、ogv、ogm、ogg）。
# 使用 ffmpeg 压缩，类似命令：ffmpeg -i input.mkv -map 0 -c:v libsvtav1 -crf 32 -preset 5 -c:a aac -q:a 0.64 -c:s copy output.mkv。
# 视频参数为：av1 格式，Const.Qualty: Quality=32，Preset=5。音频参数为：aac 格式，遍历每个音轨，质量模式。q=0.64。字幕保持不变。
# 生成的文件重新用 mkvmerge 再生成同名文件到目标文件夹位置，文件夹结构保持一致。   

# 导入模块
import os
import subprocess

# 函数用于询问用户文件夹位置
def ask_folder_location(prompt, default_folder):
    """
    提示用户输入文件夹路径，如果按回车则使用默认路径。
    :param prompt: 提示信息
    :param default_folder: 默认文件夹路径
    :return: 文件夹路径
    """
    folder_path = input(f"{prompt}（按回车键使用默认位置 {default_folder}）: ").strip() or default_folder
    while not os.path.isdir(folder_path):
        print("文件夹不存在，请重新输入。")
        folder_path = input(f"{prompt}（按回车键使用默认位置 {default_folder}）: ").strip() or default_folder
    return folder_path

# 获取源文件夹和目标文件夹位置
source_folder = ask_folder_location("请输入源文件夹位置（默认“d:\\Works\\In\\”）", "d:\\Works\\In\\")
target_folder = ask_folder_location("请输入目标文件夹位置（默认“d:\\Works\\Out\\”）", "d:\\Works\\Out\\")

# 支持的文件格式
video_formats = (".mkv", ".avi", ".f4v", ".flv", ".ts", ".mpeg", ".mpg", ".rm", ".rmvb", ".asf", ".wmv", ".mov", ".webm", ".mp4", ".ogv", ".ogm", ".ogg")

# 确保目标文件夹存在
os.makedirs(target_folder, exist_ok=True)

def compress_and_remux_video(source_path, target_folder, relative_path):
    """
    压缩视频并重新封装到目标文件夹，保持目录结构。
    :param source_path: 源视频文件路径
    :param target_folder: 目标文件夹路径
    :param relative_path: 相对于源文件夹的路径
    """
    # 获取文件名和扩展名
    file_name, _ = os.path.splitext(os.path.basename(source_path))
    
    # 在目标文件夹中创建相同的目录结构
    target_subfolder = os.path.join(target_folder, relative_path)
    os.makedirs(target_subfolder, exist_ok=True)
    
    temp_output_path = os.path.join(target_subfolder, f"{file_name}_temp.mkv")
    final_output_path = os.path.join(target_subfolder, f"{file_name}.mkv")
    
    # 构建 ffmpeg 命令
    ffmpeg_command = [
        "ffmpeg", "-i", source_path,
        "-c:v", "libsvtav1", "-preset", "5", "-crf", "32",
        "-c:a", "aac", "-q:a", "0.64",
        "-c:s", "copy",
        "-map", "0",
        temp_output_path
    ]

    print(f"正在压缩视频: {source_path}")
    try:
        subprocess.run(ffmpeg_command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"ffmpeg 压缩失败: {source_path}")
        print(f"错误信息: {e}")
        return

    # 构建 mkvmerge 命令
    mkvmerge_command = [
        "mkvmerge", "-o", final_output_path, temp_output_path
    ]

    print(f"正在重新封装视频: {temp_output_path}")
    try:
        subprocess.run(mkvmerge_command, check=True)
        os.remove(temp_output_path)  # 删除临时文件
        
        # 检查最终输出文件是否存在且大小合理
        if os.path.exists(final_output_path) and os.path.getsize(final_output_path) > 0:
            # 删除源文件
            os.remove(source_path)
            print(f"已删除源文件: {source_path}")
        else:
            print(f"警告: 最终输出文件可能有问题，保留源文件: {source_path}")
            return
            
    except subprocess.CalledProcessError as e:
        print(f"mkvmerge 封装失败: {temp_output_path}")
        print(f"错误信息: {e}")
        return
    except Exception as e:
        print(f"删除源文件时出错: {source_path}")
        print(f"错误信息: {e}")
        return

    print(f"处理完成: {final_output_path}")

# 遍历源文件夹及其子文件夹中的所有视频文件
for root, dirs, files in os.walk(source_folder):
    for file in files:
        if file.lower().endswith(video_formats):  # 检查文件扩展名
            source_path = os.path.join(root, file)
            
            # 计算相对于源文件夹的路径
            relative_path = os.path.relpath(root, source_folder)
            
            compress_and_remux_video(source_path, target_folder, relative_path)

print("所有视频处理完成！")
input("按回车键退出...")