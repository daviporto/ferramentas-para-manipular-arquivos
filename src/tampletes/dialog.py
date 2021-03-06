from PyQt5 import QtCore, QtWidgets


class Ui_Dialog(QtWidgets.QDialog):
    def __init__(self, text, title,action, buttonText='escolher',parent=None):
        super(Ui_Dialog, self).__init__(parent)
        self.setWindowTitle(title)
        self.setObjectName("Dialog")
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.resize(409, 182)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setModal(True)
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(30, 140, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.setObjectName("buttonBox")
        self.lbl_txt = QtWidgets.QLabel(self)
        self.lbl_txt.setGeometry(QtCore.QRect(10, 20, 381, 41))
        self.lbl_txt.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_txt.setText(text)
        self.lbl_txt.setObjectName("lbl_txt")
        self.btn_escolher = QtWidgets.QPushButton(self)
        self.btn_escolher.setGeometry(QtCore.QRect(50, 80, 281, 31))
        self.btn_escolher.setObjectName("btn_escolher")
        self.btn_escolher.setText(buttonText)
        self.btn_escolher.clicked.connect(action)
        self.show()

        self.buttonBox.rejected.connect(self.reject)
        self.btn_escolher.clicked.connect(self.accept)
