from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import re
import logging

def run(driver, quartos):
    driver.get("https://www.evandroproencaimoveis.com.br/imobiliaria/locacao/guaratingueta-sp/casa-casa/" + str(quartos) +"-quartos-ou-mais/imoveis/7423")

    results = driver.find_elements(By.CSS_SELECTOR, 'article')
    
    houses = []
    new_cached = []

    with open('cache/evandro', 'r') as file:
        cached = file.read().splitlines()                
        file.close()

    for result in results:
        strip = []

        try:
            strip = result.find_elements(By.CSS_SELECTOR, '[class*=strip]')
        except Exception as e:
            logging.error(f'Imóvel da imobiliária Evandro Proença falhou capturando strip')
            continue

        if (strip == []):
            href = None

            try:
                href = result.find_element(By.TAG_NAME, 'header').get_attribute('onclick')
                href = re.search(r"open\('(.+?)'", href)
                href = href.group(1)

            except Exception as e:
                logging.error(f'Imóvel da imobiliária Evandro Proença falhou capturando href')
                continue

            new_cached.append('\n'+href)

            new = False
            if href not in cached:
                new = True

            image = None
            try:
                image = result.find_element(By.CSS_SELECTOR, '.carousel-item.active img').get_attribute('src')

            except Exception as e:
                logging.error(f'Imóvel da imobiliária Evandro Proença falhou capturando imagem')
                continue

            value = None

            try:
                value = result.find_element(By.CSS_SELECTOR, '[class*=property-card_rent-price]').text
            except Exception as e:
                logging.error(f'Imóvel da imobiliária Evandro Proença falhou capturando valor')
                continue

            location = None

            try:
                location = result.find_element(By.CSS_SELECTOR, '[class*=property-card_address]').text
            except Exception as e:
                logging.error(f'Imóvel da imobiliária Evandro Proença falhou capturando location')
                continue

            houses.append({
                "href": href,
                "value": '' if value == None else value,
                "image": image,
                "location": '' if location == None else location,
                "new": new
            })
    
    file = open('cache/evandro', 'w')
    file.writelines(new_cached)
    file.close()

    return houses