import os
import time
import getpass
import numpy as np
import pandas as pd
from tqdm import tqdm
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

start = time.time()

delays = [0.5, 1.5, 2, 2.1, 2.6,]
delay = int(np.random.choice(delays))

url               = 'https://instagram.com'
email             = input('Defina uma conta: ')
password          = getpass.getpass('Senha: ')
publication_list  = ['https://www.instagram.com/p/B9zw_1hJmxW/', 'https://www.instagram.com/p/B9xZ6BzBeuN/']

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--ignore-ssl-errors=yes')
chrome_options.add_argument('--ignore-certificate-errors')
browser = webdriver.Chrome('chromedriver', chrome_options=chrome_options)
browser.get(url)

emailInput = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.NAME,  'username')))
passwordInput = browser.find_element(By.NAME, 'password')

emailInput.send_keys(email)
time.sleep(delay)
passwordInput.send_keys(password)

button = browser.find_element(By.XPATH, '//button[@class = "sqdOP  L3NKy   y3zKF     "]').click()

buttonpu = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.XPATH, '//button[@class = "aOOlW   HoLwm "]' ))).click()

comment_list = list()
users_list   = list()
data_list    = list()

for publication in tqdm(publication_list):
    browser.get(publication)

    contador = 0
    while(contador <= 100):
        try:
            loading_button = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//button[@class = "dCJp8 afkep"]'))).click()
            time.sleep(delay)
        except:
            contador = 101

    comments_publication = list()
    comments = browser.find_elements_by_xpath('//div[@class = "C4VMK"]/span')
    for comment in comments:
        comment = comment.text
        comments_publication.append(comment)

    comments_publication.pop(0)
    for comment in comments_publication:
        comment_list.append(comment)

    usernames_publication = list()
    users = browser.find_elements(By.XPATH, '//h3[@class = "_6lAjh "]')
    for user in users:
        user = user.text
        usernames_publication.append(user)
    for user in usernames_publication:
        users_list.append(user)

    data_publication = list()
    data_comments = browser.find_elements(By.XPATH, '//time[@class = "FH9sR Nzb55"]')
    for data in data_comments:
        data = data.get_attribute('datetime')
        data_publication.append(data)
    data_publication.pop(0)
    for data in data_publication:
        data_list.append(data)

    time.sleep(delay)

end = time.time()

base = {'username':users_list, 'comentario':comment_list, 'data_comentario':data_list}
df = pd.DataFrame(base)
print(df)
tamanho = len(df)
print(f'{tamanho} dados extraídos em {start - end} segundos')

df.to_csv ('tabataamaral_instagram_database', index = False, sep='\t')

browser.quit()
