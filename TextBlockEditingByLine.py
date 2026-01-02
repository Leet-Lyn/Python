# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始，提示我处理方案。如果我输入的是回车。则对剪贴板内的文本进行格式化处理，重新写入剪贴板；如果我输入的是一段文字（以 Crtl＋回车代替回车换行，以回车结束），则对这一段文字进行格式化处理，重新写入剪贴板；如果我输入的是某一文件的路径（要求真实存在），则对该文件内的文本进行格式化处理。
# 依次处理每一行。
# 1. 单元移动：单元为方括号“[]”包绕到字符（包括[]）。先询问我第几个单元。再询问我是向前移动、向后移动、移到最前、移到最后。向前移动、向后移动需要问我移动几个单位（不是字符，而是方括号“[]”包绕到字符）。
# 2. 单元删除：单元为方括号“[]”包绕到字符（包括[]）。先询问我第几个单元，将该单元删除。
# 3. 单元复制：单元为方括号“[]”包绕到字符（包括[]）。先询问我第几个单元，再询问我第几个单元后（最前为0、最后为-1），将改单元复制。
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


def extract_units(line):
    """提取一行中的 [] 单元"""
    return re.findall(r"\[.*?\]", line)


# ========= ⭐ 核心修复函数（允许单元数量变化） ⭐ =========
def reconstruct_line_from_units(original_line, new_units):
    """
    根据新的单元列表重建行
    支持：删除 / 复制 / 移动（单元数量变化）
    """
    pattern = r"(\[.*?\])"
    parts = re.split(pattern, original_line)

    result = []
    unit_idx = 0

    for part in parts:
        if re.fullmatch(pattern, part):
            if unit_idx < len(new_units):
                result.append(new_units[unit_idx])
                unit_idx += 1
            else:
                # 原本存在单元，但现在被删除 → 跳过
                pass
        else:
            result.append(part)

    return "".join(result)


def move_unit(units, index, move_type, count=0):
    units = units.copy()
    unit = units.pop(index)

    if move_type == "向前移动":
        units.insert(max(0, index - count), unit)
    elif move_type == "向后移动":
        units.insert(min(len(units), index + count), unit)
    elif move_type == "移到最前":
        units.insert(0, unit)
    elif move_type == "移到最后":
        units.append(unit)

    return units


def delete_unit(units, index):
    units = units.copy()
    units.pop(index)
    return units


def copy_unit(units, index, target):
    units = units.copy()
    unit = units[index]

    if target == 0:
        units.insert(0, unit)
    elif target == -1:
        units.append(unit)
    else:
        units.insert(target + 1, unit)

    return units


def get_operation_parameters():
    print("\n请选择操作类型:")
    print("1. 单元移动")
    print("2. 单元删除")
    print("3. 单元复制")
    print("0. 退出程序")

    choice = input("请选择 (1-3, 0退出): ").strip()

    if choice == "0":
        return "退出", None, None, None

    # 获取单元索引（从1开始）
    index = int(input("第几个单元（从 1 开始）: ")) - 1

    if choice == "1":
        print("1 向前  2 向后  3 最前  4 最后")
        m = input("选择: ")
        move_map = {"1": "向前移动", "2": "向后移动", "3": "移到最前", "4": "移到最后"}
        move_type = move_map[m]
        count = 0
        if move_type in ("向前移动", "向后移动"):
            count = int(input("移动几个单位: "))
        return "移动", index, move_type, count

    if choice == "2":
        return "删除", index, None, None

    if choice == "3":
        target = int(input("复制到位置（0=最前，-1=最后）: "))
        return "复制", index, target, None

    return None, None, None, None


def process_text(text):
    lines = text.split("\n")
    op, p1, p2, p3 = get_operation_parameters()

    # 处理退出操作
    if op == "退出":
        return None, "退出"

    # 处理单元操作
    new_lines = []
    for line in lines:
        units = extract_units(line)
        if not units or p1 >= len(units):
            new_lines.append(line)
            continue

        if op == "移动":
            units = move_unit(units, p1, p2, p3)
        elif op == "删除":
            units = delete_unit(units, p1)
        elif op == "复制":
            units = copy_unit(units, p1, p2)

        new_lines.append(reconstruct_line_from_units(line, units))

    return "\n".join(new_lines), None


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