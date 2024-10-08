
# TFG-Movistar

# INTRODUCCIÓN
Este proyecto se basa en el desarrollo experimental para la integración de herramientas de inteligencia artificial que pueda mejorar la interfaz y la base de datos de la Videoteca de Movistar+, https://videotecamovistarplus.es/.

La plataforma de Movistar+ proporciona una variedad de contenido de películas o series, pero no incluye sistemas de recomendación del contenido o de transcripción de audio a texto. A partir de una demanda creciente de soluciones personalizadas se identificó una oportunidad de mejora en cuanto a la experiencia de usuario.
Para mejorar la experiencia de usuario, se ha identificado una necesidad de añadir funcionalidades que mejoren la personalización del contenido y así como otras funcionalidades que puedan servir de ayuda al usuario a 
la hora de visualizar los vídeos de modo que favorezca la accesibilidad. Se planteó enriquecer la plataforma con un sistema de recomendación de películas que ofrezca sugerencias personalizadas basadas en el contenido
que el usuario visualiza. Además, también se pensó añadir funcionalidades de transcripción de audio a texto, para proporcionar subtítulos en tiempo real. Todo esto usando técnicas de análisis de datos y el uso de 
Inteligencia Artificial. 


# DESARROLLO E IMPLEMENTACIÓN

**Análisis Exploratorio de los Datos:** 

  - Inicia el desarrollo con un análisis exploratorio para comprender mejor los datos disponibles.

**Selección del Modelo de Clustering:**   

  - Se elige el algoritmo de clustering más adecuado basado en los resultados del análisis exploratorio. K-Means con 6 clústeres.

**Implementación del Recomendador:**   

  - Se integra el sistema de recomendación, coincidiendo con el final de la selección del modelo de clustering.


 <div align="center">
  <img src="https://github.com/user-attachments/assets/0952d998-026d-434c-be83-bda4ed006a78" alt="Index" width="800">
</div>
<br>
 <div align="center">
  <img src="https://github.com/user-attachments/assets/3c532165-305e-4a74-b66f-bf1a8dedf5c1" alt="top10" width="800">
</div>
  
  
**Selección del Modelo de Speech to Text:**  

  - Se selecciona y ajusta el modelo de transcripción de voz.
    
<div align="center">
  <img src="https://github.com/user-attachments/assets/6d7ccc1c-0f0b-47e3-871e-31edb5c6dfec" alt="trasncrip" width="800">
</div>
<br>
<div align="center">
  <img src="https://github.com/user-attachments/assets/232c41c8-bcbc-4081-b77c-f13211b94b00" alt="trasncrip2" width="800">
</div>
    

**Implementación de la Interfaz Web:** 
  - Se desarrolla la interfaz web para integrar todas las funcionalidades del sistema.


------------------------------------------------------------------------------------------------------------------------------------------------
# EJECUCIÓN DEL PROYECTO
  1. Navegar hasta el archivo principal app.py que se encuentra en la carpeta flask_clustering_app (cd src/flask_clustering_app)
  2. Ejecutar el comando python app.py
  3. Si queremos tener transcripción, tenemos que ejecutar antes del paso 2, python transcribe_audio.

