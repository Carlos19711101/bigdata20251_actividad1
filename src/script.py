# # import pandas as pd
# # import os
# # from dotenv import load_dotenv
# # from api.base import fetch_data_from_api
# # from static.db.config import create_connection
# # from utils.helpers import create_xlsx_file, audit_data

# # load_dotenv()

# # def main():
# #     # Se cambia la URL de nasa porque solo tenia un registro
# #     api_url = 'https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY'

# #     try:
# #         # Obtener datos de la API
# #         data = fetch_data_from_api(api_url)

# #         # Verificar si la respuesta es un diccionario
# #         if isinstance(data, dict):
# #             # Normalizar el JSON directamente (sin record_path)
# #             df_api = pd.json_normalize(data)

# #             # Auditoría y creación del archivo XLSX
# #             audit_data(df_api)
# #             create_xlsx_file(df_api)

# #             # Insertar datos en la base de datos (si está configurada)
           
# #             conn = create_connection()
# #             if conn:
# #                 df_api = df_api.applymap(lambda x: str(x) if isinstance(x, list) else x)
# #                 df_api.to_sql('table_name', conn, if_exists='replace', index=False)
# #                 print("Datos insertados en la base de datos exitosamente.")
# #                 conn.close()
    
    

# #     except Exception as e:
# #         print(f"Error: {e}")

# # if __name__ == '__main__':
# #     main()
# import pandas as pd
# import os
# from dotenv import load_dotenv
# from api.base import fetch_data_from_api
# from static.db.config  import create_connection, create_table
# from utils.helpers import  create_file, audit_data


# load_dotenv()

# def main():

#     api_url = 'https://api.sampleapis.com/movies/animation'

#     data = fetch_data_from_api(api_url)

#     df_api = pd.json_normalize(data, record_path=['data'], meta=['timestamp'])

#     audit_data(df_api)

#     create_file(df_api, 'src/static/xlsx/request_api_xlsx.xlsx', file_format='xlsx')

#     conn = create_connection('bd_analisis.sqlite')

#     create_table(conn, table_name='api.n.exchange', data=df_api)

# if __name__ == '__main__':
#     main()
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