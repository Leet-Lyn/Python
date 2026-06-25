# 将脚本改写下：请帮我写个中文的 Python 脚本，批注也是中文：
# 询问我 Sitemap 链接，分析内容，将网页的地址导出（<loc>网页地址</loc>）。
# 写入剪贴板，每行一个链接。同时写入:“e:\Documents\Softwares\Codes\Python\Sitemap.txt”。

# 导入模块
import signal
import subprocess
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

# ==================== 全局配置 ====================

OUTPUT_FILE = Path(r"e:\Documents\Softwares\Codes\Python\Sitemap.txt")
DEFAULT_PROXY = "http://127.0.0.1:10808"

_quit_requested = False  # Ctrl+Q 中断标志

# --- 消息常量 ---
MSG_INTERRUPTED = "\n\n用户中断程序，已退出。"
MSG_ERROR = "\n程序运行出错: {}"
MSG_EXIT = "\n按回车键退出..."
MSG_CLIPBOARD_FAIL = "复制到剪贴板失败：{}"
MSG_FETCHING = "正在通过代理 {} 获取 {} ..."
MSG_DIRECT_FETCHING = "正在直接获取 {} ..."
MSG_NETWORK_ERROR = "网络错误：{}（可能代理不可用或目标网站无法访问）"
MSG_FETCH_UNKNOWN_ERROR = "获取 Sitemap 时发生未知错误：{}"
MSG_XML_PARSE_ERROR = "XML 解析错误：{}"
MSG_EXTRACT_ERROR = "提取网址时发生错误：{}"
MSG_TITLE = "=== Sitemap 链接提取器（支持代理）==="
MSG_ASK_URL = "请输入 Sitemap 的完整网址："
MSG_PROXY_PROMPT = "是否使用代理？(y=使用默认代理, 输入地址=自定义代理, n=不使用)"
MSG_NO_PROXY = "不使用代理，直接连接。"
MSG_URL_EMPTY = "网址不能为空，程序退出。"
MSG_FETCH_FAILED = "无法获取 Sitemap 内容，程序终止。"
MSG_NO_LOC = "未找到任何 <loc> 标签，请检查 Sitemap 格式。"
MSG_EXTRACTED_COUNT = "共提取到 {} 个网址。"
MSG_COPIED_COUNT = "成功将 {} 个网址复制到剪贴板。"
MSG_SAVED_COUNT = "成功将 {} 个网址保存到文件：{}"
MSG_SAVE_FAILED = "保存文件失败：{}"
MSG_DONE = "操作完成！"


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
        print(MSG_CLIPBOARD_FAIL.format(e))


def fetch_sitemap(url: str, proxy: str | None = None) -> str | None:
    """获取 Sitemap XML 内容（可选代理），失败返回 None。"""
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36"
            )
        }
        if proxy:
            print(MSG_FETCHING.format(proxy, url))
            proxy_handler = urllib.request.ProxyHandler({"http": proxy, "https": proxy})
            opener = urllib.request.build_opener(proxy_handler)
        else:
            print(MSG_DIRECT_FETCHING.format(url))
            opener = urllib.request.build_opener()
        req = urllib.request.Request(url, headers=headers)
        with opener.open(req, timeout=10) as response:
            content = response.read()
        charset = response.headers.get_content_charset()
        return content.decode(charset or "utf-8")
    except urllib.error.URLError as e:
        print(MSG_NETWORK_ERROR.format(e))
    except Exception as e:
        print(MSG_FETCH_UNKNOWN_ERROR.format(e))
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
        print(MSG_XML_PARSE_ERROR.format(e))
    except Exception as e:
        print(MSG_EXTRACT_ERROR.format(e))
    return urls
# ==================== 中断处理 ====================


def _on_quit_signal(signum, frame):
    global _quit_requested
    _quit_requested = True
    raise KeyboardInterrupt()


def _init_quit_handler():
    if hasattr(signal, "SIGQUIT"):
        signal.signal(signal.SIGQUIT, _on_quit_signal)


def _check_quit() -> bool:
    global _quit_requested
    if sys.platform == "win32":
        try:
            import msvcrt
            while msvcrt.kbhit():
                if msvcrt.getch() == b"\x11":
                    _quit_requested = True
        except Exception:
            pass
    return _quit_requested


def main() -> None:
    """主流程：输入 Sitemap URL → 提取网址 → 复制到剪贴板 + 保存到文件。"""
    print(MSG_TITLE)

    # 询问代理设置
    proxy_input = input(f"{MSG_PROXY_PROMPT} (默认: {DEFAULT_PROXY}): ").strip()
    if proxy_input.lower() == 'n':
        proxy = None
        print(MSG_NO_PROXY)
    elif proxy_input == '' or proxy_input.lower() == 'y':
        proxy = DEFAULT_PROXY
    else:
        proxy = proxy_input  # 自定义代理地址

    url = input(MSG_ASK_URL).strip()
    if not url:
        print(MSG_URL_EMPTY)
        return

    # 1. 获取 Sitemap
    xml_text = fetch_sitemap(url, proxy)
    if xml_text is None:
        print(MSG_FETCH_FAILED)
        return

    # 2. 提取 <loc> 网址
    urls = extract_locations(xml_text)
    if not urls:
        print(MSG_NO_LOC)
        return
    print(MSG_EXTRACTED_COUNT.format(len(urls)))

    # 3. 复制到剪贴板
    copy_to_clipboard("\n".join(urls))
    print(MSG_COPIED_COUNT.format(len(urls)))

    # 4. 保存到文件
    try:
        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_FILE.write_text("\n".join(urls), encoding="utf-8")
        print(MSG_SAVED_COUNT.format(len(urls), OUTPUT_FILE))
    except OSError as e:
        print(MSG_SAVE_FAILED.format(e))

    print(MSG_DONE)


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
