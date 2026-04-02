# 将脚本改写下：请帮我写个中文的 Python 脚本，批注也是中文：
# 询问我 Sitemap 链接，分析内容，将网页的地址导出（<loc>网页地址</loc>）。
# 写入剪贴板，每行一个链接。同时写入“e:\Documents\Creations\Scripts\Attachments\Python\Sitemap.txt”。

# 导入模块
import os
import sys
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET

# 尝试导入 pyperclip 用于操作剪贴板，若失败则提示安装
try:
    import pyperclip
except ImportError:
    print("错误：需要 pyperclip 库来复制到剪贴板。")
    print("请使用以下命令安装：pip install pyperclip")
    sys.exit(1)

# 目标文件路径（注意使用原始字符串避免转义问题）
OUTPUT_FILE = r"e:\Documents\Creations\Scripts\Attachments\Python\Sitemap.txt"

# 代理设置（根据您的要求硬编码）
PROXY = "http://127.0.0.1:10808"
# 为 HTTP 和 HTTPS 设置相同的代理（HTTP 代理通常可以处理 HTTPS 通过 CONNECT 方法）
PROXY_HANDLER = urllib.request.ProxyHandler({
    'http': PROXY,
    'https': PROXY
})

def fetch_sitemap_content(url):
    """
    从指定的 URL 通过代理获取 Sitemap 内容（XML 格式）
    :param url: Sitemap 的网址
    :return: 成功时返回 XML 文本（字符串），失败时返回 None
    """
    try:
        print(f"正在通过代理 {PROXY} 从 {url} 获取 Sitemap...")
        # 设置请求头，模拟浏览器访问
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        # 创建带有代理的 opener
        opener = urllib.request.build_opener(PROXY_HANDLER)
        # 构建请求对象
        req = urllib.request.Request(url, headers=headers)
        # 使用 opener 打开请求
        with opener.open(req, timeout=10) as response:
            content = response.read()
            # 尝试检测编码，若无法检测则默认 UTF-8
            charset = response.headers.get_content_charset()
            if charset:
                xml_text = content.decode(charset)
            else:
                xml_text = content.decode('utf-8')
            return xml_text
    except urllib.error.URLError as e:
        print(f"网络错误：{e}（可能代理不可用或目标网站无法访问）")
    except Exception as e:
        print(f"获取 Sitemap 时发生未知错误：{e}")
    return None


def extract_locations(xml_text):
    """
    解析 XML 内容，提取所有 <loc> 标签内的文本
    :param xml_text: XML 字符串
    :return: 网址列表
    """
    urls = []
    try:
        # 解析 XML
        root = ET.fromstring(xml_text)
        # 查找所有 <loc> 标签，注意处理命名空间
        for elem in root.iter():
            # 如果元素的标签（忽略命名空间）是 'loc'，则取其文本
            tag = elem.tag
            # 去除命名空间部分（如果存在）
            if '}' in tag:
                local_tag = tag.split('}', 1)[1]
            else:
                local_tag = tag
            if local_tag == 'loc':
                if elem.text:
                    urls.append(elem.text.strip())
    except ET.ParseError as e:
        print(f"XML 解析错误：{e}")
    except Exception as e:
        print(f"提取网址时发生错误：{e}")
    return urls


def save_to_clipboard(urls):
    """
    将网址列表（每行一个）复制到系统剪贴板
    :param urls: 网址列表
    """
    if not urls:
        print("没有网址可复制到剪贴板。")
        return
    text = "\n".join(urls)
    try:
        pyperclip.copy(text)
        print(f"成功将 {len(urls)} 个网址复制到剪贴板。")
    except Exception as e:
        print(f"复制到剪贴板失败：{e}")


def save_to_file(urls, file_path):
    """
    将网址列表（每行一个）保存到指定文件
    :param urls: 网址列表
    :param file_path: 文件路径
    """
    if not urls:
        print("没有网址可保存。")
        return
    # 确保目标目录存在
    dir_name = os.path.dirname(file_path)
    if dir_name and not os.path.exists(dir_name):
        try:
            os.makedirs(dir_name)
            print(f"已创建目录：{dir_name}")
        except OSError as e:
            print(f"无法创建目录 {dir_name}：{e}")
            return
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(urls))
        print(f"成功将 {len(urls)} 个网址保存到文件：{file_path}")
    except Exception as e:
        print(f"保存文件失败：{e}")


def main():
    """
    主函数：询问用户 Sitemap 链接，执行提取、复制和保存操作
    """
    print("=== Sitemap 链接提取器（支持代理）===")
    url = input("请输入 Sitemap 的完整网址：").strip()
    if not url:
        print("网址不能为空，程序退出。")
        return

    # 1. 获取 Sitemap 内容（通过代理）
    xml_text = fetch_sitemap_content(url)
    if xml_text is None:
        print("无法获取 Sitemap 内容，程序终止。")
        return

    # 2. 提取所有 <loc> 网址
    urls = extract_locations(xml_text)
    if not urls:
        print("未找到任何 <loc> 标签，请检查 Sitemap 格式。")
        return
    print(f"共提取到 {len(urls)} 个网址。")

    # 3. 复制到剪贴板
    save_to_clipboard(urls)

    # 4. 保存到文件
    save_to_file(urls, OUTPUT_FILE)

    print("操作完成！")


if __name__ == "__main__":
    main()