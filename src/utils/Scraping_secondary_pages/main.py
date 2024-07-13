from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import json
import time

class individual_scraper():

    def __init__(self, pag_secundaria, timeout = 10):
        self.pag_secundaria = pag_secundaria
        self.timeout = timeout

    def scraping_individual(self):
        html_text = requests.get(self.pag_secundaria)

        status_code = html_text.status_code
        try:
            html_text = requests.get(self.pag_secundaria, timeout=self.timeout)
            status_code = html_text.status_code
            time.sleep(3)
            if status_code == 200:
                conexion_url = html_text.url
                soup = BeautifulSoup(html_text.text, 'lxml')

                # Buscar todas las etiquetas <div>
                list_features = []
                script = soup.find('script', type='application/ld+json')

                # Extraer el contenido del script como texto
                script_content = script.text.strip()

                # Convertir el contenido del script a un objeto JSON
                data = json.loads(script_content)

                features_1 = list(data['offers'].keys())
                features_2 = list(data.keys())
                features_2 = [item for item in features_2 if item != 'offers']
                features = features_1 + features_2

                values_1 = list(data['offers'].values())
                values_2 = [value for key, value in data.items() if key != 'offers']
                values = values_1 + values_2

                df = pd.DataFrame(
                                    {
                                        'Caracteristicas':features,
                                        'Valores': values
                                    }
                                )

                df['Registro'] = pd.Timestamp.now()
                df['Origen_individual'] = conexion_url
                Key = df[df['Caracteristicas']=='productID']['Valores'].values[0]
                df['Key'] = Key
                index_to_delete = df[df['Caracteristicas'] == 'productID'].index
                df = df.drop(index_to_delete)
                df = df.reset_index(drop=True)
            return df

        except requests.exceptions.RequestException as e:
            print(f"Error al hacer la solicitud HTTP: {e}")

if __name__ == "__main__":
    url_provisional = 'https://articulo.tucarro.com.co/MCO-1451550515-ford-explorer-_JM#position%3D1%26search_layout%3Dgrid%26type%3Ditem%26tracking_id%3Df96ec29f-690d-46e5-a630-13b2492a1fd9'
    scraper_individual = individual_scraper(url_provisional, timeout=10)

    # Obtener las páginas a scrapear
    detail = scraper_individual.scraping_individual()