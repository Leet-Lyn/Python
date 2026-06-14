# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问原文件位置与目标文件夹（默认为 "Z:\"）位置。
# 尝试将原文件向目标文件夹移动。
# 如果无法移动，则重命名原文件（从后删除1个字符（不包括扩展名）），再次尝试将原文件向目标文件夹移动。
# 反复循环，直至能将原文件向目标文件夹移动。
# 将生成的文件名，写入剪贴板。
# 最后询问我是否继续，默认（"y"，或回车），返回开头，询问原文件位置与目标文件夹（默认为 "Z:\"）位置。按"n"，择退出。

# 导入模块
import shutil
import subprocess
from pathlib import Path

def copy_to_clipboard(text: str) -> None:
    """将文本复制到 Windows 剪贴板（使用系统自带 clip.exe）。"""
    try:
        # Windows 自带 clip.exe，无需额外依赖
        subprocess.run(
            ["clip.exe"],
            input=text,
            encoding="utf-16-le",
            errors="ignore",
            check=True,
        )
    except Exception as e:
        print(f"复制到剪贴板失败：{e}")


def try_move_file(source: Path, target_dir: Path, stem: str, suffix: str) -> Path | None:
    """
    尝试将文件移动到目标目录。
    若因文件名冲突失败，则逐次缩短文件名（每次从末尾去掉一个字符，
    不含扩展名）并重试，直到移动成功或文件名长度耗尽。
    """
    while True:
        new_name = f"{stem}{suffix}"
        target = target_dir / new_name

        try:
            # 跨盘移动使用 shutil.move；同盘时它会用 os.rename（高效）
            shutil.move(str(source), str(target))
            return target  # 成功，返回目标 Path
        except shutil.Error as e:
            # shutil.move 在同名文件已存在时通常不会抛异常，
            # 但跨盘复制+删除场景可能产生 Error，同样走缩短逻辑
            print(f"文件移动失败：{e}")
        except OSError as e:
            print(f"文件移动失败：{e}")

        # --- 移动失败：缩短文件名后重试 ---
        if len(stem) <= 1:
            print("文件名已无法缩短，无法移动文件。")
            return None

        # 从文件名末尾删除一个字符（不含扩展名）
        stem = stem[:-1]
        new_source = source.with_stem(stem)

        try:
            # 重命名原文件
            source.rename(new_source)
            source = new_source  # 更新源文件路径供下次循环使用
            print(f"文件已重命名为：{source}")
        except OSError as rename_error:
            print(f"文件重命名失败：{rename_error}")
            return None


def main() -> None:
    """主循环：获取输入 → 移动文件 → 复制路径到剪贴板 → 询问是否继续。"""
    while True:
        # --- 获取原文件路径 ---
        raw = input("请输入原文件的完整路径：").strip()
        source = Path(raw)

        if not source.is_file():
            print("输入的原文件路径无效，请重新输入。")
            continue

        # --- 获取目标文件夹 ---
        raw_target = input("请输入目标文件夹位置（默认为 Z:\）：").strip()
        target_dir = Path(raw_target) if raw_target else Path(r"Z:／")

        # 确保目标文件夹存在
        if not target_dir.exists():
            try:
                target_dir.mkdir(parents=True)
                print(f"目标文件夹已创建：{target_dir}")
            except OSError as e:
                print(f"创建目标文件夹失败：{e}")
                continue

        # --- 执行移动 ---
        stem = source.stem      # 不含扩展名的文件名
        suffix = source.suffix  # 扩展名（含点号）
        result = try_move_file(source, target_dir, stem, suffix)

        if result is not None:
            target_str = str(result)
            copy_to_clipboard(target_str)
            print(f"文件已成功移动至：{target_str}")
            print(f"文件路径已复制到剪贴板：{target_str}")
        else:
            print("操作失败。")
            break

        # --- 询问是否继续 ---
        cont = input("是否继续操作？（Y / 回车继续，N 退出）：").strip().lower()
        if cont == "n":
            print("程序结束。")
            break


# 程序入口
if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
    input("按回车键退出...")