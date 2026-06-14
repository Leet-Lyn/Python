# 将脚本改写下：请帮我写个中文的 Python 脚本，批注也是中文：
# 询问我 Sitemap 链接，分析内容，将网页的地址导出（<loc>网页地址</loc>）。
# 写入剪贴板，每行一个链接。同时写入:“e:\Documents\Softwares\Codes\Python\Sitemap.txt”。

# 导入模块
import subprocess
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

# --- 常量 ---
OUTPUT_FILE = Path(r"e:\Documents\Softwares\Codes\Python\Sitemap.txt")
PROXY = "http://127.0.0.1:10808"
PROXY_HANDLER = urllib.request.ProxyHandler({"http": PROXY, "https": PROXY})


def copy_to_clipboard(text: str) -> None:
    """将文本复制到 Windows 剪贴板（使用系统自带 clip.exe）。"""
    try:
        subprocess.run(
            ["clip.exe"],
            input=text,
            encoding="utf-16-le",
            errors="ignore",
            check=True,
        )
    except Exception as e:
        print(f"复制到剪贴板失败：{e}")


def fetch_sitemap(url: str) -> str | None:
    """通过代理获取 Sitemap XML 内容，失败返回 None。"""
    try:
        print(f"正在通过代理 {PROXY} 获取 {url} ...")
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36"
            )
        }
        opener = urllib.request.build_opener(PROXY_HANDLER)
        req = urllib.request.Request(url, headers=headers)
        with opener.open(req, timeout=10) as response:
            content = response.read()
        charset = response.headers.get_content_charset()
        return content.decode(charset or "utf-8")
    except urllib.error.URLError as e:
        print(f"网络错误：{e}（可能代理不可用或目标网站无法访问）")
    except Exception as e:
        print(f"获取 Sitemap 时发生未知错误：{e}")
    return None


def extract_locations(xml_text: str) -> list[str]:
    """解析 XML，提取所有 <loc> 标签内的网址。"""
    urls: list[str] = []
    try:
        root = ET.fromstring(xml_text)
        for elem in root.iter():
            # 去除命名空间前缀，匹配 <loc> 标签
            local_tag = elem.tag.split("}")[-1] if "}" in elem.tag else elem.tag
            if local_tag == "loc" and elem.text:
                urls.append(elem.text.strip())
    except ET.ParseError as e:
        print(f"XML 解析错误：{e}")
    except Exception as e:
        print(f"提取网址时发生错误：{e}")
    return urls


def main() -> None:
    """主流程：输入 Sitemap URL → 提取网址 → 复制到剪贴板 + 保存到文件。"""
    print("=== Sitemap 链接提取器（支持代理）===")
    url = input("请输入 Sitemap 的完整网址：").strip()
    if not url:
        print("网址不能为空，程序退出。")
        return

    # 1. 获取 Sitemap
    xml_text = fetch_sitemap(url)
    if xml_text is None:
        print("无法获取 Sitemap 内容，程序终止。")
        return

    # 2. 提取 <loc> 网址
    urls = extract_locations(xml_text)
    if not urls:
        print("未找到任何 <loc> 标签，请检查 Sitemap 格式。")
        return
    print(f"共提取到 {len(urls)} 个网址。")

    # 3. 复制到剪贴板
    copy_to_clipboard("\n".join(urls))
    print(f"成功将 {len(urls)} 个网址复制到剪贴板。")

    # 4. 保存到文件
    try:
        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_FILE.write_text("\n".join(urls), encoding="utf-8")
        print(f"成功将 {len(urls)} 个网址保存到文件：{OUTPUT_FILE}")
    except OSError as e:
        print(f"保存文件失败：{e}")

    print("操作完成！")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
