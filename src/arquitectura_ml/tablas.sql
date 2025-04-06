 Tabla: api_exchange (Datos brutos de la API)
 

Campo	Tipo de dato	Descripción

id	                TEXT    (PK)	Identificador único de la criptomoneda (ej: bitcoin).
symbol	            TEXT	Símbolo (ej: BTC).
name	            TEXT	Nombre completo (ej: Bitcoin).
current_price	    REAL	Precio en USD.
market_cap	        REAL	Capitalización de mercado.
total_volume	    REAL	Volumen de operaciones (24h).
high_24h	        REAL	Precio máximo (24h).
low_24h	            REAL	Precio mínimo (24h).
price_change_24h	REAL	Variación de precio (24h).
last_updated	    TEXT	Fecha de última actualización.
roi	                REAL	Retorno de inversión (ROI).
max_supply	        REAL	Suministro máximo.


Tabla: api_clean (Datos normalizados)

Campo	Tipo de dato	Transformaciones aplicadas

id	        TEXT (PK)	Conservado.
symbol	    TEXT	Convertido a mayúsculas (ej: BTC).
name	    TEXT	Convertido a minúsculas (ej: bitcoin).
roi     	REAL	Valores nulos reemplazados por 0.
max_supply	REAL	Valores nulos reemplazados por 0.


Tabla: info_exchange (Metadatos - bd_info.sqlite)

Campo	Tipo de dato	Descripción

id	                TEXT (PK)	Clave foránea a api_clean.id.
symbol	            TEXT	Símbolo de la moneda.
image	            TEXT	URL del logo.
circulating_supply	REAL	Suministro circulante.
total_supply	    REAL	Suministro total.
ath_date	        TEXT	Fecha del precio histórico máximo.

Tabla: market_exchange (Datos de mercado - bd_market.sqlite)

Campo	Tipo de dato	Descripción

id	                        TEXT (PK)	Clave foránea a api_clean.id.
symbol	                    TEXT	Símbolo.
market_cap_rank	            INTEGER	Ranking por capitalización.
fully_diluted_valuation	    REAL	Valuación diluida.
price_change_percentage_24h	REAL	Cambio porcentual (24h).
last_updated	            TEXT	Fecha de actualización.

