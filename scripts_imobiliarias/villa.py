from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
import locale
import time
import logging

logging.basicConfig(filename='log.log', level=logging.INFO)
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def run(driver, quartos):
    driver.get("https://villaimoveis.com/encontre-seu-imovel/jsf/jet-engine:resultados/tax/property_action_category:678/")

    casa_checkbox = driver.find_element(By.CSS_SELECTOR, 'input[name="property_category"][value="714"]')
    casa_label = casa_checkbox.find_element(By.XPATH, '..')
    casa_label.click()

    advanced = driver.find_element(By.CSS_SELECTOR, '.jet-toggle__label-text')
    advanced.click()

    quartos_value = driver.find_element(By.CSS_SELECTOR, 'input[type="range"][aria-label="Minimal value"]')
    driver.execute_script(f"arguments[0].value = {quartos};", quartos_value)
    time.sleep(2)

    houses = []
    new_cached = []

    with open('cache/villa', 'r') as file:
        cached = file.read().splitlines()                
        file.close()

    repeat = True

    while repeat:
        time.sleep(2)
        results = driver.find_elements(By.XPATH, '//*[@data-url]')

        for result in results:
            href = result.get_attribute('data-url')
            
            value = result.find_element(By.CSS_SELECTOR, '.elementor-element.elementor-element-ce1e766.elementor-widget.elementor-widget-jet-listing-dynamic-field')
            
            value_string = value.text

            if (value_string == 'CONSULTARR$ 0,00'):
                continue
            
            value_float = float(value_string.replace('R$ ', '').replace('.', '').replace(',', '.'))
            
            if(value_float < 1200 or value_float > 1800):
                continue

            image = result.find_element(By.CSS_SELECTOR, '.elementor-image img').get_attribute('src')
            
            location = driver.find_element(By.CSS_SELECTOR, '.elementor-element.elementor-element-b6ba0b7.elementor-widget__width-auto.elementor-widget.elementor-widget-jet-listing-dynamic-terms')
            
            location = location.text.replace(',', '')

            new_cached.append('\n'+href)

            new = False
            if href not in cached:
                new = True

            house = {
                "href": href,
                "value": value_string,
                "image": image,
                "location": location,
                "new": new
            }

            houses.append(house)

        try:
            next_button = WebDriverWait(driver, 5).until(
                expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".jet-filters-pagination__item.prev-next.next"))
            )
        except Exception as e:
            repeat = False
            continue

        try:
            driver.execute_script("arguments[0].click();", next_button)
        except Exception as e:
            repeat = False
            continue


    file = open('cache/villa', 'w')
    file.writelines(new_cached)
    file.close()

    return houses