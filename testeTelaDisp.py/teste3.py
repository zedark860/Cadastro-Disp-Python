import sys
import json
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QFileDialog, QMessageBox, QTableView
import pandas as pd

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_LoginDialog()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.login)

    def login(self):
        username = self.ui.lineEdit_2.text()
        password = self.ui.lineEdit.text()
        if self.check_login(username, password):
            global logged_in
            logged_in = True  # Definir a variável global como True
            self.close()  # Fechar a janela de login
        else:
            QMessageBox.critical(self, "Erro de login", "Login falhou. Verifique suas credenciais.")

    def check_login(self, username, password):
        try:
            with open('login.json', 'r') as file:
                data = json.load(file)
                if username in data and data[username] == password:
                    return True
                else:
                    return False
        except Exception as e:
            print(f"Erro ao fazer login: {str(e)}")
            return False


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Conectar o botão "..." ao diálogo de seleção de arquivo
        self.ui.toolButton.clicked.connect(self.attach_spreadsheet)

        # Inicializar a tabela vazia
        self.model = QtGui.QStandardItemModel()
        self.ui.tableView.setModel(self.model)

    def attach_spreadsheet(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Anexar Planilha", "", "Arquivos Excel (*.xlsx);;Todos os arquivos (*)", options=options)
        
        if file_path:
            self.ui.lineEdit_2.setText(file_path)  # Exibir o caminho do arquivo na caixa de texto
            self.load_spreadsheet(file_path)

    def load_spreadsheet(self, file_path):
        try:
            df = pd.read_excel(file_path)  # Ler a planilha Excel
            self.update_table_model(df)
        except Exception as e:
            print(f"Erro ao carregar a planilha: {str(e)}")

    def update_table_model(self, df):
        self.model = QtGui.QStandardItemModel()
        self.model.setColumnCount(len(df.columns))
        self.model.setRowCount(len(df.index))
        
        for row in range(len(df.index)):
            for col in range(len(df.columns)):
                item = QtGui.QStandardItem(str(df.iloc[row, col]))
                self.model.setItem(row, col, item)
        
        self.ui.tableView.setModel(self.model)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # Código para a interface gráfica da janela principal
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(407, 509)
        MainWindow.setFixedSize(407, 509)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(110, 20, 191, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(130, 60, 151, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(130, 110, 151, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(110, 150, 191, 135))
        self.textEdit.setObjectName("textEdit")
        
        # Adicionar o botão "..." ao lado do campo de entrada de anexo de planilha
        self.toolButton = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton.setGeometry(QtCore.QRect(290, 110, 25, 19))
        self.toolButton.setObjectName("toolButton")
        self.toolButton.setText("...")  # Definir o texto como "..."
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(90, 350, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(170, 350, 75, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(250, 350, 75, 23))
        self.pushButton_4.setObjectName("pushButton_4")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(90, 310, 113, 20))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_4.setGeometry(QtCore.QRect(210, 310, 113, 20))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(90, 390, 101, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        
         # Adicionar o QTableView
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(90, 420, 300, 150))  # Ajuste o tamanho e a posição conforme necessário
        self.tableView.setObjectName("tableView")
        
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(200, 390, 121, 61))
        self.listWidget.setObjectName("listWidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 407, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Configurações de Envio"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "Limite de envios"))
        self.lineEdit_2.setPlaceholderText(_translate("MainWindow", "Anexar planilha"))
        self.textEdit.setPlaceholderText(_translate("MainWindow", "Adicione o texto"))
        self.pushButton_3.setText(_translate("MainWindow", "Disparar"))
        self.pushButton_4.setText(_translate("MainWindow", "Desconectar"))
        self.lineEdit_3.setPlaceholderText(_translate("MainWindow", "Porta mínima"))
        self.lineEdit_4.setPlaceholderText(_translate("MainWindow", "Porta máxima"))

class Ui_LoginDialog(object):
    def setupUi(self, Dialog):
        # Código para a interface gráfica da janela de login
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        Dialog.setFixedSize(400, 300)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(160, 180, 75, 23))
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton.setObjectName("pushButton")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(100, 130, 201, 20))
        self.lineEdit.setText("")
        self.lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(100, 70, 201, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(130, 30, 141, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label.setStyleSheet("font: 75 8pt \"MS Shell Dlg 2\";\n"
                                  "font: 12pt \"MS Shell Dlg 2\";")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "ENTRAR"))
        self.lineEdit.setPlaceholderText(_translate("Dialog", "Senha"))
        self.lineEdit_2.setPlaceholderText(_translate("Dialog", "Usuário"))
        self.label.setText(_translate("Dialog", "LOGIN"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    logged_in = False  # Variável global para controlar o login

    login_window = LoginWindow()
    login_window.show()

    app.exec_()  # Executar o aplicativo PyQt

    if logged_in:
        main_window = MainWindow()
        main_window.show()

    sys.exit(app.exec_())
