from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Frame(object):
    def setupUi(self, Frame, mainWindow):
        self.Frame = Frame
        self.Frame.setObjectName("Frame")
        self.Frame.resize(474, 283)
        self.Frame.setMinimumSize(QtCore.QSize(474, 283))
        self.Frame.setMaximumSize(QtCore.QSize(474, 283))
        self.mainWindow = mainWindow
        self.lbl_tamanhoMinimo = QtWidgets.QLabel(Frame)
        self.lbl_tamanhoMinimo.setGeometry(QtCore.QRect(9, 9, 116, 17))
        self.lbl_tamanhoMinimo.setMinimumSize(QtCore.QSize(1, 0))
        self.lbl_tamanhoMinimo.setObjectName("lbl_tamanhoMinimo")
        self.spin_tamanhoMaximo = QtWidgets.QSpinBox(Frame)
        self.spin_tamanhoMaximo.setGeometry(QtCore.QRect(131, 9, 111, 26))
        self.spin_tamanhoMaximo.setValue(1)
        self.spin_tamanhoMaximo.setMaximum(99999999)
        self.spin_tamanhoMaximo.setObjectName("spin_tamanhoMaximo")
        self.cb_ordemCrescente = QtWidgets.QCheckBox(Frame)
        self.cb_ordemCrescente.setGeometry(QtCore.QRect(9, 41, 131, 23))
        self.cb_ordemCrescente.setObjectName("checkBox")
        self.textEdit = QtWidgets.QTextEdit(Frame)
        self.textEdit.setGeometry(QtCore.QRect(9, 93, 427, 88))
        self.textEdit.setObjectName("textEdit")
        self.lbl_extensoes = QtWidgets.QLabel(Frame)
        self.lbl_extensoes.setGeometry(QtCore.QRect(31, 70, 381, 20))
        self.lbl_extensoes.setObjectName("lbl_extensoes")
        self.btn_filtrar = QtWidgets.QPushButton(Frame)
        self.btn_filtrar.setGeometry(QtCore.QRect(170, 250, 121, 25))
        self.btn_filtrar.setObjectName("btn_filtrar")
        self.btn_filtrar.clicked.connect(self.filtrar)
        self.gb_mesure = QtWidgets.QGroupBox(Frame)
        self.gb_mesure.setGeometry(QtCore.QRect(250, 0, 211, 41))
        self.gb_mesure.setTitle("")
        self.gb_mesure.setObjectName("groupBox")
        self.rb_B = QtWidgets.QRadioButton(self.gb_mesure)
        self.rb_B.setGeometry(QtCore.QRect(10, 10, 34, 23))
        self.rb_B.setObjectName("rb_B")
        self.rb_KB = QtWidgets.QRadioButton(self.gb_mesure)
        self.rb_KB.setGeometry(QtCore.QRect(50, 10, 43, 23))
        self.rb_KB.setObjectName("rb_KB")
        self.rb_MB = QtWidgets.QRadioButton(self.gb_mesure)
        self.rb_MB.setGeometry(QtCore.QRect(100, 10, 46, 23))
        self.rb_MB.setObjectName("rb_MB")
        self.rb_KB.setChecked(True)
        self.rb_GB = QtWidgets.QRadioButton(self.gb_mesure)
        self.rb_GB.setGeometry(QtCore.QRect(150, 10, 44, 23))
        self.rb_GB.setObjectName("rb_GB")
        self.gb_inclusive = QtWidgets.QGroupBox(Frame)
        self.gb_inclusive.setGeometry(QtCore.QRect(10, 180, 231, 61))
        self.gb_inclusive.setTitle("")
        self.gb_inclusive.setObjectName("groupBox_2")
        self.rb_apenasListadas = QtWidgets.QRadioButton(self.gb_inclusive)
        self.rb_apenasListadas.setGeometry(QtCore.QRect(10, 10, 216, 23))
        self.rb_apenasListadas.setObjectName("rb_apenasListadas")
        self.rb_apenasListadas.setChecked(True)
        self.rb_excetoListadas = QtWidgets.QRadioButton(self.gb_inclusive)
        self.rb_excetoListadas.setGeometry(QtCore.QRect(10, 30, 212, 23))
        self.rb_excetoListadas.setObjectName("rb_excetoListadas")

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def filtrar(self):
        filtros = []
        size = self.spin_tamanhoMaximo.value()

        if self.rb_B.isChecked():
            size = size
            filtros.append('B')
        elif self.rb_KB.isChecked():
            size = size * 1024
            filtros.append('KB')
        elif self.rb_MB.isChecked():
            size = size * 1024 * 1024
            filtros.append('MB')
        elif self.rb_GB.isChecked():
            size = size * 1024 * 1024 * 1024
            filtros.append('GB')

        filtros.append(size)
        filtros.append(self.cb_ordemCrescente.isChecked())
        filtros.append(self.textEdit.toPlainText().split(','))
        filtros.append(self.rb_apenasListadas.isChecked())

        self.Frame.hide()
        self.mainWindow.filtrar(filtros)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "Filtros"))
        self.lbl_tamanhoMinimo.setText(_translate("Frame", "tamanho minimo "))
        self.cb_ordemCrescente.setText(_translate("Frame", "orden crescebte"))
        self.lbl_extensoes.setText(_translate("Frame", "extensões, separe-as por virgula. Eg-> pt,java,txt,html"))
        self.btn_filtrar.setText(_translate("Frame", "filtrar"))
        self.rb_B.setText(_translate("Frame", "B"))
        self.rb_KB.setText(_translate("Frame", "KB"))
        self.rb_MB.setText(_translate("Frame", "MB"))
        self.rb_GB.setText(_translate("Frame", "GB"))
        self.rb_apenasListadas.setText(_translate("Frame", "apenas as extensões listadas"))
        self.rb_excetoListadas.setText(_translate("Frame", "exceto as extensões listadas"))
