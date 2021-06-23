from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox


def no_input_error():
    error_dialog = QtWidgets.QMessageBox()
    error_dialog.setIcon(QMessageBox.Critical)
    error_dialog.setText('No Input Error!')
    error_dialog.setInformativeText('Please an IP and a Port')
    error_dialog.setWindowTitle('Error!')

    error_dialog.exec_()
