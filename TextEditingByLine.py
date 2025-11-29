# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始，提示我处理方案。如果我输入的是回车。则对剪贴板内的文本进行格式化处理，重新写入剪贴板；如果我输入的是一段文字（以 Crtl＋回车代替回车换行，以回车结束），则对这一段文字进行格式化处理，重新写入剪贴板；如果我输入的是某一文件的路径（要求真实存在），则对该文件内的文本进行格式化处理。
# 依次处理每一行。
# 1. 单元移动：单元为方括号“[]”包绕到字符（包括[]）。先询问我第几个单元。再询问我是向前移动、向后移动、移到最前、移到最后。向前移动、向后移动需要问我移动几个单位（不是字符，而是方括号“[]”包绕到字符）。
# 2. 单元删除：单元为方括号“[]”包绕到字符（包括[]）。先询问我第几个单元，将该单元删除。
# 3. 复制删除：单元为方括号“[]”包绕到字符（包括[]）。先询问我第几个单元，再询问我第几个单元后（最前为0、最后为-1）。

# 导入模块
# -*- coding: utf-8 -*-
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
    print("2. 输入文本（Ctrl+回车换行，回车结束）- 处理输入文本")
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

def extract_units(line):
    """
    从一行文本中提取所有方括号单元
    返回单元列表和单元在原文中的位置信息
    """
    units = []
    positions = []
    
    # 使用正则表达式匹配所有方括号包绕的内容
    pattern = r'(\[.*?\])'
    matches = list(re.finditer(pattern, line))
    
    for match in matches:
        units.append(match.group(1))
        positions.append((match.start(), match.end()))
    
    return units, positions

def reconstruct_line(original_line, units, positions):
    """
    根据移动后的单元重新构建行文本
    """
    if not units:
        return original_line
    
    # 将原始行拆分为单元和非单元部分
    result_parts = []
    last_end = 0
    
    for i, (start, end) in enumerate(positions):
        # 添加单元前的非单元文本
        if start > last_end:
            result_parts.append(original_line[last_end:start])
        
        # 添加当前单元
        result_parts.append(units[i])
        last_end = end
    
    # 添加最后一个单元后的文本
    if last_end < len(original_line):
        result_parts.append(original_line[last_end:])
    
    return ''.join(result_parts)

def move_unit(units, unit_index, move_type, move_count=0):
    """
    移动指定单元
    """
    if unit_index < 0 or unit_index >= len(units):
        return units
    
    unit_to_move = units[unit_index]
    new_units = units.copy()
    
    if move_type == "向前移动":
        # 向前移动指定单位数
        new_position = max(0, unit_index - move_count)
        new_units.pop(unit_index)
        new_units.insert(new_position, unit_to_move)
    
    elif move_type == "向后移动":
        # 向后移动指定单位数
        new_position = min(len(new_units) - 1, unit_index + move_count)
        new_units.pop(unit_index)
        new_units.insert(new_position, unit_to_move)
    
    elif move_type == "移到最前":
        # 移到最前面
        new_units.pop(unit_index)
        new_units.insert(0, unit_to_move)
    
    elif move_type == "移到最后":
        # 移到最后面
        new_units.pop(unit_index)
        new_units.append(unit_to_move)
    
    return new_units

def delete_unit(units, unit_index):
    """
    删除指定单元
    """
    if unit_index < 0 or unit_index >= len(units):
        return units
    
    new_units = units.copy()
    new_units.pop(unit_index)
    return new_units

def copy_unit(units, source_index, target_position):
    """
    复制指定单元到目标位置
    """
    if source_index < 0 or source_index >= len(units):
        return units
    
    unit_to_copy = units[source_index]
    new_units = units.copy()
    
    # 计算目标位置
    if target_position == 0:  # 最前
        new_units.insert(0, unit_to_copy)
    elif target_position == -1:  # 最后
        new_units.append(unit_to_copy)
    else:  # 指定位置之后
        # 将target_position转换为索引（用户输入的是从1开始的序号）
        target_index = target_position
        if target_index >= len(new_units):
            new_units.append(unit_to_copy)
        else:
            new_units.insert(target_index + 1, unit_to_copy)
    
    return new_units

def get_operation_parameters():
    """
    获取用户的操作参数
    """
    # 询问操作类型
    print("\n请选择操作类型:")
    print("1. 单元移动")
    print("2. 单元删除")
    print("3. 单元复制")
    
    while True:
        operation_choice = input("请选择操作类型 (1-3): ").strip()
        if operation_choice in ["1", "2", "3"]:
            break
        else:
            print("请输入 1-3 之间的数字")
    
    # 询问要操作第几个单元
    while True:
        try:
            unit_num = input("请选择要操作的第几个单元 (输入0跳过): ").strip()
            if unit_num == "0":
                return None, None, None, None
            
            unit_index = int(unit_num) - 1
            if unit_index >= 0:
                break
            else:
                print("请输入有效数字")
        except ValueError:
            print("请输入有效数字")
    
    if operation_choice == "1":  # 单元移动
        # 询问移动类型
        print("\n移动选项:")
        print("1. 向前移动")
        print("2. 向后移动") 
        print("3. 移到最前")
        print("4. 移到最后")
        
        move_options = {
            "1": "向前移动",
            "2": "向后移动", 
            "3": "移到最前",
            "4": "移到最后"
        }
        
        while True:
            move_choice = input("请选择移动类型 (1-4): ").strip()
            if move_choice in move_options:
                move_type = move_options[move_choice]
                break
            else:
                print("请输入 1-4 之间的数字")
        
        move_count = 0
        if move_type in ["向前移动", "向后移动"]:
            # 询问移动单位数
            while True:
                try:
                    move_count = int(input("请输入移动几个单位: "))
                    if move_count > 0:
                        break
                    else:
                        print("请输入正整数")
                except ValueError:
                    print("请输入有效数字")
        
        return "移动", unit_index, move_type, move_count
    
    elif operation_choice == "2":  # 单元删除
        return "删除", unit_index, None, None
    
    elif operation_choice == "3":  # 单元复制
        print("\n复制选项:")
        print("0. 最前")
        print("-1. 最后")
        print("或输入其他数字表示在第几个单元之后")
        
        while True:
            try:
                target_pos = input("请选择复制到哪个位置: ").strip()
                target_position = int(target_pos)
                break
            except ValueError:
                print("请输入有效数字")
        
        return "复制", unit_index, target_position, None

def process_text(text):
    """
    处理文本的每一行
    """
    if not text:
        return text
    
    lines = text.split('\n')
    processed_lines = []
    
    # 先显示所有行的单元情况
    print("\n=== 文本分析结果 ===")
    all_units = []
    for line_num, line in enumerate(lines, 1):
        units, _ = extract_units(line)
        all_units.append(units)
        print(f"第 {line_num} 行: 找到 {len(units)} 个单元 - {line}")
    
    # 获取操作参数（只询问一次）
    operation_type, unit_index, param1, param2 = get_operation_parameters()
    
    if operation_type is None:
        print("跳过操作，返回原始文本")
        return text
    
    # 对所有行执行相同的操作
    print("\n=== 开始处理所有行 ===")
    for line_num, line in enumerate(lines, 1):
        units, positions = extract_units(line)
        
        if not units:
            print(f"第 {line_num} 行: 未找到方括号单元，跳过")
            processed_lines.append(line)
            continue
        
        # 检查单元索引是否有效
        if unit_index >= len(units):
            print(f"第 {line_num} 行: 单元索引超出范围 (只有 {len(units)} 个单元)，跳过")
            processed_lines.append(line)
            continue
        
        # 执行操作
        if operation_type == "移动":
            new_units = move_unit(units, unit_index, param1, param2)
        elif operation_type == "删除":
            new_units = delete_unit(units, unit_index)
        elif operation_type == "复制":
            new_units = copy_unit(units, unit_index, param1)
        
        # 重新构建行
        new_line = reconstruct_line(line, new_units, positions)
        processed_lines.append(new_line)
        
        print(f"第 {line_num} 行: 处理完成")
        print(f"  原始: {line}")
        print(f"  结果: {new_line}")
    
    return '\n'.join(processed_lines)

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
    processed_text = process_text(text)
    
    if processed_text and processed_text != text:
        # 将结果写入剪贴板
        try:
            pyperclip.copy(processed_text)
            print(f"\n处理完成！结果已写入剪贴板")
            print("处理后的文本预览:")
            print("-" * 40)
            print(processed_text)
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
        sys.exit(1)
    
    main()