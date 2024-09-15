import speech_recognition as sr
import pyttsx3, pywhatkit, wikipedia, datetime, keyboard, os
import subprocess as sub
from pygame import mixer

name = "lola"
listener = sr.Recognizer()
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

sites = {
    'google': 'google.com',
    'youtube': 'youtube.com',
    'facebook': 'facebook.com',
    'whatsapp': 'web.whatsapp.com',
    'cursos': 'freecodecamp.org/learn'
}

files = {
    'carta': 'Carta Pasantias - Javier Luna.pdf',
    'cédula': 'Cédula y papeleta - Javier Luna.docx',
    'foto': 'Foto Javier Luna.jpg'
}

programs = {
    'notas': r"C:\Program Files\Notepad++\notepad++.exe",
    'calc': r"C:\Program Files\LibreOffice\program\scalc.exe",
    'writer': r"C:\Program Files\LibreOffice\program\swriter.exe"
}

def talk(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    listener = sr.Recognizer()
    with sr.Microphone() as source:
        print("Escuchando...")
        listener.adjust_for_ambient_noise(source)
        pc = listener.listen(source)
    try:
        rec = listener.recognize_google(pc, language="es-ES")
        rec = rec.lower()
    except sr.UnknownValueError:
        print("No se ha podido entender lo que dijiste")
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
                    wikipedia.set_lang("es-ES")
                    wiki = wikipedia.summary(search, 1)
                    print(search +": " + wiki)
                    talk(wiki)
                    
                elif "alarma" in rec:
                    num = rec.replace("alarma", "")
                    num = num.strip()
                    talk("Alarma activada a las " + num + " horas")
                    while True:
                        if datetime.datetime.now().strftime("%H:%M") == num:
                            print("DESPIERTA!!!")
                            mixer.init()
                            mixer.music.load("auronplay-alarm.mp3")
                            mixer.music.play()
                            if keyboard.read_key() == "s":
                                mixer.music.stop()
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
        
if __name__ == "__main__":
    run_lola()
    

