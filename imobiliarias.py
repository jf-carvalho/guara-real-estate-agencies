from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import argparse
import scripts_imobiliarias.wanor as wanor
import scripts_imobiliarias.rony as rony
import scripts_imobiliarias.i3a as i3a
import scripts_imobiliarias.habit as habit
import scripts_imobiliarias.ferri as ferri
import scripts_imobiliarias.oliveira as oliveira
import scripts_imobiliarias.ativa as ativa
import scripts_imobiliarias.evandro as evandro
import scripts_imobiliarias.villa as villa
import scripts_imobiliarias.castro_santos as castro_santos
import scripts_imobiliarias.olimpo as olimpo
import output
import time

def run(quartos):
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_experimental_option("detach", False)

    driver = webdriver.Chrome(options=chrome_options)

    items = {
        "wanor": wanor,
        "rony": rony,
        "3a": i3a,
        "habit": habit,
        "ferri lorigio": ferri,
        "oliveira alves": oliveira,
        "ativa": ativa,
        "evandro proença": evandro,
        "villa": villa,
        "castro_santos": castro_santos,
        "olimpo": olimpo,
    }

    l = len(items)

    houses = {}

    for i, (item_name, item) in enumerate(items.items()):
        printProgressBar(i, l, prefix = 'Running ' + item_name + ': ', suffix = '', length = 50)

        houses[item_name] = item.run(driver, quartos)
        time.sleep(0.1)

    output.build(houses)

    printProgressBar(i + 1, l, prefix = '', suffix = 'Completed', length = 50)

    driver.quit()

    print('\n\033[32mAll done!\033[0m\n')

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)

    percent = percent + '%'
    print(f'\r{prefix} |{bar}| {percent} {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

if(__name__ == "__main__"):
    parser = argparse.ArgumentParser()
    parser.add_argument('--quartos')
    args = parser.parse_args()
    quartos_value = args.quartos

    if quartos_value == None:
        quartos_value = 2

    run(quartos_value)