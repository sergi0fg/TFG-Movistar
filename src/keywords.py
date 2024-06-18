from flask import Flask, render_template, request, flash
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Necesario para flash messages

# Cargar el JSON con los datos
try:
    with open('actores_descripciones.json', 'r', encoding='utf-8') as f:
        actores_descripciones = json.load(f)
except FileNotFoundError:
    actores_descripciones = []
    print("Error: No se encontró el archivo 'actores_descripciones.json'")

# Vectorizar los textos usando TF-IDF
def combinar_texto(actores, descripcion, descripcion_secundaria):
    return ' '.join(actores) + ' ' + descripcion + ' ' + descripcion_secundaria

textos = [combinar_texto(obj['actores'], obj['descripcion'], obj['descripcion_secundaria']) for obj in actores_descripciones]
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(textos)

# Función para recomendar basándose en un actor
def recomendar_por_actor(actor, actores_descripciones, tfidf_matrix, n_recommendations=5):
    if not actor:
        return []
    
    # Filtrar objetos que contengan el actor especificado (ignorando mayúsculas/minúsculas)
    objetos_filtrados = [obj for obj in actores_descripciones if any(actor.lower() in a.lower() for a in obj['actores'])]
    
    # Si no hay coincidencias, retornar una lista vacía
    if not objetos_filtrados:
        return []
    
    # Calcular similitudes y ordenar las recomendaciones basadas en la similitud de descripción
    textos_filtrados = [combinar_texto(obj['actores'], obj['descripcion'], obj['descripcion_secundaria']) for obj in objetos_filtrados]
    tfidf_matrix_filtrada = vectorizer.transform(textos_filtrados)
    
    similitudes = cosine_similarity(tfidf_matrix_filtrada, tfidf_matrix)
    
    recomendaciones = []
    for idx, similaridad in enumerate(similitudes):
        indices_similares = similaridad.argsort()[-n_recommendations-1:-1][::-1]
        recomendaciones.extend([actores_descripciones[i] for i in indices_similares if actores_descripciones[i] not in recomendaciones])

    # Limitar el número de recomendaciones a n_recommendations
    recomendaciones = recomendaciones[:n_recommendations]
    
    return recomendaciones

@app.route('/', methods=['GET', 'POST'])
def index():
    recomendaciones = []
    if request.method == 'POST':
        actor = request.form['actor'].strip()
        if not actor:
            flash('Por favor, introduce el nombre de un actor.', 'error')
        else:
            recomendaciones = recomendar_por_actor(actor, actores_descripciones, tfidf_matrix)
            if not recomendaciones:
                flash(f'No se encontraron recomendaciones para el actor: {actor}', 'info')
    return render_template('index.html', recomendaciones=recomendaciones)

if __name__ == '__main__':
    app.run(debug=True)
