# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件夹位置（默认为 d:\\Works\\In\\）与目标文件夹位置（默认为 d:\\Works\\Out\\）。
# 遍历源文件夹内所有图片文件（bmp、jpg、jpeg、png、webp、avif、heic），进行调整大小：1280*720：宽度1280，高度根据宽度调整保持纵横比。
# 生成的文件放到目标文件夹中以“源文件夹的子文件夹”中，保持文件夹及子文件结构。如果生成新文件成功，则删除原始文件。

# 导入模块
import os
import shutil
from PIL import Image

def resize_and_move_images(source_dir, target_dir):
    """
    调整图片大小并移动到目标文件夹，保持目录结构
    
    参数:
        source_dir (str): 源文件夹路径
        target_dir (str): 目标文件夹路径
    """
    # 支持的图片格式
    valid_exts = ('.bmp', '.jpg', '.jpeg', '.png', '.webp', '.avif', '.heic')
    # 目标宽度
    target_width = 1280
    
    # 遍历源文件夹及其所有子文件夹
    for root, dirs, files in os.walk(source_dir):
        for filename in files:
            # 检查文件扩展名
            ext = os.path.splitext(filename)[1].lower()
            if ext not in valid_exts:
                continue
                
            # 源文件完整路径
            source_path = os.path.join(root, filename)
            
            # 计算相对路径（用于在目标文件夹中创建相同结构）
            rel_path = os.path.relpath(root, source_dir)
            target_subdir = os.path.join(target_dir, rel_path)
            
            # 创建目标子目录（如果不存在）
            os.makedirs(target_subdir, exist_ok=True)
            
            # 目标文件完整路径
            target_path = os.path.join(target_subdir, filename)
            
            try:
                # 打开原始图片
                with Image.open(source_path) as img:
                    # 计算新高度（保持原始宽高比）
                    w_percent = target_width / float(img.size[0])
                    new_height = int(float(img.size[1]) * float(w_percent))
                    
                    # 调整图片尺寸
                    resized_img = img.resize((target_width, new_height), Image.LANCZOS)
                    
                    # 保存调整后的图片到目标路径
                    resized_img.save(target_path, quality=95)
                    print(f"✓ 已调整尺寸: {target_width}x{new_height} | 保存到: {target_path}")
                    
                    # 删除原始文件（仅在新文件成功创建后）
                    os.remove(source_path)
                    print(f"✓ 已删除原始文件: {source_path}")
                    
            except Exception as e:
                print(f"✗ 处理失败: {source_path} | 错误: {e}")

def main():
    """主函数：用户交互和图片处理"""
   
    # 获取源文件夹路径（带默认值）
    source_dir = input("\n请输入源文件夹路径（默认为 d:\\Works\\In\\）: ").strip()
    if not source_dir:
        source_dir = "d:\\Works\\In\\"
    
    # 获取目标文件夹路径（带默认值）
    target_dir = input("请输入目标文件夹路径（默认为 d:\\Works\\Out\\）: ").strip()
    if not target_dir:
        target_dir = "d:\\Works\\Out\\"
    
    # 确保路径以分隔符结尾
    source_dir = os.path.normpath(source_dir) + os.sep
    target_dir = os.path.normpath(target_dir) + os.sep
    
    # 检查文件夹是否存在
    if not os.path.isdir(source_dir):
        print(f"错误：源文件夹不存在 - {source_dir}")
        return
    if not os.path.isdir(target_dir):
        print(f"目标文件夹不存在，正在创建: {target_dir}")
        os.makedirs(target_dir, exist_ok=True)
    
    print("\n开始处理图片...")
    print(f"源文件夹: {source_dir}")
    print(f"目标文件夹: {target_dir}")
    print("目标尺寸: 1280×720 (宽度固定，高度按比例调整)")
    print("-"*50)
    
    # 执行图片处理
    resize_and_move_images(source_dir, target_dir)
    
    print("\n" + "="*50)
    print("所有图片处理完成！")
    print(f"源文件夹中的图片已删除")
    print(f"处理后的图片已保存到: {target_dir}")
    print("="*50)

if __name__ == "__main__":
    # 检查Pillow库是否安装
    try:
        from PIL import Image
    except ImportError:
        print("错误：需要安装Pillow库，请执行: pip install Pillow")
        exit(1)
    
    main()

if __name__ == "__main__":
    compress_file()
    input("按回车键退出...")