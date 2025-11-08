# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件夹位置（默认“d:\\Works\\In\\”）与目标文件夹位置（默认“d:\\Works\\Out\\”）。
# 将文件夹下所有的 doc、xsl、ppt 文件转为 docx、xslx、pptx 文件。

# 导入模块
import os
import comtypes.client

def convert_files(source_folder, target_folder):
    """
    将源文件夹下的 .doc、.xls、.ppt 文件转换为 .docx、.xlsx、.pptx 格式，并保存到目标文件夹中。
    转换前将文件名中的中括号 "[" 和 "]" 替换为圆括号 "(" 和 ")"，转换后还原。
    """
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    for file_name in os.listdir(source_folder):
        full_file_path = os.path.join(source_folder, file_name)
        if not os.path.isfile(full_file_path):
            continue

        file_ext = os.path.splitext(file_name)[1].lower()
        temp_file_name = file_name.replace("[", "(").replace("]", ")")  # 替换中括号为圆括号
        temp_file_path = os.path.join(source_folder, temp_file_name)

        try:
            # 重命名为临时文件名，避免文件名中括号问题
            if full_file_path != temp_file_path:
                os.rename(full_file_path, temp_file_path)

            if file_ext == '.doc':  # 转换 Word 文档
                new_file_path = os.path.join(target_folder, temp_file_name.rsplit('.', 1)[0] + '.docx')
                word = comtypes.client.CreateObject('Word.Application')
                doc = word.Documents.Open(temp_file_path)
                doc.SaveAs(new_file_path, FileFormat=16)
                doc.Close()
                word.Quit()
                print(f"已转换文件：{file_name} 为 {os.path.basename(new_file_path)}")
            elif file_ext == '.xls':  # 转换 Excel 文档
                new_file_path = os.path.join(target_folder, temp_file_name.rsplit('.', 1)[0] + '.xlsx')
                excel = comtypes.client.CreateObject('Excel.Application')
                wb = excel.Workbooks.Open(temp_file_path)
                wb.SaveAs(new_file_path, FileFormat=51)
                wb.Close()
                excel.Quit()
                print(f"已转换文件：{file_name} 为 {os.path.basename(new_file_path)}")
            elif file_ext == '.ppt':  # 转换 PowerPoint 文档
                new_file_path = os.path.join(target_folder, temp_file_name.rsplit('.', 1)[0] + '.pptx')
                powerpoint = comtypes.client.CreateObject('Powerpoint.Application')
                ppt = powerpoint.Presentations.Open(temp_file_path, WithWindow=False)
                ppt.SaveAs(new_file_path, FileFormat=24)
                ppt.Close()
                powerpoint.Quit()
                print(f"已转换文件：{file_name} 为 {os.path.basename(new_file_path)}")
            else:
                print(f"跳过文件：{file_name}（不支持的格式）")
        except Exception as e:
            print(f"转换文件 {file_name} 时出错：{e}")
        finally:
            # 恢复原文件名
            if os.path.exists(temp_file_path) and temp_file_path != full_file_path:
                os.rename(temp_file_path, full_file_path)

def restore_original_names(target_folder):
    """
    遍历目标文件夹，将文件名中的圆括号 "(" 和 ")" 恢复为中括号 "[" 和 "]"。
    """
    for file_name in os.listdir(target_folder):
        full_file_path = os.path.join(target_folder, file_name)
        restored_file_name = file_name.replace("(", "[").replace(")", "]")
        restored_file_path = os.path.join(target_folder, restored_file_name)

        if full_file_path != restored_file_path:  # 避免重命名自己
            os.rename(full_file_path, restored_file_path)
            print(f"已还原文件名：{file_name} 为 {restored_file_name}")

def main():
    # 询问用户源文件夹路径
    source_folder = input("请输入源文件夹路径（按回车则为“d:\\Works\\In\\”）：").strip() or "d:\\Works\\In\\"
    # 询问用户目标文件夹路径
    target_folder = input("请输入目标文件夹路径（按回车则为“d:\\Works\\Out\\”）：").strip() or "d:\\Works\\Out\\"

    if not os.path.exists(source_folder):
        print(f"源文件夹 '{source_folder}' 不存在。")
        return

    print("开始文件格式转换...")
    convert_files(source_folder, target_folder)

    print("开始还原文件名...")
    restore_original_names(target_folder)

    print("操作完成！")

if __name__ == "__main__":
    main()
    input("按回车键退出...")