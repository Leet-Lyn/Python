# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件夹位置（默认地址“d:\Works\Benchs\”）与目标文件夹位置（默认地址“d:\Works\Finisheds\”）。
# 遍历源文件夹内所有子文件夹中的文件（剔除隐藏文件）。
# 用 Leanify 进行压缩，生成的文件放到到目标文件夹中以“源文件夹的子文件夹”中，保持文件夹及子文件结构。

# 导入模块
import subprocess
import os
import shutil

def is_hidden_file(file_path):
    """
    判断文件是否为隐藏文件
    """
    # 方法1：检查文件名是否以点开头（Unix/Linux系统）
    if os.path.basename(file_path).startswith('.'):
        return True
    
    # 方法2：检查文件属性（Windows系统）
    try:
        import win32file
        import win32con
        attributes = win32file.GetFileAttributes(file_path)
        return attributes & (win32con.FILE_ATTRIBUTE_HIDDEN | win32con.FILE_ATTRIBUTE_SYSTEM)
    except:
        # 如果无法使用win32api，尝试使用其他方法
        try:
            return os.stat(file_path).st_file_attributes & 0x2  # 隐藏属性
        except:
            # 最后回退到检查文件名
            return os.path.basename(file_path).startswith('.')

def compress_files_with_leanify():
    """
    使用 Leanify 压缩源文件夹中的所有文件，并将结果保存到目标文件夹中，保留源文件夹的子文件夹结构。
    """
    # 提示用户输入源文件夹和目标文件夹位置
    input_path = input("请输入源文件夹位置（按回车键使用默认地址：“d:\\Works\\Benchs\\”）：").strip() or "d:\\Works\\Benchs\\"
    output_path = input("请输入目标文件夹位置（按回车键使用默认地址：“d:\\Works\\Finisheds\\”）：").strip() or "d:\\Works\\Finisheds\\"

    # 验证输入路径
    if not os.path.isdir(input_path):
        print(f"源文件夹路径无效：{input_path}")
        return
    
    # 确保目标文件夹存在
    os.makedirs(output_path, exist_ok=True)
    
    # 统计变量
    total_files = 0
    processed_files = 0
    skipped_hidden_files = 0
    failed_files = 0

    # 遍历源文件夹内的所有子文件夹和文件
    for root, dirs, files in os.walk(input_path):
        # 剔除隐藏文件夹
        dirs[:] = [d for d in dirs if not is_hidden_file(os.path.join(root, d))]
        
        for file in files:
            file_path = os.path.join(root, file)
            
            # 跳过隐藏文件
            if is_hidden_file(file_path):
                skipped_hidden_files += 1
                continue
            
            total_files += 1
            
            # 生成目标文件夹中的对应路径
            relative_path = os.path.relpath(root, input_path)
            target_dir = os.path.join(output_path, relative_path)
            os.makedirs(target_dir, exist_ok=True)

            # 构造目标文件路径
            target_file_path = os.path.join(target_dir, file)

            try:
                # 调用 Leanify 对文件进行压缩
                result = subprocess.run(
                    ["d:\\ProApps\\Leanify\\Leanify.exe", file_path],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )

                if result.returncode == 0:
                    # 压缩成功，将文件移动到目标文件夹
                    shutil.move(file_path, target_file_path)
                    print(f"成功压缩并移动：{file_path} -> {target_file_path}")
                    processed_files += 1
                else:
                    # 压缩失败，打印错误信息
                    print(f"文件 {file_path} 压缩失败，错误代码：{result.returncode}")
                    failed_files += 1
            except Exception as e:
                print(f"处理文件 {file_path} 时发生错误：{e}")
                failed_files += 1

    # 输出处理统计
    print("\n文件处理完成！")
    print(f"总文件数: {total_files}")
    print(f"成功处理: {processed_files}")
    print(f"跳过隐藏文件: {skipped_hidden_files}")
    print(f"处理失败: {failed_files}")

if __name__ == "__main__":
    compress_files_with_leanify()
    input("操作完成，按回车键退出...")