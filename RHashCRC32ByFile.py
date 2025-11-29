# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件位置。
# 计算并生成文件的 CRC32，用方括号“[]”包绕并写入剪贴板。
# 我安装了 RHash，位置“d:\ProApps\RHash\rhash.exe”。
# 如此循环，再次前询问我源文件位置。

# 导入模块
import subprocess
import pyperclip
import os
import sys

def get_crc32_hash(file_path):
    """
    使用RHash计算文件的CRC32值    
    参数:
        file_path: 文件路径        
    返回:
        用方括号包绕的CRC32值字符串，如果失败则返回None
    """
    try:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            print(f"错误：文件 '{file_path}' 不存在")
            return None
            
        # 构建RHash命令 - 使用--crc32参数计算CRC32值
        rhash_path = r"d:\ProApps\RHash\rhash.exe"
        command = [rhash_path, "--crc32", file_path]
        
        # 执行命令并获取输出
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        
        # RHash输出格式通常是 "文件路径  哈希值"
        # 我们需要提取CRC32部分
        output = result.stdout.strip()
        
        # 从输出中提取CRC32值
        # 假设输出格式为 "文件路径  CRC32值"
        parts = output.split()
        if len(parts) >= 2:
            crc32_value = parts[-1].upper()  # 取最后一个部分并转为大写
            return f"[{crc32_value}]"
        else:
            print(f"无法解析RHash输出: {output}")
            return None
            
    except subprocess.CalledProcessError as e:
        print(f"RHash执行错误: {e}")
        return None
    except Exception as e:
        print(f"计算CRC32时发生错误: {e}")
        return None

def main():
    """
    主函数：循环询问文件路径并计算CRC32值
    """   
    while True:
        try:
            # 询问用户输入文件路径
            file_path = input("请输入源文件路径（输入'quit'退出程序）: ").strip()
            
            # 检查是否退出
            if file_path.lower() in ['quit', 'exit', 'q']:
                print("程序已退出")
                break
                
            # 移除路径两端的引号（如果有的话）
            file_path = file_path.strip('"\'')
            
            # 检查输入是否为空
            if not file_path:
                print("错误：文件路径不能为空")
                continue
                
            # 计算CRC32值
            print(f"\n正在计算文件的CRC32值: {file_path}")
            crc32_value = get_crc32_hash(file_path)
            
            if crc32_value:
                # 显示在屏幕上
                print("生成的CRC32值:")
                print(crc32_value)
                
                # 写入剪贴板
                try:
                    pyperclip.copy(crc32_value)
                    print("✓ CRC32值已复制到剪贴板")
                except Exception as e:
                    print(f"⚠ 无法复制到剪贴板: {e}")
                    
            else:
                print("计算CRC32值失败，请检查文件路径是否正确")
                
        except KeyboardInterrupt:
            print("\n\n程序被用户中断")
            break
        except Exception as e:
            print(f"发生未知错误: {e}")

if __name__ == "__main__":
    # 检查是否安装了pyperclip
    try:
        import pyperclip
    except ImportError:
        print("错误：需要安装pyperclip库")
        print("请运行: pip install pyperclip")
        sys.exit(1)
        
    # 检查RHash是否存在
    rhash_path = r"d:\ProApps\RHash\rhash.exe"
    if not os.path.exists(rhash_path):
        print(f"警告：未找到RHash程序，请确认路径是否正确: {rhash_path}")
        print("请修改脚本中的rhash_path变量为正确的RHash路径")
        
    main()