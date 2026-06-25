# 请帮我写个中文的 Python 脚本，批注也是中文，但是变量参数不要是中文：
# 在脚本开始前询问我 excel 文件位置（默认为：d:\Studios\Attachments\标准.xlsx）。
# 读取 excel 文件，第一行为表头（字段名）。此后每一行为一条记录。
# 依据 excel 文件中的“名字”、“平台”字段，查询该游戏在该平台下封面、类型、发行公司填入“封面”、“类型”及“发行公司”字段里。“名字内可能含有其版本”。“封面”为链接地址。
# 反复循环。

# 导入模块
import signal
import os
import re
import sys
import time
from pathlib import Path

import pandas as pd
import requests

# ==================== 全局配置 ====================

# --- 代理设置 ---
PROXY = {
     "http": "http://127.0.0.1:10808",
     "https": "http://127.0.0.1:10808"
}

# --- 默认路径 ---
DEFAULT_EXCEL_PATH = Path(r"d:\Studios\Attachments\标准.xlsx")

# --- API 配置 ---
SGDB_API_KEY_FILE = Path(r"e:\Documents\Softwares\Codes\Attachments\APIKEY\SteamGridDBAPIKey.txt")
IGDB_CLIENT_ID_FILE = Path(r"e:\Documents\Softwares\Codes\Attachments\APIKEY\IGDBClientID.txt")
IGDB_CLIENT_SECRET_FILE = Path(r"e:\Documents\Softwares\Codes\Attachments\APIKEY\IGDBClientSecret.txt")
REQUEST_DELAY = 0.8

_quit_requested = False  # Ctrl+Q 中断标志

# --- 消息常量 ---
MSG_PROMPT_EXCEL = "请输入 Excel 文件路径"
MSG_ERR_FILE_NOT_FOUND = "错误：文件不存在 - {}"
MSG_READING_EXCEL = "\n正在读取 Excel：{}"
MSG_ROW_COUNT = "成功读取 {} 行"
MSG_READ_FAILED = "读取失败：{}"
MSG_MISSING_COLUMNS = '错误：Excel 缺少"名字"或"平台"列'
MSG_SGDB_LOADED = "✅ SteamGridDB API Key 已加载"
MSG_SGDB_SKIPPED = "⚠️ SteamGridDB API Key 未配置，将跳过"
MSG_IGDB_LOADED = "✅ IGDB 凭证已加载"
MSG_IGDB_SKIPPED = "⚠️ IGDB 凭证不完整，将跳过"
MSG_QUERY_START = "\n开始查询（封面来自 SteamGridDB，类型/发行公司由 IGDB / Steam 补全）"
MSG_SKIP_EMPTY_NAME = "[{}/{}] 游戏名为空，跳过"
MSG_PROCESSING_ROW = "\n[{}/{}] 处理：{} | 平台：{}"
MSG_CLEANED_NAME = "    搜索名称清理为：{}"
MSG_FINAL_RESULT = "    最终结果 → 封面: {}, 类型: {}, 发行公司: {}"
MSG_NO_INFO = "    未获取到任何信息"
MSG_DONE_SUMMARY = "完成！共 {} 行，获取到封面 {} 行"
MSG_DONE_PATH = "文件保存至：{}"
MSG_TOOL_TITLE = "游戏封面多源查询工具（SteamGridDB → IGDB → Steam）"
MSG_CONTINUE = "\n是否继续处理另一个文件？(y/n，默认 n): "
MSG_PROGRAM_END = "程序结束。"
MSG_INTERRUPTED = "\n\n用户中断程序，已退出。"
MSG_ERROR = "\n程序运行出错: {}"
MSG_EXIT = "\n按回车键退出..."
MSG_PLATFORM_EMPTY = "未填写"
MSG_COVER_HAS = "有"
MSG_COVER_NONE = "无"

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

# ==================== 辅助函数 ====================

def get_input_with_default(prompt_text: str, default_value: str) -> str:
    """获取带默认值的用户输入。"""
    user_input = input(f"{prompt_text} (默认: {default_value}): ").strip()
    return user_input if user_input else str(default_value)
def clean_game_name(name):
    """清理游戏名称：删除所有中英文括号及内部内容"""
    if not name:
        return ""
    cleaned = re.sub(r'（[^）]*）', '', name)
    cleaned = re.sub(r'\([^)]*\)', '', cleaned)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned if cleaned else name.strip()

def read_file_content(file_path: Path, prompt_name: str) -> str | None:
    """读取文本文件内容，若文件不存在则提示用户输入并可选择保存"""
    if file_path.is_file():
        content = file_path.read_text(encoding="utf-8").strip()
        if content:
            return content
    print(f"未找到 {prompt_name} 文件：{file_path}")
    user_input = input(f"请输入 {prompt_name}（直接回车跳过）: ").strip()
    if not user_input:
        return None
    save_choice = input(f"是否保存 {prompt_name} 到文件？(y/n): ").strip().lower()
    if save_choice == 'y':
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(user_input, encoding="utf-8")
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
                new_path = str(Path(path).parent / new_path)
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
    raw = get_input_with_default(MSG_PROMPT_EXCEL, str(DEFAULT_EXCEL_PATH))
    excel_path = Path(raw) if raw else DEFAULT_EXCEL_PATH
    if not excel_path.is_file():
        print(MSG_ERR_FILE_NOT_FOUND.format(excel_path))
        return

    print(MSG_READING_EXCEL.format(excel_path))
    try:
        df = pd.read_excel(excel_path, dtype=str)
        print(MSG_ROW_COUNT.format(len(df)))
    except Exception as e:
        print(MSG_READ_FAILED.format(e))
        return

    # 检查必要列
    if "名字" not in df.columns or "平台" not in df.columns:
        print(MSG_MISSING_COLUMNS)
        return
    # 自动补充缺失列
    for col in ["封面", "类型", "发行公司"]:
        if col not in df.columns:
            df[col] = ""

    # 加载凭证
    sgdb_api_key = read_file_content(SGDB_API_KEY_FILE, "SteamGridDB API Key")
    if sgdb_api_key:
        print(MSG_SGDB_LOADED)
    else:
        print(MSG_SGDB_SKIPPED)

    igdb_id = read_file_content(IGDB_CLIENT_ID_FILE, "IGDB Client ID")
    igdb_secret = read_file_content(IGDB_CLIENT_SECRET_FILE, "IGDB Client Secret")
    if igdb_id and igdb_secret:
        print(MSG_IGDB_LOADED)
    else:
        print(MSG_IGDB_SKIPPED)

    print(MSG_QUERY_START)
    success = 0
    for idx, row in df.iterrows():
        name = str(row["名字"]).strip() if pd.notna(row["名字"]) else ""
        platform = str(row["平台"]).strip() if pd.notna(row["平台"]) else ""

        if not name:
            print(MSG_SKIP_EMPTY_NAME.format(idx+1, len(df)))
            continue

        clean_name = clean_game_name(name)
        print(MSG_PROCESSING_ROW.format(idx+1, len(df), name, platform or MSG_PLATFORM_EMPTY))
        if clean_name != name:
            print(MSG_CLEANED_NAME.format(clean_name))

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
            print(MSG_FINAL_RESULT.format(
                MSG_COVER_HAS if cover_url else MSG_COVER_NONE,
                genre or MSG_COVER_NONE,
                publisher or MSG_COVER_NONE))
        else:
            print(MSG_NO_INFO)

        safe_save_excel(df, excel_path)
        time.sleep(REQUEST_DELAY)

    print(f"\n{'='*50}")
    print(MSG_DONE_SUMMARY.format(len(df), success))
    print(MSG_DONE_PATH.format(excel_path))
    print("="*50)

def main():
    while True:
        print("\n" + "="*60)
        print(MSG_TOOL_TITLE)
        print("="*60)
        run_once()
        cont = input(MSG_CONTINUE).strip().lower()
        if cont != 'y':
            print(MSG_PROGRAM_END)
            break


# ==================== 程序入口 ====================

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    try:
        main()
    except KeyboardInterrupt:
        print(MSG_INTERRUPTED)
    except Exception as e:
        print(MSG_ERROR.format(e))
    finally:
        input(MSG_EXIT)