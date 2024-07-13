from utils import main_scraper

# Crear una instancia de la clase
scraper = main_scraper(url='https://carros.tucarro.com.co/',brand='ford')

# Obtener las páginas a scrapear
paginas = scraper.paginas_a_scrapear(page_num=30)  # Cambiar a la cantidad de páginas que deseas scrapear

# Ejecutar el scraping y obtener el DataFrame resultante
df_resultado = scraper.scraping_principal(paginas=paginas)

# Mostrar el DataFrame resultante
print(df_resultado.count())

df_resultado.to_excel('Results.xlsx', index=False)