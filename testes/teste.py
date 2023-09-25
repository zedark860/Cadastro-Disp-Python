import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import json
import subprocess
import webbrowser
import time
import psutil
import pandas as pd
import customtkinter

# Variável para armazenar o caminho do arquivo Excel
caminho_arquivo = ""

# Defina a variável configuracoes no escopo global
configuracoes = {
    "limiteQuantidade": "",
    "mensagem_principal": "",
    "caminho_arquivo": caminho_arquivo
}

# Função para iniciar o terminal do VS Code
def iniciar_vscode_terminal(janela_raiz):
    # Comando para abrir o terminal do VS Code (substitua pelo caminho do seu código)
    comando = "code"

    # Abra o processo do VS Code e redirecione a saída
    processo = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    # Crie uma janela tkinter para exibir a saída do terminal do VS Code
    janela_terminal = tk.Toplevel(janela_raiz)
    janela_terminal.title("Terminal do VS Code")

    # Crie uma área de texto para exibir a saída
    texto_terminal = scrolledtext.ScrolledText(janela_terminal, wrap=tk.WORD)
    texto_terminal.pack(fill=tk.BOTH, expand=True)

    # Função para atualizar a saída do terminal na área de texto
    def atualizar_saida_terminal():
        while True:
            linha = processo.stdout.readline().decode("utf-8")
            if not linha:
                break
            texto_terminal.insert(tk.END, linha)
            texto_terminal.see(tk.END)
    
    # Inicie uma thread para ler e exibir a saída do terminal em tempo real
    import threading
    thread_saida_terminal = threading.Thread(target=atualizar_saida_terminal)
    thread_saida_terminal.start()

# Função para ler planilha do Excel
def ler_planilha_excel():
    global configuracoes  # Acesso à variável configuracoes global
    try:
        caminho_arquivo = configuracoes.get("caminho_arquivo")

        if caminho_arquivo:
            contatos = pd.read_excel(caminho_arquivo, engine="openpyxl")
            return contatos
        else:
            raise Exception("Caminho do arquivo não encontrado nas configurações.")
    except Exception as e:
        raise Exception(f"Erro ao ler planilha: {str(e)}")

# Função para salvar as informações em um arquivo JSON
def salvar_configuracoes_json(config):
    with open("config.json", "w") as json_file:
        json.dump(config, json_file)

# Função para iniciar o disparador oficial como um processo separado
def iniciar_disparador():
    # Substitua o comando abaixo pelo comando correto para iniciar o disparador
    comando_disparador = "python disp.py"
    subprocess.Popen(comando_disparador, shell=True)

# Função para iniciar o servidor Node.js como um processo separado
def iniciar_node_disparador():
    comando_node = "node disparador.js"
    subprocess.Popen(comando_node, shell=True)

# Função para encerrar o processo do Node.js
def encerrar_node_disparador():
    for process in psutil.process_iter(attrs=['pid', 'name']):
        if 'node' in process.info['name']:
            try:
                psutil.Process(process.info['pid']).terminate()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

def abrir_localhost():
    webbrowser.open("http://localhost:8000")

# Função para carregar a planilha
def carregar_planilha():
    global caminho_arquivo
    caminho_arquivo = filedialog.askopenfilename(filetypes=[("Arquivos Excel", "*.xlsx")])
    if caminho_arquivo:
        contatos = ler_planilha_excel()
        if contatos is not None:
            messagebox.showinfo("Sucesso", "Planilha carregada com sucesso!")
            # Exibir configurações atuais na interface
            config_atual = f"Limite de Quantidade: {configuracoes['limiteQuantidade']}\nMensagem Principal:\n{configuracoes['mensagem_principal']}"
            if 'configuracoes_atuais' in globals():
                configuracoes_atuais.config(text=config_atual)
        else:
            messagebox.showerror("Erro", "Erro ao carregar a planilha. Verifique se é um arquivo Excel válido.")
    else:
        messagebox.showerror("Erro", "Selecione um arquivo Excel válido.")

# Função para disparar
def disparar():
    global caminho_arquivo
    # Obtenha os valores inseridos na interface
    limiteQuantidade = configuracoes["limiteQuantidade"]
    mensagemPrincipal = configuracoes["mensagem_principal"]

    # Crie um dicionário com as informações
    configuracoes = {
        "limiteQuantidade": limiteQuantidade,
        "mensagem_principal": mensagemPrincipal,
        "caminho_arquivo": caminho_arquivo
    }

    # Salve as informações em um arquivo JSON
    salvar_configuracoes_json(configuracoes)

    # Inicie o disparador oficial como um processo separado
    iniciar_disparador()

# Função para mostrar um pop-up de sucesso
def mostrar_sucesso_popup():
    messagebox.showinfo("Sucesso", "Envios finalizados com sucesso!")

# Função para verificar as credenciais de login
def verificar_credenciais():
    login = login_entry.get()
    senha = senha_entry.get()

    # Verifique as credenciais (substitua por sua lógica de autenticação)
    if login == "123" and senha == "123":
        login_window.destroy()  # Feche a janela de login
        mostrar_tela_principal()
    else:
        messagebox.showerror("Erro de Login", "Credenciais inválidas.")

# Função para mostrar a tela principal
def mostrar_tela_principal():
    # Crie a janela principal
    root =customtkinter.CTk()
    root.title("Envio de Mensagens via WhatsApp")
    root.geometry('1000x400')
    root.resizable(width=False, height=False)
    root._set_appearance_mode('system')

    # Crie os widgets da interface
    titulo = customtkinter.CTkLabel(root, text="Configurações de Envio de Mensagens", font=("Montserrat", 14))
    titulo.pack()

    frame = customtkinter.CTkFrame(root)
    frame.pack()

    label_limite_quantidade = customtkinter.CTkLabel(frame, text="Limite de Quantidade:")
    label_limite_quantidade.grid(row=0, column=0)

    limite_quantidade = customtkinter.CTkEntry(frame)
    limite_quantidade.grid(row=0, column=1)

    label_arquivo_excel = customtkinter.CTkLabel(frame, text="Selecione um arquivo Excel:")
    label_arquivo_excel.grid(row=1, column=0)

    arquivo_excel = customtkinter.CTkEntry(frame, state="disabled")
    arquivo_excel.grid(row=1, column=1)

    procurar_arquivo = customtkinter.CTkButton(frame, text="Procurar", command=carregar_planilha)
    procurar_arquivo.grid(row=1, column=2)

    carregar_planilha_button = customtkinter.CTkButton(frame, text="Carregar Planilha", command=carregar_planilha)
    carregar_planilha_button.grid(row=2, column=0, columnspan=3)

    label_mensagem_principal = customtkinter.CTkLabel(frame, text="Mensagem Principal:")
    label_mensagem_principal.grid(row=3, column=0)

    mensagem_principal = scrolledtext.ScrolledText(frame, width=40, height=5)
    mensagem_principal.grid(row=3, column=1, columnspan=2)

    global configuracoes_atuais  # Defina configuracoes_atuais como uma variável global
    configuracoes_atuais = customtkinter.CTkLabel(root, text="Configurações Atuais:")
    configuracoes_atuais.pack()

    frame_botoes = customtkinter.CTkFrame(root)
    frame_botoes.pack()

    abrir_qrcode_button = customtkinter.CTkButton(frame_botoes, text="Abrir QRCode", command=iniciar_node_disparador)
    abrir_qrcode_button.pack(side="left")

    disparar_button = customtkinter.CTkButton(frame_botoes, text="Disparar", command=disparar)
    disparar_button.pack(side="left")

    desconectar_button = customtkinter.CTkButton(frame_botoes, text="Desconectar", command=root.quit)
    desconectar_button.pack(side="left")

    # Loop principal da interface
    root.mainloop()

    # Encerrar o processo do Node.js antes de sair
    encerrar_node_disparador()

# Crie a janela de login
login_window = customtkinter.CTk()
login_window.title("Login")
login_window._set_appearance_mode('system')
login_window.resizable(width=False, height=False)
login_window.geometry('400x250')

# Estilo para widgets de login
estilo_login = ttk.Style()
estilo_login.configure("TLabel", font=("Helvetica", 12))
estilo_login.configure("TEntry", font=("Helvetica", 12))
estilo_login.configure("TButton", font=("Helvetica", 12))

login_label = customtkinter.CTkLabel(login_window, text="Login:")
login_label.grid(column=0, row=0, padx=10, pady=5, sticky="e")

login_entry = customtkinter.CTkEntry(login_window)
login_entry.grid(column=1, row=0, padx=10, pady=5)

senha_label = customtkinter.CTkLabel(login_window, text="Senha:")
senha_label.grid(column=0, row=1, padx=10, pady=5, sticky="e")

senha_entry = customtkinter.CTkEntry(login_window, show="*")
senha_entry.grid(column=1, row=1, padx=10, pady=5)

login_button = customtkinter.CTkButton(login_window, text="Login", command=verificar_credenciais)
login_button.grid(column=1, row=2, padx=10, pady=5)

# Loop da janela de login
login_window.mainloop()