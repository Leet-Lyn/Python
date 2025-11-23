# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件夹位置（默认地址：d:\\Works\\Downloads\\）与目标文件位置（默认地址：d:\Works\0\Ed2kList.txt）。
# 遍历源文件夹内所有子文件夹中的文件。计算并生成改文件的Ed2K链接。
# 我安装了 RHash，位置“d:\\ProApps\\RHash\\rhash.exe”。生成 ed2k 的命令类似：rhash.exe --uppercase --ed2k-link "\\TS-464C\Temps\rustdesk-1.4.3-x86_64.exe"。生成如“ed2k://|file|rustdesk-1.4.3-x86_64.exe|23369352|DF952EEB0438E288409858E6C960E261|h=T7BJKLDRQ7VDCDKOO525FO7YHJCZVKDK|/”的ed2k链接。
# 先清空目标文件位置，然后将生成的 ed2k链接，依次写入目标文件位置，一行一个 ed2k 链接。

# 导入模块
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
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

def process_directory(source_dir, target_file):
    """
    遍历源文件夹并生成所有文件的ed2k链接
    
    参数:
        source_dir: 源文件夹路径
        target_file: 目标文件路径
    """
    try:
        # 清空目标文件
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write('')
        print(f"已清空目标文件: {target_file}")
        
        # 计数器
        total_files = 0
        processed_files = 0
        success_files = 0
        
        # 首先统计文件总数
        print("正在扫描文件...")
        for root, dirs, files in os.walk(source_dir):
            total_files += len(files)
        
        print(f"找到 {total_files} 个文件，开始生成ed2k链接...")
        
        # 遍历所有文件
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                processed_files += 1
                file_path = os.path.join(root, file)
                
                # 显示进度
                print(f"[{processed_files}/{total_files}] 处理: {file}")
                
                # 生成ed2k链接
                ed2k_link = get_ed2k_link(file_path)
                
                if ed2k_link:
                    # 写入目标文件
                    with open(target_file, 'a', encoding='utf-8') as f:
                        f.write(ed2k_link + '\n')
                    success_files += 1
                    print(f"  ✓ 成功生成链接")
                else:
                    print(f"  ✗ 生成链接失败")
        
        # 显示统计信息
        print(f"处理完成!")
        print(f"总文件数: {total_files}")
        print(f"成功生成: {success_files}")
        print(f"失败: {total_files - success_files}")
        print(f"ed2k链接已保存到: {target_file}")
        
    except Exception as e:
        print(f"处理文件夹时发生错误: {e}")

def main():
    """
    主函数：获取用户输入并处理文件夹
    """
    
    try:
        # 询问源文件夹位置
        default_source = r"d:\Works\Downloads\"
        source_dir = input(f"请输入源文件夹位置 [默认: {default_source}]: ").strip()
        if not source_dir:
            source_dir = default_source
        
        # 移除路径两端的引号（如果有的话）
        source_dir = source_dir.strip('"\'')
        
        # 检查源文件夹是否存在
        if not os.path.exists(source_dir):
            print(f"错误：源文件夹 '{source_dir}' 不存在")
            return
        
        # 询问目标文件位置
        default_target = r"d:\Works\0\Ed2kList.txt"
        target_file = input(f"请输入目标文件位置 [默认: {default_target}]: ").strip()
        if not target_file:
            target_file = default_target
        
        # 移除路径两端的引号（如果有的话）
        target_file = target_file.strip('"\'')
        
        # 确保目标文件的目录存在
        target_dir = os.path.dirname(target_file)
        if not os.path.exists(target_dir):
            print(f"创建目标目录: {target_dir}")
            os.makedirs(target_dir, exist_ok=True)
        
        # 确认信息
        print("确认信息:")
        print(f"源文件夹: {source_dir}")
        print(f"目标文件: {target_file}")
        
        confirm = input("是否开始处理? (y/n): ").strip().lower()
        if confirm not in ['y', 'yes', '是']:
            print("已取消操作")
            return
        
        # 开始处理
        process_directory(source_dir, target_file)
        
    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
    except Exception as e:
        print(f"发生未知错误: {e}")

if __name__ == "__main__":
    # 检查RHash是否存在
    rhash_path = r"d:\ProApps\RHash\rhash.exe"
    if not os.path.exists(rhash_path):
        print(f"错误：未找到RHash程序")
        print(f"请确认RHash路径是否正确: {rhash_path}")
        print("如果需要修改路径，请编辑脚本中的 rhash_path 变量")
        sys.exit(1)
        
    main()