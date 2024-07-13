from utils.Scraping_primary_pages import main_scraper
from utils.Scraping_secondary_pages import individual_scraper
import pandas as pd

# Crear una instancia de la clase
scraper = main_scraper(url='https://carros.tucarro.com.co/',brand='ford')

# Obtener las páginas a scrapear
paginas = scraper.paginas_a_scrapear(page_num=5)  # Cambiar a la cantidad de páginas que deseas scrapear

# Ejecutar el scraping y obtener el DataFrame resultante
df_resultado = scraper.scraping_principal(paginas=paginas)

# Mostrar el DataFrame resultante
print(df_resultado.count())

# Enviarmos los resultados a un archivo Excel que vamos a utilizar posteriormente
df_resultado.dropna().to_csv('Results_main_pages.csv', index=False, encoding='utf-8',sep=';')

links = df_resultado['link'].dropna().tolist()

df = pd.DataFrame()
counter = len(links)

for link in links:
    print(f'Quedan {counter} paginas por scrapear')
    counter -= 1
    scraper = individual_scraper(link)
    df_temp = scraper.scraping_individual()
    df = pd.concat([df,df_temp], ignore_index=True)

df.to_csv('Results_secondary_pages.csv', index=False, encoding='utf-8',sep=';')
print(df)