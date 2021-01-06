from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(556, 236)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.btn_tamanho = QtWidgets.QPushButton(self.centralwidget)
        self.btn_tamanho.setObjectName("btn_tamanho")
        self.verticalLayout_2.addWidget(self.btn_tamanho)
        self.btn_copiar = QtWidgets.QPushButton(self.centralwidget)
        self.btn_copiar.setObjectName("btn_copiar")
        self.verticalLayout_2.addWidget(self.btn_copiar)
        self.btn_refatorar = QtWidgets.QPushButton(self.centralwidget)
        self.btn_refatorar.setObjectName("btn_similaridade")
        self.verticalLayout_2.addWidget(self.btn_refatorar)
        self.btn_separar = QtWidgets.QPushButton(self.centralwidget)
        self.btn_separar.setObjectName("btn_separar")
        self.verticalLayout_2.addWidget(self.btn_separar)
        self.btn_sair = QtWidgets.QPushButton(self.centralwidget)
        self.btn_sair.setObjectName("btn_sair")
        self.verticalLayout_2.addWidget(self.btn_sair)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 556, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ferramentas para manipular arquivos"))
        self.btn_tamanho.setText(_translate("MainWindow", "Tamanho dos arquivos "))
        self.btn_copiar.setText(_translate("MainWindow", "fazer bkup e ignorar erros"))
        self.btn_refatorar.setText(_translate("MainWindow", "refatorar diretorio"))
        self.btn_separar.setText(_translate("MainWindow", "separar em pedaços menores/juntar"))
        self.btn_sair.setText(_translate("MainWindow", "sair"))
