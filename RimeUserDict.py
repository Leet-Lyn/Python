# 请帮我写个中文的 Python 脚本，批注也是中文：
# 将当前剪贴板内的词组，存入变量 1 中。然后将其变量 1 中的汉语词组解析为汉语拼音，每个字用空格隔开；如词组间有英文字母，则该位置保留英文字母，英文字母和汉语拼音间用空格隔开。存入变量 2。
# 将变量 1 与变量 2 用 utf-8 写入“d:\\ProApps\\Rime\\config\\dicts\\user.dict.yaml”，用 tab 隔开，再添加数字（默认为10），也用 tab 隔开。添加为末尾新的行。

# 需安装第三方库，运行前请执行以下命令：
# pip install pyperclip pypinyin

# 导入模块
"""
功能：将剪贴板中的中文词组转换为带符号声调的拼音，并添加到Rime用户词典
用法：运行脚本前请确保已安装所需库：pip install pyperclip pypinyin
"""
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

def convert_to_tone_pinyin(text):
    """将中文字符串转换为带符号声调的拼音"""
    # 使用Style.TONE获取带符号声调的拼音
    pinyin_list = lazy_pinyin(text, style=Style.TONE)
    return pinyin_list

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
        if block and is_chinese(block[0]):
            # 中文转带符号声调的拼音
            pinyin_list = convert_to_tone_pinyin(block)
            pinyin_blocks.append(' '.join(pinyin_list))
        else:
            # 英文保留原样
            pinyin_blocks.append(block)
    
    # 拼接最终拼音结果
    pinyin_result = ' '.join(pinyin_blocks)

    # 构建写入内容
    output_line = f"{clipboard_content}\t{pinyin_result}\t10\n"
    
    # 写入文件
    file_path = r'd:\ProApps\Rime\config\dicts\user.dict.yaml'
    try:
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(output_line)
        print(f"成功添加到词典：")
        print(f"  词组：{clipboard_content}")
        print(f"  拼音：{pinyin_result}")
        print(f"  已写入：{file_path}")
    except FileNotFoundError:
        print(f"错误：文件路径不存在，请检查路径：{file_path}")
        print("请确保目录存在：d:\\ProApps\\Rime\\config\\dicts\\")
    except Exception as e:
        print(f"写入文件时出错：{str(e)}")

    print("\n处理完成！")
    input("按回车键退出...")

# 示例测试函数
def test_pinyin_conversion():
    """测试拼音转换功能"""
    test_cases = [
        "你好世界",
        "hello世界",
        "拼音pinyin",
        "测试声调",
        "中国",
        "北京欢迎你",
        "a测试b",
    ]
    
    print("拼音转换测试（带符号声调）：")
    print("-" * 50)
    
    for test in test_cases:
        text_blocks = split_mixed_text(test)
        pinyin_blocks = []
        
        for block in text_blocks:
            if block and is_chinese(block[0]):
                pinyin_list = lazy_pinyin(block, style=Style.TONE)
                pinyin_blocks.append(' '.join(pinyin_list))
            else:
                pinyin_blocks.append(block)
        
        result = ' '.join(pinyin_blocks)
        print(f"原文：{test}")
        print(f"拼音：{result}")
        
        # 显示每个字符的拼音详细信息
        if any(is_chinese(char) for char in test):
            print("详细转换：")
            for char in test:
                if is_chinese(char):
                    pinyin = lazy_pinyin(char, style=Style.TONE)[0]
                    print(f"  '{char}' -> {pinyin}")
        print("-" * 50)

if __name__ == "__main__":
    # 运行测试函数查看拼音转换效果
    # test_pinyin_conversion()
    
    # 如果需要实际运行主程序，取消下面一行的注释
    main()