import pandas as pd
import os
from dotenv import load_dotenv
from api.base import fetch_data_from_api
from static.db.config  import create_connection, create_table
from utils.helpers import  create_file, audit_data

load_dotenv()

def main():
    # URL de CoinGecko
    api_url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false'

    # Obtener datos de la API
    data = fetch_data_from_api(api_url)

    # Normalizar el JSON (no se usa record_path)
    df_api = pd.json_normalize(data)

    # Auditoría y creación de archivos
    audit_data(df_api)
    create_file(df_api, 'src/static/xlsx/request_api_xlsx.xlsx', file_format='xlsx')

    # Conexión a la base de datos y creación de la tabla
    conn = create_connection('bd_analisis.sqlite')
    create_table(conn, table_name='api_exchange', data=df_api)

if __name__ == '__main__':
    main()


