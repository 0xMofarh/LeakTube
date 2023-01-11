# -*- coding: utf-8 -*-
import sys
import threading
from functools import cached_property
import pytube
from tkinter import filedialog
from PyQt5.QtGui import QMovie
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

class QPyTube(QtCore.QObject):
    initialized = QtCore.pyqtSignal(bool, str)
    download_started = QtCore.pyqtSignal()
    download_progress_changed = QtCore.pyqtSignal(int)
    download_finished = QtCore.pyqtSignal()
    
    def __init__(self, url):
        super().__init__()
        self._url = url
        self._yt = None
        self._mutex = threading.Lock()

        threading.Thread(target=self._init, daemon=True).start()

    @property
    def url(self):
        return self._url

    @cached_property
    def resolutions(self):
        return list()

    def _init(self):
        with self._mutex:
            self.resolutions.clear()
        try:
            self._yt = pytube.YouTube(
                self.url,
                on_progress_callback=self._on_progress,
                on_complete_callback=self._on_complete,
            )
            streams = self._yt.streams.filter(mime_type="video/mp4", progressive="True")
        except Exception as e:
            self.initialized.emit(False, str(e))
            return
        with self._mutex:
            self.resolutions = [stream.resolution for stream in streams]
        self.initialized.emit(True, "")

    def download(self, resolution, directory):
        threading.Thread(
            target=self._download, args=(resolution, directory), daemon=True
        ).start()

    def _download(self, resolution, directory):
        stream = self._yt.streams.get_by_resolution(resolution)
        self.download_started.emit()
        stream.download(directory)

    def _on_progress(self, stream, chunk, bytes_remaining):
        self.download_progress_changed.emit(
            100 * (stream.filesize - bytes_remaining) // stream.filesize
        )

    def _on_complete(self, stream, filepath):
        self.download_finished.emit()
class Ui_Form(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.lineEdit_url = QtWidgets.QLineEdit("")
        self.btn_search = QtWidgets.QPushButton("")
        self.res_comboBox = QtWidgets.QComboBox()
        self.pushButton_download = QtWidgets.QPushButton("Download")
        self.progressBar_downloa_stutus = QtWidgets.QProgressBar()

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        lay = QtWidgets.QGridLayout(central_widget)
        lay.addWidget(self.lineEdit_url, 0, 0)
        lay.addWidget(self.btn_search, 0, 1)
        lay.addWidget(self.res_comboBox, 1, 0)
        lay.addWidget(self.pushButton_download, 1, 2)
        lay.addWidget(self.progressBar_downloa_stutus, 2, 0, 1, 3)

        self.pushButton_download.setEnabled(False)

        self._qpytube = None

        self.btn_search.clicked.connect(self.handle_search_clicked)
        self.pushButton_download.clicked.connect(self.handle_download_clicked)
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(271, 499)
        Form.setMinimumSize(QtCore.QSize(271, 499))
        Form.setMaximumSize(QtCore.QSize(271, 499))
        font = QtGui.QFont()
        font.setPointSize(6)
        Form.setFont(font)
        Form.setLayoutDirection(QtCore.Qt.LeftToRight)
        Form.setStyleSheet("background-color: rgb(57, 91, 100);")
        self.lineEdit_url = QtWidgets.QLineEdit(Form)
        self.lineEdit_url.setGeometry(QtCore.QRect(10, 150, 181, 41))
        font = QtGui.QFont()
        font.setFamily("Terminal")
        self.lineEdit_url.setFont(font)
        self.lineEdit_url.setStyleSheet("QLineEdit{\n"
"    border: 2px solid rgb(37,39,48);\n"
"    border-radius: 20px;\n"
"    color:#FFF;\n"
"    padding-left: 20px;\n"
"    padding-right: 20px;\n"
"    background-color: rgb(34,36,44);\n"
"}\n"
"QLineEdit:hover{\n"
"    border: 2px solid #FFD700;\n"
"}\n"
"QLineEdit:focus{\n"
"    border: 2px solid #FFD700;\n"
"    background-color: rgb(43,45,56);\n"
"\n"
"}\n"
"\n"
"")
        self.lineEdit_url.setObjectName("lineEdit_url")
        self.pushButton_download = QtWidgets.QPushButton(Form)
        self.pushButton_download.clicked.connect(self.handle_download_clicked)
        self.pushButton_download.setGeometry(QtCore.QRect(60, 300, 151, 31))
        self.pushButton_download.setStyleSheet("QPushButton{\n"
"    border: 2px solid rgb(37,39,48);\n"
"    border-radius: 10px;\n"
"    color:#FFF;\n"
"    padding-left: 10px;\n"
"    padding-right: 10px;\n"
"    background-color: rgb(34,36,44);\n"
"    font: 75 9pt \"Terminal\";\n"
"}\n"
"QPushButton:hover{\n"
"    border: 2px solid #FFD700;\n"
"}\n"
"QPushButton:focus{\n"
"    border: 2px solid #FFD700;\n"
"    background-color: rgb(43,45,56);\n"
"\n"
"}")
        self.pushButton_download.setObjectName("pushButton_download")
        self.pushButton_3_about_me = QtWidgets.QPushButton(Form)
        self.pushButton_3_about_me.setGeometry(QtCore.QRect(60, 340, 151, 31))
        self.pushButton_3_about_me.setStyleSheet("QPushButton{\n"
"    border: 2px solid rgb(37,39,48);\n"
"    border-radius: 10px;\n"
"    color:#FFF;\n"
"    padding-left: 10px;\n"
"    padding-right: 10px;\n"
"    background-color: rgb(34,36,44);\n"
"    font: 75 9pt \"Terminal\";\n"
"}\n"
"QPushButton:hover{\n"
"    border: 2px solid #FFD700;\n"
"}\n"
"QPushButton:focus{\n"
"    border: 2px solid #FFD700;\n"
"    background-color: rgb(43,45,56);\n"
"\n"
"}")
        self.pushButton_3_about_me.setObjectName("pushButton_3_about_me")
        self.label_gif = QtWidgets.QLabel(Form)
        self.label_gif.setGeometry(QtCore.QRect(60, 10, 211, 111))
        self.label_gif.setStyleSheet("")
        self.label_gif.setText("")
        self.label_gif.setObjectName("label_gif")
        self.movie = QMovie("q.gif")
        self.label_gif.setMovie(self.movie)
        self.startAnimation()
        self.progressBar_downloa_stutus = QtWidgets.QProgressBar(Form)
        self.progressBar_downloa_stutus.setGeometry(QtCore.QRect(20, 420, 221, 31))
        self.progressBar_downloa_stutus.setStyleSheet("QProgressBar {\n"
"border: 2px solid rgba(33, 37, 43, 180);\n"
"border-radius: 5px;\n"
"text-align: center;\n"
"background-color: rgba(33, 37, 43, 180);\n"
"color: black;\n"
"}\n"
"QProgressBar::chunk {\n"
"    background-color: #FFD700;    \n"
"    border-radius: 5px;\n"
"\n"
"}")
        self.progressBar_downloa_stutus.setObjectName("progressBar_downloa_stutus")
        self.res_comboBox = QtWidgets.QComboBox(Form)
        self.res_comboBox.setGeometry(QtCore.QRect(30, 200, 141, 22))
        self.res_comboBox.setStyleSheet("border-radius: 5px;\n"
"color:#FFF;\n"
"padding: 0 20 0 20;\n"
"background-color: rgb(34,36,44);\n"
"")
        self.res_comboBox.setObjectName("res_comboBox")
        self.res_comboBox.addItem("")
        self.btn_search = QtWidgets.QPushButton(Form)
        self.btn_search.setGeometry(QtCore.QRect(200, 150, 51, 41))
        self.btn_search.setStyleSheet("QPushButton{\n"
"    border: 2px solid rgb(37,39,48);\n"
"    border-radius: 10px;\n"
"    color:#FFF;\n"
"    padding-left: 10px;\n"
"    padding-right: 10px;\n"
"    background-color: rgb(34,36,44);\n"
"    font: 75 9pt \"Terminal\";\n"
"    image: url(:/icon/search.png);\n"
"\n"
"}\n"
"QPushButton:hover{\n"
"    border: 2px solid #FFD700;\n"
"}\n"
"QPushButton:focus{\n"
"    border: 2px solid #FFD700;\n"
"    background-color: rgb(43,45,56);\n"
"\n"
"}")
        self.btn_search.setText("")
        self.btn_search.setObjectName("pushButton")
        self.btn_search.clicked.connect(self.handle_search_clicked)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
    def startAnimation(self):
        self.movie.start()
    def handle_search_clicked(self):
        self.res_comboBox.clear()
        self.btn_search.setEnabled(False)
        self.pushButton_download.setEnabled(False)
        #self.lbl_error.clear()
        self._qpytube = QPyTube(self.lineEdit_url.text())
        self._qpytube.initialized.connect(self.handle_initialized)
        self._qpytube.download_progress_changed.connect(self.progressBar_downloa_stutus.setValue)
        self._qpytube.download_started.connect(self.handle_download_started)
        self._qpytube.download_finished.connect(self.handle_download_finished)
    def show_info_messagebox(self,msgs):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(msgs)
        msg.setWindowTitle("Information MessageBox")
        retval = msg.exec_()

    @QtCore.pyqtSlot(bool, str)
    def handle_initialized(self, status, error=""):
        if status:
            self.res_comboBox.addItems(self._qpytube.resolutions)
            self.pushButton_download.setEnabled(True)
        else:
            #self.lbl_error.setText(error)
            print("error")
        self.btn_search.setEnabled(True)

    def handle_download_clicked(self):
        foldr = filedialog.askdirectory()
        self._qpytube.download(
            self.res_comboBox.currentText(), foldr)
        self.btn_search.setEnabled(False)
        self.pushButton_download.setEnabled(False)
        #self.le_directory.setEnabled(False)
    def handle_download_started(self):
        #self.lbl_error.clear()
        print("started")

    def handle_download_finished(self):
        self.progressBar_downloa_stutus.setValue(100)
        self.btn_search.setEnabled(True)
        self.pushButton_download.setEnabled(True)
        #self.le_directory.setEnabled(True)
        self.show_info_messagebox("Complet Download .. 🎃")

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.lineEdit_url.setPlaceholderText(_translate("Form", "Enter Url Video "))
        self.pushButton_download.setText(_translate("Form", "Download"))
        self.pushButton_3_about_me.setText(_translate("Form", "About Me"))
import icons_rc1


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
