from flask import Flask, render_template, request, url_for
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import hstack
import os

app = Flask(__name__)

# Definir las variables globales
movies = None
cosine_sim = None

def load_and_process_data():
    global movies, cosine_sim
    # Cargar el archivo CSV
    movies = pd.read_csv("movies.dat", sep="\t", engine="python", header=0, encoding="ISO-8859-1",
                        names=["MovieID", "Title", "imdbID", "spanishTitle", "imdbPictureURL", "year",
                                "rtID", "rtAllCriticsRating", "rtAllCriticsNumReviews", "rtAllCriticsNumFresh",
                                "rtAllCriticsNumRotten", "rtAllCriticsScore", "rtTopCriticsRating", "rtTopCriticsNumReviews",
                                "rtTopCriticsNumFresh", "rtTopCriticsNumRotten", "rtTopCriticsScore", "rtAudienceRating",
                                "rtAudienceNumRatings", "rtAudienceScore", "rtPictureURL"])

    # Eliminar duplicados basados en 'imdbID'
    movies = movies.drop_duplicates(subset=['imdbID'])

    # Eliminar columnas innecesarias
    movies = movies.drop(columns=['imdbPictureURL', 'rtID'])

    # Convertir las columnas relevantes a formato numérico
    cols_to_convert = ['rtAllCriticsRating', 'rtAllCriticsNumReviews', 'rtAllCriticsNumFresh', 'rtAllCriticsNumRotten',
                    'rtAllCriticsScore', 'rtTopCriticsRating', 'rtTopCriticsNumReviews', 'rtTopCriticsNumFresh',
                    'rtTopCriticsNumRotten', 'rtTopCriticsScore', 'rtAudienceRating', 'rtAudienceNumRatings',
                    'rtAudienceScore']

    movies[cols_to_convert] = movies[cols_to_convert].apply(pd.to_numeric, errors='coerce')
    movies = movies.dropna()

    # Seleccionar las características relevantes
    features = movies[['year', 'rtAllCriticsRating', 'rtAllCriticsNumRotten', 
                    'rtTopCriticsRating', 'rtAudienceRating', 'rtAudienceNumRatings']]

    # Normalizar las características numéricas
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    # Convertir el texto (título de la película) en vectores TF-IDF
    tfidf_vectorizer = TfidfVectorizer()
    title_tfidf = tfidf_vectorizer.fit_transform(movies['spanishTitle'])

    # Concatenar características numéricas y texto
    X_combined = hstack([scaled_features, title_tfidf])

    # Aplicar K-Means
    kmeans = KMeans(n_clusters=6, random_state=42)
    kmeans_labels = kmeans.fit_predict(X_combined)

    # Agregar las etiquetas de cluster al DataFrame
    movies['KMeans_Cluster'] = kmeans_labels
    
    # Calcular la similitud de coseno para todas las películas y definirla globalmente
    cosine_sim = cosine_similarity(X_combined)

# Cargar y procesar los datos cuando se inicia la aplicación
load_and_process_data()

@app.route('/')
def index():
    # Crear una lista de tuplas (MovieID, spanishTitle)
    movie_options = [(row['MovieID'], row['spanishTitle']) for _, row in movies.iterrows()]
    # Renderizar la plantilla sin recomendaciones y sin película seleccionada
    return render_template('index.html', movie_options=movie_options, selected_movie_id=None, recommendations=None)

@app.route('/recommend', methods=['POST'])
def recommend():
    selected_movie_id = request.form['movie_id']
    
    # Asegúrate de que el MovieID recibido es un entero
    movie_id = int(selected_movie_id)

    # Encontrar el índice de la película seleccionada en el DataFrame
    movie_idx = movies[movies['MovieID'] == movie_id].index[0]

    # Obtener las similitudes de coseno para la película seleccionada
    sim_scores = list(enumerate(cosine_sim[movie_idx]))

    # Ordenar las películas por similitud de coseno
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Obtener los índices de las 10 películas más similares (excluyendo la propia película seleccionada)
    top_indices = [i for i, _ in sim_scores[1:11]]

    # Obtener las recomendaciones
    recommendations = movies.iloc[top_indices][['MovieID', 'spanishTitle']]

    # Convertir el DataFrame a una lista de diccionarios
    recommendations_list = recommendations.to_dict(orient='records')

    # Crear la lista de opciones de películas para el desplegable
    movie_options = [(row['MovieID'], row['spanishTitle']) for _, row in movies.iterrows()]
    
    # Obtener la transcripción del video (si existe)
    transcription = None
    transcription_path = 'static/transcriptions/transcription.txt'
    if os.path.exists(transcription_path):
        with open(transcription_path, 'r') as file:
            transcription = file.read()

    # Renderizar la plantilla con las recomendaciones y la película seleccionada
    return render_template('index.html', movie_options=movie_options, 
                           recommendations=recommendations_list,
                           selected_movie_id=selected_movie_id,
                           video_url=url_for('static', filename='videos/video.mp4'),
                           transcription=transcription)

if __name__ == '__main__':
    app.run(debug=True,port=9050)
