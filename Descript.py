# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件夹位置。
# 遍历源文件夹位置中所有的文件（mkv、avi、f4v、flv、ts、mpeg、mpg、rm、rmvb、asf、wmv、mov、webm、mp4、mp3、ogg、aac、ac3、wma、pdf、epub、zip、rar、7z）。在该文件夹下生成同名 txt 文件。
# 写入的内容，UTF-8编码：
# ---
# 名字: {Name}
# 引用页: 
# 属于: 
# 主链接: 
# 下载方式: 
# ---
# 读取其文件名（包括后缀名），替换文中{Name}。

# 导入模块
import os

def main():
    # 定义支持的扩展名集合（统一小写格式，带点号）
    SUPPORTED_EXTENSIONS = {
        '.mkv', '.avi', '.f4v', '.flv', '.ts',
        '.mpeg', '.mpg', '.rm', '.rmvb', '.asf',
        '.wmv', '.mov', '.webm', '.mp4',
        '.mp3', '.ogg', '.aac', '.wma', '.ac3',
        '.pdf', '.epub',
        '.zip', '.rar', '.7z'
    }

    # 定义文本模板
    TEMPLATE = """---
名字: {Name}
引用页: 
属于: 
主链接: 
下载方式: 
---"""

    # 获取并清理输入的文件夹路径
    source_dir = input("请输入源文件夹位置：").strip('"').strip()

    # 验证文件夹有效性
    if not os.path.isdir(source_dir):
        print("错误：指定的路径不存在或不是文件夹！")
        return

    # 计数器记录生成文件数
    generated_count = 0

    # 遍历文件夹及其所有子文件夹
    for root, _, files in os.walk(source_dir):
        for filename in files:
            # 获取文件扩展名（保留点号并转换为小写）
            file_ext = os.path.splitext(filename)[1].lower()
            
            # 检查是否为支持的文件类型
            if file_ext in SUPPORTED_EXTENSIONS:
                # 构建原始文件完整路径
                original_path = os.path.join(root, filename)
                
                # 生成目标txt文件路径（与原始文件同级）
                txt_path = f"{original_path}.txt"

                try:
                    # 替换模板中的占位符
                    content = TEMPLATE.replace("{Name}", filename)
                    
                    # 写入UTF-8编码文件（新增：避免覆盖已有文件）
                    if not os.path.exists(txt_path):
                        with open(txt_path, "w", encoding="utf-8") as f:
                            f.write(content)
                        generated_count += 1
                        print(f"已生成：{txt_path}")
                    else:
                        print(f"跳过已存在文件：{txt_path}")
                
                except PermissionError:
                    print(f"权限不足，无法写入：{txt_path}")
                except Exception as e:
                    print(f"处理 {filename} 时发生错误：{str(e)}")

    print(f"\n处理完成！共生成 {generated_count} 个文本文件")
    input("按回车键退出程序...")

if __name__ == "__main__":
    main()