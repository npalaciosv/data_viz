from utils.Scraping_primary_pages import main_scraper
from utils.Scraping_secondary_pages import individual_scraper
import pandas as pd

# Iniciamos nuestra clase main_scraper para poder traer la informacio de las paginas principales.
scraper = main_scraper(url='https://carros.tucarro.com.co/',brand='ford')

# Definimos cuantas paginas principales vamos a scrapear
paginas = scraper.paginas_a_scrapear(page_num=5)  # Cambiar a la cantidad de páginas que deseas scrapear

# Ejecutamos la funcion que extrae los datos y la almacenamos en un dataframe - la funcion, por defecto, devuelve un dataframe
df_resultado = scraper.scraping_principal(paginas=paginas)

# Verificamos el numero de registros que trae la extraccion
print(df_resultado.count())

# Quitamos aquellas filas que vienen vacias y guardamos los resultados a un archivo CSV que vamos a utilizar posteriormente
df_resultado.dropna().to_csv('Results_main_pages.csv', index=False, encoding='utf-8',sep=';')

# Tomamos todos los links particulares que se extrajeron para hacer el scraping secundario
links = df_resultado['link'].dropna().tolist()

# Creamos un dataframe vacio donde vamos a almacenar la nueva extraccion
df = pd.DataFrame()

# Definimos un counter que nos dira cuantas paginas se van a scrapear en total
counter = len(links)

# Ejecutamos la funcion scraping individual para cada link
for link in links:
    print(f'Quedan {counter} paginas por scrapear')
    counter -= 1
    scraper = individual_scraper(link)
    
    # Almacenamis la informacion extraida en un dataframe temporal
    df_temp = scraper.scraping_individual()
    
    # Unimos la la extraccion con la informacion anterior
    df = pd.concat([df,df_temp], ignore_index=True)

# Enviamos los datos a un archivo CSV
df.to_csv('Results_secondary_pages.csv', index=False, encoding='utf-8',sep=';')

# Mostramos la informacion generada para terminos de chequeo
print(df)