import requests
import json
import numpy as np
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity



# URL de la API y credenciales
url = "https://videotecamovistarplus.es/api/media/mmobj.json"

auth = ('sergiofernandezgonzalez', 'SergioFG')

# ID del objeto multimedia específico para el cual queremos hacer recomendaciones
mmobj_id = '5df1f5c9487d0f4c498b4577'


# Parámetros de filtrado por ID
params = {
    'criteria[id]': mmobj_id
}

try:
    # Realizar la solicitud GET con autenticación y parámetros de filtrado
    response = requests.get(url, auth=auth, params=params)

    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        data = response.json()  # Analizar el JSON de la respuesta

        # Extraer los datos del objeto multimedia específico
        if 'mmobjs' in data and len(data['mmobjs']) > 0:
            target_mmobj = data['mmobjs'][0]
            target_id = target_mmobj['id']
            target_title = target_mmobj['title']
            target_description = target_mmobj['description']

            print(f"Objeto multimedia ID {target_id}: {target_title}")
            print(f"Descripción:\n{target_description}\n")

            # Ejemplo de lista de otros objetos multimedia desde el JSON completo
            otros_mmobjs = data['mmobjs']

            # Función para calcular la similitud coseno entre las descripciones de dos objetos multimedia
            def calcular_similitud(desc1, desc2):
                vectorizer = TfidfVectorizer()
                tfidf_matrix = vectorizer.fit_transform([desc1, desc2])
                return cosine_similarity(tfidf_matrix)[0, 1]

            # Calcular la similitud entre el objeto multimedia específico y otros
            similaridades = []
            for otro_mmobj in otros_mmobjs:
                if otro_mmobj['id'] != target_id:  # Evitar comparar el objeto consigo mismo
                    similitud = calcular_similitud(target_description, otro_mmobj['description'])
                    similaridades.append((otro_mmobj['id'], otro_mmobj['title'], similitud))

            # Ordenar los objetos multimedia por similitud descendente y mostrar recomendaciones
            similaridades.sort(key=lambda x: x[2], reverse=True)
            if len(similaridades) > 0:
                print(f"Recomendaciones para el objeto multimedia ID {target_id} - {target_title}:")
                for rec_id, rec_title, sim in similaridades:
                    print(f"Objeto multimedia ID {rec_id} - {rec_title} - Similitud: {sim}")
            else:
                print(f"No se encontraron recomendaciones para el objeto multimedia ID {target_id} - {target_title}")

        else:
            print(f"No se encontró el objeto multimedia con ID {mmobj_id}")

    else:
        print(f"Error en la solicitud: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"Error en la solicitud: {e}")