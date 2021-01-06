from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QThread, pyqtSignal
import os, sys, time

maxfileload = 1000000
tamanho_pecacos = 1024 * 10
cancelar = False


class copyThread(QThread):
    signal = pyqtSignal(str)

    def __init__(self, source, destination, apenasErros=True):
        super(copyThread, self).__init__()
        self.source = source
        self.destination = destination
        self.apenasErros = apenasErros

    def copyfile(self, pathFrom, pathTo, maxfileload=maxfileload):
        global cancelar
        if cancelar:
            self.terminate()
            cancelar = False

        if os.path.getsize(pathFrom) <= maxfileload:
            bytesFrom = open(pathFrom, 'rb').read()  # arquivos pequenos lidos de uma só vez
            open(pathTo, 'wb').write(bytesFrom)
        else:
            fileFrom = open(pathFrom, 'rb')  # arquibos grandes em pedaçõs
            fileTo = open(pathTo, 'wb')
            while True:
                bytesFrom = fileFrom.read(tamanho_pecacos)
                if not bytesFrom: break
                fileTo.write(bytesFrom)

    def copytree(self, dirFrom, dirTo):
        for filename in os.listdir(dirFrom):  # for files/dirs here
            pathFrom = os.path.join(dirFrom, filename)
            pathTo = os.path.join(dirTo, filename)  # extend both paths
            if not os.path.isdir(pathFrom):  # copy simple files
                try:
                    if not self.apenasErros:
                        self.signal.emit('copying' + pathFrom + 'to' + pathTo)
                        self.copyfile(pathFrom, pathTo)
                    # fcount += 1
                except:
                    self.signal.emit('Error copying' + pathFrom + 'to' + pathTo + '--skipped')
                    self.signal.emit(str(sys.exc_info()[0]) + '\n' + str(sys.exc_info()[1]))
            else:
                if not self.apenasErros:
                    self.signal.emit('copying dir' + pathFrom + 'to' + pathTo)
                try:
                    os.mkdir(pathTo)  # make new subdir
                    below = self.copytree(pathFrom, pathTo)  # recur into subdirs
                    # fcount += below[0]  # add subdir  counts
                    # dcount += below[1]
                    # dcount += 1
                except:
                    self.signal.emit('Error creating' + pathTo + '--skipped')
                    self.signal.emit(sys.exc_info()[0])
                    self.signal.emit(sys.exc_info()[1])

    def run(self):
        while True:
            try:
                os.mkdir(self.destination)
                break
            except:
                self.destination = self.destination + '1'

        self.copytree(self.source, self.destination)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow, menuWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(619, 526)
        self.source_directory = self.destination_folder = ''
        self.menuWindow = menuWindow
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.btn_fazerBkup = QtWidgets.QPushButton(self.centralwidget)
        self.btn_fazerBkup.setObjectName("fazer Bkup")
        self.btn_fazerBkup.clicked.connect(self.fazerBkup)
        self.gridLayout.addWidget(self.btn_fazerBkup, 6, 0, 1, 1)
        self.btn_mostrarApenasErros = QtWidgets.QCheckBox(self.centralwidget)
        self.btn_mostrarApenasErros.setObjectName("mostrarApenasErros")
        self.btn_mostrarApenasErros.setChecked(True)
        self.gridLayout.addWidget(self.btn_mostrarApenasErros, 6, 1, 1, 1)
        self.btn_cancelar = QtWidgets.QPushButton(self.centralwidget)
        self.btn_cancelar.setObjectName("cancelar")
        self.btn_cancelar.clicked.connect(self.cancelar)
        self.gridLayout.addWidget(self.btn_cancelar, 6, 2, 1, 1)
        self.lbl_dirCopia = QtWidgets.QLabel(self.centralwidget)
        self.lbl_dirCopia.setMinimumSize(QtCore.QSize(0, 35))
        self.lbl_dirCopia.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_dirCopia.setObjectName("lbl_dirCopia")
        self.gridLayout.addWidget(self.lbl_dirCopia, 1, 0, 1, 3)
        self.lbl_dirSave = QtWidgets.QLabel(self.centralwidget)
        self.lbl_dirSave.setMinimumSize(QtCore.QSize(0, 35))
        self.lbl_dirSave.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_dirSave.setObjectName("lbl_dirSave")
        self.gridLayout.addWidget(self.lbl_dirSave, 5, 0, 1, 3)
        self.btn_diretorioCopia = QtWidgets.QPushButton(self.centralwidget)
        self.btn_diretorioCopia.setObjectName("btn_diretorioCopia")
        self.btn_diretorioCopia.clicked.connect(self.askSourceDirectory)
        self.gridLayout.addWidget(self.btn_diretorioCopia, 0, 0, 1, 3)
        self.btn_Save = QtWidgets.QPushButton(self.centralwidget)
        self.btn_Save.setObjectName("btn_Save")
        self.btn_Save.clicked.connect(self.askDestinationFolder)
        self.gridLayout.addWidget(self.btn_Save, 3, 0, 1, 3)
        self.txt_relatorio = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.txt_relatorio.setObjectName("txt_relatorio")
        self.txt_relatorio.setReadOnly(True)
        self.gridLayout.addWidget(self.txt_relatorio, 7, 0, 1, 3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 619, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def cancelar(self):
        global cancelar
        cancelar = True

    def askSourceDirectory(self):
        self.source_directory = QFileDialog.getExistingDirectory(self, caption='selecione o diretoria para fazer bkup')
        self.lbl_dirCopia.setText(self.source_directory)

    def askDestinationFolder(self):
        self.destination_folder = QFileDialog.getExistingDirectory(self, caption='selecione a pasta de destino')
        self.lbl_dirSave.setText(self.destination_folder)
        if self.destination_folder:
            self.destination_folder = os.path.join(self.destination_folder, "myBkup")

    def fazerBkup(self):
        if not self.source_directory:
            self.txt_relatorio.setPlainText("")
            self.txt_relatorio.setPlainText("por favor seleciono o diretorio que deseja fazer bkup primeiro")
            return
        if not self.destination_folder:
            self.txt_relatorio.setPlainText("")
            self.txt_relatorio.setPlainText("por favor seleciono o diretorio aonde deseja salvar o bkup primeiro")
            return
        self.txt_relatorio.setPlainText("")
        t = copyThread(self.source_directory, self.destination_folder, self.btn_mostrarApenasErros.isChecked())
        t.signal.connect(self.txt_relatorio.appendPlainText)
        t.start()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Bkup"))
        self.lbl_dirCopia.setText(_translate("MainWindow", "diretorio a ser copiado"))
        self.lbl_dirSave.setText(_translate("MainWindow", "diretorio a ser copiado"))
        self.btn_diretorioCopia.setText(_translate("MainWindow", "selecione o diretorio a ser copiado "))
        self.btn_Save.setText(_translate("MainWindow", "selecione o local para salvar a cópia "))
        self.btn_fazerBkup.setText(_translate("MainWindow", "fazer bkup"))
        self.btn_mostrarApenasErros.setText(_translate("MainWindow", "mostrar apenas erros"))
        self.btn_cancelar.setText(_translate("MainWindow", "parar"))
