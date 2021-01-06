import os
import sys
import time

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal, QThread, QRegularExpression
from PyQt5.QtWidgets import QFileDialog

from src.highliter import Highlighter
from src.tampletes.dialog import Ui_Dialog
from src.tampletes.entryDialog import Ui_Entry

default_extensions = "java,py,pyw,txt,odt,c,c++"


class refactorThread(QThread):
    appendTextSigal = pyqtSignal(str)
    setTextSignal = pyqtSignal(str)
    statusBarSignal = pyqtSignal(str)
    focousSignal = pyqtSignal(int, int)

    refactorAll = False
    refactor = False
    pular = False
    substituirPor = ''

    def __init__(self, directory, expression):
        super(refactorThread, self).__init__()
        self.directory = directory
        self.expression = expression

    def run(self):
        self.searchTree(self.directory)
        self.statusBarSignal.emit("termino/inativo")

    def enable_refactor_all(self):
        self.refactorAll = True

    def searchTree(self, dir):
        self.statusBarSignal.emit(f"varrendo diretorio {dir}")
        for filename in os.listdir(dir):  # for files/dirs here
            if not os.path.isdir(filename):  # copy simple files
                self.statusBarSignal.emit(f'analisando se o arquivo: {filename} esta na lista')
                if filename.split('.')[-1] in default_extensions:
                    try:
                        print(filename.split('.')[-1])
                        file = open(os.path.join(dir, filename))
                        self.statusBarSignal.emit(f'abrindo arquivo {filename}')
                        content = file.read()
                        self.setTextSignal.emit(content)
                        content = self.findMatches(content)
                        file = open(os.path.join(dir, filename), 'w')
                        file.write(content)
                    except:
                        self.statusBarSignal.emit(f'erro ao abrir o arquivo{filename}')
                        self.setTextSignal.emit('')
                        self.appendTextSigal.emit(f'Error openning file {filename}--skipped')
                        self.appendTextSigal.emit(str(sys.exc_info()[0]) + '\n' + str(sys.exc_info()[1]))
                        print(str(sys.exc_info()[0]) + '\n' + str(sys.exc_info()[1]))
                    finally:
                        if file:
                            file.close()
                            self.statusBarSignal.emit(f"fechando arquivo{filename}")
            else:
                self.searchTree(filename)  # recur into subdirs

    def findMatches(self, content):
        refactorThread.reset_actions()
        matches = (self.expression.globalMatch(content))
        offset = 0
        while matches.hasNext():
            match = matches.next()
            self.focousSignal.emit(match.capturedStart() + offset, match.capturedLength())
            refactorThread.reset_actions(True)
            while True:
                if refactorThread.refactorAll:
                    content, _offset = self._replace(content, match.capturedStart() + offset, match.capturedLength())
                    offset += _offset
                    self.setTextSignal.emit(content)
                    break
                elif refactorThread.refactor:
                    content, _offset = self._replace(content, match.capturedStart() + offset, match.capturedLength())
                    offset += _offset
                    self.setTextSignal.emit(content)
                    break
                elif refactorThread.pular:
                    break
                time.sleep(0.05)
        return content



    def _replace(self, content, curretIndice, size):
        content = list(content)
        maxindice = 0
        for l in range(size):
            content.pop(curretIndice)
        for i, l in enumerate(list(refactorThread.substituirPor)):
            content.insert(curretIndice + i, l)
            maxindice = i
        return ''.join(content), maxindice

    @staticmethod
    def comparator(obj):
        return obj.capturedStart()

    @staticmethod
    def reset_actions(scapeRefactorAll=False):
        if not scapeRefactorAll:
            refactorThread.refactor = refactorThread.refactorAll = refactorThread.pular = False
        else:
            refactorThread.refactor = refactorThread.pular = False



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(673, 525)
        self.diretorio = ''
        self.txtAlvo = ''
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.btn_escolheDiretorio = QtWidgets.QPushButton(self.centralwidget)
        self.btn_escolheDiretorio.setObjectName("btn_escolheDiretorio")
        self.gridLayout.addWidget(self.btn_escolheDiretorio, 0, 0, 1, 2)
        self.lbl_diretorio = QtWidgets.QLabel(self.centralwidget)
        self.lbl_diretorio.setObjectName("lbl_diretorio")
        self.gridLayout.addWidget(self.lbl_diretorio, 0, 2, 1, 2)
        self.lbl_extensoesPossivel = QtWidgets.QLabel(self.centralwidget)
        self.lbl_extensoesPossivel.setObjectName("lbl_extensoesPossivel")
        self.gridLayout.addWidget(self.lbl_extensoesPossivel, 1, 0, 1, 4)
        self.txtextensions = QtWidgets.QTextEdit(self.centralwidget)
        self.txtextensions.setObjectName("txtextensions")
        self.txtextensions.setText(default_extensions)
        self.gridLayout.addWidget(self.txtextensions, 2, 0, 1, 4)
        self.cb_palavraToda = QtWidgets.QCheckBox(self.centralwidget)
        self.cb_palavraToda.setObjectName("cb_palavraToda")
        self.gridLayout.addWidget(self.cb_palavraToda, 3, 0, 1, 1)
        self.cb_keySensitive = QtWidgets.QCheckBox(self.centralwidget)
        self.cb_keySensitive.setObjectName("cb_keySensitive")
        self.gridLayout.addWidget(self.cb_keySensitive, 3, 1, 1, 2)
        self.lne_textAlvo = QtWidgets.QLineEdit(self.centralwidget)
        self.lne_textAlvo.setObjectName("lne_textAlvo")
        self.gridLayout.addWidget(self.lne_textAlvo, 3, 3, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 673, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dockWidget = QtWidgets.QDockWidget(MainWindow)
        # self.dockWidget.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea)
        self.dockWidget.setObjectName("dockWidget")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidget.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable |
                                    QtWidgets.QDockWidget.DockWidgetMovable |
                                    QtWidgets.QDockWidget.DockWidgetVerticalTitleBar)
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.dockWidgetContents)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.lne_substituirPor = QtWidgets.QLineEdit(self.dockWidgetContents)
        self.lne_substituirPor.setObjectName("lne_substituirPor")
        self.gridLayout_2.addWidget(self.lne_substituirPor, 0, 0, 1, 3)
        self.txt_textoAlvo = QtWidgets.QTextEdit(self.dockWidgetContents)
        self.txt_textoAlvo.setObjectName("txt_textoAlvo")
        self.gridLayout_2.addWidget(self.txt_textoAlvo, 1, 0, 1, 3)
        self.btn_sustituir = QtWidgets.QPushButton(self.dockWidgetContents)
        self.btn_sustituir.setObjectName("btn_sustituir")
        self.gridLayout_2.addWidget(self.btn_sustituir, 2, 0, 1, 1)
        self.btn_substituirTodos = QtWidgets.QPushButton(self.dockWidgetContents)
        self.btn_substituirTodos.setObjectName("btn_substituirTodos")
        self.gridLayout_2.addWidget(self.btn_substituirTodos, 2, 2, 1, 1)
        self.dockWidget.setWidget(self.dockWidgetContents)
        self.btnProcurar = QtWidgets.QPushButton(MainWindow)
        self.btnProcurar.clicked.connect(self.procurar)
        self.btnProcurar.setText("procurar")
        self.gridLayout.addWidget(self.btnProcurar, 4, 0, 1, 4)
        self.btnPular = QtWidgets.QPushButton(self.dockWidgetContents)
        self.btnPular.setText("pular")
        self.gridLayout_2.addWidget(self.btnPular, 2, 1, 1, 1)
        self.lbl_status = QtWidgets.QLabel()
        self.statusbar.addPermanentWidget(self.lbl_status)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.dockWidget)
        self.highlother = Highlighter(self.txt_textoAlvo.document())

        self.lne_textAlvo.textChanged.connect(self.txtAlvoChanged)
        self.cb_palavraToda.clicked.connect(self.txtAlvoChanged)
        self.cb_keySensitive.clicked.connect(self.txtAlvoChanged)
        self.btn_escolheDiretorio.clicked.connect(self.escolherDiretorio)
        self.btn_sustituir.clicked.connect(self.setRefactor)
        self.btn_substituirTodos.clicked.connect(self.setRefactorAll)
        self.btnPular.clicked.connect(self.setPular)
        self.txtextensions.textChanged.connect(self.extensionsChanged)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.txtextensions, self.btn_escolheDiretorio)

    def setRefactor(self):
        refactorThread.substituirPor = self.lne_substituirPor.text()
        refactorThread.refactor = True

    def setRefactorAll(self):
        refactorThread.substituirPor = self.lne_substituirPor.text()
        refactorThread.refactorAll = True

    def setPular(self):
        refactorThread.pular = True
        print(refactorThread.pular)

    def txtAlvoChanged(self, txt=None):
        self.highlother.setExpression(self.lne_textAlvo.text(), self.cb_keySensitive.isChecked(), self.cb_palavraToda.isChecked())

    def escolherDiretorio(self):
        self.diretorio = QFileDialog.getExistingDirectory(self, caption="escolha o diretorio alvo")
        self.lbl_diretorio.setText(self.diretorio)

    def extensionsChanged(self):
        global default_extensions
        default_extensions = self.txtextensions.toPlainText()

    def procurar(self):
        if not self.diretorio:
            Ui_Dialog(text="selecione o diretorio alvo primeiro",
                      title="diretorio alvo",
                      buttonText="selecionar",
                      action=self.selecionarDiretorioDialog)
            return

        self.txtAlvo = self.lne_textAlvo.text()
        print(self.txtAlvo)
        if self.txtAlvo == '' or self.txtAlvo == 'Texto alvo':
            a = Ui_Entry(
                parent=self,
                lblText='digite o texto alvo, que será procurado',
                title="valro alvo",
            )
            a.signal.connect(self.dialogPronto)
            return

        exp =self.lne_textAlvo.text()
        if self.cb_palavraToda.isChecked():
            exp = "\\b" + exp + "\\b"

        if not self.cb_keySensitive.isChecked():
            self.expression = QRegularExpression(exp)
        else:
            self.expression = QRegularExpression(exp, QRegularExpression.CaseInsensitiveOption)

        t = refactorThread(self.diretorio, self.expression)
        t.appendTextSigal.connect(self.txt_textoAlvo.append)
        t.setTextSignal.connect(self.txt_textoAlvo.setText)
        t.statusBarSignal.connect(self.lbl_status.setText)
        t.focousSignal.connect(self.setFocousFormat)
        t.start()

    def selecionarDiretorioDialog(self):
        self.escolherDiretorio()
        self.procurar()

    @QtCore.pyqtSlot(str)
    def dialogPronto(self, text):
        print(text)
        self.lne_textAlvo.setText(text)
        self.procurar()

    @QtCore.pyqtSlot(int, int)
    def setFocousFormat(self, start, size):
        self.highlother.currentFocoused(start, size)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "refatorar conteudo no diretorio "))
        self.btn_escolheDiretorio.setText(_translate("MainWindow", "escolher diretorio "))
        self.lbl_diretorio.setText(_translate("MainWindow", "diretorio-> "))
        self.lbl_extensoesPossivel.setText(
            _translate("MainWindow", "extensõs possivel, arquivos que serão refatorados, Ex. txt,py,java"))
        self.cb_palavraToda.setText(_translate("MainWindow", "palavra toda"))
        self.cb_keySensitive.setText(_translate("MainWindow", "key Sensitive"))
        self.lne_textAlvo.setText(_translate("MainWindow", "Texto alvo"))
        self.lne_substituirPor.setText(_translate("MainWindow", "substituir por"))
        self.btn_sustituir.setText(_translate("MainWindow", "subtituir"))
        self.btn_substituirTodos.setText(_translate("MainWindow", "substituir todos"))
