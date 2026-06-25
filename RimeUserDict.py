# 请帮我写个中文的 Python 脚本，批注也是中文：
# 将当前剪贴板内的词组存入变量。将其中的汉语词组解析为汉语拼音，每个字用空格隔开；
# 如词组间有英文字母，则该位置保留英文字母，英文字母和汉语拼音间用空格隔开。
# 将原词组与拼音用 Tab 隔开，再加数字（默认 10），也用 Tab 隔开，
# 以 UTF-8 追加写入 D:\ProApps\Rime\config\dicts\user.dict.yaml。

# 运行前请执行：pip install pypinyin

import signal
import subprocess
import sys
from pathlib import Path

from pypinyin import lazy_pinyin, Style

# ==================== 全局配置 ====================

# --- 路径常量 ---
DICT_PATH = Path(r"D:\ProApps\Rime\config\dicts\user.dict.yaml")

# --- 配置常量 ---
DEFAULT_WEIGHT = 10

_quit_requested = False  # Ctrl+Q 中断标志

# --- 消息常量 ---
MSG_CLIPBOARD_EMPTY = "剪贴板内容为空！"
MSG_READ_CLIPBOARD_FAIL = "读取剪贴板失败：{}"
MSG_WRITE_SUCCESS = "成功添加到词典："
MSG_WRITE_DETAIL_WORD = "  词组：{}"
MSG_WRITE_DETAIL_PINYIN = "  拼音：{}"
MSG_WRITE_DETAIL_PATH = "  已写入：{}"
MSG_WRITE_FAIL = "写入文件时出错：{}"
MSG_INTERRUPTED = "\n用户中断，程序退出。"
MSG_ERROR = "❌ 发生未捕获的异常：{}"
MSG_EXIT = "\n按回车键退出..."


def read_clipboard() -> str | None:
    """从 Windows 剪贴板读取文本，失败返回 None。"""
    try:
        result = subprocess.run(
            ["powershell", "-NonInteractive", "-Command", "Get-Clipboard -Raw"],
            capture_output=True,
            encoding="utf-8",
            check=True,
        )
        return result.stdout
    except Exception as e:
        print(MSG_READ_CLIPBOARD_FAIL.format(e))
        return None


def is_chinese(char: str) -> bool:
    """判断字符是否为汉字。"""
    return "一" <= char <= "鿿"


def text_to_pinyin(text: str) -> str:
    """
    将中英混合文本转换为拼音。
    汉字 → 带声调拼音（字间空格隔开）；英文 → 保持原样。
    中英文交界处用空格隔开。
    """
    if not text:
        return ""

    # 第一步：将文本按中/英边界拆分为连续段
    blocks: list[str] = []
    current = [text[0]]
    current_type = is_chinese(text[0])

    for char in text[1:]:
        char_type = is_chinese(char)
        if char_type == current_type:
            current.append(char)
        else:
            blocks.append("".join(current))
            current = [char]
            current_type = char_type
    blocks.append("".join(current))

    # 第二步：中文段转拼音，英文段保留
    result: list[str] = []
    for block in blocks:
        if block and is_chinese(block[0]):
            pinyin_list = lazy_pinyin(block, style=Style.TONE)
            result.append(" ".join(pinyin_list))
        else:
            result.append(block)

    return " ".join(result)
# ==================== 中断处理 ====================


def _on_quit_signal(signum, frame):
    global _quit_requested
    _quit_requested = True
    raise KeyboardInterrupt()


def _init_quit_handler():
    if hasattr(signal, "SIGQUIT"):
        signal.signal(signal.SIGQUIT, _on_quit_signal)


def _check_quit() -> bool:
    global _quit_requested
    if sys.platform == "win32":
        try:
            import msvcrt
            while msvcrt.kbhit():
                if msvcrt.getch() == b"\x11":
                    _quit_requested = True
        except Exception:
            pass
    return _quit_requested


def main() -> None:
    """主流程：读取剪贴板 → 转拼音 → 追加写入词典。"""
    clipboard_content = read_clipboard()
    if not clipboard_content:
        print(MSG_CLIPBOARD_EMPTY)
        return

    clipboard_content = clipboard_content.strip()
    pinyin_result = text_to_pinyin(clipboard_content)

    # 构建写入内容：词组 \t 拼音 \t 权重
    output_line = f"{clipboard_content}\t{pinyin_result}\t{DEFAULT_WEIGHT}\n"

    try:
        DICT_PATH.parent.mkdir(parents=True, exist_ok=True)
        with DICT_PATH.open("a", encoding="utf-8") as f:
            f.write(output_line)
        print(MSG_WRITE_SUCCESS)
        print(MSG_WRITE_DETAIL_WORD.format(clipboard_content))
        print(MSG_WRITE_DETAIL_PINYIN.format(pinyin_result))
        print(MSG_WRITE_DETAIL_PATH.format(DICT_PATH))
    except OSError as e:
        print(MSG_WRITE_FAIL.format(e))


def test_pinyin_conversion() -> None:
    """测试拼音转换功能。"""
    test_cases = [
        "你好世界",
        "hello世界",
        "拼音pinyin",
        "测试声调",
        "中国",
        "北京欢迎你",
        "a测试b",
    ]

    print("拼音转换测试（带符号声调）：")
    print("-" * 50)

    for test in test_cases:
        result = text_to_pinyin(test)
        print(f"原文：{test}")
        print(f"拼音：{result}")

        if any(is_chinese(c) for c in test):
            print("详细转换：")
            for char in test:
                if is_chinese(char):
                    pinyin = lazy_pinyin(char, style=Style.TONE)[0]
                    print(f"  '{char}' -> {pinyin}")



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
