# 请帮我写个中文的 Python 脚本，批注也是中文：
# 询问我复制还是删除。
# 选择复制，询问源文件夹（默认：d:\Studios\Folders\Ins\）与目标文件夹（默认：d:\Studios\Folders\Outs\）。根据源文件名（不包括扩展名），找出源文件夹里所有同名文件（扩展名可以不同），连同其父文件夹复制到目标文件夹中。
# 选择删除，询问源文件夹（默认：d:\Studios\Folders\Ins\）。删除源文件，同时 根据源文件名（不包括扩展名），找出源文件夹里所有同名文件（扩展名可以不同），一并删除。
# 完成后，再次循环。

import shutil
import sys
from pathlib import Path

# ==================== 全局配置 ====================

DEFAULT_SOURCE_DIR = Path(r"d:\Studios\Folders\Ins")
DEFAULT_TARGET_DIR = Path(r"d:\Studios\Folders\Outs")


# ==================== 辅助函数 ====================


def get_input_with_default(prompt_text: str, default_value: str) -> str:
    """获取带默认值的用户输入。"""
    user_input = input(f"{prompt_text} (默认: {default_value}): ").strip()
    return user_input if user_input else str(default_value)


# ==================== 处理函数 ====================


def find_files_by_stem(root_dir: Path, stem: str) -> list[Path]:
    """
    在 root_dir 目录下递归查找所有主文件名等于 stem 的文件。
    """
    return [p for p in root_dir.rglob("*") if p.is_file() and p.stem == stem]


def copy_file_with_parents(src: Path, dst_root: Path, src_root: Path) -> bool:
    """
    将 src 复制到 dst_root，保留相对于 src_root 的目录结构。
    """
    try:
        rel = src.relative_to(src_root)
        dst = dst_root / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(src), str(dst))
        print(f"  已复制: {src} -> {dst}")
        return True
    except OSError as e:
        print(f"  复制失败: {src}\n    错误: {e}")
        return False


def delete_files(file_paths: list[Path], confirm: bool = True) -> None:
    """删除给定的文件列表，可选确认。"""
    if not file_paths:
        print("  没有需要删除的文件。")
        return

    print("即将删除以下文件：")
    for f in file_paths:
        print(f"  {f}")

    if confirm:
        answer = input("确认删除以上所有文件吗？(y/n)：").strip().lower()
        if answer != "y":
            print("已取消删除操作。")
            return

    for f in file_paths:
        try:
            f.unlink()
            print(f"  已删除: {f}")
        except OSError as e:
            print(f"  删除失败: {f}\n    错误: {e}")


# ==================== 主程序 ====================


def main() -> None:
    print("=== 同名文件（不同扩展名）批量处理工具 ===")

    while True:
        print("\n请选择操作：")
        print("  1 - 复制")
        print("  2 - 删除")
        print("  0 或 q - 退出")
        choice = input("请输入数字 (1/2/0)：").strip().lower()

        if choice in ("0", "q", "quit", "exit"):
            print("程序结束。")
            break

        if choice == "1":
            # ---------- 复制模式 ----------
            src_input = get_input_with_default("请输入源文件路径（用于提取主文件名）：", "")
            if not src_input:
                print("错误：未输入文件路径，操作取消。")
                continue

            src_file = Path(src_input)
            if not src_file.is_file():
                print(f"错误：文件不存在 -> {src_file}，操作取消。")
                continue

            stem = src_file.stem
            print(f"提取的文件主名：{stem}")

            src_root_str = get_input_with_default("请输入源文件夹：", str(DEFAULT_SOURCE_DIR))
            src_root = Path(src_root_str)
            if not src_root.is_dir():
                print(f"错误：源文件夹不存在 -> {src_root}，操作取消。")
                continue

            dst_root_str = get_input_with_default("请输入目标文件夹：", str(DEFAULT_TARGET_DIR))
            dst_root = Path(dst_root_str)
            dst_root.mkdir(parents=True, exist_ok=True)

            matched = find_files_by_stem(src_root, stem)
            if not matched:
                print(f"在源文件夹 {src_root} 中没有找到主名为 {stem} 的文件。")
                continue

            print(f"找到 {len(matched)} 个匹配的文件：")
            for f in matched:
                print(f"  {f}")

            confirm = input("确认复制这些文件到目标文件夹吗？(y/n)：").strip().lower()
            if confirm != "y":
                print("复制操作已取消。")
                continue

            ok = sum(1 for f in matched if copy_file_with_parents(f, dst_root, src_root))
            print(f"复制完成：成功 {ok} / 总数 {len(matched)}")

        elif choice == "2":
            # ---------- 删除模式 ----------
            src_input = get_input_with_default("请输入源文件路径（用于提取主文件名，该文件本身也会被删除）：", "")
            if not src_input:
                print("错误：未输入文件路径，操作取消。")
                continue

            src_file = Path(src_input)
            if not src_file.is_file():
                print(f"错误：文件不存在 -> {src_file}，操作取消。")
                continue

            stem = src_file.stem
            print(f"提取的文件主名：{stem}")

            src_root_str = get_input_with_default("请输入源文件夹：", str(DEFAULT_SOURCE_DIR))
            src_root = Path(src_root_str)
            if not src_root.is_dir():
                print(f"错误：源文件夹不存在 -> {src_root}，操作取消。")
                continue

            matched = find_files_by_stem(src_root, stem)
            if src_file not in matched:
                matched.append(src_file)

            # 去重（保持顺序）
            seen: set[str] = set()
            unique: list[Path] = []
            for f in matched:
                key = str(f.resolve())
                if key not in seen:
                    seen.add(key)
                    unique.append(f)
            matched = unique

            if not matched:
                print(f"没有找到任何需要删除的文件（主名 {stem}）。")
                continue

            print(f"将要删除的文件（共 {len(matched)} 个）：")
            for f in matched:
                print(f"  {f}")

            confirm = input("确认永久删除以上所有文件吗？(y/n)：").strip().lower()
            if confirm != "y":
                print("删除操作已取消。")
                continue

            delete_files(matched, confirm=False)
            print("删除操作执行完毕。")

        else:
            print("无效输入，请输入 1、2 或 0 退出。")


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
