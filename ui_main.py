
from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *

from PyQt5 import QtCore, QtGui, QtWidgets
from codee import simpleNetworkSEIQRModel
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QPixmap, QRegExpValidator, QDoubleValidator
import time
import sys
import pandas as pd


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1000, 500)
        MainWindow.setMinimumSize(QSize(1000, 500))
        MainWindow.setStyleSheet(u"background-color: rgb(240, 245, 246);")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.Top_Bar = QFrame(self.centralwidget)
        self.Top_Bar.setObjectName(u"Top_Bar")
        self.Top_Bar.setMaximumSize(QSize(16777215, 80))
        self.Top_Bar.setStyleSheet(u"background-color: rgb(168, 193, 232);")
        self.Top_Bar.setFrameShape(QFrame.NoFrame)
        self.Top_Bar.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.Top_Bar)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_toggle = QFrame(self.Top_Bar)
        self.frame_toggle.setObjectName(u"frame_toggle")
        self.frame_toggle.setMaximumSize(QSize(70, 40))
        self.frame_toggle.setStyleSheet(u"background-color: rgb(85, 170, 255);")
        self.frame_toggle.setFrameShape(QFrame.StyledPanel)
        self.frame_toggle.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_toggle)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.Btn_Toggle = QPushButton(self.frame_toggle)
        self.Btn_Toggle.setObjectName(u"Btn_Toggle")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Btn_Toggle.sizePolicy().hasHeightForWidth())
        self.Btn_Toggle.setSizePolicy(sizePolicy)
        self.Btn_Toggle.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"border: 0px solid;")

        self.verticalLayout_2.addWidget(self.Btn_Toggle)


        self.horizontalLayout.addWidget(self.frame_toggle)

        self.frame_top = QFrame(self.Top_Bar)
        self.frame_top.setObjectName(u"frame_top")
        self.frame_top.setFrameShape(QFrame.StyledPanel)
        self.frame_top.setFrameShadow(QFrame.Raised)

        validator = QRegExpValidator(QRegExp(r'[1-9]+[0-9]*'))
        validator_float = QRegExpValidator(QRegExp(r'0\.[0-9]+'))

        self.gridLayout = QtWidgets.QGridLayout(self.frame_top)
        self.gridLayout.setObjectName("gridLayout")

        self.lineEdit_Susceptible = QtWidgets.QLineEdit(self.frame_top)
        self.lineEdit_Susceptible.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_Susceptible.setFont(font)
        self.lineEdit_Susceptible.setStyleSheet("QLineEdit{\n"
"    border: none;\n"
"    border-top: 2px solid rgb(255, 99, 71);\n"
"    color: rgb(0, 0, 0);\n"
"    background-color: transparent;\n"
"    padding: 3px;\n"
"    width: 180px;\n"
"}\n"
"")
        self.lineEdit_Susceptible.setValidator(validator)
        self.lineEdit_Susceptible.setText("")
        self.lineEdit_Susceptible.setObjectName("lineEdit_Susceptible")
        self.gridLayout.addWidget(self.lineEdit_Susceptible, 0, 0, 1, 1)

        self.lineEdit_Infected = QtWidgets.QLineEdit(self.frame_top)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_Infected.setFont(font)
        self.lineEdit_Infected.setStyleSheet("QLineEdit{\n"
"    border: none;\n"
"    border-top: 2px solid rgb(255, 99, 71);\n"
"    color: rgb(0, 0, 0);\n"
"    background-color: transparent;\n"
"    padding: 3px;\n"
"    width: 180px;\n"
"}\n"
"")
        self.lineEdit_Infected.setValidator(validator)
        self.lineEdit_Infected.setObjectName("lineEdit_Infected")
        self.gridLayout.addWidget(self.lineEdit_Infected, 0, 1, 1, 1)

        self.lineEdit_Beta = QtWidgets.QLineEdit(self.frame_top)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_Beta.setFont(font)
        self.lineEdit_Beta.setStyleSheet("QLineEdit{\n"
"    border: none;\n"
"    border-top: 2px solid rgb(255, 99, 71);\n"
"    color: rgb(0, 0, 0);\n"
"    background-color: transparent;\n"
"    padding: 3px;\n"
"    width: 180px;\n"
"}\n"
"")
        self.lineEdit_Beta.setValidator(validator_float) #QDoubleValidator(0.00, 1.00,3)
        self.lineEdit_Beta.setObjectName("lineEdit_Beta")
        self.gridLayout.addWidget(self.lineEdit_Beta, 0, 2, 1, 1)

        self.lineEdit_Epsilon = QtWidgets.QLineEdit(self.frame_top)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_Epsilon.setFont(font)
        self.lineEdit_Epsilon.setStyleSheet("QLineEdit{\n"
"    border: none;\n"
"    border-top: 2px solid rgb(255, 99, 71);\n"
"    color: rgb(0, 0, 0);\n"
"    background-color: transparent;\n"
"    padding: 3px;\n"
"    width: 180px;\n"
"}\n"
"")
        # rgb(100, 149, 237)
        self.lineEdit_Epsilon.setValidator(validator)
        self.lineEdit_Epsilon.setObjectName("lineEdit_Epsilon")
        self.gridLayout.addWidget(self.lineEdit_Epsilon, 0, 3, 1, 1)

        self.lineEdit_Rho = QtWidgets.QLineEdit(self.frame_top)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_Rho.setFont(font)
        self.lineEdit_Rho.setStyleSheet("QLineEdit{\n"
"    border: none;\n"
"    border-top: 2px solid rgb(255, 99, 71);\n"
"    color: rgb(0, 0, 0);\n"
"    background-color: transparent;\n"
"    padding: 3px;\n"
"    width: 180px;\n"
"}\n"
"")
        self.lineEdit_Rho.setValidator(validator)
        self.lineEdit_Rho.setObjectName("lineEdit_Rho")
        self.gridLayout.addWidget(self.lineEdit_Rho, 0, 4, 1, 1)

        self.lineEdit_Omega = QtWidgets.QLineEdit(self.frame_top)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_Omega.setFont(font)
        self.lineEdit_Omega.setStyleSheet("QLineEdit{\n"
"    border: none;\n"
"    border-bottom: 2px solid rgb(255, 99, 71);\n"
"    color: rgb(0, 0, 0);\n"
"    background-color: transparent;\n"
"    padding: 3px;\n"
"    width: 180px;\n"
"}\n"
"")
        self.lineEdit_Omega.setValidator(validator)
        self.lineEdit_Omega.setObjectName("lineEdit_Omega")
        self.gridLayout.addWidget(self.lineEdit_Omega, 2, 0, 1, 1)

        self.lineEdit_Kappa = QtWidgets.QLineEdit(self.frame_top)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_Kappa.setFont(font)
        self.lineEdit_Kappa.setStyleSheet("QLineEdit{\n"
"    border: none;\n"
"    border-bottom: 2px solid rgb(255, 99, 71);\n"
"    color: rgb(0, 0, 0);\n"
"    background-color: transparent;\n"
"    padding: 3px;\n"
"    width: 180px;\n"
"}\n"
"")
        self.lineEdit_Kappa.setValidator(validator)
        self.lineEdit_Kappa.setObjectName("lineEdit_Kappa")
        self.gridLayout.addWidget(self.lineEdit_Kappa, 2, 1, 1, 1)

        self.lineEdit_Tau = QtWidgets.QLineEdit(self.frame_top)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_Tau.setFont(font)
        self.lineEdit_Tau.setStyleSheet("QLineEdit{\n"
"    border: none;\n"
"    border-bottom: 2px solid rgb(255, 99, 71);\n"
"    color: rgb(0, 0, 0);\n"
"    background-color: transparent;\n"
"    padding: 3px;\n"
"    width: 180px;\n"
"}\n"
"")
        self.lineEdit_Tau.setValidator(validator)
        self.lineEdit_Tau.setObjectName("lineEdit_Tau")
        self.gridLayout.addWidget(self.lineEdit_Tau, 2, 2, 1, 1)

        self.lineEdit_Sigma = QtWidgets.QLineEdit(self.frame_top)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_Sigma.setFont(font)
        self.lineEdit_Sigma.setStyleSheet("QLineEdit{\n"
"    border: none;\n"
"    border-bottom: 2px solid rgb(255, 99, 71);\n"
"    color: rgb(0, 0, 0);\n"
"    background-color: transparent;\n"
"    padding: 3px;\n"
"    width: 180px;\n"
"}\n"
"")
        self.lineEdit_Sigma.setValidator(validator)
        self.lineEdit_Sigma.setObjectName("lineEdit_Sigma")
        self.gridLayout.addWidget(self.lineEdit_Sigma, 2, 3, 1, 1)

        self.horizontalLayout_n = QtWidgets.QHBoxLayout()
        self.horizontalLayout_n.setObjectName("horizontalLayout")
        self.lineEdit_nSimulation = QtWidgets.QLineEdit(self.frame_top)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_nSimulation.setFont(font)
        self.lineEdit_nSimulation.setStyleSheet("QLineEdit{\n"
"    border: none;\n"
"    border-bottom: 2px solid rgb(255, 99, 71);\n"
"    color: rgb(0, 0, 0);\n"
"    background-color: transparent;\n"
"    padding: 3px;\n"
"    width: 180px;\n"
"}\n"
"")
        self.lineEdit_nSimulation.setValidator(validator)
        self.lineEdit_nSimulation.setObjectName("lineEdit_nSimulation")
        self.horizontalLayout_n.addWidget(self.lineEdit_nSimulation)
        self.pushButton_Run = QtWidgets.QPushButton(self.frame_top)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_Run.setFont(font)
        self.pushButton_Run.setStyleSheet("QPushButton{\n"
"    border: 2px solid rgb(255, 99, 71);\n"
"    color: rgb(60, 60, 60);\n"
"    background-color: transparent;\n"
"    padding: 3px;\n"
"    width: 180px;\n"
"}\n"
"\n"
"QPushButton:focus {\n"
"    outline: none;\n"
"}"
"QPushButton:hover {\n"
"       background-color: rgba(255, 99, 71, 0.3);\n"
"       color: rgb(100, 149, 237);\n"
"}")
        self.pushButton_Run.setObjectName("pushButton_Run")
        self.horizontalLayout_n.addWidget(self.pushButton_Run)
        self.gridLayout.addLayout(self.horizontalLayout_n, 2, 4, 1, 1)

        self.horizontalLayout.addWidget(self.frame_top)


        self.verticalLayout.addWidget(self.Top_Bar)

        self.Content = QFrame(self.centralwidget)
        self.Content.setObjectName(u"Content")
        self.Content.setFrameShape(QFrame.NoFrame)
        self.Content.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.Content)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame_left_menu = QFrame(self.Content)
        self.frame_left_menu.setObjectName(u"frame_left_menu")
        self.frame_left_menu.setMinimumSize(QSize(70, 0))
        self.frame_left_menu.setMaximumSize(QSize(70, 16777215))
        self.frame_left_menu.setStyleSheet(u"background-color: rgb(168, 193, 232);")
        self.frame_left_menu.setFrameShape(QFrame.StyledPanel)
        self.frame_left_menu.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_left_menu)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.frame_top_menus = QFrame(self.frame_left_menu)
        self.frame_top_menus.setObjectName(u"frame_top_menus")
        self.frame_top_menus.setFrameShape(QFrame.NoFrame)
        self.frame_top_menus.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_top_menus)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.btn_page_1 = QPushButton(self.frame_top_menus)
        self.btn_page_1.setObjectName(u"btn_page_1")
        self.btn_page_1.setMinimumSize(QSize(0, 40))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.btn_page_1.setFont(font)
        self.btn_page_1.setStyleSheet(u"QPushButton {\n"
"	color: rgb(60, 60, 60);\n"
"	background-color: transparent;\n"
"	border: 0px solid;\n"
"}\n"
"QPushButton:focus {\n"
"    outline: none;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgba(100, 149, 237, 0.4);\n"
"       color: rgb(255, 99, 71);\n"
"}")

        self.verticalLayout_4.addWidget(self.btn_page_1)

        self.btn_page_2 = QPushButton(self.frame_top_menus)
        self.btn_page_2.setObjectName(u"btn_page_2")
        self.btn_page_2.setMinimumSize(QSize(0, 40))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.btn_page_2.setFont(font)
        self.btn_page_2.setStyleSheet(u"QPushButton {\n"
"	color: rgb(60, 60, 60);\n"
"	background-color: transparent;\n"
"	border: 0px solid;\n"
"}\n"
"QPushButton:focus {\n"
"    outline: none;\n"
"}\n"
"QPushButton:hover {\n"
"       background-color: rgba(100, 149, 237, 0.4);\n"
"       color: rgb(255, 99, 71);\n"
"}")

        self.verticalLayout_4.addWidget(self.btn_page_2)

        self.btn_page_3 = QPushButton(self.frame_top_menus)
        self.btn_page_3.setObjectName(u"btn_page_3")
        self.btn_page_3.setMinimumSize(QSize(0, 40))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.btn_page_3.setFont(font)
        self.btn_page_3.setStyleSheet(u"QPushButton {\n"
"	color: rgb(60, 60, 60);\n"
"	background-color: transparent;\n"
"	border: 0px solid;\n"
"}\n"
"QPushButton:focus {\n"
"    outline: none;\n"
"}\n"
"QPushButton:hover {\n"
"       background-color: rgba(100, 149, 237, 0.4);\n"
"       color: rgb(255, 99, 71);\n"
"}")

        self.verticalLayout_4.addWidget(self.btn_page_3)

        self.btn_page_4 = QPushButton(self.frame_top_menus)
        self.btn_page_4.setObjectName(u"btn_page_4")
        self.btn_page_4.setMinimumSize(QSize(0, 40))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.btn_page_4.setFont(font)
        self.btn_page_4.setStyleSheet(u"QPushButton {\n"
"       color: rgb(60, 60, 60);\n"
"       background-color: transparent;\n"
"       border: 0px solid;\n"
"}\n"
"QPushButton:focus {\n"
"    outline: none;\n"
"}\n"
"QPushButton:hover {\n"
"       background-color: rgba(100, 149, 237, 0.4);\n"
"       color: rgb(255, 99, 71);\n"
"}")

        self.verticalLayout_4.addWidget(self.btn_page_4)

        self.verticalLayout_3.addWidget(self.frame_top_menus, 0, Qt.AlignTop)


        self.horizontalLayout_2.addWidget(self.frame_left_menu)

        self.frame_pages = QFrame(self.Content)
        self.frame_pages.setObjectName(u"frame_pages")
        self.frame_pages.setFrameShape(QFrame.StyledPanel)
        self.frame_pages.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_pages)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.stackedWidget = QStackedWidget(self.frame_pages)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page_1 = QWidget()
        self.page_1.setObjectName(u"page_1")

        self.gridLayout_4 = QtWidgets.QGridLayout(self.page_1)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_4.setContentsMargins(90,0,90,0)
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer.setMedia(QMediaContent())
        self.playlist = QMediaPlaylist()
        self.mediaPlayer.setPlaylist(self.playlist)

        self.videoWidget = QVideoWidget(self.page_1)
        self.videoWidget.setGeometry(QtCore.QRect(0, 0, 711, 400))
        self.videoWidget.setAspectRatioMode(Qt.KeepAspectRatio)

        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)
        self.gridLayout_4.addWidget(self.videoWidget, 0, 0, 1, 4)

        self.pushButton_play = QtWidgets.QPushButton(self.page_1)
        self.pushButton_play.setIcon(QIcon(QPixmap("play.png")))
        self.pushButton_play.clicked.connect(self.play_video)
        self.pushButton_play.setMaximumSize(QtCore.QSize(60, 30))
        self.pushButton_play.setStyleSheet("QPushButton{\n"
"    background-color: transparent;\n"
"    icon-size: 30px;\n"
"}\n"
"\n"
"QPushButton:focus {\n"
"    outline: none;\n"
"}")
        self.pushButton_play.setObjectName("pushButton")
        self.gridLayout_4.addWidget(self.pushButton_play, 1, 1, 1, 1)
        self.horizontalSlider = QtWidgets.QSlider(self.page_1)
        self.horizontalSlider.setMaximumSize(QtCore.QSize(350, 30))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalSlider.sliderMoved.connect(self.set_position)
        self.horizontalSlider.setStyleSheet("QSlider::groove:horizontal {\n"
"border: 1px solid #bbb;\n"
"background: white;\n"
"height: 10px;\n"
"border-radius: 4px;\n"
"}\n"
"\n"
"QSlider::sub-page:horizontal {\n"
"background: qlineargradient(x1: 0, y1: 0,    x2: 0, y2: 1,\n"
"    stop: 0 #f3593e, stop: 1 #ff7759);\n"
"background: qlineargradient(x1: 0, y1: 0.2, x2: 1, y2: 1,\n"
"    stop: 0 #ff7759, stop: 1 #dc442d);\n"
"border: 1px solid #6bff7d;\n"
"height: 10px;\n"
"border-radius: 4px;\n"
"}\n"
"\n"
"QSlider::add-page:horizontal {\n"
"background: #fff;\n"
"border: 1px solid #dc442d;\n"
"height: 10px;\n"
"border-radius: 4px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"background: qlineargradient(x1:0, y1:0, x2:1, y2:1,\n"
"    stop:0 #eee, stop:1 #ccc);\n"
"border: 1px solid #777;\n"
"width: 13px;\n"
"margin-top: -2px;\n"
"margin-bottom: -2px;\n"
"border-radius: 4px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal:hover {\n"
"background: qlineargradient(x1:0, y1:0, x2:1, y2:1,\n"
"    stop:0 #fff, stop:1 #ddd);\n"
"border: 1px solid #444;\n"
"border-radius: 4px;\n"
"}\n"
"\n"
"QSlider::sub-page:horizontal:disabled {\n"
"background: #bbb;\n"
"border-color: #999;\n"
"}\n"
"\n"
"QSlider::add-page:horizontal:disabled {\n"
"background: #eee;\n"
"border-color: #999;\n"
"}\n"
"\n"
"QSlider::handle:horizontal:disabled {\n"
"background: #eee;\n"
"border: 1px solid #aaa;\n"
"border-radius: 4px;\n"
"}")
        self.gridLayout_4.addWidget(self.horizontalSlider, 1, 2, 1, 1)


        self.stackedWidget.addWidget(self.page_1)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.verticalLayout_6 = QVBoxLayout(self.page_2)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label_2 = QLabel(self.page_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignCenter)
        self.label_2.setStyleSheet("QLabel{\n"
"    margin: 5px;\n"
"}\n"
"\n"
"")
        self.verticalLayout_6.addWidget(self.label_2)

        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.verticalLayout_8 = QVBoxLayout(self.page_3)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.label = QLabel(self.page_3)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("QLabel{\n"
"}\n"
"\n"
"")
        self.verticalLayout_8.addWidget(self.label)

        self.pushButton_open_data = QtWidgets.QPushButton(self.page_3)
        self.pushButton_open_data.setMaximumSize(QtCore.QSize(102, 29))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_open_data.setFont(font)
        self.pushButton_open_data.setStyleSheet("QPushButton{\n"
"    border: 2px solid rgb(255, 99, 71);\n"
"    color: rgb(100, 149, 237);\n"
"    background-color: transparent;\n"
"    padding: 3px;\n"
"    width: 180px;\n"
"}\n"
"\n"
"QPushButton:focus {\n"
"    outline: none;\n"
"}"
"QPushButton:hover {\n"
"       background-color: rgba(255, 99, 71, 0.4);\n"
"       color: rgb(100, 149, 237);\n"
"}")
        self.pushButton_open_data.setObjectName("pushButton_open_data")
        self.verticalLayout_8.addWidget(self.pushButton_open_data)
        self.stackedWidget.addWidget(self.page_3)

        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.verticalLayout_7 = QVBoxLayout(self.page_4)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")

        self.label_4 = QLabel()
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font)
        self.label_4.setText("")
        self.label_4.setAlignment(Qt.AlignCenter)
        self.label_4.setWordWrap(True)
        self.label_4.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.label_4.setMinimumSize(QSize(800, 4500))
        self.label_4.setStyleSheet("QLabel{\n"
"       color: rgb(100, 149, 237);\n"
"}\n"
"")
        self.scrollArea = QScrollArea(self.page_4)
        
        self.verticalLayout_sa = QVBoxLayout(self.scrollArea)
        self.verticalLayout_sa.setObjectName(u"verticalLayout_sa")
        self.scrollArea.setWidget(self.label_4)
        self.scrollArea.setStyleSheet("QScrollArea{\n"
"    border: none;\n"
"    margin-left: 70px;\n"
"}\n"
"QScrollBar:vertical {\n"
"    border: none;\n"
"    background: transparent;\n"
"    width: 14px;\n"
"    margin: 15px 0 15px 0;\n"
"    border-radius: 0px;\n"
" }\n"
"QScrollBar::handle:vertical:hover{    \n"
"    background-color: rgb(255, 99, 71);\n"
"}\n"
"QScrollBar::handle:vertical:pressed {    \n"
"    background-color: rgb(255, 99, 71);\n"
"}\n"
"/*  HANDLE BAR VERTICAL */\n"
"QScrollBar::handle:vertical {    \n"
"    border: 2px solid rgb(255, 99, 71);\n"
"    min-height: 30px;\n"
"    border-radius: 7px;\n"
"}\n"
"/* BTN TOP - SCROLLBAR */\n"
"QScrollBar::sub-line:vertical {\n"
"    border: none;\n"
"    background-color: rgb(255, 99, 71);\n"
"    height: 15px;\n"
"    border-top-left-radius: 7px;\n"
"    border-top-right-radius: 7px;\n"
"    border-bottom-left-radius: 7px;\n"
"    border-bottom-right-radius: 7px;\n"
"    subcontrol-position: top;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"/* BTN BOTTOM - SCROLLBAR */\n"
"QScrollBar::add-line:vertical {\n"
"    border: none;\n"
"    background-color: rgb(255, 99, 71);\n"
"    height: 15px;\n"
"    border-bottom-left-radius: 7px;\n"
"    border-bottom-right-radius: 7px;\n"
"    border-top-left-radius: 7px;\n"
"    border-top-right-radius: 7px;\n"
"    subcontrol-position: bottom;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"/* RESET ARROW */\n"
"QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
"    background: none;\n"
"}\n"
"QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"    background: none;\n"
"}")

        self.verticalLayout_7.addWidget(self.scrollArea)

        self.stackedWidget.addWidget(self.page_4)
   

        

        self.verticalLayout_5.addWidget(self.stackedWidget)


        self.horizontalLayout_2.addWidget(self.frame_pages)


        self.verticalLayout.addWidget(self.Content)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(0)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.Btn_Toggle.setText(QCoreApplication.translate("MainWindow", u"TOGGLE", None))
        self.btn_page_1.setText(QCoreApplication.translate("MainWindow", u"Animation", None))
        self.btn_page_2.setText(QCoreApplication.translate("MainWindow", u"SEIQR graph", None))
        self.btn_page_3.setText(QCoreApplication.translate("MainWindow", u"Data comparison", None))
        self.btn_page_4.setText(QCoreApplication.translate("MainWindow", u"Output Data", None))
        
        self.lineEdit_Epsilon.setPlaceholderText("Epsilon (latent period)")
        self.lineEdit_Sigma.setPlaceholderText("Sigma (Q -> D rate)")
        self.pushButton_Run.setText("Run")
        self.lineEdit_Susceptible.setPlaceholderText("Susceptible")
        self.lineEdit_Tau.setPlaceholderText("Tau (Q -> R rate)")
        self.lineEdit_Infected.setPlaceholderText("Infected")
        self.lineEdit_Omega.setPlaceholderText("Omega (I -> R rate)")
        self.lineEdit_Beta.setPlaceholderText("Beta (transmission rate)")
        self.lineEdit_Kappa.setPlaceholderText("Kappa (I -> D rate)")
        self.lineEdit_Rho.setPlaceholderText("Rho (I -> Q rate)")
        self.lineEdit_nSimulation.setPlaceholderText("N° simulation")
        self.pushButton_Run.clicked.connect(self.test_values)
        self.pushButton_open_data.setText(QCoreApplication.translate("MainWindow", u"Open Data", None))
        self.pushButton_open_data.clicked.connect(self.openFile)


    def test_values(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText('There is wrong input')
        msg.setWindowTitle('Error')
        msg.setStandardButtons(QMessageBox.Ok)
        if int(self.lineEdit_Infected.text()) >= int(self.lineEdit_Susceptible.text()):
            msg.setDetailedText('Number of infeced must be less than number of Susceptible')
            msg.exec_()
        elif self.lineEdit_Beta.text() == '0.0':
            print('no')
            msg.setDetailedText("Beta mustn't be null value")
            msg.exec_()
        else:    
            self.run_simulation()                    



    def run_simulation(self):
        beta = float(self.lineEdit_Beta.text())  # transmission rate
        epsilon = float(self.lineEdit_Epsilon.text()) # the latent period   
        rho = float(self.lineEdit_Rho.text())   # I -> Q rate          
        omega = float(self.lineEdit_Omega.text())  # I -> R rate
        kappa = float(self.lineEdit_Kappa.text())   # I -> D rate
        tau =  float(self.lineEdit_Tau.text())   # Q -> R rate
        sigma = float(self.lineEdit_Sigma.text())  # Q -> D rate  
        nSimul = int(self.lineEdit_nSimulation.text())
        S = int(self.lineEdit_Susceptible.text())
        E = int(self.lineEdit_Infected.text())
        I = 0
        Q = 0
        R = 0
        self.simulation_code = simpleNetworkSEIQRModel(beta, epsilon, rho, omega, kappa, tau, sigma, S, E, I, Q, R)
        self.result = self.simulation_code.mainn(beta, epsilon, rho, omega, kappa, tau, sigma, S, E, I, Q, R, nSimul)
        time.sleep(5)

        qpixmap = QPixmap("All_classes_plot.png")
        self.label_2.setPixmap(qpixmap)
          
        self.playlist.clear()
        if self.result[0] == self.result[2]:
        	self.playlist.addMedia(QMediaContent(QUrl().fromLocalFile('Animation.mp4')))
	        self.playlist.setPlaybackMode(QMediaPlaylist.Loop)
        	self.mediaPlayer.setPlaylist(self.playlist)
	        self.mediaPlayer.play()
        self.readFile()        


    
    def readFile(self):
        file = QFile("output4.csv")
        if not file.open(QIODevice.ReadOnly | QIODevice.Text):
                return
        inn = QTextStream(file)
        line = inn.readAll()
        self.label_4.setText(line)


    def openFile(self):
        filename = QFileDialog.getOpenFileName()
        path = filename[0]
        exlFile = pd.read_excel(path)
        exlFile = exlFile.dropna()
        exlFile = exlFile.sort_index(ascending=False)
        realData = exlFile.iloc[:,1].tolist()   
        try:             
                self.simulation_code.comparisonPlot(realData, self.result[1])
                time.sleep(2)
                qpixmap2 = QPixmap("Two_plot.png")
                self.label.setPixmap(qpixmap2)
        except Exception as e:
                pass
                


    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()    

    def mediastate_changed(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.pushButton_play.setIcon(QIcon(QPixmap("pause.png")))
        else:
            self.pushButton_play.setIcon(QIcon(QPixmap("play.png")))

    def position_changed(self, position):
        self.horizontalSlider.setValue(position)


    def duration_changed(self, duration):
        self.horizontalSlider.setRange(0, duration)


    def set_position(self, position):
        self.mediaPlayer.setPosition(position)        



