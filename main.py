import sys

import pandas as pd

from etl import EtlProccess
from PySide2.QtCore import QAbstractTableModel, QPoint, Qt, QThread
from PySide2.QtWidgets import *

import tools
import ui
from ui.lang_ru import *


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = ui.MainWindow()
        self.load_excel_form = ui.LoadExcelForm()
        self.load_csv_form = ui.LoadCSVForm()
        self.is_etl_work = False
        self.app_thread = Thread()
        self.df = None
        self.ui.setupUi(self)


class Thread(QThread):
    def __init__(self, parent=None):
        QThread.__init__(self, parent)

    def run(self):
        while w.is_etl_work:
            app.processEvents()
            print("run ETL iteration")
            get_data_by_url()
            if etl.output_enable:
                if etl.output_file_format == "xls":
                    load_data_to_excel_file()
                if etl.output_file_format == "csv":
                    load_data_to_csv_file()

            if etl.period == -1:
                etl_stop()
            elif etl.period == 0:  # 1 минута
                for i in range(60):
                    app.processEvents()
                    QThread.sleep(1)
            elif etl.period == 1:  # 5 минут
                for i in range(300):
                    app.processEvents()
                    QThread.sleep(1)
            elif etl.period == 2:  # 10 минут
                for i in range(600):
                    app.processEvents()
                    QThread.sleep(1)
            elif etl.period == 3:  # 30 минут
                for i in range(1800):
                    app.processEvents()
                    QThread.sleep(1)
            elif etl.period == 3:  # 60 минут
                for i in range(3600):
                    app.processEvents()
                    QThread.sleep(1)


class PandasModel(QAbstractTableModel):
    def __init__(self, data):
        super(PandasModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])


def menu_exit():
    on_close()
    sys.exit(app.exec_())


def menu_about():
    app.processEvents()
    about = ui.AboutWindow(w)
    about.move(w.geometry().center() - about.rect().center() - QPoint(4, 30))
    about.show()


def on_close():
    etl_stop()


def get_data_by_url():
    if url := w.ui.url.text():
        result_text = etl.get_text_by_url(url)
        w.ui.result_txt.setText(result_text)
        w.df = tools.to_dataframe.xml_to_df(input_text=result_text, clear_NaN=True)
        if w.df.shape[0] == 0:
            w.df = tools.to_dataframe.json_to_df(input_text=result_text, clear_NaN=True)
        model = PandasModel(data=w.df)
        w.ui.result_table.setModel(model)
        w.ui.result_table.resizeColumnsToContents()


def on_timer_switch():
    if w.ui.timer_checkbox.isChecked():
        w.ui.task_timer.setEnabled(True)
    else:
        w.ui.task_timer.setEnabled(False)


def on_load_excel_switch():
    if w.ui.btn_excel.isChecked():
        w.load_excel_form.exec_()


def on_load_csv_switch():
    if w.ui.btn_csv.isChecked():
        w.load_csv_form.exec_()


def on_excel_file_dialog():
    file_name = QFileDialog.getOpenFileName(
        parent=w, caption=SET_EXCEL_FILE, filter="*.xls, *.xlsx"
    )
    w.load_excel_form.filepath.setText(file_name[0])


def on_csv_file_dialog():
    file_name = QFileDialog.getOpenFileName(
        parent=w, caption=SET_CSV_FILE, filter="*.csv"
    )
    w.load_csv_form.filepath.setText(file_name[0])


def etl_start():
    w.is_etl_work = True
    etl.url = w.ui.url.text()
    if w.ui.timer_checkbox.isChecked():
        etl.period = w.ui.task_timer.currentIndex()
    else:
        etl.period = -1
    w.ui.btn_start.setText(STOP)
    w.ui.btn_start.setStyleSheet("QPushButton {background-color: #eeaeae}")
    w.app_thread.run()


def etl_stop():
    w.is_etl_work = False
    w.ui.btn_start.setText(START)
    w.ui.btn_start.setStyleSheet("QPushButton {background-color: #aeeec0}")


def on_start_etl():
    if w.is_etl_work:
        etl_stop()
    else:
        etl_start()


def on_save_excel_form():
    if w.load_excel_form.filepath.text() == "":
        msg = QMessageBox()
        msg.setText(SET_EXCEL_FILE)
        msg.exec()
    else:
        etl.output_filepath = w.load_excel_form.filepath.text()
    etl.output_file_format = "xls"
    sheetname = w.load_excel_form.excel_sheetname.text()
    if sheetname == "":
        etl.output_xls_sheetname = "DesktopETL"
    else:
        etl.output_xls_sheetname = sheetname
    etl.output_rewrite = w.load_excel_form.is_rewrite_records.isChecked()
    etl.output_xls_write_header = w.load_excel_form.is_write_header.isChecked()
    etl.output_xls_write_rownums = w.load_excel_form.is_write_numrows.isChecked()
    if etl.output_filepath:
        etl.output_enable = True
        w.load_excel_form.close()


def on_save_csv_form():
    if w.load_csv_form.filepath.text() == "":
        msg = QMessageBox()
        msg.setText(SET_CSV_FILE)
        msg.exec()
    else:
        etl.output_filepath = w.load_csv_form.filepath.text()
    etl.output_file_format = "csv"
    etl.output_rewrite = w.load_csv_form.is_rewrite_records.isChecked()
    etl.output_csv_write_header = w.load_csv_form.is_write_header.isChecked()
    etl.output_csv_write_rownums = w.load_csv_form.is_write_numrows.isChecked()
    if w.load_csv_form.sep.text() == "":
        etl.output_csv_sep = ","
    else:
        etl.output_csv_sep = w.load_csv_form.sep.text()
    if etl.output_filepath:
        etl.output_enable = True
        w.load_csv_form.close()


def load_data_to_excel_file():
    if etl.output_rewrite:
        with pd.ExcelWriter(
            etl.output_filepath, mode="a", engine="openpyxl", if_sheet_exists="replace"
        ) as writer:
            w.df.to_excel(
                writer,
                sheet_name=etl.output_xls_sheetname,
                header=etl.output_xls_write_header,
                index=etl.output_xls_write_rownums,
            )
    else:
        df_to_read = pd.read_excel(
            open(etl.output_filepath, "rb"), sheet_name=etl.output_xls_sheetname
        )
        startrow = df_to_read.shape[0] + 1
        with pd.ExcelWriter(
            etl.output_filepath, mode="a", engine="openpyxl", if_sheet_exists="overlay"
        ) as writer:
            w.df.to_excel(
                writer,
                sheet_name=etl.output_xls_sheetname,
                header=etl.output_xls_write_header,
                index=etl.output_xls_write_rownums,
                startrow=startrow,
            )


def load_data_to_csv_file():
    if etl.output_rewrite:
        w.df.to_csv(
            etl.output_filepath,
            header=etl.output_csv_write_header,
            index=etl.output_csv_write_rownums,
            sep=etl.output_csv_sep,
        )
    else:
        w.df.to_csv(
            etl.output_filepath,
            mode="a",
            header=etl.output_csv_write_header,
            index=etl.output_csv_write_rownums,
            sep=etl.output_csv_sep,
        )


if __name__ == "__main__":
    app = QApplication([])
    app.setStyle("Fusion")
    w = MainWindow()
    etl = EtlProccess()
    w.app_thread.start()

    w.ui.menu_exit.triggered.connect(menu_exit)
    w.ui.menu_about.triggered.connect(menu_about)
    w.ui.btn_get_data.released.connect(get_data_by_url)
    w.ui.btn_get_data_short.released.connect(get_data_by_url)
    w.ui.timer_checkbox.stateChanged.connect(on_timer_switch)
    w.ui.btn_excel.stateChanged.connect(on_load_excel_switch)
    w.ui.btn_csv.stateChanged.connect(on_load_csv_switch)
    w.load_excel_form.filedialog.released.connect(on_excel_file_dialog)
    w.load_csv_form.filedialog.released.connect(on_csv_file_dialog)
    w.ui.btn_start.released.connect(on_start_etl)
    w.load_excel_form.btn_save.released.connect(on_save_excel_form)
    w.load_csv_form.btn_save.released.connect(on_save_csv_form)
    w.show()

    sys.exit(app.exec_())
