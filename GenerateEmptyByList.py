# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件位置（d:\Studios\Attachments\Lists.txt）与目标文件夹位置（d:\Studios\Folders\Downloads\）。
# 读取源文件每行，在目标文件夹位置生成空文件，文件名与读取的一致。

import sys
from pathlib import Path

# ==================== 全局配置 ====================

DEFAULT_SOURCE_FILE = Path(r"d:\Studios\Attachments\Lists.txt")
DEFAULT_TARGET_DIR = Path(r"d:\Studios\Folders\Downloads")

# ==================== 辅助函数 ====================


def get_input_with_default(prompt_text: str, default_value: str) -> str:
    """获取带默认值的用户输入。"""
    user_input = input(f"{prompt_text} (默认: {default_value}): ").strip()
    return user_input if user_input else str(default_value)


def read_lines_with_fallback(file_path: Path) -> list[str] | None:
    """
    尝试多种编码读取文件行，返回行列表；全部失败返回 None。
    """
    for encoding in ("utf-8", "gbk", "gb2312", "latin-1"):
        try:
            text = file_path.read_text(encoding=encoding)
            print(f"成功使用 {encoding} 编码读取源文件")
            return text.splitlines()
        except (UnicodeDecodeError, OSError):
            continue
    return None


# ==================== 处理函数 ====================


def create_empty_files_from_list(
    source_file: Path,
    target_dir: Path,
) -> int:
    """
    读取源文件每行作为文件名，在目标文件夹创建对应空文件。
    返回创建的文件数量。
    """
    # 检查源文件
    if not source_file.is_file():
        print(f"源文件不存在：{source_file}")
        return 0

    # 读取行
    lines = read_lines_with_fallback(source_file)
    if lines is None:
        print("无法使用常见编码读取源文件，请检查文件编码")
        return 0

    # 确保目标文件夹存在
    target_dir.mkdir(parents=True, exist_ok=True)

    created = 0
    for line in lines:
        file_name = line.strip()
        if not file_name:
            continue

        target_path = target_dir / file_name
        try:
            target_path.write_text("", encoding="utf-8")
            print(f"已生成空文件：{file_name}")
            created += 1
        except OSError as e:
            print(f"创建文件失败：{file_name}，错误：{e}")

    return created


# ==================== 主程序 ====================


def main() -> None:
    """主函数：获取用户输入并调用文件生成函数。"""
    print("=== 批量创建空文件工具 ===")

    source_str = get_input_with_default("请输入源文件位置：", str(DEFAULT_SOURCE_FILE))
    target_str = get_input_with_default("请输入目标文件夹位置：", str(DEFAULT_TARGET_DIR))

    source_file = Path(source_str)
    target_dir = Path(target_str)

    print(f"使用的源文件：{source_file}")
    print(f"使用的目标文件夹：{target_dir}")

    count = create_empty_files_from_list(source_file, target_dir)
    print(f"文件生成完成，共创建了 {count} 个空文件。")


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
