from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Entry(QtWidgets.QDialog):
    signal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None, title='Dialog', lblText='digite o valor de entrada'):
        super(Ui_Entry, self).__init__(parent)
        self.setObjectName("Dialog")
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.resize(490, 190)
        self.setWindowTitle(title)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setModal(True)
        self.lbl_text = QtWidgets.QLabel(self)
        self.lbl_text.setGeometry(QtCore.QRect(0, 20, 481, 21))
        self.lbl_text.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_text.setObjectName("lbl_text")
        self.lbl_text.setText(lblText)
        self.ln_entry = QtWidgets.QLineEdit(self)
        self.ln_entry.setGeometry(QtCore.QRect(0, 60, 481, 51))
        self.ln_entry.setObjectName("ln_entry")
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(150, 130, 161, 41))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("pronto")
        self.pushButton.clicked.connect(self.pronto)
        self.show()

    def pronto(self):
        self.signal.emit(self.ln_entry.text())
        self.close()
