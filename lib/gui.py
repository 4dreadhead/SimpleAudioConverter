from PyQt6 import QtCore, QtGui, QtWidgets
from pathlib import Path


class UIMainWindow(object):
    central_widget: QtWidgets.QWidget
    button_select_files: QtWidgets.QPushButton
    button_convert: QtWidgets.QPushButton
    files_browser: QtWidgets.QTextBrowser
    status_browser: QtWidgets.QTextBrowser
    title: QtWidgets.QLabel
    out_format: QtWidgets.QComboBox
    statusbar: QtWidgets.QStatusBar

    def setup_ui(self, main_window):
        main_window.setObjectName("main_window")
        main_window.resize(800, 650)
        main_window.setMinimumSize(QtCore.QSize(800, 650))
        main_window.setMaximumSize(QtCore.QSize(800, 650))
        main_window.setStyleSheet("background-color: rgb(32, 28, 42);")

        self.central_widget = QtWidgets.QWidget(main_window)
        self.central_widget.setObjectName("centralwidget")

        self.title = QtWidgets.QLabel(self.central_widget)
        self.title.setGeometry(QtCore.QRect(0, 0, 800, 180))
        self.title.setObjectName("title")
        gif = QtGui.QMovie(str(Path("media/title.gif").resolve()))
        self.title.setMovie(gif)
        gif.start()

        font = self.set_font(size=11, bold=True, italic=True)

        self.button_select_files = QtWidgets.QPushButton(self.central_widget)
        self.button_select_files.setGeometry(QtCore.QRect(30, 180, 200, 30))
        self.button_select_files.setFont(font)
        self.button_select_files.setObjectName("ButtonSelectFiles")
        self.button_select_files.setStyleSheet(self.button_stylesheet())

        self.button_convert = QtWidgets.QPushButton(self.central_widget)
        self.button_convert.setGeometry(QtCore.QRect(300, 180, 200, 30))
        self.button_convert.setFont(font)
        self.button_convert.setObjectName("ButtonConvert")
        self.button_convert.setStyleSheet(self.button_stylesheet())

        self.out_format = QtWidgets.QComboBox(self.central_widget)
        self.out_format.addItems(["mp3", "wav", "flac", "aac"])
        self.out_format.setFont(font)
        self.out_format.setStyleSheet(self.combo_box_stylesheet())
        self.out_format.setGeometry(QtCore.QRect(570, 180, 200, 30))

        font = self.set_font(size=10)

        self.files_browser = QtWidgets.QTextBrowser(self.central_widget)
        self.files_browser.setGeometry(QtCore.QRect(30, 240, 355, 380))
        self.files_browser.setFont(font)
        self.files_browser.setStyleSheet(self.browser_stylesheet())
        self.files_browser.setObjectName("FilesBrowser")

        self.status_browser = QtWidgets.QTextBrowser(self.central_widget)
        self.status_browser.setGeometry(QtCore.QRect(415, 240, 355, 380))
        self.status_browser.setFont(font)
        self.status_browser.setStyleSheet(self.browser_stylesheet())
        self.status_browser.setObjectName("TextBrowser")

        main_window.setCentralWidget(self.central_widget)
        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        self.statusbar.setStyleSheet("color: rgb(238, 238, 236);")
        main_window.setStatusBar(self.statusbar)

        self.button_select_files.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.button_convert.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.files_browser.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.CursorShape.IBeamCursor))
        self.status_browser.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.CursorShape.IBeamCursor))

        self.re_translate_ui(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def re_translate_ui(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window", "Simple Audio Converter"))

        self.button_select_files.setText(_translate("main_window", "Select files"))
        self.button_convert.setText(_translate("main_window", "Covert"))

        self.files_browser.setHtml(_translate("main_window", self.set_html()))
        self.status_browser.setText(_translate("main_window", self.set_html()))

    @staticmethod
    def set_font(family=None, size=12, weight=None, bold=False, italic=False):
        font = QtGui.QFont()
        if family:
            font.setFamily(family)
        font.setPointSize(size)
        font.setBold(bold)
        font.setItalic(italic)
        if weight:
            font.setWeight(weight)
        return font

    @staticmethod
    def button_stylesheet():
        style = """
            QPushButton:hover {
                background-color: rgb(64, 56, 84);
                color: rgb(14,149,226);
                border: 2px solid rgb(14,149,226);
                border-radius: 5px;
            }
            QPushButton {
                background-color: rgb(48, 42, 61);
                color: rgb(14,149,226);
                border-radius: 5px;
            }
            QPushButton:pressed {
                background-color: rgb(24, 21, 30);
                color: rgb(14,149,226);
                border: 2px solid rgb(14,149,226);
                border-radius: 5px;
                padding: 1px 18px 1px 10px;
            }
        """
        return style

    @staticmethod
    def combo_box_stylesheet():
        style = """
            QComboBox QAbstractItemView {	
                background-color: rgb(48, 42, 61);
                padding: 10px;
                selection-background-color: rgb(48, 42, 61);
                border-radius: 5px;
                border: 1px solid darkgray;
                color: rgb(238, 238, 236);
            }
            QComboBox {
                border: 1px solid darkgray;
                border-radius: 3px;
                min-width: 6em;
                color: rgb(238, 238, 236);
                padding-left: 10px;
            }
    
            QComboBox:editable {
                background: rgb(48, 42, 61);
                color: rgb(238, 238, 236);
            }
    
            QComboBox:!editable, QComboBox::drop-down:editable {
                background: rgb(48, 42, 61);
                color: rgb(238, 238, 236);
            }
    
            QComboBox:!editable:on, QComboBox::drop-down:editable:on {
                background: rgb(48, 42, 61);
                color: rgb(238, 238, 236);
                padding-left: 10px;
            }
    
            QComboBox:on {
                color: rgb(238, 238, 236);
                padding-top: 3px;
                padding-left: 4px;
            }
    
            QComboBox::drop-down {
                background: rgb(48, 42, 61);
                width: 15px;
    
                border-left-width: 1px;
                border-left-color: darkgray;
                border-left-style: solid;
            }
            QComboBox::down-arrow {
                image: url(./lib/media/arrow-down.png);
                width: 5px;
                height: 5px;
            }
        """
        return style

    @staticmethod
    def browser_stylesheet():
        style = """
            background-color: rgb(48, 42, 61);
            color: rgb(238, 238, 236);
            border-radius: 5px;
        """
        return style

    @staticmethod
    def set_html():
        style = "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"" + \
                "http://www.w3.org/TR/REC-html40/strict.dtd\">\n" + \
                "<html><head><meta name=\"qrichtext\" content=\"1\" />" + \
                "<style type=\"text/css\">\n" + \
                "p, li { white-space: pre-wrap; }\n" + \
                "</style></head><body style=\" font-family:\'Ubuntu\'; " + \
                "font-size:12pt; font-weight:400; font-style:normal;\">\n" + \
                "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; " + \
                "margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;" + \
                "\"><br /></p></body></html>"
        return style
