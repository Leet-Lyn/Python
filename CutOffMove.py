# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问原文件位置与目标文件夹（默认为“z:\\”）位置。
# 尝试将原文件向目标文件夹移动。
# 如果无法移动，则重命名原文件（从后删除1个字符（不包括扩展名）），再次尝试将原文件向目标文件夹移动。
# 反复循环，直至能将原文件向目标文件夹移动。
# 将生成的文件名，写入剪贴板。
# 最后询问我是否继续，默认（“y”，或回车），返回开头，询问原文件位置与目标文件夹（默认为“z:\\”）位置。按“n”，择退出。

# 导入模块
import os
import shutil
import pyperclip

# 定义主函数
def main():
    while True:
        # 获取用户输入的原文件路径和目标文件夹
        original_file = input("请输入原文件的完整路径：").strip()
        if not os.path.isfile(original_file):
            print("输入的原文件路径无效，请重新输入。")
            continue

        target_folder = input("请输入目标文件夹位置（默认为z:\\）：").strip() or "z:\\"

        # 确保目标文件夹存在
        if not os.path.exists(target_folder):
            try:
                os.makedirs(target_folder)
                print(f"目标文件夹已创建：{target_folder}")
            except Exception as e:
                print(f"创建目标文件夹失败：{e}")
                continue

        # 分离文件名和扩展名
        filename, file_extension = os.path.splitext(os.path.basename(original_file))

        # 移动文件的核心逻辑
        target_file = try_move_file(original_file, target_folder, filename, file_extension)

        if target_file:
            # 将最终的目标文件路径写入剪贴板
            pyperclip.copy(target_file)
            print(f"文件已成功移动至：{target_file}")
            print(f"文件路径已复制到剪贴板：{target_file}")
        else:
            print("文件名已无法缩短，操作失败。")
            break

        # 询问是否继续
        # continue_choice = input("是否继续操作？（y/回车继续，n 退出）：").strip().lower()
        # if continue_choice == 'n':
        #     print("程序结束。")
        #     break


# 尝试移动文件的函数
def try_move_file(original_file, target_folder, filename, file_extension):
    while True:
        try:
            # 构建目标文件路径
            target_file = os.path.join(target_folder, f"{filename}{file_extension}")
            
            # 尝试移动文件
            shutil.move(original_file, target_file)
            return target_file  # 成功时返回目标文件路径
        
        except Exception as e:
            print(f"文件移动失败：{e}")

            # 判断是否需要缩短文件名
            if len(filename) > 1:
                # 从文件名末尾删除一个字符
                filename = filename[:-1]
                new_original_file = os.path.join(os.path.dirname(original_file), f"{filename}{file_extension}")

                try:
                    # 重命名原文件
                    os.rename(original_file, new_original_file)
                    original_file = new_original_file  # 更新原文件路径
                    print(f"文件已重命名为：{original_file}")
                except Exception as rename_error:
                    print(f"文件重命名失败：{rename_error}")
                    return None
            else:
                # 文件名无法再缩短
                print("文件名已无法缩短，无法移动文件。")
                return None


# 程序入口
if __name__ == "__main__":
    main()

# 按回车键退出
input("按回车键退出程序...")