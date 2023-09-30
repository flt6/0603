# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'editLWSieV.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QProgressBar, QPushButton, QSizePolicy,
    QSlider, QSpacerItem, QTableWidget, QTableWidgetItem,
    QTextBrowser, QToolButton, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(599, 549)
        self.horizontalLayout_3 = QHBoxLayout(Form)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, -1, 10, 10)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(10, 20, 10, 20)
        self.add = QToolButton(Form)
        self.add.setObjectName(u"add")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.add.sizePolicy().hasHeightForWidth())
        self.add.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.add)

        self.horizontalSpacer = QSpacerItem(20, 10, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.sub = QToolButton(Form)
        self.sub.setObjectName(u"sub")
        sizePolicy.setHeightForWidth(self.sub.sizePolicy().hasHeightForWidth())
        self.sub.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.sub)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.names = QTableWidget(Form)
        if (self.names.columnCount() < 1):
            self.names.setColumnCount(1)
        __qtablewidgetitem = QTableWidgetItem()
        self.names.setHorizontalHeaderItem(0, __qtablewidgetitem)
        self.names.setObjectName(u"names")

        self.verticalLayout.addWidget(self.names)

        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 5)

        self.horizontalLayout_3.addLayout(self.verticalLayout)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, 10, -1, 10)
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.optDir = QLineEdit(Form)
        self.optDir.setObjectName(u"optDir")

        self.horizontalLayout_2.addWidget(self.optDir)

        self.start = QPushButton(Form)
        self.start.setObjectName(u"start")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.start.sizePolicy().hasHeightForWidth())
        self.start.setSizePolicy(sizePolicy1)

        self.horizontalLayout_2.addWidget(self.start)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_4.addWidget(self.label_3)

        self.size = QSlider(Form)
        self.size.setObjectName(u"size")
        self.size.setMinimum(200)
        self.size.setMaximum(600)
        self.size.setSingleStep(1)
        self.size.setValue(350)
        self.size.setOrientation(Qt.Horizontal)

        self.horizontalLayout_4.addWidget(self.size)

        self.sizeLabel = QLabel(Form)
        self.sizeLabel.setObjectName(u"sizeLabel")

        self.horizontalLayout_4.addWidget(self.sizeLabel)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.log = QTextBrowser(Form)
        self.log.setObjectName(u"log")

        self.verticalLayout_2.addWidget(self.log)


        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        self.progressBar = QProgressBar(Form)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)

        self.verticalLayout_3.addWidget(self.progressBar)


        self.horizontalLayout_3.addLayout(self.verticalLayout_3)

        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 2)

        self.retranslateUi(Form)
        self.optDir.returnPressed.connect(self.start.click)
        self.size.sliderMoved.connect(self.sizeLabel.setNum)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.add.setText(QCoreApplication.translate("Form", u"+", None))
        self.sub.setText(QCoreApplication.translate("Form", u"-", None))
        ___qtablewidgetitem = self.names.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"names", None));
        self.label_2.setText(QCoreApplication.translate("Form", u"\u8f93\u51fa\u6587\u4ef6\u5939", None))
        self.optDir.setText(QCoreApplication.translate("Form", u"imgs", None))
        self.start.setText(QCoreApplication.translate("Form", u"\u542f\u52a8", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u5b57\u4f53\u5927\u5c0f", None))
        self.sizeLabel.setText(QCoreApplication.translate("Form", u"350", None))
        self.label.setText(QCoreApplication.translate("Form", u"Log", None))
    # retranslateUi

