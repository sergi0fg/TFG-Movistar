import speech_recognition as sr 

def speech_to_text():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Habla ahora...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=5)

        try:
            print("Procesando...")

            # Utilizamos el reconocimiento de voz de Google
            text = recognizer.recognize_google(audio, language="es-ES")
            print("Texto reconocido:", text)

        except sr.UnknownValueError:
            print("No se pudo entender el audio")

        except sr.RequestError as e:
            print(f"Error en la solicitud a Google API: {e}")

if __name__ == "__main__":
    speech_to_text()
