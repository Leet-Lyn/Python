# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件位置。
# 在脚本开始前询问我源 torrent 文件所在文件夹（默认：“d:\Works\Attachment\”）。
# 依次读取该文件夹下所有 torrent 文件，生成同名的两个 txt 文件（分别后缀名为“.txt”与“.percent-encoding.txt”）
# 读取每个 torrent 文件，提取每一个 ed2k hash 生成 ed2k link。要求 Hash 大写，分别写入这两个 txt 文件。
# 写入后缀名为“.txt”的 txt 文件，里的链接要求不转为 Percent-encoding。写入后缀名为“.percent-encoding.txt”的 txt 文件，里的链接要求转为 Percent-encoding。二者链接数量相同。
# 同时将不转为 Percent-encoding 的 ed2k link 写入剪贴板中。

# 导入模块
import os
import binascii
import bencodepy
import pyperclip
from urllib.parse import quote

def bytes_to_hex_upper(data: bytes) -> str:
    """将二进制 MD4 hash 转为大写 HEX 字符串"""
    return binascii.hexlify(data).decode().upper()

def build_ed2k_link(filename: str, size: int, md4_hex: str) -> str:
    """生成不做 Percent-encoding 的 ed2k 链接"""
    return f"ed2k://|file|{filename}|{size}|{md4_hex}|/"

def build_ed2k_link_percent(filename: str, size: int, md4_hex: str) -> str:
    """生成做 Percent-encoding 的 ed2k 链接"""
    encoded_name = quote(filename, safe="")
    return f"ed2k://|file|{encoded_name}|{size}|{md4_hex}|/"

def sanitize_filename(path_parts):
    """将文件路径拼接，并将所有路径分隔符替换为下划线"""
    return "_".join([p.replace("/", "_").replace("\\", "_") for p in path_parts])

def extract_ed2k_from_torrent(torrent_path: str):
    """
    从单个 torrent 文件中提取 ed2k 链接
    文件名中所有路径分隔符替换为 '_'
    """
    with open(torrent_path, "rb") as f:
        torrent = bencodepy.decode(f.read())

    info = torrent.get(b"info", {})
    links_raw = []
    links_encoded = []

    # 多文件 torrent
    if b"files" in info:
        for f in info[b"files"]:
            if b"ed2k" not in f:
                continue

            size = f[b"length"]
            md4_hex = bytes_to_hex_upper(f[b"ed2k"])

            # 文件名处理
            filename = sanitize_filename([p.decode(errors="ignore") for p in f[b"path"]])

            links_raw.append(build_ed2k_link(filename, size, md4_hex))
            links_encoded.append(build_ed2k_link_percent(filename, size, md4_hex))

    # 单文件 torrent（BitComet 私有字段）
    else:
        for key in (b"ed2k", b"emulehash", b"filehash"):
            if key in info:
                size = info.get(b"length", 0)
                md4_hex = bytes_to_hex_upper(info[key])

                name = info.get(b"name", b"").decode(errors="ignore")
                filename = sanitize_filename([name])

                links_raw.append(build_ed2k_link(filename, size, md4_hex))
                links_encoded.append(build_ed2k_link_percent(filename, size, md4_hex))
                break

    return links_raw, links_encoded

def main():
    # 只询问一次路径
    base_path = input(
        "请输入 torrent 文件所在文件夹，默认 d:\\Works\\Attachment\\）："
    ).strip()

    if not base_path:
        base_path = r"d:\Works\Attachment"

    base_path = base_path.rstrip("\\/")

    all_clipboard_links = []

    for name in os.listdir(base_path):
        if not name.lower().endswith(".torrent"):
            continue

        torrent_path = os.path.join(base_path, name)
        base_name = os.path.splitext(name)[0]

        raw_links, encoded_links = extract_ed2k_from_torrent(torrent_path)

        if not raw_links:
            continue

        txt_path = os.path.join(base_path, base_name + ".txt")
        pct_path = os.path.join(base_path, base_name + ".percent-encoding.txt")

        with open(txt_path, "w", encoding="utf-8") as f:
            f.write("\n".join(raw_links))

        with open(pct_path, "w", encoding="utf-8") as f:
            f.write("\n".join(encoded_links))

        all_clipboard_links.extend(raw_links)

    # 写入剪贴板
    if all_clipboard_links:
        pyperclip.copy("\n".join(all_clipboard_links))
        print(f"已完成：共生成并复制 {len(all_clipboard_links)} 条 ed2k 链接到剪贴板。")
    else:
        print("未在任何 torrent 中找到 ed2k hash。")

if __name__ == "__main__":
    main()