from pathlib import Path
from threading import Thread

from PySide6.QtCore import QObject, Qt, Signal
from PySide6.QtGui import (QClipboard, QColor, QFont, QImage, QKeySequence,
                           QPainter, QShortcut)
from PySide6.QtWidgets import (QApplication, QMessageBox, QTableWidgetItem,
                               QWidget)

import _editUI

WID = 1800
HEI = 900


class MySignal(QObject):
    writeLog = Signal(str)
    update = Signal()

    def run(self, log):
        self.writeLog.emit(log)
        self.update.emit()


class Edit:
    def __init__(self, form: QWidget) -> None:
        self.ui = _editUI.Ui_Form()
        self._form = form
        self.ui.setupUi(form)
        self.sig = MySignal(form)
        self.progress = 0
        self.sig.writeLog.connect(self.ui.log.append)
        self.sig.update.connect(self.update)
        self.ui.add.clicked.connect(self.add)
        self.ui.sub.clicked.connect(self.sub)
        self.ui.start.clicked.connect(self.start)
        QShortcut(QKeySequence.StandardKey.Paste, self._form).activated.connect(
            self.paste
        )

    def paste(self):
        clip = QClipboard()
        t = clip.text().splitlines()
        prefix = self.ui.names.rowCount()
        self.ui.names.setRowCount(self.ui.names.rowCount() + len(t))
        for i, line in enumerate(t):
            item = QTableWidgetItem()
            item.setText(line.strip())
            self.ui.names.setItem(prefix + i, 0, item)

    def update(self):
        print("tmp")
        self.progress += 1
        self.ui.progressBar.setValue(self.progress)

    def add(self):
        if self.ui.names.currentRow() < 0:
            self.ui.names.insertRow(self.ui.names.rowCount())
        self.ui.names.insertRow(self.ui.names.currentRow() + 1)

    def sub(self):
        ran = self.ui.names.selectedRanges()[0]
        print(ran.topRow(), ran.bottomRow())
        for i in range(ran.rowCount()):
            self.ui.names.removeRow(ran.topRow())

    def start(self):
        optDir = Path(self.ui.optDir.text())
        if not optDir.exists():
            yes = QMessageBox.StandardButton.Yes
            no = QMessageBox.StandardButton.No
            choose = QMessageBox.warning(self._form, "Warning", "文件夹不存在，是否创建？", yes, no)
            if choose == yes:
                optDir.mkdir()
            else:
                QMessageBox.about(self._form, "Question", "无法访问对应文件夹")
                return
        if optDir.is_file():
            QMessageBox.critical(self._form, "Error", "指定路径是文件")
            return
        names = []
        for i in range(self.ui.names.rowCount()):
            names.append(self.ui.names.item(i, 0).text().strip())
        self.ui.progressBar.reset()
        self.progress = 0
        self.ui.progressBar.setMaximum(len(names))
        Thread(target=self.createImage, args=(optDir, names)).start()

    def createImage(self, optDir, names):
        for name in names:
            img = self.draw_text(name)
            self.sig.run(f"Created {optDir/name}.png")
            img.save(str(optDir / f"{name}.png"))

    def draw_text(self, name):
        img = QImage(WID, HEI, QImage.Format.Format_RGB32)
        painter = QPainter()
        painter.begin(img)

        bgColor = QColor(255, 255, 255)
        painter.setBrush(bgColor)
        painter.drawRect(img.rect())

        font = QFont("微软雅黑", self.ui.size.value())
        font.setBold(True)
        painter.setFont(font)
        penColor = QColor(0, 0, 0)
        painter.setPen(penColor)

        text_rect = painter.boundingRect(img.rect(), Qt.AlignmentFlag.AlignCenter, name)
        painter.drawText(text_rect, name)

        painter.end()
        return img


if __name__ == "__main__":
    app = QApplication()
    ui = QWidget()
    edit = Edit(ui)
    ui.show()
    app.exec()
