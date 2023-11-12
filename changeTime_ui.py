# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'changeTime.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QHeaderView,
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(571, 503)
        self.horizontalLayout_3 = QHBoxLayout(Form)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.table = QTableWidget(Form)
        if (self.table.columnCount() < 2):
            self.table.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.table.setObjectName(u"table")
        self.table.horizontalHeader().setDefaultSectionSize(65)
        self.table.verticalHeader().setDefaultSectionSize(50)

        self.horizontalLayout_3.addWidget(self.table)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.refresh = QPushButton(Form)
        self.refresh.setObjectName(u"refresh")

        self.horizontalLayout.addWidget(self.refresh)

        self.reset = QPushButton(Form)
        self.reset.setObjectName(u"reset")

        self.horizontalLayout.addWidget(self.reset)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.change = QPushButton(Form)
        self.change.setObjectName(u"change")

        self.horizontalLayout.addWidget(self.change)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.line_2 = QFrame(Form)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_2)

        self.img = QLabel(Form)
        self.img.setObjectName(u"img")

        self.verticalLayout.addWidget(self.img)

        self.fileName = QLabel(Form)
        self.fileName.setObjectName(u"fileName")
        font = QFont()
        font.setPointSize(20)
        self.fileName.setFont(font)

        self.verticalLayout.addWidget(self.fileName)

        self.line = QFrame(Form)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.setT = QPushButton(Form)
        self.setT.setObjectName(u"setT")

        self.horizontalLayout_4.addWidget(self.setT)

        self.setF = QPushButton(Form)
        self.setF.setObjectName(u"setF")

        self.horizontalLayout_4.addWidget(self.setF)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(2, 5)

        self.horizontalLayout_3.addLayout(self.verticalLayout)

        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 1)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        ___qtablewidgetitem = self.table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"\u6587\u4ef6\u540d", None));
        ___qtablewidgetitem1 = self.table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"\u5df2\u5220\u9664", None));
        self.refresh.setText(QCoreApplication.translate("Form", u"refresh", None))
        self.reset.setText(QCoreApplication.translate("Form", u"reset", None))
        self.change.setText(QCoreApplication.translate("Form", u"\u5207\u6362", None))
        self.img.setText(QCoreApplication.translate("Form", u"img", None))
        self.fileName.setText(QCoreApplication.translate("Form", u"Filename", None))
        self.setT.setText(QCoreApplication.translate("Form", u"\u8bbe\u7f6e\u4e3a\u662f", None))
        self.setF.setText(QCoreApplication.translate("Form", u"\u8bbe\u7f6e\u4e3a\u5426", None))
    # retranslateUi

