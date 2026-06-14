# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我文件夹位置（默认"d:\Studios\Folders\Downloads\"）与想要删除的字段（默认"（Via："）。
# 将文件夹及其子文件夹内所有文件以文件内容读出重命名为文件名（不包括扩展名，最长 20 个字符）。
# 再文件夹及其子文件夹内所有文件重命名，从某一字段开始至末尾删除（不包括扩展名）。

import sys
from pathlib import Path

# ==================== 全局配置 ====================

DEFAULT_SOURCE_DIR = Path(r"d:\Studios\Folders\Downloads")
DEFAULT_FIELD = "（Via："
MAX_CONTENT_LENGTH = 20

# ==================== 辅助函数 ====================


def get_input_with_default(prompt_text: str, default_value: str) -> str:
    """获取带默认值的用户输入。"""
    user_input = input(f"{prompt_text} (默认: {default_value}): ").strip()
    return user_input if user_input else str(default_value)


def read_file_content(file_path: Path, max_length: int = MAX_CONTENT_LENGTH) -> str | None:
    """
    读取文件内容作为新文件名（不含扩展名）。
    返回新文件名，失败时返回 None。
    """
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore").strip()
        content = " ".join(content.split())
        if len(content) > max_length:
            content = content[:max_length]
        return content if content else None
    except OSError as e:
        print(f"无法读取文件内容 {file_path.name}：{e}")
        return None


# ==================== 处理函数 ====================


def rename_by_content(source_dir: Path) -> tuple[int, int]:
    """根据文件内容重命名所有文件。返回 (重命名数, 跳过数)。"""
    renamed = 0
    skipped = 0

    for file_path in source_dir.rglob("*"):
        if not file_path.is_file():
            continue

        new_name = read_file_content(file_path)
        if not new_name:
            print(f"跳过文件（无法读取内容）：{file_path.name}")
            skipped += 1
            continue

        new_path = file_path.parent / (new_name + file_path.suffix)
        if new_path.exists():
            print(f"警告：目标文件 '{new_path.name}' 已存在，跳过 '{file_path.name}'")
            skipped += 1
            continue

        try:
            file_path.rename(new_path)
            print(f"已将 '{file_path.name}' 重命名为 '{new_path.name}'")
            renamed += 1
        except OSError as e:
            print(f"错误：无法重命名文件 '{file_path.name}'，{e}")
            skipped += 1

    return renamed, skipped


def remove_field_from_filenames(source_dir: Path, field: str) -> tuple[int, int]:
    """删除文件名中指定字段及其后内容。返回 (重命名数, 跳过数)。"""
    renamed = 0
    skipped = 0

    for file_path in source_dir.rglob("*"):
        if not file_path.is_file():
            continue

        if field not in file_path.name:
            print(f"跳过文件：'{file_path.name}'（不包含字段 '{field}'）")
            skipped += 1
            continue

        try:
            index = file_path.name.index(field)
            prefix = file_path.name[:index]
            new_name = prefix + file_path.suffix
            new_path = file_path.parent / new_name

            if new_path.exists():
                print(f"警告：目标文件 '{new_name}' 已存在，跳过 '{file_path.name}'")
                skipped += 1
                continue

            file_path.rename(new_path)
            print(f"已将 '{file_path.name}' 重命名为 '{new_name}'")
            renamed += 1
        except OSError as e:
            print(f"错误：无法重命名文件 '{file_path.name}'，{e}")
            skipped += 1

    return renamed, skipped


# ==================== 主程序 ====================


def main() -> None:
    """主函数：获取用户输入并调用重命名函数。"""
    print("欢迎使用文件批量重命名工具！")

    source_str = get_input_with_default("请输入文件夹路径：", str(DEFAULT_SOURCE_DIR))
    field = get_input_with_default("请输入想要删除的字段：", DEFAULT_FIELD)

    source_dir = Path(source_str)
    if not source_dir.is_dir():
        print(f"错误：文件夹 '{source_dir}' 不存在或不是有效的文件夹。")
        return

    print(f"\n即将处理文件夹：{source_dir}")
    print("将执行以下操作：")
    print("1. 根据文件内容重命名文件（文件名最长20个字符）")
    print(f"2. 删除文件名中 '{field}' 及其后面的内容")
    confirm = input("确认执行操作？(y/n): ").strip().lower()
    if confirm != "y":
        print("操作已取消。")
        return

    print("\n=== 第一步：根据文件内容重命名 ===")
    content_renamed, _ = rename_by_content(source_dir)

    print("\n=== 第二步：删除指定字段后的内容 ===")
    field_renamed, _ = remove_field_from_filenames(source_dir, field)

    print(f"\n操作完成！")
    print(f"内容重命名：{content_renamed} 个文件")
    print(f"字段删除：{field_renamed} 个文件")


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
