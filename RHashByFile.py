# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件位置。
# 计算并生成文件的 Ed2K 链接。
# 我安装了 RHash，位置：“d:\ProApps\rhash\current\rhash.exe”。生成 ed2k 的命令类似：rhash.exe --uppercase --ed2k-link "file_path"。
# 生成如 "ed2k://|file|rustdesk-1.4.3-x86_64.exe|23369352|DF952...|/" 的 ed2k 链接，显示在屏幕，并写入剪贴板。
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


def get_ed2k_link(file_path: Path) -> str | None:
    """使用 RHash 生成文件的 ed2k 链接，失败返回 None。"""
    if not file_path.is_file():
        print(f"错误：文件 '{file_path}' 不存在")
        return None

    command = [str(RHASH), "--uppercase", "--ed2k-link", str(file_path)]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            check=True,
        )
        return result.stdout.strip()
    except FileNotFoundError:
        print(f"错误：未找到 RHash —— {RHASH}")
        return None
    except subprocess.CalledProcessError as e:
        print(f"RHash 执行错误：{e}")
        return None


def main() -> None:
    """主循环：输入文件路径 → 生成 ed2k 链接 → 复制到剪贴板。"""
    while True:
        try:
            raw = input("请输入源文件路径（输入 Q 退出程序）：").strip()

            if raw.lower() in ("quit", "exit", "q"):
                print("程序已退出")
                break

            # 移除路径两端的引号
            file_path = Path(raw.strip("\"'"))

            if raw == "" or str(file_path) == ".":
                print("错误：文件路径不能为空")
                continue

            print(f"\n正在为文件生成 ed2k 链接：{file_path}")
            ed2k_link = get_ed2k_link(file_path)

            if ed2k_link:
                print("生成的 ED2K 链接：")
                print(ed2k_link)
                copy_to_clipboard(ed2k_link)
                print("✓ ED2K 链接已复制到剪贴板")
            else:
                print("生成 ed2k 链接失败，请检查文件路径是否正确")

        except KeyboardInterrupt:
            print("\n程序被用户中断")
            break


# 程序入口
if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if not RHASH.is_file():
        print(f"警告：未找到 RHash 程序，请确认路径：{RHASH}")
    main()
