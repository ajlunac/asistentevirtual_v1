import speech_recognition as sr
import pyttsx3, pywhatkit, wikipedia, datetime, keyboard, os
import subprocess as sub
from pygame import mixer
from tkinter import *
from PIL import Image, ImageTk
import threading as tr

# Interfaz grafica del asistente virtual.
main_window = Tk()
main_window.title("Asistente Virtual | Lola")
main_window.geometry("800x600")
main_window.resizable(0, 0)
main_window.config(bg="#eea849")

comandos = """
    Comandos que puedes utlizar
        - Reproduce... (cancion)
        - Buca... (algo)
        - Alarma... (hora)
        - Abre... (sitio web)
        - Archivo... (nombre de archivo)
        - Escribe... (algo)
        - Termina... (nada)
"""

label_title = Label(main_window, text="Asistente Virtual | Lola", font=("Arial", 24, 'bold'), bg="#eea849", fg="#2C5364")
label_title.pack(pady=10)

canva_comandos = Canvas(main_window, bg="#2C5364", height=180, width=600)
canva_comandos.pack(pady=10)
canva_comandos.create_text(120, 90, text=comandos, fill="#eea849", font=("Arial", 12))

text_info = Text(main_window, bg="#2C5364", fg="#eea849", font=("Arial", 12),)
text_info.place(x=100, y=270, width=600, height=60)

lola_img = ImageTk.PhotoImage(Image.open("Logo.png"))
window_img = Label(main_window, image=lola_img, bg="#eea849")
window_img.place(x=100, y=330, width=600, height=200)

def mexican_voice():
    change_voice(0)
def american_voice():
    change_voice(1)
def change_voice(id):
    engine.setProperty('voice', voices[id].id)
    engine.setProperty('rate', 145)
    talk("Hola, soy Lola, asistente virtual personal. ¿Qué puedo hacer por ti?")

name = "lola"
listener = sr.Recognizer()
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 145)

sites = dict()
files = dict()
programs = dict()

def talk(text):
    engine.say(text)
    engine.runAndWait()
    
def read_and_talk():
    text = text_info.get("1.0", "end-1c")
    talk(text)

def write_text(text_wiki):
    text_info.insert(INSERT, text_wiki)

def clock(rec):
    num = rec.replace("alarma", "")
    num = num.strip()
    talk("Alarma activada a las " + num + " horas")
    if num[0] != "0" and len(num) < 5:
        num = "0" + num
    print(num)
    while True:
        if datetime.datetime.now().strftime("%H:%M") == num:
            print("DESPIERTA!!!")
            mixer.init()
            mixer.music.load("auronplay-alarm.mp3")
            mixer.music.play()
        else:
            continue
        if keyboard.read_key() == "s":  
            mixer.music.stop()
            break

def listen():
    listener = sr.Recognizer()
    with sr.Microphone() as source:
        talk("¿Qué deseas hacer?")
        listener.adjust_for_ambient_noise(source)
        pc = listener.listen(source)
    try:
        rec = listener.recognize_google(pc, language="es")
        rec = rec.lower()
    except sr.UnknownValueError:
        talk("No se ha podido entender lo que dijiste")
        return "" # Aseguramos que se retorne algo si no se entiende
    return rec

def run_lola():
    while True:
        rec = listen()
        if rec: # Solo continuar si hay algo en rec
            if name in rec:
                rec = rec.replace(name, "") # Quitamos el nombre de la oración
                if "reproduce" in rec:
                    music = rec.replace("reproduce", "")
                    print(f"Reproduciendo {music}")
                    talk(f"Reproduciendo {music}")
                    pywhatkit.playonyt(music)
                elif "busca" in rec:
                    search = rec.replace("busca", "")
                    wikipedia.set_lang("es")
                    wiki = wikipedia.summary(search, 1)
                    talk(wiki)
                    write_text(search +": " + wiki)
                    break
                elif "alarma" in rec:
                    t = tr.Thread(target=clock, args=(rec,))
                    t.start()
                    break
                            
                elif "abre" in rec:
                    for site in sites:
                        if site in rec:
                            sub.call(f'start chrome.exe {sites[site]}', shell=True)
                            talk(f"Abriendo {site}")
                    for app in programs:
                        if app in rec:
                            talk(f"Abriendo {app}")
                            sub.Popen([programs[app]])
                        
                elif "archivo" in rec:
                    for file in files:
                        if file in rec:
                            sub.Popen([files[file]], shell=True)
                            talk(f"Abriendo {file}")
                            break
                        
                elif "escribe" in rec:
                    try:
                        with open("notas.txt", "a") as f:
                            write(f)
                    except FileNotFoundError as e:
                        file = open("notas.txt", "w")
                        write(file)
                
                            
                elif "termina" in rec:
                    talk("Adiós!")
                    break

        else:
            print("No se ha podido entender lo que dijiste")

def write(f):
    talk("¿Que quieres escribir?")
    rec_write = listen()
    f.write(rec_write + os.linesep)
    f.close()
    talk("Listo, puedes revisar tus notas")
    sub.Popen("notas.exe", shell=True)
    
def open_w_files():
    window_files = Toplevel()
    window_files.title("Agregar archivos")
    window_files.geometry("400x200")
    window_files.config(bg="#2C5364")
    window_files.resizable(0, 0)
    main_window.eval(f'tk::PlaceWindow {str(window_files)} center')

    title_label = Label(window_files, text="Agregar archivos", font=("Arial", 16, 'bold'), bg="#2C5364", fg="#eea849")
    title_label.pack(pady=3)
    name_label = Label(window_files, text="Nombre del archivo", font=("Arial", 12, 'bold'), bg="#2C5364", fg="#eea849")
    name_label.pack(pady=2)
    
    namefile_entry = Entry(window_files, font=("Arial", 12), bg="#2C5364", fg="#eea849")
    namefile_entry.pack(pady=1)
    
    path_label = Label(window_files, text="Ruta del archivo", font=("Arial", 12, 'bold'), bg="#2C5364", fg="#eea849")
    path_label.pack(pady=2)
    
    path_entry = Entry(window_files, font=("Arial", 12), bg="#2C5364", fg="#eea849", width=35)
    path_entry.pack(pady=1)
    
    save_button = Button(window_files, text="Guardar", bg="#2C5364", fg="#eea849", font=("Arial", 12, 'bold'), width=8, height=1)
    save_button.pack(pady=4)
    
def open_w_apps():
    window_apps = Toplevel()
    window_apps.title("Agregar APPs")
    window_apps.geometry("400x200")
    window_apps.config(bg="#2C5364")
    window_apps.resizable(0, 0)
    main_window.eval(f'tk::PlaceWindow {str(window_apps)} center')

    title_label = Label(window_apps, text="Agregar APPs", font=("Arial", 16, 'bold'), bg="#2C5364", fg="#eea849")
    title_label.pack(pady=3)
    name_label = Label(window_apps, text="Nombre de la APP", font=("Arial", 12, 'bold'), bg="#2C5364", fg="#eea849")
    name_label.pack(pady=2)
    
    nameapp_entry = Entry(window_apps, font=("Arial", 12), bg="#2C5364", fg="#eea849")
    nameapp_entry.pack(pady=1)
    
    path_label = Label(window_apps, text="Ruta del APP", font=("Arial", 12, 'bold'), bg="#2C5364", fg="#eea849")
    path_label.pack(pady=2)
    
    path_entry = Entry(window_apps, font=("Arial", 12), bg="#2C5364", fg="#eea849", width=35)
    path_entry.pack(pady=1)
    
    save_button = Button(window_apps, text="Guardar", bg="#2C5364", fg="#eea849", font=("Arial", 12, 'bold'), width=8, height=1)
    save_button.pack(pady=4)

def open_w_pages():
    window_pages = Toplevel()
    window_pages.title("Agregar páginas")
    window_pages.geometry("400x200")
    window_pages.config(bg="#2C5364")
    window_pages.resizable(0, 0)
    main_window.eval(f'tk::PlaceWindow {str(window_pages)} center')

    title_label = Label(window_pages, text="Agregar página", font=("Arial", 16, 'bold'), bg="#2C5364", fg="#eea849")
    title_label.pack(pady=3)
    name_label = Label(window_pages, text="Nombre de la página", font=("Arial", 12, 'bold'), bg="#2C5364", fg="#eea849")
    name_label.pack(pady=2)
    
    pagefile_entry = Entry(window_pages, font=("Arial", 12), bg="#2C5364", fg="#eea849")
    pagefile_entry.pack(pady=1)
    
    path_label = Label(window_pages, text="Ruta de la página", font=("Arial", 12, 'bold'), bg="#2C5364", fg="#eea849")
    path_label.pack(pady=2)
    
    path_entry = Entry(window_pages, font=("Arial", 12), bg="#2C5364", fg="#eea849", width=35)
    path_entry.pack(pady=1)
    
    save_button = Button(window_pages, text="Guardar", bg="#2C5364", fg="#eea849", font=("Arial", 12, 'bold'), width=8, height=1)
    save_button.pack(pady=4)

button_voice_mx = Button(main_window, text="Voz México", bg="#2C5364", fg="#eea849", font=("Arial", 12, 'bold'), command=mexican_voice)
button_voice_mx.place(x=20, y=400, width=100, height=30)

button_voice_us = Button(main_window, text="Voz USA", bg="#2C5364", fg="#eea849", font=("Arial", 12, 'bold'), command=american_voice)
button_voice_us.place(x=130, y=400, width=100, height=30)

button_listen = Button(main_window, text="Escuchar", bg="#2C5364", fg="#eea849", font=("Arial", 12, 'bold'), command=run_lola)
button_listen.place(x=240, y=400, width=100, height=30)

button_speak = Button(main_window, text="Hablar", bg="#2C5364", fg="#eea849", font=("Arial", 12, 'bold'), command=read_and_talk)
button_speak.place(x=350, y=400, width=100, height=30)

button_add_files = Button(main_window, text="Archivos", bg="#2C5364", fg="#eea849", font=("Arial", 12, 'bold'), command=open_w_files)
button_add_files.place(x=460, y=400, width=100, height=30)

button_add_app = Button(main_window, text="APPs", bg="#2C5364", fg="#eea849", font=("Arial", 12, 'bold'), command=open_w_apps)
button_add_app.place(x=570, y=400, width=100, height=30)

button_add_pages = Button(main_window, text="Páginas", bg="#2C5364", fg="#eea849", font=("Arial", 12, 'bold'), command=open_w_pages)
button_add_pages.place(x=680, y=400, width=100, height=30)

main_window.mainloop()