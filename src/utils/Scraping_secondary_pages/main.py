from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import json
import time

class individual_scraper():

    def __init__(self, pag_secundarias, timeout = 10):
        self.pag_secundarias = pag_secundarias
        self.timeout = timeout

    def scraping_individual(self):
        df_final = pd.DataFrame()
        counter = len(self.pag_secundarias)
        for pag_secundaria in self.pag_secundarias:
            print(f'Quedan {counter} paginas por scrapear')
            counter -= 1
            try:
                html_text = requests.get(pag_secundaria, timeout=self.timeout)
                status_code = html_text.status_code
                time.sleep(3)
                if status_code == 200:
                    conexion_url = html_text.url
                    soup = BeautifulSoup(html_text.text, 'lxml')

                    # Buscamos en elemento script dentro del bloque del html
                    script = soup.find('script', type='application/ld+json')

                    # Extraer el contenido del script como texto
                    script_content = script.text.strip()

                    # Convertir el contenido del script a un objeto JSON
                    data = json.loads(script_content)

                    # Extramos a una lista las llaves del objeto JSON unicamente para el atributo offers
                    features_ONLY_offers = list(data['offers'].keys())

                    # Extramos a una lista las llaves del objeto JSON para todos los atributos diferentes a offers
                    features_NO_offers = list(data.keys())
                    features_NO_offers = [item for item in features_NO_offers if item != 'offers']

                    #Unimos ambas listas
                    features = features_ONLY_offers + features_NO_offers

                    # Extramos a una lista los valores del objeto JSON unicamente para el atributo offers
                    values_ONLY_offers = list(data['offers'].values())

                    # Extramos a una lista los valores del objeto JSON para todos los atributos diferentes a offers
                    values_NO_offers = [value for key, value in data.items() if key != 'offers']

                    #Unimos ambas listas
                    values = values_ONLY_offers + values_NO_offers

                    # Creamos un diccionario que una las listas
                    data_dict = {str(feature): value for feature, value in zip(features, values)}

                    # Creamos un dataframe con el diccionario previamente definido. Index = [0] hace que las caracteristicas se conviertan en el nombre de las columnas
                    df = pd.DataFrame(data_dict, index=[0])

                    # Creamos una columna que almacene el registro de tiempo cuando se estan haciendo las transacciones
                    df['Registro'] = pd.Timestamp.now()

                    # Creamos una columna que almacene la url de donde estamos trayendo la informacion
                    df['Origen_individual'] = conexion_url

                    # Se agrega la informacion de la extraccion a la historia
                    df_final = pd.concat([df_final,df], ignore_index=True)

            except requests.exceptions.RequestException as e:
                print(f"Error al hacer la solicitud HTTP: {e}")

        return df_final

if __name__ == "__main__":
    url_provisional = 'https://articulo.tucarro.com.co/MCO-1451550515-ford-explorer-_JM#position%3D1%26search_layout%3Dgrid%26type%3Ditem%26tracking_id%3Df96ec29f-690d-46e5-a630-13b2492a1fd9'
    scraper_individual = individual_scraper(url_provisional, timeout=10)

    # Obtener las páginas a scrapear
    detail = scraper_individual.scraping_individual()