# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件夹位置（默认“d:\\Works\\In\\”）。
# 遍历源文件夹及其子文件夹位置中所有音频文件（mp3、m4a、wma、ogg、aac、ac3、rm、wav）。
# 读取每一个音频文件所有元数据写入以该文件夹名为文件名的 xls 文件中。
# 标签有：标题（TITLE）、歌手（ARTIST）、作曲（COMPOSER）、作词（LYRICIST）、专辑（ALBUM）、专辑作者（ALBUMARTIST）、年份（YEAR）、流派（GENRE）、碟号（DISCNUMBER）、音轨（TRACK）。
# 将文件重命名为[歌手][标题].扩展名。如果有多个歌手，则重命名为[歌手1&歌手2][标题].扩展名。
# 同时将内嵌的封面导出为同名 jpg 文件（640*640大小），同时将内嵌的歌词导出为同名 lrc 文件。

# 导入模块
import os
import sys
import xlwt
import re
from PIL import Image
import io
from mutagen import File
from mutagen.id3 import ID3, APIC, USLT
from mutagen.mp4 import MP4
from mutagen.asf import ASF
from mutagen.oggvorbis import OggVorbis
from mutagen.flac import FLAC
import traceback

"""
音频文件处理脚本
功能：重命名音频文件、提取元数据到Excel、导出封面和歌词
重命名规则：[歌手][标题].扩展名，多个歌手用&连接
"""

def get_user_input():
    """获取用户输入的源文件夹路径"""
    default_path = "d:\\Works\\In\\"
    user_input = input(f"请输入源文件夹位置（直接回车使用默认值 '{default_path}'）：").strip()
    
    if user_input == "":
        source_folder = default_path
    else:
        source_folder = user_input
    
    # 标准化路径
    source_folder = os.path.normpath(source_folder)
    
    # 检查文件夹是否存在
    if not os.path.exists(source_folder):
        print(f"错误：文件夹 '{source_folder}' 不存在！")
        sys.exit(1)
    
    return source_folder

def get_audio_files(folder_path):
    """递归获取文件夹中所有音频文件"""
    audio_extensions = {'.mp3', '.m4a', '.wma', '.ogg', '.aac', '.ac3', '.rm', '.wav'}
    audio_files = []
    
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_ext = os.path.splitext(file)[1].lower()
            if file_ext in audio_extensions:
                full_path = os.path.join(root, file)
                audio_files.append(full_path)
    
    return audio_files

def clean_filename(text):
    """清理文件名，移除非法字符"""
    if not text:
        return ""
    
    # 定义非法字符（Windows文件名中不允许的字符）
    illegal_chars = r'[<>:"/\\|?*\x00-\x1F]'
    # 移除非法字符
    cleaned = re.sub(illegal_chars, '', str(text))
    # 替换空格为下划线（可选）
    cleaned = cleaned.replace(' ', '_')
    # 移除首尾空白
    cleaned = cleaned.strip()
    
    return cleaned

def rename_audio_file(file_path, artist, title):
    """根据歌手和标题重命名音频文件"""
    if not artist and not title:
        return file_path, False, "缺少歌手和标题信息"
    
    # 获取文件目录和扩展名
    dir_name = os.path.dirname(file_path)
    ext = os.path.splitext(file_path)[1]
    
    # 清理歌手和标题
    artist_clean = clean_filename(artist)
    title_clean = clean_filename(title)
    
    # 处理多个歌手的情况
    if artist_clean:
        # 分割歌手（支持多种分隔符）
        separators = ['/', ';', '&', '、', ',', '，', '\\|']
        for sep in separators:
            if sep in artist_clean:
                artists = [a.strip() for a in artist_clean.split(sep) if a.strip()]
                if len(artists) > 1:
                    # 用&连接多个歌手
                    artist_clean = '&'.join(artists)
                    break
    
    # 构建新文件名
    if artist_clean and title_clean:
        new_filename = f"[{artist_clean}][{title_clean}]{ext}"
    elif artist_clean:
        new_filename = f"[{artist_clean}]{ext}"
    elif title_clean:
        new_filename = f"[{title_clean}]{ext}"
    else:
        return file_path, False, "无法生成新文件名"
    
    # 构建完整的新文件路径
    new_file_path = os.path.join(dir_name, new_filename)
    
    # 检查新文件名是否已存在（处理重名）
    counter = 1
    original_new_file_path = new_file_path
    while os.path.exists(new_file_path) and new_file_path != file_path:
        name_part, ext_part = os.path.splitext(original_new_file_path)
        new_file_path = f"{name_part}_{counter}{ext_part}"
        counter += 1
    
    # 重命名文件
    try:
        os.rename(file_path, new_file_path)
        return new_file_path, True, "重命名成功"
    except Exception as e:
        return file_path, False, f"重命名失败: {str(e)}"

def extract_metadata(file_path):
    """提取音频文件的元数据"""
    try:
        # 根据文件扩展名使用不同的解析方法
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == '.mp3':
            return extract_mp3_metadata(file_path)
        elif file_ext == '.m4a':
            return extract_m4a_metadata(file_path)
        elif file_ext == '.wma':
            return extract_wma_metadata(file_path)
        elif file_ext == '.ogg':
            return extract_ogg_metadata(file_path)
        elif file_ext in ['.flac', '.aac', '.ac3', '.rm', '.wav']:
            return extract_generic_metadata(file_path)
        else:
            return {}
            
    except Exception as e:
        print(f"提取元数据时出错 {file_path}: {str(e)}")
        return {}

def extract_mp3_metadata(file_path):
    """提取MP3文件元数据"""
    metadata = {}
    
    try:
        audio = ID3(file_path)
        
        # 提取文本标签
        metadata['标题'] = str(audio.get('TIT2', [''])[0]) if 'TIT2' in audio else ''
        metadata['歌手'] = str(audio.get('TPE1', [''])[0]) if 'TPE1' in audio else ''
        metadata['作曲'] = str(audio.get('TCOM', [''])[0]) if 'TCOM' in audio else ''
        metadata['作词'] = str(audio.get('TEXT', [''])[0]) if 'TEXT' in audio else ''
        metadata['专辑'] = str(audio.get('TALB', [''])[0]) if 'TALB' in audio else ''
        metadata['专辑作者'] = str(audio.get('TPE2', [''])[0]) if 'TPE2' in audio else ''
        metadata['年份'] = str(audio.get('TDRC', [''])[0]) if 'TDRC' in audio else ''
        metadata['流派'] = str(audio.get('TCON', [''])[0]) if 'TCON' in audio else ''
        metadata['碟号'] = str(audio.get('TPOS', [''])[0]) if 'TPOS' in audio else ''
        metadata['音轨'] = str(audio.get('TRCK', [''])[0]) if 'TRCK' in audio else ''
        
        # 提取封面
        if 'APIC:' in audio:
            for key in audio.keys():
                if key.startswith('APIC'):
                    metadata['封面'] = audio[key].data
                    break
        
        # 提取歌词
        if 'USLT::' in audio:
            for key in audio.keys():
                if key.startswith('USLT'):
                    metadata['歌词'] = audio[key].text
                    break
        
    except Exception as e:
        # 如果ID3标签读取失败，尝试使用通用方法
        return extract_generic_metadata(file_path)
    
    return metadata

def extract_m4a_metadata(file_path):
    """提取M4A文件元数据"""
    metadata = {}
    
    try:
        audio = MP4(file_path)
        
        # MP4标签映射
        tag_map = {
            '标题': '\xa9nam',
            '歌手': '\xa9ART',
            '作曲': '\xa9wrt',
            '作词': '\xa9lyr',
            '专辑': '\xa9alb',
            '专辑作者': 'aART',
            '年份': '\xa9day',
            '流派': '\xa9gen',
            '碟号': 'disk',
            '音轨': 'trkn'
        }
        
        for key, tag in tag_map.items():
            if tag in audio:
                value = audio[tag]
                if isinstance(value, list) and len(value) > 0:
                    metadata[key] = str(value[0])
                else:
                    metadata[key] = str(value)
            else:
                metadata[key] = ''
        
        # 提取封面
        if 'covr' in audio:
            metadata['封面'] = audio['covr'][0]
        
        # 提取歌词
        if '\xa9lyr' in audio:
            metadata['歌词'] = str(audio['\xa9lyr'][0])
            
    except Exception as e:
        print(f"提取M4A元数据失败 {file_path}: {str(e)}")
    
    return metadata

def extract_wma_metadata(file_path):
    """提取WMA文件元数据"""
    metadata = {}
    
    try:
        audio = ASF(file_path)
        
        # WMA标签映射
        tag_map = {
            '标题': 'Title',
            '歌手': 'Author',
            '作曲': 'Composer',
            '作词': 'Lyricist',
            '专辑': 'WM/AlbumTitle',
            '专辑作者': 'WM/AlbumArtist',
            '年份': 'WM/Year',
            '流派': 'WM/Genre',
            '碟号': 'WM/PartOfSet',
            '音轨': 'WM/TrackNumber'
        }
        
        for key, tag in tag_map.items():
            if tag in audio:
                value = audio[tag]
                if isinstance(value, list) and len(value) > 0:
                    metadata[key] = str(value[0])
                else:
                    metadata[key] = str(value)
            else:
                metadata[key] = ''
        
        # 提取封面
        if 'WM/Picture' in audio:
            for picture in audio['WM/Picture']:
                if picture.type == 3:  # 3表示封面图片
                    metadata['封面'] = picture.data
                    break
        
        # 提取歌词
        if 'Lyrics' in audio:
            metadata['歌词'] = str(audio['Lyrics'][0])
            
    except Exception as e:
        print(f"提取WMA元数据失败 {file_path}: {str(e)}")
    
    return metadata

def extract_ogg_metadata(file_path):
    """提取OGG文件元数据"""
    metadata = {}
    
    try:
        audio = OggVorbis(file_path)
        
        # OGG标签映射
        tag_map = {
            '标题': 'title',
            '歌手': 'artist',
            '作曲': 'composer',
            '作词': 'lyricist',
            '专辑': 'album',
            '专辑作者': 'albumartist',
            '年份': 'date',
            '流派': 'genre',
            '碟号': 'discnumber',
            '音轨': 'tracknumber'
        }
        
        for key, tag in tag_map.items():
            if tag in audio:
                value = audio[tag]
                if isinstance(value, list) and len(value) > 0:
                    metadata[key] = str(value[0])
                else:
                    metadata[key] = str(value)
            else:
                metadata[key] = ''
        
        # 提取封面（OGG通常将封面存储在metadata_block_picture中）
        if 'metadata_block_picture' in audio:
            metadata['封面'] = audio['metadata_block_picture'][0]
        elif 'coverart' in audio:
            metadata['封面'] = audio['coverart'][0]
        
        # 提取歌词
        if 'lyrics' in audio:
            metadata['歌词'] = str(audio['lyrics'][0])
            
    except Exception as e:
        print(f"提取OGG元数据失败 {file_path}: {str(e)}")
    
    return metadata

def extract_generic_metadata(file_path):
    """使用通用方法提取音频文件元数据"""
    metadata = {}
    
    try:
        audio = File(file_path, easy=True)
        
        if audio is None:
            return metadata
        
        # 通用标签提取
        tag_map = {
            '标题': 'title',
            '歌手': 'artist',
            '作曲': 'composer',
            '作词': 'lyricist',
            '专辑': 'album',
            '专辑作者': 'albumartist',
            '年份': 'date',
            '流派': 'genre',
            '碟号': 'discnumber',
            '音轨': 'tracknumber'
        }
        
        for key, tag in tag_map.items():
            if tag in audio:
                value = audio[tag]
                if isinstance(value, list) and len(value) > 0:
                    metadata[key] = str(value[0])
                else:
                    metadata[key] = str(value)
            else:
                metadata[key] = ''
        
        # 尝试提取封面（非easy模式）
        audio_detailed = File(file_path)
        if audio_detailed is not None:
            # 对于FLAC文件
            if isinstance(audio_detailed, FLAC):
                if audio_detailed.pictures:
                    for picture in audio_detailed.pictures:
                        if picture.type == 3:  # 封面图片
                            metadata['封面'] = picture.data
                            break
            
            # 对于其他格式
            elif hasattr(audio_detailed, 'tags'):
                tags = audio_detailed.tags
                for key in tags.keys():
                    if 'APIC' in key or 'PIC' in key or 'picture' in key.lower():
                        if hasattr(tags[key], 'data'):
                            metadata['封面'] = tags[key].data
                            break
        
        # 提取歌词
        if 'unsyncedlyrics' in audio:
            metadata['歌词'] = str(audio['unsyncedlyrics'][0])
        elif 'lyrics' in audio:
            metadata['歌词'] = str(audio['lyrics'][0])
            
    except Exception as e:
        print(f"通用方法提取元数据失败 {file_path}: {str(e)}")
    
    return metadata

def save_cover_image(cover_data, output_path, size=(640, 640)):
    """保存封面图片"""
    try:
        # 从字节数据创建图像
        image = Image.open(io.BytesIO(cover_data))
        
        # 转换为RGB模式（如果必要）
        if image.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'P':
                image = image.convert('RGBA')
            background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
            image = background
        
        # 调整大小到640x640
        image.thumbnail(size, Image.Resampling.LANCZOS)
        
        # 创建640x640的画布
        new_image = Image.new('RGB', size, (255, 255, 255))
        
        # 将缩略图粘贴到中心
        offset = ((size[0] - image.size[0]) // 2, (size[1] - image.size[1]) // 2)
        new_image.paste(image, offset)
        
        # 保存为JPG
        new_image.save(output_path, 'JPEG', quality=90)
        return True
        
    except Exception as e:
        print(f"保存封面图片失败 {output_path}: {str(e)}")
        return False

def save_lyrics(lyrics_text, output_path):
    """保存歌词文件"""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(lyrics_text)
        return True
    except Exception as e:
        print(f"保存歌词文件失败 {output_path}: {str(e)}")
        return False

def create_excel_report(folder_path, metadata_list):
    """创建Excel报告"""
    try:
        # 获取文件夹名作为Excel文件名
        folder_name = os.path.basename(folder_path)
        if not folder_name:
            folder_name = "音频元数据"
        
        excel_path = os.path.join(folder_path, f"{folder_name}_元数据.xls")
        
        # 创建Excel工作簿
        workbook = xlwt.Workbook(encoding='utf-8')
        worksheet = workbook.add_sheet('音频元数据')
        
        # 定义列标题
        headers = ['原文件名', '新文件名', '重命名状态', '标题', '歌手', '作曲', '作词', '专辑', 
                   '专辑作者', '年份', '流派', '碟号', '音轨', '封面导出', '歌词导出']
        
        # 设置列宽
        column_widths = [40, 40, 15, 30, 30, 20, 20, 30, 20, 10, 15, 10, 10, 10, 10]
        for i, width in enumerate(column_widths):
            worksheet.col(i).width = 256 * width
        
        # 写入标题行
        for col, header in enumerate(headers):
            worksheet.write(0, col, header)
        
        # 写入数据行
        for row, item in enumerate(metadata_list, start=1):
            worksheet.write(row, 0, item['原文件名'])
            worksheet.write(row, 1, item['新文件名'])
            worksheet.write(row, 2, item['重命名状态'])
            worksheet.write(row, 3, item['标题'])
            worksheet.write(row, 4, item['歌手'])
            worksheet.write(row, 5, item['作曲'])
            worksheet.write(row, 6, item['作词'])
            worksheet.write(row, 7, item['专辑'])
            worksheet.write(row, 8, item['专辑作者'])
            worksheet.write(row, 9, item['年份'])
            worksheet.write(row, 10, item['流派'])
            worksheet.write(row, 11, item['碟号'])
            worksheet.write(row, 12, item['音轨'])
            worksheet.write(row, 13, item['封面导出'])
            worksheet.write(row, 14, item['歌词导出'])
        
        # 保存Excel文件
        workbook.save(excel_path)
        print(f"Excel报告已保存: {excel_path}")
        return excel_path
        
    except Exception as e:
        print(f"创建Excel报告失败: {str(e)}")
        return None

def main():
    """主函数"""
    print("音频文件处理工具")
    
    # 1. 获取源文件夹路径
    source_folder = get_user_input()
    print(f"正在扫描文件夹: {source_folder}")
    
    # 2. 获取所有音频文件
    audio_files = get_audio_files(source_folder)
    
    if not audio_files:
        print("未找到任何音频文件！")
        return
    
    print(f"找到 {len(audio_files)} 个音频文件")
    
    # 3. 询问是否继续
    response = input(f"是否继续处理 {len(audio_files)} 个文件？(y/n): ").strip().lower()
    if response not in ['y', 'yes', '是']:
        print("操作已取消")
        return
    
    # 4. 处理每个音频文件
    metadata_list = []
    renamed_count = 0
    
    for i, file_path in enumerate(audio_files, 1):
        print(f"\n处理文件中 ({i}/{len(audio_files)}): {os.path.basename(file_path)}")
        
        # 提取元数据
        metadata = extract_metadata(file_path)
        
        # 记录原文件名
        original_filename = os.path.basename(file_path)
        
        # 重命名文件
        artist = metadata.get('歌手', '')
        title = metadata.get('标题', '')
        
        if artist or title:
            new_file_path, rename_success, rename_message = rename_audio_file(file_path, artist, title)
            if rename_success:
                renamed_count += 1
                print(f"  重命名: {original_filename} -> {os.path.basename(new_file_path)}")
                current_file_path = new_file_path
                current_filename = os.path.basename(new_file_path)
            else:
                print(f"  重命名失败: {rename_message}")
                current_file_path = file_path
                current_filename = original_filename
        else:
            print("  无法重命名：缺少歌手或标题信息")
            current_file_path = file_path
            current_filename = original_filename
            rename_message = "缺少歌手或标题信息"
        
        # 准备记录项
        item = {
            '原文件名': original_filename,
            '新文件名': os.path.basename(current_file_path),
            '重命名状态': '成功' if (artist or title) and '成功' in rename_message else '失败',
            '标题': title,
            '歌手': artist,
            '作曲': metadata.get('作曲', ''),
            '作词': metadata.get('作词', ''),
            '专辑': metadata.get('专辑', ''),
            '专辑作者': metadata.get('专辑作者', ''),
            '年份': metadata.get('年份', ''),
            '流派': metadata.get('流派', ''),
            '碟号': metadata.get('碟号', ''),
            '音轨': metadata.get('音轨', ''),
            '封面导出': '否',
            '歌词导出': '否'
        }
        
        # 导出封面图片
        if '封面' in metadata and metadata['封面']:
            cover_path = os.path.splitext(current_file_path)[0] + '.jpg'
            if save_cover_image(metadata['封面'], cover_path):
                item['封面导出'] = '是'
                print(f"  封面导出: {os.path.basename(cover_path)}")
        
        # 导出歌词
        if '歌词' in metadata and metadata['歌词']:
            lyrics_path = os.path.splitext(current_file_path)[0] + '.lrc'
            if save_lyrics(metadata['歌词'], lyrics_path):
                item['歌词导出'] = '是'
                print(f"  歌词导出: {os.path.basename(lyrics_path)}")
        
        metadata_list.append(item)
    
    # 5. 创建Excel报告
    if metadata_list:
        excel_file = create_excel_report(source_folder, metadata_list)
        if excel_file:
            print(f"\n处理完成！")
            print(f"总计处理文件: {len(metadata_list)}")
            print(f"成功重命名文件: {renamed_count}")
            print(f"导出封面的文件: {sum(1 for item in metadata_list if item['封面导出'] == '是')}")
            print(f"导出歌词的文件: {sum(1 for item in metadata_list if item['歌词导出'] == '是')}")
            print(f"Excel报告位置: {excel_file}")
    
    print("\n程序执行完毕！")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n用户中断操作")
    except Exception as e:
        print(f"\n程序执行出错: {str(e)}")
        traceback.print_exc()