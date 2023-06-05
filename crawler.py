import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json
import hashlib

url = "http://192.168.50.131:3000/#/"

wordlist_path = "directory-list-2.3-small.txt"

service = Service("chromedriver.exe")
options = webdriver.ChromeOptions()
# options.add_argument("--silent-launch")

# capabilities = DesiredCapabilities.CHROME.copy()
# capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}


driver = webdriver.Chrome(service=service, options=options)  # desired_capabilities=capabilities
import requests

driver.get("http://192.168.50.131:3000/#/login")
name = driver.find_element(By.ID, "email")
name.send_keys('a@a.com')
time.sleep(3)
passw = driver.find_element(By.ID, "password")
passw.send_keys('123123')
time.sleep(3)
login = driver.find_element(By.ID, "loginButton")
login.click()
print("LOGIN FEITO!")

hashes = []

with open(wordlist_path, 'r') as wordlist_file:
    # Lê cada linha da wordlist
    for linha in wordlist_file:
        diretorio = linha.strip()  # Remove espaços em branco e quebras de linha
        full_url = url + diretorio
        # print('testando',full_url)
        driver.get(full_url)
        # logs = driver.get_log('browser')
        # print(logs)
        # response = requests.get(full_url)
        content = driver.page_source.encode('utf-8')
        page_hash = hashlib.md5(content).hexdigest()

        if page_hash in hashes:
            # print("Página duplicada encontrada:", url)
            pass
        else:
            hashes.append(page_hash)

            element1 = driver.find_elements(By.TAG_NAME, "input")
            element2 = driver.find_elements(By.TAG_NAME, "textarea")

            if element1:
                # print(element)
                print(full_url)
                # print('[+] Campos encontrados:')
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
