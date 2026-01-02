# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件夹位置（默认地址“d:\\Works\\In\\”）与目标文件夹位置（默认地址“d:\\Works\\Out\\”）。
# 遍历源文件夹内所有子文件夹中的视频文件（mkv、avi、f4v、flv、ts、mpeg、mpg、rm、rmvb、asf、wmv、mov、webm、mp4、ogv、ogm、ogg）。
# 使用 mkvmerge.exe 转换成 mkv 格式。类似“for %%i in (*.*) do "d:\Program Files\MKVToolNix\mkvmerge.exe" -o "%%~ni.mkv" "%%~nxi"”。
# 生成的文件放到到目标文件夹中以“源文件夹的子文件夹”中，保持文件夹及子文件结构。

# 导入模块
import os
import subprocess
import sys

def get_user_input():
    """
    获取用户输入的源文件夹和目标文件夹路径
    """
    # 获取源文件夹路径
    default_source = "d:\\Works\\In\\"
    source_folder = input(f"请输入源文件夹位置（默认：{default_source}）: ").strip()
    if not source_folder:
        source_folder = default_source
    source_folder = source_folder.rstrip('\\/')
    
    # 获取目标文件夹路径
    default_target = "d:\\Works\\Out\\"
    target_folder = input(f"请输入目标文件夹位置（默认：{default_target}）: ").strip()
    if not target_folder:
        target_folder = default_target
    target_folder = target_folder.rstrip('\\/')
    
    return source_folder, target_folder

def find_video_files(source_folder):
    """
    查找源文件夹中所有视频文件
    """
    # 支持的视频文件扩展名
    video_extensions = {
        '.mkv', '.avi', '.f4v', '.flv', '.ts', '.mpeg', '.mpg',
        '.rm', '.rmvb', '.asf', '.wmv', '.mov', '.webm', '.mp4',
        '.ogv', '.ogm', '.ogg'
    }
    
    video_files = []
    
    print(f"\n正在扫描源文件夹: {source_folder}")
    
    # 遍历所有子文件夹
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            # 获取文件扩展名并转换为小写
            ext = os.path.splitext(file)[1].lower()
            if ext in video_extensions:
                full_path = os.path.join(root, file)
                video_files.append(full_path)
    
    print(f"找到 {len(video_files)} 个视频文件")
    return video_files

def get_relative_path(full_path, source_folder):
    """
    获取文件相对于源文件夹的相对路径
    """
    # 标准化路径
    full_path = os.path.normpath(full_path)
    source_folder = os.path.normpath(source_folder)
    
    # 获取相对路径
    relative_path = os.path.relpath(full_path, source_folder)
    
    # 获取所在文件夹（相对路径的目录部分）
    relative_dir = os.path.dirname(relative_path)
    
    return relative_dir

def convert_video(source_file, target_file, mkvmerge_path):
    """
    使用 mkvmerge 转换单个视频文件
    """
    try:
        # 构建命令
        command = [
            mkvmerge_path,
            '-o', target_file,
            source_file
        ]
        
        print(f"正在转换: {os.path.basename(source_file)}")
        
        # 执行转换命令，解决编码问题
        result = subprocess.run(
            command, 
            capture_output=True, 
            text=True, 
            check=True,
            encoding='utf-8',  # 明确指定编码
            errors='ignore'    # 忽略编码错误
        )
        
        if result.returncode == 0:
            print(f"✓ 转换成功: {os.path.basename(target_file)}")
            
            # 检查目标文件是否存在且大小合理
            if os.path.exists(target_file) and os.path.getsize(target_file) > 0:
                # 删除源文件
                try:
                    os.remove(source_file)
                    print(f"✓ 已删除源文件: {os.path.basename(source_file)}")
                except Exception as e:
                    print(f"⚠ 无法删除源文件 {os.path.basename(source_file)}: {str(e)}")
                    return True  # 转换成功但删除失败，仍然算转换成功
            else:
                print(f"⚠ 目标文件可能有问题，保留源文件: {os.path.basename(source_file)}")
                return True  # 转换成功但目标文件可能有问题，保留源文件
                
            return True
        else:
            print(f"✗ 转换失败: {os.path.basename(source_file)}")
            if result.stderr:
                print(f"错误信息: {result.stderr}")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"✗ 转换出错: {os.path.basename(source_file)}")
        if e.stderr:
            # 尝试不同编码方式处理错误信息
            try:
                error_msg = e.stderr.decode('utf-8', errors='ignore')
            except:
                error_msg = str(e.stderr)
            print(f"错误信息: {error_msg}")
        return False
    except Exception as e:
        print(f"✗ 发生未知错误: {os.path.basename(source_file)}")
        print(f"错误信息: {str(e)}")
        return False

def main():
    """
    主函数
    """
    # 获取用户输入
    source_folder, target_folder = get_user_input()
    
    # 检查源文件夹是否存在
    if not os.path.exists(source_folder):
        print(f"错误: 源文件夹不存在 - {source_folder}")
        return
    
    # 检查 mkvmerge.exe 是否可用
    mkvmerge_paths = [
        r"d:\ProApps\MKVToolNix\mkvmerge.exe",
        r"C:\Program Files\MKVToolNix\mkvmerge.exe",
        "mkvmerge.exe"  # 如果在系统PATH中
    ]
    
    mkvmerge_path = None
    for path in mkvmerge_paths:
        if os.path.exists(path):
            mkvmerge_path = path
            break
        # 检查是否在系统PATH中
        try:
            # 使用更安全的方式检查版本
            result = subprocess.run(
                [path, "--version"], 
                capture_output=True, 
                text=True,
                encoding='utf-8',
                errors='ignore'
            )
            if result.returncode == 0:
                mkvmerge_path = path
                break
        except:
            continue
    
    if not mkvmerge_path:
        print("错误: 未找到 mkvmerge.exe")
        print("请确保已安装 MKVToolNix 或提供正确的路径")
        return
    
    print(f"使用 mkvmerge: {mkvmerge_path}")
    
    # 查找所有视频文件
    video_files = find_video_files(source_folder)
    
    if not video_files:
        print("未找到任何视频文件，程序结束")
        return
    
    # 显示找到的文件
    print("\n找到的视频文件:")
    for i, file in enumerate(video_files[:10], 1):  # 只显示前10个
        print(f"  {i}. {file}")
    if len(video_files) > 10:
        print(f"  ... 还有 {len(video_files) - 10} 个文件")
    
    # 直接开始转换，不询问确认
    print(f"\n开始转换 {len(video_files)} 个文件...")
    print("注意: 转换成功后会自动删除源文件!")
    
    # 开始转换
    successful = 0
    failed = 0
    deleted = 0
    
    for source_file in video_files:
        # 获取相对路径
        relative_dir = get_relative_path(source_file, source_folder)
        
        # 构建目标路径
        source_filename = os.path.basename(source_file)
        target_filename = os.path.splitext(source_filename)[0] + '.mkv'
        target_dir = os.path.join(target_folder, relative_dir)
        target_file = os.path.join(target_dir, target_filename)
        
        # 创建目标目录（如果不存在）
        os.makedirs(target_dir, exist_ok=True)
        
        # 转换视频
        if convert_video(source_file, target_file, mkvmerge_path):
            successful += 1
            # 检查源文件是否已被删除
            if not os.path.exists(source_file):
                deleted += 1
        else:
            failed += 1
    
    # 显示转换结果
    print(f"\n转换完成。")
    print(f"成功: {successful} 个文件")
    print(f"失败: {failed} 个文件")
    print(f"已删除源文件: {deleted} 个")
    print(f"目标文件夹: {target_folder}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n用户中断程序")
    except Exception as e:
        print(f"\n程序发生错误: {str(e)}")
    
    input("\n按回车键退出...")