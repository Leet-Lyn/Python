# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始，提示我处理方案。如果我输入的是回车。则对剪贴板内的文本进行格式化处理，重新写入剪贴板；如果我输入的是一段文字（以 Crtl＋回车代替回车换行，以回车结束），则对这一段文字进行格式化处理，重新写入剪贴板；如果我输入的是某一文件的路径（要求真实存在），则对该文件内的文本进行格式化处理。
# 依次处理每一行。
# 1. 单元移动：单元为方括号“[]”包绕到字符（包括[]）。先询问我第几个单元。再询问我是向前移动、向后移动、移到最前、移到最后。向前移动、向后移动需要问我移动几个单位（不是字符，而是方括号“[]”包绕到字符）。
# 2. 单元删除：单元为方括号“[]”包绕到字符（包括[]）。先询问我第几个单元，将该单元删除。
# 3. 单元复制：单元为方括号“[]”包绕到字符（包括[]）。先询问我第几个单元，再询问我第几个单元后（最前为0、最后为-1），将改单元复制。
# 4. 添加字符，先询问我在每一行到第几个位置后添加？再询问我添加什么字符。
# 5. 删除字符，先询问我删除什么字符。再询问是每行删除几次（删除几次后该行再出现这个字符就不删除，但每行都执行。）？
# 6. 替换字符，先询问我原来什么字符，替换为什么字符。再询问是每行替换几次（删除几次后该行再出现这个字符就不删除，但每行都执行。）？

# 导入所需模块
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
        print("提示：按回车键结束输入，按Ctrl+回车键换行")
        
        # 存储输入的行
        lines = []
        
        # 读取第一行
        try:
            line = input()
        except (EOFError, KeyboardInterrupt):
            return None
        
        # 如果第一行就是空行，直接返回空
        if line == "":
            return ""
        
        # 继续读取，直到遇到单独的空行
        while line != "":
            lines.append(line)
            try:
                line = input()
            except (EOFError, KeyboardInterrupt):
                # 遇到结束信号，跳出循环
                break
        
        # 将所有行用换行符连接
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
    参数说明：
    - units: 单元列表
    - source_index: 要复制的单元索引（从0开始）
    - target_position: 目标位置（整数）
      - 0: 最前
      - -1: 最后
      - 其他数字: 在第n个单元之后复制（n从1开始）
    """
    if source_index < 0 or source_index >= len(units):
        return units
    
    unit_to_copy = units[source_index]
    new_units = units.copy()
    
    if target_position == 0:  # 最前
        new_units.insert(0, unit_to_copy)
    elif target_position == -1:  # 最后
        new_units.append(unit_to_copy)
    else:  # 在第n个单元之后复制
        # target_position是用户输入的从1开始的序号
        target_index = target_position  # 用户输入的是在第几个单元之后
        
        # 如果目标位置大于等于当前单元数，则添加到末尾
        if target_index >= len(new_units):
            new_units.append(unit_to_copy)
        else:
            # 在第target_index个单元之后插入
            new_units.insert(target_index + 1, unit_to_copy)
    
    return new_units

def add_string_to_lines(lines, position, string_to_add):
    """
    在每一行的指定位置后添加字符串
    参数说明：
    - lines: 行列表
    - position: 要添加字符串的位置（从0开始计数，0表示在最前，1表示在第一个字符后）
    - string_to_add: 要添加的字符串
    """
    new_lines = []
    
    for line_num, line in enumerate(lines, 1):
        # position是从0开始计数的，表示在第n个字符后添加
        # 如果position为0，则在行首添加
        # 如果position大于等于行长度，则在行尾添加
        insert_index = position
        
        if insert_index >= len(line):
            new_line = line + string_to_add
            position_desc = f"行尾（第{len(line)}个字符后）"
        elif insert_index <= 0:
            new_line = string_to_add + line
            position_desc = "行首"
        else:
            new_line = line[:insert_index] + string_to_add + line[insert_index:]
            position_desc = f"第{insert_index}个字符后"
        
        new_lines.append(new_line)
        print(f"第 {line_num} 行: 在{position_desc}添加字符串 '{string_to_add}'")
        print(f"  原始: {repr(line)}")
        print(f"  结果: {repr(new_line)}")
    
    return new_lines

def delete_string_from_lines(lines, string_to_delete, times_per_line):
    """
    在每一行中删除指定字符串，每行删除指定次数
    参数说明：
    - lines: 行列表
    - string_to_delete: 要删除的字符串
    - times_per_line: 每行删除的次数（删除指定次数后，该行再出现这个字符串就不删除）
    """
    new_lines = []
    
    for line_num, line in enumerate(lines, 1):
        count = 0
        new_line = line
        string_length = len(string_to_delete)
        
        # 使用while循环进行字符串查找和删除
        search_pos = 0
        while count < times_per_line:
            # 从search_pos开始查找字符串
            found_pos = new_line.find(string_to_delete, search_pos)
            if found_pos == -1:
                # 没有找到更多匹配
                break
            
            # 删除找到的字符串
            new_line = new_line[:found_pos] + new_line[found_pos + string_length:]
            count += 1
            # 从删除位置开始继续搜索
            search_pos = found_pos
        
        new_lines.append(new_line)
        print(f"第 {line_num} 行: 删除字符串 '{string_to_delete}' {count}次")
        print(f"  原始: {repr(line)}")
        print(f"  结果: {repr(new_line)}")
    
    return new_lines

def replace_string_in_lines(lines, old_string, new_string, times_per_line):
    """
    在每一行中替换指定字符串，每行替换指定次数
    参数说明：
    - lines: 行列表
    - old_string: 要替换的字符串
    - new_string: 替换为的字符串
    - times_per_line: 每行替换的次数（替换指定次数后，该行再出现这个字符串就不替换）
    """
    new_lines = []
    
    for line_num, line in enumerate(lines, 1):
        count = 0
        new_line = line
        old_length = len(old_string)
        
        # 使用while循环进行字符串查找和替换
        search_pos = 0
        while count < times_per_line:
            # 从search_pos开始查找字符串
            found_pos = new_line.find(old_string, search_pos)
            if found_pos == -1:
                # 没有找到更多匹配
                break
            
            # 替换找到的字符串
            new_line = new_line[:found_pos] + new_string + new_line[found_pos + old_length:]
            count += 1
            # 从替换后的位置开始继续搜索
            search_pos = found_pos + len(new_string)
        
        new_lines.append(new_line)
        print(f"第 {line_num} 行: 替换字符串 '{old_string}' -> '{new_string}' {count}次")
        print(f"  原始: {repr(line)}")
        print(f"  结果: {repr(new_line)}")
    
    return new_lines

def get_non_empty_input(prompt):
    """
    获取非空输入（包括空格）
    允许输入空格或其他空白字符
    """
    while True:
        user_input = input(prompt)
        if user_input == "":
            print("输入不能为空，请重新输入")
        else:
            return user_input

def get_string_input(prompt):
    """
    获取字符串输入（允许空格）
    """
    user_input = input(prompt)
    return user_input

def get_operation_parameters():
    """
    获取用户的操作参数
    """
    # 询问操作类型
    print("\n请选择操作类型:")
    print("1. 单元移动")
    print("2. 单元删除")
    print("3. 单元复制")
    print("4. 添加字符串")
    print("5. 删除字符串")
    print("6. 替换字符串")
    
    while True:
        operation_choice = input("请选择操作类型 (1-6): ").strip()
        if operation_choice in ["1", "2", "3", "4", "5", "6"]:
            break
        else:
            print("请输入 1-6 之间的数字")
    
    if operation_choice == "4":  # 添加字符串
        # 询问添加位置（第几个字符后）
        print("\n位置说明：")
        print("0 - 在最前面添加")
        print("1 - 在第一个字符后添加")
        print("...")
        
        while True:
            try:
                position = input("请在每一行的第几个字符后添加字符串（输入数字）: ").strip()
                position = int(position)
                if position >= 0:
                    break
                else:
                    print("请输入有效数字（0表示在最前，1表示在第一个字符后）")
            except ValueError:
                print("请输入有效数字")
        
        # 询问要添加的字符串
        string_to_add = get_string_input("请输入要添加的字符串（可以为空，也可以包含空格）: ")
        
        return "添加字符串", None, position, string_to_add
    
    elif operation_choice == "5":  # 删除字符串
        # 询问要删除的字符串
        print("\n注意：如果要删除空格或其他字符串，请直接输入")
        string_to_delete = get_string_input("请输入要删除的字符串: ")
        
        if string_to_delete == "":
            print("警告：删除空字符串会导致无变化")
        
        # 询问每行删除的次数
        print("\n删除次数说明：")
        print("每行删除指定次数后，该行再出现这个字符串就不删除")
        
        while True:
            try:
                times = input("每行删除几次（输入数字）: ").strip()
                times_per_line = int(times)
                if times_per_line >= 0:
                    break
                else:
                    print("请输入有效数字（0表示不删除）")
            except ValueError:
                print("请输入有效数字")
        
        return "删除字符串", string_to_delete, times_per_line, None
    
    elif operation_choice == "6":  # 替换字符串
        # 询问要替换的字符串
        print("\n注意：如果要替换空格或其他字符串，请直接输入")
        old_string = get_string_input("请输入要替换的字符串: ")
        
        if old_string == "":
            print("警告：替换空字符串会导致在所有位置插入新字符串")
        
        # 询问替换为的字符串
        new_string = get_string_input("请输入替换为什么字符串: ")
        
        # 询问每行替换的次数
        print("\n替换次数说明：")
        print("每行替换指定次数后，该行再出现这个字符串就不替换")
        
        while True:
            try:
                times = input("每行替换几次（输入数字）: ").strip()
                times_per_line = int(times)
                if times_per_line >= 0:
                    break
                else:
                    print("请输入有效数字（0表示不替换）")
            except ValueError:
                print("请输入有效数字")
        
        return "替换字符串", old_string, new_string, times_per_line
    
    # 对于单元操作（移动、删除、复制），需要询问单元序号
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
        print("或输入其他数字表示在第几个单元之后复制")
        
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
    
    # 显示文本行数
    print(f"\n文本共 {len(lines)} 行")
    
    # 获取操作参数
    operation_type, param1, param2, param3 = get_operation_parameters()
    
    if operation_type is None:
        print("跳过操作，返回原始文本")
        return text
    
    # 处理字符串操作（添加、删除、替换）
    if operation_type == "添加字符串":
        print(f"\n开始在所有行添加字符串")
        processed_lines = add_string_to_lines(lines, param1, param2)
        return '\n'.join(processed_lines)
    
    elif operation_type == "删除字符串":
        print(f"\n开始在所有行删除字符串")
        processed_lines = delete_string_from_lines(lines, param1, param2)
        return '\n'.join(processed_lines)
    
    elif operation_type == "替换字符串":
        print(f"\n开始在所有行替换字符串")
        processed_lines = replace_string_in_lines(lines, param1, param2, param3)
        return '\n'.join(processed_lines)
    
    # 对于单元操作（移动、删除、复制），需要先提取单元并显示单元情况
    print("\n文本分析结果")
    for line_num, line in enumerate(lines, 1):
        units, _ = extract_units(line)
        print(f"第 {line_num} 行: 找到 {len(units)} 个单元 - {line}")
    
    # 处理单元操作（移动、删除、复制）
    print("\n开始处理所有行")
    processed_lines = []
    for line_num, line in enumerate(lines, 1):
        units, positions = extract_units(line)
        
        if not units:
            print(f"第 {line_num} 行: 未找到方括号单元，跳过")
            processed_lines.append(line)
            continue
        
        # 检查单元索引是否有效
        if param1 >= len(units):  # param1在这里是unit_index
            print(f"第 {line_num} 行: 单元索引超出范围 (只有 {len(units)} 个单元)，跳过")
            processed_lines.append(line)
            continue
        
        # 执行操作
        if operation_type == "移动":
            new_units = move_unit(units, param1, param2, param3)
        elif operation_type == "删除":
            new_units = delete_unit(units, param1)
        elif operation_type == "复制":
            new_units = copy_unit(units, param1, param2)
        
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
    
    # 检查依赖
    try:
        import pyperclip
    except ImportError:
        print("请先安装 pyperclip 模块: pip install pyperclip")
        sys.exit(1)
    
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
            print(processed_text)
        except Exception as e:
            print(f"写入剪贴板失败: {e}")
    else:
        print("文本未发生变化")

if __name__ == "__main__":
    main()