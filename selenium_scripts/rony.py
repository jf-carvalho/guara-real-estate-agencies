from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run(driver, quartos):
    driver.get("https://www.rony.com.br/aluguel/casa/guaratingueta/todos-os-bairros/" + str(quartos) + "-quartos/0-suite-ou-mais/0-vaga-ou-mais/0-banheiro-ou-mais/sem-portaria-24horas/sem-area-lazer/sem-dce/sem-mobilia/sem-area-privativa/sem-area-servico/sem-box-despejo/sem-circuito-tv/?valorminimo=1.200,00&valormaximo=1.800,00&pagina=1")         

    repeat = True

    while(repeat):
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".page-link"))
            )
        except Exception as e:
            print(str(e))

        results = driver.find_elements(By.CSS_SELECTOR, ".card-imovel")

        houses = []
        new_cached = []

        with open('cache/rony', 'w+') as file:
            cached = file.read().splitlines()                
            file.close()

        for result in results:
            location = result.find_element(By.CSS_SELECTOR, 'a h5').text
            parts = location.split(',')
            location = parts[-1]

            href = result.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')

            new_cached.append('\n'+href)

            new = False
            if href not in cached:
                new = True

            houses.append({
                "href": href,
                "location": location,
                "image": result.find_element(By.CSS_SELECTOR, 'img').get_attribute('src'),
                "value": result.find_element(By.CSS_SELECTOR, '.text-center.caracteristicas-card-imoveis.my-auto').text,
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
            if "background-color: var(--cor-primaria)" in element.get_attribute("style"):
                selected_index = index
                break

        last_item_index = len(page_items) - 1

        if selected_index == last_item_index - 2:
            repeat = False
        else:
            page_items[last_item_index - 1].click()

    file = open('cache/rony', 'w')
    file.writelines(new_cached)
    file.close()
    
    return houses

if(__name__ == "__main__"):
    run()