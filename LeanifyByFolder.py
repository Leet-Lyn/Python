# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件夹位置与目标文件夹位置。
# 遍历源文件夹内所有子文件夹中的图片或文件。
# 用 Leanify 进行压缩，生成的 文件放到到目标文件夹中以“源文件夹的子文件夹”中，保持文件夹及子文件结构。

# 导入模块
import subprocess
import os
import shutil

def compress_files_with_leanify():
    """
    使用 Leanify 压缩源文件夹中的所有文件，并将结果保存到目标文件夹中，保留源文件夹的子文件夹结构。
    """
    # 提示用户输入源文件夹和目标文件夹位置
    input_path = input("请输入源文件夹位置（按回车键使用默认地址：d:\\Works\\Webpages\\）：").strip() or "d:\\Works\\Webpages\\"
    output_path = input("请输入目标文件夹位置（按回车键使用默认地址：e:\\Documents\\Literatures\\Webpages\\）：").strip() or "e:\\Documents\\Literatures\\Webpages\\"

    # 验证输入路径
    if not os.path.isdir(input_path):
        print(f"源文件夹路径无效：{input_path}")
        return
    
    # 确保目标文件夹存在
    os.makedirs(output_path, exist_ok=True)

    # 遍历源文件夹内的所有子文件夹和文件
    for root, _, files in os.walk(input_path):
        for file in files:
            file_path = os.path.join(root, file)
            
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
                else:
                    # 压缩失败，打印错误信息
                    print(f"文件 {file_path} 压缩失败，错误代码：{result.returncode}")
            except Exception as e:
                print(f"处理文件 {file_path} 时发生错误：{e}")

    print("文件处理完成！")

if __name__ == "__main__":
    compress_files_with_leanify()
    input("操作完成，按回车键退出...")