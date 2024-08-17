import pyautogui
import keyboard
import threading
import time
import tkinter as tk
from tkinter import messagebox, ttk
import pygetwindow as gw

# Variáveis globais
keys_to_send = [None, None, None]  # Lista para armazenar as teclas
delays = [0.1, 0.1, 0.1]  # Lista para armazenar os delays
running = False
send_thread = None
selected_window = None

# Inicializando listas para os campos de entrada
entry_keys = []
entry_delays = []

def send_key():
    """Função que envia as teclas repetidamente enquanto o programa estiver ativo."""
    while running:
        if selected_window:
            selected_window.activate()  # Ativa a janela selecionada
            for i in range(3):
                if keys_to_send[i]:
                    pyautogui.press(keys_to_send[i])
                    time.sleep(delays[i])  # Usa o delay configurado para cada tecla
            time.sleep(0.1)  # Intervalo entre ciclos de envio

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

def set_keys_and_delays():
    """Configura as teclas e delays a serem enviados."""
    global keys_to_send, delays
    for i in range(3):
        keys_to_send[i] = entry_keys[i].get()
        try:
            delays[i] = float(entry_delays[i].get())
            if delays[i] < 0:
                raise ValueError("Delay não pode ser negativo.")
        except ValueError:
            messagebox.showwarning("Erro", f"Por favor, insira um valor válido para o delay da tecla {i+1}.")
            return
    
    print(f"Teclas configuradas: {keys_to_send}, Delays: {delays}")
    messagebox.showinfo("Configuração de Teclas", f"Teclas configuradas: {keys_to_send}\nDelays: {delays}")

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
                                    "1. Insira até 3 teclas que deseja enviar nos campos abaixo.\n"
                                    "2. Configure um delay para cada tecla.\n"
                                    "3. Selecione a janela desejada no dropdown.\n"
                                    "4. Pressione 'Home' para ativar/desativar o envio de teclas.\n"
                                    "5. As teclas serão enviadas repetidamente enquanto o programa estiver ativado.",
                       padx=10, pady=10)
description.pack()

# Labels e campos de entrada para as teclas e delays
for i in range(3):
    frame = tk.Frame(root)
    frame.pack(pady=5)

    tk.Label(frame, text=f"Tecla {i + 1}:").pack(side=tk.LEFT)
    entry_key = tk.Entry(frame, width=5)
    entry_key.pack(side=tk.LEFT, padx=5)
    entry_keys.append(entry_key)

    tk.Label(frame, text=f"Delay {i + 1} (segundos):").pack(side=tk.LEFT)
    entry_delay = tk.Entry(frame, width=5)
    entry_delay.pack(side=tk.LEFT, padx=5)
    entry_delays.append(entry_delay)

# Dropdown para selecionar a janela
window_label = tk.Label(root, text="Selecione a Janela:")
window_label.pack(pady=5)

window_dropdown = ttk.Combobox(root)
window_dropdown.pack(pady=5)
update_window_list()  # Atualiza a lista de janelas ao iniciar
window_dropdown.bind("<<ComboboxSelected>>", select_window)  # Atualiza a janela selecionada

# Botão para configurar as teclas e delays
set_keys_button = tk.Button(root, text="Configurar Teclas e Delays", command=set_keys_and_delays)
set_keys_button.pack(pady=5)

# Botão para ativar/desativar o programa
start_button = tk.Button(root, text="Ativar", command=toggle_program)
start_button.pack(pady=5)

# Adicionando a marca d'água
watermark = tk.Label(root, text="codexmark - 2024 todos os direitos reservados", 
                      fg="gray", font=("Arial", 8))
watermark.pack(side=tk.BOTTOM, pady=10)

# Iniciando a interface
root.mainloop()