from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run(driver, quartos):
    driver.get("https://ferriloriggio.com.br/imoveis-locacao.php?busca=&codigo_imovel=&negociacao=Aluguel&situacao=&cidade=GUARATINGUETA&area_minima=&area_maxima=&valor_minimo=1200&valor_maximo=1800&qtd_quartos=" + str(quartos) + "&qtd_banheiros=&qtd_vagas=&tipo=Casa")

    repeat = True

    while repeat:
        try:
            WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".carregar-mais"))
            )

            pagination_button = driver.find_element(By.CSS_SELECTOR, ".carregar-mais")      

            qtt_results = len(driver.find_elements(By.CSS_SELECTOR, '#conteudo .removePedDiv'))

            driver.execute_script("arguments[0].click();", pagination_button)

            new_qtt_results = len(driver.find_elements(By.CSS_SELECTOR, '#conteudo .removePedDiv'))
             
            if new_qtt_results == qtt_results:
                repeat = False

        except Exception as e:
            repeat = False

    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "p.text-muted a"))
    )

    results = driver.find_elements(By.CSS_SELECTOR, '#conteudo .removePedDiv')

    houses = []
    new_cached = []

    with open('cache/ferri', 'w+') as file:
        cached = file.read().splitlines()                
        file.close()

    for result in results:
        image = result.find_element(By.CSS_SELECTOR, '.imagem img').get_attribute('src')
        
        location = result.find_element(By.CSS_SELECTOR, 'p.text-muted a').text
        index_of_no_bairro = location.find("no bairro")
        location = location[index_of_no_bairro + len("no bairro"):].lstrip()

        if (image != 'https://ferriloriggio.com.br/images/nao-disponivel.jpg'):
            href = result.find_element(By.CSS_SELECTOR, 'a.imagem').get_attribute('href')

            new_cached.append('\n'+href)

            new = False
            if href not in cached:
                new = True

            houses.append({
                "href": href,
                "image": image,
                "location": location,
                "value": result.find_element(By.CSS_SELECTOR, 'strong').text,
                "new": new
            })

    file = open('cache/ferri', 'w')
    file.writelines(new_cached)
    file.close()

    return houses    
