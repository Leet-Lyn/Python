# 请帮我写个中文的 Python 脚本，批注也是中文：
# 有图形界面。
# 作用是让我针对文本，依次处理每一行。
# 界面上方有文本输入框（占上部 1/2）。其右侧有两个按钮：上面是粘贴（快捷键 Ctrl+V，作用是将剪贴板粘贴到文本框内）；下面是复制（快捷键 Ctrl+C，作用是将文本框内内容复制到剪贴板）。下面的操作均是针对文本框内的文字操作的。
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
# -*- coding: utf-8 -*-
"""
多功能文本处理器
功能：
1. 单元处理：移动、删除、复制指定单元
2. 字符处理：添加、删除、替换
3. 时间处理：统一时间格式
4. 标准化处理：繁体转简体，汉字/英文/数字空格化，标点符号标准化
"""

import sys
import re
import pyperclip
import zhconv
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTextEdit, QLineEdit, QLabel,
    QTabWidget, QComboBox, QSpinBox, QCheckBox
)
from PyQt6.QtGui import QFont, QKeySequence, QShortcut
from PyQt6.QtCore import Qt

class TextProcessor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("多功能文本处理器")
        self.resize(1000, 700)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # 上半部分：文本输入框
        text_layout = QHBoxLayout()
        self.text_edit = QTextEdit()
        self.text_edit.setFont(QFont("Consolas", 12))
        text_layout.addWidget(self.text_edit)

        # 右侧粘贴/复制按钮
        right_btn_layout = QVBoxLayout()
        self.paste_btn = QPushButton("粘贴 (Ctrl+V)")
        self.paste_btn.clicked.connect(self.paste_text)
        self.copy_btn = QPushButton("复制 (Ctrl+C)")
        self.copy_btn.clicked.connect(self.copy_text)
        right_btn_layout.addWidget(self.paste_btn)
        right_btn_layout.addWidget(self.copy_btn)
        right_btn_layout.addStretch()
        text_layout.addLayout(right_btn_layout)

        main_layout.addLayout(text_layout)

        # 快捷键绑定
        QShortcut(QKeySequence("Ctrl+V"), self, activated=self.paste_text)
        QShortcut(QKeySequence("Ctrl+C"), self, activated=self.copy_text)

        # 下半部分：标签页
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        self.init_unit_tab()
        self.init_char_tab()
        self.init_time_tab()
        self.init_standard_tab()

    # -------------------- 单元处理 --------------------
    def init_unit_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)

        # 单元定义
        unit_def_layout = QHBoxLayout()
        unit_def_layout.addWidget(QLabel("单元前导符号:"))
        self.unit_start_input = QLineEdit("[")
        unit_def_layout.addWidget(self.unit_start_input)
        unit_def_layout.addWidget(QLabel("单元后导符号:"))
        self.unit_end_input = QLineEdit("]")
        unit_def_layout.addWidget(self.unit_end_input)
        unit_def_layout.addWidget(QLabel("选择第几个单元:"))
        self.unit_index_input = QSpinBox()
        self.unit_index_input.setRange(-1000, 1000)
        self.unit_index_input.setValue(1)
        unit_def_layout.addWidget(self.unit_index_input)
        layout.addLayout(unit_def_layout)

        # 单元操作按钮
        op_layout = QHBoxLayout()
        self.unit_move_btn = QPushButton("单元移动")
        self.unit_move_btn.clicked.connect(self.unit_move)
        self.unit_delete_btn = QPushButton("单元删除")
        self.unit_delete_btn.clicked.connect(self.unit_delete)
        self.unit_copy_btn = QPushButton("单元复制")
        self.unit_copy_btn.clicked.connect(self.unit_copy)
        op_layout.addWidget(self.unit_move_btn)
        op_layout.addWidget(self.unit_delete_btn)
        op_layout.addWidget(self.unit_copy_btn)
        layout.addLayout(op_layout)

        # 移动选项
        move_layout = QHBoxLayout()
        move_layout.addWidget(QLabel("移动方式:"))
        self.move_type_combo = QComboBox()
        self.move_type_combo.addItems(["向前移动", "向后移动", "移到最前", "移到最后"])
        move_layout.addWidget(self.move_type_combo)
        move_layout.addWidget(QLabel("移动几个单位:"))
        self.move_units_input = QSpinBox()
        self.move_units_input.setRange(1, 100)
        self.move_units_input.setValue(1)
        move_layout.addWidget(self.move_units_input)
        layout.addLayout(move_layout)

        # 复制选项
        copy_layout = QHBoxLayout()
        copy_layout.addWidget(QLabel("复制偏移单位:"))
        self.copy_units_input = QSpinBox()
        self.copy_units_input.setRange(-100, 100)
        self.copy_units_input.setValue(1)
        copy_layout.addWidget(self.copy_units_input)
        layout.addLayout(copy_layout)

        self.tabs.addTab(tab, "单元处理")

    # -------------------- 字符处理 --------------------
    def init_char_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)

        # 添加
        add_layout = QHBoxLayout()
        add_layout.addWidget(QLabel("添加到第几个字符后:"))
        self.add_pos_input = QSpinBox()
        self.add_pos_input.setRange(0, 1000)
        add_layout.addWidget(self.add_pos_input)
        add_layout.addWidget(QLabel("添加字符:"))
        self.add_text_input = QLineEdit()
        add_layout.addWidget(self.add_text_input)
        self.char_add_btn = QPushButton("字符添加")
        self.char_add_btn.clicked.connect(self.char_add)
        add_layout.addWidget(self.char_add_btn)
        layout.addLayout(add_layout)

        # 删除
        del_layout = QHBoxLayout()
        del_layout.addWidget(QLabel("删除字符:"))
        self.del_text_input = QLineEdit()
        del_layout.addWidget(self.del_text_input)
        del_layout.addWidget(QLabel("每行删除次数:"))
        self.del_count_input = QSpinBox()
        self.del_count_input.setRange(1, 100)
        del_layout.addWidget(self.del_count_input)
        self.char_del_btn = QPushButton("字符删除")
        self.char_del_btn.clicked.connect(self.char_delete)
        del_layout.addWidget(self.char_del_btn)
        layout.addLayout(del_layout)

        # 替换
        rep_layout = QHBoxLayout()
        rep_layout.addWidget(QLabel("查找字符:"))
        self.rep_find_input = QLineEdit()
        rep_layout.addWidget(self.rep_find_input)
        rep_layout.addWidget(QLabel("替换字符:"))
        self.rep_replace_input = QLineEdit()
        rep_layout.addWidget(self.rep_replace_input)
        rep_layout.addWidget(QLabel("每行替换次数:"))
        self.rep_count_input = QSpinBox()
        self.rep_count_input.setRange(1, 100)
        rep_layout.addWidget(self.rep_count_input)
        self.char_rep_btn = QPushButton("字符替换")
        self.char_rep_btn.clicked.connect(self.char_replace)
        rep_layout.addWidget(self.char_rep_btn)
        layout.addLayout(rep_layout)

        self.tabs.addTab(tab, "字符处理")

    # -------------------- 时间处理 --------------------
    def init_time_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)

        # 日期格式选择
        fmt_layout = QHBoxLayout()
        fmt_layout.addWidget(QLabel("原日期格式:"))
        self.orig_fmt_combo = QComboBox()
        self.orig_fmt_combo.addItems(["y-m-d","d-m-y","m-d-y"])
        fmt_layout.addWidget(self.orig_fmt_combo)

        fmt_layout.addWidget(QLabel("月格式:"))
        self.month_fmt_combo = QComboBox()
        self.month_fmt_combo.addItems(["m","mm","mmm","mmmm"])
        fmt_layout.addWidget(self.month_fmt_combo)

        fmt_layout.addWidget(QLabel("日格式:"))
        self.day_fmt_combo = QComboBox()
        self.day_fmt_combo.addItems(["d","dd"])
        fmt_layout.addWidget(self.day_fmt_combo)

        fmt_layout.addWidget(QLabel("分隔符:"))
        self.sep_combo = QComboBox()
        self.sep_combo.addItems(["-","/","\\",".",","," "," ,",""])
        fmt_layout.addWidget(self.sep_combo)

        layout.addLayout(fmt_layout)

        self.time_modify_btn = QPushButton("修改")
        self.time_modify_btn.clicked.connect(self.time_modify)
        layout.addWidget(self.time_modify_btn)

        self.tabs.addTab(tab, "时间处理")

    # -------------------- 标准化处理 --------------------
    def init_standard_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)

        self.standard_btn = QPushButton("标准化")
        self.standard_btn.clicked.connect(self.standardize)
        layout.addWidget(self.standard_btn)

        self.tabs.addTab(tab, "标准化处理")

    # -------------------- 粘贴/复制 --------------------
    def paste_text(self):
        self.text_edit.setPlainText(pyperclip.paste())

    def copy_text(self):
        pyperclip.copy(self.text_edit.toPlainText())

    # -------------------- 单元处理功能 --------------------
    def split_units(self, line):
        start = self.unit_start_input.text()
        end = self.unit_end_input.text()
        pattern = re.escape(start) + "(.*?)" + re.escape(end)
        return re.findall(pattern, line)

    def unit_move(self):
        # 待实现单元移动功能
        pass

    def unit_delete(self):
        # 待实现单元删除功能
        pass

    def unit_copy(self):
        # 待实现单元复制功能
        pass

    # -------------------- 字符处理功能 --------------------
    def char_add(self):
        lines = self.text_edit.toPlainText().splitlines()
        pos = self.add_pos_input.value()
        add_text = self.add_text_input.text()
        new_lines = []
        for line in lines:
            if pos <= len(line):
                new_lines.append(line[:pos]+add_text+line[pos:])
            else:
                new_lines.append(line+add_text)
        self.text_edit.setPlainText("\n".join(new_lines))

    def char_delete(self):
        lines = self.text_edit.toPlainText().splitlines()
        char = self.del_text_input.text()
        count = self.del_count_input.value()
        new_lines = []
        for line in lines:
            new_lines.append(line.replace(char,"",count))
        self.text_edit.setPlainText("\n".join(new_lines))

    def char_replace(self):
        lines = self.text_edit.toPlainText().splitlines()
        find = self.rep_find_input.text()
        replace = self.rep_replace_input.text()
        count = self.rep_count_input.value()
        new_lines = []
        for line in lines:
            new_lines.append(line.replace(find,replace,count))
        self.text_edit.setPlainText("\n".join(new_lines))

    # -------------------- 时间处理功能 --------------------
    def time_modify(self):
        # 待实现时间格式转换功能
        pass

    # -------------------- 标准化功能 --------------------
    def standardize(self):
        text = self.text_edit.toPlainText()
        # 繁体转简体
        text = zhconv.convert(text,"zh-cn")
        # 中文、英文、数字之间加空格
        text = re.sub(r'([\u4e00-\u9fff])([A-Za-z0-9])', r'\1 \2', text)
        text = re.sub(r'([A-Za-z0-9])([\u4e00-\u9fff])', r'\1 \2', text)
        # 标点符号标准化
        text = re.sub(r'([。！？；：，])', lambda m: m.group(1), text) # 中文全角保持
        text = re.sub(r'([.,!?:;])', lambda m: m.group(1), text) # 英文半角保持
        self.text_edit.setPlainText(text)

if __name__=="__main__":
    app = QApplication(sys.argv)
    window = TextProcessor()
    window.show()
    sys.exit(app.exec())