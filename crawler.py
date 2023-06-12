import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json
import hashlib
import requests

url = "http://192.168.50.131:3000/#/" #Endereço do alvo hospedado localmente.


wordlist_path = "directory-list-2.3-small.txt" #Diretório utilizado para crawling. Disponível em: https://github.com/daviddias/node-dirbuster/blob/master/lists/directory-list-2.3-small.txt

service = Service("chromedriver.exe")
options = webdriver.ChromeOptions()
# options.add_argument("--silent-launch")

driver = webdriver.Chrome(service=service, options=options)  


driver.get("http://192.168.50.131:3000/#/login")
name = driver.find_element(By.ID, "email")
#A conta de usuário a@a.com e senha 123123 foi criada previamente.
name.send_keys('a@a.com')  
time.sleep(3)
passw = driver.find_element(By.ID, "password")
passw.send_keys('123123')
time.sleep(3)
login = driver.find_element(By.ID, "loginButton")
login.click()
print("LOGIN FEITO!")

hashes = []

#O acesso de subdiretórios e cliques em botões que levam para outras páginas não são suportados pelo Crawler implementado.
with open(wordlist_path, 'r') as wordlist_file:
    for linha in wordlist_file:
        diretorio = linha.strip() 
        full_url = url + diretorio
        driver.get(full_url)
        content = driver.page_source.encode('utf-8')
        page_hash = hashlib.md5(content).hexdigest()

        if page_hash in hashes: #Evita páginas duplicadas através da comparação de valores hash.
            pass
        else:
            hashes.append(page_hash)
            #A geração de casos de teste está embasado na técnica de fuzzing, a qual baseia-se em strings, logo, não buscando por botões, por exemplo.
            element1 = driver.find_elements(By.TAG_NAME, "input")
            element2 = driver.find_elements(By.TAG_NAME, "textarea")

            if element1:
                print(full_url)
                print('[+] Campos encontrados:')
                for i in element1:
                    if i.get_property("type") == "checkbox":
                        pass
                    else:
                        time.sleep(1)
                        print(i.get_property("id"))
            if element2:
                for j in element2:
                    if j.get_property("type") == "checkbox":
                        pass
                    else:
                        time.sleep(1)
                        print(i.get_property("id"))

            time.sleep(2)

driver.quit()
