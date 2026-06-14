# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件夹位置（默认"d:\Studios\Folders\Ins\"）与目标文件夹位置（默认"d:\Studios\Folders\Outs\"）。
# 复制源文件夹位置内所有文件的文件名生成空文件到目标文件夹。

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


def create_empty_files(source_dir: Path, target_dir: Path) -> int:
    """
    根据源文件夹内文件的文件名，在目标文件夹中生成对应的空文件。
    返回创建的空文件数量。
    """
    # 检查源文件夹是否存在
    if not source_dir.is_dir():
        print(f"源文件夹 '{source_dir}' 不存在。")
        return 0

    # 确保目标文件夹存在
    target_dir.mkdir(parents=True, exist_ok=True)

    # 遍历源文件夹内所有文件（仅顶层，不递归子文件夹）
    file_count = 0
    for p in source_dir.iterdir():
        if not p.is_file():
            print(f"跳过非文件项：'{p.name}'")
            continue

        target_file = target_dir / p.name
        try:
            target_file.write_text("", encoding="utf-8")
            print(f"已创建空文件：'{p.name}'")
            file_count += 1
        except OSError as e:
            print(f"创建文件 '{p.name}' 时发生错误：{e}")

    return file_count


# ==================== 主程序 ====================


def main() -> None:
    """主函数：获取用户输入并执行空文件创建操作。"""

    # 获取用户输入
    source_str = get_input_with_default("请输入源文件夹位置：", str(DEFAULT_SOURCE_DIR))
    target_str = get_input_with_default("请输入目标文件夹位置：", str(DEFAULT_TARGET_DIR))

    source_dir = Path(source_str)
    target_dir = Path(target_str)

    # 执行
    count = create_empty_files(source_dir, target_dir)
    print(f"共创建 {count} 个空文件")


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
