# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件位置。
# 计算并生成文件的Ed2K链接。
# 我安装了 RHash，位置“d:\\ProApps\\RHash\\rhash.exe”。生成 ed2k 的命令类似：rhash.exe --uppercase --ed2k-link "\\TS-464C\Temps\rustdesk-1.4.3-x86_64.exe"。生成如“ed2k://|file|rustdesk-1.4.3-x86_64.exe|23369352|DF952EEB0438E288409858E6C960E261|h=T7BJKLDRQ7VDCDKOO525FO7YHJCZVKDK|/”的ed2k链接，显示在屏幕，并写入剪贴板。
# 如此循环，再次前询问我源文件位置。

# 导入模块
import subprocess
import pyperclip
import os
import sys

def get_ed2k_link(file_path):
    """
    使用RHash生成文件的ed2k链接
    
    参数:
        file_path: 文件路径
        
    返回:
        ed2k链接字符串，如果失败则返回None
    """
    try:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            print(f"错误：文件 '{file_path}' 不存在")
            return None
            
        # 构建RHash命令
        rhash_path = r"d:\ProApps\RHash\rhash.exe"
        command = [rhash_path, "--uppercase", "--ed2k-link", file_path]
        
        # 执行命令并获取输出
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        ed2k_link = result.stdout.strip()
        
        return ed2k_link
        
    except subprocess.CalledProcessError as e:
        print(f"RHash执行错误: {e}")
        return None
    except Exception as e:
        print(f"生成ed2k链接时发生错误: {e}")
        return None

def main():
    """
    主函数：循环询问文件路径并生成ed2k链接
    """
    print("=" * 60)
    print("ED2K链接生成工具")
    print("=" * 60)
    
    while True:
        try:
            # 询问用户输入文件路径
            print("\n" + "-" * 40)
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
                
            # 生成ed2k链接
            print(f"\n正在为文件生成ed2k链接: {file_path}")
            ed2k_link = get_ed2k_link(file_path)
            
            if ed2k_link:
                # 显示在屏幕上
                print("\n" + "=" * 40)
                print("生成的ED2K链接:")
                print("=" * 40)
                print(ed2k_link)
                print("=" * 40)
                
                # 写入剪贴板
                try:
                    pyperclip.copy(ed2k_link)
                    print("✓ ED2K链接已复制到剪贴板")
                except Exception as e:
                    print(f"⚠ 无法复制到剪贴板: {e}")
                    
            else:
                print("生成ed2k链接失败，请检查文件路径是否正确")
                
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