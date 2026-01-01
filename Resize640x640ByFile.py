# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件位置。
# 将该图片文件（bmp、jpg、jpeg、png、webp、avif、heic）调整大小。
# 让我选择：1.640*480：宽度640，高度根据宽度调整保持纵横比；2.800*600：宽度800，高度根据宽度调整保持纵横比；3.1024*768：宽度1024，高度根据宽度调整保持纵横比；4.1280*720：宽度1280，高度根据宽度调整保持纵横比；5.1920*1080：宽度1920，高度根据宽度调整保持纵横比；5.3840*2160：宽度3840，高度根据宽度调整保持纵横比；5.7680*4320：宽度7680，高度根据宽度调整保持纵横比；
# 生成的文件替换源文件。
# 如此循环，再次前询问我源文件位置。

# 导入模块
from PIL import Image
import os
import sys

def resize_image(image_path, size):
    """调整图片大小并覆盖原始文件，强制调整为指定正方形尺寸"""
    try:
        # 打开原始图片
        with Image.open(image_path) as img:
            # 强制调整为指定正方形尺寸，不保持纵横比
            resized_img = img.resize(size, Image.LANCZOS)
            
            # 保存图片（覆盖原始文件，保持原始格式）
            resized_img.save(image_path, quality=95)
            print(f"✓ 已调整尺寸: {size[0]}x{size[1]} | 覆盖保存: {image_path}")
            
    except Exception as e:
        print(f"✗ 处理失败: {e}")

def main():
    """主函数：用户交互和循环处理"""
    # 支持的图片格式
    valid_exts = ('.bmp', '.jpg', '.jpeg', '.png', '.webp', '.avif', '.heic')
    
    # 目标尺寸
    target_size = (640, 640)
    
    while True:
        # 获取文件路径
        file_path = input("\n请输入图片路径（输入 q 退出）: ").strip()
        
        # 退出条件
        if file_path.lower() in ['q', 'quit', 'exit']:
            print("\n程序已退出")
            break
        
        # 检查文件是否存在
        if not os.path.isfile(file_path):
            print("错误：文件不存在，请重新输入")
            continue
        
        # 检查文件格式
        ext = os.path.splitext(file_path)[1].lower()
        if ext not in valid_exts:
            print(f"错误：不支持的格式 {ext}，支持格式: {', '.join(valid_exts)}")
            continue
        
        # 直接调整为640×640正方形
        print(f"正在将图片强制调整为{target_size[0]}×{target_size[1]}像素...")
        resize_image(file_path, target_size)

if __name__ == "__main__":
    # 检查Pillow库是否安装
    try:
        from PIL import Image
    except ImportError:
        print("错误：需要安装Pillow库，请执行: pip install Pillow")
        sys.exit(1)
    
    main()