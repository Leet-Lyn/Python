# 请帮我写个中文的 Python 脚本，批注也是中文：
# 有图形界面。
# 作用是让我选择某一文件（图片或视频，或其他格式），选择到底是保留还是删除。
# 界面最上方有一个路径选择器，可以输入或可以选择某一路径（源文件夹）。
# 下面，界面左侧会列出该路径下所有文件（上下移动或鼠标可以选择某一文件），在它的下面是筛选器（可以筛选出想要的文件）。
# 右侧是针对选择的文件的预览（占用最大）。预览下有三个按钮，左侧是“剔除”，按后将该文件移动到剔除文件夹，中间是“待定”，按后再左侧文件下移选择一个文件，右侧是“保留”，按后将该文件移动到保留文件夹。右侧是“撤销”，用于撤销刚才的行动。
# 再之下是有两个路径选择器，可以输入或可以选择路径（分别是剔除文件夹与保留文件夹）。右侧是 个单选框，不移动到剔除文件夹，直接移动到回收站。
# 并设置快捷键：剔除（Ctrl+D）；保留（Ctrl+Q）；待定（Ctrl+Space）；撤销（Ctrl+Z）。

# 导入模块
import sys
import os
import shutil
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QListWidget, QLabel, QFileDialog, QLineEdit, QCheckBox
)
from PyQt6.QtGui import QPixmap, QMovie, QFont, QKeySequence, QShortcut
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from send2trash import send2trash
from PIL import Image

# pip install pillow pillow-avif-plugin send2trash

class FileReviewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("文件筛选工具（全内置+默认程序打开+撤销）")
        self.resize(1050, 650)

        self.source_path = ""
        self.keep_path = ""
        self.delete_path = ""
        self.file_list = []

        self.gif_movie = None
        self.video_player = None
        self.video_widget = None

        self.action_stack = []  # 用于撤销操作记录

        self.init_ui()
        self.init_shortcuts()

    # 初始化快捷键
    def init_shortcuts(self):
        QShortcut(QKeySequence("Ctrl+D"), self, activated=lambda: self.move_file("delete"))
        QShortcut(QKeySequence("Ctrl+Q"), self, activated=lambda: self.move_file("keep"))
        QShortcut(QKeySequence("Ctrl+Space"), self, activated=lambda: self.move_file("pending"))
        QShortcut(QKeySequence("Ctrl+Z"), self, activated=self.undo_action)

    def init_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # 顶部：源文件夹选择 + 刷新
        top_layout = QHBoxLayout()
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("选择源文件夹路径...")
        path_btn = QPushButton("浏览")
        path_btn.clicked.connect(self.select_source_path)
        refresh_btn = QPushButton("刷新")
        refresh_btn.clicked.connect(self.load_files)
        top_layout.addWidget(self.path_input)
        top_layout.addWidget(path_btn)
        top_layout.addWidget(refresh_btn)
        main_layout.addLayout(top_layout)

        # 中间布局：文件列表 + 预览
        file_preview_layout = QHBoxLayout()
        main_layout.addLayout(file_preview_layout)

        # 左侧文件列表
        left_layout = QVBoxLayout()
        self.file_list_widget = QListWidget()
        self.file_list_widget.currentRowChanged.connect(self.show_preview)
        left_layout.addWidget(self.file_list_widget)

        # 文件筛选器
        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("文件名筛选...")
        self.filter_input.textChanged.connect(self.apply_filter)
        left_layout.addWidget(self.filter_input)
        file_preview_layout.addLayout(left_layout, 1)

        # 右侧预览 + 按钮 + 文件夹选择
        right_layout = QVBoxLayout()
        self.preview_label = QLabel("预览")
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setFixedSize(600, 400)
        right_layout.addWidget(self.preview_label)

        # 视频播放器
        self.video_widget = QVideoWidget()
        self.video_widget.setFixedSize(600, 400)
        right_layout.addWidget(self.video_widget)
        self.video_widget.hide()
        self.audio_output = QAudioOutput()
        self.video_player = QMediaPlayer()
        self.video_player.setAudioOutput(self.audio_output)
        self.video_player.setVideoOutput(self.video_widget)

        # 按钮：剔除 / 待定 / 保留 / 撤销
        btn_layout = QHBoxLayout()
        btn_font = QFont()
        btn_font.setPointSize(16)
        self.delete_btn = QPushButton("剔除")
        self.delete_btn.setFont(btn_font)
        self.delete_btn.setFixedHeight(40)
        self.delete_btn.clicked.connect(lambda: self.move_file("delete"))

        self.pending_btn = QPushButton("待定")
        self.pending_btn.setFont(btn_font)
        self.pending_btn.setFixedHeight(40)
        self.pending_btn.clicked.connect(lambda: self.move_file("pending"))

        self.keep_btn = QPushButton("保留")
        self.keep_btn.setFont(btn_font)
        self.keep_btn.setFixedHeight(40)
        self.keep_btn.clicked.connect(lambda: self.move_file("keep"))

        self.undo_btn = QPushButton("撤销")
        self.undo_btn.setFont(btn_font)
        self.undo_btn.setFixedHeight(40)
        self.undo_btn.clicked.connect(self.undo_action)

        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.pending_btn)
        btn_layout.addWidget(self.keep_btn)
        btn_layout.addWidget(self.undo_btn)
        right_layout.addLayout(btn_layout)

        # 文件夹选择布局（剔除/保留互换）
        folder_layout = QHBoxLayout()
        # 剔除文件夹
        del_layout = QVBoxLayout()
        del_label = QLabel("剔除文件夹")
        self.delete_input = QLineEdit()
        self.delete_input.setPlaceholderText("选择剔除文件夹...")
        del_btn = QPushButton("浏览")
        del_btn.clicked.connect(self.select_delete_path)
        del_layout.addWidget(del_label)
        del_layout.addWidget(self.delete_input)
        del_layout.addWidget(del_btn)
        folder_layout.addLayout(del_layout)
        # 保留文件夹
        keep_layout = QVBoxLayout()
        keep_label = QLabel("保留文件夹")
        self.keep_input = QLineEdit()
        self.keep_input.setPlaceholderText("选择保留文件夹...")
        keep_btn = QPushButton("浏览")
        keep_btn.clicked.connect(self.select_keep_path)
        keep_layout.addWidget(keep_label)
        keep_layout.addWidget(self.keep_input)
        keep_layout.addWidget(keep_btn)
        folder_layout.addLayout(keep_layout)

        # 回收站选项
        self.trash_checkbox = QCheckBox("不移动到剔除文件夹，直接移到回收站")
        folder_layout.addWidget(self.trash_checkbox)
        right_layout.addLayout(folder_layout)

        file_preview_layout.addLayout(right_layout, 3)

    # 文件夹选择
    def select_source_path(self):
        path = QFileDialog.getExistingDirectory(self, "选择源文件夹")
        if path:
            self.source_path = path
            self.path_input.setText(path)
            self.load_files()

    def select_keep_path(self):
        path = QFileDialog.getExistingDirectory(self, "选择保留文件夹")
        if path:
            self.keep_path = path
            self.keep_input.setText(path)

    def select_delete_path(self):
        path = QFileDialog.getExistingDirectory(self, "选择剔除文件夹")
        if path:
            self.delete_path = path
            self.delete_input.setText(path)

    # 加载文件
    def load_files(self):
        if not self.source_path:
            return
        self.file_list = os.listdir(self.source_path)
        self.file_list.sort()
        self.apply_filter()

    def apply_filter(self):
        filter_text = self.filter_input.text().lower()
        self.file_list_widget.clear()
        for f in self.file_list:
            if filter_text in f.lower():
                self.file_list_widget.addItem(f)

    # 预览
    def show_preview(self, index):
        if index < 0 or index >= len(self.file_list_widget):
            self.preview_label.clear()
            self.preview_label.show()
            self.video_widget.hide()
            return
        filename = self.file_list_widget.currentItem().text()
        filepath = os.path.join(self.source_path, filename)

        # 停止 GIF 动画
        if self.gif_movie:
            self.gif_movie.stop()
            self.gif_movie = None
        # 停止视频
        if self.video_player.playbackState() != QMediaPlayer.PlaybackState.StoppedState:
            self.video_player.stop()
        self.preview_label.show()
        self.video_widget.hide()

        try:
            if filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp")):
                pixmap = QPixmap(filepath)
                self.preview_label.setPixmap(pixmap.scaled(
                    self.preview_label.width(),
                    self.preview_label.height(),
                    Qt.AspectRatioMode.KeepAspectRatio
                ))
            elif filename.lower().endswith(".avif"):
                im = Image.open(filepath).convert("RGBA")
                im.save("temp_preview.png")
                pixmap = QPixmap("temp_preview.png")
                self.preview_label.setPixmap(pixmap.scaled(
                    self.preview_label.width(),
                    self.preview_label.height(),
                    Qt.AspectRatioMode.KeepAspectRatio
                ))
                os.remove("temp_preview.png")
            elif filename.lower().endswith(".gif"):
                self.gif_movie = QMovie(filepath)
                self.preview_label.setMovie(self.gif_movie)
                self.gif_movie.start()
            elif filename.lower().endswith((".mp4", ".avi", ".mkv", ".webm")):
                self.video_player.setSource(QUrl.fromLocalFile(filepath))
                self.preview_label.hide()
                self.video_widget.show()
                self.video_player.play()
            else:
                raise Exception("无法内置预览")
        except Exception:
            # 调用系统默认程序打开
            self.preview_label.setText(f"无法预览: {filename}\n请用系统默认程序打开")
            self.open_external(filepath)

    def open_external(self, filepath):
        try:
            os.startfile(filepath)
        except Exception as e:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "错误", f"无法用默认程序打开文件：{e}")

    # 移动文件
    def move_file(self, action):
        item = self.file_list_widget.currentItem()
        if not item:
            return
        filename = item.text()
        src = os.path.join(self.source_path, filename)

        # 保存撤销记录
        self.action_stack.append((filename, action, src, self.keep_input.text() or self.keep_path,
                                  self.delete_input.text() or self.delete_path))

        if action == "keep":
            dst_folder = self.keep_input.text() or self.keep_path
        elif action == "delete":
            if self.trash_checkbox.isChecked():
                send2trash(src)
                self.remove_from_list()
                return
            else:
                dst_folder = self.delete_input.text() or self.delete_path
        else:  # 待定
            next_row = (self.file_list_widget.currentRow() + 1) % self.file_list_widget.count()
            self.file_list_widget.setCurrentRow(next_row)
            return

        if dst_folder:
            os.makedirs(dst_folder, exist_ok=True)
            dst = os.path.join(dst_folder, filename)
            shutil.move(src, dst)
            self.remove_from_list()

    # 撤销功能
    def undo_action(self):
        if not self.action_stack:
            return
        filename, action, src, keep_path, delete_path = self.action_stack.pop()

        # 撤销移动文件
        if action in ("keep", "delete"):
            if action == "keep":
                dst_folder = keep_path
            else:
                if self.trash_checkbox.isChecked():
                    # 回收站删除无法撤销
                    return
                dst_folder = delete_path
            dst = os.path.join(dst_folder, filename)
            if os.path.exists(dst):
                shutil.move(dst, src)
                self.file_list_widget.addItem(filename)
        # 待定撤销不需要移动，只恢复列表
        if action == "pending":
            self.file_list_widget.addItem(filename)

    def remove_from_list(self):
        row = self.file_list_widget.currentRow()
        self.file_list_widget.takeItem(row)
        next_row = min(row, self.file_list_widget.count() - 1)
        if next_row >= 0:
            self.file_list_widget.setCurrentRow(next_row)
        else:
            self.preview_label.clear()
            self.preview_label.show()
            self.video_widget.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileReviewer()
    window.show()
    sys.exit(app.exec())