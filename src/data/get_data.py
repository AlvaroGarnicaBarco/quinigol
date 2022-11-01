import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


class ProbsScraper:
    def __init__(self, driver_path='/Users/Alvaro/Documents/Drivers/chromedriver'):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        self.driver = webdriver.Chrome(service=Service(driver_path), options=options)
        self.driver.get('https://www.eduardolosilla.es/quinigol/ayudas/orden')
        
    def cambiar_tabla(self, jornada, tipo_prob):
        tipo_probs_map = {'EL': 0, 'real': 1, 'LAE': 2}
        filtros = self.driver.find_elements(By.TAG_NAME, 'app-selector')
        tipo_probs = filtros[0]
        jornadas = filtros[1]        
        tipo_probs.find_element(By.XPATH, f"//option[@title='{tipo_probs_map[tipo_prob]}']").click()
        jornadas.find_element(By.XPATH, f"//option[@title='{jornada}']").click()
        
    def extraer_datos(self):
        # time.sleep(0.5)
        soup = BeautifulSoup(self.driver.page_source)
        base = soup.find('body').find('app-orden-quinigol').find('div', {'c-listado-orden__datos__tabla-porcentajes'})
        partidos = base.find_all('div', {'class': 'c-tabla-porcentajes-quinigol__datos u-clearfix ng-star-inserted'})
        my_dict = {
            'partido': [],
            'local_0': [], 'visitante_0': [],
            'local_1': [], 'visitante_1': [],
            'local_2': [], 'visitante_2': [],
            'local_M': [], 'visitante_M': []
        }
        for partido in partidos:
            lista_valores = partido.text.replace(' ', '').split()[1:]
            my_dict['partido'].append(lista_valores[0] + '-' + lista_valores[1])
            my_dict['local_0'].append(lista_valores[2])
            my_dict['visitante_0'].append(lista_valores[3])
            my_dict['local_1'].append(lista_valores[4])
            my_dict['visitante_1'].append(lista_valores[5])
            my_dict['local_2'].append(lista_valores[6])
            my_dict['visitante_2'].append(lista_valores[7])
            my_dict['local_M'].append(lista_valores[8])
            my_dict['visitante_M'].append(lista_valores[9])
        
        return pd.DataFrame(my_dict)
    
    def quit(self):
        self.driver.quit()
        