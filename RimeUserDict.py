# 请帮我写个中文的 Python 脚本，批注也是中文：
# 将当前剪贴板内的词组，存入变量 1 中。然后将其变量 1 中的汉语词组解析为汉语拼音，每个字用空格隔开；如词组间有英文字母，则该位置保留英文字母，英文字母和汉语拼音间用空格隔开。存入变量 2。
# 将变量 1 与变量 2 用 utf-8 写入“d:\ProApps\Rime\config\dicts\user.dict.yaml”，用 tab 隔开，再添加数字（默认为10），也用 tab 隔开。添加为末尾新的行。

# 需安装第三方库，运行前请执行以下命令：
# pip install pyperclip pypinyin

# 导入模块
import pyperclip
from pypinyin import lazy_pinyin, Style

def is_chinese(char):
    """判断字符是否为汉字"""
    return '\u4e00' <= char <= '\u9fff'

def split_mixed_text(text):
    """将中英文混合字符串分割为连续的中/英文字段"""
    blocks = []
    if not text:
        return blocks
    
    current_block = [text[0]]
    current_type = is_chinese(text[0])
    
    for char in text[1:]:
        char_type = is_chinese(char)
        if char_type == current_type:
            current_block.append(char)
        else:
            blocks.append(''.join(current_block))
            current_block = [char]
            current_type = char_type
    blocks.append(''.join(current_block))
    
    return blocks

def main():
    # 从剪贴板获取内容
    clipboard_content = pyperclip.paste().strip()
    if not clipboard_content:
        print("剪贴板内容为空！")
        return

    # 处理拼音转换
    text_blocks = split_mixed_text(clipboard_content)
    pinyin_blocks = []
    
    for block in text_blocks:
        if is_chinese(block[0]):
            # 中文转拼音，无音标格式
            pinyin = ' '.join(lazy_pinyin(block, style=Style.NORMAL))
            pinyin_blocks.append(pinyin)
        else:
            # 英文保留原样
            pinyin_blocks.append(block)
    
    # 拼接最终拼音结果
    pinyin_result = ' '.join(pinyin_blocks)

    # 构建写入内容
    output_line = f"{clipboard_content}\t{pinyin_result}\t10\n"
    
    # 写入文件（请确保路径存在）
    file_path = r'd:\ProApps\Rime\config\dicts\user.dict.yaml'
    try:
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(output_line)
        # 新增反馈信息：显示实际添加内容
        print(f"成功添加：'{clipboard_content}' → '{pinyin_result}'")
    except Exception as e:
        print(f"写入文件时出错：{str(e)}")

    print("处理完成！")
    input("按回车键退出...")

if __name__ == "__main__":
    main()
