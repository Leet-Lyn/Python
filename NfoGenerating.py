# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件夹位置（默认为“d:\Studios\Folders\Outs”）。
# 遍历源文件夹位置中所有的文件（mkv、avi、f4v、flv、ts、mpeg、mpg、rm、rmvb、asf、wmv、mov、webm、mp4、mp3、ogg、aac、ac3、wma、pdf、epub、zip、rar、7z）。在该文件夹下生成同名 nfo 文件。
# 询问我 nfo 文件内写入的内容。UTF-8编码，默认为：<?xml version="1.0" encoding="UTF-8" standalone="yes"?><movie><title> </title></movie>
# 再次枚举源文件夹位置中所有 nfo 文件，读取其文件名（不包括后缀名），将文件名中的”][“，替换为半角空格，再将”]“与”[“删除。，替换“<title> </title>”内的“ ”。

# 导入模块
import os
import sys

# ==================== 全局配置 ====================

DEFAULT_SOURCE_DIR = r"d:\Studios\Folders\Outs"

# --- 消息常量 ---
MSG_INTERRUPTED = "\n\n用户中断程序，已退出。"
MSG_ERROR = "\n程序运行出错: {}"
MSG_EXIT = "\n按回车键退出..."
MSG_PATH_INVALID = "错误：路径 '{}' 不存在或不是文件夹，请重新输入。"
MSG_NFO_GENERATED = "已生成 NFO 文件: {}"
MSG_NFO_SKIP_EXISTS = "跳过，NFO 文件已存在: {}"
MSG_NFO_GEN_DONE = "\nNFO 文件生成完成。共生成 {} 个新文件。"
MSG_NFO_UPDATED = "已更新 NFO 文件: {}"
MSG_NFO_SKIP_NO_TITLE = "跳过，未找到 <title> </title> 标签: {}"
MSG_NFO_PROCESS_ERROR = "处理文件时出错 {}: {}"
MSG_NFO_UPDATE_DONE = "\nNFO 文件更新完成。共更新 {} 个文件。"
MSG_TITLE = "批量生成和更新 NFO 文件工具"
MSG_PROMPT_SOURCE_DIR = "请输入源文件夹路径（直接回车使用默认路径 '{}'）: "
MSG_USING_FOLDER = "使用文件夹: {}"
MSG_PROMPT_TEMPLATE = "\n请输入 NFO 文件的内容模板（直接回车使用默认模板）:"
MSG_DEFAULT_TEMPLATE_LABEL = "默认模板为："
MSG_TEMPLATE_INPUT = "您的模板: "
MSG_USING_USER_TEMPLATE = "使用用户提供的模板。"
MSG_USING_DEFAULT_TEMPLATE = "使用默认模板。"
MSG_START_GENERATING = "\n开始生成 NFO 文件..."
MSG_START_UPDATING = "\n开始更新 NFO 文件..."
MSG_ALL_DONE = "\n操作完成！"
MSG_GENERATED_COUNT = "共生成 {} 个新 NFO 文件"
MSG_UPDATED_COUNT = "共更新 {} 个 NFO 文件"
MSG_PRESS_ENTER = "\n按回车键退出程序..."


def 获取有效文件夹路径(提示信息, 默认文件夹=None):
    """
    获取用户输入的文件夹路径，支持默认路径和验证有效性

    参数:
        提示信息: 显示给用户的提示文本
        默认文件夹: 用户不输入时使用的默认路径

    返回:
        有效的文件夹路径字符串
    """
    while True:
        文件夹路径 = input(提示信息).strip()

        # 如果用户没有输入且提供了默认路径，则使用默认路径
        if not 文件夹路径 and 默认文件夹 is not None:
            文件夹路径 = 默认文件夹

        # 验证路径是否存在且是文件夹
        if os.path.isdir(文件夹路径):
            return 文件夹路径
        else:
            print(MSG_PATH_INVALID.format(文件夹路径))

def 处理文件名(原始文件名):
    """
    处理文件名：替换"]["为空格，删除"]"和"["
    
    参数:
        原始文件名: 待处理的文件名（不含扩展名）
    
    返回:
        处理后的文件名
    """
    # 先将"]["替换为空格，再删除所有的"]"和"["
    return 原始文件名.replace('][', ' ').replace(']', '').replace('[', '')

def 生成NFO文件(源文件夹路径, XML模板):
    """
    遍历源文件夹中的所有支持的文件，生成对应的NFO文件
    
    参数:
        源文件夹路径: 要遍历的文件夹路径
        XML模板: NFO文件的XML模板内容
    """
    # 支持的文件扩展名集合（转换为小写以便比较）
    支持的文件扩展名 = {
        # 视频文件
        '.mkv', '.avi', '.f4v', '.flv', '.ts',
        '.mpeg', '.mpg', '.rm', '.rmvb', '.asf',
        '.wmv', '.mov', '.webm', '.mp4',
        # 音频文件
        '.mp3', '.ogg', '.aac', '.ac3', '.wma',
        # 文档文件
        '.pdf', '.epub',
        # 压缩文件
        '.zip', '.rar', '.7z'
    }
    
    已生成文件数 = 0
    
    # 使用 os.walk 遍历源文件夹及其所有子文件夹
    for 当前目录路径, 子文件夹列表, 文件列表 in os.walk(源文件夹路径):
        for 文件名 in 文件列表:
            # 获取文件扩展名并转换为小写
            文件扩展名 = os.path.splitext(文件名)[1].lower()
            
            # 检查文件扩展名是否在支持的列表中
            if 文件扩展名 in 支持的文件扩展名:
                # 获取文件名（不含扩展名）
                基本文件名 = os.path.splitext(文件名)[0]
                
                # 构建 NFO 文件完整路径
                NFO文件路径 = os.path.join(当前目录路径, f"{基本文件名}.nfo")
                
                # 检查 NFO 文件是否已存在
                if not os.path.exists(NFO文件路径):
                    # 以 UTF-8 编码写入 XML 模板内容
                    with open(NFO文件路径, 'w', encoding='utf-8') as NFO文件:
                        NFO文件.write(XML模板)
                    已生成文件数 += 1
                    print(MSG_NFO_GENERATED.format(NFO文件路径))
                else:
                    print(MSG_NFO_SKIP_EXISTS.format(NFO文件路径))

    print(MSG_NFO_GEN_DONE.format(已生成文件数))
    return 已生成文件数

def 更新NFO文件(源文件夹路径):
    """
    遍历源文件夹中的所有NFO文件，用处理后的文件名更新<title>标签内容
    
    参数:
        源文件夹路径: 要遍历的文件夹路径
    
    返回:
        更新的文件数量
    """
    已更新文件数 = 0
    
    # 使用 os.walk 遍历源文件夹及其所有子文件夹
    for 当前目录路径, 子文件夹列表, 文件列表 in os.walk(源文件夹路径):
        for 文件名 in 文件列表:
            # 只处理 .nfo 文件
            if 文件名.endswith('.nfo'):
                # 获取文件名（不含扩展名）
                基本文件名 = os.path.splitext(文件名)[0]
                
                # 处理文件名：替换"]["为空格，删除"]"和"["
                处理后的文件名 = 处理文件名(基本文件名)
                
                # 构建 NFO 文件完整路径
                NFO文件路径 = os.path.join(当前目录路径, 文件名)
                
                try:
                    # 以 UTF-8 编码读取文件内容
                    with open(NFO文件路径, 'r', encoding='utf-8') as 文件:
                        文件内容 = 文件.read()
                    
                    # 检查文件中是否包含<title> </title>标签
                    if "<title> </title>" in 文件内容:
                        # 替换<title> </title>为<title>处理后的文件名</title>
                        新内容 = 文件内容.replace(
                            "<title> </title>", 
                            f"<title>{处理后的文件名}</title>"
                        )
                        
                        # 以 UTF-8 编码写回文件
                        with open(NFO文件路径, 'w', encoding='utf-8') as 文件:
                            文件.write(新内容)
                        
                        已更新文件数 += 1
                        print(MSG_NFO_UPDATED.format(NFO文件路径))
                    else:
                        print(MSG_NFO_SKIP_NO_TITLE.format(NFO文件路径))

                except Exception as 错误:
                    print(MSG_NFO_PROCESS_ERROR.format(NFO文件路径, 错误))

    print(MSG_NFO_UPDATE_DONE.format(已更新文件数))
    return 已更新文件数

def main():
    """
    主程序流程控制
    """
    print("=" * 50)
    print(MSG_TITLE)
    print("=" * 50)

    # 获取源文件夹路径
    提示信息 = MSG_PROMPT_SOURCE_DIR.format(DEFAULT_SOURCE_DIR)
    源文件夹路径 = 获取有效文件夹路径(提示信息, DEFAULT_SOURCE_DIR)

    print(MSG_USING_FOLDER.format(源文件夹路径))

    # 获取 XML 模板内容
    print(MSG_PROMPT_TEMPLATE)
    print(MSG_DEFAULT_TEMPLATE_LABEL)
    print('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>')
    print('<movie>')
    print('  <title> </title>')
    print('</movie>')

    用户输入模板 = input(MSG_TEMPLATE_INPUT).strip()

    # 使用用户输入的模板或默认模板
    if 用户输入模板:
        XML模板 = 用户输入模板
        print(MSG_USING_USER_TEMPLATE)
    else:
        XML模板 = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<movie>\n  <title> </title>\n</movie>'
        print(MSG_USING_DEFAULT_TEMPLATE)

    print("\n" + "=" * 50)
    print(MSG_START_GENERATING.strip())
    print("=" * 50)

    # 生成 NFO 文件
    生成的文件数 = 生成NFO文件(源文件夹路径, XML模板)

    print("\n" + "=" * 50)
    print(MSG_START_UPDATING.strip())
    print("=" * 50)

    # 更新 NFO 文件
    更新的文件数 = 更新NFO文件(源文件夹路径)

    print("\n" + "=" * 50)
    print(MSG_ALL_DONE.strip())
    print(MSG_GENERATED_COUNT.format(生成的文件数))
    print(MSG_UPDATED_COUNT.format(更新的文件数))
    print("=" * 50)


# ==================== 程序入口 ====================

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    try:
        main()
    except KeyboardInterrupt:
        print(MSG_INTERRUPTED)
    except Exception as e:
        print(MSG_ERROR.format(e))
    finally:
        input(MSG_EXIT)