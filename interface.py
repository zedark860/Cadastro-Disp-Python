import sys
import json
import subprocess
import webbrowser
import psutil
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QMessageBox, QDesktopWidget, QSlider
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QIcon

# Variável global para armazenar o estado de login
logged_in = False

# Defina a variável configuracoes no escopo global
configuracoes = {
    "limiteQuantidade": "",
    "mensagem_principal": "",
    "planilha_lead": "",
    "portas_abertas": [],  # Lista para armazenar as portas abertas
    "num_celulares": 1  # Número de celulares padrão
}

# Verifique se o arquivo JSON existe e carregue as configurações, se existir
try:
    with open('configinterface.json', 'r') as arquivo_json:
        configuracoes = json.load(arquivo_json)
except FileNotFoundError:
    # Crie um arquivo JSON vazio se ele não existir
    with open('configinterface.json', 'w') as arquivo_json:
        json.dump(configuracoes, arquivo_json)

estiloLogin = """
QWidget{
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #22B3E2, stop: 1 #022859);
}
QLabel{
    color: white;
    background: transparent;
    font-weight: 600;
    font-size: 15px;
}
QLineEdit {
    border-radius: 8px;
    border: 1px solid #e0e4e7;
    padding: 5px 15px;
    background: white;
}
QPushButton {
    background-color: #343434;
    color: #fff;
    font-weight: 600;
    border-radius: 8px;
    padding: 10px 20px;
    margin-top: 10px;
    outline: 0px;
    font-size: 12px;
}
QPushButton:hover,
QPushButton:focus {
    background-color: #0b5ed7;
    border: 3px solid #9ac3fe;
}
QSlider {
    border-radius: 5px;
    background: white;
    height: 20px;
    margin-top: 10px;
}
"""

estiloMain = """
QWidget{
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #22B3E2, stop: 1 #022859);
}
QLabel{
    color: white;
    background: transparent;
    font-weight: 600;
    font-size: 15px;
}
QLineEdit {
    border-radius: 8px;
    border: 1px solid #e0e4e7;
    padding: 5px 15px;
    background: white;
}
QPushButton {
    background-color: #343434;
    color: #fff;
    font-weight: 600;
    border-radius: 8px;
    padding: 10px 20px;
    margin-top: 10px;
    outline: 0px;
    font-size: 12px;
}
QPushButton:hover,
QPushButton:focus {
    background-color: #0b5ed7;
    border: 3px solid #9ac3fe;
}
QTextEdit{
    background-color: white;
    padding: 5px 15px;
    border-radius: 8px;
}
QSlider {
    border-radius: 5px;
    background: white;
    height: 20px;
    margin-top: 10px;
}
"""

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.logged_in = False  # Use uma variável de instância para controlar o login
        self.setWindowTitle("Login")
        self.setFixedSize(400, 240)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
        self.setStyleSheet(estiloLogin)
        self.setWindowIcon(QIcon('logosemfundo.png'))

        self.center_window()

        self.username_label = QLabel("Nome de Usuário:")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Ex: web123')
        self.password_label = QLabel("Senha:")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Ex: 123web')
        self.password_input.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton("Entrar")
        self.login_button.clicked.connect(self.login)

        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def center_window(self):
        # Obtém a geometria da tela principal
        screen = QDesktopWidget().screenGeometry()

        # Obtém a geometria da própria janela
        window = self.geometry()

        # Calcula a posição x e y para centralizar a janela
        x = (screen.width() - window.width()) // 2
        y = (screen.height() - window.height()) // 2

        # Define a posição da janela para centralizá-la
        self.move(x, y)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if self.check_login(username, password):
            self.logged_in = True
            self.close()
        else:
            QMessageBox.critical(self, "Erro de login",
                                 "Login falhou. Verifique suas credenciais.")

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

class ConsoleLogger(QThread):
    log_update = pyqtSignal(str)

    def run(self):
        process = subprocess.Popen(
            "python disp.py", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in process.stdout:
            self.log_update.emit(line)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Disparador via WhatsApp")
        self.setFixedSize(400, 650)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
        self.setStyleSheet(estiloMain)
        self.setWindowIcon(QIcon('logosemfundo.png'))

        self.center_window()

        with open('configinterface.json', 'r') as arquivo_json:
            configuracoes = json.load(arquivo_json)

        # Defina os valores iniciais nos campos
        self.limiteQuantidade_label = QLabel("Limite de Quantidade:")
        self.limiteQuantidade_input = QLineEdit()
        self.limiteQuantidade_input.setPlaceholderText('Ex: 50')
        self.limiteQuantidade_input.setText(configuracoes.get("limiteQuantidade", ""))

        self.planilha_lead_label = QLabel("Selecione um arquivo Excel:")
        self.planilha_lead_input = QLineEdit()
        self.planilha_lead_input.setReadOnly(True)
        self.planilha_lead_button = QPushButton("Procurar")
        self.planilha_lead_button.clicked.connect(self.browse_excel)
        self.planilha_lead_input.setText(configuracoes.get("planilha_lead", ""))
        self.abrir_google_button = QPushButton("Modelo Planilha")
        self.abrir_google_button.clicked.connect(self.abrir_google)

        self.mensagem_principal_label = QLabel("Mensagem Principal:")
        self.mensagem_principal_input = QTextEdit()
        self.mensagem_principal_input.setFixedSize(380, 100)
        self.mensagem_principal_input.setText(configuracoes.get("mensagem_principal", ""))

        self.num_celulares_label = QLabel("Número de Celulares:")
        self.num_celulares_input = QLineEdit()
        self.num_celulares_input.setPlaceholderText('Ex: 2')
        self.num_celulares_input.setText(str(len(configuracoes.get("portas_abertas", []))))

        self.num_celulares_slider = QSlider(Qt.Horizontal)
        self.num_celulares_slider.setMinimum(1)
        self.num_celulares_slider.setMaximum(5)
        self.num_celulares_slider.setValue(int(self.num_celulares_input.text()))
        self.num_celulares_slider.valueChanged.connect(self.slider_changed)

        self.num_celulares_value_label = QLabel()
        self.num_celulares_value_label.setText(str(self.num_celulares_slider.value()))

        self.abrir_qr_button = QPushButton("Abrir QRCode")
        self.abrir_qr_button.setIcon(QIcon('qrcode.png'))
        self.abrir_qr_button.clicked.connect(self.abrir_localhosts)
        self.disparar_button = QPushButton("Disparar")
        self.disparar_button.setIcon(QIcon('disparar.png'))
        self.disparar_button.clicked.connect(self.iniciar_disparador)
        self.desconectar_button = QPushButton("Desconectar")
        self.desconectar_button.setIcon(QIcon('desconectar.png'))
        self.desconectar_button.clicked.connect(self.encerrar_node_disparador)

        self.disparar_button.setStyleSheet('background: green;')
        self.desconectar_button.setStyleSheet('background: red;')

        labels = [self.limiteQuantidade_label, self.planilha_lead_label, self.mensagem_principal_label, self.num_celulares_label]
        for label in labels:
            label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.limiteQuantidade_label)
        layout.addWidget(self.limiteQuantidade_input)
        layout.addWidget(self.planilha_lead_label)
        layout.addWidget(self.planilha_lead_input)
        layout.addWidget(self.planilha_lead_button)
        layout.addWidget(self.abrir_google_button)
        layout.addWidget(self.mensagem_principal_label)
        layout.addWidget(self.mensagem_principal_input)
        layout.addWidget(self.num_celulares_label)
        layout.addWidget(self.num_celulares_slider)
        layout.addWidget(self.num_celulares_value_label)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.abrir_qr_button)
        button_layout.addWidget(self.disparar_button)
        button_layout.addWidget(self.desconectar_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

        self.limiteQuantidade_input.textChanged.connect(self.atualizar_configuracoes)
        self.mensagem_principal_input.textChanged.connect(self.atualizar_configuracoes)
        self.planilha_lead_input.textChanged.connect(self.atualizar_configuracoes)
        self.num_celulares_input.textChanged.connect(self.atualizar_num_celulares)

    def abrir_google(self):
        webbrowser.open("https://onedrive.live.com/download?resid=E8701D9025964978%21771316&authkey=!AJAjIJQOwJEovMQ&em=2")

    def center_window(self):
        # Obtém a geometria da tela principal
        screen = QDesktopWidget().screenGeometry()

        # Obtém a geometria da própria janela
        window = self.geometry()

        # Calcula a posição x e y para centralizar a janela
        x = (screen.width() - window.width()) // 2
        y = (screen.height() - window.height()) // 2

        # Define a posição da janela para centralizá-la
        self.move(x, y)

    def atualizar_configuracoes(self):
        configuracoes["limiteQuantidade"] = self.limiteQuantidade_input.text()
        configuracoes["mensagem_principal"] = self.mensagem_principal_input.toPlainText()
        configuracoes["planilha_lead"] = self.planilha_lead_input.text()

        with open('configinterface.json', 'w') as arquivo_json:
            json.dump(configuracoes, arquivo_json)

    def atualizar_num_celulares(self):
        num_celulares = int(self.num_celulares_input.text())
        portas_abertas = list(range(8000, 8000 + num_celulares))
        configuracoes["portas_abertas"] = portas_abertas
        self.atualizar_configuracoes()

    def slider_changed(self):
        value = self.num_celulares_slider.value()
        self.num_celulares_input.setText(str(value))
        self.num_celulares_value_label.setText(str(value))
        self.atualizar_num_celulares()

    def iniciar_disparador(self):
        comando_disparador = "python disp.py"
        subprocess.Popen(comando_disparador, shell=True)

    def abrir_localhosts(self):
        num_celulares = self.num_celulares_slider.value()
        portas_abertas = [8000 + i for i in range(num_celulares)]

        try:
            for porta in portas_abertas:
                comando_node = f"node disparador{porta}"
                subprocess.Popen(comando_node, shell=True)

                url = f"http://localhost:{porta}"
                webbrowser.open(url)

        except Exception as e:
            QMessageBox.critical(
                self, "Erro ao abrir URL", f"Ocorreu um erro ao abrir a URL: {str(e)}")

    def browse_excel(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Selecione um arquivo Excel", "", "Arquivos Excel (*.xlsx)", options=options)
        if file_path:
            self.planilha_lead_input.setText(file_path)

    def encerrar_node_disparador(self):
        for process in psutil.process_iter(attrs=['pid', 'name']):
            if 'node' in process.info['name']:
                try:
                    psutil.Process(process.info['pid']).terminate()
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
        # Feche a janela principal após encerrar os processos
        self.close()

    def closeEvent(self, event):
        self.encerrar_node_disparador()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    login_window = LoginWindow()
    login_window.show()

    app.exec_()

    if login_window.logged_in:
        main_window = MainWindow()
        main_window.show()

    sys.exit(app.exec_())