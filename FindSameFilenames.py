# 文件去重工具。
# 模式 1 — 仅查找：列出源文件夹中重名的文件，不移动。
# 模式 2 — 查找并移动：移动文件到目标文件夹，重名文件跳过并记录。

import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path

# ==================== 全局配置 ====================

DEFAULT_SOURCE_DIR = Path(r"d:\Studios\Folders\Ins")
DEFAULT_TARGET_DIR = Path(r"d:\Studios\Folders\Outs")

# --- 消息常量 ---
MSG_TITLE = "=" * 50 + "\n文件去重工具\n" + "=" * 50
MSG_MODE_PROMPT = "\n请选择模式：\n  1. 仅查找重复文件名（默认）\n  2. 查找并移动（重名文件跳过）\n\n请输入 (1/2，默认1)："
MSG_MODE_INVALID = "无效选项，请重新输入。"
MSG_PROMPT_SOURCE = "请输入源文件夹位置（默认: d:\\Studios\\Folders\\Ins）："
MSG_PROMPT_TARGET = "请输入目标文件夹位置（默认: d:\\Studios\\Folders\\Outs）："
MSG_SOURCE_NOT_FOUND = "错误：源文件夹不存在 —— {}"
MSG_SOURCE_EMPTY = "源文件夹中没有文件或文件夹。"
MSG_FOUND_ITEMS = "找到 {} 个文件/文件夹，开始处理…"
MSG_PROGRESS = "[{}/{}] {}"
MSG_MOVED = "  已移动 -> {}"
MSG_SKIPPED = "  跳过（重名）: {}"
MSG_COMPLETE = "\n处理完成：移动 {} 个，跳过 {} 个。"
MSG_NO_DUP = "没有重名文件。"
MSG_DUP_HEADER = "\n===== 以下文件因文件名重复被跳过 ====="
MSG_CLIPBOARD_COPIED = "已复制到剪贴板。"
MSG_CLIPBOARD_FAIL = "复制到剪贴板失败：{}"
MSG_INTERRUPTED = "\n\n用户中断程序，已退出。"
MSG_ERROR = "\n程序运行出错: {}"
MSG_EXIT = "\n按回车键退出..."

# ==================== 剪贴板 ====================

def copy_to_clipboard(text: str) -> None:
    """文本 -> Windows 剪贴板。"""
    try:
        subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "Add-Type -AssemblyName System.Windows.Forms;"
             "[System.Windows.Forms.Clipboard]::SetText($Input)"],
            input=text,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            check=True,
        )
        print(MSG_CLIPBOARD_COPIED)
    except Exception:
        try:
            subprocess.run(
                ["clip.exe"],
                input=text,
                encoding="utf-8",
                errors="ignore",
                check=True,
            )
            print(MSG_CLIPBOARD_COPIED)
        except Exception as e:
            print(MSG_CLIPBOARD_FAIL.format(e))

# ==================== 模式 1：仅查找 ====================

def mode_find_only(source_dir: Path) -> None:
    """扫描源文件夹，找出所有重复文件名。"""
    name_counts: Counter[str] = Counter()
    name_paths: dict[str, list[Path]] = {}

    for p in source_dir.rglob("*"):
        if p.is_file():
            name = p.name
            name_counts[name] += 1
            name_paths.setdefault(name, []).append(p)

    if not name_counts:
        print(MSG_SOURCE_EMPTY)
        return

    total_files = sum(name_counts.values())
    print("找到 {} 个文件。".format(total_files))

    # 筛选出现次数 >= 2 的文件名
    duplicates = {name: paths for name, paths in name_paths.items() if name_counts[name] >= 2}
    dup_count = sum(len(paths) for paths in duplicates.values())

    if duplicates:
        header = "===== 重复文件名列表（共 {} 个文件名，{} 个文件）=====".format(
            len(duplicates), dup_count)
        print("\n" + header)
        lines: list[str] = [header]
        for name, paths in sorted(duplicates.items()):
            lines.append("\n[{}] 出现 {} 次：".format(name, len(paths)))
            for p in paths:
                line = "    {}".format(p)
                lines.append(line)
                print(line)
        dup_list = "\n".join(lines)
        copy_to_clipboard(dup_list)
    else:
        print(MSG_NO_DUP)

# ==================== 模式 2：查找并移动 ====================

def mode_find_and_move(source_dir: Path, target_dir: Path) -> None:
    """移动文件到目标文件夹，重名文件跳过并记录。"""
    # 收集源文件夹下所有文件
    all_items: list[Path] = []
    for p in source_dir.rglob("*"):
        if p.is_file():
            all_items.append(p)

    if not all_items:
        print(MSG_SOURCE_EMPTY)
        return

    all_items.sort(key=lambda p: len(p.relative_to(source_dir).parts))
    total = len(all_items)
    print(MSG_FOUND_ITEMS.format(total))

    moved_names: set[str] = set()
    skipped_paths: list[str] = []
    moved_count = 0
    skipped_count = 0

    for idx, src_path in enumerate(all_items, 1):
        name = src_path.name
        print(MSG_PROGRESS.format(idx, total, src_path.relative_to(source_dir)))

        if name in moved_names:
            skipped_paths.append(str(src_path))
            skipped_count += 1
            print(MSG_SKIPPED.format(name))
            continue

        rel = src_path.relative_to(source_dir)
        dst_path = target_dir / rel

        try:
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src_path), str(dst_path))
            moved_names.add(name)
            moved_count += 1
            print(MSG_MOVED.format(dst_path))
        except Exception as e:
            skipped_paths.append(str(src_path))
            skipped_count += 1
            print("  移动失败: {}".format(e))

    print(MSG_COMPLETE.format(moved_count, skipped_count))

    if skipped_paths:
        print(MSG_DUP_HEADER)
        dup_list = "\n".join(skipped_paths)
        print(dup_list)
        copy_to_clipboard(dup_list)
    else:
        print(MSG_NO_DUP)

# ==================== 主程序 ====================

def main() -> None:
    print(MSG_TITLE)

    while True:
        print()
        # 选择模式
        while True:
            raw = input(MSG_MODE_PROMPT).strip()
            if raw in ("", "1", "2"):
                mode = raw if raw else "1"
                break
            print(MSG_MODE_INVALID)

        print()
        raw = input(MSG_PROMPT_SOURCE).strip()
        source_dir = Path(raw) if raw else DEFAULT_SOURCE_DIR

        if not source_dir.is_dir():
            print(MSG_SOURCE_NOT_FOUND.format(source_dir))
            continue

        if mode == "1":
            mode_find_only(source_dir)
        else:
            raw = input(MSG_PROMPT_TARGET).strip()
            target_dir = Path(raw) if raw else DEFAULT_TARGET_DIR
            target_dir.mkdir(parents=True, exist_ok=True)
            mode_find_and_move(source_dir, target_dir)

# ==================== 程序入口 ====================

if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (OSError, AttributeError):
        pass
    try:
        main()
    except KeyboardInterrupt:
        print(MSG_INTERRUPTED)
    except Exception as e:
        print(MSG_ERROR.format(e))
    finally:
        input(MSG_EXIT)
