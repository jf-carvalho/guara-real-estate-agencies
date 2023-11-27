from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import locale
import sys

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def run(driver, quartos):
    driver.get("https://villaimoveis.com/encontre-seu-imovel/jsf/jet-engine:resultados/tax/property_action_category:678/")

    casa_checkbox = driver.find_element(By.CSS_SELECTOR, 'input[name="property_category"][value="714"]')
    casa_label = casa_checkbox.find_element(By.XPATH, '..')
    casa_label.click()

    quartos_value = driver.find_element(By.CSS_SELECTOR, 'input[type="range"][aria-label="Minimal value"]')
    driver.execute_script(f"arguments[0].value = {quartos};", quartos_value)

    driver.implicitly_wait(5)

    repeat = True

    while repeat:
        results = driver.find_elements(By.XPATH, '//*[@data-url]')

        houses = []
        new_cached = []

        with open('cache/villa', 'r') as file:
            cached = file.read().splitlines()                
            file.close()

        for result in results:
            href = result.get_attribute('data-url')
            
            try:
                WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable(result.find_element(By.CSS_SELECTOR, '.elementor-element.elementor-element-ce1e766.elementor-widget.elementor-widget-jet-listing-dynamic-field'))
                )
            
            except Exception as e:
                print('erro: 41')
                sys.exit()
            
            value = result.find_element(By.CSS_SELECTOR, '.elementor-element.elementor-element-ce1e766.elementor-widget.elementor-widget-jet-listing-dynamic-field')
            value_string = value.text
            print(value_string)

            if (value_string == 'CONSULTARR$ 0,00'):
                continue
            
            value_float = float(value_string.replace('R$ ', '').replace('.', '').replace(',', '.'))
            
            if(value_float < 1200 or value_float > 1800):
                continue

            try:
                image = result.find_element(By.CSS_SELECTOR, '.elementor-image img')
                WebDriverWait(driver, 4).until(
                    EC.visibility_of(image)
                )

                image = result.find_element(By.CSS_SELECTOR, '.elementor-image img').get_attribute('src')
            except Exception as e:
                continue

            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located(result.find_element(By.CSS_SELECTOR, '.elementor-element.elementor-element-b6ba0b7.elementor-widget__width-auto.elementor-widget.elementor-widget-jet-listing-dynamic-terms'))
                )
            
            except Exception as e:
                continue
            
            location = result.find_element(By.CSS_SELECTOR, '.elementor-element.elementor-element-b6ba0b7.elementor-widget__width-auto.elementor-widget.elementor-widget-jet-listing-dynamic-terms')
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
            WebDriverWait(driver, 4).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".jet-filters-pagination__item.prev-next.next"))
            )
        except Exception as e:
            repeat = False
            continue

        next_button = driver.find_element(By.CSS_SELECTOR, ".jet-filters-pagination__item.prev-next.next")
        driver.execute_script("arguments[0].click();", next_button)

    file = open('cache/villa', 'w')
    file.writelines(new_cached)
    file.close()

    return houses