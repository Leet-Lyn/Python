# 请帮我写个中文的 Python 脚本，批注也是中文，但是变量参数不要是中文：
# 询问我需要的操作：
# 1. 移动：询问我列表路径（默认"d:\Studios\Attachments\Lists.txt"）。源文件夹路径（默认"d:\Studios\Folders\Ins\"）与目标文件夹路径（默认"d:\Studios\Folders\Outs\"）。列表里一行一个文件名（有扩展名）。请枚举每一行的文件名，找到源文件夹里匹配的文件，移动到目标文件夹。
# 2. 复制：询问我列表路径（默认"d:\Studios\Attachments\Lists.txt"）。源文件夹路径（默认"d:\Studios\Folders\Ins\"）与目标文件夹路径（默认"d:\Studios\Folders\Outs\"）。列表里一行一个文件名（有扩展名）。请枚举每一行的文件名，找到源文件夹里匹配的文件，复制到目标文件夹。
# 3. 重命名：询问我列表路径（默认"d:\Studios\Attachments\Lists.txt"）。源文件夹路径（默认"d:\Studios\Folders\Ins\"）。列表里一行一个文件名（有扩展名）。请枚举每一行的文件名，重命名文件夹里的路径（按名称排序）。不涉及文件夹。
# 4. 文件路径生成：询问我列表路径（默认"d:\Studios\Attachments\Lists.txt"）。源文件夹路径（默认"d:\Studios\Folders\Ins\"）。询问我是否匹配文件夹，询问我是否包含子文件夹里。将源文件夹路径里的所有文件的路径写入列表中。
# 5. 文件名生成列表（包含子文件夹里）：询问我列表路径（默认"d:\Studios\Attachments\Lists.txt"）。源文件夹路径（默认"d:\Studios\Folders\Ins\"）。询问我是否匹配文件夹，询问我是否包含子文件夹里。将源文件夹路径里的所有文件的名称写入列表中。
# 结束后重复询问。

import shutil
import sys
from pathlib import Path

# ==================== 全局配置 ====================

DEFAULT_LIST_PATH = Path(r"d:\Studios\Attachments\Lists.txt")
DEFAULT_SOURCE_DIR = Path(r"d:\Studios\Folders\Ins")
DEFAULT_TARGET_DIR = Path(r"d:\Studios\Folders\Outs")

# ==================== 辅助函数 ====================


def get_input_with_default(prompt_text: str, default_value: str) -> str:
    """获取用户输入，若直接回车则返回默认值。"""
    user_input = input(f"{prompt_text} (默认: {default_value}): ").strip()
    return user_input if user_input else str(default_value)


def read_list_file(file_path: Path) -> list[str]:
    """读取列表文件，每行一个文件名，忽略空行。"""
    if not file_path.is_file():
        print(f"错误：列表文件不存在 -> {file_path}")
        return []
    text = file_path.read_text(encoding="utf-8-sig")
    return [line.strip() for line in text.splitlines() if line.strip()]


def collect_entries(
    src_dir: Path, include_folders: bool, include_subdirs: bool,
) -> list[str]:
    """收集源文件夹中的文件（及可选文件夹）路径。"""
    iterator = src_dir.rglob("*") if include_subdirs else src_dir.iterdir()
    entries: list[str] = []
    for p in iterator:
        if p.is_file():
            entries.append(str(p))
        elif p.is_dir() and include_folders:
            entries.append(str(p))
    return entries


# ==================== 核心操作 ====================


def move_files(list_path: Path, src_dir: Path, dst_dir: Path) -> None:
    """根据列表文件名，从源文件夹移动到目标文件夹。"""
    names = read_list_file(list_path)
    if not names:
        return
    if not src_dir.is_dir():
        print(f"错误：源文件夹不存在 -> {src_dir}")
        return
    dst_dir.mkdir(parents=True, exist_ok=True)

    moved = 0
    for name in names:
        src_path = src_dir / name
        dst_path = dst_dir / name
        if not src_path.is_file():
            print(f"警告：未找到文件，跳过 -> {src_path}")
            continue
        if dst_path.exists():
            print(f"警告：目标已存在，跳过 -> {dst_path}")
            continue
        shutil.move(str(src_path), str(dst_path))
        print(f"已移动: {name}")
        moved += 1
    print(f"移动完成，共处理 {moved} 个文件。")


def copy_files(list_path: Path, src_dir: Path, dst_dir: Path) -> None:
    """根据列表文件名，从源文件夹复制到目标文件夹。"""
    names = read_list_file(list_path)
    if not names:
        return
    if not src_dir.is_dir():
        print(f"错误：源文件夹不存在 -> {src_dir}")
        return
    dst_dir.mkdir(parents=True, exist_ok=True)

    copied = 0
    for name in names:
        src_path = src_dir / name
        dst_path = dst_dir / name
        if not src_path.is_file():
            print(f"警告：未找到文件，跳过 -> {src_path}")
            continue
        if dst_path.exists():
            print(f"警告：目标已存在，跳过 -> {dst_path}")
            continue
        shutil.copy2(str(src_path), str(dst_path))
        print(f"已复制: {name}")
        copied += 1
    print(f"复制完成，共处理 {copied} 个文件。")


def rename_files(list_path: Path, src_dir: Path) -> None:
    """按名称排序后，依次重命名为列表中提供的新名称。"""
    new_names = read_list_file(list_path)
    if not new_names:
        return
    if not src_dir.is_dir():
        print(f"错误：源文件夹不存在 -> {src_dir}")
        return

    old_names = sorted(p.name for p in src_dir.iterdir() if p.is_file())
    if len(old_names) != len(new_names):
        print(f"警告：源文件夹有 {len(old_names)} 个文件，列表提供 {len(new_names)} 个名称，数量不匹配。")
        if input("是否仍要继续重命名？(y/n): ").strip().lower() != "y":
            print("操作已取消。")
            return

    renamed = 0
    for old_name, new_name in zip(old_names, new_names):
        if old_name == new_name:
            print(f"跳过（名称未变）: {old_name}")
            continue
        new_path = src_dir / new_name
        if new_path.exists():
            print(f"警告：目标名称已存在，跳过 -> {new_name}")
            continue
        (src_dir / old_name).rename(new_path)
        print(f"重命名: {old_name} -> {new_name}")
        renamed += 1
    print(f"重命名完成，共处理 {renamed} 个文件。")


def generate_path_list(
    list_path: Path, src_dir: Path, include_folders: bool, include_subdirs: bool,
) -> None:
    """生成文件（及可选文件夹）路径列表写入指定文件。"""
    if not src_dir.is_dir():
        print(f"错误：源文件夹不存在 -> {src_dir}")
        return
    entries = collect_entries(src_dir, include_folders, include_subdirs)
    list_path.parent.mkdir(parents=True, exist_ok=True)
    list_path.write_text("\n".join(entries) + "\n", encoding="utf-8")
    print(f"已生成路径列表，共 {len(entries)} 条，保存至: {list_path}")


def generate_name_list(
    list_path: Path, src_dir: Path, include_folders: bool, include_subdirs: bool,
) -> None:
    """生成文件名（及可选文件夹名）列表写入指定文件。"""
    if not src_dir.is_dir():
        print(f"错误：源文件夹不存在 -> {src_dir}")
        return
    entries = collect_entries(src_dir, include_folders, include_subdirs)
    names = [Path(e).name for e in entries]
    list_path.parent.mkdir(parents=True, exist_ok=True)
    list_path.write_text("\n".join(names) + "\n", encoding="utf-8")
    print(f"已生成名称列表，共 {len(names)} 条，保存至: {list_path}")


# ==================== 主程序 ====================


def main() -> None:
    while True:
        print("\n===== 文件管理工具（列表驱动）=====")
        print("1. 移动")
        print("2. 复制")
        print("3. 重命名")
        print("4. 文件路径生成")
        print("5. 文件名生成列表")
        print("0. 退出")
        choice = input("请输入数字(0-5): ").strip()

        if choice == "0":
            print("程序已退出。")
            break

        elif choice == "1":
            print("\n--- 移动文件 ---")
            lst = Path(get_input_with_default("列表文件路径", str(DEFAULT_LIST_PATH)))
            src = Path(get_input_with_default("源文件夹路径", str(DEFAULT_SOURCE_DIR)))
            dst = Path(get_input_with_default("目标文件夹路径", str(DEFAULT_TARGET_DIR)))
            move_files(lst, src, dst)

        elif choice == "2":
            print("\n--- 复制文件 ---")
            lst = Path(get_input_with_default("列表文件路径", str(DEFAULT_LIST_PATH)))
            src = Path(get_input_with_default("源文件夹路径", str(DEFAULT_SOURCE_DIR)))
            dst = Path(get_input_with_default("目标文件夹路径", str(DEFAULT_TARGET_DIR)))
            copy_files(lst, src, dst)

        elif choice == "3":
            print("\n--- 重命名文件 ---")
            lst = Path(get_input_with_default("列表文件路径", str(DEFAULT_LIST_PATH)))
            src = Path(get_input_with_default("源文件夹路径", str(DEFAULT_SOURCE_DIR)))
            rename_files(lst, src)

        elif choice == "4":
            print("\n--- 生成文件路径列表 ---")
            lst = Path(get_input_with_default("列表文件路径", str(DEFAULT_LIST_PATH)))
            src = Path(get_input_with_default("源文件夹路径", str(DEFAULT_SOURCE_DIR)))
            inc_folders = get_input_with_default("是否包含文件夹路径？(y/n)", "n").lower() == "y"
            inc_sub = get_input_with_default("是否包含子文件夹？(y/n)", "n").lower() == "y"
            generate_path_list(lst, src, inc_folders, inc_sub)

        elif choice == "5":
            print("\n--- 生成文件名列表 ---")
            lst = Path(get_input_with_default("列表文件路径", str(DEFAULT_LIST_PATH)))
            src = Path(get_input_with_default("源文件夹路径", str(DEFAULT_SOURCE_DIR)))
            inc_folders = get_input_with_default("是否包含文件夹名称？(y/n)", "n").lower() == "y"
            inc_sub = get_input_with_default("是否包含子文件夹？(y/n)", "n").lower() == "y"
            generate_name_list(lst, src, inc_folders, inc_sub)

        else:
            print("无效的选择，请输入 0-5 之间的数字。")

        input("\n按回车键继续...")


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
