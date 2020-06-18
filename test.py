from bs4 import BeautifulSoup as bs
import requests
import re
url = 'https://euroauto.ru/part/used/30187637/'
MAIN_CARD_URL = 'https://euroauto.ru'





response = requests.get(url)
soup = bs(response.content, 'html.parser')
container = soup.find_all('div', class_='col-md-4 col-lg-4')[1]
# for div in container:
#     if div.find('label').text == 'Вес:':
#         weight = div.text.strip()
#         white_clear = re.search(r'[0-9.,]+', weight)[0]
# print(white_clear)

for div in container:
    label = div.find('label')
    if type(label) != int:
        try:
            if label.text == 'Вес:':
                print(div.text)
        except:
            pass