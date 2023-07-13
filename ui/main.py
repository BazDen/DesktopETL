# -*- coding: utf-8 -*-

from PySide2 import QtCore, QtGui
from PySide2.QtWidgets import *
from .lang_ru import *
from .img import *


class MainWindow(object):
    def __init__(self):
        super().__init__()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(700, 500)
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(QtCore.QByteArray.fromRawData(logo_png), 'PNG')
        MainWindow.setWindowIcon(QtGui.QIcon(pixmap))
        # -- Menu--
        self.menu = QMenuBar(MainWindow)
        self.menu.setGeometry(QtCore.QRect(0, 0, 802, 21))
        self.menu.setObjectName("menu")
        self.menu_file = QMenu(self.menu)
        self.menu_exit = QAction(MainWindow)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.menu_exit)
        self.menu.addAction(self.menu_file.menuAction())
        # ----------------About-----------------
        self.menu_about = QAction(MainWindow)
        self.menu.addAction(self.menu_about)
        # -------------Menu set--------------
        MainWindow.setMenuBar(self.menu)

        MainWindow.setWindowTitle(f"{CAPTION} {VERSION}")
        self.menu_file.setTitle(FILE)
        self.menu_about.setText(ABOUT)
        self.menu_exit.setText(EXIT)

        self.central_widget = QWidget(MainWindow)

        MainWindow.setCentralWidget(self.central_widget)

        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.setAlignment(QtCore.Qt.AlignTop)
        self.central_widget.setLayout(self.vertical_layout)
        self.url = QLineEdit(placeholderText=TASK_URL_PLACEHOLDER)

        self.btn_get_data_short = QPushButton(text=">>")
        self.btn_get_data_short.setMaximumWidth(35)
        # self.vertical_layout.addWidget(self.btn_get_data)
        self.url_layout = QHBoxLayout()
        self.url_layout.addWidget(self.url)
        self.url_layout.addWidget(self.btn_get_data_short)
        self.vertical_layout.addLayout(self.url_layout)

        self.main_layout = QHBoxLayout()

        self.tab_text = QWidget()
        self.tab_table = QWidget()

        self.result_txt = QTextEdit()
        self.tab_text.layout = QVBoxLayout()
        self.tab_text.setLayout(self.tab_text.layout)
        self.tab_text.layout.addWidget(self.result_txt)

        self.result_table = QTableView()
        # self.result_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tab_table.layout = QVBoxLayout()
        self.tab_table.setLayout(self.tab_table.layout)
        self.tab_table.layout.addWidget(self.result_table)

        self.tabs = QTabWidget()
        self.tabs.addTab(self.tab_text, TEXT)
        self.tabs.addTab(self.tab_table, TABLE)

        self.main_workarea_layout = QVBoxLayout()
        self.main_workarea_layout.addWidget(self.tabs)
        self.btn_get_data = QPushButton(text=GET_DATA)
        self.main_workarea_layout.addWidget(self.btn_get_data)

        self.timer_checkbox = QCheckBox(START_ON_TIMETABLE)
        self.main_workarea_layout.addWidget(self.timer_checkbox)
        self.task_timer = QComboBox()
        self.task_timer.addItems(TIMER_DATA)
        self.task_timer.setEnabled(False)
        self.main_workarea_layout.addWidget(self.task_timer)

        self.output_layout = QHBoxLayout()

        self.btn_excel = QCheckBox(" Excel")
        
        pixmap.loadFromData(QtCore.QByteArray.fromRawData(table_excel), 'PNG')
        self.btn_excel.setIcon(QtGui.QIcon(pixmap))
        self.output_layout.addWidget(self.btn_excel)

        self.btn_csv = QCheckBox(" CSV")
        pixmap.loadFromData(QtCore.QByteArray.fromRawData(csv), 'PNG')
        self.btn_csv.setIcon(QtGui.QIcon(pixmap))
        self.output_layout.addWidget(self.btn_csv)

        self.main_workarea_layout.addLayout(self.output_layout)

        self.btn_start = QPushButton(START)
        self.btn_start.setStyleSheet("QPushButton {background-color: #aeeec0}")
        self.main_workarea_layout.addWidget(self.btn_start)
        self.main_layout.addLayout(self.main_workarea_layout)
        self.vertical_layout.addLayout(self.main_layout)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)
