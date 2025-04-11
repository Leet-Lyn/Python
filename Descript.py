# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件位置。
# 生成同名 txt 文件。
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

# 获取用户输入的源文件路径，并去除首尾可能存在的引号
source_path = input("请输入源文件位置：").strip('"').strip("'")

# 检查文件是否存在
if not os.path.exists(source_path):
    print("错误：指定的文件不存在！")
    exit()

# 从路径中提取文件名（包含后缀）
file_name = os.path.basename(source_path)

# 构建目标txt文件路径（原路径同级目录，追加.txt后缀）
target_path = os.path.join(
    os.path.dirname(source_path),  # 获取原目录路径
    f"{file_name}.txt"            # 原文件名追加.txt
)

# 定义文本模板
template = """---
名字: {Name}
引用页: 
属于: 
主链接: 
下载方式: 
---"""

# 使用文件名替换模板中的占位符
content = template.replace("{Name}", file_name)

try:
    # 写入UTF-8编码文本文件
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"文件已生成：{target_path}")
except PermissionError:
    print("错误：没有写入权限！")
except Exception as e:
    print(f"发生未知错误：{str(e)}")

# 按下回车键退出。
input("按回车键退出...")