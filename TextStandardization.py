# 请帮我写个中文的 Python 脚本，批注也是中文：
# 对文本格式进行格式化处理。
# 再脚本开始，提示我处理方案。如果我输入的是回车。则对剪贴板内的文本进行格式化处理，重新写入剪贴板；如果我输入的是一段文字（允许回车，以 Crtl＋回车结束），则对这一段文字进行格式化处理，重新写入剪贴板；如果我输入的是某一文件的路径（要求真实存在），则对该文件内的文本进行格式化处理。
# 格式化要求：
# 1. 繁体汉字转简体汉字。
# 2. 汉字、英文单词、数字，彼此之间有空格。
# 3. 汉字后标点符号转换为全角符号，英文后标点符号转换为半角符号。

# 导入模块
import os
import re
import pyperclip  # 用于剪贴板操作
from opencc import OpenCC  # 用于简繁转换

# 初始化 OpenCC 转换器（简体到繁体）
cc = OpenCC('t2s')  

def format_text(text):
    """
    对文本进行格式化处理。
    :param text: 原始文本。
    :return: 格式化后的文本。
    """
    # 简体转繁体
    text = cc.convert(text)
    
    # 汉字与英文单词、数字之间加空格
    text = re.sub(r'([\u4e00-\u9fa5])([a-zA-Z0-9])', r'\1 \2', text)  # 汉字后加空格
    text = re.sub(r'([a-zA-Z0-9])([\u4e00-\u9fa5])', r'\1 \2', text)  # 英文或数字后加空格

    # 替换标点符号
    text = re.sub(r'([\u4e00-\u9fa5])([,.!?])', lambda m: f"{m.group(1)}{to_fullwidth(m.group(2))}", text)  # 汉字后标点转全角
    text = re.sub(r'([a-zA-Z0-9])([，。！？])', lambda m: f"{m.group(1)}{to_halfwidth(m.group(2))}", text)  # 英文后标点转半角

    return text

def to_fullwidth(char):
    """
    将半角标点符号转换为全角标点符号。
    :param char: 半角标点符号。
    :return: 全角标点符号。
    """
    mapping = {',': '，', '.': '。', '!': '！', '?': '？'}
    return mapping.get(char, char)

def to_halfwidth(char):
    """
    将全角标点符号转换为半角标点符号。
    :param char: 全角标点符号。
    :return: 半角标点符号。
    """
    mapping = {'，': ',', '。': '.', '！': '!', '？': '?'}
    return mapping.get(char, char)

def process_clipboard():
    """
    处理剪贴板内的文本。
    """
    text = pyperclip.paste()
    if not text.strip():
        print("剪贴板内无内容，请重新复制后重试。")
        return
    formatted_text = format_text(text)
    pyperclip.copy(formatted_text)
    print("剪贴板内的文本已格式化处理并重新写入剪贴板。")

def process_manual_input():
    """
    处理用户手动输入的文本。
    """
    print("请输入需要格式化的文本（输入 Ctrl+回车结束）：")
    text = []
    while True:
        try:
            line = input()
            text.append(line)
        except EOFError:  # 捕获 Ctrl+回车
            break
    text = "\n".join(text)
    if not text.strip():
        print("输入的文本为空，操作终止。")
        return
    formatted_text = format_text(text)
    pyperclip.copy(formatted_text)
    print("输入的文本已格式化处理并写入剪贴板。")

def process_file(file_path):
    """
    处理指定文件的文本。
    :param file_path: 文件路径。
    """
    if not os.path.isfile(file_path):
        print(f"文件路径 {file_path} 不存在或不是一个文件。")
        return
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    formatted_text = format_text(text)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(formatted_text)
    print(f"文件 {file_path} 的文本已格式化处理并覆盖写回。")

def main():
    """
    主函数：根据用户选择执行对应的操作。
    """
    print("请选择处理方式：")
    print("1. 直接按回车处理剪贴板内的文本")
    print("2. 输入一段文字（支持多行，Ctrl+回车结束）")
    print("3. 输入一个文件路径（要求真实存在）")
    
    choice = input("请输入选择（默认：处理剪贴板）：").strip()

    if not choice:  # 默认处理剪贴板
        process_clipboard()
    elif os.path.isfile(choice):  # 输入文件路径
        process_file(choice)
    else:  # 输入文本
        print("检测到输入内容为手动文本...")
        process_manual_input()

if __name__ == "__main__":
    main()