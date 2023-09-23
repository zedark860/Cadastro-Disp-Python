import tkinter as tk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
import customtkinter

def selecionar_arquivo():
    arquivo = filedialog.askopenfilename()
    if arquivo:
        print('Arquivo selecionado:', arquivo)

janela = customtkinter.CTk()
janela.geometry('1000x500')

selecioneArquivo = customtkinter.CTkLabel(janela, text='Selecione sua planilha(xlsx)')
selecioneArquivo.pack(padx=10, pady=10)

botao_selecionar = customtkinter.CTkButton(janela, text='Selecionar Arquivo', command=selecionar_arquivo)
botao_selecionar.pack(pady=10)

quantidadeTexto = customtkinter.CTkLabel(janela, text='Digite a quantidade de disparos')
quantidadeTexto.pack(pady=10)

quantidadeDisparo = customtkinter.CTkEntry(janela, placeholder_text='Ex: 200')
quantidadeDisparo.pack(padx=10, pady=10)

textoEnvio = customtkinter.CTkLabel(janela, text='Digite seu texto para envio')
textoEnvio.pack(pady=10)

# Usando ScrolledText com tamanho menor
textoEnviar = ScrolledText(janela, wrap=tk.WORD, height=5, width=40)
textoEnviar.pack(pady=10, padx=10)

janela.mainloop()