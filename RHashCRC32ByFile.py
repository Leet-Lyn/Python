# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件位置。
# 计算并生成文件的 CRC32，用方括号"[]"包绕并写入剪贴板。
# 我安装了 RHash，位置：“d:\ProApps\rhash\current\rhash.exe”。
# 如此循环，再次询问我源文件位置。

# 导入模块
import subprocess
import sys
from pathlib import Path

# --- 常量 ---
RHASH = Path(r"d:\ProApps\rhash\current\rhash.exe")


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


def get_crc32(file_path: Path) -> str | None:
    """使用 RHash 计算文件的 CRC32 值，返回 [CRC32] 格式，失败返回 None。"""
    if not file_path.is_file():
        print(f"错误：文件 '{file_path}' 不存在")
        return None

    command = [str(RHASH), "--crc32", str(file_path)]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            check=True,
        )
        # RHash 输出格式："文件路径  CRC32值"
        output = result.stdout.strip()
        parts = output.split()
        if len(parts) >= 2:
            crc32_value = parts[-1].upper()
            return f"[{crc32_value}]"
        else:
            print(f"无法解析 RHash 输出：{output}")
            return None
    except FileNotFoundError:
        print(f"错误：未找到 RHash —— {RHASH}")
        return None
    except subprocess.CalledProcessError as e:
        print(f"RHash 执行错误：{e}")
        return None


def main() -> None:
    """主循环：输入文件路径 → 计算 CRC32 → 复制到剪贴板。"""
    while True:
        try:
            raw = input("请输入源文件路径（输入 Q 退出程序）：").strip()

            if raw.lower() in ("quit", "exit", "q"):
                print("程序已退出")
                break

            file_path = Path(raw.strip("\"'"))

            if raw == "" or str(file_path) == ".":
                print("错误：文件路径不能为空")
                continue

            print(f"\n正在计算文件的 CRC32 值：{file_path}")
            crc32_value = get_crc32(file_path)

            if crc32_value:
                print("生成的 CRC32 值：")
                print(crc32_value)
                copy_to_clipboard(crc32_value)
                print("✓ CRC32 值已复制到剪贴板")
            else:
                print("计算 CRC32 值失败，请检查文件路径是否正确")

        except KeyboardInterrupt:
            print("\n程序被用户中断")
            break


# 程序入口
if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if not RHASH.is_file():
        print(f"警告：未找到 RHash 程序，请确认路径：{RHASH}")
    main()
