from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run(driver, quartos):
    driver.get("https://www.imobiliaria3a.com/imoveis/para-alugar/casa/guaratingueta?quartos=" + str(quartos) + "+&preco-de-locacao=1200~1800")         

    repeat = True

    while repeat:
        try:
            WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".pagination-cell button"))
            )

            pagination_button = driver.find_element(By.CSS_SELECTOR, ".pagination-cell button")            
            driver.execute_script("arguments[0].click();", pagination_button)

        except Exception as e:
            repeat = False

    results = driver.find_elements(By.CSS_SELECTOR, ".listing-results a")

    houses = []
    new_cached = []

    with open('cache/3a', 'r') as file:
        cached = file.read().splitlines()                
        file.close()

    for result in results:
        value_titles = result.find_elements(By.CSS_SELECTOR, ".card-with-buttons__value-title")

        for value_title in value_titles:
            if 'Locação' == value_title.text:
                value = value_title.find_element(By.XPATH, 'following-sibling::p').text
                break

        href = result.get_attribute('href')

        image = result.find_element(By.CSS_SELECTOR, 'img');
        location = result.find_element(By.CSS_SELECTOR, '.card-with-buttons__heading');

        new_cached.append('\n'+href)

        new = False
        if href not in cached:
            new = True

        house = {
            "href": href,
            "value": value,
            "image": image.get_attribute('src'),
            "location": location.text,
            "new": new
        }

        houses.append(house)

    file = open('cache/3a', 'w')
    file.writelines(new_cached)
    file.close()

    return houses

if(__name__ == "__main__"):
    run()