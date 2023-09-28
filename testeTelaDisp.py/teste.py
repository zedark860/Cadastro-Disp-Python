import sys
import json
import subprocess
import webbrowser
import psutil
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QVBoxLayout, QFileDialog, QMessageBox

# Variável para armazenar o caminho do arquivo Excel
caminho_arquivo = ""
porta_min = ""
porta_max = ""

# Defina a variável configuracoes no escopo global
configuracoes = {
    "limiteQuantidade": "",
    "mensagem_principal": "",
    "arquivo_excel": "",  # Corrigido: adicionado "arquivo_excel" aqui
    "porta_min": porta_min,
    "porta_max": porta_max,
}

disparo_iniciado = False

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 200, 140)

        self.username_label = QLabel("Nome de Usuário:")
        self.username_input = QLineEdit()
        self.password_label = QLabel("Senha:")
        self.password_input = QLineEdit()
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

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if self.check_login(username, password):
            global logged_in
            logged_in = True  
            self.close() 
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


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Envio de Mensagens via WhatsApp")
        self.setGeometry(100, 100, 400, 350)

        self.limiteQuantidade_label = QLabel("Limite de Quantidade:")
        self.limiteQuantidade_input = QLineEdit()
        self.arquivo_excel_label = QLabel("Selecione um arquivo Excel:")
        self.arquivo_excel_input = QLineEdit()
        self.arquivo_excel_button = QPushButton("Procurar")
        self.arquivo_excel_button.clicked.connect(self.browse_excel)
        self.mensagem_principal_label = QLabel("Mensagem Principal:")
        self.mensagem_principal_input = QTextEdit()
        self.porta_min_label = QLabel("Porta Mínima:")
        self.porta_min_input = QLineEdit()
        self.porta_max_label = QLabel("Porta Máxima:")
        self.porta_max_input = QLineEdit()

        self.abrir_qr_button = QPushButton("Abrir QRCode")
        self.abrir_qr_button.clicked.connect(self.abrir_qr_code)
        self.disparar_button = QPushButton("Disparar")
        self.disparar_button.clicked.connect(self.iniciar_disparador)
        self.desconectar_button = QPushButton("Desconectar")
        self.desconectar_button.clicked.connect(self.encerrar_node_disparador)

        layout = QVBoxLayout()
        layout.addWidget(self.limiteQuantidade_label)
        layout.addWidget(self.limiteQuantidade_input)
        layout.addWidget(self.arquivo_excel_label)
        layout.addWidget(self.arquivo_excel_input)
        layout.addWidget(self.arquivo_excel_button)
        layout.addWidget(self.mensagem_principal_label)
        layout.addWidget(self.mensagem_principal_input)
        layout.addWidget(self.porta_min_label)
        layout.addWidget(self.porta_min_input)
        layout.addWidget(self.porta_max_label)
        layout.addWidget(self.porta_max_input)
        layout.addWidget(self.abrir_qr_button)
        layout.addWidget(self.disparar_button)
        layout.addWidget(self.desconectar_button)

        self.setLayout(layout)

    def browse_excel(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self, "Selecione um arquivo Excel", "", "Arquivos Excel (*.xlsx)", options=options)
        if file_path:
            self.arquivo_excel_input.setText(file_path)

    # Função para iniciar os servidores Node.js como processos separados
    def iniciar_node_disparadores():
        if porta_min == porta_max:
            subprocess.Popen("node disparador.js", shell=True)
        else:
            comandos = ["node disparador.js", "node disparador2.js",
                        "node disparador3.js", "node disparador4.js", "node disparador5.js"]
            for comando in comandos:
                subprocess.Popen(comando, shell=True)

    def abrir_qr_code(self, porta_min=None, porta_max=None):
        if not porta_min and not porta_max:
            for porta in range(8000, 8005):
                url = f"http://localhost:{porta}"
                webbrowser.open(url)
        elif porta_min and porta_max:
            porta_min = int(porta_min)
            porta_max = int(porta_max)
            if 8000 <= porta_min <= 8004 and 8000 <= porta_max <= 8004:
                if porta_min == porta_max:
                    url = f"http://localhost:{porta_min}"
                    webbrowser.open(url)
                else:
                    for porta in range(porta_min, porta_max + 1):
                        url = f"http://localhost:{porta}"
                        webbrowser.open(url)
            else:
                raise ValueError(
                    "Portas devem estar no intervalo de 8000 a 8004.")
        else:
            raise ValueError(
                "Ambos os limites de porta (mínimo e máximo) devem ser especificados.")

    # Função para iniciar o disparador oficial como um processo separado
    def iniciar_disparador():
        # Substitua o comando abaixo pelo comando correto para iniciar o disparador
        comando_disparador = "python disp.py"
        subprocess.Popen(comando_disparador, shell=True)

    def encerrar_node_disparador():
        for process in psutil.process_iter(attrs=['pid', 'name']):
            if 'node' in process.info['name']:
                try:
                    psutil.Process(process.info['pid']).terminate()
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    logged_in = False 

    login_window = LoginWindow()
    login_window.show()

    app.exec_()  # Executar o aplicativo PyQt

    if logged_in:
        main_window = MainWindow()
        main_window.show()

    sys.exit(app.exec_())
