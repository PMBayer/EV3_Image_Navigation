#!/usr/bin/env python3
import sys

from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QLabel


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    # noinspection PyAttributeOutsideInit
    def init_ui(self):
        # general window settings
        self.resize(500, 500)
        self.setWindowTitle('EV3 Image Navigation')


        # title hbox
        self.title_hbox = QHBoxLayout()
        self.title_label = QLabel('Totally Awesome EV3 Image Navigation')
        self.title_label.setStyleSheet()
        self.title_hbox.addWidget(self.title_label)
        self.setLayout(self.title_hbox)




def main():
    # initialize Window
    app = QApplication(sys.argv)
    window = Window()

    # open Window
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
