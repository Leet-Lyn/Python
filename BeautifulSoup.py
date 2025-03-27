# # 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我网站链接。
# 询问我目标文件夹位置（默认为“D:\\Downloads\\”）。
# 抓取该网站内所有文章的链接，生成 Links.txt，到目标文件夹。

# 导入模块
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def get_valid_url():
    """询问用户输入有效的网站链接，并确保格式正确"""
    while True:
        url = input("请输入要抓取的网站链接（例如 https://example.com）: ").strip()
        if not url:
            print("链接不能为空，请重新输入！")
            continue
        
        # 如果没有协议头（http/https），自动添加
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # 验证URL格式是否正确
        parsed = urlparse(url)
        if not parsed.netloc:  # 如果没有域名，则无效
            print("链接格式不正确，请重新输入！")
        else:
            return url

def get_save_folder():
    """询问用户保存文件夹位置，默认是 D:\\Downloads\\"""
    default_folder = "D:\\Downloads\\"
    folder = input(f"请输入保存文件夹位置（默认: {default_folder}）: ").strip()
    
    if not folder:
        folder = default_folder
    
    # 确保文件夹存在，如果不存在则创建
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"文件夹 {folder} 不存在，已自动创建。")
    
    return folder

def extract_links_from_page(url):
    """从单个页面提取所有文章链接"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # 检查请求是否成功
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 提取所有 <a> 标签的 href
        links = set()
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            
            # 跳过空链接、JavaScript 链接和锚点
            if not href or href.startswith(('javascript:', '#')):
                continue
            
            # 处理相对路径，转换为完整 URL
            full_url = urljoin(url, href)
            
            # 确保链接属于同一域名
            if urlparse(full_url).netloc == urlparse(url).netloc:
                links.add(full_url)
        
        return links
    except Exception as e:
        print(f"抓取 {url} 时出错: {e}")
        return set()

def crawl_website(base_url, max_pages=10000):
    """爬取网站的所有页面链接（限制最多 max_pages 页）"""
    visited = set()
    to_visit = {base_url}
    all_links = set()
    
    while to_visit and len(visited) < max_pages:
        current_url = to_visit.pop()
        if current_url in visited:
            continue
        
        print(f"正在抓取: {current_url}")
        visited.add(current_url)
        
        # 提取当前页面的所有链接
        new_links = extract_links_from_page(current_url)
        all_links.update(new_links)
        
        # 将新链接加入待访问队列
        for link in new_links:
            if link not in visited:
                to_visit.add(link)
    
    return all_links

def save_links_to_file(links, folder):
    """将链接保存到目标文件夹的 Links.txt"""
    file_path = os.path.join(folder, "Links.txt")
    with open(file_path, 'w', encoding='utf-8') as f:
        for link in sorted(links):
            f.write(link + '\n')
    print(f"所有链接已保存至: {file_path}")

def main():
    print("=== 网站文章链接抓取工具 ===")
    
    # 1. 获取用户输入的网站链接
    base_url = get_valid_url()
    
    # 2. 获取保存文件夹位置
    save_folder = get_save_folder()
    
    # 3. 开始抓取链接
    print("\n开始抓取文章链接，请稍候...")
    all_links = crawl_website(base_url)
    
    # 4. 保存到文件
    if all_links:
        save_links_to_file(all_links, save_folder)
    else:
        print("未找到任何有效链接！")

if __name__ == "__main__":
    main()

# 按回车键退出
input("按回车键退出程序...")