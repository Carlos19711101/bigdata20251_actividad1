import requests
import json

def obtener_datos_api(url="", params={}):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Lanza una excepción si la respuesta no es exitosa
        return response.json()
    except requests.exceptions.RequestException as error:
        print("Error al hacer la solicitud:", error)
        return {}

# URL de la API de APOD de la NASA
url = "https://api.nasa.gov/planetary/apod"

# Parámetros (usamos la clave de demostración)
params = {
    "api_key": "DEMO_KEY"  # Clave de demostración (no requiere registro)
}

# Obtener datos de la API
datos = obtener_datos_api(url=url, params=params)

# Mostrar los datos
if datos:
    print(json.dumps(datos, indent=4))
else:
    print("No se encontraron datos")