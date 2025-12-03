# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件夹位置（默认“e:\\Documents\\Audios\\Musics\\Singles\\”）与目标文件夹位置（默认“e:\\Documents\\Audios\\Musics\\Singles\\”）。
# 遍历源文件夹及其子文件夹位置中所有音频文件（mp3、m4a、wma、ogg、aac、ac3、rm、wav）。
# 读取每一个音频文件所有元数据写入以改文件夹名为文件名的 xls 文件中。

# 导入模块
import os
import sys
import xlwt
from pathlib import Path
from datetime import datetime
import mutagen  # 用于读取音频元数据
from mutagen.easyid3 import EasyID3
from mutagen.mp4 import MP4
from mutagen.asf import ASF
from mutagen.oggvorbis import OggVorbis
from mutagen.flac import FLAC
from mutagen.wave import WAVE

"""
音频文件元数据提取脚本
功能：遍历指定文件夹中的音频文件，提取元数据并保存到Excel文件
支持的音频格式：mp3, m4a, wma, ogg, aac, ac3, rm, wav
"""

# 支持的音频文件扩展名
AUDIO_EXTENSIONS = {
    '.mp3', '.m4a', '.wma', '.ogg', '.aac', 
    '.ac3', '.rm', '.wav', '.flac'
}

def get_user_input(prompt, default_path):
    """
    获取用户输入的文件夹路径
    
    参数:
        prompt: 提示信息
        default_path: 默认路径
        
    返回:
        用户输入的路径或默认路径
    """
    user_input = input(f"{prompt} (默认: {default_path}): ").strip()
    if not user_input:
        return default_path
    return user_input

def find_audio_files(source_folder):
    """
    递归查找源文件夹中的所有音频文件
    
    参数:
        source_folder: 源文件夹路径
        
    返回:
        字典，键为文件夹路径，值为该文件夹下的音频文件列表
    """
    audio_files_by_folder = {}
    
    # 遍历源文件夹及其所有子文件夹
    for root, dirs, files in os.walk(source_folder):
        audio_files = []
        
        for file in files:
            # 获取文件扩展名并转换为小写
            ext = os.path.splitext(file)[1].lower()
            
            # 检查是否为支持的音频文件
            if ext in AUDIO_EXTENSIONS:
                file_path = os.path.join(root, file)
                audio_files.append(file_path)
        
        # 如果当前文件夹有音频文件，则添加到字典中
        if audio_files:
            audio_files_by_folder[root] = audio_files
    
    return audio_files_by_folder

def get_audio_metadata(file_path):
    """
    读取音频文件的元数据
    
    参数:
        file_path: 音频文件路径
        
    返回:
        字典，包含音频文件的元数据
    """
    metadata = {
        '文件名': os.path.basename(file_path),
        '文件路径': file_path,
        '文件大小(MB)': round(os.path.getsize(file_path) / (1024 * 1024), 2),
        '修改时间': datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
    }
    
    try:
        # 根据文件扩展名使用不同的方法读取元数据
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == '.mp3':
            audio = EasyID3(file_path)
            # 常见的MP3元数据标签
            tags = {
                '标题': 'title',
                '艺术家': 'artist',
                '专辑': 'album',
                '专辑艺术家': 'albumartist',
                '作曲': 'composer',
                '年代': 'date',
                '流派': 'genre',
                '音轨号': 'tracknumber',
                '光盘号': 'discnumber',
                '比特率': 'bitrate',
                '时长': 'length'
            }
            
        elif ext == '.m4a':
            audio = MP4(file_path)
            # MP4/M4A元数据标签
            tags = {
                '标题': '\xa9nam',
                '艺术家': '\xa9ART',
                '专辑': '\xa9alb',
                '专辑艺术家': 'aART',
                '作曲': '\xa9wrt',
                '年代': '\xa9day',
                '流派': '\xa9gen',
                '音轨号': 'trkn',
                '光盘号': 'disk',
                '时长': None  # MP4文件没有直接的时长标签
            }
            
        elif ext == '.wma':
            audio = ASF(file_path)
            # WMA元数据标签
            tags = {
                '标题': 'Title',
                '艺术家': 'Author',
                '专辑': 'WM/AlbumTitle',
                '专辑艺术家': 'WM/AlbumArtist',
                '作曲': 'WM/Composer',
                '年代': 'WM/Year',
                '流派': 'WM/Genre',
                '音轨号': 'WM/TrackNumber',
                '时长': None
            }
            
        elif ext == '.ogg':
            audio = OggVorbis(file_path)
            # OGG元数据标签
            tags = {
                '标题': 'title',
                '艺术家': 'artist',
                '专辑': 'album',
                '专辑艺术家': 'albumartist',
                '作曲': 'composer',
                '年代': 'date',
                '流派': 'genre',
                '音轨号': 'tracknumber',
                '时长': None
            }
            
        elif ext in ['.flac', '.wav']:
            # FLAC和WAV文件使用相同的处理方式
            if ext == '.flac':
                audio = FLAC(file_path)
            else:  # .wav
                audio = WAVE(file_path)
            
            tags = {
                '标题': 'title',
                '艺术家': 'artist',
                '专辑': 'album',
                '专辑艺术家': 'albumartist',
                '作曲': 'composer',
                '年代': 'date',
                '流派': 'genre',
                '音轨号': 'tracknumber',
                '光盘号': 'discnumber',
                '时长': None
            }
            
        else:  # 其他格式如.aac, .ac3, .rm等
            # 使用mutagen通用方法读取
            audio = mutagen.File(file_path)
            tags = {}
            if audio:
                # 获取所有可用标签
                for key in audio.keys():
                    tags[key] = key
            else:
                return metadata
        
        # 提取元数据
        for display_name, tag_name in tags.items():
            if tag_name:
                try:
                    if tag_name == 'bitrate':
                        # 比特率特殊处理
                        if hasattr(audio.info, 'bitrate'):
                            metadata[display_name] = f"{audio.info.bitrate // 1000} kbps"
                    elif tag_name == 'length':
                        # 时长特殊处理
                        if hasattr(audio.info, 'length'):
                            length = audio.info.length
                            minutes = int(length // 60)
                            seconds = int(length % 60)
                            metadata[display_name] = f"{minutes}:{seconds:02d}"
                    else:
                        # 普通标签处理
                        value = audio.get(tag_name, [None])[0]
                        if value:
                            metadata[display_name] = str(value)
                except (KeyError, IndexError, AttributeError):
                    # 如果标签不存在，跳过
                    pass
        
        # 尝试获取通用信息（时长、比特率等）
        if hasattr(audio, 'info'):
            info = audio.info
            if hasattr(info, 'length') and '时长' not in metadata:
                length = info.length
                minutes = int(length // 60)
                seconds = int(length % 60)
                metadata['时长'] = f"{minutes}:{seconds:02d}"
                
            if hasattr(info, 'bitrate') and '比特率' not in metadata:
                metadata['比特率'] = f"{info.bitrate // 1000} kbps" if info.bitrate else "未知"
                
            if hasattr(info, 'sample_rate') and '采样率' not in metadata:
                metadata['采样率'] = f"{info.sample_rate} Hz"
    
    except Exception as e:
        # 如果读取元数据失败，记录错误信息
        metadata['错误信息'] = f"读取元数据失败: {str(e)}"
    
    return metadata

def create_excel_for_folder(folder_path, audio_files, target_folder):
    """
    为指定文件夹创建Excel文件并写入元数据
    
    参数:
        folder_path: 文件夹路径
        audio_files: 该文件夹下的音频文件列表
        target_folder: 目标文件夹路径
        
    返回:
        Excel文件路径
    """
    # 获取文件夹名作为Excel文件名
    folder_name = os.path.basename(folder_path)
    if not folder_name:
        folder_name = "根目录"
    
    # 创建Excel工作簿和工作表
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('音频元数据')
    
    # 设置列标题
    headers = [
        '文件名', '文件路径', '文件大小(MB)', '修改时间',
        '标题', '艺术家', '专辑', '专辑艺术家', '作曲',
        '年代', '流派', '音轨号', '光盘号', '时长',
        '比特率', '采样率', '错误信息'
    ]
    
    # 写入标题行
    for col, header in enumerate(headers):
        worksheet.write(0, col, header)
    
    # 写入音频文件元数据
    for row, file_path in enumerate(audio_files, start=1):
        metadata = get_audio_metadata(file_path)
        
        for col, header in enumerate(headers):
            value = metadata.get(header, '')
            worksheet.write(row, col, value)
    
    # 自动调整列宽（简单实现）
    for col in range(len(headers)):
        worksheet.col(col).width = 256 * 20  # 20个字符宽度
    
    # 保存Excel文件
    excel_filename = f"{folder_name}_音频元数据.xls"
    excel_path = os.path.join(target_folder, excel_filename)
    
    # 确保目标文件夹存在
    os.makedirs(target_folder, exist_ok=True)
    
    # 处理文件名冲突
    counter = 1
    while os.path.exists(excel_path):
        excel_filename = f"{folder_name}_音频元数据_{counter}.xls"
        excel_path = os.path.join(target_folder, excel_filename)
        counter += 1
    
    workbook.save(excel_path)
    return excel_path

def main():
    """主函数"""
    print("=" * 60)
    print("音频文件元数据提取工具")
    print("=" * 60)
    
    # 设置默认路径
    default_source = "e:\\Documents\\Audios\\Musics\\Singles\\"
    default_target = "e:\\Documents\\Audios\\Musics\\Singles\\"
    
    # 获取用户输入
    source_folder = get_user_input("请输入源文件夹位置", default_source)
    target_folder = get_user_input("请输入目标文件夹位置", default_target)
    
    # 检查源文件夹是否存在
    if not os.path.exists(source_folder):
        print(f"错误: 源文件夹不存在: {source_folder}")
        return
    
    # 规范化路径
    source_folder = os.path.normpath(source_folder)
    target_folder = os.path.normpath(target_folder)
    
    print(f"\n正在扫描源文件夹: {source_folder}")
    print("正在查找音频文件...")
    
    # 查找所有音频文件
    audio_files_by_folder = find_audio_files(source_folder)
    
    if not audio_files_by_folder:
        print("未找到任何音频文件！")
        return
    
    # 统计信息
    total_folders = len(audio_files_by_folder)
    total_files = sum(len(files) for files in audio_files_by_folder.values())
    
    print(f"找到 {total_files} 个音频文件，分布在 {total_folders} 个文件夹中")
    print(f"目标文件夹: {target_folder}")
    print("-" * 60)
    
    # 处理每个文件夹
    created_files = []
    for i, (folder_path, audio_files) in enumerate(audio_files_by_folder.items(), start=1):
        folder_name = os.path.basename(folder_path) or "根目录"
        print(f"处理文件夹 {i}/{total_folders}: {folder_name} ({len(audio_files)} 个文件)")
        
        try:
            excel_path = create_excel_for_folder(folder_path, audio_files, target_folder)
            created_files.append(excel_path)
            print(f"  已创建: {os.path.basename(excel_path)}")
        except Exception as e:
            print(f"  错误: 处理文件夹 {folder_name} 时出错: {str(e)}")
    
    # 完成提示
    print("-" * 60)
    print(f"处理完成！")
    print(f"共创建 {len(created_files)} 个Excel文件:")
    for excel_file in created_files:
        print(f"  {excel_file}")
    
    # 询问是否打开目标文件夹
    open_folder = input("\n是否要打开目标文件夹？(y/n): ").strip().lower()
    if open_folder == 'y':
        try:
            os.startfile(target_folder)  # Windows系统
        except:
            try:
                # 其他操作系统
                import subprocess
                subprocess.run(['open', target_folder])  # macOS
            except:
                try:
                    subprocess.run(['xdg-open', target_folder])  # Linux
                except:
                    print("无法自动打开文件夹，请手动访问。")

if __name__ == "__main__":
    # 检查必要的库
    try:
        import mutagen
    except ImportError:
        print("错误: 需要安装 mutagen 库")
        print("请运行: pip install mutagen")
        sys.exit(1)
    
    try:
        import xlwt
    except ImportError:
        print("错误: 需要安装 xlwt 库")
        print("请运行: pip install xlwt")
        sys.exit(1)
    
    main()