from flask import Flask, render_template, request, url_for, jsonify
import pandas as pd
import json
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import hstack
import os

app = Flask(__name__)

movies = None
cosine_sim = None

def load_and_process_data():
    global movies, cosine_sim
    movies = pd.read_csv("movies.dat", sep="\t", engine="python", header=0, encoding="ISO-8859-1",
                        names=["MovieID", "Title", "imdbID", "spanishTitle", "imdbPictureURL", "year",
                                "rtID", "rtAllCriticsRating", "rtAllCriticsNumReviews", "rtAllCriticsNumFresh",
                                "rtAllCriticsNumRotten", "rtAllCriticsScore", "rtTopCriticsRating", "rtTopCriticsNumReviews",
                                "rtTopCriticsNumFresh", "rtTopCriticsNumRotten", "rtTopCriticsScore", "rtAudienceRating",
                                "rtAudienceNumRatings", "rtAudienceScore", "rtPictureURL"])

    movies = movies.drop_duplicates(subset=['imdbID'])
    movies = movies.drop(columns=['imdbPictureURL', 'rtID'])

    cols_to_convert = ['rtAllCriticsRating', 'rtAllCriticsNumReviews', 'rtAllCriticsNumFresh', 'rtAllCriticsNumRotten',
                    'rtAllCriticsScore', 'rtTopCriticsRating', 'rtTopCriticsNumReviews', 'rtTopCriticsNumFresh',
                    'rtTopCriticsNumRotten', 'rtTopCriticsScore', 'rtAudienceRating', 'rtAudienceNumRatings',
                    'rtAudienceScore']

    movies[cols_to_convert] = movies[cols_to_convert].apply(pd.to_numeric, errors='coerce')
    movies = movies.dropna()

    features = movies[['year', 'rtAllCriticsRating', 'rtAllCriticsNumRotten', 
                    'rtTopCriticsRating', 'rtAudienceRating', 'rtAudienceNumRatings']]

    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    tfidf_vectorizer = TfidfVectorizer()
    title_tfidf = tfidf_vectorizer.fit_transform(movies['spanishTitle'])

    X_combined = hstack([scaled_features, title_tfidf])

    kmeans = KMeans(n_clusters=6, random_state=42)
    kmeans_labels = kmeans.fit_predict(X_combined)

    movies['KMeans_Cluster'] = kmeans_labels
    
    cosine_sim = cosine_similarity(X_combined)

load_and_process_data()

@app.route('/')
def index():
    movie_options = [(row['MovieID'], row['spanishTitle']) for _, row in movies.iterrows()]
    return render_template('index.html', movie_options=movie_options, selected_movie_id=None, recommendations=None)

@app.route('/recommend', methods=['POST'])
def recommend():
    selected_movie_id = request.form['movie_id']
    movie_id = int(selected_movie_id)
    movie_idx = movies[movies['MovieID'] == movie_id].index[0]
    sim_scores = list(enumerate(cosine_sim[movie_idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    top_indices = [i for i, _ in sim_scores[1:11]]
    recommendations = movies.iloc[top_indices][['MovieID', 'spanishTitle']]
    recommendations_list = recommendations.to_dict(orient='records')

    movie_options = [(row['MovieID'], row['spanishTitle']) for _, row in movies.iterrows()]
    
    return render_template('index.html', movie_options=movie_options, 
                           recommendations=recommendations_list,
                           selected_movie_id=selected_movie_id,
                           video_url=url_for('static', filename='videos/video.mp4'))

@app.route('/transcription', methods=['GET'])
def get_transcription():
    json_path = 'static/transcriptions/transcription.json'
    if os.path.exists(json_path):
        with open(json_path, 'r') as file:
            transcription = json.load(file)
        return jsonify(transcription)
    else:
        return jsonify([])

if __name__ == '__main__':
    app.run(debug=True,port=4060)
