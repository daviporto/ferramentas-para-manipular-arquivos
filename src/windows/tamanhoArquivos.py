from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QThread, pyqtSignal
import time
from src.windows.filtro import Ui_Frame
import os

import sys

mesures = {'B': 1, 'KB': 1024, 'MB': 1024 * 1024, 'GB': 1024 * 1024 * 1024}

# mesure = 'KB'
threadAlive = False


class FiltrosFrame(QtWidgets.QMainWindow, Ui_Frame):
    def __init__(self, mainWidow, parent=None):
        super(FiltrosFrame, self).__init__(parent)
        self.setupUi(self, mainWidow)


class FindThread(QThread):
    chang = pyqtSignal(str)

    def __init__(self, dirBase, resultado, files):
        super(FindThread, self).__init__()
        self.dirBase = dirBase
        self.resultado = resultado
        self.files = files

    def run(self):
        global threadAlive
        threadAlive = True
        visited = []
        for (thisDir, subsHere, filesHere) in os.walk(self.dirBase):
            if thisDir not in visited:
                for file in filesHere:
                    if filesHere:
                        currentFile = os.path.join(thisDir, file)
                        try:
                            if os.stat(currentFile).st_size >= 1024:
                                self.files.append(currentFile)
                                time.sleep(0.0001)
                                self.chang.emit("file-> {}\n\tsize-> {:.2f}{}\n".format(currentFile, os.stat(
                                    currentFile).st_size / 1024, 'MB'))
                        except Exception as e:
                            print(e)
                            print("impossivel analizar o aqruivo", currentFile)

                        visited.append(thisDir)

        def comparator(value):
            try:
                return os.stat(value).st_size
            except:
                self.files.remove(value)

        self.files.sort(key=comparator, reverse=True)
        t = WriteThread(files=self.files, measures=1024, measure="KB", chang=self.chang)
        self.resultado.setPlainText("")
        t.start()


class WriteThread(QThread):

    def __init__(self, files, measures, measure, chang, reverse=False):
        super(WriteThread, self).__init__()
        self.files = files
        self.reverse = reverse
        self.measures = measures
        self.measure = measure
        self.chang = chang
        self.threadAlive = threadAlive

    def run(self):
        if not self.reverse:
            for file in self.files:
                self.chang.emit(
                    "file-> {}\n\tsize-> {:.2f}{}\n".format(file, os.stat(file).st_size / self.measures,
                                                            self.measures))
            time.sleep(0.01)
        else:
            for i in range(1, len(self.files)):
                self.chang.emit("file-> {}\n\tsize-> {:.2f}{}\n".format(self.files[-i],
                                                                        os.stat(self.files[-i]).st_size / self.mesures[
                                                                            self.mesure],
                                                                        self.mesure))
                time.sleep(0.0001)
        global threadAlive
        threadAlive = False


class Ui_MainWindow(object):
    def setupUi(self, mainWindow, menuWindow):
        mainWindow.setObjectName("MainWindow")
        mainWindow.resize(642, 545)
        self.menuWindow = menuWindow
        self.files = []
        self.currentMeasure = 'KB'
        self.filtros = [1024, False, [" "], True]
        self.directory = ''
        self.working = False
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.filtrosFrame = FiltrosFrame(mainWindow, self)
        self.someThreadAlive = False

        self.voltar = QtWidgets.QPushButton(self.centralwidget)
        self.voltar.setObjectName("voltar")
        self.voltar.clicked.connect(self.destruir)
        self.gridLayout.addWidget(self.voltar, 2, 2, 1, 1)

        self.btn_filtros = QtWidgets.QPushButton(self.centralwidget)
        self.btn_filtros.setObjectName("filtros")
        self.gridLayout.addWidget(self.btn_filtros, 2, 1, 1, 1)
        self.btn_filtros.clicked.connect(self.showFiltros)

        self.esolher_diretorio = QtWidgets.QPushButton(self.centralwidget)
        self.esolher_diretorio.setObjectName("esolher_diretorio")
        self.gridLayout.addWidget(self.esolher_diretorio, 2, 0, 1, 1)
        self.esolher_diretorio.clicked.connect(self.asrDirectory)

        self.btn_procurar = QtWidgets.QPushButton(self.centralwidget)
        self.btn_procurar.setObjectName("procurar")
        self.gridLayout.addWidget(self.btn_procurar, 2, 3, 1, 1)
        self.btn_procurar.clicked.connect(self.procurar)

        self.resultado = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.resultado.setLocale(QtCore.QLocale(QtCore.QLocale.Portuguese, QtCore.QLocale.Angola))
        self.resultado.setReadOnly(True)
        self.resultado.setPlainText("escolha um diretorio e clike em procurar")
        print(self.resultado.toPlainText())
        self.resultado.setObjectName("resultado")
        self.gridLayout.addWidget(self.resultado, 3, 0, 1, 4)
        mainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def asrDirectory(self):
        self.directory = QFileDialog.getExistingDirectory(self, caption="escolha o diretorio base")
        print(self.directory)

    def showFiltros(self):
        self.filtrosFrame.show()

    def filtrar(self, filtros):
        global threadAlive
        if threadAlive:
            print("already working ")
            return

        print("nothing alive")
        filtered_files = self.files
        if self.filtros[0] != filtros[0]:
            size = filtros[1]
            filtered_files = []
            # deprecated couse exceptions
            # filtered_files = [file for file in self.files if os.stat(file).st_size >= size]
            for file in self.files:
                try:
                    if os.stat(file).st_size >= size:
                        filtered_files.append(file)
                except:
                    pass

        if filtros[3][0] != '':
            extensions = filtros[3]
            if filtros[4]:  # se é para considerar apenas as extensões listadas
                print("on first")
                filtered_files = [file for file in filtered_files if file.split('.')[-1] in extensions]
            else:
                filtered_files = [file for file in filtered_files if file.split('.')[-1] not in extensions]

        self.resultado.setPlainText('')
        if not filtros[2]:
            for file in filtered_files:
                self.resultado.appendPlainText(
                    "file-> {}\n\tsize-> {:.2f}{}\n".format(file, os.stat(file).st_size / mesures[filtros[0]],
                                                            filtros[0]))
        else:
            for i in range(1, len(filtered_files)):
                self.resultado.appendPlainText(
                    "file-> {}\n\tsize-> {:.2f}{}\n".format(filtered_files[-i],
                                                            os.stat(filtered_files[-i]).st_size / mesures[filtros[0]],
                                                            filtros[0]))

    def procurar(self):
        print("done")
        if self.directory != ' ':
            self.files.clear()
            self.resultado.setPlainText("")
            t = FindThread(self.directory, self.resultado, self.files)
            t.chang.connect(self.resultado.appendPlainText)
            t.start()

        #

    def destruir(self):
        self.destroy()
        self.menuWindow.show()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.voltar.setText(_translate("MainWindow", "voltar"))
        self.btn_procurar.setText(_translate("MainWindow", "procurar"))
        self.btn_filtros.setText(_translate("MainWindow", "filtros"))
        self.esolher_diretorio.setText(_translate("MainWindow", "escolher diretorio base"))
