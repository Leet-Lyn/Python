# 请帮我写个中文的 Python 脚本，批注也是中文：
# 询问我询问源文件夹位置（默认：d:\Works\Downloads\）。
# 1. 检索该文件夹下，所有一级子文件夹（不包括其下子文件夹）。列出子文件夹数量。
# 2. 分别检索该文件夹下，所有一级子文件夹（不包括其下子文件夹），枚举出所有一级子文件夹下所拥有的文件数量。最后汇总：有1个文件的子文件夹子文件夹有几个，分别是：……有2个文件的子文件夹子文件夹有几个，分别是：……有3个文件的子文件夹子文件夹有几个，分别是：……以此类推。
# 完成后，跳到开始询问我源文件夹位置。反复循环。

# 导入模块
import os

def main():
    """
    主循环：反复询问源文件夹路径，执行统计并输出结果。
    """
    while True:
        # 询问源文件夹位置，默认路径为 d:\Works\Downloads\
        user_input = input("请输入源文件夹位置（默认：d:\\Works\\Downloads\\，输入 exit 退出）：").strip()
        
        # 退出条件
        if user_input.lower() in ('exit', 'quit'):
            print("程序已退出。")
            break
        
        # 若输入为空，使用默认路径
        if user_input == "":
            folder_path = r"d:\Works\Downloads"
        else:
            folder_path = user_input
        
        # 规范化路径（去除末尾斜杠、统一分隔符）
        folder_path = os.path.normpath(folder_path)
        
        # 检查路径是否存在且为文件夹
        if not os.path.isdir(folder_path):
            print("错误：文件夹不存在或路径无效，请重新输入。\n")
            continue
        
        # ------------------------------------------------------------------
        # 1. 获取该文件夹下所有一级子文件夹（仅目录，不递归）
        # ------------------------------------------------------------------
        try:
            all_items = os.listdir(folder_path)
        except PermissionError:
            print(f"错误：没有权限访问文件夹 {folder_path}，请检查权限后重试。\n")
            continue
        
        subdirs = []
        for item in all_items:
            item_path = os.path.join(folder_path, item)
            if os.path.isdir(item_path):
                subdirs.append(item)
        
        print(f"\n一级子文件夹数量：{len(subdirs)}")
        
        if len(subdirs) == 0:
            print("没有找到任何一级子文件夹。\n")
            continue
        
        # ------------------------------------------------------------------
        # 2. 统计每个一级子文件夹下的文件数量（不包含子文件夹内的文件）
        # ------------------------------------------------------------------
        file_count_dict = {}  # key: 子文件夹名, value: 文件数量
        for sub in subdirs:
            sub_path = os.path.join(folder_path, sub)
            try:
                entries = os.listdir(sub_path)
                # 只统计文件（不包括子目录）
                file_num = sum(1 for e in entries if os.path.isfile(os.path.join(sub_path, e)))
                file_count_dict[sub] = file_num
            except PermissionError:
                print(f"警告：无法访问子文件夹 {sub}，已跳过该文件夹的统计。")
                continue
        
        # ------------------------------------------------------------------
        # 3. 按文件数量分组，并输出结果
        # ------------------------------------------------------------------
        # groups: key = 文件数量, value = 子文件夹名列表
        groups = {}
        for name, cnt in file_count_dict.items():
            groups.setdefault(cnt, []).append(name)
        
        # 按文件数量从小到大输出
        for cnt in sorted(groups.keys()):
            folder_list = groups[cnt]
            print(f"有 {cnt} 个文件的子文件夹有 {len(folder_list)} 个，分别是：{', '.join(folder_list)}")
        
        print("\n" + "-" * 50 + "\n")  # 分隔线，便于区分每次循环

if __name__ == "__main__":
    main()