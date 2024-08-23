import json
import os
import speech_recognition as sr
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
from pydub.silence import split_on_silence

# Definir los caminos de los archivos
video_path = 'static/videos/video.mp4'
audio_path = 'static/transcriptions/audio.wav'
json_path = 'static/transcriptions/transcription.json'

# Extraer audio del video
def extract_audio(video_path, audio_path):
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(audio_path, codec='pcm_s16le')

# Dividir el audio en segmentos donde se detecta voz
def split_audio_on_speech(audio_path):
    audio = AudioSegment.from_wav(audio_path)
    
    # Dividir el audio en segmentos basados en silencio
    chunks = split_on_silence(
        audio,
        min_silence_len=500,  # Ajusta según sea necesario
        silence_thresh=audio.dBFS - 14,  # Ajustar para ser más o menos sensible
        keep_silence=300
    )
    
    return chunks

# Transcribir cada segmento de audio
def transcribe_audio(chunks):
    recognizer = sr.Recognizer()
    transcript = []
    
    for i, chunk in enumerate(chunks):
        chunk.export("temp_chunk.wav", format="wav")
        
        with sr.AudioFile("temp_chunk.wav") as source:
            audio_segment = recognizer.record(source)
            
            try:
                # Reconocer el audio
                text = recognizer.recognize_google(audio_segment, language='es-ES')
                transcript.append({
                    'startTime': i * 10,  # Aproximado
                    'endTime': (i + 1) * 10,  # Aproximado
                    'text': text
                })
            except sr.UnknownValueError:
                transcript.append({
                    'startTime': i * 10,
                    'endTime': (i + 1) * 10,
                    'text': "[Sin reconocimiento]"
                })
            except sr.RequestError as e:
                transcript.append({
                    'startTime': i * 10,
                    'endTime': (i + 1) * 10,
                    'text': f"[Error: {e}]"
                })
    
    return transcript

# Asegurarse de que el directorio de transcripciones exista
os.makedirs(os.path.dirname(json_path), exist_ok=True)

# Extraer el audio del video
extract_audio(video_path, audio_path)

# Dividir el audio basado en detección de voz
chunks = split_audio_on_speech(audio_path)

# Transcribir el audio
transcription = transcribe_audio(chunks)

# Guardar la transcripción en un archivo JSON
with open(json_path, 'w') as json_file:
    json.dump(transcription, json_file, indent=4, ensure_ascii=False)

print(f"Transcripción guardada en {json_path}")
