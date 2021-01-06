import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication

from src.windows import tamanhoArquivos, laucher, bkup, separarJuntar, refatorar
import qdarkstyle



class TamanhoArquivos(QtWidgets.QMainWindow, tamanhoArquivos.Ui_MainWindow):
    def __init__(self, menuWindow, parent=None, ):
        super(TamanhoArquivos, self).__init__(parent)
        self.setupUi(self, menuWindow)


class Bkup(QtWidgets.QMainWindow, bkup.Ui_MainWindow):
    def __init__(self, menuWindow, parent=None,):
        super(Bkup, self).__init__(parent)
        self.setupUi(self, menuWindow)

class SepararJuntar(QtWidgets.QMainWindow, separarJuntar.Ui_separjuntarar):
    def __init__(self, parent=None, ):
        super(SepararJuntar, self).__init__(parent)
        self.setupUi(self)

class Refatorar(QtWidgets.QMainWindow, refatorar.Ui_MainWindow):
    def __init__(self, parent=None):
        super(Refatorar, self).__init__(parent)
        self.setupUi(self)


class MainMenuFrame(QtWidgets.QMainWindow, laucher.Ui_MainWindow):
    def __init__(self, parent=None):
        print('initiating')
        app = QApplication(sys.argv)
        app.setStyleSheet(qdarkstyle.load_stylesheet())
        super(MainMenuFrame, self).__init__(parent)
        self.setupUi(self)
        self.btn_tamanho.clicked.connect(self.tamanho_arquivos)
        self.btn_sair.clicked.connect(self.destroy)
        self.btn_copiar.clicked.connect(self.bkup)
        self.btn_separar.clicked.connect(self.separar_juntar)
        self.btn_refatorar.clicked.connect(self.refatorar)
        self.show()
        app.exec_()

    def tamanho_arquivos(self):
        self.a = TamanhoArquivos(self)
        self.a.show()
        self.hide()

    def bkup(self):
        self.a = Bkup(self)
        self.a.show()
        self.hide()

    def separar_juntar(self):
        self.a = SepararJuntar(self)
        self.a.show()
        self.hide()

    def refatorar(self):
        self.a = Refatorar(self)
        self.a.show()
        self.hide()

if __name__ == '__main__':
    MainMenuFrame()
