from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QErrorMessage,
    QMessageBox,
    QLabel,
    QGridLayout,
    QSizePolicy,
)
from PySide6.QtGui import QPixmap, QImageReader
from PySide6.QtCore import Qt, QTimer, QPoint,QEvent,QObject
import _mainUI
from random import shuffle
from pathlib import Path
from time import time
import ctypes

IMG_DIR = Path("imgs")
WAIT_TIME = 60


class AutoChoose(QObject):
    def __init__(self, Form: QWidget) -> None:
        super().__init__()
        self.ui = _mainUI.Ui_Form()
        self._form = Form
        self.ui.setupUi(Form)
        self.removed = {}
        self._cur = None
        self.img_gen = self._choose()
        self.timer = QTimer(Form)
        self.timer.timeout.connect(self.choose)
        self.ui.start.pressed.connect(self.start)
        self.ui.end.pressed.connect(self.stop)
        self.ui.start_2.pressed.connect(self.start)
        self.ui.end_2.pressed.connect(self.stop)
        self.ui.reload.pressed.connect(self.setupImgs)
        self.ui.reset.pressed.connect(self._reset)
        self.ui.reset.released.connect(self._resetRelease)
        self.ui.reset.installEventFilter(self)
        self._form.resizeEvent = self._resized
        self.resize_timmer = QTimer(Form)
        self.resize_timmer.setSingleShot(True)
        self.resize_timmer.timeout.connect(self.resizing_end)
        self.setupImgs()

        scr = QApplication.primaryScreen().size()
        print("Screen size:", scr)
        self._form.setGeometry(
            scr.width() * 0.1,
            scr.height() * 0.1,
            scr.width() * 0.75,
            scr.height() * 0.7,
        )
    
    def eventFilter(self,obj,event):
        if obj==self.ui.reset:
            if event.type()==QEvent.Type.TouchBegin:
                self.ui.reset.setDown(True)
            elif event.type()==QEvent.Type.TouchEnd:
                self.ui.reset.setDown(False)
        return False

    def _resized(self, event):
        self.ui.img.clear()
        self.ui.img.setText("Loading...")
        self.timer.stop()
        self.resize_timmer.start(500)

    def resizing_end(self):
        self.setupImgs()

    def start(self):
        if self.timer.isActive():
            QMessageBox().warning(self._form, "Warning", "已经启动，请勿重复运行。")
            return
        cnt = 0
        cur = time()
        for val in self.removed.values():
            if cur >= val:
                cnt += 1
        print(
            f"Image list health condition: {cnt}/{len(self.removed)} ({cnt*100/len(self.removed)}%)"
        )
        if cnt == 1:
            QMessageBox.information(self._form, "Info", "图片数量仅剩1张，自动重置。")
            self.reset()
        elif cnt <= 10:
            btn_yes = QMessageBox.StandardButton.Yes
            btn_no = QMessageBox.StandardButton.No
            if (
                QMessageBox.warning(
                    self._form, "Warning", "图片数量少于10张，是否重置图片列表？", btn_yes, btn_no
                )
                == btn_yes
            ):
                self.reset()
        self.timer.start(WAIT_TIME)

    def stop(self):
        if not self.timer.isActive():
            return
        self.timer.stop()
        if self._cur is None:
            QMessageBox.about(self._form, "Question", "还没换图就点End了？")
            return
        self.removed[self._cur] = time() + 60 * 40
        self.img_gen = self._choose()
        self._cur = None

    def _choose(self):
        while True:
            keys = list(self.imgs.keys())
            shuffle(keys)
            for key in keys:
                if time() >= self.removed[key]:
                    yield key, self.imgs[key]

    def choose(self):
        self._cur, img = next(self.img_gen)
        if img is None:
            return
        self.ui.img.setPixmap(img)

    def _reset(self):
        self._tmp = time()
        print(self._tmp)

    def _resetRelease(self):
        print(time() - self._tmp)
        if time() - self._tmp < 1:
            self.reset()
        else:
            print("Removed list: ")
            cur = time()
            for name, wait in self.removed.items():
                if cur < wait:
                    print("%-15s: %.2f (Left: %.2f)" % (name, wait, wait - cur))
        self._tmp = None

    def reset(self):
        for key in self.removed.keys():
            self.removed[key] = 0

    def setupImgs(self):
        self.timer.stop()
        self.ui.img.clear()
        self.imgs = {}
        self._size = self.ui.img.size()
        for file in IMG_DIR.iterdir():
            try:
                img = QImageReader(str(file.resolve()))
                img.setAutoTransform(True)
                img = QPixmap.fromImageReader(img)
                self.imgs[file.name] = img.scaled(
                    self._size, Qt.AspectRatioMode.KeepAspectRatio
                )
                self.removed[file.name] = 0
            except Exception as e:
                err = QErrorMessage()
                err.showMessage(
                    f"Filed to import image {file}: {e}".replace("\n", "<br>")
                )
                err.exec()
        self.img_gen = self._choose()
        self.choose()


class FloatingWindow(QWidget):
    def __init__(self, win: QWidget):
        super().__init__()
        self.win = win
        self._winCloseEvent = self.win.closeEvent
        self.win.closeEvent = self._close

        # 设置窗口属性
        self.setWindowFlags(
            self.windowFlags()|
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )

        # 设置窗口初始位置和大小
        scr = QApplication.primaryScreen().size()
        print("Screen size:", scr)
        self.setGeometry(
            scr.width() * 0.9,
            scr.height() * 0.8,
            scr.width() * 0.03,
            scr.width() * 0.03,
        )
        self.setWindowOpacity(0.7)

        self.label = QLabel(self)
        self.label.setText("激活")
        self.label.setAlignment(Qt.AlignCenter)

        sizePolicy = QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())

        self.label.setSizePolicy(sizePolicy)
        self.label.setStyleSheet("background-color: rgb(98, 255, 237);")

        gridLayout = QGridLayout(self)
        gridLayout.setContentsMargins(0, 0, 0, 0)
        gridLayout.addWidget(self.label)

        # 初始化鼠标偏移
        self.drag_position = None

    def _close(self, e):
        self.close()
        self._winCloseEvent(e)

    def mousePressEvent(self, event):
        # 记录鼠标按下时的位置，用于拖动窗口
        self.drag_position = event.globalPosition().toPoint()
        self.init_pos = self.drag_position

    def mouseMoveEvent(self, event):
        # 计算鼠标移动的偏移量，并移动窗口
        if self.drag_position:
            cur = event.globalPosition().toPoint()
            delta = cur - self.drag_position
            if (cur - self.init_pos).manhattanLength() < 10:
                return
            self.move(self.pos() + delta)
            self.drag_position = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        # 清除鼠标偏移
        delta: QPoint = event.globalPosition().toPoint() - self.init_pos
        if delta.manhattanLength() < 10:
            self.onclik()
        self.drag_position = None

    def onclik(self):
        self.win.showNormal()
        self.win.raise_()
        self.win.setWindowFlags(
            self.win.windowFlags() | Qt.WindowType.WindowStaysOnTopHint
        )
        self.win.setWindowFlags(
            self.win.windowFlags() & ~Qt.WindowType.WindowStaysOnTopHint
        )
        self.win.show()


class FloatWindowOnce(FloatingWindow):
    def __init__(self, win: QWidget, main: AutoChoose):
        super().__init__(win)
        self._main = main

        self.timer = QTimer(win)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self._main.stop)

        self.label.setText("选一个")
        self.label.setStyleSheet("background-color: #58dc2a;")

        scr = QApplication.primaryScreen().size()
        print("Screen size:", scr)
        self.setGeometry(
            scr.width() * 0.1,
            scr.height() * 0.8,
            scr.width() * 0.03,
            scr.width() * 0.03,
        )

    def onclik(self):
        super().onclik()
        self._main.start()
        self.timer.start(300)

# class ChangeTime:
#     def __init__(self, Form: QWidget, main:AutoChoose) -> None:
#         self.ui = _mainUI.Ui_Form()
#         self._form = Form
#         self._main = main
#         self.ui.setupUi(Form)
#         self.

if __name__ == "__main__":
    app = QApplication()
    ui = QWidget()
    main = AutoChoose(ui)
    ui.show()
    floatWin = FloatingWindow(ui)
    floatWin.show()
    once = FloatWindowOnce(ui, main)
    once.show()
    # chTime=ChangeTime(ui,main)
    # chTimeUI=QWidget(ui)
    # chTimeUI.show()
    app.exec()
