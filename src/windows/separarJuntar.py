from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from src.tampletes.dialog import Ui_Dialog
from src.tampletes.caution import Ui_Caution

import os
import time

ThreadWorking = False


class ThreadSeparar(QThread):
    signal = pyqtSignal(str)

    def __init__(self, file, local_save, pieces_size=None):
        super(ThreadSeparar, self).__init__()
        self.size = pieces_size
        print(self.size)
        self.file_from = os.path.join(file)
        self.extension = self.file_from.split(".")[-1]
        self.file_to = os.path.join(local_save, "partes")

    def run(self):
        global ThreadWorking
        ThreadWorking = True
        if not os.path.exists(self.file_to):  # caller handles errors
            os.mkdir(self.file_to)  # make dir, read/write parts
        else:
            for fname in os.listdir(self.file_to):  # delete any existing files
                os.remove(os.path.join(self.file_to, fname))
                self.signal.emit("excluindo conteudo anterior -> " + os.path.join(self.file_to, fname))
        partnum = 0
        with open(self.file_from, 'rb') as input:
            while True:
                chunk = input.read(self.size)
                if not chunk: break  # empty mens end
                partnum += 1
                filename = os.path.join(self.file_to, ('part{:04d}.{}'.format(partnum, self.extension)))
                with open(filename, 'wb') as fileobj:
                    fileobj.write(chunk)
                    self.signal.emit("writing part -> " + filename)
        self.signal.emit(40 * '-')
        self.signal.emit('done')
        self.signal.emit(40 * '-')
        ThreadWorking = False


class ThreadJuntar(QThread):
    signal = pyqtSignal(str)

    def __init__(self, directory):
        super(ThreadJuntar, self).__init__()
        self.directory = directory

    def run(self):
        global ThreadWorking
        ThreadWorking = True
        parts = os.listdir(self.directory)
        parts.sort()
        extension = parts[0].split(".")[-1]
        with open(os.path.join(self.directory,'original' + extension), 'wb') as original:
            for filename in parts:
                filepath = os.path.join(self.directory, filename)
                with open(filepath, 'rb') as part:
                    self.signal.emit("juntando a parte -> " + filename)
                    while True:
                        filebytes = part.read(1024)
                        if not filebytes:
                            break
                        original.write(filebytes)
                    self.signal.emit("parte " + filename + " junta com sucesso")

        self.signal.emit(60 * '-')
        self.signal.emit('done')
        self.signal.emit("arquivo salvo como original em ->" + self.directory)
        self.signal.emit("mesma pasta em que as partes se encontram")
        self.signal.emit(60 * '-')
        ThreadWorking = False


class Ui_separjuntarar(object):
    def setupUi(self, separjuntarar):
        separjuntarar.setObjectName("separjuntarar")
        separjuntarar.resize(523, 465)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(separjuntarar.sizePolicy().hasHeightForWidth())
        separjuntarar.setSizePolicy(sizePolicy)
        self.file = self.local_save = ''
        self.centralwidget = QtWidgets.QWidget(separjuntarar)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.rb_separar = QtWidgets.QRadioButton(self.groupBox)
        self.rb_separar.setGeometry(QtCore.QRect(10, 10, 106, 23))
        self.rb_separar.setChecked(True)
        self.rb_separar.setObjectName("rb_jutnar")
        self.rb_juntar = QtWidgets.QRadioButton(self.groupBox)
        self.rb_juntar.setGeometry(QtCore.QRect(110, 10, 106, 23))
        self.rb_juntar.setObjectName("radioButton_2")
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 3)
        self.lbl_tamanhoPedacos = QtWidgets.QLabel(self.centralwidget)
        self.lbl_tamanhoPedacos.setObjectName("lbl_tamanhoPedacos")
        self.gridLayout.addWidget(self.lbl_tamanhoPedacos, 1, 0, 1, 1)
        self.spn_tamanho = QtWidgets.QSpinBox(self.centralwidget)
        self.spn_tamanho.setMaximum(999999999)
        self.spn_tamanho.setMinimum(1)
        self.spn_tamanho.setSuffix(" MB")
        self.spn_tamanho.setObjectName("spn_tamanho")
        self.gridLayout.addWidget(self.spn_tamanho, 1, 1, 1, 1)
        self.cb_measure = QtWidgets.QComboBox(self)
        self.cb_measure.addItems(["B", "KB", "MB", "GB"])
        self.cb_measure.setCurrentIndex(2)
        self.gridLayout.addWidget(self.cb_measure, 1, 2, 1, 1)
        self.btn_escolherArquivo = QtWidgets.QPushButton(self.centralwidget)
        self.btn_escolherArquivo.setObjectName("btn_escolherArquivo")
        self.gridLayout.addWidget(self.btn_escolherArquivo, 2, 0, 1, 2)
        self.btn_action = QtWidgets.QPushButton(self.centralwidget)
        self.btn_action.setObjectName("btn_action")
        self.gridLayout.addWidget(self.btn_action, 2, 2, 1, 1)
        self.txt_relatorio = QtWidgets.QTextEdit(self.centralwidget)
        self.txt_relatorio.setObjectName("txt_relatorio")
        self.gridLayout.addWidget(self.txt_relatorio, 3, 0, 1, 3)
        separjuntarar.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(separjuntarar)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 523, 22))
        self.menubar.setObjectName("menubar")
        separjuntarar.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(separjuntarar)
        self.statusbar.setObjectName("statusbar")
        separjuntarar.setStatusBar(self.statusbar)

        self.rb_separar.toggled.connect(self.dividrOuJuntar)
        self.cb_measure.currentTextChanged.connect(self.cb_changed)
        self.btn_escolherArquivo.clicked.connect(self.escolher_arquivo)
        self.btn_action.clicked.connect(self.action)

        self.retranslateUi(separjuntarar)
        QtCore.QMetaObject.connectSlotsByName(separjuntarar)

    def dividrOuJuntar(self):
        if self.rb_separar.isChecked():
            self.spn_tamanho.setEnabled(True)
            self.cb_measure.setEnabled(True)
            self.btn_escolherArquivo.setText("escolher arquivo")
            self.btn_action.setText("separar")
        else:
            self.spn_tamanho.setEnabled(False)
            self.cb_measure.setEnabled(False)
            self.btn_escolherArquivo.setText("escolher diretorio")
            self.btn_action.setText("juntar")
            print("separar on ")

    def cb_changed(self):
        self.spn_tamanho.setSuffix(" " + self.cb_measure.currentText())

    def action(self):
        global ThreadWorking
        if ThreadWorking:
            Ui_Caution(self,
                       title="processo já em funcionamento",
                       text="espere pelo fim do processo para iniciar outro")
            return
        if self.rb_separar.isChecked():
            if not self.file:
                dialog = Ui_Dialog(text="escolha o arquivo a ser salvo",
                                   title="arquivo a ser separado",
                                   parent=self,
                                   action=self.escolher_arquivo_dialog)
                print("file-> ", self.file)
                return
            size = self.spn_tamanho.value()
            if self.cb_measure.currentIndex():  # > 0 AKA nao B
                size = 1024 ** (self.cb_measure.currentIndex())

            if not self.local_save:
                save_dialog = Ui_Dialog(text='slecione o local para salvar',
                                        title='save',
                                        parent=self,
                                        action=self.escolher_diretorio)
                return

            a = ThreadSeparar(self.file, self.local_save, size)
            self.txt_relatorio.clear()
            a.signal.connect(self.txt_relatorio.append)
            a.start()
        else:
            if not self.file:
                dialog = Ui_Dialog(text="escolha a pasta com as partes",
                                   title="partes ",
                                   parent=self,
                                   action=self.escolher_diertorio_partes)
                print("file-> ", self.file)
                return
            a = ThreadJuntar(self.file)
            self.txt_relatorio.clear()
            a.signal.connect(self.txt_relatorio.append)
            self.file = self.local_save = ''
            a.start()

    def escolher_arquivo(self):
        if self.rb_separar.isChecked():
            self.file = QtWidgets.QFileDialog.getOpenFileName(self, caption="arquivo a ser separado")[0]
            print(self.file)
        else:
            self.file = QtWidgets.QFileDialog.getExistingDirectory(self, caption="diretorio onde as partes estão")

    def escolher_arquivo_dialog(self):
        self.file = QtWidgets.QFileDialog.getOpenFileName(self)[0]
        if self.file:
            self.action()

    def escolher_diretorio(self):
        self.local_save = QtWidgets.QFileDialog.getExistingDirectory(self)
        if self.local_save:
            self.action()

    def escolher_diertorio_partes(self):
        self.file = QtWidgets.QFileDialog.getExistingDirectory(self)
        if self.file:
            self.action()

    def retranslateUi(self, separjuntarar):
        _translate = QtCore.QCoreApplication.translate
        separjuntarar.setWindowTitle(_translate("separjuntarar", "separar juntar arquivos"))
        self.rb_separar.setText(_translate("separjuntarar", "separar"))
        self.rb_juntar.setText(_translate("separjuntarar", "juntar"))
        self.lbl_tamanhoPedacos.setText(_translate("separjuntarar", "tamanho dos pedaços"))
        self.btn_escolherArquivo.setText(_translate("separjuntarar", "escolher arquivo"))
        self.btn_action.setText(_translate("separjuntarar", "separar"))
        self.txt_relatorio.setHtml(_translate("separjuntarar",
                                              "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                              "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                              "p, li { white-space: pre-wrap; }\n"
                                              "</style></head><body style=\" font-family:\'Fira Sans Semi-Light\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
                                              "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">ou solte os aqui </p>\n"
                                              "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
