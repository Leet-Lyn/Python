# 请帮我写个中文的 Python 脚本，批注也是中文：
# 有图形界面。
# 作用是让我选择某一文件（图片或视频，或其他格式），选择到底是保留还是删除。
# 界面最上方有一个路径选择器，可以输入或可以选择某一路径（源文件夹）。
# 下面，界面左侧会列出该路径下所有文件（上下移动或鼠标可以选择某一文件），在它的下面是筛选器（可以筛选出想要的文件）。
# 右侧是针对选择的文件的预览（占用最大）。预览下有三个按钮，左侧是“剔除”，按后将该文件移动到剔除文件夹，中间是“待定”，按后再左侧文件下移选择一个文件，右侧是“保留”，按后将该文件移动到保留文件夹。右侧是“撤销”，用于撤销刚才的行动。
# 再之下是有两个路径选择器，可以输入或可以选择路径（分别是剔除文件夹与保留文件夹）。右侧是 个单选框，不移动到剔除文件夹，直接移动到回收站。
# 并设置快捷键：剔除（Ctrl+D）；保留（Ctrl+Q）；待定（Ctrl+Space）；撤销（Ctrl+Z）。

# 导入模块
import os
import sys
import gc
import shutil
import time
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QListWidget, QListWidgetItem,
    QFileDialog, QCheckBox, QMessageBox, QSplitter, QStackedWidget,
    QSlider
)
from PySide6.QtCore import Qt, QUrl, QTimer
from PySide6.QtGui import QPixmap, QMovie, QIcon, QShortcut, QKeySequence, QImage
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget

# 尝试导入 PIL 用于 AVIF 支持
try:
    from PIL import Image
    import pillow_avif
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

# 尝试导入 send2trash
try:
    from send2trash import send2trash
    HAS_SEND2TRASH = True
except ImportError:
    HAS_SEND2TRASH = False
    send2trash = None

# 支持的图片扩展名（静态）
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp', '.avif'}
# 支持的视频扩展名
VIDEO_EXTENSIONS = {'.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv', '.m4v', '.mpg', '.mpeg'}


class FileSorterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("文件筛选工具")
        self.resize(1200, 700)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)

        # 顶部：源文件夹路径选择 + 刷新按钮
        top_layout = QHBoxLayout()
        self.src_path_edit = QLineEdit()
        self.src_path_edit.setPlaceholderText("选择源文件夹...")
        self.src_browse_btn = QPushButton("浏览...")
        self.src_browse_btn.clicked.connect(self.browse_src_folder)
        self.refresh_btn = QPushButton("刷新")
        self.refresh_btn.clicked.connect(self.refresh_folder)
        top_layout.addWidget(QLabel("源文件夹:"))
        top_layout.addWidget(self.src_path_edit)
        top_layout.addWidget(self.src_browse_btn)
        top_layout.addWidget(self.refresh_btn)
        main_layout.addLayout(top_layout)

        # 中间区域：左侧文件列表 + 右侧预览
        middle_splitter = QSplitter(Qt.Horizontal)

        # 左侧：文件列表 + 筛选器
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)

        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QListWidget.SingleSelection)
        self.file_list.currentItemChanged.connect(self.on_file_selected)
        left_layout.addWidget(self.file_list)

        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("筛选:"))
        self.filter_edit = QLineEdit()
        self.filter_edit.setPlaceholderText("输入文件名过滤...")
        self.filter_edit.textChanged.connect(self.apply_filter)
        filter_layout.addWidget(self.filter_edit)
        left_layout.addLayout(filter_layout)

        middle_splitter.addWidget(left_widget)

        # 右侧：预览区域（堆叠控件）
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)

        self.preview_stack = QStackedWidget()
        self.preview_stack.setMinimumSize(400, 300)
        self.preview_stack.setStyleSheet("border: 1px solid gray; background-color: #f0f0f0;")

        self.preview_label = QLabel("选择一个文件以预览")
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setScaledContents(False)
        self.preview_stack.addWidget(self.preview_label)

        self.video_widget = QVideoWidget()
        self.video_widget.setStyleSheet("background-color: black;")
        self.video_player = QMediaPlayer()
        self.video_player.setVideoOutput(self.video_widget)
        self.preview_stack.addWidget(self.video_widget)

        right_layout.addWidget(self.preview_stack)

        # 视频控制栏 + 终止预览按钮（静默），快捷键 Ctrl+S
        control_layout = QHBoxLayout()
        self.play_pause_btn = QPushButton("播放")
        self.play_pause_btn.setEnabled(False)
        self.play_pause_btn.clicked.connect(self.toggle_video_play)

        self.video_slider = QSlider(Qt.Horizontal)
        self.video_slider.setEnabled(False)
        self.video_slider.sliderMoved.connect(self.video_player.setPosition)
        self.video_player.positionChanged.connect(self.video_slider.setValue)
        self.video_player.durationChanged.connect(self.video_slider.setRange)

        control_layout.addWidget(self.play_pause_btn)
        control_layout.addWidget(self.video_slider)

        # 静默终止预览按钮（无弹窗），显示快捷键
        self.stop_preview_btn = QPushButton("终止预览 (Ctrl+S)")
        self.stop_preview_btn.clicked.connect(self.stop_preview)
        control_layout.addWidget(self.stop_preview_btn)

        right_layout.addLayout(control_layout)

        middle_splitter.addWidget(right_widget)

        middle_splitter.setSizes([300, 600])
        main_layout.addWidget(middle_splitter)

        # 操作按钮区域
        btn_layout = QHBoxLayout()

        self.discard_btn = QPushButton("剔除 (Ctrl+D)")
        self.hold_btn = QPushButton("待定 (Ctrl+Space)")
        self.keep_btn = QPushButton("保留 (Ctrl+Q)")
        self.undo_btn = QPushButton("撤销 (Ctrl+Z)")

        btn_layout.addWidget(self.discard_btn)
        btn_layout.addWidget(self.hold_btn)
        btn_layout.addWidget(self.keep_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.undo_btn)

        main_layout.addLayout(btn_layout)

        # 底部：目标文件夹选择 + 回收站选项
        bottom_layout = QHBoxLayout()

        self.discard_path_edit = QLineEdit()
        self.discard_path_edit.setPlaceholderText("选择剔除文件夹...")
        self.discard_browse_btn = QPushButton("浏览...")
        self.discard_browse_btn.clicked.connect(lambda: self.browse_folder(self.discard_path_edit))

        self.keep_path_edit = QLineEdit()
        self.keep_path_edit.setPlaceholderText("选择保留文件夹...")
        self.keep_browse_btn = QPushButton("浏览...")
        self.keep_browse_btn.clicked.connect(lambda: self.browse_folder(self.keep_path_edit))

        self.recycle_check = QCheckBox("不移动到剔除文件夹，直接移动到回收站")

        bottom_layout.addWidget(QLabel("剔除文件夹:"))
        bottom_layout.addWidget(self.discard_path_edit)
        bottom_layout.addWidget(self.discard_browse_btn)
        bottom_layout.addSpacing(20)
        bottom_layout.addWidget(QLabel("保留文件夹:"))
        bottom_layout.addWidget(self.keep_path_edit)
        bottom_layout.addWidget(self.keep_browse_btn)
        bottom_layout.addSpacing(20)
        bottom_layout.addWidget(self.recycle_check)

        main_layout.addLayout(bottom_layout)

        # 数据
        self.src_folder = ""
        self.all_files = []
        self.filtered_files = []
        self.current_file = None
        self.history = []
        self.current_movie = None

        self.discard_btn.clicked.connect(self.discard_current)
        self.hold_btn.clicked.connect(self.hold_current)
        self.keep_btn.clicked.connect(self.keep_current)
        self.undo_btn.clicked.connect(self.undo)

        QShortcut(QKeySequence("Ctrl+D"), self, self.discard_current)
        QShortcut(QKeySequence("Ctrl+Q"), self, self.keep_current)
        QShortcut(QKeySequence("Ctrl+Space"), self, self.hold_current)
        QShortcut(QKeySequence("Ctrl+Z"), self, self.undo)
        # 新增：终止预览快捷键 Ctrl+S
        QShortcut(QKeySequence("Ctrl+S"), self, self.stop_preview)

        self.update_buttons_state()

    # ---------- 辅助函数 ----------
    def browse_src_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "选择源文件夹")
        if folder:
            self.src_path_edit.setText(folder)
            self.load_folder(folder)

    def refresh_folder(self):
        folder = self.src_path_edit.text().strip()
        if folder and os.path.isdir(folder):
            self.load_folder(folder)
        else:
            QMessageBox.warning(self, "警告", "请先选择有效的源文件夹")

    def browse_folder(self, line_edit):
        folder = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if folder:
            line_edit.setText(folder)

    def load_folder(self, folder):
        self.src_folder = folder
        self.all_files = []
        try:
            for entry in os.scandir(folder):
                if entry.is_file():
                    self.all_files.append(entry.path)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"无法读取文件夹：{e}")
            return

        self.all_files.sort(key=lambda p: os.path.basename(p).lower())
        self.apply_filter()

    def apply_filter(self):
        filter_text = self.filter_edit.text().strip().lower()
        if not filter_text:
            self.filtered_files = self.all_files.copy()
        else:
            self.filtered_files = [f for f in self.all_files if filter_text in os.path.basename(f).lower()]

        self.refresh_file_list()

    def refresh_file_list(self):
        self.file_list.clear()
        for file_path in self.filtered_files:
            item = QListWidgetItem(os.path.basename(file_path))
            item.setData(Qt.UserRole, file_path)
            self.file_list.addItem(item)

        if self.filtered_files:
            self.file_list.setCurrentRow(0)
        else:
            self.preview_label.setText("无匹配文件")
            self.current_file = None
            self.update_buttons_state()

    def on_file_selected(self, current, previous):
        if current:
            file_path = current.data(Qt.UserRole)
            self.current_file = file_path
            self.preview_file(file_path)
        else:
            self.current_file = None
            self.clear_preview()
        self.update_buttons_state()

    def clear_preview(self):
        """清理预览资源"""
        self.video_player.stop()
        self.video_player.setSource(QUrl())
        self.play_pause_btn.setEnabled(False)
        self.video_slider.setEnabled(False)

        if self.current_movie:
            self.current_movie.stop()
            self.current_movie.deleteLater()
            self.current_movie = None

        self.preview_label.setPixmap(QPixmap())
        self.preview_label.setMovie(None)
        self.preview_label.setText("")

        for _ in range(3):
            QApplication.processEvents()
            QApplication.sendPostedEvents()

        gc.collect()

    def stop_preview(self):
        """终止预览按钮：静默释放文件句柄，无弹窗"""
        self.clear_preview()

    def pil_to_qpixmap(self, pil_image):
        if pil_image.mode == "RGBA":
            qimage = QImage(pil_image.tobytes(), pil_image.width, pil_image.height, QImage.Format_RGBA8888)
        else:
            qimage = QImage(pil_image.tobytes(), pil_image.width, pil_image.height, QImage.Format_RGB888)
        return QPixmap.fromImage(qimage)

    def preview_file(self, file_path):
        self.clear_preview()
        ext = os.path.splitext(file_path)[1].lower()

        if ext == '.gif':
            movie = QMovie(file_path)
            if movie.isValid():
                self.preview_stack.setCurrentIndex(0)
                self.preview_label.setMovie(movie)
                movie.start()
                self.current_movie = movie
                self.preview_label.setText("")
            else:
                self.preview_label.setText("无法加载GIF")

        elif ext in VIDEO_EXTENSIONS:
            url = QUrl.fromLocalFile(file_path)
            self.video_player.setSource(url)
            self.video_player.play()
            self.preview_stack.setCurrentIndex(1)
            self.play_pause_btn.setEnabled(True)
            self.play_pause_btn.setText("暂停")
            self.video_slider.setEnabled(True)

        elif ext in IMAGE_EXTENSIONS:
            if ext == '.avif':
                if not HAS_PIL:
                    self.preview_label.setText("需要安装pillow和pillow-avif-plugin才能预览AVIF")
                    return
                try:
                    pil_img = Image.open(file_path)
                    if pil_img.mode not in ("RGB", "RGBA"):
                        pil_img = pil_img.convert("RGBA")
                    qpix = self.pil_to_qpixmap(pil_img)
                    if not qpix.isNull():
                        label_size = self.preview_label.size()
                        scaled = qpix.scaled(label_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                        self.preview_stack.setCurrentIndex(0)
                        self.preview_label.setPixmap(scaled)
                        self.preview_label.setText("")
                    else:
                        self.preview_label.setText("无法加载AVIF")
                except Exception as e:
                    self.preview_label.setText(f"AVIF加载失败: {str(e)}")
            else:
                pixmap = QPixmap(file_path)
                if not pixmap.isNull():
                    label_size = self.preview_label.size()
                    scaled = pixmap.scaled(label_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    self.preview_stack.setCurrentIndex(0)
                    self.preview_label.setPixmap(scaled)
                    self.preview_label.setText("")
                else:
                    self.preview_label.setPixmap(QPixmap())
                    self.preview_label.setText("无法加载图片")

        else:
            self.preview_stack.setCurrentIndex(0)
            icon = QIcon.fromTheme("video-x-generic")
            if not icon.isNull():
                pixmap = icon.pixmap(128, 128)
                self.preview_label.setPixmap(pixmap)
                self.preview_label.setText("")
            else:
                self.preview_label.setText(f"无法预览此类型文件\n{os.path.basename(file_path)}")

    def toggle_video_play(self):
        if self.video_player.playbackState() == QMediaPlayer.PlayingState:
            self.video_player.pause()
            self.play_pause_btn.setText("播放")
        else:
            self.video_player.play()
            self.play_pause_btn.setText("暂停")

    def update_buttons_state(self):
        has_file = self.current_file is not None and os.path.exists(self.current_file)
        self.discard_btn.setEnabled(has_file)
        self.keep_btn.setEnabled(has_file)
        self.hold_btn.setEnabled(has_file)

    # ---------- 移动操作 ----------
    def move_file_with_retry(self, src, dst, max_retries=2, delay=0.2):
        for attempt in range(max_retries):
            try:
                shutil.move(src, dst)
                return True, None
            except PermissionError as e:
                if attempt < max_retries - 1:
                    # 切换文件以解除占用
                    self.select_next_file()
                    time.sleep(delay)
                    self.clear_preview()
                    gc.collect()
                else:
                    return False, str(e)
            except Exception as e:
                return False, str(e)
        return False, "未知错误"

    def discard_current(self):
        if not self.current_file:
            return
        src_path = self.current_file
        self.clear_preview()  # 自动终止预览

        discard_folder = self.discard_path_edit.text().strip()
        use_recycle = self.recycle_check.isChecked()

        if use_recycle:
            if not HAS_SEND2TRASH:
                QMessageBox.critical(self, "错误", "未安装 send2trash 库，无法移动到回收站。请运行 pip install send2trash 或选择剔除文件夹。")
                return
            try:
                send2trash(src_path)
            except Exception as e:
                QMessageBox.critical(self, "错误", f"移动到回收站失败：{e}")
                return
            dest_info = ("回收站", None)
        else:
            if not discard_folder:
                QMessageBox.warning(self, "警告", "请先指定剔除文件夹或勾选回收站选项。")
                return
            if not os.path.exists(discard_folder):
                try:
                    os.makedirs(discard_folder)
                except Exception as e:
                    QMessageBox.critical(self, "错误", f"无法创建剔除文件夹：{e}")
                    return
            dest_path = os.path.join(discard_folder, os.path.basename(src_path))
            success, error_msg = self.move_file_with_retry(src_path, dest_path)
            if not success:
                reply = QMessageBox.question(self, "移动失败", 
                                             f"移动文件失败（已尝试切换文件重试）: {error_msg}\n\n是否尝试使用“终止预览”按钮手动释放后重试？",
                                             QMessageBox.Retry | QMessageBox.Cancel)
                if reply == QMessageBox.Retry:
                    QMessageBox.information(self, "提示", "请先点击下方的“终止预览”按钮，然后再次点击“剔除”或“保留”。")
                return
            dest_info = (discard_folder, dest_path)

        self.history.append({
            'action': 'discard',
            'src': src_path,
            'dest_info': dest_info,
            'position': self.file_list.currentRow()
        })
        self.remove_current_from_list()

    def keep_current(self):
        if not self.current_file:
            return
        src_path = self.current_file
        self.clear_preview()  # 自动终止预览

        keep_folder = self.keep_path_edit.text().strip()
        if not keep_folder:
            QMessageBox.warning(self, "警告", "请先指定保留文件夹。")
            return
        if not os.path.exists(keep_folder):
            try:
                os.makedirs(keep_folder)
            except Exception as e:
                QMessageBox.critical(self, "错误", f"无法创建保留文件夹：{e}")
                return
        dest_path = os.path.join(keep_folder, os.path.basename(src_path))
        success, error_msg = self.move_file_with_retry(src_path, dest_path)
        if not success:
            reply = QMessageBox.question(self, "移动失败", 
                                         f"移动文件失败（已尝试切换文件重试）: {error_msg}\n\n是否尝试使用“终止预览”按钮手动释放后重试？",
                                         QMessageBox.Retry | QMessageBox.Cancel)
            if reply == QMessageBox.Retry:
                QMessageBox.information(self, "提示", "请先点击下方的“终止预览”按钮，然后再次点击“剔除”或“保留”。")
            return

        self.history.append({
            'action': 'keep',
            'src': src_path,
            'dest': dest_path,
            'position': self.file_list.currentRow()
        })
        self.remove_current_from_list()

    def hold_current(self):
        if not self.current_file:
            return
        self.select_next_file()

    def undo(self):
        if not self.history:
            QMessageBox.information(self, "撤销", "没有可撤销的操作")
            return

        last = self.history[-1]
        if last['action'] == 'discard' and last['dest_info'][0] == "回收站":
            QMessageBox.information(self, "撤销", "无法从回收站恢复文件，请手动处理。")
            return

        last = self.history.pop()
        action = last['action']
        src = last['src']
        position = last['position']

        if action == 'discard':
            dest_info = last['dest_info']
            dest_path = dest_info[1]
            try:
                shutil.move(dest_path, src)
            except Exception as e:
                QMessageBox.critical(self, "错误", f"撤销失败：{e}")
                return
        elif action == 'keep':
            dest_path = last['dest']
            try:
                shutil.move(dest_path, src)
            except Exception as e:
                QMessageBox.critical(self, "错误", f"撤销失败：{e}")
                return

        self.all_files.append(src)
        self.all_files.sort(key=lambda p: os.path.basename(p).lower())
        self.apply_filter()
        try:
            new_index = self.filtered_files.index(src)
        except ValueError:
            new_index = 0
        self.file_list.setCurrentRow(new_index)

    def remove_current_from_list(self):
        if not self.current_file:
            return
        if self.current_file in self.all_files:
            self.all_files.remove(self.current_file)
        if self.current_file in self.filtered_files:
            self.filtered_files.remove(self.current_file)

        self.refresh_file_list()

    def select_next_file(self):
        current_row = self.file_list.currentRow()
        if current_row < self.file_list.count() - 1:
            self.file_list.setCurrentRow(current_row + 1)
        else:
            if self.file_list.count() > 0:
                self.file_list.setCurrentRow(0)

    def closeEvent(self, event):
        self.clear_preview()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileSorterApp()
    window.show()
    sys.exit(app.exec())