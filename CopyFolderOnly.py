# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件夹位置（默认"d:\Studios\Folders\Ins\"）与目标文件夹位置（默认"d:\Studios\Folders\Outs\"）。
# 复制源文件夹结构到目标文件夹中，但不复制文件。

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


def copy_folder_structure(source_dir: Path, target_dir: Path) -> int:
    """
    从源文件夹复制文件夹结构到目标文件夹，但不复制文件。
    返回创建的文件夹数量。
    """
    # 检查源文件夹是否存在
    if not source_dir.is_dir():
        print(f"源文件夹 '{source_dir}' 不存在。")
        return 0

    # 确保目标根文件夹存在
    target_dir.mkdir(parents=True, exist_ok=True)

    # 收集源文件夹下所有子目录（递归），排除根目录自身
    all_dirs = [p for p in source_dir.rglob("*") if p.is_dir()]

    count = 0
    for sub_dir in all_dirs:
        rel = sub_dir.relative_to(source_dir)
        new_dir = target_dir / rel
        if not new_dir.is_dir():
            new_dir.mkdir(parents=True, exist_ok=True)
            print(f"已创建文件夹：'{new_dir}'")
            count += 1

    return count


# ==================== 主程序 ====================


def main() -> None:
    """主函数：获取用户输入并执行文件夹结构复制操作。"""

    source_str = get_input_with_default("请输入源文件夹位置：", str(DEFAULT_SOURCE_DIR))
    target_str = get_input_with_default("请输入目标文件夹位置：", str(DEFAULT_TARGET_DIR))

    source_dir = Path(source_str)
    target_dir = Path(target_str)

    count = copy_folder_structure(source_dir, target_dir)
    print(f"文件夹结构复制完成！共创建 {count} 个文件夹。")


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
