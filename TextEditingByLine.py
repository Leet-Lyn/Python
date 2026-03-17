# 请帮我写个中文的 Python 脚本，批注也是中文：
# 有图形界面。
# 作用是让我针对文本，依次处理每一行。
# 界面上方有文本输入框（占上部 1/2）。其右侧有两个按钮：上面是粘贴（快捷键 Ctrl+V，作用是将剪贴板粘贴到文本框内）；下面是复制（快捷键 Ctrl+C，作用是将文本框内内容复制到剪贴板）。下面是撤销（快捷键 Ctrl+Z，作用是撤销上一次的操作）。下面的操作均是针对文本框内的文字操作的。
# 下面以标签呈现，实现功能。
# 1. 第一个标签，是块处理。
# 定义单元：通过文本框询问我单元前导符号与单元后导符号（默认为“[”与“]”），则一个“[内容]”为一个单元（包括[]）。
# 定义第几单元：通过文本框询问我选择第几个单元。（设置为正数为正向，负数为逆向，-2表示倒数第2个单元。）
# 下面是三个按钮：单元移动、单元删除、单元复制（纵向排布）。
# “单元移动”按钮：通过单选框，询问我单元需要向前移动、向后移动、移到最前、移到最后。向前移动、向后移动后通过文本框询问我移动几个单位（不是字符，而是方括号“[]”包绕到字符）。按“单元移动”按钮，将文本输入框的文本，以行为单位，将定义的第几单元，按照设置，进行移动。
# “单元删除”按钮，按“单元删除”按钮，将文本输入框的文本，以行为单位，将定义的第几单元，进行删除。
# “单元复制”按钮，通过文本框询问我在定义的第几单元，几个单位后复制。（设置为正数为正向，负数为逆向，1表示后面复制；-1表示前面复制，2表示后面间隔1个单位复制；-2表示前面间隔1个单元复制，0表示最前面复制；-0表示最后面复制。）按“单元复制”按钮，将文本输入框的文本，以行为单位，将定义的第几单元，按照设置，进行复制。
# 2. 第二个标签，是字符处理。
# 下面是三个按钮：字符添加、字符删除、字符替换（纵向排布）。
# “字符添加”按钮，通过文本框询问我在每一行到第几个位置后添加？通过文本框询问我添加什么字符。按“字符添加”按钮，将文本输入框的文本，以行为单位，在每一行到第几个位置，添加字符。
# “字符删除”按钮，通过文本框询问我删除什么字符。通过文本框询问我每行删除几次（删除几次后该行再出现这个字符就不删除，但每行都执行）。按“字符添加”按钮，将文本输入框的文本，以行为单位，进行删除（每行受次数限制）。
# “字符替换”按钮，通过文本框询问我查找什么字符、替换为什么字符。通过文本框询问我每行替换几次（删除几次后该行再出现这个字符就不替换，但每行都执行）。按“字符替换”按钮，将文本输入框的文本，以行为单位，进行查找替换（每行受次数限制）。
# 3. 第三个标签，是时间处理。
# 依次处理每一行。
# 通过单选框，询问我日期格式为何种类型的？原形式可以为：y-m-d、d-m-y、m-d-y。
# 通过单选框，询问我 m 的格式是什么（m、mm、mmm、mmmm）？。可为 1 位（m 如 1~12）或 2 位（mm 如 01~12）或 3 位（mmm 如 Jan~Dec），或多位（mmmm 如 January~December）。
# 通过单选框，询问我 d 的格式是什么（d、dd）？。可为 1 位（d 如 1~31）或 2 位（dd 如 01~31），
# 通过单选框，询问我间隔是什么？短横（-）、斜杠（/）或（\）、半角点（.）、半角逗号（,）、半角空格（ ）、半角空格逗号（ ,），或者没有间隔。
# 底部有个“修改”按钮，按“修改”按钮，将文本输入框的文本里的时间格式统一改为：yyyy-mm-dd。
# 4. 第四个标签，是标准化处理。
# “标准化”按钮，按“标准化”按钮，将文本输入框的文本格式化。要求：1. 繁体汉字转简体汉字。2. 汉字、英文单词、数字，彼此之间有空格。3. 汉字后标点符号转换为全角符号，英文后标点符号转换为半角符号。

# 导入模块
import sys
import re
from datetime import datetime

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QTabWidget, QGroupBox, QRadioButton,
    QButtonGroup, QLabel, QLineEdit, QGridLayout, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QShortcut, QKeySequence

import pyperclip
from opencc import OpenCC

# ================== 核心功能函数 ==================
cc = OpenCC('t2s')

def to_fullwidth(char):
    mapping = {',': '，', '.': '。', '!': '！', '?': '？'}
    return mapping.get(char, char)

def to_halfwidth(char):
    mapping = {'，': ',', '。': '.', '！': '!', '？': '?'}
    return mapping.get(char, char)

def format_text(text):
    text = cc.convert(text)
    text = re.sub(r'([\u4e00-\u9fa5])([a-zA-Z0-9])', r'\1 \2', text)
    text = re.sub(r'([a-zA-Z0-9])([\u4e00-\u9fa5])', r'\1 \2', text)
    text = re.sub(r'([\u4e00-\u9fa5])([,.!?])', lambda m: f"{m.group(1)}{to_fullwidth(m.group(2))}", text)
    text = re.sub(r'([a-zA-Z0-9])([，。！？])', lambda m: f"{m.group(1)}{to_halfwidth(m.group(2))}", text)
    return text

def format_date(text, date_format_type, month_format, day_format, separator):
    month_map = {
        'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
        'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12,
        'january': 1, 'february': 2, 'march': 3, 'april': 4,
        'may': 5, 'june': 6, 'july': 7, 'august': 8,
        'september': 9, 'october': 10, 'november': 11, 'december': 12
    }
    if separator == '没有间隔':
        sep_regex = ''
    elif separator == '半角空格':
        sep_regex = r'\s+'
    elif separator == '半角空格逗号':
        sep_regex = r'\s*,\s*'
    else:
        sep_regex = re.escape(separator)
    pattern = f'(\\d+){sep_regex}(\\d+|\\w+){sep_regex}(\\d+)'

    def replace_date(match):
        if date_format_type == 'y-m-d':
            year, month, day = match.group(1), match.group(2), match.group(3)
        elif date_format_type == 'd-m-y':
            day, month, year = match.group(1), match.group(2), match.group(3)
        else:  # m-d-y
            month, day, year = match.group(1), match.group(2), match.group(3)

        if month.isdigit():
            month_num = int(month)
        else:
            month_num = month_map.get(month.lower(), 1)

        if len(year) == 2:
            if int(year) >= 50:
                year = '19' + year
            else:
                year = '20' + year

        return f'{year}-{str(month_num).zfill(2)}-{str(int(day)).zfill(2)}'

    return re.sub(pattern, replace_date, text, flags=re.IGNORECASE)

# ----- 字符处理 -----
def add_string_to_lines(lines, position, string_to_add):
    new_lines = []
    for line in lines:
        if position == 0:
            new_lines.append(string_to_add + line)
        elif position > 0:
            if position >= len(line):
                new_lines.append(line + string_to_add)
            else:
                new_lines.append(line[:position] + string_to_add + line[position:])
        else:
            m = -position
            insert_pos = max(0, len(line) - m)
            new_lines.append(line[:insert_pos] + string_to_add + line[insert_pos:])
    return new_lines

def delete_string_from_lines(lines, string_to_delete, times_per_line):
    new_lines = []
    for line in lines:
        if times_per_line >= 0:
            new_line = line
            count = 0
            start = 0
            while count < times_per_line:
                idx = new_line.find(string_to_delete, start)
                if idx == -1:
                    break
                new_line = new_line[:idx] + new_line[idx + len(string_to_delete):]
                count += 1
                start = idx
            new_lines.append(new_line)
        else:
            rev_line = line[::-1]
            rev_string = string_to_delete[::-1]
            rev_times = -times_per_line
            new_rev_line = rev_line
            count = 0
            start = 0
            while count < rev_times:
                idx = new_rev_line.find(rev_string, start)
                if idx == -1:
                    break
                new_rev_line = new_rev_line[:idx] + new_rev_line[idx + len(rev_string):]
                count += 1
                start = idx
            new_lines.append(new_rev_line[::-1])
    return new_lines

def replace_string_in_lines(lines, old, new, times_per_line):
    new_lines = []
    for line in lines:
        if times_per_line >= 0:
            new_line = line
            count = 0
            start = 0
            while count < times_per_line:
                idx = new_line.find(old, start)
                if idx == -1:
                    break
                new_line = new_line[:idx] + new + new_line[idx + len(old):]
                count += 1
                start = idx + len(new)
            new_lines.append(new_line)
        else:
            rev_line = line[::-1]
            rev_old = old[::-1]
            rev_new = new[::-1]
            rev_times = -times_per_line
            new_rev_line = rev_line
            count = 0
            start = 0
            while count < rev_times:
                idx = new_rev_line.find(rev_old, start)
                if idx == -1:
                    break
                new_rev_line = new_rev_line[:idx] + rev_new + new_rev_line[idx + len(rev_old):]
                count += 1
                start = idx + len(rev_new)
            new_lines.append(new_rev_line[::-1])
    return new_lines

# ----- 块处理 -----
def extract_units(line, left_delim, right_delim):
    pattern = re.escape(left_delim) + r'.*?' + re.escape(right_delim)
    return re.findall(pattern, line)

def reconstruct_line_from_units(original_line, new_units, left_delim, right_delim):
    pattern = '(' + re.escape(left_delim) + r'.*?' + re.escape(right_delim) + ')'
    parts = re.split(pattern, original_line)
    result = []
    unit_idx = 0
    for part in parts:
        if re.match(pattern, part):
            if unit_idx < len(new_units):
                result.append(new_units[unit_idx])
                unit_idx += 1
        else:
            result.append(part)
    return ''.join(result)

def move_unit(units, index, move_type, count=0):
    units = units.copy()
    unit = units.pop(index)
    if move_type == '向前移动':
        units.insert(max(0, index - count), unit)
    elif move_type == '向后移动':
        units.insert(min(len(units), index + count), unit)
    elif move_type == '移到最前':
        units.insert(0, unit)
    elif move_type == '移到最后':
        units.append(unit)
    return units

def delete_unit(units, index):
    units = units.copy()
    units.pop(index)
    return units

def copy_unit(units, index, offset):
    units = units.copy()
    unit = units[index]
    if offset == 0:
        units.insert(0, unit)
    elif offset == 'last':  # -0
        units.append(unit)
    elif offset > 0:
        pos = min(index + offset + 1, len(units))
        units.insert(pos, unit)
    else:  # offset < 0
        pos = max(index + offset, 0)
        units.insert(pos, unit)
    return units


# ================== PySide6 主窗口 ==================

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("文本行处理工具")
        self.resize(1000, 800)

        # 历史记录栈（最大20步）
        self.history = []
        self.max_history = 20

        # 中央控件
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)

        # ---------- 顶部：文本框（占1/3） + 右侧按钮（粘贴、复制、撤销）----------
        top_layout = QHBoxLayout()
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("在此输入或粘贴文本...")
        top_layout.addWidget(self.text_edit, stretch=1)

        btn_layout = QVBoxLayout()
        self.paste_btn = QPushButton("粘贴 (Ctrl+V)")
        self.copy_btn = QPushButton("复制 (Ctrl+C)")
        self.undo_btn = QPushButton("撤销 (Ctrl+Z)")

        self.paste_btn.clicked.connect(self.paste_text)
        self.copy_btn.clicked.connect(self.copy_text)
        self.undo_btn.clicked.connect(self.undo)

        btn_layout.addWidget(self.paste_btn)
        btn_layout.addWidget(self.copy_btn)
        btn_layout.addWidget(self.undo_btn)
        btn_layout.addStretch()  # 使按钮靠上，不留空白

        top_layout.addLayout(btn_layout)

        main_layout.addLayout(top_layout, stretch=1)  # 顶部占1份

        # 快捷键
        self.paste_shortcut = QShortcut(QKeySequence.StandardKey.Paste, self.text_edit, self.paste_text)
        self.copy_shortcut = QShortcut(QKeySequence.StandardKey.Copy, self.text_edit, self.copy_text)
        self.undo_shortcut = QShortcut(QKeySequence("Ctrl+Z"), self, self.undo)

        # ---------- 选项卡 ----------
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget, stretch=2)  # 选项卡占2份

        # 创建四个标签页
        self.block_tab = BlockTab(self)
        self.char_tab = CharTab(self)
        self.date_tab = DateTab(self)
        self.std_tab = StdTab(self)

        self.tab_widget.addTab(self.block_tab, "块处理")
        self.tab_widget.addTab(self.char_tab, "字符处理")
        self.tab_widget.addTab(self.date_tab, "时间处理")
        self.tab_widget.addTab(self.std_tab, "标准化")

    # ---------- 历史记录管理 ----------
    def push_history(self):
        current = self.text_edit.toPlainText()
        if not self.history or self.history[-1] != current:
            self.history.append(current)
            if len(self.history) > self.max_history:
                self.history.pop(0)

    def undo(self):
        if not self.history:
            QMessageBox.information(self, "撤销", "没有可撤销的操作")
            return
        last = self.history.pop()
        self.text_edit.setPlainText(last)

    # ---------- 剪贴板操作 ----------
    def paste_text(self):
        self.push_history()
        try:
            text = pyperclip.paste()
            self.text_edit.setPlainText(text)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"无法粘贴：{e}")

    def copy_text(self):
        try:
            text = self.text_edit.toPlainText()
            pyperclip.copy(text)
            QMessageBox.information(self, "提示", "已复制到剪贴板")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"无法复制：{e}")

    # ---------- 辅助函数 ----------
    def get_lines(self):
        content = self.text_edit.toPlainText()
        return content.split('\n'), content

    def update_text(self, new_lines):
        self.text_edit.setPlainText('\n'.join(new_lines))


# ================== 各标签页 ==================

class BlockTab(QWidget):
    """块处理标签页"""
    def __init__(self, main_window):
        super().__init__()
        self.main = main_window
        layout = QVBoxLayout(self)

        # 定界符
        delim_group = QGroupBox("单元定界符")
        delim_layout = QHBoxLayout(delim_group)
        delim_layout.addWidget(QLabel("前导符号："))
        self.left_delim = QLineEdit("[")
        self.left_delim.setMaximumWidth(50)
        delim_layout.addWidget(self.left_delim)
        delim_layout.addWidget(QLabel("后导符号："))
        self.right_delim = QLineEdit("]")
        self.right_delim.setMaximumWidth(50)
        delim_layout.addWidget(self.right_delim)
        delim_layout.addStretch()
        layout.addWidget(delim_group)

        # 单元索引
        idx_group = QGroupBox("选择单元")
        idx_layout = QHBoxLayout(idx_group)
        idx_layout.addWidget(QLabel("第几个单元（正数正向，负数逆向，如-2倒数第2个）："))
        self.block_index = QLineEdit("1")
        self.block_index.setMaximumWidth(80)
        idx_layout.addWidget(self.block_index)
        idx_layout.addStretch()
        layout.addWidget(idx_group)

        # 三个主操作按钮
        btn_layout = QHBoxLayout()
        self.move_btn = QPushButton("单元移动")
        self.delete_btn = QPushButton("单元删除")
        self.copy_btn = QPushButton("单元复制")
        btn_layout.addWidget(self.move_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.copy_btn)
        layout.addLayout(btn_layout)

        # 移动选项
        move_group = QGroupBox("移动选项")
        move_grid = QGridLayout(move_group)

        self.move_type = QButtonGroup(self)
        rb_forward = QRadioButton("向前移动")
        rb_backward = QRadioButton("向后移动")
        rb_first = QRadioButton("移到最前")
        rb_last = QRadioButton("移到最后")
        self.move_type.addButton(rb_forward, 1)
        self.move_type.addButton(rb_backward, 2)
        self.move_type.addButton(rb_first, 3)
        self.move_type.addButton(rb_last, 4)
        rb_forward.setChecked(True)

        move_grid.addWidget(rb_forward, 0, 0)
        move_grid.addWidget(rb_backward, 0, 1)
        move_grid.addWidget(rb_first, 0, 2)
        move_grid.addWidget(rb_last, 0, 3)

        move_grid.addWidget(QLabel("移动几个单位（仅向前/向后有效）："), 1, 0)
        self.move_count = QLineEdit("1")
        self.move_count.setMaximumWidth(80)
        move_grid.addWidget(self.move_count, 1, 1)

        layout.addWidget(move_group)

        # 复制选项
        copy_group = QGroupBox("复制选项")
        copy_layout = QHBoxLayout(copy_group)
        copy_layout.addWidget(QLabel("复制偏移（正数后移，负数前移，0最前，-0最后）："))
        self.copy_offset = QLineEdit("1")
        self.copy_offset.setMaximumWidth(80)
        copy_layout.addWidget(self.copy_offset)
        copy_layout.addStretch()
        layout.addWidget(copy_group)

        layout.addStretch()

        # 连接信号
        self.move_btn.clicked.connect(self.block_move)
        self.delete_btn.clicked.connect(self.block_delete)
        self.copy_btn.clicked.connect(self.block_copy)

    # 操作执行（略，与之前相同，但需调用 self.main.push_history()）
    def block_move(self):
        self.main.push_history()
        lines, _ = self.main.get_lines()
        left = self.left_delim.text()
        right = self.right_delim.text()
        try:
            idx_raw = int(self.block_index.text())
        except ValueError:
            QMessageBox.critical(self, "错误", "单元索引必须是整数")
            return

        move_type_map = {1: '向前移动', 2: '向后移动', 3: '移到最前', 4: '移到最后'}
        move_type = move_type_map.get(self.move_type.checkedId())
        count = 0
        if move_type in ('向前移动', '向后移动'):
            try:
                count = int(self.move_count.text())
            except ValueError:
                QMessageBox.critical(self, "错误", "移动次数必须是整数")
                return

        new_lines = []
        for line in lines:
            units = extract_units(line, left, right)
            if not units:
                new_lines.append(line)
                continue
            n = len(units)
            if idx_raw > 0:
                actual = idx_raw - 1
            elif idx_raw < 0:
                actual = n + idx_raw
            else:
                QMessageBox.critical(self, "错误", "单元索引不能为0")
                return
            if actual < 0 or actual >= n:
                QMessageBox.critical(self, "错误", f"索引 {idx_raw} 超出范围（该行有{n}个单元）")
                return
            new_units = move_unit(units, actual, move_type, count)
            new_lines.append(reconstruct_line_from_units(line, new_units, left, right))
        self.main.update_text(new_lines)

    def block_delete(self):
        self.main.push_history()
        lines, _ = self.main.get_lines()
        left = self.left_delim.text()
        right = self.right_delim.text()
        try:
            idx_raw = int(self.block_index.text())
        except ValueError:
            QMessageBox.critical(self, "错误", "单元索引必须是整数")
            return

        new_lines = []
        for line in lines:
            units = extract_units(line, left, right)
            if not units:
                new_lines.append(line)
                continue
            n = len(units)
            if idx_raw > 0:
                actual = idx_raw - 1
            elif idx_raw < 0:
                actual = n + idx_raw
            else:
                QMessageBox.critical(self, "错误", "单元索引不能为0")
                return
            if actual < 0 or actual >= n:
                QMessageBox.critical(self, "错误", f"索引 {idx_raw} 超出范围（该行有{n}个单元）")
                return
            new_units = delete_unit(units, actual)
            new_lines.append(reconstruct_line_from_units(line, new_units, left, right))
        self.main.update_text(new_lines)

    def block_copy(self):
        self.main.push_history()
        lines, _ = self.main.get_lines()
        left = self.left_delim.text()
        right = self.right_delim.text()
        try:
            idx_raw = int(self.block_index.text())
        except ValueError:
            QMessageBox.critical(self, "错误", "单元索引必须是整数")
            return
        offset_str = self.copy_offset.text().strip()
        if offset_str == '-0':
            offset = 'last'
        else:
            try:
                offset = int(offset_str)
            except ValueError:
                QMessageBox.critical(self, "错误", "复制偏移必须是整数或-0")
                return

        new_lines = []
        for line in lines:
            units = extract_units(line, left, right)
            if not units:
                new_lines.append(line)
                continue
            n = len(units)
            if idx_raw > 0:
                actual = idx_raw - 1
            elif idx_raw < 0:
                actual = n + idx_raw
            else:
                QMessageBox.critical(self, "错误", "单元索引不能为0")
                return
            if actual < 0 or actual >= n:
                QMessageBox.critical(self, "错误", f"索引 {idx_raw} 超出范围（该行有{n}个单元）")
                return
            new_units = copy_unit(units, actual, offset)
            new_lines.append(reconstruct_line_from_units(line, new_units, left, right))
        self.main.update_text(new_lines)


class CharTab(QWidget):
    """字符处理标签页"""
    def __init__(self, main_window):
        super().__init__()
        self.main = main_window
        layout = QVBoxLayout(self)

        # 添加
        add_group = QGroupBox("字符添加")
        add_layout = QGridLayout(add_group)
        add_layout.addWidget(QLabel("位置（0最前，正数后，负数倒数前）："), 0, 0)
        self.add_pos = QLineEdit("0")
        add_layout.addWidget(self.add_pos, 0, 1)
        add_layout.addWidget(QLabel("添加字符："), 1, 0)
        self.add_char = QLineEdit()
        add_layout.addWidget(self.add_char, 1, 1)
        self.add_btn = QPushButton("执行添加")
        add_layout.addWidget(self.add_btn, 2, 0, 1, 2)
        layout.addWidget(add_group)

        # 删除
        del_group = QGroupBox("字符删除")
        del_layout = QGridLayout(del_group)
        del_layout.addWidget(QLabel("删除字符："), 0, 0)
        self.del_char = QLineEdit()
        del_layout.addWidget(self.del_char, 0, 1)
        del_layout.addWidget(QLabel("每行删除次数（正数正向，负数逆向）："), 1, 0)
        self.del_times = QLineEdit("1")
        del_layout.addWidget(self.del_times, 1, 1)
        self.del_btn = QPushButton("执行删除")
        del_layout.addWidget(self.del_btn, 2, 0, 1, 2)
        layout.addWidget(del_group)

        # 替换
        rep_group = QGroupBox("字符替换")
        rep_layout = QGridLayout(rep_group)
        rep_layout.addWidget(QLabel("查找字符："), 0, 0)
        self.rep_old = QLineEdit()
        rep_layout.addWidget(self.rep_old, 0, 1)
        rep_layout.addWidget(QLabel("替换为："), 1, 0)
        self.rep_new = QLineEdit()
        rep_layout.addWidget(self.rep_new, 1, 1)
        rep_layout.addWidget(QLabel("每行替换次数（正数正向，负数逆向）："), 2, 0)
        self.rep_times = QLineEdit("1")
        rep_layout.addWidget(self.rep_times, 2, 1)
        self.rep_btn = QPushButton("执行替换")
        rep_layout.addWidget(self.rep_btn, 3, 0, 1, 2)
        layout.addWidget(rep_group)

        layout.addStretch()

        self.add_btn.clicked.connect(self.char_add)
        self.del_btn.clicked.connect(self.char_delete)
        self.rep_btn.clicked.connect(self.char_replace)

    def char_add(self):
        self.main.push_history()
        lines, _ = self.main.get_lines()
        try:
            pos = int(self.add_pos.text())
        except ValueError:
            QMessageBox.critical(self, "错误", "位置必须是整数")
            return
        char = self.add_char.text()
        if not char:
            QMessageBox.critical(self, "错误", "请输入要添加的字符")
            return
        new_lines = add_string_to_lines(lines, pos, char)
        self.main.update_text(new_lines)

    def char_delete(self):
        self.main.push_history()
        lines, _ = self.main.get_lines()
        char = self.del_char.text()
        if not char:
            QMessageBox.critical(self, "错误", "请输入要删除的字符")
            return
        try:
            times = int(self.del_times.text())
        except ValueError:
            QMessageBox.critical(self, "错误", "次数必须是整数")
            return
        new_lines = delete_string_from_lines(lines, char, times)
        self.main.update_text(new_lines)

    def char_replace(self):
        self.main.push_history()
        lines, _ = self.main.get_lines()
        old = self.rep_old.text()
        new = self.rep_new.text()
        if not old:
            QMessageBox.critical(self, "错误", "请输入查找字符")
            return
        try:
            times = int(self.rep_times.text())
        except ValueError:
            QMessageBox.critical(self, "错误", "次数必须是整数")
            return
        new_lines = replace_string_in_lines(lines, old, new, times)
        self.main.update_text(new_lines)


class DateTab(QWidget):
    """时间处理标签页"""
    def __init__(self, main_window):
        super().__init__()
        self.main = main_window
        layout = QVBoxLayout(self)

        type_group = QGroupBox("原日期格式")
        type_layout = QHBoxLayout(type_group)
        self.date_type = QButtonGroup(self)
        rb_ymd = QRadioButton("年-月-日 (y-m-d)")
        rb_dmy = QRadioButton("日-月-年 (d-m-y)")
        rb_mdy = QRadioButton("月-日-年 (m-d-y)")
        self.date_type.addButton(rb_ymd, 1)
        self.date_type.addButton(rb_dmy, 2)
        self.date_type.addButton(rb_mdy, 3)
        rb_ymd.setChecked(True)
        type_layout.addWidget(rb_ymd)
        type_layout.addWidget(rb_dmy)
        type_layout.addWidget(rb_mdy)
        layout.addWidget(type_group)

        month_group = QGroupBox("月份格式")
        month_layout = QHBoxLayout(month_group)
        self.month_format = QButtonGroup(self)
        rb_m = QRadioButton("m (1-12)")
        rb_mm = QRadioButton("mm (01-12)")
        rb_mmm = QRadioButton("mmm (Jan-Dec)")
        rb_mmmm = QRadioButton("mmmm (January-December)")
        self.month_format.addButton(rb_m, 1)
        self.month_format.addButton(rb_mm, 2)
        self.month_format.addButton(rb_mmm, 3)
        self.month_format.addButton(rb_mmmm, 4)
        rb_m.setChecked(True)
        month_layout.addWidget(rb_m)
        month_layout.addWidget(rb_mm)
        month_layout.addWidget(rb_mmm)
        month_layout.addWidget(rb_mmmm)
        layout.addWidget(month_group)

        day_group = QGroupBox("日期格式")
        day_layout = QHBoxLayout(day_group)
        self.day_format = QButtonGroup(self)
        rb_d = QRadioButton("d (1-31)")
        rb_dd = QRadioButton("dd (01-31)")
        self.day_format.addButton(rb_d, 1)
        self.day_format.addButton(rb_dd, 2)
        rb_d.setChecked(True)
        day_layout.addWidget(rb_d)
        day_layout.addWidget(rb_dd)
        layout.addWidget(day_group)

        sep_group = QGroupBox("间隔符")
        sep_grid = QGridLayout(sep_group)
        self.separator = QButtonGroup(self)
        self.sep_vals = [
            ("-", "短横 -"),
            ("/", "斜杠 /"),
            ("\\", "反斜杠 \\"),
            (".", "半角点 ."),
            (",", "半角逗号 ,"),
            ("半角空格", "半角空格"),
            ("半角空格逗号", "半角空格逗号"),
            ("没有间隔", "没有间隔")
        ]
        for i, (val, lbl) in enumerate(self.sep_vals):
            rb = QRadioButton(lbl)
            self.separator.addButton(rb, i)
            sep_grid.addWidget(rb, i // 3, i % 3)
        self.separator.buttons()[0].setChecked(True)
        layout.addWidget(sep_group)

        self.convert_btn = QPushButton("修改日期格式")
        layout.addWidget(self.convert_btn)
        layout.addStretch()

        self.convert_btn.clicked.connect(self.date_convert)

    def date_convert(self):
        self.main.push_history()
        _, text = self.main.get_lines()
        type_map = {1: 'y-m-d', 2: 'd-m-y', 3: 'm-d-y'}
        date_type = type_map.get(self.date_type.checkedId(), 'y-m-d')
        month_map = {1: 'm', 2: 'mm', 3: 'mmm', 4: 'mmmm'}
        month_fmt = month_map.get(self.month_format.checkedId(), 'm')
        day_map = {1: 'd', 2: 'dd'}
        day_fmt = day_map.get(self.day_format.checkedId(), 'd')
        sep_idx = self.separator.checkedId()
        sep = self.sep_vals[sep_idx][0] if 0 <= sep_idx < len(self.sep_vals) else '-'

        try:
            new_text = format_date(text, date_type, month_fmt, day_fmt, sep)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"日期转换失败：{e}")
            return
        self.main.text_edit.setPlainText(new_text)


class StdTab(QWidget):
    """标准化标签页"""
    def __init__(self, main_window):
        super().__init__()
        self.main = main_window
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("点击下方按钮对文本框内容进行标准化处理"))
        self.std_btn = QPushButton("标准化")
        layout.addWidget(self.std_btn)
        layout.addStretch()
        self.std_btn.clicked.connect(self.standardize)

    def standardize(self):
        self.main.push_history()
        _, text = self.main.get_lines()
        try:
            new_text = format_text(text)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"标准化失败：{e}")
            return
        self.main.text_edit.setPlainText(new_text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())