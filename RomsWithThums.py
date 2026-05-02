# 请帮我写个中文的 Python 脚本，批注也是中文：
# 询问我复制还是删除。
# 选择复制，则询问源文件路径，提取出文件名（不包括扩展名）；询问源文件夹（默认：d:\Works\Ins\）与目标文件夹（默认：d:\Works\Outs\）。根据源文件名（不包括扩展名），找出源文件夹里所有同名文件（扩展名可以不同），连同其父文件夹复制到目标文件夹中。
# 选择删除，则询问源文件路径，提取出文件名（不包括扩展名）；询问源文件夹（默认：d:\Works\Ins\）。删除源文件，同时 根据源文件名（不包括扩展名），找出源文件夹里所有同名文件（扩展名可以不同），一并删除。
# 完成后，询问我复制还是删除。

# 导入模块
import shutil
from pathlib import Path
from typing import List

def get_stem_from_file(file_path: str) -> str:
    """
    从完整文件路径中提取文件名主名（不含扩展名）
    例如：C:\test\example.txt -> "example"
    """
    return Path(file_path).stem

def find_files_by_stem(root_dir: Path, stem: str) -> List[Path]:
    """
    在 root_dir 目录下递归查找所有文件名主名等于 stem 的文件
    返回匹配文件的 Path 列表
    """
    matches = []
    # rglob 递归遍历所有文件
    for file_path in root_dir.rglob("*"):
        if file_path.is_file() and file_path.stem == stem:
            matches.append(file_path)
    return matches

def copy_file_with_parents(src: Path, dst_root: Path, src_root: Path) -> bool:
    """
    将 src 文件复制到 dst_root 下，并保留相对于 src_root 的目录结构
    例如：src_root = d:\Works\Ins，src = d:\Works\Ins\sub\file.txt
          dst_root = d:\Works\Outs
          复制后得到 d:\Works\Outs\sub\file.txt
    返回是否复制成功
    """
    try:
        # 计算相对路径
        relative_path = src.relative_to(src_root)
        # 目标完整路径
        dst_path = dst_root / relative_path
        # 创建目标父目录
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        # 复制文件（保留元数据）
        shutil.copy2(src, dst_path)
        print(f"  已复制: {src} -> {dst_path}")
        return True
    except Exception as e:
        print(f"  复制失败: {src}\n    错误: {e}")
        return False

def delete_files(file_paths: List[Path], confirm: bool = True) -> None:
    """
    删除给定的文件列表，可选择先确认
    """
    if not file_paths:
        print("  没有需要删除的文件。")
        return

    print("即将删除以下文件：")
    for f in file_paths:
        print(f"  {f}")

    if confirm:
        answer = input("确认删除以上所有文件吗？(y/n)：").strip().lower()
        if answer != 'y':
            print("已取消删除操作。")
            return

    for f in file_paths:
        try:
            f.unlink()
            print(f"  已删除: {f}")
        except Exception as e:
            print(f"  删除失败: {f}\n    错误: {e}")

def main():
    print("=== 同名文件（不同扩展名）批量处理工具 ===")

    while True:
        print("\n请选择操作：")
        print("  1 - 复制")
        print("  2 - 删除")
        print("  0 或 q - 退出")
        choice = input("请输入数字 (1/2/0)：").strip().lower()

        if choice in ('0', 'q', 'quit', 'exit'):
            print("程序结束。")
            break

        if choice == '1':
            # ---------- 复制模式 ----------
            # 1. 获取基准文件路径
            src_file_input = input("请输入源文件路径（用于提取文件名主名）：").strip()
            if not src_file_input:
                print("错误：未输入文件路径，操作取消。")
                continue
            src_file_path = Path(src_file_input)
            if not src_file_path.is_file():
                print(f"错误：文件不存在 -> {src_file_path}，操作取消。")
                continue

            stem = get_stem_from_file(src_file_input)
            print(f"提取的文件主名：{stem}")

            # 2. 源文件夹（默认 d:\Works\Ins\）
            src_root_input = input("请输入源文件夹（默认 d:\\Works\\Ins\\）：").strip()
            if not src_root_input:
                src_root = Path("d:\\Works\\Ins")
            else:
                src_root = Path(src_root_input)
            if not src_root.is_dir():
                print(f"错误：源文件夹不存在 -> {src_root}，操作取消。")
                continue

            # 3. 目标文件夹（默认 d:\Works\Outs\）
            dst_root_input = input("请输入目标文件夹（默认 d:\\Works\\Outs\\）：").strip()
            if not dst_root_input:
                dst_root = Path("d:\\Works\\Outs")
            else:
                dst_root = Path(dst_root_input)
            # 目标文件夹可以不存在，自动创建
            dst_root.mkdir(parents=True, exist_ok=True)

            # 4. 查找所有同名文件
            matched_files = find_files_by_stem(src_root, stem)
            if not matched_files:
                print(f"在源文件夹 {src_root} 中没有找到主名为 {stem} 的文件。")
                continue

            print(f"找到 {len(matched_files)} 个匹配的文件：")
            for f in matched_files:
                print(f"  {f}")

            confirm_copy = input("确认复制这些文件到目标文件夹吗？(y/n)：").strip().lower()
            if confirm_copy != 'y':
                print("复制操作已取消。")
                continue

            # 5. 执行复制
            success_count = 0
            for f in matched_files:
                if copy_file_with_parents(f, dst_root, src_root):
                    success_count += 1
            print(f"复制完成：成功 {success_count} / 总数 {len(matched_files)}")

        elif choice == '2':
            # ---------- 删除模式 ----------
            # 1. 获取基准文件路径（该文件本身也要删除）
            src_file_input = input("请输入源文件路径（用于提取文件名主名，该文件本身也会被删除）：").strip()
            if not src_file_input:
                print("错误：未输入文件路径，操作取消。")
                continue
            src_file_path = Path(src_file_input)
            if not src_file_path.is_file():
                print(f"错误：文件不存在 -> {src_file_path}，操作取消。")
                continue

            stem = get_stem_from_file(src_file_input)
            print(f"提取的文件主名：{stem}")

            # 2. 源文件夹（搜索同名文件的范围）
            src_root_input = input("请输入源文件夹（默认 d:\\Works\\Ins\\）：").strip()
            if not src_root_input:
                src_root = Path("d:\\Works\\Ins")
            else:
                src_root = Path(src_root_input)
            if not src_root.is_dir():
                print(f"错误：源文件夹不存在 -> {src_root}，操作取消。")
                continue

            # 3. 查找所有同名文件（包括指定的源文件本身吗？如果它在源文件夹内会重复，但不影响）
            matched_files = find_files_by_stem(src_root, stem)
            # 将用户指定的文件也加入删除列表（如果它不在源文件夹内也要删）
            if src_file_path not in matched_files:
                matched_files.append(src_file_path)

            # 去重（可能用户指定的文件就在源文件夹内，避免重复）
            matched_files = list(set(matched_files))

            if not matched_files:
                print(f"没有找到任何需要删除的文件（主名 {stem}）。")
                continue

            print(f"将要删除的文件（共 {len(matched_files)} 个）：")
            for f in matched_files:
                print(f"  {f}")

            confirm_del = input("确认永久删除以上所有文件吗？(y/n)：").strip().lower()
            if confirm_del != 'y':
                print("删除操作已取消。")
                continue

            # 4. 执行删除
            delete_files(matched_files, confirm=False)   # 已经二次确认，不再重复询问
            print("删除操作执行完毕。")

        else:
            print("无效输入，请输入 1、2 或 0 退出。")

if __name__ == "__main__":
    main()