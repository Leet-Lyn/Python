# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件夹位置（默认为 d:\\Works\\In\\）。
# 依次将源文件夹下的所有文件，移动至以它们文件名（不包括扩展名）为文件夹名的文件夹中。

# 导入模块
import os
import shutil

def 移动文件到同名文件夹():
    # 步骤1：获取源文件夹路径（带默认值）
    默认路径 = r"d:\Works\In"
    用户输入 = input(f"请输入源文件夹路径（默认为 '{默认路径}'）：").strip()
    源文件夹 = 用户输入 if 用户输入 else 默认路径

    # 验证路径是否存在
    if not os.path.exists(源文件夹):
        print(f"错误：路径 '{源文件夹}' 不存在！")
        return

    # 步骤2：遍历源文件夹中的所有文件
    for 文件名 in os.listdir(源文件夹):
        文件路径 = os.path.join(源文件夹, 文件名)
        
        # 跳过子目录，只处理文件
        if not os.path.isfile(文件路径):
            continue
        
        # 步骤3：提取文件名和扩展名
        主文件名, 扩展名 = os.path.splitext(文件名)
        目标文件夹名 = os.path.join(源文件夹, 主文件名)
        
        # 步骤4：创建目标文件夹（如果不存在）
        if not os.path.exists(目标文件夹名):
            os.makedirs(目标文件夹名)
            print(f"已创建文件夹: {目标文件夹名}")
        
        # 步骤5：移动文件
        目标路径 = os.path.join(目标文件夹名, 文件名)
        shutil.move(文件路径, 目标路径)
        print(f"移动文件: {文件名} -> {目标文件夹名}")

if __name__ == "__main__":
    try:
        移动文件到同名文件夹()
        print("\n操作完成！")
    except Exception as 错误:
        print(f"发生错误: {错误}")
    
# 按下回车键退出。
input("按回车键退出...")