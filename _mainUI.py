# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainpywMkG.ui'
##
## Created by: Qt User Interface Compiler version 6.4.3
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QToolButton, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(624, 449)
        font = QFont()
        font.setPointSize(14)
        Form.setFont(font)
        self.horizontalLayout_2 = QHBoxLayout(Form)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, 20, -1, 20)
        self.start_2 = QPushButton(Form)
        self.start_2.setObjectName(u"start_2")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.start_2.sizePolicy().hasHeightForWidth())
        self.start_2.setSizePolicy(sizePolicy)
        self.start_2.setMinimumSize(QSize(0, 0))
        self.start_2.setSizeIncrement(QSize(0, 0))
        self.start_2.setBaseSize(QSize(100, 100))
        font1 = QFont()
        font1.setPointSize(20)
        self.start_2.setFont(font1)
        self.start_2.setMouseTracking(False)
        self.start_2.setAutoFillBackground(False)
        self.start_2.setAutoDefault(False)
        self.start_2.setFlat(False)

        self.verticalLayout.addWidget(self.start_2)

        self.verticalSpacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Preferred)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.end_2 = QPushButton(Form)
        self.end_2.setObjectName(u"end_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.end_2.sizePolicy().hasHeightForWidth())
        self.end_2.setSizePolicy(sizePolicy1)
        self.end_2.setFont(font1)

        self.verticalLayout.addWidget(self.end_2)

        self.reload = QToolButton(Form)
        self.reload.setObjectName(u"reload")
        sizePolicy.setHeightForWidth(self.reload.sizePolicy().hasHeightForWidth())
        self.reload.setSizePolicy(sizePolicy)
        font2 = QFont()
        font2.setPointSize(12)
        self.reload.setFont(font2)

        self.verticalLayout.addWidget(self.reload)

        self.verticalLayout.setStretch(0, 2)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 2)

        self.horizontalLayout.addLayout(self.verticalLayout)

        self.img = QLabel(Form)
        self.img.setObjectName(u"img")
        self.img.setFont(font1)
        self.img.setTextFormat(Qt.PlainText)
        self.img.setScaledContents(False)
        self.img.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.img)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(-1, 20, -1, 20)
        self.start = QPushButton(Form)
        self.start.setObjectName(u"start")
        sizePolicy1.setHeightForWidth(self.start.sizePolicy().hasHeightForWidth())
        self.start.setSizePolicy(sizePolicy1)
        self.start.setMinimumSize(QSize(0, 0))
        self.start.setSizeIncrement(QSize(0, 0))
        self.start.setBaseSize(QSize(100, 100))
        self.start.setFont(font1)

        self.verticalLayout_2.addWidget(self.start)

        self.verticalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Preferred)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.end = QPushButton(Form)
        self.end.setObjectName(u"end")
        sizePolicy1.setHeightForWidth(self.end.sizePolicy().hasHeightForWidth())
        self.end.setSizePolicy(sizePolicy1)
        self.end.setFont(font1)

        self.verticalLayout_2.addWidget(self.end)

        self.reset = QToolButton(Form)
        self.reset.setObjectName(u"reset")
        sizePolicy.setHeightForWidth(self.reset.sizePolicy().hasHeightForWidth())
        self.reset.setSizePolicy(sizePolicy)
        self.reset.setFont(font2)

        self.verticalLayout_2.addWidget(self.reset)

        self.verticalLayout_2.setStretch(0, 2)
        self.verticalLayout_2.setStretch(1, 1)
        self.verticalLayout_2.setStretch(2, 2)

        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 3)
        self.horizontalLayout.setStretch(2, 1)

        self.horizontalLayout_2.addLayout(self.horizontalLayout)


        self.retranslateUi(Form)

        self.start_2.setDefault(False)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.start_2.setText(QCoreApplication.translate("Form", u"Start", None))
        self.end_2.setText(QCoreApplication.translate("Form", u"End", None))
        self.reload.setText(QCoreApplication.translate("Form", u"\u91cd\u65b0\u52a0\u8f7d\u56fe\u7247", None))
        self.img.setText(QCoreApplication.translate("Form", u"Loading...", None))
        self.start.setText(QCoreApplication.translate("Form", u"Start", None))
        self.end.setText(QCoreApplication.translate("Form", u"End", None))
        self.reset.setText(QCoreApplication.translate("Form", u"\u91cd\u7f6e\u56fe\u7247\u5217\u8868", None))
    # retranslateUi

