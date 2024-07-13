from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import time

class main_scraper():

    def __init__(self, url, brand = None ,timeout=10000):
        self.url = url
        self.timeout = timeout
        self.brand = brand

    def paginas_a_scrapear(self, page_num):
        paginas = {}
        if self.brand == None:
            for i in range(1,page_num+1):
                if i == 1:
                    paginas[str(i)] = f'{self.url}_NoIndex_True'
                else:
                    paginas[str(i)] = f'{self.url}_Desde_{48*(i-1)+1}_NoIndex_True'
            return paginas
        else:
            for i in range(1,page_num+1):
                if i == 1:
                    paginas[str(i)] = f'{self.url}{self.brand}/_NoIndex_True'
                else:
                    paginas[str(i)] = f'{self.url}{self.brand}/_Desde_{48*(i-1)+1}_NoIndex_True'
            return paginas

    def scraping_principal(self, paginas):
        df_final = pd.DataFrame()
        for pagina in paginas.values():
            try:
                html_text = requests.get(pagina, timeout=self.timeout)
                status_code = html_text.status_code
                print(f'Pagina {pagina} fue leida')
                time.sleep(9)
                if status_code == 200:
                    conexion_url = html_text.url
                    soup = BeautifulSoup(html_text.text, 'lxml')
                    cars_grill = soup.find('ol', class_ = 'ui-search-layout ui-search-layout--grid')
                    cars = cars_grill.find_all('li', class_ = 'ui-search-layout__item')
                    df = pd.DataFrame()

                    car_name_list = []
                    price_car_list = []
                    model_car_list = []
                    km_car_list = []
                    location_car_list = []
                    links_car_list = []

                    for car in cars:
                        car_name = car.find('img', alt = True)
                        pattern = r'<img[^>]*alt="([^"]*)"'
                        car_name_adjusted = re.findall(pattern, str(car_name))
                        car_name_list.append(car_name_adjusted)
                    df = pd.DataFrame(car_name_list, columns=['Nombre_del_vehiculo'])

                    for car in cars:
                        price_car = car.find('span', class_ = 'andes-money-amount ui-search-price__part ui-search-price__part--medium andes-money-amount--cents-superscript')
                        pattern = r'aria-label="(\d+)'
                        price_car_adjusted = re.findall(pattern, str(price_car))
                        try:
                            price_car_adjusted = int(price_car_adjusted[0]) if price_car_adjusted else None
                        except (ValueError, IndexError):
                            price_car_adjusted = None
                        price_car_list.append(price_car_adjusted)
                    df['Precio_del_vehiculo'] = price_car_list

                    for car in cars:
                        # Inicializamos los valores en None
                        model_car = None
                        km_car = None
                        try:
                            # Extraemos el modelo del carro
                            model_car = int(car.find_all('li', class_='ui-search-card-attributes__attribute')[0].text)
                            # Extraemos el kilometraje del carro
                            km_car = car.find_all('li', class_='ui-search-card-attributes__attribute')[1].text
                            km_car = int(km_car.replace(" Km", "").replace(".", ""))
                        except (ValueError, IndexError):
                            pass
                        model_car_list.append(model_car)
                        km_car_list.append(km_car)
                    df['Modelo_del_vehiculo'] = model_car_list
                    df['Kilometraje_del_vehiculo'] = km_car_list

                    for car in cars:
                        location_car = None
                        try:
                            location_car = car.find('span', class_='ui-search-item__group__element ui-search-item__location').text
                        except (AttributeError, ValueError):
                            pass
                        location_car_list.append(location_car)
                    df['Ubicacion_del_vehiculo'] = location_car_list

                    for car in cars:
                        link_car = None
                        try:
                            link_car = car.find('a', class_='ui-search-link')['href']
                        except (TypeError, KeyError, AttributeError):
                            pass
                        links_car_list.append(link_car)
                    df['link'] = links_car_list

                    df['Marca_del_vehiculo'] = df['Nombre_del_vehiculo'].str.split(" ").str[0]

                    df['Registro_pagina_principal'] = pd.Timestamp.now()
                    df['origen_general'] = conexion_url

                    def extract_mco_code(url):
                        pattern = r'MCO-\d+'
                        match = re.search(pattern, url)
                        if match:
                            return match.group()
                        else:
                            return None

                    if link_car != None:
                        df['Key'] = df['link'].apply(extract_mco_code)
                    else:
                        df['Key'] = None

                    df_final = pd.concat([df_final,df], ignore_index=True)

                else:
                    print(f"No se ha podido establecer conexión con la página:{pagina}")
            except requests.exceptions.RequestException as e:
                print(f"Error al hacer la solicitud HTTP: {e}")

        print(df_final.count())
        return df_final

# Ejemplo de uso en el archivo principal
if __name__ == "__main__":
    # Crear una instancia de la clase
    scraper = main_scraper('https://carros.tucarro.com.co/', timeout=10000)

    # Obtener las páginas a scrapear
    paginas = scraper.paginas_a_scrapear(10)  # Cambiar a la cantidad de páginas que deseas scrapear

    # Ejecutar el scraping y obtener el DataFrame resultante
    df_resultado = scraper.scraping_principal(paginas)