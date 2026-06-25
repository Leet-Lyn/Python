# 请帮我写个中文的 Python 脚本，批注也是中文：
# 有图形界面。
# 作用是让我选择某一文件（图片或视频，或其他格式），选择到底是保留还是删除。
# 界面最上方有一个路径选择器，可以输入或可以选择某一路径（源文件夹，默认：d:\Studios\Folders\Downloads\）。
# 下面，界面左侧会列出该路径下所有文件（上下移动或鼠标可以选择某一文件），在它的下面是筛选器（可以筛选出想要的文件）。
# 右侧是针对选择的文件的预览（占用最大）。预览下有三个按钮，左侧是"剔除"，按后将该文件移动到剔除文件夹，中间是"待定"，按后再左侧文件下移选择一个文件，右侧是"保留"，按后将该文件移动到保留文件夹。右侧是"撤销"，用于撤销刚才的行动。在撤销按键的左侧添加按键"随机"，按下否在左侧列表中随机选择一个文件浏览。
# 再之下是有两个路径选择器，可以输入或可以选择路径（分别是剔除文件夹，默认：d:\Studios\Folders\Deletes\。与保留文件夹，默认：d:\Studios\Folders\Retains\）。右侧是 个单选框，不移动到剔除文件夹，直接移动到回收站。
# 并设置快捷键：剔除（D）；保留（Q）；待定（H）；随机（Space）；撤销（U）。

# 导入模块
import gc
import random
import shutil
import sys
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

# ==================== 全局配置 ====================

DEFAULT_SOURCE_DIR = Path(r"d:\Studios\Folders\Downloads")
DEFAULT_DISCARD_DIR = Path(r"d:\Studios\Folders\Deletes")
DEFAULT_KEEP_DIR = Path(r"d:\Studios\Folders\Retains")

# 支持的图片扩展名（静态）
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp', '.avif'}
# 支持的视频扩展名
VIDEO_EXTENSIONS = {'.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv', '.m4v', '.mpg', '.mpeg'}

# --- 消息常量 ---

# 程序退出相关
MSG_INTERRUPTED = "\n\n用户中断程序，已退出。"
MSG_ERROR = "\n程序运行出错: {}"
MSG_EXIT = "\n按回车键退出..."

# 窗口
MSG_WINDOW_TITLE = "文件筛选工具"

# 占位符文本
MSG_PLACEHOLDER_SRC = "选择源文件夹..."
MSG_PLACEHOLDER_DISCARD = "选择剔除文件夹..."
MSG_PLACEHOLDER_KEEP = "选择保留文件夹..."
MSG_PLACEHOLDER_FILTER = "输入文件名过滤..."

# 按钮文本
MSG_BTN_BROWSE = "浏览..."
MSG_BTN_REFRESH = "刷新"
MSG_BTN_DISCARD = "剔除 (D)"
MSG_BTN_HOLD = "待定 (H)"
MSG_BTN_KEEP = "保留 (Q)"
MSG_BTN_RANDOM = "随机 (Space)"
MSG_BTN_UNDO = "撤销 (U)"
MSG_BTN_PLAY = "播放"
MSG_BTN_PAUSE = "暂停"

# 标签文本
MSG_LABEL_SRC = "源文件夹:"
MSG_LABEL_FILTER = "筛选:"
MSG_LABEL_DISCARD = "剔除文件夹:"
MSG_LABEL_KEEP = "保留文件夹:"

# 复选框文本
MSG_CHECK_RECYCLE = "不移动到剔除文件夹，直接移动到回收站"

# 预览区域文本
MSG_PREVIEW_DEFAULT = "选择一个文件以预览"
MSG_PREVIEW_NO_MATCH = "无匹配文件"
MSG_PREVIEW_CANNOT_PREVIEW = "无法预览此类型文件\n{}"
MSG_PREVIEW_GIF_FAIL = "无法加载GIF"
MSG_PREVIEW_NEED_PIL = "需要安装pillow才能预览{}"
MSG_PREVIEW_LOAD_FAIL = "{}加载失败: {}"
MSG_PREVIEW_IMG_FAIL = "无法加载图片"
MSG_PREVIEW_GENERIC = "无法加载{}"

# QMessageBox 标题
MSG_MBOX_INFO = "提示"
MSG_MBOX_WARNING = "警告"
MSG_MBOX_ERROR = "错误"
MSG_MBOX_MOVE_FAIL = "移动失败"
MSG_MBOX_UNDO = "撤销"

# QMessageBox 消息
MSG_MBOX_DEFAULT_SRC_MISSING = "默认源文件夹不存在：{}\n请选择有效的源文件夹。"
MSG_MBOX_SELECT_VALID_SRC = "请先选择有效的源文件夹"
MSG_MBOX_CANNOT_READ_FOLDER = "无法读取文件夹：{}"
MSG_MBOX_NO_SEND2TRASH = "未安装 send2trash 库，无法移动到回收站。请运行 pip install send2trash 或选择剔除文件夹。"
MSG_MBOX_TRASH_FAIL = "移动到回收站失败：{}"
MSG_MBOX_SPECIFY_DISCARD = "请先指定剔除文件夹或勾选回收站选项。"
MSG_MBOX_CANNOT_CREATE_DISCARD = "无法创建剔除文件夹：{}"
MSG_MBOX_SPECIFY_KEEP = "请先指定保留文件夹。"
MSG_MBOX_CANNOT_CREATE_KEEP = "无法创建保留文件夹：{}"
MSG_MBOX_MOVE_FAIL_MSG = "移动文件失败（已尝试切换文件重试）: {}\n\n是否重试？"
MSG_MBOX_RETRY_HINT = "请重试操作。"
MSG_MBOX_NO_FILES = "没有可用的文件。"
MSG_MBOX_NO_UNDO = "没有可撤销的操作"
MSG_MBOX_UNDO_RECYCLE = "无法从回收站恢复文件，请手动处理。"
MSG_MBOX_UNDO_FAIL = "撤销失败：{}"
MSG_UNKNOWN_ERROR = "未知错误"

# QFileDialog 标题
MSG_DLG_SELECT_SRC = "选择源文件夹"
MSG_DLG_SELECT_FOLDER = "选择文件夹"

# ==================== 主窗口 ====================


class FileSorterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(MSG_WINDOW_TITLE)
        self.resize(1200, 700)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)

        # 顶部：源文件夹路径选择 + 刷新按钮
        top_layout = QHBoxLayout()
        self.src_path_edit = QLineEdit()
        self.src_path_edit.setPlaceholderText(MSG_PLACEHOLDER_SRC)
        self.src_browse_btn = QPushButton(MSG_BTN_BROWSE)
        self.src_browse_btn.clicked.connect(self.browse_src_folder)
        self.refresh_btn = QPushButton(MSG_BTN_REFRESH)
        self.refresh_btn.clicked.connect(self.refresh_folder)
        top_layout.addWidget(QLabel(MSG_LABEL_SRC))
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
        filter_layout.addWidget(QLabel(MSG_LABEL_FILTER))
        self.filter_edit = QLineEdit()
        self.filter_edit.setPlaceholderText(MSG_PLACEHOLDER_FILTER)
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

        self.preview_label = QLabel(MSG_PREVIEW_DEFAULT)
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setScaledContents(False)
        self.preview_stack.addWidget(self.preview_label)

        self.video_widget = QVideoWidget()
        self.video_widget.setStyleSheet("background-color: black;")
        self.video_player = QMediaPlayer()
        self.video_player.setVideoOutput(self.video_widget)
        self.preview_stack.addWidget(self.video_widget)

        right_layout.addWidget(self.preview_stack)

        # 视频控制栏
        control_layout = QHBoxLayout()
        self.play_pause_btn = QPushButton(MSG_BTN_PLAY)
        self.play_pause_btn.setEnabled(False)
        self.play_pause_btn.clicked.connect(self.toggle_video_play)

        self.video_slider = QSlider(Qt.Horizontal)
        self.video_slider.setEnabled(False)
        self.video_slider.sliderMoved.connect(self.video_player.setPosition)
        self.video_player.positionChanged.connect(self.video_slider.setValue)
        self.video_player.durationChanged.connect(self.video_slider.setRange)

        control_layout.addWidget(self.play_pause_btn)
        control_layout.addWidget(self.video_slider)

        right_layout.addLayout(control_layout)

        middle_splitter.addWidget(right_widget)

        middle_splitter.setSizes([300, 600])
        main_layout.addWidget(middle_splitter)

        # 操作按钮区域（剔除、待定、保留、随机、撤销）
        btn_layout = QHBoxLayout()

        self.discard_btn = QPushButton(MSG_BTN_DISCARD)
        self.hold_btn = QPushButton(MSG_BTN_HOLD)
        self.keep_btn = QPushButton(MSG_BTN_KEEP)
        self.random_btn = QPushButton(MSG_BTN_RANDOM)
        self.undo_btn = QPushButton(MSG_BTN_UNDO)

        btn_layout.addWidget(self.discard_btn)
        btn_layout.addWidget(self.hold_btn)
        btn_layout.addWidget(self.keep_btn)
        btn_layout.addWidget(self.random_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.undo_btn)

        main_layout.addLayout(btn_layout)

        # 底部：目标文件夹选择 + 回收站选项
        bottom_layout = QHBoxLayout()

        self.discard_path_edit = QLineEdit()
        self.discard_path_edit.setPlaceholderText(MSG_PLACEHOLDER_DISCARD)
        self.discard_browse_btn = QPushButton(MSG_BTN_BROWSE)
        self.discard_browse_btn.clicked.connect(lambda: self.browse_folder(self.discard_path_edit))

        self.keep_path_edit = QLineEdit()
        self.keep_path_edit.setPlaceholderText(MSG_PLACEHOLDER_KEEP)
        self.keep_browse_btn = QPushButton(MSG_BTN_BROWSE)
        self.keep_browse_btn.clicked.connect(lambda: self.browse_folder(self.keep_path_edit))

        self.recycle_check = QCheckBox(MSG_CHECK_RECYCLE)

        bottom_layout.addWidget(QLabel(MSG_LABEL_DISCARD))
        bottom_layout.addWidget(self.discard_path_edit)
        bottom_layout.addWidget(self.discard_browse_btn)
        bottom_layout.addSpacing(20)
        bottom_layout.addWidget(QLabel(MSG_LABEL_KEEP))
        bottom_layout.addWidget(self.keep_path_edit)
        bottom_layout.addWidget(self.keep_browse_btn)
        bottom_layout.addSpacing(20)
        bottom_layout.addWidget(self.recycle_check)

        main_layout.addLayout(bottom_layout)

        # ---------- 设置默认路径 ----------
        self.src_path_edit.setText(str(DEFAULT_SOURCE_DIR))
        self.discard_path_edit.setText(str(DEFAULT_DISCARD_DIR))
        self.keep_path_edit.setText(str(DEFAULT_KEEP_DIR))

        # 路径输入框支持回车确认
        self.src_path_edit.returnPressed.connect(self.refresh_folder)

        # 可选：提示用户源文件夹是否存在（不自动创建，由用户决定）
        if not DEFAULT_SOURCE_DIR.is_dir():
            QMessageBox.information(self, MSG_MBOX_INFO, MSG_MBOX_DEFAULT_SRC_MISSING.format(DEFAULT_SOURCE_DIR))

        # 数据
        self.src_folder = ""
        self.all_files: list[str] = []
        self.filtered_files: list[str] = []
        self.current_file: str | None = None
        self.history: list[dict] = []
        self.current_movie = None
        self.anim_timer = QTimer(self)
        self.anim_timer.timeout.connect(self._next_anim_frame)
        self.anim_frames: list[QPixmap] = []
        self.anim_delays: list[int] = []
        self.anim_index = 0

        self.discard_btn.clicked.connect(self.discard_current)
        self.hold_btn.clicked.connect(self.hold_current)
        self.keep_btn.clicked.connect(self.keep_current)
        self.random_btn.clicked.connect(self.random_select)
        self.undo_btn.clicked.connect(self.undo)

        # 快捷键：单键（无修饰符）
        QShortcut(QKeySequence("D"), self, self.discard_current)
        QShortcut(QKeySequence("Q"), self, self.keep_current)
        QShortcut(QKeySequence("H"), self, self.hold_current)       # 待定改为 H
        QShortcut(QKeySequence("Space"), self, self.random_select)  # 随机使用空格
        QShortcut(QKeySequence("U"), self, self.undo)

        self.update_buttons_state()

    # ---------- 辅助函数 ----------
    def browse_src_folder(self):
        folder = QFileDialog.getExistingDirectory(self, MSG_DLG_SELECT_SRC)
        if folder:
            self.src_path_edit.setText(folder)
            self.load_folder(folder)

    def refresh_folder(self):
        folder = self.src_path_edit.text().strip()
        if folder and Path(folder).is_dir():
            self.load_folder(folder)
        else:
            QMessageBox.warning(self, MSG_MBOX_WARNING, MSG_MBOX_SELECT_VALID_SRC)

    def browse_folder(self, line_edit):
        folder = QFileDialog.getExistingDirectory(self, MSG_DLG_SELECT_FOLDER)
        if folder:
            line_edit.setText(folder)

    def load_folder(self, folder):
        self.src_folder = folder
        self.all_files = []
        try:
            src = Path(folder)
            for p in src.rglob("*"):
                if p.is_file():
                    self.all_files.append(str(p))
        except Exception as e:
            QMessageBox.critical(self, MSG_MBOX_ERROR, MSG_MBOX_CANNOT_READ_FOLDER.format(e))
            return

        self.all_files.sort(key=lambda p: Path(p).name.lower())
        self.apply_filter()

    def apply_filter(self):
        filter_text = self.filter_edit.text().strip().lower()
        if not filter_text:
            self.filtered_files = self.all_files.copy()
        else:
            self.filtered_files = [f for f in self.all_files if filter_text in Path(f).name.lower()]

        self.refresh_file_list()

    def refresh_file_list(self):
        self.file_list.clear()
        for file_path in self.filtered_files:
            item = QListWidgetItem(Path(file_path).name)
            item.setData(Qt.UserRole, file_path)
            self.file_list.addItem(item)

        if self.filtered_files:
            self.file_list.setCurrentRow(0)
        else:
            self.preview_label.setText(MSG_PREVIEW_NO_MATCH)
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

    def _next_anim_frame(self):
        """播放动图下一帧（支持逐帧延迟）"""
        if not self.anim_frames:
            self.anim_timer.stop()
            return
        self.anim_index = (self.anim_index + 1) % len(self.anim_frames)
        label_size = self.preview_label.size()
        scaled = self.anim_frames[self.anim_index].scaled(
            label_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.preview_label.setPixmap(scaled)
        # 设置下一帧延迟
        if self.anim_delays:
            delay = self.anim_delays[self.anim_index % len(self.anim_delays)]
            self.anim_timer.setInterval(delay)

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

        self.anim_timer.stop()
        self.anim_frames = []
        self.anim_delays = []
        self.anim_index = 0
        self.preview_label.setScaledContents(False)
        self.preview_label.setPixmap(QPixmap())
        self.preview_label.setMovie(None)
        self.preview_label.setText("")

        for _ in range(3):
            QApplication.processEvents()
            QApplication.sendPostedEvents()

        gc.collect()

    def pil_to_qpixmap(self, pil_image):
        if pil_image.mode == "RGBA":
            qimage = QImage(pil_image.tobytes(), pil_image.width, pil_image.height, QImage.Format_RGBA8888)
        else:
            qimage = QImage(pil_image.tobytes(), pil_image.width, pil_image.height, QImage.Format_RGB888)
        return QPixmap.fromImage(qimage)

    def preview_file(self, file_path):
        self.clear_preview()
        ext = Path(file_path).suffix.lower()

        if ext == '.gif':
            movie = QMovie(file_path)
            if movie.isValid():
                self.preview_stack.setCurrentIndex(0)
                self.preview_label.setScaledContents(True)
                movie.setScaledSize(self.preview_label.size())
                self.preview_label.setMovie(movie)
                movie.start()
                self.current_movie = movie
                self.preview_label.setText("")
            else:
                self.preview_label.setText(MSG_PREVIEW_GIF_FAIL)

        elif ext in VIDEO_EXTENSIONS:
            url = QUrl.fromLocalFile(file_path)
            self.video_player.setSource(url)
            self.video_player.play()
            self.preview_stack.setCurrentIndex(1)
            self.play_pause_btn.setEnabled(True)
            self.play_pause_btn.setText(MSG_BTN_PAUSE)
            self.video_slider.setEnabled(True)

        elif ext in IMAGE_EXTENSIONS:
            # WebP 和 AVIF 需检测是否为动图
            if ext in ('.webp', '.avif'):
                if not HAS_PIL:
                    self.preview_label.setText(MSG_PREVIEW_NEED_PIL.format(ext))
                    return
                try:
                    pil_img = Image.open(file_path)
                    # 检测是否为动图
                    is_animated = getattr(pil_img, 'is_animated', False)
                    n_frames = getattr(pil_img, 'n_frames', 1)
                    if is_animated and n_frames > 1:
                        # 提取所有帧
                        frames = []
                        delays = []
                        for i in range(n_frames):
                            pil_img.seek(i)
                            frame = pil_img.copy()
                            if frame.mode not in ("RGB", "RGBA"):
                                frame = frame.convert("RGBA")
                            qpix = self.pil_to_qpixmap(frame)
                            frames.append(qpix)
                            # 帧延迟（毫秒），默认 100ms
                            dur = pil_img.info.get('duration', 100)
                            delays.append(dur)
                        self.anim_frames = frames
                        self.anim_delays = delays
                        self.anim_index = 0
                        self.preview_stack.setCurrentIndex(0)
                        label_size = self.preview_label.size()
                        scaled = frames[0].scaled(label_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                        self.preview_label.setPixmap(scaled)
                        self.preview_label.setText("")
                        # 启动定时器播放
                        self.anim_timer.start(delays[0] if delays else 100)
                    else:
                        # 静态图片处理
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
                            self.preview_label.setText(MSG_PREVIEW_GENERIC.format(ext))
                except Exception as e:
                    self.preview_label.setText(MSG_PREVIEW_LOAD_FAIL.format(ext, str(e)))
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
                    self.preview_label.setText(MSG_PREVIEW_IMG_FAIL)

        else:
            self.preview_stack.setCurrentIndex(0)
            icon = QIcon.fromTheme("video-x-generic")
            if not icon.isNull():
                pixmap = icon.pixmap(128, 128)
                self.preview_label.setPixmap(pixmap)
                self.preview_label.setText("")
            else:
                self.preview_label.setText(MSG_PREVIEW_CANNOT_PREVIEW.format(Path(file_path).name))

    def toggle_video_play(self):
        if self.video_player.playbackState() == QMediaPlayer.PlayingState:
            self.video_player.pause()
            self.play_pause_btn.setText(MSG_BTN_PLAY)
        else:
            self.video_player.play()
            self.play_pause_btn.setText(MSG_BTN_PAUSE)

    def update_buttons_state(self):
        has_file = self.current_file is not None and Path(self.current_file).is_file()
        self.discard_btn.setEnabled(has_file)
        self.keep_btn.setEnabled(has_file)
        self.hold_btn.setEnabled(has_file)
        self.random_btn.setEnabled(len(self.filtered_files) > 0)

    # ---------- 移动操作 ----------
    def move_file_with_retry(self, src, dst, max_retries=10, delay=1.0):
        for attempt in range(max_retries):
            try:
                shutil.move(str(src), str(dst))
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
        return False, MSG_UNKNOWN_ERROR

    def discard_current(self):
        if not self.current_file:
            return
        src_path = self.current_file
        self.clear_preview()  # 自动终止预览

        discard_folder = self.discard_path_edit.text().strip()
        use_recycle = self.recycle_check.isChecked()

        if use_recycle:
            if not HAS_SEND2TRASH:
                QMessageBox.critical(self, MSG_MBOX_ERROR, MSG_MBOX_NO_SEND2TRASH)
                return
            try:
                send2trash(src_path)
            except Exception as e:
                QMessageBox.critical(self, MSG_MBOX_ERROR, MSG_MBOX_TRASH_FAIL.format(e))
                return
            dest_info = ("回收站", None)
        else:
            if not discard_folder:
                QMessageBox.warning(self, MSG_MBOX_WARNING, MSG_MBOX_SPECIFY_DISCARD)
                return
            discard_path = Path(discard_folder)
            if not discard_path.is_dir():
                try:
                    discard_path.mkdir(parents=True, exist_ok=True)
                except Exception as e:
                    QMessageBox.critical(self, MSG_MBOX_ERROR, MSG_MBOX_CANNOT_CREATE_DISCARD.format(e))
                    return
            dest_path = str(discard_path / Path(src_path).name)
            success, error_msg = self.move_file_with_retry(src_path, dest_path)
            if not success:
                reply = QMessageBox.question(self, MSG_MBOX_MOVE_FAIL,
                                             MSG_MBOX_MOVE_FAIL_MSG.format(error_msg),
                                             QMessageBox.Retry | QMessageBox.Cancel)
                if reply == QMessageBox.Retry:
                    QMessageBox.information(self, MSG_MBOX_INFO, MSG_MBOX_RETRY_HINT)
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
            QMessageBox.warning(self, MSG_MBOX_WARNING, MSG_MBOX_SPECIFY_KEEP)
            return
        keep_path = Path(keep_folder)
        if not keep_path.is_dir():
            try:
                keep_path.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                QMessageBox.critical(self, MSG_MBOX_ERROR, MSG_MBOX_CANNOT_CREATE_KEEP.format(e))
                return
        dest_path = str(keep_path / Path(src_path).name)
        success, error_msg = self.move_file_with_retry(src_path, dest_path)
        if not success:
            reply = QMessageBox.question(self, MSG_MBOX_MOVE_FAIL,
                                         MSG_MBOX_MOVE_FAIL_MSG.format(error_msg),
                                         QMessageBox.Retry | QMessageBox.Cancel)
            if reply == QMessageBox.Retry:
                QMessageBox.information(self, MSG_MBOX_INFO, MSG_MBOX_RETRY_HINT)
            return

        self.history.append({
            'action': 'keep',
            'src': src_path,
            'dest': dest_path,
            'position': self.file_list.currentRow()
        })
        self.remove_current_from_list()

    def hold_current(self):
        """待定：不做移动，直接跳到下一个文件"""
        if not self.current_file:
            return
        self.select_next_file()

    def random_select(self):
        """随机选择一个文件进行预览"""
        if not self.filtered_files:
            QMessageBox.information(self, MSG_MBOX_INFO, MSG_MBOX_NO_FILES)
            return
        # 随机选择索引
        random_index = random.randint(0, len(self.filtered_files) - 1)
        self.file_list.setCurrentRow(random_index)

    def undo(self):
        if not self.history:
            QMessageBox.information(self, MSG_MBOX_UNDO, MSG_MBOX_NO_UNDO)
            return

        last = self.history[-1]
        if last['action'] == 'discard' and last['dest_info'][0] == "回收站":
            QMessageBox.information(self, MSG_MBOX_UNDO, MSG_MBOX_UNDO_RECYCLE)
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
                QMessageBox.critical(self, MSG_MBOX_ERROR, MSG_MBOX_UNDO_FAIL.format(e))
                return
        elif action == 'keep':
            dest_path = last['dest']
            try:
                shutil.move(dest_path, src)
            except Exception as e:
                QMessageBox.critical(self, MSG_MBOX_ERROR, MSG_MBOX_UNDO_FAIL.format(e))
                return

        self.all_files.append(src)
        self.all_files.sort(key=lambda p: Path(p).name.lower())
        self.apply_filter()
        try:
            new_index = self.filtered_files.index(src)
        except ValueError:
            new_index = 0
        self.file_list.setCurrentRow(new_index)

    def remove_current_from_list(self):
        """从内部数据中移除当前文件，并选中下一个文件（而不是回到第一个）"""
        if not self.current_file:
            return

        # 获取当前选中行索引
        current_index = self.file_list.currentRow()

        # 从数据中删除
        if self.current_file in self.all_files:
            self.all_files.remove(self.current_file)
        if self.current_file in self.filtered_files:
            self.filtered_files.remove(self.current_file)

        # 重建列表
        self.refresh_file_list()

        # 确定新的选中索引：如果删除的不是最后一项，则原下一个还在原位置；如果删除的是最后一项，则选上一个
        if self.filtered_files:
            if current_index < len(self.filtered_files):
                # 原下一个还在当前位置
                new_index = current_index
            else:
                # 原最后一项被删，新索引为前一个
                new_index = len(self.filtered_files) - 1
            self.file_list.setCurrentRow(new_index)

    def select_next_file(self):
        """选中列表中的下一个文件"""
        current_row = self.file_list.currentRow()
        if current_row < self.file_list.count() - 1:
            self.file_list.setCurrentRow(current_row + 1)
        else:
            if self.file_list.count() > 0:
                self.file_list.setCurrentRow(0)

    def closeEvent(self, event):
        self.clear_preview()
        super().closeEvent(event)


# ==================== 程序入口 ====================

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    app = QApplication(sys.argv)
    window = FileSorterApp()
    window.show()
    try:
        sys.exit(app.exec())
    except KeyboardInterrupt:
        print(MSG_INTERRUPTED)
    except Exception as e:
        print(MSG_ERROR.format(e))
    finally:
        input(MSG_EXIT)
