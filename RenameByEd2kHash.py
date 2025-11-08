# 请帮我写个中文的 Python 脚本，批注也是中文：
# 请输入源文件夹位置（默认“d:\\Works\\Targets\\”）
# 我安装了 RHash，位置“d:\\ProApps\\RHash\\rhash.exe”。生成 ed2k 的命令类似：rhash.exe --uppercase --ed2k-link "\\TS-464C\Temps\rustdesk-1.4.3-x86_64.exe"。生成如“ed2k://|file|rustdesk-1.4.3-x86_64.exe|23369352|DF952EEB0438E288409858E6C960E261|h=T7BJKLDRQ7VDCDKOO525FO7YHJCZVKDK|/”的ed2k链接。
# 用文件名大小与 ed2k hash 对文件夹及其子文件夹下所有文件重命名。如 rustdesk-1.4.3-x86_64.exe 重命名为 [23369352][DF952EEB0438E288409858E6C960E261].exe（用方括号包绕，扩展名不变）。

# 导入模块
import os
import subprocess

def ed2k_hash(file_path):
    """
    使用 RHash 计算文件的 ED2K 哈希值。
    :param file_path: 文件路径
    :return: ED2K 哈希值字符串，失败时返回空字符串
    """
    rhash_path = "d:\\ProApps\\RHash\\rhash.exe"
    
    # 检查 RHash 是否存在
    if not os.path.isfile(rhash_path):
        print(f"错误：找不到 RHash 工具，请确保路径正确：{rhash_path}")
        return ''
    
    try:
        # 构建 RHash 命令
        cmd = [rhash_path, "--uppercase", "--ed2k-link", file_path]
        
        # 执行命令并捕获输出
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        # 从输出中提取 ED2K 哈希值
        # 输出格式：ed2k://|file|filename|filesize|HASH|...|/
        output = result.stdout.strip()
        
        # 解析 ED2K 链接提取哈希值
        parts = output.split('|')
        if len(parts) >= 5:
            ed2k_hash = parts[4]  # 哈希值在第五个位置
            return ed2k_hash
        else:
            print(f"无法解析 RHash 输出：{output}")
            return ''
            
    except subprocess.CalledProcessError as e:
        print(f"RHash 执行错误：{e}")
        return ''
    except Exception as e:
        print(f"计算文件 {file_path} 的 ED2K 哈希时出错：{e}")
        return ''

def rename_files_in_folder_recursively(source_folder):
    """
    遍历指定文件夹及其所有子文件夹中的文件，并将其重命名为 ED2K 哈希格式。
    :param source_folder: 源文件夹路径
    """
    if not os.path.isdir(source_folder):
        print("指定的路径无效，请确保它是一个文件夹。")
        return

    for root, _, files in os.walk(source_folder):
        for file in files:
            file_path = os.path.join(root, file)

            # 检查是否为文件
            if not os.path.isfile(file_path):
                print(f"跳过非文件项：{file_path}")
                continue

            file_size = os.path.getsize(file_path)
            if file_size == 0:
                print(f"{file} 是空文件，已跳过。")
                continue

            # 计算文件哈希
            file_hash = ed2k_hash(file_path)
            if not file_hash:
                print(f"无法计算文件 {file} 的 ED2K 哈希，已跳过。")
                continue

            # 生成新的文件名
            file_ext = os.path.splitext(file)[1].lower()
            new_file_name = f"[{file_size}][{file_hash}]{file_ext}"
            new_file_path = os.path.join(root, new_file_name)

            # 检查新文件名是否已存在
            if os.path.exists(new_file_path):
                print(f"目标文件已存在，跳过重命名：{new_file_name}")
                continue

            try:
                os.rename(file_path, new_file_path)
                print(f"成功重命名：{file} -> {new_file_name}")
            except Exception as e:
                print(f"无法重命名文件 {file_path}：{e}")

def main():
    """
    主程序入口，处理用户输入并执行文件重命名操作。
    """
    # 获取源文件夹路径
    source_folder = input("请输入源文件夹位置（按回车键使用默认地址：d:\\Works\\Targets\\）：").strip() or "d:\\Works\\Targets\\"

    # 调用重命名函数
    rename_files_in_folder_recursively(source_folder)

    # 退出提示
    input("操作完成，按回车键退出...")

if __name__ == "__main__":
    main()