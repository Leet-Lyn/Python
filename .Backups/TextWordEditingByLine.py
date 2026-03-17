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


# ========= 字符操作函数（支持负数参数） =========
def add_string_to_lines(lines, position, string_to_add):
    """
    在每行的指定位置后添加字符
    position: 0=最前，正数=在第n个字符后，负数=在倒数第n个字符前
    """
    new_lines = []
    for line in lines:
        if position == 0:
            new_lines.append(string_to_add + line)
        elif position > 0:
            # 正向：在第 position 个字符之后插入，即索引 position
            if position >= len(line):
                new_lines.append(line + string_to_add)
            else:
                new_lines.append(line[:position] + string_to_add + line[position:])
        else:  # position < 0
            m = -position  # 绝对值
            insert_pos = max(0, len(line) - m)  # 插入位置（0 到 len(line)）
            new_lines.append(line[:insert_pos] + string_to_add + line[insert_pos:])
    return new_lines


def delete_string_from_lines(lines, string_to_delete, times_per_line):
    """
    从每行中删除指定字符（子串）若干次
    times_per_line: 正数=正向删除，负数=逆向删除
    """
    new_lines = []
    for line in lines:
        if times_per_line >= 0:
            # 正向删除
            new_line = line
            count = 0
            start = 0
            while count < times_per_line:
                idx = new_line.find(string_to_delete, start)
                if idx == -1:
                    break
                new_line = new_line[:idx] + new_line[idx + len(string_to_delete):]
                count += 1
                start = idx  # 保持原有查找逻辑（可能存在跳跃问题，但简单场景可用）
            new_lines.append(new_line)
        else:
            # 逆向删除：反转字符串，删除子串也反转，再反转回来
            rev_line = line[::-1]
            rev_string = string_to_delete[::-1]
            rev_times = -times_per_line
            new_rev_line = rev_line
            count = 0
            start = 0
            while count < rev_times:
                idx = new_rev_line.find(rev_string, start)
                if idx == -1:
                    break
                new_rev_line = new_rev_line[:idx] + new_rev_line[idx + len(rev_string):]
                count += 1
                start = idx
            new_line = new_rev_line[::-1]
            new_lines.append(new_line)
    return new_lines


def replace_string_in_lines(lines, old, new, times_per_line):
    """
    在每行中替换指定字符（子串）若干次
    times_per_line: 正数=正向替换，负数=逆向替换
    """
    new_lines = []
    for line in lines:
        if times_per_line >= 0:
            # 正向替换
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
        else:
            # 逆向替换：反转字符串，替换子串也反转，再反转回来
            rev_line = line[::-1]
            rev_old = old[::-1]
            rev_new = new[::-1]
            rev_times = -times_per_line
            new_rev_line = rev_line
            count = 0
            start = 0
            while count < rev_times:
                idx = new_rev_line.find(rev_old, start)
                if idx == -1:
                    break
                new_rev_line = new_rev_line[:idx] + rev_new + new_rev_line[idx + len(rev_old):]
                count += 1
                start = idx + len(rev_new)
            new_line = new_rev_line[::-1]
            new_lines.append(new_line)
    return new_lines


def get_operation_parameters():
    print("\n请选择操作类型:")
    print("1. 添加字符")
    print("2. 删除字符")
    print("3. 替换字符")
    print("4. 返回主菜单（处理新文本）")
    print("0. 退出程序")

    choice = input("请选择 (0-4): ").strip()

    if choice == "0":
        return "退出", None, None, None
    if choice == "4":
        return "返回主菜单", None, None, None

    # ---- 字符操作 ----
    if choice == "1":
        try:
            pos = int(input("在每一行第几个字符后添加（0=最前，正数=正向，负数=逆向）: "))
        except ValueError:
            print("输入无效，默认最前。")
            pos = 0
        s = input("添加什么字符: ")
        return "添加字符", pos, s, None

    if choice == "2":
        s = input("删除什么字符: ")
        try:
            times = int(input("每行删除几次（正数=正向，负数=逆向）: "))
        except ValueError:
            print("输入无效，默认1次。")
            times = 1
        return "删除字符", s, times, None

    if choice == "3":
        old = input("原字符: ")
        new = input("替换为: ")
        try:
            times = int(input("每行替换几次（正数=正向，负数=逆向）: "))
        except ValueError:
            print("输入无效，默认1次。")
            times = 1
        return "替换字符", old, new, times

    return None, None, None, None


def process_text(text):
    lines = text.split("\n")
    op, p1, p2, p3 = get_operation_parameters()

    # 处理特殊状态
    if op == "退出":
        return None, "退出"
    if op == "返回主菜单":
        return None, "返回主菜单"
    if op is None:
        return None, "无效操作"

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
    while True:  # 外层循环：处理方案选择
        # 获取初始文本
        text = get_user_input()
        if text is None:
            print("无有效文本，退出程序。")
            break

        current_text = text
        print(f"\n初始文本内容：\n{current_text}\n")

        # 内层循环：字符操作
        while True:
            print("\n" + "=" * 50)
            print("当前文本内容：")
            print(current_text[:200] + ("..." if len(current_text) > 200 else ""))
            print("=" * 50)

            # 获取操作并处理
            result, status = process_text(current_text)

            if status == "退出":
                print("程序已退出")
                return  # 直接结束整个程序
            elif status == "返回主菜单":
                # 将最终文本写入剪贴板（如果存在变化）
                pyperclip.copy(current_text)
                print("\n✅ 当前文本已写入剪贴板，返回主菜单。\n")
                break  # 跳出内层循环，重新选择处理方案
            elif result is not None:
                # 正常操作，更新当前文本并写入剪贴板
                current_text = result
                pyperclip.copy(current_text)
                print("\n✅ 处理完成，已写入剪贴板：\n")
                print(current_text)
            else:
                print("处理失败或无变化")


if __name__ == "__main__":
    main()