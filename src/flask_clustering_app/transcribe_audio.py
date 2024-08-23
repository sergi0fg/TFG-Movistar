from moviepy.editor import VideoFileClip
import speech_recognition as sr

def extract_audio(video_path, audio_output_path):
    """
    Extrae el audio de un archivo de video y lo guarda como un archivo WAV.
    
    :param video_path: Ruta al archivo de video.
    :param audio_output_path: Ruta donde se guardará el archivo de audio.
    """
    # Cargar el video
    video = VideoFileClip(video_path)
    
    # Extraer y guardar el audio
    video.audio.write_audiofile(audio_output_path)
    print(f'Audio extraído y guardado en {audio_output_path}')

def transcribe_audio_to_text(audio_path):
    """
    Transcribe el audio de un archivo a texto utilizando SpeechRecognition y la API de Google.
    
    :param audio_path: Ruta al archivo de audio.
    :return: Transcripción del audio en forma de texto.
    """
    # Crear un reconocedor de voz
    recognizer = sr.Recognizer()

    # Leer el archivo de audio
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
    
    # Usar el reconocedor para convertir el audio a texto
    try:
        text = recognizer.recognize_google(audio, language="es-ES")
        print("Transcripción completa.")
        return text
    except sr.UnknownValueError:
        print("Google Speech Recognition no pudo entender el audio.")
        return ""
    except sr.RequestError as e:
        print(f"No se pudo solicitar el servicio de Google Speech Recognition; {e}")
        return ""

def main():
    # Definir las rutas de los archivos
    video_path = 'static/videos/video.mp4'
    audio_output_path = 'static/videos/video_audio.wav'
    transcription_file_path = 'static/transcriptions/transcription.txt'
    
    # Extraer el audio del video
    extract_audio(video_path, audio_output_path)
    
    # Transcribir el audio a texto
    transcription_text = transcribe_audio_to_text(audio_output_path)
    
    # Guardar la transcripción en un archivo de texto
    with open(transcription_file_path, 'w') as file:
        file.write(transcription_text)
    
    print(f'Transcripción guardada en {transcription_file_path}')

if __name__ == "__main__":
    main()
