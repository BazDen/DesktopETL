from PySide2 import QtGui, QtCore
from PySide2.QtWidgets import *

from .lang_ru import *
from .img import table_excel


class LoadExcelForm(QDialog):
    def __init__(self, parent=None):
        super(LoadExcelForm, self).__init__(parent)
        self.setMinimumWidth(500)
        self.setWindowTitle(LOAD_EXCEL_FORM_TITLE)
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(QtCore.QByteArray.fromRawData(table_excel), 'PNG')
        self.setWindowIcon(QtGui.QIcon(pixmap))
        layout = QVBoxLayout()
        file_layout = QHBoxLayout()
        self.filepath = QLineEdit()
        self.filepath.setPlaceholderText(FILE_PATH)
        self.filedialog = QPushButton("...")
        file_layout.addWidget(self.filepath)
        file_layout.addWidget(self.filedialog)
        layout.addLayout(file_layout)
        self.excel_sheetname = QLineEdit(placeholderText=SPECIFY_SHEET_NAME)
        layout.addWidget(self.excel_sheetname)
        self.is_append_records = QRadioButton(text=APPEND_RECORDS)
        self.is_rewrite_records = QRadioButton(text=REWRITE_RECORDS)
        self.is_write_header = QCheckBox(text=WRITE_HEADER)
        self.is_write_numrows = QCheckBox(text=WRITE_NUMROWS)
        layout.addWidget(self.is_write_header)
        layout.addWidget(self.is_write_numrows)
        layout.addWidget(self.is_append_records)
        layout.addWidget(self.is_rewrite_records)
        self.btn_save = QPushButton(SAVE)
        self.btn_cancel = QPushButton(CANCEL)
        self.btn_cancel.released.connect(self.close)
        layout.addWidget(self.btn_save)
        layout.addWidget(self.btn_cancel)
        self.setLayout(layout)
