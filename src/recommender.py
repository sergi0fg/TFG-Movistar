from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Suponiendo que tienes una lista de descripciones de objetos multimedia
descriptions = [
    "Presentado por Antonio Banderas y Ana Obregón...",
    # Agrega más descripciones aquí
]

# Vectorización de las descripciones usando TF-IDF
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(descriptions)

# Cálculo de la similitud coseno entre las descripciones
similarities = cosine_similarity(X)

# Ejemplo: obtener recomendaciones para un objeto multimedia dado (índice 0 en este caso)
obj_index = 0
similar_indices = similarities[obj_index].argsort()[:-6:-1]  # Top 5 similares excluyendo el mismo

# Imprime los IDs de los objetos multimedia recomendados
print(f"Recomendaciones para {mmobjs[obj_index]['id']}:")
for i, idx in enumerate(similar_indices[1:], start=1):  # Empieza desde 1 para excluir el mismo objeto
    print(f"{i}. ID: {mmobjs[idx]['id']}")

