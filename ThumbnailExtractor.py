# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件夹位置与目标文件夹位置。
# 遍历源文件夹位置中所有视频文件（mkv、avi、f4v、flv、ts、mpeg、mpg、rm、rmvb、asf、wmv、mov、webm、mp4）。
# 使用 ffmpeg 压缩，类似命令：ffmpeg -i input.mp4 -ss 00:00:01 -vframes 1 output.jpg。
# 分别截取第 1 秒、第 10 秒以及一半时间的视频的图片，后缀名为-s01.jpg、-s10.jpg、-ss.jpg。

# 导入模块
import os
import subprocess

def get_input(prompt, default_value):
    """
    获取用户输入，提供默认值。
    """
    value = input(f"{prompt} (默认: {default_value}): ").strip()
    return value if value else default_value

def is_video_file(file_name):
    """
    检查文件是否为支持的视频格式。
    """
    video_extensions = [".mkv", ".avi", ".f4v", ".flv", ".ts", ".mpeg", ".mpg", ".rm", ".rmvb", ".asf", ".wmv", ".mov", ".webm", ".mp4"]
    return any(file_name.lower().endswith(ext) for ext in video_extensions)

def create_output_folder(folder_path):
    """
    如果目标文件夹不存在，则创建。
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def extract_thumbnails(video_path, output_folder):
    """
    使用 ffmpeg 从视频中截取第 1 秒、第 10 秒及视频中间位置的图片。
    """
    video_name, _ = os.path.splitext(os.path.basename(video_path))

    # 获取视频时长
    cmd_get_duration = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", video_path]
    try:
        duration_output = subprocess.check_output(cmd_get_duration, stderr=subprocess.STDOUT).strip()
        duration_lines = duration_output.decode("utf-8").splitlines()
        duration_str = next((line for line in duration_lines if line.replace('.', '', 1).isdigit()), None)
        if duration_str is None:
            raise ValueError("未找到有效的时长信息")
        duration = float(duration_str)  # 转换为浮点数
    except Exception as e:
        print(f"获取视频时长失败: {video_path}, 错误: {e}")
        return

    # 确定截图时间点
    timestamps = [(1, "-s01"), (10, "-s10"), (duration / 2, "-ss")]

    for timestamp, suffix in timestamps:
        output_file = os.path.join(output_folder, f"{video_name}{suffix}.jpg")
        cmd_extract = [
            "ffmpeg", "-i", video_path, "-ss", f"{timestamp:.2f}", "-vframes", "1", output_file
        ]
        try:
            subprocess.run(cmd_extract, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"截图成功: {output_file}")
        except subprocess.CalledProcessError as e:
            print(f"截图失败: {output_file}, 错误: {e}")

def main():
    """
    主程序入口：获取用户输入的文件夹，遍历文件并处理。
    """
    # 默认源文件夹和目标文件夹路径
    default_source_folder = "d:\\Works\\Out\\"
    default_target_folder = "d:\\Works\\Out\\"

    # 获取源文件夹和目标文件夹路径
    source_folder = get_input("请输入源文件夹路径：", default_source_folder)
    target_folder = get_input("请输入目标文件夹路径：", default_target_folder)

    # 创建目标文件夹
    create_output_folder(target_folder)

    # 遍历源文件夹中的视频文件
    for root, _, files in os.walk(source_folder):
        for file in files:
            if is_video_file(file):
                video_path = os.path.join(root, file)
                relative_path = os.path.relpath(root, source_folder)
                output_folder = os.path.join(target_folder, relative_path)

                # 创建子文件夹以保持目录结构
                create_output_folder(output_folder)

                # 截图
                extract_thumbnails(video_path, output_folder)

if __name__ == "__main__":
    main()

print("所有视频处理完成！")
input("按回车键退出...")