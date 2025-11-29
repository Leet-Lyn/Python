# 请帮我写个中文的 Python 脚本，批注也是中文：
# 对文本格式进行格式化处理。
# 在脚本开始，提示我处理方案。如果我输入的是回车。则对剪贴板内的文本进行格式化处理，重新写入剪贴板；如果我输入的是一段文字（以 Crtl＋回车代替回车换行，以回车结束），则对这一段文字进行格式化处理，重新写入剪贴板；如果我输入的是某一文件的路径（要求真实存在），则对该文件内的文本进行格式化处理。
# 格式化要求：
# 1. 繁体汉字转简体汉字。
# 2. 汉字、英文单词、数字，彼此之间有空格。
# 3. 汉字后标点符号转换为全角符号，英文后标点符号转换为半角符号。

# 导入模块
import os
import re
import pyperclip  # 用于剪贴板操作
from opencc import OpenCC  # 用于简繁转换

# 初始化 OpenCC 转换器（繁体到简体）
cc = OpenCC('t2s')  

def format_text(text):
    """
    对文本进行格式化处理。
    :param text: 原始文本。
    :return: 格式化后的文本。
    """
    # 繁体转简体
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

def get_user_input():
    """
    获取用户输入并判断处理方案
    """
    print("请选择处理方案：")
    print("1. 直接按回车 - 处理剪贴板内容")
    print("2. 输入文本（以Ctrl+回车代替回车换行，以回车结束）- 处理输入文本")
    print("3. 输入文件路径 - 处理文件内容")
    
    user_input = input("请输入: ").strip()
    
    if user_input == "":
        # 处理剪贴板内容
        try:
            text = pyperclip.paste()
            if not text:
                print("剪贴板为空！")
                return None
            print(f"从剪贴板获取文本，共{len(text)}个字符")
            return text
        except Exception as e:
            print(f"读取剪贴板失败: {e}")
            return None
    elif os.path.exists(user_input):
        # 处理文件内容
        try:
            with open(user_input, 'r', encoding='utf-8') as f:
                text = f.read()
            print(f"从文件 '{user_input}' 读取文本，共{len(text)}个字符")
            return text
        except Exception as e:
            print(f"读取文件失败: {e}")
            return None
    else:
        # 处理直接输入的文本
        print("请输入文本（使用Ctrl+回车换行，单独回车结束）:")
        lines = []
        while True:
            try:
                line = input()
                if line == "":
                    break
                lines.append(line)
            except EOFError:
                # 捕获Ctrl+Z或Ctrl+D等结束输入信号
                break
        text = '\n'.join(lines)
        return text if text else None

def main():
    """
    主函数
    """
    print("=== 文本格式化工具 ===")
    
    # 获取输入文本
    text = get_user_input()
    if not text:
        print("未获取到有效文本，程序退出")
        return
    
    # 处理文本
    formatted_text = format_text(text)
    
    if formatted_text and formatted_text != text:
        # 将结果写入剪贴板
        try:
            pyperclip.copy(formatted_text)
            print(f"\n处理完成！结果已写入剪贴板")
            print("处理后的文本预览:")
            print("-" * 40)
            print(formatted_text)
            print("-" * 40)
        except Exception as e:
            print(f"写入剪贴板失败: {e}")
    else:
        print("文本未发生变化")

if __name__ == "__main__":
    # 检查依赖
    try:
        import pyperclip
    except ImportError:
        print("请先安装 pyperclip 模块: pip install pyperclip")
        exit(1)
    
    try:
        from opencc import OpenCC
    except ImportError:
        print("请先安装 opencc 模块: pip install opencc-python-reimplemented")
        exit(1)
    main()