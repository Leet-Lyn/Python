# 请帮我写个中文的 Python 脚本，批注也是中文。
# 开始询问我目标文件夹位置（默认为“E:\\Backups\\StartMenu\\”）。依次运行该文件夹下所有 *.lnk 指向的内容。

# 导入模块
import os

# 获取用户输入的目标文件夹路径，默认值为“E:\\Backups\\StartMenu\\”
folder = input("请输入目标文件夹位置（默认 E:\\Backups\\StartMenu\\）：").strip()
if not folder:
    folder = "E:\\Backups\\StartMenu\\"
# 规范路径格式并转换为绝对路径
folder = os.path.abspath(os.path.normpath(folder))

# 检查目标文件夹是否存在
if not os.path.isdir(folder):
    print(f"错误：文件夹 '{folder}' 不存在。")
    exit(1)

# 扫描目录下所有.lnk文件（不区分大小写）
lnk_files = [
    os.path.join(folder, f)
    for f in os.listdir(folder)
    if f.lower().endswith(".lnk")
]

if not lnk_files:
    print(f"在文件夹 '{folder}' 中未找到任何快捷方式文件。")
    exit(0)

# 依次执行每个快捷方式
for lnk_path in lnk_files:
    try:
        # 使用系统关联程序打开文件（效果类似双击）
        os.startfile(lnk_path)
        print(f"✅ 已启动：{os.path.basename(lnk_path)}")
    except Exception as e:
        print(f"❌ 启动失败：{os.path.basename(lnk_path)}\n    错误信息：{str(e)}")


# 按下回车键退出。
input("按回车键退出...")