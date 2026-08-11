# 请帮我写个中文的 Python 脚本，批注也是中文：
# 在脚本开始前询问我源文件夹位置（默认"d:\Studios\Folders\Ins\"）与目标文件夹位置（默认"d:\Studios\Folders\Outs\"）。
# 遍历目标文件夹及其子文件夹位置中所有后缀名为 bc! 的文件。在源文件夹中找到其对应的文件（无bc!后缀名）（匹配文件夹子文件夹层级）。
# 将其复制到目标文件夹的 bc! 的文件的所在文件夹（匹配文件夹子文件夹层级）。

import shutil
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# 消息常量（集中定义，MSG_ 前缀 + f-string 占位符）
# ---------------------------------------------------------------------------
MSG_BANNER = "=" * 60
MSG_TITLE = "  BcRestore —— .bc! 文件批量还原工具"
MSG_DIVIDER = "-" * 60

MSG_SRC_PROMPT = "请输入源文件夹路径（默认 d:\\Studios\\Folders\\Ins\\）："
MSG_DST_PROMPT = "请输入目标文件夹路径（默认 d:\\Studios\\Folders\\Outs\\）："

MSG_SRC_NOT_FOUND = '源文件夹不存在："{path}"，脚本退出。'
MSG_DST_NOT_FOUND = '目标文件夹不存在："{path}"，脚本退出。'
MSG_NO_BC_FILES = "在目标文件夹中未找到任何 .bc! 文件，无需处理。"

MSG_FOUND_BC_COUNT = "共找到 {count} 个 .bc! 文件"
MSG_START_PROCESS = "开始处理..."

MSG_OVERWRITE_PROMPT = (
    '  目标文件 "{dst}" 已存在，是否覆盖？(y=覆盖 / n=跳过 / q=退出)：'
)
MSG_INVALID_CHOICE = "  请输入 y / n / q"
MSG_SKIPPED = "  [跳过] {dst}"
MSG_OVERWRITTEN = "  [覆盖] {src} -> {dst}"
MSG_COPIED = "  [复制] {src} -> {dst}"
MSG_MISSING = "  [缺失] 源文件不存在：{src}"
MSG_FAILED = "  [失败] {src} -> {dst}，错误：{error}"
MSG_QUIT_KEY = "\n检测到 Ctrl+Q，准备退出..."
MSG_QUIT_EARLY = "用户请求退出，脚本中止。"

MSG_REPORT_TITLE = "处理完成 —— 统计报告"
MSG_REPORT_TOTAL = "  找到的 .bc! 文件数：{total}"
MSG_REPORT_COPIED = "  成功复制数：         {copied}"
MSG_REPORT_MISSING = "  源文件缺失数：       {missing}"
MSG_REPORT_SKIPPED = "  跳过数（已存在）：   {skipped}"
MSG_REPORT_FAILED = "  失败数：             {failed}"

BC_SUFFIX = ".bc!"

# ---------------------------------------------------------------------------
# Ctrl+Q 轮询检测（msvcrt）
# ---------------------------------------------------------------------------
HAS_MSVCRT = False
try:
    import msvcrt

    HAS_MSVCRT = True
except ImportError:
    pass  # 非 Windows 环境，不使用键盘检测


def check_quit_key() -> bool:
    """检测是否有 Ctrl+Q (ASCII 17) 按下，返回 True 表示需要退出。"""
    if not HAS_MSVCRT:
        return False
    while msvcrt.kbhit():
        ch = msvcrt.getch()
        if ch == b"\x11":  # Ctrl+Q 的 ASCII 码
            print(MSG_QUIT_KEY)
            return True
    return False


# ---------------------------------------------------------------------------
# 输入清理
# ---------------------------------------------------------------------------
def clean_path(raw: str) -> str:
    """去除首尾空格及可能存在的引号（单引号、双引号）。"""
    s = raw.strip()
    if len(s) >= 2:
        if (s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'"):
            s = s[1:-1]
    return s


def prompt_path(msg: str, default: str) -> Path:
    """提示用户输入路径，回车使用默认值；返回 Path 对象。"""
    user_input = input(msg)
    cleaned = clean_path(user_input)
    if not cleaned:
        cleaned = default
    return Path(cleaned)


# ---------------------------------------------------------------------------
# 辅助函数
# ---------------------------------------------------------------------------
def collect_bc_files(root: Path) -> list[Path]:
    """递归收集 root 下所有 .bc! 文件，返回按路径排序的列表。"""
    result: list[Path] = []
    for entry in root.rglob("*"):
        if entry.is_file() and entry.name.endswith(BC_SUFFIX):
            result.append(entry)
    result.sort()
    return result


def strip_bc_suffix(filename: str) -> str:
    """去掉文件名尾部的 .bc! 后缀。例: 'xxx.mp4.bc!' -> 'xxx.mp4'。"""
    if filename.endswith(BC_SUFFIX):
        return filename[: -len(BC_SUFFIX)]
    return filename  # 防御：不含后缀时原样返回


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------
def main() -> None:
    # --- 0. 启动横幅 ---
    print(MSG_BANNER)
    print(MSG_TITLE)
    print(MSG_BANNER)
    print()

    # --- 1. 获取源 / 目标路径 ---
    src_path = prompt_path(MSG_SRC_PROMPT, "d:\\Studios\\Folders\\Ins\\")
    dst_path = prompt_path(MSG_DST_PROMPT, "d:\\Studios\\Folders\\Outs\\")

    # --- 2. 校验路径 ---
    if not src_path.exists() or not src_path.is_dir():
        print(MSG_SRC_NOT_FOUND.format(path=src_path))
        sys.exit(1)
    if not dst_path.exists() or not dst_path.is_dir():
        print(MSG_DST_NOT_FOUND.format(path=dst_path))
        sys.exit(1)

    # 规整化为绝对路径
    src_path = src_path.resolve()
    dst_path = dst_path.resolve()

    print()
    print(MSG_DIVIDER)

    # --- 3. 收集所有 .bc! 文件 ---
    bc_files = collect_bc_files(dst_path)

    if not bc_files:
        print(MSG_NO_BC_FILES)
        sys.exit(0)

    print(MSG_FOUND_BC_COUNT.format(count=len(bc_files)))
    print(MSG_START_PROCESS)
    print(MSG_DIVIDER)

    # --- 4. 统计变量 ---
    copied = 0
    missing = 0
    skipped = 0
    failed = 0
    quit_requested = False

    # --- 5. 遍历处理 ---
    for bc_file in bc_files:
        # 每轮检测 Ctrl+Q
        if check_quit_key():
            print(MSG_QUIT_EARLY)
            quit_requested = True
            break

        # 去 .bc! 后缀得到目标文件名
        target_filename = strip_bc_suffix(bc_file.name)

        # 计算相对路径层级，在源文件夹中定位对应源文件
        relative_dir = bc_file.relative_to(dst_path).parent
        src_file = src_path / relative_dir / target_filename

        # 目标输出位置（.bc! 文件同目录下）
        dst_file = bc_file.parent / target_filename

        # 进度提示
        print(f"\n[{bc_file.relative_to(dst_path)}]")

        # --- 5a. 源文件缺失 ---
        if not src_file.exists() or not src_file.is_file():
            print(MSG_MISSING.format(src=src_file))
            missing += 1
            continue

        # --- 5b. 覆盖询问 ---
        was_overwrite = False  # 用于区分 [覆盖] vs [复制] 消息
        if dst_file.exists():
            choice = ask_overwrite(dst_file)
            if choice is None:
                # 用户按 Ctrl+Q 或被 EOF/KeyboardInterrupt 中断
                print(MSG_QUIT_EARLY)
                quit_requested = True
                break
            if choice == "n":
                print(MSG_SKIPPED.format(dst=dst_file))
                skipped += 1
                continue
            # choice == "y" → 继续复制
            was_overwrite = True

        # --- 5c. 执行复制 ---
        try:
            shutil.copy2(src_file, dst_file)
            if was_overwrite:
                print(MSG_OVERWRITTEN.format(src=src_file, dst=dst_file))
            else:
                print(MSG_COPIED.format(src=src_file, dst=dst_file))
            copied += 1
        except Exception as exc:
            print(MSG_FAILED.format(src=src_file, dst=dst_file, error=exc))
            failed += 1

    # --- 6. 统计报告 ---
    print()
    print(MSG_BANNER)
    print(MSG_REPORT_TITLE)
    print(MSG_BANNER)
    print(MSG_REPORT_TOTAL.format(total=len(bc_files)))
    print(MSG_REPORT_COPIED.format(copied=copied))
    print(MSG_REPORT_MISSING.format(missing=missing))
    print(MSG_REPORT_SKIPPED.format(skipped=skipped))
    print(MSG_REPORT_FAILED.format(failed=failed))
    if quit_requested:
        print(f"  （处理被中断，共 {len(bc_files)} 个文件，以上为已处理部分）")
    print(MSG_BANNER)


def ask_overwrite(dst_file: Path) -> str | None:
    """询问用户是否覆盖已存在的目标文件。

    返回 'y'（覆盖）、'n'（跳过）、'q'（退出整个脚本），
    若用户按 Ctrl+Q 或异常中断则返回 None。
    """
    while True:
        if check_quit_key():
            return None
        try:
            choice = input(MSG_OVERWRITE_PROMPT.format(dst=dst_file)).strip().lower()
        except (EOFError, KeyboardInterrupt):
            return None

        if choice in ("y", "n", "q"):
            return choice
        print(MSG_INVALID_CHOICE)


# ---------------------------------------------------------------------------
# 入口
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    main()
