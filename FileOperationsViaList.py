# 请帮我写个中文的 Python 脚本，批注也是中文，但是变量参数不要是中文：
# 询问我需要的操作：1. 移动； 2. 复制；3. 重命名；4. 文件路径生成；5. 文件名生成列表。

# 1. 移动：询问我列表路径（默认“d:\\Works\\Attachments\\Lists.txt”）。源文件夹路径（默认“d:\\Works\\Ins\\”）与目标文件夹路径（默认“d:\\Works\\Outs\\”）。列表里一行一个文件名（有扩展名）。请枚举每一行的文件名，找到源文件夹里匹配的文件，移动到目标文件夹。
# 2. 复制：询问我列表路径（默认“d:\\Works\\Attachments\\Lists.txt”）。源文件夹路径（默认“d:\\Works\\Ins\\”）与目标文件夹路径（默认“d:\\Works\\Outs\\”）。列表里一行一个文件名（有扩展名）。请枚举每一行的文件名，找到源文件夹里匹配的文件，复制到目标文件夹。
# 3. 重命名：询问我列表路径（默认“d:\\Works\\Attachments\\Lists.txt”）。源文件夹路径（默认“d:\\Works\\Ins\\”）。列表里一行一个文件名（有扩展名）。请枚举每一行的文件名，重命名文件夹里的路径（按名称排序）。不涉及文件夹。
# 4. 文件路径生成：询问我列表路径（默认“d:\\Works\\Attachments\\Lists.txt”）。源文件夹路径（默认“d:\\Works\\Ins\\”）。询问我是否匹配文件夹，询问我是否包含子文件夹里。将源文件夹路径里的所有文件的路径写入列表中。
# 5. 文件名生成列表（包含子文件夹里）：询问我列表路径（默认“d:\\Works\\Attachments\\Lists.txt”）。源文件夹路径（默认“d:\\Works\\Ins\\”）。询问我是否匹配文件夹，询问我是否包含子文件夹里。将源文件夹路径里的所有文件的名称写入列表中。
# 结束后重复询问。

# 导入模块
import os
import shutil
import sys

def get_input(prompt, default):
    """
    获取用户输入，若直接回车则返回默认值
    """
    user_input = input(f"{prompt} (默认: {default}): ").strip()
    return user_input if user_input else default

def read_list_file(file_path):
    """
    读取列表文件，每行一个文件名（含扩展名），忽略空行和首尾空白
    """
    if not os.path.isfile(file_path):
        print(f"错误：列表文件不存在 -> {file_path}")
        return []
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        items = [line.strip() for line in f if line.strip()]
    return items

def move_files(list_path, src_dir, dst_dir):
    """
    移动文件：根据列表中的文件名，从源文件夹移动到目标文件夹
    """
    file_names = read_list_file(list_path)
    if not file_names:
        print("列表为空或读取失败，操作取消。")
        return
    if not os.path.isdir(src_dir):
        print(f"错误：源文件夹不存在 -> {src_dir}")
        return
    os.makedirs(dst_dir, exist_ok=True)

    moved_count = 0
    for name in file_names:
        src_path = os.path.join(src_dir, name)
        dst_path = os.path.join(dst_dir, name)
        if not os.path.isfile(src_path):
            print(f"警告：未找到文件，跳过 -> {src_path}")
            continue
        if os.path.exists(dst_path):
            print(f"警告：目标已存在，跳过 -> {dst_path}")
            continue
        shutil.move(src_path, dst_path)
        print(f"已移动: {name}")
        moved_count += 1
    print(f"移动完成，共处理 {moved_count} 个文件。")

def copy_files(list_path, src_dir, dst_dir):
    """
    复制文件：根据列表中的文件名，从源文件夹复制到目标文件夹
    """
    file_names = read_list_file(list_path)
    if not file_names:
        print("列表为空或读取失败，操作取消。")
        return
    if not os.path.isdir(src_dir):
        print(f"错误：源文件夹不存在 -> {src_dir}")
        return
    os.makedirs(dst_dir, exist_ok=True)

    copied_count = 0
    for name in file_names:
        src_path = os.path.join(src_dir, name)
        dst_path = os.path.join(dst_dir, name)
        if not os.path.isfile(src_path):
            print(f"警告：未找到文件，跳过 -> {src_path}")
            continue
        if os.path.exists(dst_path):
            print(f"警告：目标已存在，跳过 -> {dst_path}")
            continue
        shutil.copy2(src_path, dst_path)
        print(f"已复制: {name}")
        copied_count += 1
    print(f"复制完成，共处理 {copied_count} 个文件。")

def rename_files(list_path, src_dir):
    """
    重命名文件：将源文件夹中的文件按名称排序后，依次重命名为列表中提供的名称
    """
    new_names = read_list_file(list_path)
    if not new_names:
        print("列表为空或读取失败，操作取消。")
        return
    if not os.path.isdir(src_dir):
        print(f"错误：源文件夹不存在 -> {src_dir}")
        return

    all_files = [f for f in os.listdir(src_dir) if os.path.isfile(os.path.join(src_dir, f))]
    all_files.sort()

    if len(all_files) != len(new_names):
        print(f"警告：源文件夹中有 {len(all_files)} 个文件，但列表提供了 {len(new_names)} 个新名称，数量不匹配。")
        confirm = input("是否仍要继续重命名？(y/n): ").strip().lower()
        if confirm != 'y':
            print("操作已取消。")
            return

    renamed = 0
    for old_name, new_name in zip(all_files, new_names):
        old_path = os.path.join(src_dir, old_name)
        new_path = os.path.join(src_dir, new_name)
        if old_name == new_name:
            print(f"跳过（名称未变）: {old_name}")
            continue
        if os.path.exists(new_path):
            print(f"警告：目标名称已存在，跳过 -> {new_name}")
            continue
        os.rename(old_path, new_path)
        print(f"重命名: {old_name} -> {new_name}")
        renamed += 1
    print(f"重命名完成，共处理 {renamed} 个文件。")

def generate_path_list(list_path, src_dir, include_folders, include_subdirs):
    """
    生成文件（及可选文件夹）路径列表，写入指定文件
    """
    if not os.path.isdir(src_dir):
        print(f"错误：源文件夹不存在 -> {src_dir}")
        return

    paths = []
    if include_subdirs:
        for root, dirs, files in os.walk(src_dir):
            if include_folders:
                for d in dirs:
                    paths.append(os.path.join(root, d))
            for f in files:
                paths.append(os.path.join(root, f))
    else:
        for entry in os.listdir(src_dir):
            full_path = os.path.join(src_dir, entry)
            if os.path.isfile(full_path):
                paths.append(full_path)
            elif os.path.isdir(full_path) and include_folders:
                paths.append(full_path)

    os.makedirs(os.path.dirname(list_path), exist_ok=True) if os.path.dirname(list_path) else None
    with open(list_path, 'w', encoding='utf-8') as f:
        for p in paths:
            f.write(p + '\n')
    print(f"已生成路径列表，共 {len(paths)} 条，保存至: {list_path}")

def generate_name_list(list_path, src_dir, include_folders, include_subdirs):
    """
    生成文件名（及可选文件夹名）列表，写入指定文件
    """
    if not os.path.isdir(src_dir):
        print(f"错误：源文件夹不存在 -> {src_dir}")
        return

    names = []
    if include_subdirs:
        for root, dirs, files in os.walk(src_dir):
            if include_folders:
                for d in dirs:
                    names.append(d)
            for f in files:
                names.append(f)
    else:
        for entry in os.listdir(src_dir):
            full_path = os.path.join(src_dir, entry)
            if os.path.isfile(full_path):
                names.append(entry)
            elif os.path.isdir(full_path) and include_folders:
                names.append(entry)

    os.makedirs(os.path.dirname(list_path), exist_ok=True) if os.path.dirname(list_path) else None
    with open(list_path, 'w', encoding='utf-8') as f:
        for name in names:
            f.write(name + '\n')
    print(f"已生成名称列表，共 {len(names)} 条，保存至: {list_path}")

def main():
    # 公共默认路径
    default_list = "d:\\Works\\Attachments\\Lists.txt"
    default_src  = "d:\\Works\\Ins\\"
    default_dst  = "d:\\Works\\Outs\\"

    while True:
        print("\n===== 文件管理工具 =====")
        print("1. 移动")
        print("2. 复制")
        print("3. 重命名")
        print("4. 文件路径生成")
        print("5. 文件名生成列表")
        print("0. 退出")
        choice = input("请输入数字(0-5): ").strip()

        if choice == '0':
            print("程序已退出。")
            break

        elif choice == '1':
            print("\n--- 移动文件 ---")
            list_path = get_input("列表文件路径", default_list)
            src_dir   = get_input("源文件夹路径", default_src)
            dst_dir   = get_input("目标文件夹路径", default_dst)
            move_files(list_path, src_dir, dst_dir)

        elif choice == '2':
            print("\n--- 复制文件 ---")
            list_path = get_input("列表文件路径", default_list)
            src_dir   = get_input("源文件夹路径", default_src)
            dst_dir   = get_input("目标文件夹路径", default_dst)
            copy_files(list_path, src_dir, dst_dir)

        elif choice == '3':
            print("\n--- 重命名文件 ---")
            list_path = get_input("列表文件路径", default_list)
            src_dir   = get_input("源文件夹路径", default_src)
            rename_files(list_path, src_dir)

        elif choice == '4':
            print("\n--- 生成文件路径列表 ---")
            list_path = get_input("列表文件路径", default_list)
            src_dir   = get_input("源文件夹路径", default_src)
            inc_folders = get_input("是否包含文件夹路径？(y/n)", "n").strip().lower() == 'y'
            inc_sub     = get_input("是否包含子文件夹？(y/n)", "n").strip().lower() == 'y'
            generate_path_list(list_path, src_dir, inc_folders, inc_sub)

        elif choice == '5':
            print("\n--- 生成文件名列表 ---")
            list_path = get_input("列表文件路径", default_list)
            src_dir   = get_input("源文件夹路径", default_src)
            inc_folders = get_input("是否包含文件夹名称？(y/n)", "n").strip().lower() == 'y'
            inc_sub     = get_input("是否包含子文件夹？(y/n)", "n").strip().lower() == 'y'
            generate_name_list(list_path, src_dir, inc_folders, inc_sub)

        else:
            print("无效的选择，请输入0-5之间的数字。")

        # 每次操作后暂停一下，方便查看结果
        input("\n按回车键继续...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n操作被用户中断。")
    except Exception as e:
        print(f"发生未预期的错误: {e}")