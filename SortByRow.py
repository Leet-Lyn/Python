# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件位置（默认“e:\Documents\Creations\Scripts\Attachment\Files.txt”）。
# 将文件按行读取，按字母顺序排序重新排序，再次写入文件。

# 导入模块
import os

def sort_file_lines():
    """
    文件内容排序主函数
    功能：读取用户指定的文件，按字母顺序排序行内容后覆盖原文件
    """
    # 步骤1：获取用户输入的文件路径，设置默认值
    default_path = "e:\\Documents\\Creations\\Scripts\\Attachment\\Files.txt"
    user_input = input(f"请输入要处理的文件路径（默认为'{default_path}'）：").strip('"').strip()
    
    # 如果用户直接按回车，则使用默认路径
    file_path = user_input if user_input else default_path

    # 步骤2：验证文件有效性
    if not os.path.isfile(file_path):
        print(f"错误：'{file_path}' 不是有效的文件路径！")
        input("按回车键退出...")
        return

    try:
        # 步骤3：读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.read().splitlines()  # 读取所有行并移除换行符

        # 步骤4：处理空文件情况
        if not lines:
            print("文件内容为空，无需处理！")
            input("按回车键退出...")
            return

        # 步骤5：按字母顺序排序（区分大小写）
        sorted_lines = sorted(lines)

        # 步骤6：写入排序后的内容
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(sorted_lines))  # 用换行符连接已排序的内容

        print("文件内容已成功排序并保存！")

    except PermissionError:
        print(f"错误：没有写入权限，请关闭文件后重试 - {file_path}")
    except UnicodeDecodeError:
        print("错误：文件编码不支持，请使用UTF-8编码的文本文件")
    except Exception as e:
        print(f"处理过程中发生未知错误：{str(e)}")
    
    input("按回车键退出...")

if __name__ == "__main__":
    sort_file_lines()