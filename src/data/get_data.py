import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from itertools import product


class ProbsScraper:
    def __init__(self, driver_path='/Users/Alvaro/Documents/Drivers/chromedriver'):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        self.driver = webdriver.Chrome(service=Service(driver_path), options=options)
        self.driver.get('https://www.eduardolosilla.es/quinigol/ayudas/orden')
        time.sleep(1)

    def cambiar_tabla(self, jornada, tipo_prob):
        tipo_probs_map = {'EL': 0, 'real': 1, 'LAE': 2}
        filtros = self.driver.find_elements(By.TAG_NAME, 'app-selector')
        tipo_probs = filtros[0]
        jornadas = filtros[1]
        tipo_probs.find_element(By.XPATH, f"//option[@title='{tipo_probs_map[tipo_prob]}']").click()
        jornadas.find_element(By.XPATH, f"//option[@title='{jornada}']").click()

    def extraer_datos(self):
        time.sleep(1)
        soup = BeautifulSoup(self.driver.page_source, 'xml')
        base = soup.find('body').find('app-orden-quinigol').find('div', {'c-listado-orden__datos__tabla-porcentajes'})
        partidos = base.find_all('div', {'class': 'c-tabla-porcentajes-quinigol__datos u-clearfix ng-star-inserted'})
        # se saca la tabla con las probabilidades brutas de marcar 0, 1, 2, M para cada equipo
        probs_brutas = {}
        for partido in partidos:
            lista_valores = partido.text.replace(' ', '').split()[1:]
            probs_brutas[lista_valores[0] + '-' + lista_valores[1]] = {'local': [int(lista_valores[2]),
                                                                                 int(lista_valores[4]),
                                                                                 int(lista_valores[6]),
                                                                                 int(lista_valores[8])],
                                                                       'visitante': [int(lista_valores[3]),
                                                                                     int(lista_valores[5]),
                                                                                     int(lista_valores[7]),
                                                                                     int(lista_valores[9])]}
        # se calcula la probabilidad de cada uno de los 16 resultados posibles
        resultados = ['-'.join(i) for i in product("012M", repeat=2)]
        probs_finales = {}
        for partido in probs_brutas:
            probs_finales[partido] = {}
            for resultado, porcentajes in zip(resultados, product(probs_brutas[partido]['local'],
                                                                  probs_brutas[partido]['visitante'])):
                probs_finales[partido][resultado] = round(porcentajes[0] / 100 * porcentajes[1] / 100, 4)

        return pd.DataFrame(probs_finales).T

    def quit(self):
        self.driver.quit()


def get_prob_tables(jornada):
    my_scraper = ProbsScraper()

    my_scraper.cambiar_tabla(jornada=f'{jornada}', tipo_prob='EL')
    el = my_scraper.extraer_datos()

    my_scraper.cambiar_tabla(jornada=f'{jornada}', tipo_prob='LAE')
    lae = my_scraper.extraer_datos()

    my_scraper.cambiar_tabla(jornada=f'{jornada}', tipo_prob='real')
    real = my_scraper.extraer_datos()

    my_scraper.quit()

    estimado = el*0.1 + lae*0.9

    return real, estimado
