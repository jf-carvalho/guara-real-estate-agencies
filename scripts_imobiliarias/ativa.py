from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run(driver, quartos):
    driver.get("https://ativaimoveis.com.br/search?bairros%5B%5D=Guaratinguet%C3%A1&tipo%5B%5D=6&preco_min=1200.00&preco_max=1800.00&dormitorio=" + str(quartos) + "&suite=&banheiro=&metro_min=0.00&metro_max=10000.00")

    repeat = True

    houses = []
    new_cached = []

    with open('cache/ativa', 'r') as file:
        cached = file.read().splitlines()                
        file.close()

    while repeat:

        results = driver.find_elements(By.CSS_SELECTOR, '.saiba-mais')

        for result in results:

            parent_element = result.find_element(By.XPATH, '..')
            image = parent_element.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')
    
            href = result.get_attribute('href')
            
            new_cached.append('\n'+href)

            new = False
            if href not in cached:
                new = True

            house = {
                "href": href,
                "value": '',
                "image": image,
                "location": parent_element.find_element(By.CSS_SELECTOR, '.principal >p strong').text,
                "new": new
            }

            houses.append(house)

        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'li.page-item'))
            )

            page_links = driver.find_elements(By.CSS_SELECTOR, 'li.page-item')
            print(page_links)

            if ('disabled' in page_links[-1].get_attribute('class').split()):
                repeat = False

        except Exception as e:
            repeat = False

    file = open('cache/ativa', 'w')
    file.writelines(new_cached)
    file.close()

    return houses