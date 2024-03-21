from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys

def run(driver, quartos):
    driver.get("https://imobiliariahabit.com.br/casa/para-alugar/guaratingueta-sp?preco-minimo=1200&preco-maximo=1800&quartos[]=" + str(quartos) + "&ordernar-por=preco-decrescente")  

    repeat = True

    while repeat:
        results = driver.find_elements(By.CSS_SELECTOR, "div[data-search-results=''] >div")

        houses = []
        new_cached = []

        with open('cache/habit', 'w+') as file:
            cached = file.read().splitlines()                
            file.close()

        for result in results:
            href = result.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')

            new_cached.append('\n'+href)

            new = False
            if href not in cached:
                new = True

            houses.append({
                "href": href,
                "location": result.find_element(By.CSS_SELECTOR, '.property_card_address').text,
                "image": result.find_element(By.CSS_SELECTOR, 'picture img').get_attribute('src'),
                "value": result.find_element(By.CSS_SELECTOR, '.property_pricing').text,
                "new": new
            })

        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".page-link"))
            )
        
        except Exception as e:
                repeat = False

        page_items = driver.find_elements(By.CSS_SELECTOR, '.page-link')

        selected_index = -1

        for index, element in enumerate(page_items):
            if "active" in element.get_attribute('class').split():
                selected_index = index
                break

        last_item_index = len(page_items) - 1

        if selected_index == last_item_index - 1:
            repeat = False
        else:
            page_items[last_item_index - 1].click()
    
    file = open('cache/habit', 'w')
    file.writelines(new_cached)
    file.close()

    return houses