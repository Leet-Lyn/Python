# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件夹位置（默认 d:\Studios\Folders\Downloads\）与目标文件位置（默认 e:\Documents\Softwares\Codes\Python\Ed2kList.txt）。
# 遍历源文件夹内所有子文件夹中的文件，计算并生成该文件的 Ed2K 链接。
# 我安装了 RHash，位置：“d:\ProApps\rhash\current\rhash.exe”。生成 ed2k 的命令类似：rhash.exe --uppercase --ed2k-link "file_path"。
# 生成如 "ed2k://|file|rustdesk-1.4.3-x86_64.exe|23369352|DF952...|/" 的 ed2k 链接。
# 先清空目标文件，然后将生成的 ed2k 链接依次写入，一行一个。

# 导入模块
import subprocess
import sys
from pathlib import Path

# --- 常量 ---
RHASH = Path(r"d:\ProApps\rhash\current\rhash.exe")


def get_ed2k_link(file_path: Path) -> str | None:
    """使用 RHash 生成文件的 ed2k 链接，失败返回 None。"""
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
        print(f"  错误：未找到 RHash —— {RHASH}")
        return None
    except subprocess.CalledProcessError as e:
        print(f"  RHash 执行错误：{e}")
        return None


def process_directory(source_dir: Path, target_file: Path) -> None:
    """遍历源文件夹，为所有文件生成 ed2k 链接并写入目标文件。"""
    # 收集所有文件
    all_files = sorted(
        p for p in source_dir.rglob("*")
        if p.is_file()
    )

    if not all_files:
        print("源文件夹中没有文件。")
        return

    total = len(all_files)
    print(f"找到 {total} 个文件，开始生成 ed2k 链接...\n")

    # 清空目标文件
    target_file.parent.mkdir(parents=True, exist_ok=True)
    target_file.write_text("", encoding="utf-8")

    # 处理每个文件
    ok = 0
    fail = 0

    with target_file.open("a", encoding="utf-8") as fh:
        for idx, src in enumerate(all_files, 1):
            # 相对于源文件夹的路径，用于显示
            try:
                rel = src.relative_to(source_dir)
            except ValueError:
                rel = src

            print(f"[{idx}/{total}] {rel}")

            link = get_ed2k_link(src)
            if link:
                fh.write(link + "\n")
                ok += 1
                print(f"  ✓ 成功")
            else:
                fail += 1
                print(f"  ✗ 失败")

    print(f"\n处理完成：成功 {ok} 个，失败 {fail} 个，共 {total} 个。")
    print(f"ed2k 链接已保存到：{target_file}")


def main() -> None:
    """主流程：获取源文件夹与目标文件 → 批量生成 ed2k 链接。"""
    try:
        # --- 源文件夹 ---
        default_src = r"d:\Studios\Folders\Downloads"
        raw = input(f"请输入源文件夹位置（回车使用默认 {default_src}）：").strip()
        source_dir = Path(raw.strip("\"'")) if raw else Path(default_src)

        if not source_dir.is_dir():
            print(f"错误：源文件夹 '{source_dir}' 不存在")
            return

        # --- 目标文件 ---
        default_dst = r"e:\Documents\Softwares\Codes\Python\Ed2kList.txt"
        raw = input(f"请输入目标文件位置（回车使用默认 {default_dst}）：").strip()
        target_file = Path(raw.strip("\"'")) if raw else Path(default_dst)

        # --- 确认 ---
        print(f"\n确认信息：")
        print(f"  源文件夹：{source_dir}")
        print(f"  目标文件：{target_file}")

        confirm = input("\n是否开始处理？（回车继续，N 取消）：").strip().lower()
        if confirm in ("n", "no"):
            print("已取消操作")
            return

        process_directory(source_dir, target_file)

    except KeyboardInterrupt:
        print("\n程序被用户中断")


# 程序入口
if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if not RHASH.is_file():
        print(f"错误：未找到 RHash 程序 —— {RHASH}")
        sys.exit(1)
    main()
    input("按回车键退出...")
