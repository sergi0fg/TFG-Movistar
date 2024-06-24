from flask import Flask, request, render_template, flash
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
app.secret_key = 'some_secret_key'

# Cargar los datos de actores y descripciones
with open('actores_descripciones.json', 'r') as file:
    actores_descripciones = json.load(file)

def combinar_texto(actores, descripcion, descripcion_secundaria):
    return ' '.join(actores) + ' ' + descripcion + ' ' + descripcion_secundaria

# Preprocesamiento TF-IDF
textos = [combinar_texto(obj['actores'], obj['descripcion'], obj['descripcion_secundaria']) for obj in actores_descripciones]
vectorizer = TfidfVectorizer(stop_words='spanish')
tfidf_matrix = vectorizer.fit_transform(textos)

def recomendar_por_actor(actor, actores_descripciones, tfidf_matrix, n_recommendations=5):
    if not actor:
        return []

    actor_lower = actor.lower()
    
    # Filtrar objetos que contengan exactamente el actor especificado (ignorando mayúsculas/minúsculas)
    objetos_filtrados = [obj for obj in actores_descripciones if any(actor_lower in a.lower() for a in obj['actores'])]
    
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
    messages = []
    if request.method == 'POST':
        actor = request.form['actor']
        if actor:
            recomendaciones = recomendar_por_actor(actor, actores_descripciones, tfidf_matrix)
            if not recomendaciones:
                messages.append(('error', 'No se encontraron recomendaciones para el actor especificado.'))
        else:
            messages.append(('error', 'Por favor, ingrese un nombre de actor.'))
    
    return render_template('index.html', recomendaciones=recomendaciones, messages=messages)

if __name__ == '__main__':
    app.run(debug=True)


