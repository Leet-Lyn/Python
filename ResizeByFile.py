# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件位置。
# 将该图片文件（bmp、jpg、jpeg、png、webp、avif、heic）调整大小。
# 让我选择：1.640*480：宽度640，高度根据宽度调整保持纵横比；2.800*600：宽度800，高度根据宽度调整保持纵横比；3.1024*768：宽度1024，高度根据宽度调整保持纵横比；4.1280*720：宽度1280，高度根据宽度调整保持纵横比；5.1920*1080：宽度1920，高度根据宽度调整保持纵横比；5.3840*2160：宽度3840，高度根据宽度调整保持纵横比；5.7680*4320：宽度7680，高度根据宽度调整保持纵横比；
# 选项 0：强制 640×640 正方形（不保持纵横比）。其余选项：宽度固定，高度按纵横比自动计算。
# 生成的文件替换源文件。
# 如此循环，再次前询问我源文件位置。

import sys
from pathlib import Path

from PIL import Image

# --- 支持的格式与尺寸 ---
VALID_EXTS = {".bmp", ".jpg", ".jpeg", ".png", ".webp", ".avif", ".heic"}

SIZE_OPTIONS: dict[str, tuple[int | tuple[int, int], str]] = {
    "0": ((640, 640), "640×640  (正方) [默认]"),
    "1": (640,   "640×480  (标清)"),
    "2": (800,   "800×600  (SVGA)"),
    "3": (1024,  "1024×768 (XGA)"),
    "4": (1280,  "1280×720 (高清)"),
    "5": (1920,  "1920×1080 (全高清)"),
    "6": (3840,  "3840×2160 (4K)"),
    "7": (7680,  "7680×4320 (8K)"),
}


def resize_image(image_path: Path, target: int | tuple[int, int]) -> None:
    """调整图片大小并覆盖源文件。int=固定宽度保持纵横比；tuple=强制该尺寸。"""
    try:
        with Image.open(image_path) as img:
            if isinstance(target, tuple):
                size = target
            else:
                w_percent = target / float(img.size[0])
                new_height = int(float(img.size[1]) * w_percent)
                size = (target, new_height)
            resized_img = img.resize(size, Image.LANCZOS)
            resized_img.save(image_path, quality=95)
            print(f"✓ 已调整尺寸: {size[0]}×{size[1]} | 覆盖保存: {image_path}")
    except Exception as e:
        print(f"✗ 处理失败: {e}")


def main() -> None:
    """主循环：输入文件 → 选择尺寸 → 调整 → 替换。"""
    while True:
        raw = input("\n请输入图片路径（输入 Q 退出）: ").strip()

        if raw.lower() in ("q", "quit", "exit"):
            print("\n程序已退出")
            break

        source = Path(raw.strip("\"'"))
        if not source.is_file():
            print("错误：文件不存在，请重新输入")
            continue

        ext = source.suffix.lower()
        if ext not in VALID_EXTS:
            print(f"错误：不支持的格式 {ext}，支持: {', '.join(sorted(VALID_EXTS))}")
            continue

        print("\n请选择目标尺寸（回车默认 640×640）:")
        for key in sorted(SIZE_OPTIONS, key=int):
            _, label = SIZE_OPTIONS[key]
            print(f"  {key}. {label}")

        choice = input("请输入选项数字 (0-7, 默认 0): ").strip() or "0"
        if choice in SIZE_OPTIONS:
            target, _ = SIZE_OPTIONS[choice]
        else:
            print("无效选择，将使用默认尺寸 640×640")
            target, _ = SIZE_OPTIONS["0"]

        resize_image(source, target)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
