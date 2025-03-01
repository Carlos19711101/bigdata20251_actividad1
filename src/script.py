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
           
            conn = create_connection()
            if conn:
                df_api = df_api.applymap(lambda x: str(x) if isinstance(x, list) else x)
                df_api.to_sql('table_name', conn, if_exists='replace', index=False)
                print("Datos insertados en la base de datos exitosamente.")
                conn.close()
    
    

    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()