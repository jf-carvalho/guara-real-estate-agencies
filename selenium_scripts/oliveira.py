from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

def run(driver, quartos):
    driver.get("https://imobiliariaoliveiraalves.com/imoveis-locacao.php?tipo%5B%5D=Casa&cidade=GUARATINGUETA&codigo_imovel=&area_minima=&area_maxima=&valor_minimo=1200&valor_maximo=1800&qtd_quartos=" + str(quartos) + "&qtd_suites=&qtd_vagas=")

    repeat = True

    while repeat:

        results = driver.find_elements(By.CSS_SELECTOR, '.item-wrap')

        houses = []
        new_cached = []

        with open('cache/oliveira', 'r') as file:
            cached = file.read().splitlines()                
            file.close()

        for result in results:
            anchor = result.find_element(By.CSS_SELECTOR, 'a')

            href = anchor.get_attribute('href')

            image = anchor.value_of_css_property('background')
            image = re.search(r"url\((.+?)\)", image).group(1).replace('"', '')

            location = result.find_element(By.CSS_SELECTOR, '.property-title').text
            index_of_no_bairro = location.find("no bairro")
            location = location[index_of_no_bairro + len("no bairro"):].lstrip()

            new_cached.append('\n'+href)

            new = False
            if href not in cached:
                new = True

            houses.append({
                "href": href,
                "image": image,
                "value": result.find_element(By.CSS_SELECTOR, '.price.hide-on-list').text,
                "location": location,
                "new": new
            })

            try:
                xpath_expression = f"//a[@aria-label='Next']"
                next_button = driver.find_element_by_xpath(xpath_expression)

                WebDriverWait(driver, 1).until(
                    EC.element_to_be_clickable(next_button)
                )

                driver.execute_script("arguments[0].click();", next_button)

            except Exception as e:
                repeat = False
    
    file = open('cache/oliveira', 'w')
    file.writelines(new_cached)
    file.close()

    return houses