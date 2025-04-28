import PySimpleGUI as sg
import subprocess
import threading
import os
import re

def descargar_audio_con_progreso(url, carpeta_destino, window):
    comando = [
        'yt-dlp',
        '-f', 'bestaudio',
        '--extract-audio',
        '--audio-format', 'mp3',
        '--audio-quality', '192K',
        '-o', os.path.join(carpeta_destino, '%(title)s.%(ext)s'),
        url
    ]
    proceso = subprocess.Popen(
        comando,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        bufsize=1
    )
    for linea in proceso.stdout:
        porcentaje = extraer_porcentaje(linea)
        if porcentaje is not None:
            window['-BARRA-'].update(porcentaje)
    proceso.wait()
    window.write_event_value('-FIN-', 'ok')

def extraer_porcentaje(linea):
    match = re.search(r'(\d{1,3})%', linea)
    if match:
        return int(match.group(1))
    return None

layout = [
    [sg.Text('Pegá el link de YouTube')],
    [sg.InputText(key='-LINK-')],
    [sg.Text('Elegí la carpeta para guardar')],
    [sg.InputText(key='-CARPETA-'), sg.FolderBrowse()],
    [sg.ProgressBar(100, orientation='h', size=(30, 20), key='-BARRA-')],
    [sg.Button('Descargar y Convertir'), sg.Button('Salir')],
    [sg.Text('', key='-MENSAJE-', size=(50, 4))]
]

ventana = sg.Window('🎶 PIPO - Minimalismo Supremo', layout)

while True:
    evento, valores = ventana.read()
    if evento in (sg.WIN_CLOSED, 'Salir'):
        break
    if evento == 'Descargar y Convertir':
        url = valores['-LINK-']
        carpeta_destino = valores['-CARPETA-']
        if url and carpeta_destino:
            ventana['-MENSAJE-'].update('Descargando...')
            threading.Thread(target=descargar_audio_con_progreso, args=(url, carpeta_destino, ventana), daemon=True).start()
        else:
            ventana['-MENSAJE-'].update('Por favor, completá todos los campos.')
    if evento == '-FIN-':
        ventana['-MENSAJE-'].update('¡Descarga y conversión completadas!')
        ventana['-BARRA-'].update(0)

ventana.close()
