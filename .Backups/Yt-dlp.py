# 请帮我写个中文的 Python 脚本，批注也是中文：
# 用 yt-dlp（"d:\\ProApps\\Youtube-dl\\yt-dlp.exe"）下载视频。
# 首先询问我想下载单个链接还是列表文件中的链接？（如果输入的是网络链接，则下载该链接；按回车则为默认地址“e:\\Documents\\Creations\\Scripts\\Python\\Yt-dlpLists.txt”；如果输入的是本地链接，则下载该地址列表文件中的链接。）
# 再询问我是否需要引入 cookies 文件？（按回车或输入“y”则为引入 cookies 文件，默认地址为"d:\\ProApps\\Youtube-dl\\Yt-dlpCookies.txt"；如果输入的是本地链接，则将该地址作为 cookies 文件地址；输入“n”则不引入 cookies 文件。）
# 再询问我是否需要代理？（按回车或输入“y”则为代理，默认地址“127.0.0.1:10808”；输入“n”则不引入 cookies 文件。）
# 再询问我下载后文件存放的位置？（按回车则为默认地址“d:\\Downloads\\”；如果输入的是本地链接，则将该地址作为下载后文件存放的位置。）

# 导入模块。
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import os
import re
import pandas as pd
from datetime import datetime

# 常量定义
YT_DLP_PATH = r"d:\ProApps\Youtube-dl\yt-dlp.exe"
DEFAULT_LIST_FILE = r"e:\Documents\Creations\Scripts\Python\YoutubeYt-dlpLists.txt"
DEFAULT_COOKIES_FILE = r"d:\ProApps\Youtube-dl\YoutubeYt-dlpCookies.txt"
DEFAULT_PROXY = "127.0.0.1:10808"
DEFAULT_SAVE_PATH = r"d:\Downloads"
DEFAULT_EXCEL_FILE = r"e:\Documents\Creations\Scripts\Python\视频记录.xlsx"
RHASH_PATH = r"d:\ProApps\RHash\rhash.exe"

def get_user_input(prompt, default_value, is_boolean=False):
    """
    获取用户输入，支持默认值和布尔选择
    """
    if is_boolean:
        user_input = input(f"{prompt} (Y/n, 默认'{default_value}'): ").strip().lower()
        if user_input in ("", "y", "yes"):
            return True
        elif user_input in ("n", "no"):
            return False
        else:
            return True if default_value.lower() in ("y", "yes") else False
    else:
        user_input = input(f"{prompt} (默认: {default_value}): ").strip()
        return user_input if user_input else default_value

def extract_links_from_input(user_input):
    """
    从用户输入中提取链接
    """
    links = []
    
    if os.path.isfile(user_input):
        # 从文件读取链接
        try:
            with open(user_input, 'r', encoding='utf-8') as f:
                for line in f:
                    link = line.strip()
                    if link and not link.startswith('#'):
                        links.append(link)
        except Exception as e:
            print(f"读取文件时出错: {e}")
            return []
    else:
        # 从直接输入的文本提取链接
        url_pattern = re.compile(r'https?://[^\s<>"]+|www\.[^\s<>"]+')
        links = url_pattern.findall(user_input)
        links = [link.strip('.,;:!?') for link in links]
    
    return list(dict.fromkeys(links))  # 去重保持顺序

def download_video(url, download_dir, cookies=None, proxy=None, use_proxy=False):
    """
    使用yt-dlp下载视频，包含封面和字幕
    """
    try:
        # 构建基础命令
        command = [YT_DLP_PATH]
        
        # 添加Cookies（如果提供且文件存在）
        if cookies and os.path.exists(cookies):
            command.extend(["--cookies", cookies])
        
        # 添加代理（仅在use_proxy为True且proxy不为None时）
        if use_proxy and proxy:
            command.extend(["--proxy", f"socks5h://{proxy}"])
        
        # 核心功能：封面+字幕+最佳质量
        command += [
            "--write-thumbnail",    # 下载封面图
            "--write-subs",         # 下载字幕
            "--sub-langs", "all",   # 所有可用语言
            "--convert-subs", "srt", # 转换为通用字幕格式
            "--embed-subs",         # 将字幕嵌入视频
            "--embed-thumbnail",    # 将封面嵌入视频
            "--format", "bestvideo+bestaudio/best",
            "--merge-output-format", "mp4",
            "--output", os.path.join(download_dir, "%(title)s.%(ext)s"),
            url
        ]
        
        # 显示当前下载配置
        print(f"开始下载: {url}")
        if use_proxy and proxy:
            print(f"使用代理: {proxy}")
        if cookies and os.path.exists(cookies):
            print(f"使用Cookies文件")
        
        # 执行下载 - 使用系统默认编码，避免强制UTF-8
        result = subprocess.run(
            command, 
            capture_output=True, 
            text=True,
            encoding=sys.getdefaultencoding(),  # 使用系统默认编码
            errors='replace'  # 替换无法解码的字符
        )
        
        # 处理结果
        if result.returncode == 0:
            print(f"✓ 下载成功: {url}")
            
            # 尝试从输出中提取文件名
            downloaded_file = None
            if result.stdout:
                for line in result.stdout.split('\n'):
                    if 'Destination:' in line:
                        match = re.search(r'Destination:\s*(.+)', line)
                        if match:
                            downloaded_file = match.group(1).strip()
                            break
                    elif '[Merger] Merging formats into' in line:
                        match = re.search(r'into\s*"([^"]+)"', line)
                        if match:
                            downloaded_file = match.group(1).strip()
                            break
            
            return True, downloaded_file
        else:
            print(f"✗ 下载失败: {url}")
            if result.stderr:
                # 只显示错误信息的前300个字符
                error_msg = result.stderr[:300]
                print(f"错误信息: {error_msg}")
            return False, None
            
    except Exception as e:
        print(f"下载过程中出错: {e}")
        return False, None

def generate_ed2k_hash(filepath):
    """
    使用rhash生成文件的ed2k哈希
    """
    if not os.path.exists(RHASH_PATH):
        print(f"警告: RHash未找到于 {RHASH_PATH}")
        return None
    
    try:
        cmd = [RHASH_PATH, '--uppercase', '--ed2k-link', filepath]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print(f"生成ed2k哈希失败")
            return None
    except Exception as e:
        print(f"执行rhash时出错: {e}")
        return None

def get_file_info(filepath):
    """
    获取文件大小和哈希值
    """
    try:
        # 获取文件大小
        size_bytes = os.path.getsize(filepath)
        
        # 格式化文件大小
        if size_bytes < 1024:
            size_formatted = f"{size_bytes:.4f} B"
        elif size_bytes < 1024 * 1024:
            size_formatted = f"{size_bytes / 1024:.4f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            size_formatted = f"{size_bytes / (1024 * 1024):.4f} MB"
        else:
            size_formatted = f"{size_bytes / (1024 * 1024 * 1024):.4f} GB"
        
        # 使用rhash获取SHA1哈希
        if os.path.exists(RHASH_PATH):
            cmd = [RHASH_PATH, '--sha1', '--uppercase', filepath]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                hash_match = re.search(r'([A-F0-9]{40})', result.stdout)
                file_hash = hash_match.group(1) if hash_match else "未知"
            else:
                file_hash = "未知"
        else:
            file_hash = "未知"
        
        return size_formatted, file_hash
    except Exception as e:
        print(f"获取文件信息时出错: {e}")
        return "未知", "未知"

def update_excel(excel_path, video_info):
    """
    更新Excel文件，添加新的视频记录
    """
    try:
        # 检查Excel文件是否存在
        if os.path.exists(excel_path):
            df = pd.read_excel(excel_path)
        else:
            # 创建新的DataFrame
            df = pd.DataFrame(columns=['序号', '视频标题', '文件名', '下载链接', 'ED2K链接', '文件路径', '文件大小', 'SHA1哈希', '下载时间', '使用代理'])
        
        # 计算新的序号
        new_index = 1
        if not df.empty and '序号' in df.columns:
            last_index = df['序号'].max()
            if pd.notna(last_index):
                new_index = int(last_index) + 1
        
        # 创建新行
        new_row = {
            '序号': new_index,
            '视频标题': video_info.get('title', ''),
            '文件名': video_info.get('filename', ''),
            '下载链接': video_info.get('url', ''),
            'ED2K链接': video_info.get('ed2k_link', ''),
            '文件路径': video_info.get('filepath', ''),
            '文件大小': video_info.get('size', ''),
            'SHA1哈希': video_info.get('hash', ''),
            '下载时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            '使用代理': video_info.get('used_proxy', False)
        }
        
        # 添加新行
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        
        # 保存回Excel文件
        df.to_excel(excel_path, index=False)
        print(f"✓ 记录已保存到Excel: {excel_path}")
        
    except Exception as e:
        print(f"✗ 更新Excel文件时出错: {e}")

def find_latest_video_file(download_dir, url):
    """
    在下载目录中查找最新创建的视频文件
    """
    try:
        video_extensions = ['.mp4', '.mkv', '.webm', '.flv', '.avi', '.mov']
        video_files = []
        
        for file in os.listdir(download_dir):
            if any(file.lower().endswith(ext) for ext in video_extensions):
                filepath = os.path.join(download_dir, file)
                create_time = os.path.getctime(filepath)
                video_files.append((filepath, file, create_time))
        
        if video_files:
            # 按创建时间排序，返回最新的
            video_files.sort(key=lambda x: x[2], reverse=True)
            return video_files[0][0], video_files[0][1]
        
        return None, None
    except Exception as e:
        print(f"查找视频文件时出错: {e}")
        return None, None

def main():
    """
    主函数 - 交互式下载管理器
    """
    print("=" * 60)
    print("YT-DLP 增强版下载工具")
    print("=" * 60)
    
    while True:
        try:
            # 第一步：获取下载链接
            print("\n" + "=" * 40)
            print("步骤 1/5: 选择下载内容")
            print("-" * 40)
            
            input_link = input(f"请输入视频链接或列表文件路径\n(直接回车使用默认列表: {DEFAULT_LIST_FILE})\n> ").strip()
            
            if not input_link:
                links_source = DEFAULT_LIST_FILE
            else:
                links_source = input_link
            
            # 提取链接
            links = extract_links_from_input(links_source)
            
            if not links:
                print("未找到有效的链接，请重新输入")
                continue
            
            print(f"✓ 找到 {len(links)} 个链接:")
            for i, link in enumerate(links, 1):
                print(f"  {i}. {link}")
            
            # 第二步：配置Cookies
            print("\n" + "=" * 40)
            print("步骤 2/5: Cookies配置")
            print("-" * 40)
            
            use_cookies = get_user_input(
                "是否使用Cookies文件?", 
                "Y", 
                is_boolean=True
            )
            
            cookies_file = None
            if use_cookies:
                custom_cookies = input(f"输入Cookies文件路径 (默认: {DEFAULT_COOKIES_FILE}): ").strip()
                cookies_file = custom_cookies if custom_cookies else DEFAULT_COOKIES_FILE
                
                if not os.path.exists(cookies_file):
                    print(f"警告: Cookies文件不存在，将不使用Cookies")
                    cookies_file = None
            
            # 第三步：配置代理
            print("\n" + "=" * 40)
            print("步骤 3/5: 代理配置")
            print("-" * 40)
            
            proxy = None
            use_proxy_input = get_user_input(
                "是否使用代理?", 
                "Y", 
                is_boolean=True
            )
            
            if use_proxy_input:
                custom_proxy = input(f"输入代理地址 (默认: {DEFAULT_PROXY}): ").strip()
                proxy = custom_proxy if custom_proxy else DEFAULT_PROXY
                print(f"将使用代理: {proxy}")
            
            # 第四步：配置保存路径
            print("\n" + "=" * 40)
            print("步骤 4/5: 保存路径配置")
            print("-" * 40)
            
            save_path = get_user_input(
                "请输入保存路径", 
                DEFAULT_SAVE_PATH
            )
            
            # 确保目录存在
            os.makedirs(save_path, exist_ok=True)
            print(f"✓ 文件将保存到: {save_path}")
            
            # 第五步：Excel记录配置
            print("\n" + "=" * 40)
            print("步骤 5/5: 记录配置")
            print("-" * 40)
            
            excel_path = get_user_input(
                "Excel记录文件路径", 
                DEFAULT_EXCEL_FILE
            )
            
            # 下载每个链接
            print(f"\n{'='*60}")
            print(f"开始下载 {len(links)} 个视频")
            print(f"{'='*60}")
            
            successful_downloads = 0
            
            for idx, url in enumerate(links, 1):
                print(f"\n[进度: {idx}/{len(links)}] 处理链接: {url}")
                
                success = False
                downloaded_file = None
                used_proxy = False
                
                # 第一次尝试：不使用代理
                if proxy:
                    print("  第一次尝试: 不使用代理")
                    success, downloaded_file = download_video(
                        url, save_path, cookies_file, proxy, use_proxy=False
                    )
                
                # 如果失败且配置了代理，第二次尝试：使用代理
                if not success and proxy:
                    print("  第二次尝试: 使用代理")
                    success, downloaded_file = download_video(
                        url, save_path, cookies_file, proxy, use_proxy=True
                    )
                    used_proxy = success  # 只有成功时才标记使用了代理
                
                # 如果仍然失败且没有配置代理，直接尝试下载
                if not success and not proxy:
                    print("  尝试下载 (无代理)")
                    success, downloaded_file = download_video(
                        url, save_path, cookies_file, None, use_proxy=False
                    )
                
                if success:
                    # 如果没获取到文件名，尝试查找最新文件
                    if not downloaded_file or not os.path.exists(downloaded_file):
                        downloaded_file, filename = find_latest_video_file(save_path, url)
                        if not downloaded_file:
                            print("  警告: 无法找到下载的文件")
                            continue
                    else:
                        filename = os.path.basename(downloaded_file)
                    
                    # 获取文件信息
                    size_formatted, file_hash = get_file_info(downloaded_file)
                    
                    # 生成ed2k链接
                    ed2k_link = generate_ed2k_hash(downloaded_file)
                    
                    # 准备视频信息
                    video_info = {
                        'title': os.path.splitext(filename)[0],
                        'filename': filename,
                        'url': url,
                        'filepath': downloaded_file,
                        'size': size_formatted,
                        'hash': file_hash,
                        'ed2k_link': ed2k_link if ed2k_link else '',
                        'used_proxy': used_proxy
                    }
                    
                    # 更新Excel文件
                    update_excel(excel_path, video_info)
                    
                    successful_downloads += 1
                    print(f"  ✓ 完成: {filename}")
                else:
                    print(f"  ✗ 无法下载此链接")
            
            # 下载完成总结
            print(f"\n{'='*60}")
            print(f"下载完成!")
            print(f"成功: {successful_downloads}/{len(links)}")
            print(f"{'='*60}")
            
            # 询问是否继续
            print("\n是否继续下载其他链接?")
            continue_choice = input("输入 'y' 继续，输入 'q' 退出: ").strip().lower()
            
            if continue_choice == 'q':
                print("程序结束")
                break
                
        except KeyboardInterrupt:
            print("\n\n程序被用户中断")
            break
        except Exception as e:
            print(f"\n发生错误: {e}")
            print("请检查输入和配置后重试")

if __name__ == "__main__":
    import sys
    
    # 检查yt-dlp是否存在
    if not os.path.exists(YT_DLP_PATH):
        print(f"错误: yt-dlp 未找到于 {YT_DLP_PATH}")
        print("请检查路径或安装 yt-dlp")
        sys.exit(1)
    
    # 运行主程序
    main()