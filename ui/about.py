from PySide2 import QtCore, QtGui
from PySide2.QtWidgets import *

from .lang_ru import *
from .img import desktop_etl


class AboutWindow(QMainWindow):
    def __init__(self, parent=None):
        super(AboutWindow, self).__init__(parent)
        self.setWindowTitle(f"{CAPTION} {VERSION}")
        self.setWindowModality(QtCore.Qt.WindowModal)
        self.setFixedSize(285, 150)

        # Logo
        self.lbl = QLabel(self)
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(QtCore.QByteArray.fromRawData(desktop_etl), 'PNG')
        self.lbl.setPixmap(QtGui.QPixmap(pixmap))
        self.lbl.move(5, 5)
        self.lbl.resize(277, 51)

        # Author
        self.lbl_author = QLabel(self)
        self.lbl_author.setText(
            'Автор: Денис Базарнов, 2023г. \n Telegram: @BazDen \n GitHub: https://github.com/BazDen/ ')
        self.lbl_author.move(5, 65)
        self.lbl_author.resize(277, 50)
