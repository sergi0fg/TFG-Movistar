import requests
import json
import numpy as np
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity





# Suponiendo que ya tienes la parte de solicitud GET y filtrado de datos guardados en 'mmobj_filtered.json'

# Realizamos la solicitud GET con autenticación y guardamos los datos en 'mmobj_filtered.json'
url = 'https://videotecamovistarplus.es/api/media/mmobj.json?criteria[id]=5df1f753487d0f4c498b4883'

auth = ('sergiofernandezgonzalez', 'SergioFG')
response = requests.get(url, auth=auth)

# Verificamos si la solicitud fue exitosa
if response.status_code == 200:
    data = response.json()  # Analizamos el JSON de la respuesta

    # Guardamos el JSON en un archivo para revisarlo con más facilidad
    with open('mmobj_filtered.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print("Datos guardados en 'mmobj_filtered.json'")

    # Determinamos si 'data' es un diccionario
    if isinstance(data, dict):
        print("El JSON filtrado es un diccionario con las siguientes claves:")
        for key, value in data.items():
            print(f"  {key}: {type(value).__name__}")

        # Accedemos a los atributos relevantes de 'mmobjs'
        if 'mmobjs' in data and isinstance(data['mmobjs'], list):
            mmobjs = data['mmobjs']  # Lista de objetos multimedia

            # Mostramos la información del primer elemento encontrado por el filtro
            for item in mmobjs:
                mmobj_id = item['id']
                title = item['title']
                description = item['description']
                duration = item['duration']
                num_views = item['numview']
                tags = [tag['title'] for tag in item['tags']]  # Obtener solo los títulos de las etiquetas

                # Mostrar información del objeto multimedia
                print(f"\nID: {mmobj_id}")
                print(f"Título: {title}")
                print(f"Descripción: {description}")
                print(f"Duración: {duration} segundos")
                print(f"Número de visualizaciones: {num_views}")
                print(f"Etiquetas: {tags}")

            # --- Ejemplo de clustering con duración y número de visualizaciones ---
            # Extraer características relevantes para el clustering (duración y número de visualizaciones)
            X = np.array([[obj["duration"], obj["numview"]] for obj in mmobjs])

            # Configurar el modelo de K-Means
            kmeans = KMeans(n_clusters=3, random_state=0)

            # Entrenar el modelo
            kmeans.fit(X)

            # Obtener las etiquetas de clúster asignadas
            labels = kmeans.labels_

            # Asignar las etiquetas de clúster a los objetos multimedia
            for i, obj in enumerate(mmobjs):
                obj["cluster_label"] = labels[i]

            # Imprimir los objetos multimedia agrupados por clúster
            for cluster_num in range(3):  # Cambia esto según el número de clústeres
                print(f"\nCluster {cluster_num}:")
                for obj in mmobjs:
                    if obj["cluster_label"] == cluster_num:
                        print(f"ID: {obj['id']}, Duración: {obj['duration']}, Número de visualizaciones: {obj['numview']}")

            # --- Ejemplo de recomendación basada en similitud de descripciones ---
            # Suponiendo que tienes una lista de descripciones de objetos multimedia
            descriptions = [item['description'] for item in mmobjs]

            # Vectorización de las descripciones usando TF-IDF
            vectorizer = TfidfVectorizer(stop_words='english')
            X = vectorizer.fit_transform(descriptions)

            # Cálculo de la similitud coseno entre las descripciones
            similarities = cosine_similarity(X)

            # Ejemplo: obtener recomendaciones para el primer objeto multimedia (índice 0 en este caso)
            obj_index = 0
            similar_indices = similarities[obj_index].argsort()[:-6:-1]  # Top 5 similares excluyendo el mismo

            # Imprimir los IDs de los objetos multimedia recomendados
            print(f"\nRecomendaciones para {mmobjs[obj_index]['id']} (basado en descripción):")
            for i, idx in enumerate(similar_indices[1:], start=1):  # Empieza desde 1 para excluir el mismo objeto
                print(f"{i}. ID: {mmobjs[idx]['id']}")
else:
    print(f"Error: {response.status_code}")

