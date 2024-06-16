import requests
import json

# URL de la API y credenciales
url = "https://videotecamovistarplus.es/api/media/mmobj.json"
auth = ('sergiofernandezgonzalez', 'SergioFG')

try:
    # Realizar la solicitud GET con autenticación
    response = requests.get(url, auth=auth)

    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        data = response.json()  # Analizar el JSON de la respuesta

        # Lista para almacenar los objetos filtrados
        actores_descripciones = []

        # Extraer y filtrar objetos con actores y descripciones
        if 'mmobjs' in data:
            for mmobj in data['mmobjs']:
                # Verificar si el objeto tiene actores y descripciones en español
                if 'i18nKeywords' in mmobj and 'es' in mmobj['i18nKeywords']:
                    actores = mmobj['i18nKeywords']['es']
                    text_index_es = next((ti['text'] for ti in mmobj.get('textIndex', []) if ti['indexlanguage'] == 'es'), '')
                    secondary_text_index_es = next((sti['text'] for sti in mmobj.get('secondaryTextIndex', []) if sti['indexlanguage'] == 'es'), '')
                    
                    # Agregar el objeto filtrado a la lista
                    actores_descripciones.append({
                        'actores': actores,
                        'descripcion': text_index_es,
                        'descripcion_secundaria': secondary_text_index_es
                    })

        # Guardar los objetos filtrados en un archivo JSON
        with open('actores_descripciones.json', 'w', encoding='utf-8') as f:
            json.dump(actores_descripciones, f, ensure_ascii=False, indent=4)

        print(f"Se han guardado {len(actores_descripciones)} objetos en 'actores_descripciones.json'")

    else:
        print(f"Error en la solicitud: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"Error en la solicitud: {e}")
