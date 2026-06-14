# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件位置，默认为“e:\Documents\Softwares\Codes\Python\Ed2kList.txt”（按回车表示默认，按"c"读取剪贴板，并写入默认路径）。
# 该文件（或剪贴板）内包含许多 ed2k 链接，每行一个，顺序读取每个 ed2k 链接。
# 每个链接都是百分号编码(Percent-encoding)，请将其转回原来链接。在源文件位置下生成新的文件（读取剪贴板则在默认文件夹下），文件名为"Ed2kList.new.txt"。
# 根据"Ed2kList.new.txt"文件，在源文件位置下生成新的文件，文件名分别为"Ed2kList.name.txt"、"Ed2kList.suffix.txt"、"Ed2kList.size.txt"、"Ed2kList.hash.txt"。分别存放链接的文件名、后缀名、大小、hash。"Ed2kList.size.txt"文件中存放的文件大小请转成 B、KB、MB、GB 形式，并精确到小数点后 4 位，hash 转全部大写。
# 将大小、hash 写入剪贴板，之间用回车间隔。

# 导入模块
import subprocess
import sys
import urllib.parse
from pathlib import Path


# --- 默认路径 ---
DEFAULT_SOURCE = Path(r"e:\Documents\Softwares\Codes\Python\Ed2kList.txt")


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


def format_size(size_str: str) -> str:
    """
    将文件大小从字节数转换为 B、KB、MB、GB 形式，精确到小数点后 4 位。
    字节数应为整数字符串。
    """
    size = int(size_str)
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024:
            return f"{size:.4f} {unit}"
        size /= 1024
    return f"{size:.4f} TB"


def main() -> None:
    """主流程：获取源文件 → 解码 ed2k 链接 → 生成分类文件 → 复制到剪贴板。"""
    prompt = (
        r"请输入源文件位置"
        r"（默认 e:\Documents\Softwares\Codes\Python\Ed2kList.txt，"
        r"按回车使用默认，按 C 读取剪贴板）："
    )
    user_input = input(prompt).strip()

    if user_input.lower() == "c":
        # 从剪贴板读取内容并写入默认路径
        source_file = DEFAULT_SOURCE
        source_folder = DEFAULT_SOURCE.parent

        source_folder.mkdir(parents=True, exist_ok=True)

        try:
            result = subprocess.run(
                ["powershell", "-NonInteractive", "-Command", "Get-Clipboard -Raw"],
                capture_output=True,
                encoding="utf-8",
                check=True,
            )
            clipboard_content = result.stdout
        except Exception as e:
            print(f"读取剪贴板失败：{e}")
            return

        if not clipboard_content.strip():
            print("剪贴板为空，请先复制 ed2k 链接到剪贴板！")
            return

        source_file.write_text(clipboard_content, encoding="utf-8")
        print(f"已从剪贴板读取内容并保存到：{source_file}")
    elif not user_input:
        # 使用默认路径
        source_file = DEFAULT_SOURCE
        source_folder = DEFAULT_SOURCE.parent
    else:
        # 用户输入了自定义路径
        source_file = Path(user_input).absolute()
        source_folder = source_file.parent

    # 检查源文件是否存在
    if not source_file.is_file():
        print("源文件不存在，请检查路径或文件名！")
        return

    # --- 读取并解码所有 ed2k 链接 ---
    raw_lines = source_file.read_text(encoding="utf-8").splitlines()
    decoded_links = [urllib.parse.unquote(line.strip()) for line in raw_lines if line.strip()]

    if not decoded_links:
        print("源文件中没有有效内容。")
        return

    # --- 写入解码后的链接文件 ---
    base_name = source_file.stem
    new_file = source_folder / f"{base_name}.new.txt"
    new_file.write_text("\n".join(decoded_links), encoding="utf-8")

    # --- 按类型拆分并写入各文件 ---
    name_file = source_folder / f"{base_name}.name.txt"
    suffix_file = source_folder / f"{base_name}.suffix.txt"
    size_file = source_folder / f"{base_name}.size.txt"
    hash_file = source_folder / f"{base_name}.hash.txt"

    names: list[str] = []
    suffixes: list[str] = []
    sizes: list[str] = []
    hashes: list[str] = []
    skipped = 0

    for link in decoded_links:
        if not link.startswith("ed2k://|file|"):
            skipped += 1
            continue
        parts = link.split("|")
        if len(parts) < 5:
            skipped += 1
            continue

        filename = parts[2]
        filesize = parts[3]
        filehash = parts[4].upper()

        names.append(filename)
        suffixes.append(Path(filename).suffix)
        sizes.append(format_size(filesize))
        hashes.append(filehash)

    name_file.write_text("\n".join(names), encoding="utf-8")
    suffix_file.write_text("\n".join(suffixes), encoding="utf-8")
    size_file.write_text("\n".join(sizes), encoding="utf-8")
    hash_file.write_text("\n".join(hashes), encoding="utf-8")

    # --- 复制大小和哈希到剪贴板 ---
    clipboard_content = "\n".join(sizes) + "\n\n" + "\n".join(hashes)
    copy_to_clipboard(clipboard_content)
    print("大小和 hash 已写入剪贴板")

    if skipped:
        print(f"⚠ 跳过了 {skipped} 条无效/不完整的链接。")

    print(f"处理完成，生成的新文件保存在：{source_folder}")


# 程序入口
if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()

# 按下回车键退出程序
input("按回车键退出...")
