from bs4 import BeautifulSoup as bs
import requests
from user_agent import generate_user_agent
import time
import random


MAIN_CARD_URL = 'https://euroauto.ru'
HEADERS = {
    'User-Agent': generate_user_agent(device_type="desktop", os=('mac', 'linux')),
}
proxy = {'HTTPS': '157.245.138.230:8118'}
card_list = []
cat_url = 'https://euroauto.ru/zapchasti/dvigatel/absorber_filtr_ugolniy/?page='

def get_html(url):
    while True:
        HEADERS.update({'User-Agent': generate_user_agent(device_type="desktop", os=('mac', 'linux'))})
        #time.sleep(random.randint(random.randint(6, 10), random.randint(12, 27)))
        response = requests.get(url, headers=HEADERS, proxies=proxy)
        if response.status_code == 200:
            print(response.status_code)
            return response
        elif response.status_code == 403:
            print(response.status_code)
            print('weit to 600 sec')
            HEADERS.update({'User-Agent': generate_user_agent(device_type="desktop", os=('mac', 'linux'))})
            time.sleep(random.randint(600,800))
        else:
            time.sleep(random.randint(14, 27))
            print(response.status_code)
            continue


def get_page_count(response):
    soup = bs(response.content, 'html.parser')
    page_count = soup.find('ul', class_='pagination pagination-sm').find_all('li')[-2].find('a').text
    return int(page_count)


def get_list_url(response):
    soup = bs(response.content, 'html.parser')
    card_list = soup.find_all('div', class_='snippet-card fx-box')
    for card in card_list:
        href = card.find('a', class_='lightweight-item-desc desc-item--link')['href']
        print(href)
        card_list.append(MAIN_CARD_URL + href)


def main():
    page_count = get_page_count(get_html('https://euroauto.ru/zapchasti/dvigatel/absorber_filtr_ugolniy/?page=1'))
    for i in range(1, page_count + 1):
        print(cat_url + str(i))
        #get_list_url(get_html(cat_url + str(i)))



if __name__ == '__main__':
    main()