# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_Rec_Window(object):
    def setupUi(self, Rec_Window):
        if not Rec_Window.objectName():
            Rec_Window.setObjectName(u"Rec_Window")
        Rec_Window.resize(405, 110)
        Rec_Window.setMinimumSize(QSize(405, 110))
        Rec_Window.setMaximumSize(QSize(405, 110))
        self.centralwidget = QWidget(Rec_Window)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_3 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setMaximumSize(QSize(16777215, 16777215))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.Layout_directory = QHBoxLayout()
        self.Layout_directory.setObjectName(u"Layout_directory")
        self.LineEdit_directory = QLineEdit(self.frame)
        self.LineEdit_directory.setObjectName(u"LineEdit_directory")
        self.LineEdit_directory.setMinimumSize(QSize(0, 0))
        self.LineEdit_directory.setMaximumSize(QSize(300, 30))

        self.Layout_directory.addWidget(self.LineEdit_directory)

        self.btn_directory = QPushButton(self.frame)
        self.btn_directory.setObjectName(u"btn_directory")
        self.btn_directory.setMinimumSize(QSize(0, 0))
        self.btn_directory.setMaximumSize(QSize(75, 30))

        self.Layout_directory.addWidget(self.btn_directory)


        self.verticalLayout.addLayout(self.Layout_directory)

        self.Layout_btn = QHBoxLayout()
        self.Layout_btn.setSpacing(20)
        self.Layout_btn.setObjectName(u"Layout_btn")
        self.btn_stop = QPushButton(self.frame)
        self.btn_stop.setObjectName(u"btn_stop")
        self.btn_stop.setMinimumSize(QSize(0, 30))
        self.btn_stop.setMaximumSize(QSize(30, 30))

        self.Layout_btn.addWidget(self.btn_stop)

        self.btn_pause = QPushButton(self.frame)
        self.btn_pause.setObjectName(u"btn_pause")
        self.btn_pause.setMinimumSize(QSize(0, 0))
        self.btn_pause.setMaximumSize(QSize(30, 30))

        self.Layout_btn.addWidget(self.btn_pause)

        self.btn_play = QPushButton(self.frame)
        self.btn_play.setObjectName(u"btn_play")
        self.btn_play.setMinimumSize(QSize(0, 0))
        self.btn_play.setMaximumSize(QSize(30, 30))

        self.Layout_btn.addWidget(self.btn_play)

        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(13)
        font.setBold(True)
        self.label.setFont(font)

        self.Layout_btn.addWidget(self.label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.Layout_btn.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.Layout_btn)


        self.horizontalLayout_3.addWidget(self.frame)

        Rec_Window.setCentralWidget(self.centralwidget)

        self.retranslateUi(Rec_Window)

        QMetaObject.connectSlotsByName(Rec_Window)
    # setupUi

    def retranslateUi(self, Rec_Window):
        Rec_Window.setWindowTitle(QCoreApplication.translate("Rec_Window", u"MainWindow", None))
        self.btn_directory.setText(QCoreApplication.translate("Rec_Window", u"\u0418\u0437\u043c\u0435\u043d\u0438\u0442\u044c...", None))
        self.btn_stop.setText("")
        self.btn_pause.setText("")
        self.btn_play.setText("")
        self.label.setText("")
    # retranslateUi

