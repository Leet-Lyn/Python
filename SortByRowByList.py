# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件位置（可以是任何格式，默认是：d:\Studios\Attachments\Lists.txt）。
# 将文件按行读取，按字母顺序排序重新排序，再次写入文件。

import sys
from pathlib import Path

# ==================== 全局配置 ====================

DEFAULT_FILE_PATH = Path(r"d:\Studios\Attachments\Lists.txt")

# ==================== 辅助函数 ====================


def get_input_with_default(prompt_text: str, default_value: str) -> str:
    """获取带默认值的用户输入。"""
    user_input = input(f"{prompt_text} (默认: {default_value}): ").strip()
    return user_input if user_input else str(default_value)


# ==================== 处理函数 ====================


def sort_file_lines(file_path: Path) -> bool:
    """
    读取文件 → 按字母排序行 → 覆盖写回。
    返回 True 表示成功。
    """
    # 读取
    try:
        text = file_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"错误：'{file_path}' 不是有效的文件路径！")
        return False
    except UnicodeDecodeError:
        print("错误：文件编码不支持，请使用 UTF-8 编码的文本文件")
        return False

    lines = text.splitlines()
    if not lines:
        print("文件内容为空，无需处理！")
        return True  # 空文件不算失败

    # 排序
    sorted_lines = sorted(lines)

    # 写回
    try:
        file_path.write_text("\n".join(sorted_lines), encoding="utf-8")
    except PermissionError:
        print(f"错误：没有写入权限，请关闭文件后重试 - {file_path}")
        return False
    except OSError as e:
        print(f"写入文件时发生错误：{e}")
        return False

    print("文件内容已成功排序并保存！")
    return True


# ==================== 主程序 ====================


def main() -> None:
    """主函数：获取用户输入并执行文件排序操作。"""

    file_str = get_input_with_default(
        "请输入要处理的文件路径：", str(DEFAULT_FILE_PATH))
    file_path = Path(file_str)

    sort_file_lines(file_path)


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
