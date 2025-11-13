# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件夹位置（默认为 d:\\Works\\Downloads\\）与目标文件夹位置（默认为 d:\\Works\\In\\）。
# 1. 如果源文件格式为 bmp、jpg、jpeg、png 或静态 webp 格式、或静态 avif 格式、静态 heic 格式、静态 heif 格式，则计算“imagehash.dhash”，用这个哈希值重命名，前后用中括号包绕，扩展名不变，如[hash].jpg。
# 2. 如果图片文件格式为 gif 或动态 webp 格式、或动态 avif 格式、动态 heic 格式、动态 heif 格式或 mp4 格式，则取第一帧与最后一帧，分别计算“imagehash.dhash”，用这两个哈希值重命名，前后用中括号包绕，中间是多少帧数，扩展名不变，如[hash1][24][hash1].gif。
# 生成的文件放到目标文件夹中以“源文件夹的子文件夹”中，保持文件夹及子文件结构。如果生成新文件成功，则删除原始文件。

# 导入模块
import os
import sys
from PIL import Image
import imagehash
import shutil
import subprocess
import tempfile

def get_video_info(filepath):
    """
    使用FFprobe获取视频信息（帧数、时长等）
    """
    try:
        # 使用FFprobe获取视频信息
        cmd = [
            'ffprobe', '-v', 'error', '-select_streams', 'v:0',
            '-show_entries', 'stream=nb_frames,r_frame_rate,duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            filepath
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output_lines = result.stdout.strip().split('\n')
        
        # 解析输出
        frame_rate = None
        duration = None
        frame_count = None
        
        for line in output_lines:
            if '/' in line:  # 帧率格式如 30000/1001
                frame_rate = line
            elif line.replace('.', '').isdigit():  # 时长或帧数
                if '.' in line:
                    duration = float(line)
                else:
                    frame_count = int(line)
        
        # 如果无法直接获取帧数，尝试通过时长和帧率计算
        if frame_count is None and duration and frame_rate:
            try:
                num, den = map(int, frame_rate.split('/'))
                fps = num / den
                frame_count = int(duration * fps)
            except:
                frame_count = 100  # 默认值
        
        return frame_count or 100
    except Exception as e:
        print(f"获取视频信息失败：{filepath}，错误：{str(e)}")
        return 100  # 返回默认帧数

def extract_video_frame(filepath, frame_time, output_path):
    """
    使用FFmpeg提取视频的指定帧
    frame_time: 时间点（秒）
    """
    try:
        # 使用FFmpeg提取指定时间点的帧，添加更多参数提高兼容性
        cmd = [
            'ffmpeg', '-i', filepath, '-ss', str(frame_time),
            '-vframes', '1', '-q:v', '2', '-y',
            '-avoid_negative_ts', 'make_zero',
            '-fflags', '+genpts',
            output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"提取视频帧失败：{filepath}，时间：{frame_time}，错误码：{e.returncode}")
        if e.stderr:
            print(f"FFmpeg错误信息：{e.stderr[:200]}...")  # 只显示前200个字符
        return False
    except Exception as e:
        print(f"提取视频帧失败：{filepath}，时间：{frame_time}，错误：{str(e)}")
        return False

def extract_first_and_last_frames(filepath, temp_dir):
    """
    提取视频的第一帧和最后一帧，使用更健壮的方法
    """
    first_frame_path = os.path.join(temp_dir, "first_frame.jpg")
    last_frame_path = os.path.join(temp_dir, "last_frame.jpg")
    
    # 提取第一帧（从开始位置）
    if not extract_video_frame(filepath, 0, first_frame_path):
        return None, None
    
    # 获取视频时长
    try:
        cmd = ['ffprobe', '-v', 'error', '-show_entries', 
              'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', filepath]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        duration = float(result.stdout.strip())
        
        # 尝试多个时间点提取最后一帧
        last_frame_time = max(0, duration - 0.5)  # 从结束前0.5秒开始
        
        # 尝试提取最后一帧
        if not extract_video_frame(filepath, last_frame_time, last_frame_path):
            # 如果失败，尝试更早的时间点
            last_frame_time = max(0, duration - 1.0)
            if not extract_video_frame(filepath, last_frame_time, last_frame_path):
                # 如果仍然失败，使用第一帧作为最后一帧
                print(f"无法提取最后一帧，使用第一帧替代：{filepath}")
                shutil.copy2(first_frame_path, last_frame_path)
    except Exception as e:
        print(f"获取视频时长失败：{filepath}，错误：{str(e)}")
        # 使用第一帧作为最后一帧
        shutil.copy2(first_frame_path, last_frame_path)
    
    return first_frame_path, last_frame_path

def is_animated_image(filepath):
    """
    检测图片是否为动态图
    """
    try:
        ext = os.path.splitext(filepath)[1].lower()
        
        # MP4文件始终认为是动态的
        if ext == '.mp4':
            return True
        
        # 使用Pillow检测其他格式的动画属性
        with Image.open(filepath) as img:
            if hasattr(img, 'is_animated'):
                return img.is_animated
            
            # 对于不支持is_animated的格式，尝试获取帧数
            try:
                img.seek(1)  # 尝试跳到第二帧
                return True
            except EOFError:
                return False
                
    except Exception as e:
        print(f"动态检测失败：{filepath}，错误：{str(e)}")
        return False

def get_image_frame_count(filepath):
    """
    获取动态图片的帧数
    """
    try:
        frame_count = 1
        with Image.open(filepath) as img:
            if hasattr(img, 'is_animated') and img.is_animated:
                while True:
                    try:
                        img.seek(frame_count)
                        frame_count += 1
                    except EOFError:
                        break
        return frame_count
    except Exception as e:
        print(f"获取图片帧数失败：{filepath}，错误：{str(e)}")
        return 1

def calculate_image_hash(filepath):
    """
    计算图片的dhash值
    """
    try:
        with Image.open(filepath) as img:
            return imagehash.dhash(img)
    except Exception as e:
        print(f"计算哈希失败：{filepath}，错误：{str(e)}")
        return None

def process_static_image(filepath, dst_dir, relative_path):
    """
    处理静态图片文件
    """
    try:
        # 计算图片哈希
        hash_value = calculate_image_hash(filepath)
        if hash_value is None:
            return False
        
        # 获取文件扩展名
        _, ext = os.path.splitext(filepath)
        
        # 构建新文件名 - 修改：将哈希值转换为大写
        new_filename = f"[{str(hash_value).upper()}]{ext}"
        
        # 构建目标路径
        dst_subdir = os.path.join(dst_dir, relative_path)
        os.makedirs(dst_subdir, exist_ok=True)
        dst_path = os.path.join(dst_subdir, new_filename)
        
        # 复制文件到目标位置
        shutil.copy2(filepath, dst_path)
        print(f"静态图片处理成功：{os.path.basename(filepath)} -> {new_filename}")
        return True
        
    except Exception as e:
        print(f"静态图片处理失败：{filepath}，错误：{str(e)}")
        return False

def process_animated_image(filepath, dst_dir, relative_path):
    """
    处理动态图片文件（GIF、动态WebP等）
    """
    try:
        # 获取帧数
        frame_count = get_image_frame_count(filepath)
        
        # 提取第一帧和最后一帧计算哈希
        with Image.open(filepath) as img:
            # 第一帧
            img.seek(0)
            first_frame_hash = imagehash.dhash(img)
            
            # 最后一帧
            try:
                last_frame_index = frame_count - 1 if frame_count > 1 else 0
                img.seek(last_frame_index)
                last_frame_hash = imagehash.dhash(img)
            except:
                # 如果获取最后一帧失败，使用第一帧哈希
                last_frame_hash = first_frame_hash
        
        # 获取文件扩展名
        _, ext = os.path.splitext(filepath)
        
        # 构建新文件名 - 修改：将哈希值转换为大写
        new_filename = f"[{str(first_frame_hash).upper()}][{frame_count}][{str(last_frame_hash).upper()}]{ext}"
        
        # 构建目标路径
        dst_subdir = os.path.join(dst_dir, relative_path)
        os.makedirs(dst_subdir, exist_ok=True)
        dst_path = os.path.join(dst_subdir, new_filename)
        
        # 复制文件到目标位置
        shutil.copy2(filepath, dst_path)
        print(f"动态图片处理成功：{os.path.basename(filepath)} -> {new_filename}")
        return True
        
    except Exception as e:
        print(f"动态图片处理失败：{filepath}，错误：{str(e)}")
        return False

def process_video_file(filepath, dst_dir, relative_path):
    """
    处理视频文件（MP4等）
    """
    try:
        # 获取视频信息
        frame_count = get_video_info(filepath)
        
        # 创建临时目录用于保存提取的帧
        with tempfile.TemporaryDirectory() as temp_dir:
            # 提取第一帧和最后一帧
            first_frame_path, last_frame_path = extract_first_and_last_frames(filepath, temp_dir)
            
            if first_frame_path is None or not os.path.exists(first_frame_path):
                print(f"无法提取视频帧：{filepath}")
                return False
            
            # 计算哈希值
            first_frame_hash = calculate_image_hash(first_frame_path)
            last_frame_hash = calculate_image_hash(last_frame_path)
            
            if first_frame_hash is None:
                print(f"无法计算视频帧哈希：{filepath}")
                return False
            
            # 如果最后一帧哈希计算失败，使用第一帧哈希
            if last_frame_hash is None:
                last_frame_hash = first_frame_hash
            
            # 获取文件扩展名
            _, ext = os.path.splitext(filepath)
            
            # 构建新文件名 - 修改：将哈希值转换为大写
            new_filename = f"[{str(first_frame_hash).upper()}][{frame_count}][{str(last_frame_hash).upper()}]{ext}"
            
            # 构建目标路径
            dst_subdir = os.path.join(dst_dir, relative_path)
            os.makedirs(dst_subdir, exist_ok=True)
            dst_path = os.path.join(dst_subdir, new_filename)
            
            # 复制文件到目标位置
            shutil.copy2(filepath, dst_path)
            print(f"视频文件处理成功：{os.path.basename(filepath)} -> {new_filename}")
            return True
            
    except Exception as e:
        print(f"视频文件处理失败：{filepath}，错误：{str(e)}")
        return False

def process_files(src_folder, dst_folder):
    """
    处理源文件夹中的所有图片文件
    """
    # 支持的图片格式
    image_extensions = {'.bmp', '.jpg', '.jpeg', '.png', '.webp', '.avif', '.heic', '.heif', '.gif', '.mp4'}
    
    processed_count = 0
    error_count = 0
    
    for root, dirs, files in os.walk(src_folder):
        for file in files:
            filepath = os.path.join(root, file)
            ext = os.path.splitext(file)[1].lower()
            
            # 跳过非图片文件
            if ext not in image_extensions:
                continue
            
            try:
                # 计算相对路径
                relative_path = os.path.relpath(root, src_folder)
                if relative_path == '.':
                    relative_path = ''
                
                success = False
                
                # 判断文件类型并处理
                if ext in {'.bmp', '.jpg', '.jpeg', '.png'}:
                    # 静态图片格式
                    success = process_static_image(filepath, dst_folder, relative_path)
                
                elif ext in {'.webp', '.avif', '.heic', '.heif'}:
                    # 需要检测是否为动态
                    if is_animated_image(filepath):
                        success = process_animated_image(filepath, dst_folder, relative_path)
                    else:
                        success = process_static_image(filepath, dst_folder, relative_path)
                
                elif ext == '.gif':
                    # GIF动态图片
                    success = process_animated_image(filepath, dst_folder, relative_path)
                
                elif ext == '.mp4':
                    # MP4视频文件
                    success = process_video_file(filepath, dst_folder, relative_path)
                
                # 如果处理成功，删除原始文件
                if success:
                    os.remove(filepath)
                    processed_count += 1
                else:
                    error_count += 1
                    print(f"处理失败：{filepath}")
                    
            except Exception as e:
                print(f"处理文件时发生错误：{filepath}，错误：{str(e)}")
                error_count += 1
    
    return processed_count, error_count

def check_ffmpeg_available():
    """
    检查FFmpeg是否可用
    """
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        subprocess.run(['ffprobe', '-version'], capture_output=True, check=True)
        return True
    except:
        return False

def main():
    """
    主函数
    """    
    # 检查FFmpeg是否可用
    if not check_ffmpeg_available():
        print("错误：未找到FFmpeg或FFprobe，请确保已正确安装FFmpeg并添加到系统PATH")
        print("请参考：https://ffmpeg.org/download.html")
        input("按回车键退出...")
        return
    
    # 设置默认路径
    default_src = "d:\\Works\\Downloads\\"
    default_dst = "d:\\Works\\In\\"
    
    # 获取用户输入
    src_input = input(f"请输入源文件夹路径（默认：{default_src}）：").strip()
    dst_input = input(f"请输入目标文件夹路径（默认：{default_dst}）：").strip()
    
    # 使用默认值或用户输入
    src_folder = src_input if src_input else default_src
    dst_folder = dst_input if dst_input else default_dst
    
    # 规范化路径
    src_folder = os.path.normpath(src_folder)
    dst_folder = os.path.normpath(dst_folder)
    
    # 检查源文件夹是否存在
    if not os.path.exists(src_folder):
        print(f"错误：源文件夹不存在 - {src_folder}")
        input("按回车键退出...")
        return
    
    # 创建目标文件夹（如果不存在）
    os.makedirs(dst_folder, exist_ok=True)
    
    print(f"\n开始处理...")
    print(f"源文件夹：{src_folder}")
    print(f"目标文件夹：{dst_folder}")
    print("-" * 30)
    
    # 处理文件
    processed_count, error_count = process_files(src_folder, dst_folder)
    
    # 输出结果
    print("-" * 30)
    print(f"处理完成！")
    print(f"成功处理：{processed_count} 个文件")
    print(f"处理失败：{error_count} 个文件")
    
    input("\n按回车键退出...")

if __name__ == "__main__":
    main()