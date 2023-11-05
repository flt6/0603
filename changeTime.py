from typing import Optional
from PySide6.QtWidgets import (
    QApplication,
    QErrorMessage,
    QMessageBox,
    QLabel,
    QGridLayout,
    QSizePolicy
)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QPixmap, QImageReader,QCloseEvent,QKeyEvent
from PySide6.QtCore import Qt, QTimer, QPoint,QEvent,QObject,Signal,Slot
import changeTime_ui
from main import AutoChoose
import sys

class DevTool(QObject):
    def __init__(self, parent: QObject | None = ...) -> None:
        super().__init__(parent)
        self.ui = changeTime_ui.Ui_Form()
        self.ui.setupUi(self)
        self.ui.reload.clicked.connect(self.setupImgs)
        self.ui.reset.clicked.connect(self._reset)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = QUiLoader().load("changeTime.ui")
    win.show()
    sys.exit(app.exec())