import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import customtkinter

planilha_carregada = False
iniciar_portas_clicado = False
campos_preenchidos = False

def selecionar_arquivo():
    global planilha_carregada
    arquivo = filedialog.askopenfilename()
    if arquivo:
        print('Arquivo selecionado:', arquivo)
        planilha_carregada = True
        verificar_habilitar_iniciar_disparo()

def carregar_planilha():
    global planilha_carregada
    if planilha_carregada:
        messagebox.showinfo("Alerta", "Planilha carregada com sucesso!")
    else:
        messagebox.showwarning("Alerta", "Selecione uma planilha antes de carregar!")

def iniciar_disparo():
    if campos_preenchidos:
        messagebox.showinfo("Alerta", "Iniciando disparo!")
    else:
        messagebox.showwarning("Alerta", "Preencha todos os campos antes de iniciar o disparo!")

def encerrar_disparo():
    if messagebox.askokcancel("Confirmação", "Tem certeza de que deseja encerrar os disparos?"):
        pass

def iniciar_portas():
    global iniciar_portas_clicado
    iniciar_portas_clicado = True
    verificar_habilitar_iniciar_disparo()

def verificar_habilitar_iniciar_disparo():
    global campos_preenchidos
    if planilha_carregada and iniciar_portas_clicado and quantidadeDisparo.get() and textoEnviar.get("1.0", tk.END).strip() and selecaoPortas.get():
        campos_preenchidos = True
        iniciarDisparo['state'] = 'normal'
    else:
        campos_preenchidos = False
        iniciarDisparo['state'] = 'disabled'

janela = customtkinter.CTk()
janela.geometry('1000x400')
janela.resizable(width=False, height=False)
janela.title('Disparador Web Sender')
janela._set_appearance_mode('system')

selecioneArquivo = customtkinter.CTkLabel(janela, text='Selecione sua planilha(xlsx)')
selecioneArquivo.grid(row=0, column=0, padx=10, pady=10)

botao_selecionar = customtkinter.CTkButton(janela, text='Selecionar Arquivo', command=selecionar_arquivo, fg_color='green', hover_color='#65b307', corner_radius=20)
botao_selecionar.grid(row=0, column=1, padx=(5, 5), pady=10)

botao_carregar_planilha = customtkinter.CTkButton(janela, text='Carregar Planilha', command=carregar_planilha, fg_color='green', hover_color='#65b307', corner_radius=20)
botao_carregar_planilha.grid(row=0, column=2, padx=(5, 5), pady=10)

quantidadeTexto = customtkinter.CTkLabel(janela, text='Digite a quantidade de disparos')
quantidadeTexto.grid(row=1, column=0, pady=10)

quantidadeDisparo = customtkinter.CTkEntry(janela, placeholder_text='Ex: 200', corner_radius=20)
quantidadeDisparo.grid(row=1, column=1, padx=10, pady=10)

textoEnvio = customtkinter.CTkLabel(janela, text='Digite seu texto para envio')
textoEnvio.grid(row=2, column=0, pady=10)

textoEnviar_frame = customtkinter.CTkFrame(janela)
textoEnviar_frame.grid(row=2, column=1, pady=10, padx=10)

textoEnviar = ScrolledText(textoEnviar_frame, wrap=tk.WORD, height=5, width=40)
textoEnviar.pack(fill="both", expand=True)

numerosPortas = customtkinter.CTkLabel(janela, text='Digite o número de portas')
numerosPortas.grid(row=3, column=0, padx=10, pady=10)

selecaoPortas = customtkinter.CTkEntry(janela, placeholder_text='Ex: 5001, 5002, 5003', corner_radius=20, width=200)
selecaoPortas.grid(row=3, column=1, padx=10, pady=10)

iniciarPortas = customtkinter.CTkButton(janela, text='Iniciar Portas', fg_color='green', hover_color='#65b307', corner_radius=20, command=iniciar_portas)
iniciarPortas.grid(row=3, column=2, padx=10)

iniciarDisparo = customtkinter.CTkButton(janela, text='Iniciar Disparo', fg_color='green', hover_color='#65b307', corner_radius=20, state='disabled', command=iniciar_disparo)
iniciarDisparo.grid(row=4, column=0, padx=10, pady=100)

encerrarDisparo = customtkinter.CTkButton(janela, text='Encerrar Disparo', fg_color='red', hover_color='#90120b', corner_radius=20, command=encerrar_disparo)
encerrarDisparo.grid(row=4, column=1, padx=10, pady=100)

janela.mainloop()
