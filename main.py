from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QErrorMessage,
    QMessageBox,
    QLabel,
    QGridLayout,
    QSizePolicy,
    QTableWidgetItem
)
from PySide6.QtGui import QPixmap, QImageReader,QCloseEvent,QKeyEvent,QColor
from PySide6.QtCore import Qt, QTimer, QPoint,QEvent,QObject,Signal,Slot
import _mainUI,ui_changeTime
from random import shuffle
from json import dump,load,JSONDecodeError
from traceback import format_exc
from pathlib import Path
from time import time
from threading import Thread
from sys import exit

IMG_DIR = Path("imgs")
REMOVE_CFG=Path("removed.json")
WAIT_TIME = 60

class Worker(QObject):
    errorSignal = Signal(str,bool)
    devSignal = Signal()

    def run(self,e:str,_exit:bool=False):
        self.errorSignal.emit(e.replace("\n","<br>"),_exit)

class AutoChoose(QObject):
    def __init__(self, Form: QWidget,worker:Worker) -> None:
        super().__init__()
        self.ui = _mainUI.Ui_Form()
        self._form = Form
        self.ui.setupUi(Form)

        try:
            with open(REMOVE_CFG,"r",encoding="utf-8") as f:
                self.removed:dict[str,bool] = load(f)
                print("[+] Loaded config from "+str(REMOVE_CFG))
        except FileNotFoundError:
            print("[-] No removed config found.")
        except JSONDecodeError as e:
            QErrorMessage().showMessage(f"Cannot decode json: <br>"+format_exc(e).replace("\n","<br>"))
    
        if not hasattr(self,"removed"):
            print(1)
            self.removed:dict[str,bool] = {}
        
        self._cur = None
        self.img_gen = self._choose()
        self.timer = QTimer(Form)
        self.timer.timeout.connect(self.choose)

        self.ui.start.pressed.connect(self.start)
        self.ui.end.pressed.connect(self.stop)
        self.ui.start_2.pressed.connect(self.start)
        self.ui.end_2.pressed.connect(self.stop)

        self._form.resizeEvent = self._resized

        self._showEvent=self._form.showEvent
        self._form.showEvent=self.showEv
        self._firstStart=True

        self.block_timmer = QTimer(Form)
        self.block_timmer.setSingleShot(True)
        self._block=True
        def unblock():
            self._block=False
        self.block_timmer.timeout.connect(unblock)

        self.worker=worker
        self.worker.errorSignal.connect(self.showErr)
        self.foreceQuit=False

        self.resize_timmer = QTimer(Form)
        self.resize_timmer.setSingleShot(True)
        self.resize_timmer.timeout.connect(self.resizing_end)
        self.before_resize=None

        self._form.keyPressEvent=self.keyPressEvent
        self.keyLog="###"

        scr = QApplication.primaryScreen().size()
        print("Screen size:", scr)
        self._form.setGeometry(
            scr.width() * 0.1,
            scr.height() * 0.1,
            scr.width() * 0.75,
            scr.height() * 0.7,
        )
    
    def closeEv(self,event:QCloseEvent):
        if self.foreceQuit:
            event.accept()
            return
        btn_yes = QMessageBox.StandardButton.Yes
        btn_no = QMessageBox.StandardButton.No
        if (
            QMessageBox.question(
                self._form, "退出", "退出软件？", btn_yes, btn_no
            )
        == btn_yes
        ):
            event.accept()
        else:
            event.ignore()
    
    def showErr(self,msg:str,_exit:bool):
        err = QErrorMessage()
        err.showMessage(msg)
        err.exec()
        if _exit:
            self.foreceQuit=True
            app.quit()

    def showEv(self,event):
        self._showEvent(event)
        if self._firstStart:
            self._firstStart=False
            self.block_timmer.start(1000)
            Thread(target=self.setupImgs).start()

    def keyPressEvent(self, event: QKeyEvent):
        key = event.text()
        self.keyLog+=key
        self.keyLog=self.keyLog[1:]
        if self.keyLog=="dev":
            self.worker.devSignal.emit()
        

    def _resized(self, event):
        self.ui.img.clear()
        self.ui.img.setText("Loading...")
        if self.before_resize is None:
            self.before_resize=self._form.geometry()
        self.timer.stop()
        self.resize_timmer.start(500)

    def resizing_end(self):
        if not self._block:
            Thread(target=self.setupImgs).start()

    def start(self):
        if self.timer.isActive():
            QMessageBox().warning(self._form, "Warning", "已经启动，请勿重复运行。")
            return
        cnt = 0
        for ignore in self.removed.values():
            if not ignore:
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
        self.removed[self._cur] = True
        self._cur = None
        with open(REMOVE_CFG,"w",encoding="utf-8") as f:
            dump(self.removed,f)

    def _choose(self):
        while True:
            keys = list(self.imgs.keys())
            shuffle(keys)
            for key in keys:
                if not self.removed[key]:
                    yield key, self.imgs[key]

    def choose(self):
        self._cur, img = next(self.img_gen)
        if img is None:
            return
        self.ui.img.setPixmap(img)

    def reset(self):
        for key in self.removed.keys():
            self.removed[key] = False

    def setupImgs(self):
        self.timer.stop()
        self.ui.img.clear()
        self.imgs = {}
        self._size = self.ui.img.size()
        print(1, self.ui.img.size())
        if not IMG_DIR.is_dir():
            self.worker.run("Target dir <b>'{}'</b> not exists.".format(str(IMG_DIR)),True)
            return
        for file in IMG_DIR.iterdir():
            try:
                img = QImageReader(str(file.resolve()))
                img.setAutoTransform(True)
                img = QPixmap.fromImageReader(img)
                self.imgs[file.name] = img.scaled(
                    self._size, Qt.AspectRatioMode.KeepAspectRatio
                )
                if file.name not in self.removed.keys():
                    self.removed[file.name] = False
            except Exception as e:
                self.worker.run(f"Filed to import image {file}: {e}",False)
        self.img_gen = self._choose()
        self.choose()
        print(2,self.ui.img.size())


class DevTool(QWidget):
    def __init__(self, main:AutoChoose,worker:Worker) -> None:
        super().__init__()
        self.ui = ui_changeTime.Ui_Form()
        self.ui.setupUi(self)
        self.main=main
        self.ui.refresh.clicked.connect(self.load)
        self.ui.reset.clicked.connect(self.main.reset)
        self.ui.change.clicked.connect(self.change)
        self.worker=worker
        self.worker.devSignal.connect(self._show)
        self.load()

    def _show(self):
        self.show()
        self.load()
    
    def load(self):
        for row in range(self.ui.table.rowCount()):
            self.ui.table.removeRow(row)
        d=self.main.removed
        for i,(key,val) in enumerate(d.items()):
            self.ui.table.insertRow(i)
            self.ui.table.setItem(i,0,QTableWidgetItem())
            self.ui.table.setItem(i,1,QTableWidgetItem())
            fileName=self.ui.table.item(i,0)
            isRemoved=self.ui.table.item(i,1)
            fileName.setText(key)
            isRemoved.setText(str(val))
            if val:
                fileName.setBackground(QColor("lightblue"))
                isRemoved.setBackground(QColor("lightblue"))


    def change(self):
        pass


class FloatingWindow(QWidget):
    def __init__(self, win: QWidget):
        super().__init__()
        self.win = win
        self._winCloseEvent = self.win.closeEvent
        self.win.closeEvent = self._close

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("border-radius: 10px;")

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

    def _close(self, e:QCloseEvent):
        self._winCloseEvent(e)
        if e.isAccepted():
            self.close()

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

if __name__ == "__main__":
    app = QApplication()
    ui = QWidget()
    worker=Worker()
    try:
        main = AutoChoose(ui,worker)
        ui.closeEvent=main.closeEv
        
    except Exception:
        err = QErrorMessage()
        err.showMessage("Failed to inititalize 'AutoChoose'<br>"+format_exc().replace("\n","<br>"))
        err.exec()
    ui.show()
    try:
        floatWin = FloatingWindow(ui)
        floatWin.show()
        once = FloatWindowOnce(ui, main)
        once.show()
    except Exception:
        QErrorMessage().showMessage("Failed to inititalize Floating Window<br>"+format_exc().replace("\n","<br>"))
    

    dev=DevTool(main,worker)
    dev.show()

    app.exec()
