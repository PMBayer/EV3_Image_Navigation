#!/usr/bin/env python3
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QHBoxLayout, QWidget, QVBoxLayout, QLineEdit

import gui_errors as err


# Method; manages clicks on the gesture button
# if ip or port are empty throws no_input_error
# else start ev3 navigation by gesture
def click_gesture(ip, port):
    if ip == '' or port == '':
        err.no_input_error()
    else:
        port = int(port)


# Method; manages clicks on the gesture button
# if ip or port are empty throws no_input_error
# else start ev3 navigation by ball tracking
def click_ball(ip, port):
    if ip == '' or port == '':
        err.no_input_error()
    else:
        port = int(port)


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    # noinspection PyAttributeOutsideInit
    def init_ui(self):
        # general window settings
        self.resize(250, 250)
        self.setWindowTitle('EV3 Image Navigation')

        # HBox containing the title and everything associated with it
        self.title_hbox = QHBoxLayout()
        self.title_hbox.setAlignment(Qt.AlignTop)
        self.title_label = QLabel('Totally Awesome EV3 Image Navigation')
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont('Arial', 15))
        self.title_hbox.addWidget(self.title_label)

        # HBox containing everything related to the IP
        self.hbox_ip = QHBoxLayout()
        self.hbox_ip.setAlignment(Qt.AlignCenter)
        self.label_ip = QLabel('IP: ')
        self.input_ip = QLineEdit()
        self.hbox_ip.addWidget(self.label_ip)
        self.hbox_ip.addWidget(self.input_ip)

        # HBox containing everything related to the Port
        self.hbox_port = QHBoxLayout()
        self.hbox_port.setAlignment(Qt.AlignCenter)
        self.label_port = QLabel('Port: ')
        self.input_port = QLineEdit()
        self.input_port.setText('5000')
        self.hbox_port.addWidget(self.label_port)
        self.hbox_port.addWidget(self.input_port)

        # HBox for Button to choose, which Version of the Program to run
        self.hbox_Buttons = QHBoxLayout()
        self.hbox_Buttons.setAlignment(Qt.AlignCenter)
        self.btn_gesture = QPushButton('Gesture')
        self.btn_ball = QPushButton('Green Ball')
        self.hbox_Buttons.addWidget(self.btn_gesture)
        self.hbox_Buttons.addWidget(self.btn_ball)

        # VBox for all HBoxes
        self.general_vbox = QVBoxLayout()
        self.general_vbox.addLayout(self.title_hbox)
        self.general_vbox.addLayout(self.hbox_ip)
        self.general_vbox.addLayout(self.hbox_port)
        self.general_vbox.addLayout(self.hbox_Buttons)

        # add Complete Layout to Window
        self.setLayout(self.general_vbox)

        # Button on Click Events
        self.btn_gesture.clicked.connect(lambda: click_gesture(self.input_ip.text(), self.input_port.text()))
        self.btn_ball.clicked.connect(lambda: click_ball(self.input_ip.text(), self.input_port.text()))


def main():
    # initialize Window
    app = QApplication(sys.argv)
    window = Window()

    # open Window
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
