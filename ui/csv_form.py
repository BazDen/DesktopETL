from PySide2 import QtGui, QtCore
from PySide2.QtWidgets import *

from .lang_ru import *
from .img import csv


class LoadCSVForm(QDialog):
    def __init__(self, parent=None):
        super(LoadCSVForm, self).__init__(parent)
        self.setMinimumWidth(500)
        self.setWindowTitle(LOAD_CSV_FORM_TITLE)
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(QtCore.QByteArray.fromRawData(csv), 'PNG')
        self.setWindowIcon(QtGui.QIcon(pixmap))
        layout = QVBoxLayout()
        file_layout = QHBoxLayout()
        self.filepath = QLineEdit()
        self.filepath.setPlaceholderText(FILE_PATH)
        self.filedialog = QPushButton("...")
        file_layout.addWidget(self.filepath)
        file_layout.addWidget(self.filedialog)
        layout.addLayout(file_layout)

        self.is_append_records = QRadioButton(text=APPEND_RECORDS)
        self.is_rewrite_records = QRadioButton(text=REWRITE_RECORDS)
        self.is_write_header = QCheckBox(text=WRITE_HEADER)
        self.is_write_numrows = QCheckBox(text=WRITE_NUMROWS)
        self.sep = QLineEdit()
        self.sep.setPlaceholderText(CSV_SEPARATOR)
        layout.addWidget(self.is_write_header)
        layout.addWidget(self.is_write_numrows)
        layout.addWidget(self.is_append_records)
        layout.addWidget(self.is_rewrite_records)
        layout.addWidget(self.sep)
        self.btn_save = QPushButton(SAVE)
        self.btn_cancel = QPushButton(CANCEL)
        self.btn_cancel.released.connect(self.close)
        layout.addWidget(self.btn_save)
        layout.addWidget(self.btn_cancel)
        self.setLayout(layout)
