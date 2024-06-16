import requests
import json


# Si la URL requiere autenticación básica, reemplaza 'your_username' y 'your_password' con tus credenciales.
auth = ('sergiofernandezgonzalez', 'SergioFG')

# URL de la API
url = "https://videotecamovistarplus.es/api/media/mmobj.json"


# Realizamos la solicitud GET con autenticación
response = requests.get(url, auth=auth)

# Verificamos si la solicitud fue exitosa
if response.status_code == 200:
    data = response.json()  # Analizamos el JSON de la respuesta
    
    # Guardamos el JSON en un archivo para revisarlo con más facilidad
    with open('mmobj.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print("Datos guardados en 'mmobj.json'")
else:
    print(f"Error: {response.status_code}")
# Determinamos si 'data' es un diccionario
if isinstance(data, dict):
    print("El JSON es un diccionario con las siguientes claves:")
    for key, value in data.items():
        print(f"  {key}: {type(value).__name__}")
    
    # Exploramos la lista 'criteria'
    if 'criteria' in data and isinstance(data['criteria'], list):
        print("\nContenido de 'criteria':")
        for i, item in enumerate(data['criteria']):
            print(f"  Elemento {i+1}: {item}")
            if i >= 4:  # Mostramos solo los primeros 5 elementos
                break
    
    # Exploramos la lista 'sort'
    if 'sort' in data and isinstance(data['sort'], list):
        print("\nContenido de 'sort':")
        for i, item in enumerate(data['sort']):
            print(f"  Elemento {i+1}: {item}")
            if i >= 4:  # Mostramos solo los primeros 5 elementos
                break
    
    # Exploramos la lista 'mmobjs'
    if 'mmobjs' in data and isinstance(data['mmobjs'], list):
        print("\nContenido de 'mmobjs':")
        for i, item in enumerate(data['mmobjs']):
            print(f"  Elemento {i+1}:")
            if isinstance(item, dict):
                for key, value in item.items():
                    print(f"    {key}: {value}")
            else:
                print(f"    {item}")
            if i >= 4:  # Mostramos solo los primeros 5 elementos
                break
else:
    print("El formato de datos no es un diccionario.")
