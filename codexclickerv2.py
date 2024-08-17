import pyautogui
import keyboard
import threading
import time

# Variáveis globais
key_to_send = None
running = False

def send_key():
    while running:
        if key_to_send:
            pyautogui.press(key_to_send)
            time.sleep(0.1)  # Ajuste o intervalo conforme necessário

def toggle_program():
    global running
    running = not running
    if running:
        print("Programa ativado. Enviando teclas...")
        threading.Thread(target=send_key).start()
    else:
        print("Programa desativado.")

def set_key(key):
    global key_to_send
    key_to_send = key
    print(f"Tecla configurada para: {key}")

# Configurando hotkey para ativar/desativar o programa
keyboard.add_hotkey('ctrl+shift+s', toggle_program)

# Exemplo de configuração da tecla a ser enviada
set_key('x')  # Substitua 'a' pela tecla desejada

print("Pressione Ctrl+Shift+S para ativar/desativar o envio de teclas.")
keyboard.wait('esc')  # O programa continuará até que a tecla 'esc' seja pressionada