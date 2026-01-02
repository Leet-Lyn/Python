# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始，提示我处理方案。如果我输入的是回车。则对剪贴板内的文本进行格式化处理，重新写入剪贴板；如果我输入的是一段文字（以 Crtl＋回车代替回车换行，以回车结束），则对这一段文字进行格式化处理，重新写入剪贴板；如果我输入的是某一文件的路径（要求真实存在），则对该文件内的文本进行格式化处理。
# 依次处理每一行。
# 1. 添加字符，先询问我在每一行到第几个位置后添加？再询问我添加什么字符。
# 2. 删除字符，先询问我删除什么字符。再询问是每行删除几次（删除几次后该行再出现这个字符就不删除，但每行都执行。）？
# 3. 替换字符，先询问我原来什么字符，替换为什么字符。再询问是每行替换几次（删除几次后该行再出现这个字符就不删除，但每行都执行。）？
# 0. 退出。 
# 完成后，反复循环我要做什么。

# 导入模块
import os
import re
import pyperclip
import sys


def get_user_input():
    """
    获取用户输入并判断处理方案
    """
    print("请选择处理方案：")
    print("1. 直接按回车 - 处理剪贴板内容")
    print("2. 输入文本（Ctrl+回车换行，单独回车结束）- 处理输入文本")
    print("3. 输入文件路径 - 处理文件内容")

    user_input = input("请输入: ").strip()

    if user_input == "":
        try:
            text = pyperclip.paste()
            if not text:
                print("剪贴板为空！")
                return None
            return text
        except Exception as e:
            print(f"读取剪贴板失败: {e}")
            return None

    elif os.path.exists(user_input):
        try:
            with open(user_input, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print(f"读取文件失败: {e}")
            return None

    else:
        print("请输入文本（单独回车结束）：")
        lines = []
        while True:
            try:
                line = input()
            except (EOFError, KeyboardInterrupt):
                break
            if line == "":
                break
            lines.append(line)
        return "\n".join(lines)


# ========= 字符操作函数 =========
def add_string_to_lines(lines, position, string_to_add):
    new_lines = []
    for line in lines:
        if position <= 0:
            new_lines.append(string_to_add + line)
        elif position >= len(line):
            new_lines.append(line + string_to_add)
        else:
            new_lines.append(line[:position] + string_to_add + line[position:])
    return new_lines


def delete_string_from_lines(lines, string_to_delete, times_per_line):
    new_lines = []
    for line in lines:
        new_line = line
        count = 0
        start = 0
        while count < times_per_line:
            idx = new_line.find(string_to_delete, start)
            if idx == -1:
                break
            new_line = new_line[:idx] + new_line[idx + len(string_to_delete):]
            count += 1
            start = idx
        new_lines.append(new_line)
    return new_lines


def replace_string_in_lines(lines, old, new, times_per_line):
    new_lines = []
    for line in lines:
        new_line = line
        count = 0
        start = 0
        while count < times_per_line:
            idx = new_line.find(old, start)
            if idx == -1:
                break
            new_line = new_line[:idx] + new + new_line[idx + len(old):]
            count += 1
            start = idx + len(new)
        new_lines.append(new_line)
    return new_lines


def get_operation_parameters():
    print("\n请选择操作类型:")
    print("1. 添加字符")
    print("2. 删除字符")
    print("3. 替换字符")
    print("0. 退出程序")

    choice = input("请选择 (0-3): ").strip()

    if choice == "0":
        return "退出", None, None, None

    # ---- 字符操作 ----
    if choice == "1":
        pos = int(input("在每一行第几个字符后添加（0=最前）: "))
        s = input("添加什么字符: ")
        return "添加字符", pos, s, None

    if choice == "2":
        s = input("删除什么字符: ")
        times = int(input("每行删除几次: "))
        return "删除字符", s, times, None

    if choice == "3":
        old = input("原字符: ")
        new = input("替换为: ")
        times = int(input("每行替换几次: "))
        return "替换字符", old, new, times

    return None, None, None, None


def process_text(text):
    lines = text.split("\n")
    op, p1, p2, p3 = get_operation_parameters()

    # 处理退出操作
    if op == "退出":
        return None, "退出"

    # ---- 字符操作 ----
    if op == "添加字符":
        result = "\n".join(add_string_to_lines(lines, p1, p2))
    elif op == "删除字符":
        result = "\n".join(delete_string_from_lines(lines, p1, p2))
    elif op == "替换字符":
        result = "\n".join(replace_string_in_lines(lines, p1, p2, p3))
    else:
        result = text

    return result, None


def main():
    # 获取初始文本
    text = get_user_input()
    if not text:
        print("无有效文本")
        return
    
    current_text = text
    print(f"\n初始文本内容：\n{current_text}\n")

    while True:
        print("\n" + "="*50)
        print("当前文本内容：")
        print(current_text[:200] + ("..." if len(current_text) > 200 else ""))
        print("="*50)
        
        # 处理文本
        result, status = process_text(current_text)
        
        # 检查是否退出
        if status == "退出":
            print("程序已退出")
            break
        
        if result is not None:
            # 更新当前文本
            current_text = result
            
            # 写入剪贴板
            pyperclip.copy(current_text)
            print("\n✅ 处理完成，已写入剪贴板：\n")
            print(current_text)
        else:
            print("处理失败或无变化")


if __name__ == "__main__":
    main()