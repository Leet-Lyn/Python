# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始，提示我处理方案。如果我输入的是回车。则对剪贴板内的文本进行格式化处理，重新写入剪贴板；如果我输入的是一段文字（以 Crtl＋回车代替回车换行，以回车结束），则对这一段文字进行格式化处理，重新写入剪贴板；如果我输入的是某一文件的路径（要求真实存在），则对该文件内的文本进行格式化处理。
# 依次处理每一行。
# 询问我日期格式为何种类型的？原形式可以为：y-m-d、d-m-y、m-d-y。
# 询问我 m 的格式是什么（m、mm、mmm、mmmm）？。可为 1 位（m 如 1~12）或 2 位（mm 如 01~12）或 3 位（mmm 如 Jan~Dec），或多位（mmmm 如 January~December）。
# 询问我 d 的格式是什么（d、dd）？。可为 1 位（d 如 1~31）或 2 位（dd 如 01~31），
# 间隔是什么？短横（-）、斜杠（/）或（\）、半角点（.）、半角逗号（,）、半角空格（ ）、半角空格逗号（ ,），或者没有间隔。
# 统一改为：yyyy-mm-dd。
# 完成后，反复循环我要做什么。

# 导入模块
import os
import pyperclip
import re
from datetime import datetime

def format_date(text, date_format_type, month_format, day_format, separator):
    """
    将日期格式化为 yyyy-mm-dd
    """
    # 定义月份映射
    month_map = {
        'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
        'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12,
        'january': 1, 'february': 2, 'march': 3, 'april': 4,
        'may': 5, 'june': 6, 'july': 7, 'august': 8,
        'september': 9, 'october': 10, 'november': 11, 'december': 12
    }
    
    # 预处理间隔符，用于正则表达式匹配
    if separator == '没有间隔':
        separator_regex = ''
    elif separator == '半角空格':
        separator_regex = r'\s+'
    elif separator == '半角空格逗号':
        separator_regex = r'\s*,\s*'
    else:
        separator_regex = re.escape(separator)
    
    # 构建正则表达式
    pattern = f'(\\d+){separator_regex}(\\d+|\\w+){separator_regex}(\\d+)'
    
    def replace_date(match):
        # 根据日期格式类型确定年、月、日的顺序
        if date_format_type == 'y-m-d':
            year, month, day = match.group(1), match.group(2), match.group(3)
        elif date_format_type == 'd-m-y':
            day, month, year = match.group(1), match.group(2), match.group(3)
        elif date_format_type == 'm-d-y':
            month, day, year = match.group(1), match.group(2), match.group(3)
        
        # 处理月份
        if month.isdigit():  # 数字月份
            month_num = int(month)
        else:  # 文本月份
            month_num = month_map.get(month.lower(), 1)
        
        # 处理年份（如果只有2位，转换为4位）
        if len(year) == 2:
            if int(year) >= 50:
                year = '19' + year
            else:
                year = '20' + year
        
        # 格式化月份为2位数字
        month_formatted = str(month_num).zfill(2)
        
        # 格式化日期为2位数字
        day_formatted = str(int(day)).zfill(2)  # 先转换为整数去掉前导零，再补零
        
        return f'{year}-{month_formatted}-{day_formatted}'
    
    # 使用正则表达式替换所有匹配的日期
    result = re.sub(pattern, replace_date, text, flags=re.IGNORECASE)
    
    return result

def get_input():
    """
    获取用户输入的文本
    """
    print("\n请选择处理方案：")
    print("1. 直接按回车：处理剪贴板内容")
    print("2. 输入一段文字（以回车结束，用Ctrl+回车换行）")
    print("3. 输入文件路径")
    
    user_input = input("请输入: ").strip()
    
    if user_input == "":  # 处理剪贴板
        try:
            text = pyperclip.paste()
            print(f"从剪贴板获取了 {len(text)} 个字符")
            return text
        except Exception as e:
            print(f"无法访问剪贴板: {e}")
            return None
    elif os.path.exists(user_input):  # 处理文件
        try:
            with open(user_input, 'r', encoding='utf-8') as f:
                text = f.read()
            print(f"从文件 '{user_input}' 读取了 {len(text)} 个字符")
            return text
        except Exception as e:
            print(f"无法读取文件: {e}")
            return None
    else:  # 处理直接输入的文本
        print("请输入文本（输入完成后按回车，如需换行请按Ctrl+回车）:")
        print("（输入完成后，按两次回车结束输入）")
        
        lines = []
        while True:
            try:
                line = input()
                if line == "":
                    break
                lines.append(line)
            except EOFError:
                break
        
        return '\n'.join(lines)

def get_date_format_option():
    """
    获取用户对日期格式的选择
    """
    print("\n请选择日期格式类型:")
    print("1. y-m-d (年-月-日)")
    print("2. d-m-y (日-月-年)")
    print("3. m-d-y (月-日-年)")
    
    while True:
        choice = input("请选择 (1/2/3): ").strip()
        if choice == '1':
            return 'y-m-d'
        elif choice == '2':
            return 'd-m-y'
        elif choice == '3':
            return 'm-d-y'
        else:
            print("无效选择，请重新输入")

def get_month_format_option():
    """
    获取用户对月份格式的选择
    """
    print("\n请选择月份格式:")
    print("1. m (如: 1, 2, 12)")
    print("2. mm (如: 01, 02, 12)")
    print("3. mmm (如: Jan, Feb, Dec)")
    print("4. mmmm (如: January, February, December)")
    
    while True:
        choice = input("请选择 (1/2/3/4): ").strip()
        if choice == '1':
            return 'm'
        elif choice == '2':
            return 'mm'
        elif choice == '3':
            return 'mmm'
        elif choice == '4':
            return 'mmmm'
        else:
            print("无效选择，请重新输入")

def get_day_format_option():
    """
    获取用户对日期格式的选择
    """
    print("\n请选择日期格式:")
    print("1. d (如: 1, 2, 31)")
    print("2. dd (如: 01, 02, 31)")
    
    while True:
        choice = input("请选择 (1/2): ").strip()
        if choice == '1':
            return 'd'
        elif choice == '2':
            return 'dd'
        else:
            print("无效选择，请重新输入")

def get_separator_option():
    """
    获取用户对间隔符的选择
    """
    print("\n请选择间隔符:")
    print("1. - (短横)")
    print("2. / (斜杠)")
    print("3. \\ (反斜杠)")  # 修复：使用双反斜杠转义
    print("4. . (半角点)")
    print("5. , (半角逗号)")
    print("6. 半角空格")
    print("7. 半角空格逗号")
    print("8. 没有间隔")
    
    separator_map = {
        '1': '-',
        '2': '/',
        '3': '\\',  # 反斜杠
        '4': '.',
        '5': ',',
        '6': '半角空格',
        '7': '半角空格逗号',
        '8': '没有间隔'
    }
    
    while True:
        choice = input("请选择 (1-8): ").strip()
        if choice in separator_map:
            return separator_map[choice]
        else:
            print("无效选择，请重新输入")

def main_loop():
    """
    主循环函数
    """
    while True:
        print("\n" + "="*50)
        print("日期格式化工具")
        print("="*50)
        
        # 获取输入文本
        original_text = get_input()
        if original_text is None or original_text == "":
            print("没有获取到文本，请重试")
            continue
        
        # 获取格式选项
        date_format_type = get_date_format_option()
        month_format = get_month_format_option()
        day_format = get_day_format_option()
        separator = get_separator_option()
        
        # 格式化文本
        print("\n正在格式化日期...")
        formatted_text = format_date(original_text, date_format_type, month_format, day_format, separator)
        
        # 输出结果到剪贴板
        try:
            pyperclip.copy(formatted_text)
            print("结果已复制到剪贴板")
            
            # 显示部分结果预览
            print("\n格式化结果预览（前500字符）:")
            print("-"*30)
            print(formatted_text[:500] + ("..." if len(formatted_text) > 500 else ""))
            print("-"*30)
        except Exception as e:
            print(f"无法写入剪贴板: {e}")
            print("格式化结果:")
            print(formatted_text)
        
        # 询问是否继续
        print("\n是否继续处理？")
        continue_choice = input("输入 'q' 退出，其他键继续: ").strip().lower()
        if continue_choice == 'q':
            print("程序结束")
            break

if __name__ == "__main__":
    # 检查必要的库
    try:
        import pyperclip
    except ImportError:
        print("需要安装 pyperclip 库，请运行: pip install pyperclip")
        exit(1)
    
    # 运行主循环
    main_loop()