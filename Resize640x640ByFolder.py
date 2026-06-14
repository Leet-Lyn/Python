# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件夹位置（默认 D:\Studios\Folders\Ins\）与目标文件夹位置
# （默认 D:\Studios\Folders\Outs\）。
# 依次读取源文件夹下所有图片文件（bmp / jpg / jpeg / png / webp / avif / heic），
# 调整大小。强制 640×640 正方形（不保持纵横比）。
# 生成的文件放到目标文件夹中保持子目录结构。成功则删除源文件。

import sys
from pathlib import Path

from PIL import Image

# --- 常量 ---
VALID_EXTS = {".bmp", ".jpg", ".jpeg", ".png", ".webp", ".avif", ".heic"}
TARGET_SIZE = (640, 640)


def resize_image(source: Path, output: Path) -> bool:
    """强制调整为 640×640，保存到 output，成功返回 True 并删除 source。"""
    try:
        with Image.open(source) as img:
            resized = img.resize(TARGET_SIZE, Image.LANCZOS)
            output.parent.mkdir(parents=True, exist_ok=True)
            resized.save(output, quality=95)
        source.unlink()
        print(f"  ✅ {source.name} → {output}")
        return True
    except Exception as e:
        print(f"  ❌ 处理失败：{source.name} | {e}")
        return False


def main() -> None:
    """主流程：获取源/目标文件夹 → 遍历图片 → 强制 640×640 → 统计。"""
    default_src = r"D:\Studios\Folders\Ins"
    default_dst = r"D:\Studios\Folders\Outs"

    raw = input(f"请输入源文件夹（回车默认 {default_src}）：").strip()
    src_root = Path(raw) if raw else Path(default_src)
    raw = input(f"请输入目标文件夹（回车默认 {default_dst}）：").strip()
    dst_root = Path(raw) if raw else Path(default_dst)

    if not src_root.is_dir():
        print(f"错误：源文件夹不存在 —— {src_root}")
        return

    # 收集所有图片文件
    all_files = sorted(
        p for p in src_root.rglob("*")
        if p.is_file() and p.suffix.lower() in VALID_EXTS
    )
    total = len(all_files)

    if not total:
        print("未找到可处理的图片文件。")
        return

    print(f"\n找到 {total} 个文件，开始强制 640×640 调整...\n")
    ok = 0
    fail = 0

    for idx, src in enumerate(all_files, 1):
        try:
            rel = src.parent.relative_to(src_root)
        except ValueError:
            rel = Path()
        dst = dst_root / rel / src.name

        print(f"[{idx}/{total}] {src.relative_to(src_root)}")
        if resize_image(src, dst):
            ok += 1
        else:
            fail += 1

    print(f"\n处理完成：成功 {ok} 个，失败 {fail} 个，共 {total} 个。")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
    input("按回车键退出...")
