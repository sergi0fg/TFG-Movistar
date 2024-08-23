import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from scipy.sparse import hstack

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

# Exportar el DataFrame a un archivo CSV
csv_file_path = "movies_with_clusters.csv"
movies.to_csv(csv_file_path, index=False)
