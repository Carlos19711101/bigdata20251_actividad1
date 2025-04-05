# transformation.py
import pandas as pd
import os
import logging
from dotenv import load_dotenv
from api.base import fetch_data_from_api
from static.db.config import create_connection, create_table
from utils.helpers import create_file, audit_data

load_dotenv()

# Configuración de logging
logging.basicConfig(
    filename='src/static/audit/enrichment_report.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

columns_info = [
    "id", "symbol", "name", "image",
    "circulating_supply", "total_supply", "max_supply",
    "ath", "ath_date", "atl", "atl_date"
]

columns_market = [
    "id", "symbol", "current_price", "market_cap", "market_cap_rank",
    "fully_diluted_valuation", "total_volume", "high_24h", "low_24h",
    "price_change_24h", "price_change_percentage_24h",
    "market_cap_change_24h", "market_cap_change_percentage_24h",
    "ath_change_percentage", "atl_change_percentage", "last_updated"
]

def main():
    logging.info("==============================================")
    logging.info("INICIO DEL PROCESO DE TRANSFORMACIÓN")
    logging.info("==============================================")

    api_url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false'
    data = fetch_data_from_api(api_url)
    df_api = pd.json_normalize(data)

    logging.info(f"Registros obtenidos de la API: {len(df_api)}")
    
    audit_data(df_api)
    create_file(df_api, 'src/static/xlsx/request_api_xlsx.xlsx', file_format='xlsx')

    enriched_df = _create_alternative_databases(df_api)
    
    _safe_export(enriched_df)
    
    logging.info("==============================================")
    logging.info("PROCESO FINALIZADO CON ÉXITO")
    logging.info("==============================================")

def _create_alternative_databases(df_api):
    logging.info("Creando bases de datos especializadas...")
    
    # Crear bases de datos
    conn_info = create_connection('bd_info.sqlite')
    df_info = _prepare_data(df_api[columns_info].copy())
    create_table(conn_info, 'info_exchange', df_info)
    
    conn_market = create_connection('bd_market.sqlite')
    df_market = _prepare_data(df_api[columns_market].copy())
    create_table(conn_market, 'market_exchange', df_market)

    # Unir y procesar datos
    return _process_and_merge_data(df_info, df_market)

def _prepare_data(df):
    """Preprocesamiento común para todas las bases de datos"""
    logging.info("Preprocesando datos...")
    # Convertir listas a strings
    df = df.map(lambda x: ', '.join(x) if isinstance(x, list) else x)
    # Eliminar timezones
    return _normalize_data(df)

def _process_and_merge_data(df_info, df_market):
    logging.info("Realizando unión de datos...")
    # Normalización avanzada
    df_info = _normalize_data(df_info)
    df_market = _normalize_data(df_market)

    # Validación pre-merge
    _validate_merge_conditions(df_info, df_market)

    # Unión con clave compuesta
    merged_df = pd.merge(
        df_info,
        df_market,
        on=['id', 'symbol'],
        how='inner',
        validate='one_to_one'
    )

    # Transformaciones finales
    return _apply_transformations(merged_df)

def _normalize_data(df):
    """Normalización de datos"""
    logging.info("Normalizando datos...")
    # Normalización de columnas
    df.columns = df.columns.str.lower()
    
    # Conversión segura de fechas
    date_cols = [col for col in df.columns if '_date' in col or 'last_updated' in col]
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce').dt.tz_localize(None)
    
    # Tipo de datos consistente
    numeric_cols = df.select_dtypes(include=['object']).columns
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='ignore')
    
    return df

def _validate_merge_conditions(df1, df2):
    """Garantiza consistencia para el merge"""
    logging.info("Validando condiciones de unión...")
    if not df1[['id', 'symbol']].equals(df2[['id', 'symbol']]):
        raise ValueError("Las claves de merge no coinciden")
    if len(df1) != len(df2):
        raise ValueError("Los dataframes tienen diferente longitud")

def _apply_transformations(df):
    """Transformaciones avanzadas"""
    logging.info("Aplicando transformaciones...")
    # Cálculo de métricas
    df['total_valuation'] = df['current_price'] * df['total_supply']
    df['market_dominance'] = df['market_cap'] / df['market_cap'].sum()
    
    # Normalización de porcentajes
    pct_cols = [col for col in df.columns if 'percentage' in col]
    df[pct_cols] = df[pct_cols].apply(lambda x: x / 100)
    
    # Formato consistente
    df['symbol'] = df['symbol'].str.upper()
    
    return df.drop_duplicates(subset=['id', 'symbol'])

def _safe_export(df):
    """Exportación segura a Excel/CSV"""
    logging.info("Exportando datos enriquecidos...")
    # Conversión final de fechas a strings
    date_cols = df.select_dtypes(include=['datetime64[ns]']).columns
    df[date_cols] = df[date_cols].apply(lambda x: x.dt.strftime('%Y-%m-%d %H:%M:%S'))
    
    # Exportación múltiple
    create_file(
        df.sample(min(100, len(df))),
        'src/static/xlsx/enriched_data.xlsx',
        file_format='xlsx'
    )
    create_file(
        df,
        'src/static/csv/enriched_data.csv',
        file_format='csv'
    )

if __name__ == '__main__':
    main()


