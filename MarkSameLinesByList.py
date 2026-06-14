# 请帮我写个中文的 Python 脚本，批注也是中文：
# 询问我文件位置（可以是任何格式，默认是：d:\Studios\Attachments\Lists.txt）。以文本方式读取该文件。
# 遍历该 txt 文件所有行。每发现有某个行与前面的行相同就在行首打上"# "。

import sys
from pathlib import Path

# ==================== 全局配置 ====================

DEFAULT_FILE_PATH = Path(r"d:\Studios\Attachments\Lists.txt")

# ==================== 辅助函数 ====================


def read_text_with_fallback(file_path: Path) -> str | None:
    """
    尝试多种编码读取文本文件，全部失败返回 None。
    """
    for encoding in ("utf-8", "gbk", "gb2312", "latin-1"):
        try:
            text = file_path.read_text(encoding=encoding)
            print(f"成功使用 {encoding} 编码读取文件")
            return text
        except (UnicodeDecodeError, OSError):
            continue
    return None


# ==================== 处理函数 ====================


def mark_duplicate_lines(file_path: Path) -> int:
    """
    读取文件，对重复出现的行添加 "# " 前缀后写回。
    返回标记的重复行数。
    """
    if not file_path.is_file():
        print(f"错误：文件不存在 —— {file_path}")
        return 0

    text = read_text_with_fallback(file_path)
    if text is None:
        print("无法使用常见编码读取文件，请检查文件编码")
        return 0

    seen: set[str] = set()
    result: list[str] = []
    marked = 0

    for line in text.splitlines(keepends=True):
        stripped = line.rstrip("\n\r")
        if stripped in seen:
            result.append(f"# {line}")
            marked += 1
        else:
            seen.add(stripped)
            result.append(line)

    file_path.write_text("".join(result), encoding="utf-8")
    return marked


# ==================== 主程序 ====================


def main() -> None:
    """主函数：获取文件路径并执行重复行标记。"""
    print("=== 文件重复行标记工具 ===")

    raw = input(
        f"请输入文件位置（默认: {DEFAULT_FILE_PATH}）："
    ).strip().strip("\"'")

    file_path = Path(raw) if raw else DEFAULT_FILE_PATH

    count = mark_duplicate_lines(file_path)
    if count:
        print(f"文件处理完成，标记了 {count} 行重复内容。")
    else:
        print("未发现重复行，或文件不存在。")


# ==================== 程序入口 ====================

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n用户中断程序，已退出。")
    except Exception as e:
        print(f"\n程序运行出错: {e}")
    finally:
        input("\n按回车键退出...")
