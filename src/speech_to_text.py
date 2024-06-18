import moviepy.editor as mp
import speech_recognition as sr
from IPython.display import display
import ipywidgets as widtgets
import os 

"""
pip install moviepy
pip install SpeechRecognition
pip install ipywidgets

--- Notebook ->
     jupyter nbextension enable --py widgetsnbextension --sys-prefix
    jupyter nbextension install --py widgetsnbextension --sys-prefix

"""


# Ruta absoluta del archivo de video y audio
video_file = os.path.join('/Users/sergio/Desktop/TFG-Movistar/JupiterNotebook/', 'Kevin_Surace.mp4')
audio_file = os.path.join('/Users/sergio/Desktop/TFG-Movistar/JupiterNotebook/', 'audio_video.wav')

# Imprimir la ruta completa del archivo de video para verificar
print(f"Ruta completa del archivo de video: {video_file}")

# Verificar que la ruta del archivo de video es correcta
if not os.path.exists(video_file):
    raise FileNotFoundError(f"El archivo de video no se encontró: {video_file}")

# Extraer el audio del video
video = mp.VideoFileClip(video_file)
video.audio.write_audiofile(audio_file)

# Inicializar el reconocedor de habla
recognizer = sr.Recognizer()

# Convertir audio a texto
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Habla ahora")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=5)
        try:
            print("Procesando...")
            # Utilizo reconocimiento por voz de Google
            text = recognizer.recognize_google(audio, language="es-ES")
            print("Texto reconocido:", text)
        except sr.UnknownValueError:
            print("No se ha podido entender el audio")
        except sr.RequestError as e:
            print(f"Error en la solicitud a Google API: {e}")

# Función para transcribir el audio
def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()
    audio = sr.AudioFile(audio_file)
    with audio as source:
        audio_data = recognizer.record(source)
        try:
            transcription = recognizer.recognize_google(audio_data, language="en-EN")
            return transcription
        except sr.UnknownValueError:
            return "No se ha podido transcribir el audio"
        except sr.RequestError as e:
            return f"Error en la solicitud de transcripción: {e}"

# Llamar a la función para convertir el audio a texto
speech_to_text()

# Transcribir el audio
transcription = transcribe_audio(audio_file)
print("Transcripción del audio: ")
print(transcription)

# Guardar la transcripción en un archivo de texto
output_file = "Transcription.txt"
with open(output_file, 'w') as f:
    f.write(transcription)
