# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件夹位置（默认“d:\\Works\\In\\”）与目标文件夹位置（默认“d:\\Works\\Out\\”）。
# 遍历源文件夹及其子文件夹位置中所有音频文件（mp3、m4a、wma、ogg、aac、ac3、rm、wav）。
# 使用 ffmpeg 压缩。
# 音频参数为：ogg 格式，遍历每个音轨，质量模式。q=4。
# 生成的文件重新用 mkvmerge 再生成同名文件到 目标文件夹位置，文件夹结构保持一致。

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
source_folder = ask_folder_location("请输入源文件夹位置（默认“d:\\Works\\In\\”）", "d:\\Works\\In\\")
target_folder = ask_folder_location("请输入目标文件夹位置（默认“d:\\Works\\Out\\”）", "d:\\Works\\Out\\")

# 支持的音频格式
audio_formats = (".mp3", ".m4a", ".wma", ".ogg", ".aac", ".ac3", ".rm", ".wav")

# 确保目标文件夹存在
os.makedirs(target_folder, exist_ok=True)

def compress_and_remux_audio(source_path, target_folder, relative_path):
    """
    压缩音频并重新封装到目标文件夹，保持目录结构。
    :param source_path: 源音频文件路径
    :param target_folder: 目标文件夹路径
    :param relative_path: 相对于源文件夹的路径
    """
    # 获取文件名（不含扩展名）
    file_name, _ = os.path.splitext(os.path.basename(source_path))
    
    # 在目标文件夹中创建相同的目录结构
    target_subfolder = os.path.join(target_folder, relative_path)
    os.makedirs(target_subfolder, exist_ok=True)
    
    # 临时ogg文件路径和最终mkv文件路径
    temp_ogg_path = os.path.join(target_subfolder, f"{file_name}_temp.ogg")
    final_mkv_path = os.path.join(target_subfolder, f"{file_name}.mkv")
    
    # 构建ffmpeg命令：压缩音频为ogg格式[citation:2]
    ffmpeg_command = [
        "ffmpeg", 
        "-i", source_path,           # 输入文件
        "-c:a", "libvorbis",         # 音频编码器为libvorbis（ogg）
        "-q:a", "4",                 # 音频质量设置为4[citation:2]
        "-map", "0:a",               # 映射所有音频流
        "-y",                        # 覆盖输出文件
        temp_ogg_path
    ]
    
    print(f"正在压缩音频: {source_path}")
    try:
        # 执行ffmpeg命令
        subprocess.run(ffmpeg_command, check=True, capture_output=True)
        print(f"音频压缩完成: {temp_ogg_path}")
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg压缩失败: {source_path}")
        print(f"错误信息: {e.stderr.decode('utf-8', errors='ignore') if e.stderr else str(e)}")
        # 如果临时文件已创建，删除它
        if os.path.exists(temp_ogg_path):
            os.remove(temp_ogg_path)
        return
    except FileNotFoundError:
        print("错误: 未找到ffmpeg，请确保ffmpeg已安装并添加到系统PATH")
        return
    
    # 构建mkvmerge命令：将ogg封装为mkv[citation:3]
    mkvmerge_command = [
        "mkvmerge", 
        "-o", final_mkv_path,        # 输出文件
        temp_ogg_path                # 输入文件（压缩后的ogg）
    ]
    
    print(f"正在重新封装音频: {temp_ogg_path}")
    try:
        # 执行mkvmerge命令
        subprocess.run(mkvmerge_command, check=True, capture_output=True)
        
        # 删除临时ogg文件
        if os.path.exists(temp_ogg_path):
            os.remove(temp_ogg_path)
            print(f"临时文件已删除: {temp_ogg_path}")
            
        print(f"处理完成: {final_mkv_path}")
        
    except subprocess.CalledProcessError as e:
        print(f"mkvmerge封装失败: {temp_ogg_path}")
        print(f"错误信息: {e.stderr.decode('utf-8', errors='ignore') if e.stderr else str(e)}")
        return
    except FileNotFoundError:
        print("错误: 未找到mkvmerge，请确保mkvtoolnix已安装并添加到系统PATH")
        return

# 遍历源文件夹及其子文件夹中的所有音频文件[citation:1]
for root, dirs, files in os.walk(source_folder):
    for file in files:
        if file.lower().endswith(audio_formats):  # 检查文件扩展名（忽略大小写）
            source_path = os.path.join(root, file)
            
            # 计算相对于源文件夹的路径
            relative_path = os.path.relpath(root, source_folder)
            
            # 压缩并重新封装音频
            compress_and_remux_audio(source_path, target_folder, relative_path)

print("所有音频处理完成！")
input("按回车键退出...")