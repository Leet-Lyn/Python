# 请帮我写个中文的 Python 脚本，批注也是中文，但是变量参数不要是中文：
# 在脚本开始前询问我 excel 文件位置（默认为：d:\Works\Attachments\标准.xlsx），源文件夹位置（默认为：d:\Works\Downloads\）。
# 读取 excel 文件，第一行为表头（字段名）。此后每一行为一条记录。
# 依据 excel 文件中的“原文件名”字段，匹配源文件夹下的文件，将 excel ，“名字”、“专辑”、“盘号”、“音轨”、“年份”、“类型”、“封面”、“发行公司”、“演唱”、“作词”、“作曲”、“编曲”，作为元数据写入文件。
# “封面”链接下载后转为640*640 大小 jpg 格式嵌入。

# 导入模块
import os
import base64
import pandas as pd
import requests
from mutagen import File as MutagenFile
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4, MP4Cover
from mutagen.flac import FLAC, Picture
from mutagen.oggvorbis import OggVorbis
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TRCK, TPOS, TDRC, TCON, TCOP, TCOM, TEXT, TXXX, APIC
from PIL import Image
from io import BytesIO

# ------------------- 支持的文件扩展名 -------------------
SUPPORTED_EXT = ('.mp3', '.m4a', '.flac', '.ogg', '.wav')  # 主要支持这些

def find_file_in_folder(folder_path, filename):
    """在文件夹（包括子文件夹）中查找文件"""
    if os.path.sep in filename or '/' in filename:
        full_path = os.path.join(folder_path, filename)
        if os.path.isfile(full_path):
            return full_path
        alt_path = full_path.replace('\\', '/').replace('/', os.path.sep)
        if os.path.isfile(alt_path):
            return alt_path
    for root, _, files in os.walk(folder_path):
        if filename in files:
            return os.path.join(root, filename)
    return None

def download_and_resize_image(url, target_size=(640, 640)):
    """下载图片，缩放为指定尺寸的 JPEG，返回二进制数据"""
    if not url or not isinstance(url, str):
        return None
    try:
        # 添加浏览器头，避免 403 错误
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        resp = requests.get(url, timeout=15, headers=headers)
        resp.raise_for_status()
        img = Image.open(BytesIO(resp.content))
        if img.mode in ('RGBA', 'LA', 'P'):
            img = img.convert('RGB')
        img = img.resize(target_size, Image.LANCZOS)
        output = BytesIO()
        img.save(output, format='JPEG', quality=85)
        return output.getvalue()
    except Exception as e:
        print(f"    封面处理失败 ({url}): {e}")
        return None

def clear_old_cover(audio):
    """清除音频文件中已有的封面图片"""
    file_path = audio.filename if hasattr(audio, 'filename') else ''
    ext = os.path.splitext(file_path)[1].lower()
    try:
        # MP3文件：使用ID3标签的delall方法删除所有APIC帧
        if ext == '.mp3':
            if isinstance(audio, MP3) and audio.tags is not None:
                audio.tags.delall('APIC')
                audio.save()
        # M4A文件：删除covr键
        elif ext == '.m4a':
            if 'covr' in audio:
                del audio['covr']
                audio.save()
        # FLAC文件：调用clear_pictures
        elif ext == '.flac':
            if isinstance(audio, FLAC):
                audio.clear_pictures()
                audio.save()
        # OGG文件：清除 METADATA_BLOCK_PICTURE 及其他非标准封面
        elif ext == '.ogg':
            if 'METADATA_BLOCK_PICTURE' in audio:
                del audio['METADATA_BLOCK_PICTURE']
            if 'COVERART' in audio:
                del audio['COVERART']
            if 'COVERARTMIME' in audio:
                del audio['COVERARTMIME']
            audio.save()
    except Exception as e:
        # 不抛出异常，继续处理
        pass

def set_mp3_tags(file_path, metadata, cover_data):
    """写入 MP3 标签（ID3v2.3）- 所有字段只写入一次"""
    try:
        try:
            tags = ID3(file_path)
        except:
            tags = ID3()
        tags.delall('APIC')
        
        # 以下字段每个只添加一次
        if metadata.get('title'):
            tags.add(TIT2(encoding=3, text=metadata['title']))
        if metadata.get('artist'):
            tags.add(TPE1(encoding=3, text=metadata['artist']))
        if metadata.get('album'):
            tags.add(TALB(encoding=3, text=metadata['album']))
        if metadata.get('tracknumber'):
            tags.add(TRCK(encoding=3, text=str(metadata['tracknumber'])))
        if metadata.get('discnumber'):
            tags.add(TPOS(encoding=3, text=str(metadata['discnumber'])))
        if metadata.get('date'):
            tags.add(TDRC(encoding=3, text=str(metadata['date'])))
        if metadata.get('genre'):
            tags.add(TCON(encoding=3, text=metadata['genre']))
        if metadata.get('label'):
            tags.add(TCOP(encoding=3, text=metadata['label']))
        # 作词：标准 TEXT，不重复添加 TXXX
        if metadata.get('lyricist'):
            tags.add(TEXT(encoding=3, text=metadata['lyricist']))
        # 作曲：标准 TCOM
        if metadata.get('composer'):
            tags.add(TCOM(encoding=3, text=metadata['composer']))
        # 编曲：无标准字段，仅用 TXXX
        if metadata.get('arranger'):
            tags.add(TXXX(encoding=3, desc='Arranger', text=metadata['arranger']))
        
        if cover_data:
            apic = APIC(encoding=3, mime='image/jpeg', type=3, desc='Cover', data=cover_data)
            tags.add(apic)
        
        tags.save(file_path, v2_version=3)
        return True
    except Exception as e:
        print(f"    MP3 写入失败: {e}")
        return False

def set_m4a_tags(file_path, metadata, cover_data):
    """写入 M4A (MP4) 标签 - 只写入一次"""
    try:
        audio = MP4(file_path)
        if 'covr' in audio:
            del audio['covr']
        
        # 清理可能的旧自定义框（避免重复）
        for key in list(audio.keys()):
            if key.startswith('----:com.apple.iTunes:'):
                del audio[key]
        
        if metadata.get('title'):
            audio['\xa9nam'] = metadata['title']
        if metadata.get('artist'):
            audio['\xa9ART'] = metadata['artist']
        if metadata.get('album'):
            audio['\xa9alb'] = metadata['album']
        if metadata.get('tracknumber'):
            audio['trkn'] = [(int(metadata['tracknumber']), 0)]
        if metadata.get('discnumber'):
            audio['disk'] = [(int(metadata['discnumber']), 0)]
        if metadata.get('date'):
            audio['\xa9day'] = metadata['date']
        if metadata.get('genre'):
            audio['\xa9gen'] = metadata['genre']
        if metadata.get('label'):
            audio['cprt'] = metadata['label']
        # 作词
        if metadata.get('lyricist'):
            audio['----:com.apple.iTunes:Lyricist'] = metadata['lyricist']
        # 作曲：标准 ©wrt 加上自定义框
        if metadata.get('composer'):
            audio['\xa9wrt'] = metadata['composer']
            audio['----:com.apple.iTunes:Composer'] = metadata['composer']
        # 编曲
        if metadata.get('arranger'):
            audio['----:com.apple.iTunes:Arranger'] = metadata['arranger']
        
        if cover_data:
            audio['covr'] = [MP4Cover(cover_data, MP4Cover.FORMAT_JPEG)]
        
        audio.save()
        return True
    except Exception as e:
        print(f"    M4A 写入失败: {e}")
        return False

def set_flac_tags(file_path, metadata, cover_data):
    """写入 FLAC 标签 - 只写入一次"""
    try:
        audio = FLAC(file_path)
        audio.clear_pictures()
        
        # 清空现有 Vorbis 注释（可选，避免残留，但保留原始字段也可以）
        # 我们采用覆盖方式，不删除全部，只更新给定的字段
        if metadata.get('title'):
            audio['title'] = metadata['title']
        if metadata.get('artist'):
            audio['artist'] = metadata['artist']
        if metadata.get('album'):
            audio['album'] = metadata['album']
        if metadata.get('tracknumber'):
            audio['tracknumber'] = str(metadata['tracknumber'])
        if metadata.get('discnumber'):
            audio['discnumber'] = str(metadata['discnumber'])
        if metadata.get('date'):
            audio['date'] = str(metadata['date'])
        if metadata.get('genre'):
            audio['genre'] = metadata['genre']
        if metadata.get('label'):
            audio['organization'] = metadata['label']
        if metadata.get('lyricist'):
            audio['lyricist'] = metadata['lyricist']
        if metadata.get('composer'):
            audio['composer'] = metadata['composer']
        if metadata.get('arranger'):
            audio['arranger'] = metadata['arranger']
        
        if cover_data:
            pic = Picture()
            pic.type = 3
            pic.mime = 'image/jpeg'
            pic.data = cover_data
            pic.width = 640
            pic.height = 640
            pic.depth = 24
            audio.add_picture(pic)
        
        audio.save()
        return True
    except Exception as e:
        print(f"    FLAC 写入失败: {e}")
        return False

def set_ogg_tags(file_path, metadata, cover_data):
    """写入 OGG Vorbis 标签 - 使用标准字段名，只写入一次，封面使用 METADATA_BLOCK_PICTURE"""
    try:
        audio = OggVorbis(file_path)
        # 删除旧的封面相关字段
        if 'METADATA_BLOCK_PICTURE' in audio:
            del audio['METADATA_BLOCK_PICTURE']
        if 'COVERART' in audio:
            del audio['COVERART']
        if 'COVERARTMIME' in audio:
            del audio['COVERARTMIME']
        
        # 写入标准字段（使用大写，只一次）
        if metadata.get('title'):
            audio['TITLE'] = metadata['title']
        if metadata.get('artist'):
            audio['ARTIST'] = metadata['artist']
        if metadata.get('album'):
            audio['ALBUM'] = metadata['album']
        if metadata.get('tracknumber'):
            audio['TRACKNUMBER'] = str(metadata['tracknumber'])
        if metadata.get('discnumber'):
            audio['DISCNUMBER'] = str(metadata['discnumber'])
        if metadata.get('date'):
            audio['DATE'] = str(metadata['date'])
        if metadata.get('genre'):
            audio['GENRE'] = metadata['genre']
        if metadata.get('label'):
            audio['ORGANIZATION'] = metadata['label']
        if metadata.get('lyricist'):
            audio['LYRICIST'] = metadata['lyricist']
        if metadata.get('composer'):
            audio['COMPOSER'] = metadata['composer']
        if metadata.get('arranger'):
            audio['ARRANGER'] = metadata['arranger']
        
        # 嵌入封面：使用 Picture.write() 获取二进制，然后 base64 编码
        if cover_data:
            pic = Picture()
            pic.type = 3
            pic.mime = 'image/jpeg'
            pic.data = cover_data
            pic.width = 640
            pic.height = 640
            pic.depth = 24
            # write() 方法返回二进制串，需要 base64 编码后存入
            b64_data = base64.b64encode(pic.write()).decode('ascii')
            audio['METADATA_BLOCK_PICTURE'] = b64_data
            print("    METADATA_BLOCK_PICTURE 封面嵌入成功")
        
        audio.save()
        return True
    except Exception as e:
        print(f"    OGG 写入失败: {e}")
        return False

def set_wav_tags(file_path, metadata, cover_data):
    """WAV 标签写入支持有限，跳过"""
    print("    WAV 格式元数据写入支持有限，跳过写入")
    return False

def set_common_tags(audio, metadata, cover_data):
    """根据扩展名调用对应的写入函数"""
    file_path = audio.filename if hasattr(audio, 'filename') else ''
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.mp3':
        return set_mp3_tags(file_path, metadata, cover_data)
    elif ext == '.m4a':
        return set_m4a_tags(file_path, metadata, cover_data)
    elif ext == '.flac':
        return set_flac_tags(file_path, metadata, cover_data)
    elif ext == '.ogg':
        return set_ogg_tags(file_path, metadata, cover_data)
    elif ext == '.wav':
        return set_wav_tags(file_path, metadata, cover_data)
    else:
        print(f"    不支持的文件格式: {ext}")
        return False

# ------------------- 单次运行 -------------------
def run_once():
    default_source = r"d:\Works\Downloads"
    source_folder = input(f"请输入源文件夹路径（默认 {default_source}）: ").strip()
    if not source_folder:
        source_folder = default_source
    if not os.path.isdir(source_folder):
        print(f"错误：文件夹不存在 - {source_folder}")
        return

    default_excel = r"d:\Works\Attachments\标准.xlsx"
    excel_path = input(f"请输入 Excel 文件路径（默认 {default_excel}）: ").strip()
    if not excel_path:
        excel_path = default_excel
    if not os.path.exists(excel_path):
        print(f"错误：文件不存在 - {excel_path}")
        return

    print(f"\n读取 Excel: {excel_path}")
    df = pd.read_excel(excel_path, dtype=str)
    if '原文件名' not in df.columns:
        print("错误：缺少“原文件名”列")
        return

    field_mapping = {
        '名字': 'title', '演唱': 'artist', '专辑': 'album', '盘号': 'discnumber',
        '音轨': 'tracknumber', '年份': 'date', '类型': 'genre', '发行公司': 'label',
        '作词': 'lyricist', '作曲': 'composer', '编曲': 'arranger', '封面': 'cover_url'
    }

    success = 0
    for idx, row in df.iterrows():
        filename = str(row['原文件名']) if pd.notna(row['原文件名']) else ''
        if not filename or filename == 'nan':
            continue

        file_path = find_file_in_folder(source_folder, filename)
        if not file_path:
            print(f"[{idx+1}] 找不到文件: {filename}")
            continue

        # 提取元数据
        metadata = {}
        cover_url = ''
        for col, key in field_mapping.items():
            if col in df.columns and pd.notna(row[col]):
                val = str(row[col]).strip()
                if val and val != 'nan':
                    if key == 'cover_url':
                        cover_url = val
                    else:
                        metadata[key] = val

        # 下载并处理封面
        cover_data = None
        if cover_url:
            print(f"[{idx+1}] 下载封面: {cover_url}")
            cover_data = download_and_resize_image(cover_url, (640, 640))
            if cover_data:
                print("    封面下载并压缩成功")
            else:
                print("    封面处理失败，将不嵌入")

        # 打开音频文件
        audio = MutagenFile(file_path)
        if audio is None:
            print(f"[{idx+1}] 无法识别音频格式: {filename}")
            continue

        # 清除旧封面
        clear_old_cover(audio)

        # 写入新标签
        if set_common_tags(audio, metadata, cover_data):
            success += 1
            print(f"[{idx+1}] ✅ 写入成功: {filename}")
        else:
            print(f"[{idx+1}] ❌ 写入失败: {filename}")

    print(f"\n本次处理完成，成功 {success}/{len(df)}")

# ------------------- 主循环 -------------------
def main():
    while True:
        print("\n" + "="*60)
        print("音乐元数据反向写入工具（Excel → 音频文件）")
        print("="*60)
        run_once()
        if input("\n是否继续？(y/n，默认 n): ").strip().lower() != 'y':
            break
    print("程序结束。")

if __name__ == "__main__":
    main()