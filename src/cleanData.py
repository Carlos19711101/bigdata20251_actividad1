import pandas as pd
from static.db.config  import create_connection, create_table
from utils.helpers import create_file, format_number, log_step, get_output_txt
import numpy as np


log_step(f"Inicio proceso de limpieza de datos\n")


table_name = "api_exchange" 
table_clean = "api_clean"
conn = create_connection('bd_analisis.sqlite')
cursor = conn.cursor()
cursor.execute(f"SELECT * FROM {table_name}")

log_step(f"Conexión a la base de datos establecida y datos recuperados de {table_name}\n")

df_bd_api_exchange = pd.DataFrame(cursor.fetchall(), columns=[x[0] for x in cursor.description])
log_step(f"DataFrame inicial creada con forma:\n{df_bd_api_exchange.shape}\n")


df_api_exchange_log = get_output_txt(df_bd_api_exchange, 'info')
log_step(f"Información de DataFrame:\n{df_api_exchange_log}\n")

# nonullos=df_bd_api_exchange['maxSupply'].isnull().sum()
# print(nonullos)


df_clean = df_bd_api_exchange.drop_duplicates()
log_step(f"Duplicados eliminados. Nueva forma:\n{df_clean.shape}\n")



numeric_columns = ['roi', 'roi.times', 'roi.currency','roi.percentage']
log_step(f"Creando el array con las columnas que van a convertirse a numéricas: \n{numeric_columns}\n")

for column in numeric_columns:
    df_clean[column] = pd.to_numeric(df_clean[column], errors='coerce')
log_step("convertiendo las columnas a numéricas\n")

df_clean_log = get_output_txt(df_clean, 'info')
log_step(f"información de DataFrame con las columnas convertidas a numéricas: \n{df_clean_log}\n")
df_clean_end = df_clean


log_step(f"DataFrame final creada con forma: \n{df_clean_end.shape}\n")

df_clean_end['name'] = df_clean_end['name'].str.lower()
log_step("convertiendo la columna name a minusculas\n")

df_clean_end['symbol'] = df_clean_end['symbol'].str.upper()
log_step("convirtiendo la columna name a mayúsculas\n")


log_step("Llenando valores nulos\n")
df_clean_end = df_clean.fillna({
    'roi': 0, 
    'roi.times': 0, 
    'roi.currency': 0,
    'roi.percentage': 0,
    'max_supply': 0
    
})




df_clean_log_end = get_output_txt(df_clean_end, 'info')
log_step(f"DataFrameb despues de eliminar  elementos son nulos: \n{df_clean_log_end}\n")



create_file(df_clean_end, 'src/static/cleaned_data/cleaned_data.csv', file_format='csv')
log_step("Archivo CSV generado\n")

create_file(df_clean_end,'src/static/cleaned_data/cleaned_data.xlsx', file_format='xlsx')
log_step("Archivo Excel generado\n")


create_table(conn, table_clean, df_clean_end)
log_step(f"Tabla de limpieza creada: \n{table_clean}\n")