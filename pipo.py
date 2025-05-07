import customtkinter
import threading
import subprocess
import os
import re
import time
from tkinter import filedialog
from PIL import Image
import pygame
import threading

import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")
VERSION = "2.0.0"


def reproducir_sonido_bienvenida():
    pygame.mixer.init()
    pygame.mixer.music.load(resource_path("bienvenida.wav"))
    pygame.mixer.music.play()

def splash_screen():
    splash = customtkinter.CTk()
    splash.title("Bienvenido a PIPO 🎶")
    splash.geometry("450x450")
    splash.resizable(False, False)
    splash.attributes('-alpha', 0.0)  # Empezar invisible

    # Cargar imagen
    image = Image.open(resource_path("logo.png"))
    image = image.resize((250, 250))
    logo = customtkinter.CTkImage(light_image=image, dark_image=image, size=(250, 250))

    label_imagen = customtkinter.CTkLabel(splash, image=logo, text="")
    label_imagen.pack(pady=20)
    label_texto = customtkinter.CTkLabel(splash, text="🎶 Cargando PIPO...", font=("Arial", 18))
    label_texto.pack()

    # Centro la ventana
    splash.update_idletasks()
    ancho = splash.winfo_width()
    alto = splash.winfo_height()
    x = (splash.winfo_screenwidth() // 2) - (ancho // 2)
    y = (splash.winfo_screenheight() // 2) - (alto // 2)
    splash.geometry(f"{ancho}x{alto}+{x}+{y}")

    # --- FADE IN ---
    for i in range(0, 11):
        splash.attributes('-alpha', i * 0.1)
        time.sleep(0.05)
        splash.update()

    reproducir_sonido_bienvenida()

    time.sleep(1.5)  # Splash visible en 100% un rato

    # --- FADE OUT ---
    for i in range(10, -1, -1):
        splash.attributes('-alpha', i * 0.1)
        time.sleep(0.05)
        splash.update()

    splash.destroy()

# Función para simular un avance progresivo en la barra
def simular_progreso(barra, detener_evento):
    progreso = 0.0
    while not detener_evento.is_set() and progreso < 1.0:
        progreso += 0.01  # Sube de a 1% cada vez
        barra.set(min(progreso, 1.0))  # Nunca más de 100%
        time.sleep(0.1)  # 100 milisegundos entre cada incremento
    barra.set(1.0)  # Aseguramos que quede llena al final
    
# Funcion para popup descarga finalizada    
def mostrar_popup_exito():
    popup = customtkinter.CTkToplevel()
    popup.title("✅ ¡Listo!")
    popup.geometry("300x150")
    
    label = customtkinter.CTkLabel(
        popup,
        text="🎶 ¡Tu música ya está lista!",
        font=("Arial", 16),
        text_color="white"
    )
    label.pack(pady=20)
    
    boton_ok = customtkinter.CTkButton(
        popup,
        text="OK",
        command=popup.destroy,
        fg_color="#004225",       # Verde inglés
        hover_color="#006400",
        text_color="white"
    )
    boton_ok.pack(pady=10)


# Función de descarga de audio
def descargar_audio_con_progreso(url, carpeta_destino, barra, mensaje_label, boton_descargar):
    detener_evento = threading.Event()
    threading.Thread(target=simular_progreso, args=(barra, detener_evento), daemon=True).start()

    comando = [
        'yt-dlp',
        '-f', 'bestaudio',
        '--extract-audio',
        '--audio-format', 'mp3',
        '--audio-quality', '192K',
        '--concurrent-fragments', '10',
        '-o', os.path.join(carpeta_destino, '%(title)s.%(ext)s'),
        url
    ]

    try:
        subprocess.run(comando, check=True)
    except Exception as e:
        mensaje_label.configure(text=f"⚠️ Error: {e}")
        detener_evento.set()
        barra.set(0)
        boton_descargar.configure(state="normal")
        return

    detener_evento.set()
    barra.set(1.0)
    mensaje_label.configure(text="✅ ¡Descarga completa!")
    boton_descargar.configure(state="normal")

    # Cuando termina la descarga real:
    detener_evento.set()
    barra.set(1.0)
    mensaje_label.configure(text="✅ ¡Descarga completa!")
    boton_descargar.configure(state="normal")

    mostrar_popup_exito()  # <-- Agregás esta línea mágica


def extraer_porcentaje(linea):
    match = re.search(r'(\d{1,3})%', linea)
    if match:
        return int(match.group(1))
    return None

def seleccionar_carpeta():
    carpeta = filedialog.askdirectory()
    if carpeta:
        carpeta_entry.delete(0, customtkinter.END)
        carpeta_entry.insert(0, carpeta)

def comenzar_descarga():
    url = link_entry.get()
    carpeta_destino = carpeta_entry.get()
    if url and carpeta_destino:
        mensaje_label.configure(text="⏳ Descargando...")
        boton_descargar.configure(state="disabled")
        threading.Thread(target=descargar_audio_con_progreso, args=(url, carpeta_destino, barra, mensaje_label, boton_descargar), daemon=True).start()
    else:
        mensaje_label.configure(text="⚠️ Completá todos los campos.")

# --- LANZAR SPLASH PRIMERO ---
splash_screen()

# --- DESPUÉS LANZAMOS PIPO NORMAL ---
# --- Después del splash_screen() ---
ventana = customtkinter.CTk()
ventana.title(f"🎶 PIPO {VERSION} - by LansDev")
ventana.geometry("500x450")

titulo = customtkinter.CTkLabel(
    ventana,
    text="Convertí YouTube en Música 🎵",
    font=("Arial", 20),
    text_color="white"  # Texto blanco sobre fondo oscuro
)
titulo.pack(pady=20)

link_entry = customtkinter.CTkEntry(
    ventana,
    width=400,
    placeholder_text="Pegá el link de YouTube aquí"
)
link_entry.pack(pady=10)

carpeta_entry = customtkinter.CTkEntry(
    ventana,
    width=400,
    placeholder_text="Carpeta destino"
)
carpeta_entry.pack(pady=10)

boton_carpeta = customtkinter.CTkButton(
    ventana,
    text="Seleccionar Carpeta",
    command=seleccionar_carpeta,
    fg_color="#004225",         # Verde inglés elegante
    hover_color="#006400",      # Verde militar más claro al pasar mouse
    text_color="white"          # Texto blanco
)
boton_carpeta.pack(pady=5)

barra = customtkinter.CTkProgressBar(
    ventana,
    width=400,
    progress_color="#004225"    # Barra de progreso verde inglés
)
barra.pack(pady=20)
barra.set(0)

mensaje_label = customtkinter.CTkLabel(
    ventana,
    text="",
    font=("Arial", 14),
    text_color="white"          # Mensajes blancos
)
mensaje_label.pack(pady=5)

boton_descargar = customtkinter.CTkButton(
    ventana,
    text="Descargar y Convertir",
    command=comenzar_descarga,
    fg_color="#004225",
    hover_color="#006400",
    text_color="white"
)
boton_descargar.pack(pady=10)

ventana.mainloop()
