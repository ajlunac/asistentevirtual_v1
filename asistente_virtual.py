import speech_recognition as sr
import pyttsx3, pywhatkit

name = "lola"
listener = sr.Recognizer()
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

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
        else:
            print("No se ha podido entender lo que dijiste")
        
if __name__ == "__main__":
    run_lola()