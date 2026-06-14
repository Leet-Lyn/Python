# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件夹位置（默认 d:\Studios\Folders\Ins\）与目标文件夹位置（默认 d:\Studios\Folders\Outs\）。
# 遍历源文件夹内所有子文件夹中的文件（剔除隐藏文件）。
# 用 Leanify 进行压缩，生成的文件放到目标文件夹中保持子目录结构。

import shutil
import subprocess
import sys
from pathlib import Path

# --- 常量 ---
LEANIFY_EXE = Path(r"D:\ProApps\Leanify\Leanify.exe")


def is_hidden_file(file_path: Path) -> bool:
    """判断文件是否为隐藏文件。"""
    # 文件名以点开头（Unix/Linux / 部分 Windows 场景）
    if file_path.name.startswith("."):
        return True

    # Windows 文件属性检查
    try:
        import win32con
        import win32file
        attributes = win32file.GetFileAttributes(str(file_path))
        return bool(attributes & (win32con.FILE_ATTRIBUTE_HIDDEN | win32con.FILE_ATTRIBUTE_SYSTEM))
    except Exception:
        pass

    try:
        return bool(file_path.stat().st_file_attributes & 0x2)
    except Exception:
        return False


def main() -> None:
    """主流程：获取源/目标文件夹 → 遍历文件 → Leanify 压缩 → 统计。"""
    raw = input(
        r"请输入源文件夹位置（回车默认 d:\Studios\Folders\Ins\）："
    ).strip()
    input_path = Path(raw) if raw else Path(r"d:\Studios\Folders\Ins")
    raw = input(
        r"请输入目标文件夹位置（回车默认 d:\Studios\Folders\Outs\）："
    ).strip()
    output_path = Path(raw) if raw else Path(r"d:\Studios\Folders\Outs")

    if not input_path.is_dir():
        print(f"源文件夹路径无效：{input_path}")
        return

    output_path.mkdir(parents=True, exist_ok=True)

    total = 0
    ok = 0
    skipped = 0
    fail = 0

    for file_path in input_path.rglob("*"):
        if not file_path.is_file():
            continue

        if is_hidden_file(file_path):
            skipped += 1
            continue

        total += 1
        relative_dir = file_path.parent.relative_to(input_path)
        target_dir = output_path / relative_dir
        target_dir.mkdir(parents=True, exist_ok=True)
        target_file = target_dir / file_path.name

        try:
            result = subprocess.run(
                [str(LEANIFY_EXE), str(file_path)],
                capture_output=True,
            )

            if result.returncode == 0:
                shutil.move(str(file_path), str(target_file))
                print(f"✅ {file_path} → {target_file}")
                ok += 1
            else:
                print(f"❌ 压缩失败：{file_path}，错误码：{result.returncode}")
                fail += 1
        except FileNotFoundError:
            print(f"❌ 未找到 Leanify：{LEANIFY_EXE}")
            return
        except Exception as e:
            print(f"❌ 处理文件 {file_path} 时发生错误：{e}")
            fail += 1

    print(f"\n处理完成：成功 {ok}，失败 {fail}，跳过隐藏 {skipped}，共扫描 {total + skipped}。")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
    input("按回车键退出...")
