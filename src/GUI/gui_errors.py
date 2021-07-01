from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox


# Method; creates an Error-Message Box
# supposed to be thrown when no IP or port has been entered
def no_input_error():
    error_dialog = QtWidgets.QMessageBox()
    error_dialog.setIcon(QMessageBox.Critical)
    error_dialog.setText('No Input Error!')
    error_dialog.setInformativeText('Please an IP and a Port')
    error_dialog.setWindowTitle('Error!')

    error_dialog.exec_()
