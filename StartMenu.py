# 请帮我写个中文的 Python 脚本，批注也是中文。
# 开始询问我目标文件夹位置（默认为 E:\Backups\Windows\StartMenu\）。依次运行该文件夹下所有 *.lnk 指向的内容。

# 导入模块
import os
import time
from pathlib import Path


def main() -> None:
    """主流程：获取目标文件夹 → 扫描 .lnk → 依次启动 → 输出统计。"""
    # --- 获取目标文件夹路径 ---
    raw = input(r"请输入目标文件夹位置（默认 E:\Backups\Windows\StartMenu\）：").strip()
    folder = Path(raw) if raw else Path(r"E:\Backups\Windows\StartMenu")

    # 解析为绝对路径
    try:
        folder = folder.resolve()
    except OSError as e:
        print(f"错误：无法解析路径 '{folder}' —— {e}")
        return

    # 检查目标文件夹是否存在
    if not folder.is_dir():
        print(f"错误：文件夹 '{folder}' 不存在。")
        return

    # --- 扫描目录下所有 .lnk 文件 ---
    lnk_files = sorted(
        p for p in folder.iterdir()
        if p.is_file() and p.suffix.lower() == ".lnk"
    )

    if not lnk_files:
        print(f"在文件夹 '{folder}' 中未找到任何快捷方式文件。")
        return

    print(f"找到 {len(lnk_files)} 个快捷方式，开始依次启动...\n")

    # --- 依次启动 ---
    ok = 0
    fail = 0

    for lnk in lnk_files:
        try:
            os.startfile(str(lnk))
            print(f"✅ 已启动：{lnk.name}")
            ok += 1
        except Exception as e:
            print(f"❌ 启动失败：{lnk.name}\n    错误信息：{e}")
            fail += 1
        # 短暂间隔，避免瞬间打开大量应用导致系统卡顿
        time.sleep(0.3)

    # --- 输出统计 ---
    print(f"\n完成：成功 {ok} 个，失败 {fail} 个，共 {len(lnk_files)} 个。")


# 程序入口
if __name__ == "__main__":
    main()

# 按下回车键退出。
input("按回车键退出...")
