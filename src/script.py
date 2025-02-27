# import pandas as pd
# import json

# def main():
#     # Leer el archivo JSON
#     with open('data.json', 'r', encoding='utf-8') as f:
#         data = json.load(f)
    
#     # Si el JSON es un diccionario único, convertirlo a una lista
#     if isinstance(data, dict):
#         data = [data]
    
#     # Crear DataFrame y guardar en Excel
#     df = pd.DataFrame(data)
#     df.to_excel('output.xlsx', index=False)
#     print("Archivo Excel 'output.xlsx' generado exitosamente.")

# if __name__ == '__main__':
#     main()

# import requests
# import json

# def obtener_datos_api(url="", params={}):
#     try:
#         response = requests.get(url, params=params)
#         response.raise_for_status()  # Lanza una excepción si la respuesta no es exitosa
#         return response.json()
#     except requests.exceptions.RequestException as error:
#         print("Error al hacer la solicitud:", error)
#         return {}

# URL de la API de APOD de la NASA
# url = "https://api.nasa.gov/planetary/apod" 

# Parámetros (usamos la clave de demostración)
# params = {
#     "api_key": "DEMO_KEY"  # Clave de demostración (no requiere registro)
# }

# Obtener datos de la API
# datos = obtener_datos_api(url=url, params=params)

# Mostrar los datos
# if datos:
#     print(json.dumps(datos, indent=4))
# else:
#     print("No se encontraron datos")

# import pandas as pd
# import os
# from dotenv import load_dotenv
# from api.base import fetch_data_from_api
# from static.db.config  import create_connection
# from utils.helpers import  create_xlsx_file, audit_data

# load_dotenv()

# def main():

#     # api_url = 'https://api.coincap.io/v2/assets'
#     api_url = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"

#     data = fetch_data_from_api(api_url)


#     if isinstance(data, dict):
#         data = [data]

#     df_api = pd.json_normalize(data, record_path=['data'], meta=['timestamp'])

#     audit_data(df_api)

#     create_xlsx_file(df_api)
 
#     if os.getenv('DB_CONNECTION'):
#         conn = create_connection()
#         if conn:
#             df_api = df_api.applymap(lambda x: str(x) if isinstance(x, list) else x)
#             df_api.to_sql('table_name', conn, if_exists='replace', index=False)
#             print("Datos insertados en la base de datos exitosamente.")
#             conn.close()

# if __name__ == '__main__':
#     main()

import pandas as pd
import os
from dotenv import load_dotenv
from api.base import fetch_data_from_api
from static.db.config import create_connection
from utils.helpers import create_xlsx_file, audit_data

load_dotenv()

def main():
    # Usar la API de la NASA (APOD)
    api_url = 'https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY'

    try:
        # Obtener datos de la API
        data = fetch_data_from_api(api_url)

        # Verificar si la respuesta es un diccionario
        if isinstance(data, dict):
            # Normalizar el JSON directamente (sin record_path)
            df_api = pd.json_normalize(data)

            # Auditoría y creación del archivo XLSX
            audit_data(df_api)
            create_xlsx_file(df_api)

            # Insertar datos en la base de datos (si está configurada)
            if os.getenv('DB_CONNECTION'):
                conn = create_connection()
                if conn:
                    df_api = df_api.applymap(lambda x: str(x) if isinstance(x, list) else x)
                    df_api.to_sql('table_name', conn, if_exists='replace', index=False)
                    print("Datos insertados en la base de datos exitosamente.")
                    conn.close()
        else:
            print("La respuesta de la API no es un diccionario.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()