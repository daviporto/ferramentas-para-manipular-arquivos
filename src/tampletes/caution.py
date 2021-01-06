from PyQt5 import QtCore, QtWidgets

class Ui_Caution(QtWidgets.QDialog):
    def __init__(self, parent, text, title):
        super(QtWidgets.QDialog, self).__init__(parent)
        self.setWindowTitle(title)
        self.setObjectName("Dialog")
        self.setWindowModality(QtCore.Qt.NonModal)
        self.resize(409, 182)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setModal(False)
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(30, 140, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.OK)
        self.buttonBox.setObjectName("buttonBox")
        self.lbl_txt = QtWidgets.QLabel(self)
        self.lbl_txt.setGeometry(QtCore.QRect(10, 20, 381, 41))
        self.lbl_txt.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_txt.setText(text)
        self.lbl_txt.setObjectName("lbl_txt")
        self.show()

        self.buttonBox.accepted.connect(self.accepted)
