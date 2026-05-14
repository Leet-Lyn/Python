# 请帮我写个中文的 Python 脚本，批注也是中文，但是变量参数不要是中文：
# 在脚本开始前询问我 excel 文件位置（默认为：d:\Works\Attachments\标准.xlsx），源文件夹位置（默认为：d:\Works\Downloads\）。
# 读取 excel 文件，第一行为表头（字段名）。此后每一行为一条记录。
# 依据 excel 文件中的“原文件名”字段，匹配源文件夹下文件，读取其标题、艺术家、专辑数据，写入excel“名字”、“演唱”、“专辑”字段。
# 根据“名字”字段，查找该音乐的元数据。分别填入“专辑”、“盘号”、“音轨”、“年份”、“类型”、“封面”、“发行公司”、“演唱”、“作词”、“作曲”。“封面”为链接地址。
# 反复循环。

# 导入模块
import os
import re
import time
import subprocess
import pandas as pd
import musicbrainzngs as mb
from musicbrainzngs import caa
import zhconv
import requests
from mutagen import File as MutagenFile
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ---------------- 全局代理设置 ----------------
PROXY = "http://127.0.0.1:10808"
os.environ['http_proxy'] = PROXY
os.environ['https_proxy'] = PROXY
print(f"✅ 已为 MusicBrainz 设置代理：{PROXY}")

# ---------------- 初始化 ----------------
mb.set_useragent("MusicMetadataFiller", "1.0", "your-email@example.com")

LASTFM_KEY_FILE = r"e:\Documents\Creations\Scripts\Attachments\Python\LastfmAPIKey.txt"
NETEASE_API_BASE = "https://music.163.com/api"

SPOTIFY_CREDENTIALS = {
    "client_id": os.getenv("SPOTIPY_CLIENT_ID", ""),
    "client_secret": os.getenv("SPOTIPY_CLIENT_SECRET", "")
}

# ---------------- 网络 Session ----------------
def create_retry_session(retries=3, backoff_factor=1.0, connect_timeout=10, read_timeout=25, use_proxy=False):
    session = requests.Session()
    session.trust_env = False
    if use_proxy:
        session.proxies = {"http": PROXY, "https": PROXY}
    retry_strategy = Retry(
        total=retries, read=retries, connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    session.timeout = (connect_timeout, read_timeout)
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://music.163.com/',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    })
    return session

session = create_retry_session()                  # 直连
session_proxy = create_retry_session(use_proxy=True)   # 带代理

# ---------------- 工具函数 ----------------
def get_audio_metadata(file_path):
    result = {'title': '', 'artist': '', 'album': ''}
    try:
        audio = MutagenFile(file_path)
        if audio is None:
            return result
        if isinstance(audio, MP3):
            try:
                tags = EasyID3(file_path)
                result['title'] = tags.get('title', [''])[0]
                result['artist'] = tags.get('artist', [''])[0]
                result['album'] = tags.get('album', [''])[0]
            except:
                tags = ID3(file_path)
                result['title'] = str(tags.get('TIT2', ''))
                result['artist'] = str(tags.get('TPE1', ''))
                result['album'] = str(tags.get('TALB', ''))
        elif isinstance(audio, FLAC):
            result['title'] = audio.get('title', [''])[0] if audio.get('title') else ''
            result['artist'] = audio.get('artist', [''])[0] if audio.get('artist') else ''
            result['album'] = audio.get('album', [''])[0] if audio.get('album') else ''
        else:
            for key in ['title', '©nam', 'TIT2']:
                if key in audio: result['title'] = str(audio[key])
            for key in ['artist', '©ART', 'TPE1']:
                if key in audio: result['artist'] = str(audio[key])
            for key in ['album', '©alb', 'TALB']:
                if key in audio: result['album'] = str(audio[key])
    except Exception as e:
        print(f"  ⚠️ 读取元数据失败: {e}")
    return result

def find_file_in_folder(folder, filename):
    if not filename:
        return None
    if os.path.sep in filename or '/' in filename:
        full = os.path.join(folder, filename)
        if os.path.isfile(full): return full
        alt = full.replace('\\', '/').replace('/', os.path.sep)
        if os.path.isfile(alt): return alt
    for root, _, files in os.walk(folder):
        if filename in files:
            return os.path.join(root, filename)
    return None

# ---------------- MusicBrainz 相关 ----------------
def simplify_to_traditional(text):
    return zhconv.convert(text, 'zh-tw') if isinstance(text, str) else text

def search_recording_by_query(song_title, artist_name=""):
    try:
        query = f"{artist_name} {song_title}" if artist_name else song_title
        result = mb.search_recordings(query=query, limit=5, strict=False)
        if result and 'recording-list' in result:
            for rec in result['recording-list']:
                if rec.get('title') == song_title:
                    return rec
            return result['recording-list'][0]
    except Exception as e:
        print(f"  搜索录音失败: {e}")
    return None

def get_release_info_from_recording(recording):
    info = {'album': '', 'disc_number': '', 'track_number': '',
            'year': '', 'label': '', 'artist': '', 'release_group_id': ''}
    if 'release-list' not in recording or not recording['release-list']:
        return info
    release = recording['release-list'][0]
    info['release_group_id'] = release.get('release-group', {}).get('id', '')
    release_id = release.get('id')
    if not release_id:
        return info
    try:
        rd = mb.get_release_by_id(release_id, includes=['recordings', 'artists', 'labels', 'media'])['release']
        info['album'] = rd.get('title', '')
        date = rd.get('date', '')
        if date and len(date) >= 4: info['year'] = date[:4]
        if 'label-info-list' in rd and rd['label-info-list']:
            info['label'] = rd['label-info-list'][0]['label'].get('name', '')
        if 'artist-credit' in rd and rd['artist-credit']:
            artists = [ac['artist']['name'] for ac in rd['artist-credit'] if 'artist' in ac]
            info['artist'] = ' / '.join(artists)
        if 'medium-list' in rd:
            for medium in rd['medium-list']:
                for track in medium.get('track-list', []):
                    if track.get('recording', {}).get('id') == recording['id']:
                        info['track_number'] = str(track.get('number', ''))
                        info['disc_number'] = str(medium.get('position', ''))
                        break
                if info['track_number']: break
    except Exception as e:
        print(f"  获取发行详情失败: {e}")
    return info

# ---------------- 封面获取（已删除 SACAD） ----------------
def fetch_cover_from_caa(release_group_id):
    """ MusicBrainz CAA（代理） """
    if not release_group_id:
        return ""
    try:
        images = caa.get_release_group_image_list(release_group_id)
        if images and 'images' in images and images['images']:
            front = [img for img in images['images'] if img.get('front', False)]
            img = front[0] if front else images['images'][0]
            thumb = img.get('thumbnails', {}).get('large', '')
            if thumb:
                print("  🖼️ [CAA] 获取封面成功")
                return thumb
    except Exception as e:
        print(f"  [CAA] 错误: {e}")
    return ""

def fetch_cover_from_netease(song_title, artist_name=""):
    """ 网易云（直连） """
    try:
        keyword = f"{song_title} {artist_name}" if artist_name else song_title
        params = {'s': keyword, 'type': 1, 'limit': 5, 'offset': 0}
        url = f"{NETEASE_API_BASE}/search/get"
        for _ in range(3):
            try:
                resp = session.get(url, params=params, timeout=20)
                data = resp.json()
                if data['code'] == 200:
                    songs = data['result']['songs']
                    for song in songs:
                        if song['name'].lower() == song_title.lower():
                            sid = song['id']
                            detail = session.get(f"{NETEASE_API_BASE}/song/detail",
                                                params={'ids': f'[{sid}]'}, timeout=20).json()
                            if detail['code'] == 200 and detail['songs']:
                                pic = detail['songs'][0]['al']['picUrl']
                                if pic:
                                    print("  🎵 [网易云] 获取封面成功")
                                    return pic
                            pic = song.get('al', {}).get('picUrl')
                            if pic:
                                print("  🎵 [网易云] 获取封面成功（搜索结果）")
                                return pic
                    if songs and songs[0].get('al', {}).get('picUrl'):
                        print("  🎵 [网易云] 获取封面成功（模糊）")
                        return songs[0]['al']['picUrl']
                break
            except:
                time.sleep(1)
    except Exception as e:
        print(f"  [网易云] 错误: {e}")
    return ""

def fetch_cover_from_qqmusic(song_title, artist_name=""):
    """ QQ音乐（直连） """
    try:
        keyword = f"{song_title} {artist_name}" if artist_name else song_title
        url = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp"
        params = {"format": "json", "n": 5, "p": 1, "w": keyword, "cr": 1, "g_tk": 5381}
        headers = {'Referer': 'https://y.qq.com/'}
        resp = session.get(url, params=params, headers=headers, timeout=15)
        data = resp.json()
        songs = data.get("data", {}).get("song", {}).get("list", [])
        if not songs: return ""
        for song in songs:
            if song.get("name", "").lower() == song_title.lower():
                cover = song.get("album_pic") or song.get("album", {}).get("picUrl")
                if cover:
                    print("  🎵 [QQ音乐] 获取封面成功")
                    return cover
        if songs:
            cover = songs[0].get("album_pic")
            if cover:
                print("  🎵 [QQ音乐] 获取封面成功（模糊）")
                return cover
    except Exception as e:
        print(f"  [QQ音乐] 错误: {e}")
    return ""

def fetch_cover_from_itunes(song_title, artist_name=""):
    """ iTunes（直连） """
    try:
        term = f"{song_title} {artist_name}" if artist_name else song_title
        params = {"term": term, "country": "cn", "entity": "song", "limit": 1}
        resp = session.get("https://itunes.apple.com/search", params=params, timeout=15)
        data = resp.json()
        if data['resultCount'] > 0:
            cover = data['results'][0].get('artworkUrl100', '')
            if cover:
                print("  🍎 [iTunes] 获取封面成功")
                return cover.replace('100x100bb', '1000x1000bb')
    except Exception as e:
        print(f"  [iTunes] 错误: {e}")
    return ""

def fetch_cover_from_spotify(song_title, artist_name=""):
    """ Spotify（通过带代理的 session） """
    try:
        import spotipy
        from spotipy.oauth2 import SpotifyClientCredentials
    except ImportError:
        print("  [Spotify] 未安装 spotipy，跳过")
        return ""
    cred = SPOTIFY_CREDENTIALS
    if not cred["client_id"] or not cred["client_secret"]:
        print("  [Spotify] 未配置凭证，跳过")
        return ""
    try:
        client_mgr = SpotifyClientCredentials(
            client_id=cred["client_id"],
            client_secret=cred["client_secret"],
            requests_session=session_proxy
        )
        sp = spotipy.Spotify(client_credentials_manager=client_mgr)
        query = f"track:{song_title}"
        if artist_name: query += f" artist:{artist_name}"
        results = sp.search(q=query, type='track', limit=3)
        tracks = results['tracks']['items']
        if not tracks: return ""
        for track in tracks:
            if track['name'].lower() == song_title.lower():
                images = track['album']['images']
                if images:
                    print("  🟢 [Spotify] 获取封面成功")
                    return images[0]['url']
        if tracks[0]['album']['images']:
            print("  🟢 [Spotify] 获取封面成功（模糊）")
            return tracks[0]['album']['images'][0]['url']
    except Exception as e:
        print(f"  [Spotify] 错误: {e}")
    return ""

def fetch_best_cover(song_title, artist_name, album_name, release_group_id):
    """ 按顺序尝试所有封面来源（已移除 SACAD） """
    methods = [
        ("MusicBrainz CAA", lambda: fetch_cover_from_caa(release_group_id)),
        ("网易云", lambda: fetch_cover_from_netease(song_title, artist_name)),
        ("QQ音乐", lambda: fetch_cover_from_qqmusic(song_title, artist_name)),
        ("iTunes", lambda: fetch_cover_from_itunes(song_title, artist_name)),
        ("Spotify", lambda: fetch_cover_from_spotify(song_title, artist_name)),
    ]
    for name, func in methods:
        print(f"  尝试 {name} 获取封面...")
        try:
            url = func()
            if url:
                print(f"  ✅ 封面已由 {name} 提供: {url}")
                return url
            else:
                print(f"     {name} 未返回有效封面。")
        except Exception as e:
            print(f"     {name} 异常: {e}")
        time.sleep(0.3)
    return ""

# ---------------- 歌词/人员 ----------------
def search_netease_song(song_title, artist_name=""):
    try:
        keyword = f"{song_title} {artist_name}" if artist_name else song_title
        resp = session.get(f"{NETEASE_API_BASE}/search/get", params={"s": keyword, "type": 1, "limit": 5, "offset": 0}, timeout=20)
        data = resp.json()
        if data.get("code") != 200: return None, None
        songs = data["result"]["songs"]
        for s in songs:
            if s['name'].lower() == song_title.lower():
                return s['id'], s['name']
        return songs[0]['id'], songs[0]['name'] if songs else (None, None)
    except:
        return None, None

def get_song_lyrics(song_id):
    if not song_id: return None
    for _ in range(3):
        try:
            resp = session.get(f"{NETEASE_API_BASE}/song/lyric", params={"id": song_id, "lv": 1}, timeout=20)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("code") == 200 and data.get("lrc"):
                    return data["lrc"]["lyric"]
        except:
            time.sleep(1)
    return None

def parse_lyrics_for_credits(lyrics):
    result = {'lyricist': '', 'composer': '', 'arranger': ''}
    if not lyrics: return result
    for line in lyrics.split('\n')[:50]:
        line = line.strip()
        m = re.search(r'作词[\s:：]+([^,\n\r]+)', line)
        if m and not result['lyricist']: result['lyricist'] = m.group(1).strip()
        m = re.search(r'作曲[\s:：]+([^,\n\r]+)', line)
        if m and not result['composer']: result['composer'] = m.group(1).strip()
        m = re.search(r'编曲[\s:：]+([^,\n\r]+)', line)
        if m and not result['arranger']: result['arranger'] = m.group(1).strip()
        if not result['lyricist'] or not result['composer']:
            mixed = re.search(r'词[：:]\s*([^曲]+)曲[：:]\s*([^编]+)', line)
            if mixed:
                if not result['lyricist']: result['lyricist'] = mixed.group(1).strip()
                if not result['composer']: result['composer'] = mixed.group(2).strip()
        if not result['arranger']:
            arr = re.search(r'编曲[：:]\s*([^,\n\r]+)', line)
            if arr: result['arranger'] = arr.group(1).strip()
    return result

def fetch_netease_credits(song_title, artist_name=""):
    sid, _ = search_netease_song(song_title, artist_name)
    if sid:
        lyrics = get_song_lyrics(sid)
        if lyrics:
            credits = parse_lyrics_for_credits(lyrics)
            if any(credits.values()):
                print(f"  📝 作词={credits['lyricist']}, 作曲={credits['composer']}, 编曲={credits['arranger']}")
            return credits
    return {'lyricist': '', 'composer': '', 'arranger': ''}

# ---------------- Last.fm ----------------
def read_lastfm_api_key():
    if not os.path.exists(LASTFM_KEY_FILE): return None
    with open(LASTFM_KEY_FILE, 'r', encoding='utf-8') as f:
        key = f.read().strip()
        return key if key else None

def get_lastfm_tags(artist, title, api_key):
    if not api_key or not artist or not title: return ""
    params = {"method": "track.getTopTags", "artist": artist, "track": title,
              "api_key": api_key, "format": "json"}
    try:
        resp = session.get("http://ws.audioscrobbler.com/2.0/", params=params, timeout=10)
        data = resp.json()
        if "toptags" in data and "tag" in data["toptags"]:
            return ", ".join([t["name"] for t in data["toptags"]["tag"][:5]])
    except:
        pass
    return ""

# ---------------- 主元数据填充 ----------------
def fetch_all_metadata(song_title, artist_name, album_name, lastfm_key):
    meta = {'disc_number': '', 'track_number': '', 'year': '', 'cover_url': '',
            'label': '', 'genre': '', 'lyricist': '', 'composer': '', 'arranger': ''}
    if not song_title:
        return meta

    # MusicBrainz 搜索（代理）
    recording = None
    if album_name:
        try:
            res = mb.search_recordings(query=f"{album_name} {song_title}", limit=5, strict=False)
            if res and 'recording-list' in res:
                recording = res['recording-list'][0]
        except: pass
    if not recording:
        recording = search_recording_by_query(song_title, artist_name)
        if not recording:
            trad = simplify_to_traditional(song_title)
            if trad != song_title:
                recording = search_recording_by_query(trad, artist_name)
        if not recording:
            recording = search_recording_by_query(song_title, "")
    release_group_id = ""
    if recording:
        print(f"  匹配录音: {recording.get('title', 'Unknown')}")
        rel_info = get_release_info_from_recording(recording)
        meta['disc_number'] = rel_info['disc_number']
        meta['track_number'] = rel_info['track_number']
        meta['year'] = rel_info['year']
        meta['label'] = rel_info['label']
        release_group_id = rel_info['release_group_id']
    else:
        print("  MusicBrainz 未找到匹配")

    # 封面多源尝试
    meta['cover_url'] = fetch_best_cover(song_title, artist_name, album_name, release_group_id)

    # 流派
    if lastfm_key and artist_name:
        meta['genre'] = get_lastfm_tags(artist_name, song_title, lastfm_key)

    # 作词/作曲
    credits = fetch_netease_credits(song_title, artist_name)
    meta.update(credits)
    return meta

# ---------------- 运行流程 ----------------
def run_once():
    default_excel = r"d:\Works\Attachments\标准.xlsx"
    excel_path = input(f"请输入 Excel 文件路径（直接回车使用默认：{default_excel}）: ").strip()
    if not excel_path: excel_path = default_excel
    if not os.path.exists(excel_path):
        print(f"错误：文件不存在 - {excel_path}")
        return

    default_source = r"d:\Works\Downloads"
    source_folder = input(f"请输入音频文件夹路径（默认：{default_source}）: ").strip()
    if not source_folder: source_folder = default_source
    if not os.path.isdir(source_folder):
        print(f"错误：文件夹不存在 - {source_folder}")
        return

    print(f"\n读取 Excel: {excel_path}")
    df = pd.read_excel(excel_path, dtype=str)
    print(f"共 {len(df)} 条记录，字段：{list(df.columns)}")

    if '原文件名' not in df.columns:
        print("缺少“原文件名”列，退出。")
        return

    required = ['名字', '演唱', '专辑', '盘号', '音轨', '年份', '类型', '封面', '发行公司', '作词', '作曲', '编曲']
    for col in required:
        if col not in df.columns:
            df[col] = ''
            print(f"新增列：{col}")

    # 第一步：读取音频元数据
    print("\n--- 第一步：读取音频元数据 ---")
    for idx, row in df.iterrows():
        orig = str(row['原文件名'])
        if not orig or orig == 'nan':
            print(f"[{idx+1}/{len(df)}] 空文件名，跳过")
            continue
        file_path = find_file_in_folder(source_folder, orig)
        if not file_path:
            print(f"[{idx+1}/{len(df)}] 找不到 {orig}")
            continue
        print(f"[{idx+1}/{len(df)}] {orig} → {file_path}")
        audio = get_audio_metadata(file_path)
        df.at[idx, '名字'] = audio['title']
        df.at[idx, '演唱'] = audio['artist']
        df.at[idx, '专辑'] = audio['album']
        df.to_excel(excel_path, index=False)
        print(f"  已写: 名字={audio['title']}, 演唱={audio['artist']}, 专辑={audio['album']}")

    # 第二步：补充其他元数据
    lastfm_key = read_lastfm_api_key()
    print("\n--- 第二步：查询网络元数据 ---")
    success = 0
    for idx, row in df.iterrows():
        name = str(row['名字']) if pd.notna(row['名字']) else ''
        artist = str(row['演唱']) if pd.notna(row['演唱']) else ''
        album = str(row['专辑']) if pd.notna(row['专辑']) else ''
        if not name: continue
        print(f"\n[{idx+1}/{len(df)}] {name} - {artist} ({album})")
        try:
            meta = fetch_all_metadata(name, artist, album, lastfm_key)
            for key in ['盘号', '音轨', '年份', '封面', '发行公司', '类型', '作词', '作曲', '编曲']:
                df.at[idx, key] = meta.get(key, '')
            success += 1
            df.to_excel(excel_path, index=False)
            print("  ✅ 已更新")
            time.sleep(0.6)
        except Exception as e:
            print(f"  ❌ 出错: {e}")

    df.to_excel(excel_path, index=False)
    print(f"\n===== 完成 =====\n共 {len(df)} 条，成功补充 {success} 条\n保存至: {excel_path}")

def main():
    while True:
        print("\n" + "="*60)
        print("音乐元数据批量处理工具（多源封面+代理，已移除SACAD）")
        print("="*60)
        run_once()
        if input("\n继续处理其他文件？(y/n): ").strip().lower() != 'y':
            break
    print("程序结束。")

if __name__ == "__main__":
    main()