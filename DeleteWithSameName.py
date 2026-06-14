# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件夹位置（默认为 d:\Studios\Folders\Ins\）与目标文件夹位置（默认为 d:\Studios\Folders\Outs\）。
# 询问我是否排除扩展名（扩展名可以不同，大小写敏感）。
# 依次读取目标文件夹的所有文件的文件名，如果源文件夹内存在名字相同的文件（大小写敏感），则删除源文件的文件。
# 要求如果文件夹内有子文件夹，递归实现。

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


def delete_duplicate_files(
    source_dir: Path,
    target_dir: Path,
    exclude_extension: bool = False,
) -> tuple[int, int]:
    """
    递归遍历目标文件夹，删除源文件夹中同名文件（大小写敏感）。
    若 exclude_extension=True，仅匹配主文件名（忽略扩展名）；
    否则匹配完整文件名。
    返回 (删除成功数, 删除失败数)。
    """
    # 第一步：收集目标文件夹匹配键
    if exclude_extension:
        target_keys = {p.stem for p in target_dir.rglob("*") if p.is_file()}
        get_key = lambda p: p.stem
        label = "主文件名"
    else:
        target_keys = {p.name for p in target_dir.rglob("*") if p.is_file()}
        get_key = lambda p: p.name
        label = "完整文件名"

    print(f"\n匹配模式：{label}（大小写敏感）")

    # 第二步：遍历源文件夹并删除匹配文件
    deleted = 0
    failed = 0

    for src_file in source_dir.rglob("*"):
        if not src_file.is_file():
            continue
        if get_key(src_file) not in target_keys:
            continue

        try:
            src_file.unlink()
            print(f"已删除: {src_file}")
            deleted += 1
        except OSError as e:
            print(f"删除失败: {src_file} - {e}")
            failed += 1

    return deleted, failed


# ==================== 主程序 ====================


def main() -> None:
    """主函数：获取用户输入并执行重复文件删除。"""

    source_str = get_input_with_default("请输入源文件夹路径：", str(DEFAULT_SOURCE_DIR))
    target_str = get_input_with_default("请输入目标文件夹路径：", str(DEFAULT_TARGET_DIR))

    source_dir = Path(source_str)
    target_dir = Path(target_str)

    if not source_dir.is_dir():
        print(f"错误: 源文件夹不存在 [{source_dir}]")
        return
    if not target_dir.is_dir():
        print(f"错误: 目标文件夹不存在 [{target_dir}]")
        return
    if source_dir.resolve() == target_dir.resolve():
        print("错误: 源文件夹与目标文件夹相同，操作将删除全部文件，已阻止。")
        return

    # 询问是否排除扩展名
    ext_choice = input("是否排除扩展名（仅匹配主文件名）？(y/n，默认 n): ").strip().lower()
    exclude_extension = ext_choice in ("y", "yes")

    print(f"\n开始清理: {source_dir}")
    print(f"参照目录: {target_dir}")

    deleted, failed = delete_duplicate_files(source_dir, target_dir, exclude_extension)

    print(f"\n{'=' * 50}")
    print(f"操作完成！共删除 {deleted} 个文件，失败 {failed} 个。")
    print(f"目标文件夹文件总数: {sum(1 for p in target_dir.rglob('*') if p.is_file())}")
    print(f"{'=' * 50}")


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
