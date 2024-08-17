import pyautogui
import keyboard
import threading
import time
import tkinter as tk
from tkinter import messagebox, ttk
import pygetwindow as gw

# Variáveis globais
key_to_send = None
running = False
send_thread = None
selected_window = None

def send_key():
    """Função que envia a tecla repetidamente enquanto o programa estiver ativo."""
    while running:
        if key_to_send and selected_window:
            # Ativa a janela selecionada
            selected_window.activate()
            pyautogui.press(key_to_send)
            time.sleep(0.1)  # Ajuste o intervalo conforme necessário

def toggle_program():
    """Ativa ou desativa o envio de teclas."""
    global running, send_thread
    running = not running
    if running:
        start_button.config(text="Desativar")
        print("Programa ativado. Enviando teclas...")
        send_thread = threading.Thread(target=send_key)
        send_thread.daemon = True  # Permite que a thread feche quando a janela principal fechar
        send_thread.start()
    else:
        start_button.config(text="Ativar")
        print("Programa desativado.")

def set_key():
    """Configura a tecla a ser enviada."""
    global key_to_send
    key_to_send = entry_key.get()
    if key_to_send:
        print(f"Tecla configurada para: {key_to_send}")
        messagebox.showinfo("Configuração de Tecla", f"Tecla configurada para: {key_to_send}")
    else:
        messagebox.showwarning("Erro", "Por favor, insira uma tecla válida.")

def on_home_key():
    """Função chamada quando a tecla 'Home' é pressionada."""
    toggle_program()

def update_window_list():
    """Atualiza a lista de janelas disponíveis no dropdown."""
    windows = gw.getAllTitles()
    window_dropdown['values'] = windows
    if windows:
        window_dropdown.current(0)  # Seleciona a primeira janela por padrão
        select_window(None)  # Atualiza a janela selecionada

def select_window(event):
    """Atualiza a janela selecionada quando o dropdown é alterado."""
    global selected_window
    selected_window = gw.getWindowsWithTitle(window_dropdown.get())[0]

# Configurando hotkey para ativar/desativar o programa
keyboard.add_hotkey('home', on_home_key)

# Criando a interface gráfica
root = tk.Tk()
root.title("Anarchy Autokey")

# Descrição das funcionalidades
description = tk.Label(root, text="Anarchy Autokey\n\n"
                                    "1. Insira a tecla que deseja enviar no campo abaixo.\n"
                                    "2. Selecione a janela desejada no dropdown.\n"
                                    "3. Pressione 'Home' para ativar/desativar o envio de teclas.\n"
                                    "4. A tecla será enviada repetidamente enquanto o programa estiver ativado.",
                       padx=10, pady=10)
description.pack()

# Campo de entrada para a tecla
entry_key = tk.Entry(root, width=10)
entry_key.pack(pady=5)

# Dropdown para selecionar a janela
window_label = tk.Label(root, text="Selecione a Janela:")
window_label.pack(pady=5)

window_dropdown = ttk.Combobox(root)
window_dropdown.pack(pady=5)
update_window_list()  # Atualiza a lista de janelas ao iniciar
window_dropdown.bind("<<ComboboxSelected>>", select_window)  # Atualiza a janela selecionada

# Botão para configurar a tecla
set_key_button = tk.Button(root, text="Configurar Tecla", command=set_key)
set_key_button.pack(pady=5)

# Botão para ativar/desativar o programa
start_button = tk.Button(root, text="Ativar", command=toggle_program)
start_button.pack(pady=5)

# Iniciando a interface
root.mainloop()