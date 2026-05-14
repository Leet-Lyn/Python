# 请帮我写个中文的 Python 脚本，批注也是中文，但是变量参数不要是中文：
# 在脚本开始前询问我 excel 文件位置（默认为：d:\Works\Attachments\标准.xlsx）。
# 读取 excel 文件，第一行为表头（字段名）。此后每一行为一条记录。
# 依据 excel 文件中的“名字”、“平台”字段，查询该游戏在该平台下封面、类型、发行公司填入“封面”、“类型”及“发行公司”字段里。“名字内可能含有其版本”。“封面”为链接地址。
# 反复循环。

# 导入模块
import os
import re
import time
import pandas as pd
import requests

# ------------------- 配置区域 -------------------
# 代理设置（如需代理请取消注释并填写地址）
PROXY = {
     "http": "http://127.0.0.1:10808",
     "https": "http://127.0.0.1:10808"
}

# SteamGridDB API Key 文件路径
SGDB_API_KEY_FILE = r"e:\Documents\Creations\Scripts\Attachments\Python\SteamGridDBAPIKey.txt"

# IGDB 凭证文件路径
IGDB_CLIENT_ID_FILE = r"e:\Documents\Creations\Scripts\Attachments\Python\IGDBClientID.txt"
IGDB_CLIENT_SECRET_FILE = r"e:\Documents\Creations\Scripts\Attachments\Python\IGDBClientSecret.txt"

# 请求延迟（秒），避免触发 API 速率限制
REQUEST_DELAY = 0.8

# IGDB 平台名称 -> 平台 ID 映射
PLATFORM_MAPPING_IGDB = {
    "pc": 6, "windows": 6, "steam": 6,
    "ps5": 167, "playstation5": 167,
    "ps4": 48, "playstation4": 48,
    "ps3": 9, "playstation3": 9,
    "ps2": 8, "playstation2": 8,
    "ps1": 7, "playstation1": 7,
    "xbox series x": 169, "xbox series s": 169,
    "xbox one": 49, "xbox360": 12, "xbox 360": 12,
    "switch": 130, "nintendo switch": 130,
    "nes": 13, "nintendo entertainment system": 13, "nintendo": 13,
    "snes": 14, "super nintendo": 14,
    "n64": 15, "nintendo 64": 15,
    "gameboy": 16, "gb": 16, "game boy": 16,
    "3ds": 37, "nintendo 3ds": 37,
    "nds": 20, "nintendo ds": 20,
    "wii u": 41, "wii": 11,
    "ios": 39, "android": 34, "mac": 14, "linux": 3,
}

# ------------------- 工具函数 -------------------
def clean_game_name(name):
    """清理游戏名称：删除所有中英文括号及内部内容"""
    if not name:
        return ""
    cleaned = re.sub(r'（[^）]*）', '', name)
    cleaned = re.sub(r'\([^)]*\)', '', cleaned)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned if cleaned else name.strip()

def read_file_content(file_path, prompt_name):
    """读取文本文件内容，若文件不存在则提示用户输入并可选择保存"""
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if content:
                return content
    print(f"未找到 {prompt_name} 文件：{file_path}")
    user_input = input(f"请输入 {prompt_name}（直接回车跳过）: ").strip()
    if not user_input:
        return None
    save_choice = input(f"是否保存 {prompt_name} 到文件？(y/n): ").strip().lower()
    if save_choice == 'y':
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(user_input)
        print("已保存")
    return user_input

def get_proxies():
    return PROXY if PROXY else None

# ------------------- 数据源查询函数 -------------------
# 1. SteamGridDB 只负责封面
def search_sgdb_cover(game_name, api_key):
    """返回封面 URL 或空字符串"""
    if not api_key or not game_name:
        return ""
    base_url = "https://www.steamgriddb.com/api/v2"
    headers = {"Authorization": f"Bearer {api_key}"}
    proxies = get_proxies()

    try:
        search_url = f"{base_url}/search/autocomplete/{requests.utils.quote(game_name)}"
        resp = requests.get(search_url, headers=headers, timeout=15, proxies=proxies)
        resp.raise_for_status()
        data = resp.json()
        if not data.get("data"):
            print(f"    [SteamGridDB] 未搜索到游戏: {game_name}")
            return ""
        game_id = data["data"][0]["id"]

        grids_url = f"{base_url}/grids/game/{game_id}"
        params = {"limit": 1}
        resp = requests.get(grids_url, headers=headers, params=params, timeout=15, proxies=proxies)

        if resp.status_code in (400, 404):
            print(f"    [SteamGridDB] 无可用封面资源 (状态码: {resp.status_code})")
            return ""
        resp.raise_for_status()
        grids_data = resp.json()
        if grids_data.get("data") and len(grids_data["data"]) > 0:
            for grid in grids_data["data"]:
                if not grid.get("nsfw", False):
                    cover_url = grid["url"]
                    print(f"    [SteamGridDB] 找到封面 → {cover_url}")
                    return cover_url
            cover_url = grids_data["data"][0]["url"]
            print(f"    [SteamGridDB] 找到封面 (NSFW) → {cover_url}")
            return cover_url
        else:
            print(f"    [SteamGridDB] 无封面")
            return ""
    except Exception as e:
        print(f"    [SteamGridDB] 查询出错: {e}")
        return ""

# 2. IGDB 查询（返回封面、类型、发行商）
def get_igdb_access_token(client_id, client_secret):
    url = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }
    try:
        resp = requests.post(url, params=params, timeout=15, proxies=get_proxies())
        resp.raise_for_status()
        return resp.json().get("access_token")
    except Exception as e:
        print(f"    [IGDB] 获取令牌失败: {e}")
        return None

def search_igdb_all(game_name, platform_name, client_id, client_secret):
    """
    查询 IGDB，返回 (cover_url, genre, publisher)，无论是否有封面。
    """
    def _do_search(name, platform_id=None):
        token = get_igdb_access_token(client_id, client_secret)
        if not token:
            return "", "", ""
        fields = "name,cover.url,genres.name,involved_companies.company.name,involved_companies.publisher"
        if platform_id:
            query = f'fields {fields}; search "{name}"; where platforms = [{platform_id}]; limit 5;'
        else:
            query = f'fields {fields}; search "{name}"; limit 5;'
        headers = {
            "Client-ID": client_id,
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        url = "https://api.igdb.com/v4/games"
        try:
            resp = requests.post(url, headers=headers, data=query, timeout=15, proxies=get_proxies())
            resp.raise_for_status()
            data = resp.json()
            if data and isinstance(data, list):
                for game in data:
                    cover_url = ""
                    if "cover" in game and "url" in game["cover"]:
                        cover_url = game["cover"]["url"]
                        if cover_url.startswith("//"):
                            cover_url = "https:" + cover_url
                        cover_url = cover_url.replace("t_thumb", "t_cover_big")
                    genre = ""
                    if "genres" in game and game["genres"]:
                        genre = game["genres"][0].get("name", "")
                    publisher = ""
                    if "involved_companies" in game:
                        for comp in game["involved_companies"]:
                            if comp.get("publisher") and "company" in comp:
                                publisher = comp["company"].get("name", "")
                                break
                    # 只要找到匹配的游戏，就返回提取到的信息（封面可能为空）
                    return cover_url, genre, publisher
        except Exception:
            pass
        return "", "", ""

    # 解析平台ID
    platform_id = None
    if platform_name:
        platform_lower = platform_name.lower()
        for key, pid in PLATFORM_MAPPING_IGDB.items():
            if key in platform_lower or platform_lower in key:
                platform_id = pid
                break

    # 尝试平台过滤
    cover, genre, publisher = _do_search(game_name, platform_id)
    if cover or genre or publisher:   # 只要有任何信息就认为匹配成功
        if cover:
            print(f"    [IGDB] 找到封面（平台过滤）→ {cover}")
        if genre:
            print(f"    [IGDB] 获取到类型：{genre}")
        if publisher:
            print(f"    [IGDB] 获取到发行公司：{publisher}")
        return cover, genre, publisher

    # 尝试无平台过滤
    if platform_id:
        cover, genre, publisher = _do_search(game_name, None)
        if cover or genre or publisher:
            if cover:
                print(f"    [IGDB] 找到封面（无平台限制）→ {cover}")
            if genre:
                print(f"    [IGDB] 获取到类型：{genre}")
            if publisher:
                print(f"    [IGDB] 获取到发行公司：{publisher}")
            return cover, genre, publisher

    print(f"    [IGDB] 未找到任何匹配信息")
    return "", "", ""

# 3. Steam 商店查询
def search_steam_all(game_name):
    """返回 (cover_url, genre, publisher)"""
    if not game_name:
        return "", "", ""
    try:
        search_url = "https://store.steampowered.com/api/storesearch/"
        resp = requests.get(search_url, params={"term": game_name, "l": "zh"},
                            timeout=15, proxies=get_proxies())
        resp.raise_for_status()
        data = resp.json()
        if not data.get("items"):
            print(f"    [Steam] 未搜索到游戏")
            return "", "", ""
        app_id = data["items"][0]["id"]

        detail_url = "https://store.steampowered.com/api/appdetails"
        resp = requests.get(detail_url, params={"appids": app_id},
                            timeout=15, proxies=get_proxies())
        resp.raise_for_status()
        detail = resp.json()
        if str(app_id) not in detail or not detail[str(app_id)]["success"]:
            print(f"    [Steam] 无法获取详情")
            return "", "", ""

        app = detail[str(app_id)]["data"]
        cover_url = app.get("header_image", "")
        genres = app.get("genres", [])
        genre = genres[0]["description"] if genres else ""
        publishers = app.get("publishers", [])
        publisher = publishers[0] if publishers else ""

        if cover_url:
            print(f"    [Steam] 找到封面 → {cover_url}")
        if genre:
            print(f"    [Steam] 获取到类型：{genre}")
        if publisher:
            print(f"    [Steam] 获取到发行公司：{publisher}")
        return cover_url, genre, publisher
    except Exception as e:
        print(f"    [Steam] 查询出错: {e}")
        return "", "", ""

# ------------------- 安全保存 Excel -------------------
def safe_save_excel(df, path):
    """每次保存都尝试，若失败则提示用户"""
    while True:
        try:
            df.to_excel(path, index=False)
            return True
        except PermissionError:
            print(f"❌ 文件被占用：{path}")
            print("   请关闭 Excel 后按回车重试，或输入 's' 另存")
            choice = input(">>> ").strip().lower()
            if choice == 's':
                new_path = input("请输入新文件名（如：封面结果.xlsx）: ").strip()
                if not new_path:
                    new_path = "封面结果.xlsx"
                dir_name = os.path.dirname(path)
                new_path = os.path.join(dir_name, new_path) if dir_name else new_path
                try:
                    df.to_excel(new_path, index=False)
                    print(f"✅ 已保存到 {new_path}")
                    return True
                except Exception as e:
                    print(f"另存失败：{e}")
                    return False
            # 否则重试
        except Exception as e:
            print(f"保存出错：{e}")
            return False

# ------------------- 单次批量处理 -------------------
def run_once():
    default_excel = r"d:\Works\Attachments\标准.xlsx"
    excel_path = input(f"请输入 Excel 文件路径（直接回车使用默认：{default_excel}）: ").strip()
    if not excel_path:
        excel_path = default_excel
    if not os.path.exists(excel_path):
        print(f"错误：文件不存在 - {excel_path}")
        return

    print(f"\n正在读取 Excel：{excel_path}")
    try:
        df = pd.read_excel(excel_path, dtype=str)
        print(f"成功读取 {len(df)} 行")
    except Exception as e:
        print(f"读取失败：{e}")
        return

    # 检查必要列
    if "名字" not in df.columns or "平台" not in df.columns:
        print("错误：Excel 缺少“名字”或“平台”列")
        return
    # 自动补充缺失列
    for col in ["封面", "类型", "发行公司"]:
        if col not in df.columns:
            df[col] = ""

    # 加载凭证
    sgdb_api_key = read_file_content(SGDB_API_KEY_FILE, "SteamGridDB API Key")
    if sgdb_api_key:
        print("✅ SteamGridDB API Key 已加载")
    else:
        print("⚠️ SteamGridDB API Key 未配置，将跳过")

    igdb_id = read_file_content(IGDB_CLIENT_ID_FILE, "IGDB Client ID")
    igdb_secret = read_file_content(IGDB_CLIENT_SECRET_FILE, "IGDB Client Secret")
    if igdb_id and igdb_secret:
        print("✅ IGDB 凭证已加载")
    else:
        print("⚠️ IGDB 凭证不完整，将跳过")

    print("\n开始查询（封面来自 SteamGridDB，类型/发行公司由 IGDB / Steam 补全）")
    success = 0
    for idx, row in df.iterrows():
        name = str(row["名字"]).strip() if pd.notna(row["名字"]) else ""
        platform = str(row["平台"]).strip() if pd.notna(row["平台"]) else ""

        if not name:
            print(f"[{idx+1}/{len(df)}] 游戏名为空，跳过")
            continue

        clean_name = clean_game_name(name)
        print(f"\n[{idx+1}/{len(df)}] 处理：{name} | 平台：{platform or '未填写'}")
        if clean_name != name:
            print(f"    搜索名称清理为：{clean_name}")

        cover_url = ""
        genre = ""
        publisher = ""

        # 1. 封面优先用 SteamGridDB
        if sgdb_api_key:
            print("    [SteamGridDB] 尝试获取封面...")
            cover_url = search_sgdb_cover(clean_name, sgdb_api_key)

        # 2. 从 IGDB 补全类型、发行公司（如果有凭证，无论前面是否有封面都查）
        if igdb_id and igdb_secret:
            igdb_cover, igdb_genre, igdb_pub = search_igdb_all(clean_name, platform, igdb_id, igdb_secret)
            if not cover_url:
                cover_url = igdb_cover   # SGDB 没封面时，采纳 IGDB 的封面
            if not genre:
                genre = igdb_genre
            if not publisher:
                publisher = igdb_pub

        # 3. 若信息仍有缺失，再用 Steam 商店补全
        if not cover_url or not genre or not publisher:
            steam_cover, steam_genre, steam_pub = search_steam_all(clean_name)
            if not cover_url:
                cover_url = steam_cover
            if not genre:
                genre = steam_genre
            if not publisher:
                publisher = steam_pub

        # 写入结果
        if cover_url:
            df.at[idx, "封面"] = cover_url
            success += 1
        if genre:
            df.at[idx, "类型"] = genre
        if publisher:
            df.at[idx, "发行公司"] = publisher

        # 立即保存
        if cover_url or genre or publisher:
            print(f"    最终结果 → 封面: {'有' if cover_url else '无'}, 类型: {genre or '无'}, 发行公司: {publisher or '无'}")
        else:
            print("    未获取到任何信息")

        safe_save_excel(df, excel_path)
        time.sleep(REQUEST_DELAY)

    print(f"\n{'='*50}")
    print(f"完成！共 {len(df)} 行，获取到封面 {success} 行")
    print(f"文件保存至：{excel_path}")
    print("="*50)

def main():
    while True:
        print("\n" + "="*60)
        print("游戏封面多源查询工具（SteamGridDB → IGDB → Steam）")
        print("="*60)
        run_once()
        cont = input("\n是否继续处理另一个文件？(y/n，默认 n): ").strip().lower()
        if cont != 'y':
            print("程序结束。")
            break

if __name__ == "__main__":
    main()