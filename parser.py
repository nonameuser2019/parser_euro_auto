from bs4 import BeautifulSoup as bs
import requests
from user_agent import generate_user_agent
import time
import random
import re
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from model import *
from user_agent import generate_user_agent
import re
import os
import csv

cat_url_list = []
error_count = 0
db_engine = create_engine("sqlite:///euroauto.db", echo=True)
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'euroauto.db')
MAIN_CARD_URL = 'https://euroauto.ru'
HEADERS = {
    'User-Agent': generate_user_agent(device_type="desktop", os=('mac', 'linux')),
}
#proxy = {'HTTPS': '157.245.138.230:8118'}
global weight


def get_html(url):
    while True:
        HEADERS.update({'User-Agent': generate_user_agent(device_type="desktop", os=('mac', 'linux'))})
        #time.sleep(random.randint(random.randint(6, 10), random.randint(12, 27)))
        response = requests.get(url, headers=HEADERS)
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
            print(response.url)
            continue



def read_input():
    url_list = []
    with open('input.txt', 'r') as r:
        for row in r:
            url_list.append(r.readline())
    return url_list


def get_page_count(response):
    soup = bs(response.content, 'html.parser')
    try:
        page_count = soup.find('ul', class_='pagination pagination-sm').find_all('li')[-2].find('a').text
    except:
        page_count = 1
    return int(page_count)


def get_list_url():
    result = []
    cat_url = ['https://euroauto.ru/zapchasti/tormoznaya_sistema/tsilindr_tormoznoy_glavniy/',
               'https://euroauto.ru/zapchasti/tormoznaya_sistema/usilitel_tormozov_vakuumniy/',
               'https://euroauto.ru/zapchasti/tormoznaya_sistema/support_tormoznoy_zadniy_praviy/',
               'https://euroauto.ru/zapchasti/tormoznaya_sistema/support_tormoznoy_zadniy_leviy/',
               'https://euroauto.ru/zapchasti/tormoznaya_sistema/pilnik_tormoznogo_diska/',
                'https://euroauto.ru/zapchasti/tormoznaya_sistema/richag_stoyanochnogo_tormoza/'
               ]


    for url in cat_url:
        #print(url)
        page_count = get_page_count(get_html(url))
        print(page_count)
        for i in range(1, page_count + 1):
            response = get_html(url + '?page=' + str(i))
            soup = bs(response.content, 'html.parser')
            card_list = soup.find_all('div', class_='snippet-card fx-box')
            for card in card_list:
                href = card.find('a', class_='lightweight-item-desc')['href']
                full_url = MAIN_CARD_URL + href
                print(full_url)
                result.append(full_url)
        return result


def sub_category_parser(response):
    #функция которая парсит все подкатегории и записывает в файл
    soup = bs(response.content, 'html.parser')
    all_category = soup.find_all('div', class_='zapchasti-category')
    for category in all_category:
        cat_name = category.find('div', class_='zapchasti-category-title').text
        sub_cat_list = category.find_all('li', class_='zapchasti-category-list-item')
        for sub_cat in sub_cat_list:
            sub_cat_name = sub_cat.find('a').text.split('\n')[0]
            sub_cat_url = MAIN_CARD_URL + sub_cat.find('a')['href']
            count = sub_cat.find('a').find('span').text.strip()
            if not count:
                count = 0
            cat_url_list.append([cat_name, sub_cat_name, sub_cat_url, count])


def write_result(cat_url_list):
    try:
        with open('out.csv', 'w', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=';')
            writer.writerow(('Основная кат.', 'Под кат.', 'Ссылка', 'Количество'))
            for url in cat_url_list:
                writer.writerow([*url])
            print('Файл успешно записан')
    except PermissionError:
        print('Закрой нахуй файл out.csv иначе нихуя не запишу :)')


def parser_card(response):
    soup = bs(response.content, 'html.parser')
    container = soup.find_all('div', class_='col-md-4 col-lg-4')[1]
    try:
        name = container.find('a').find('span')['data-product-title'].strip()
    except:
        name = None
    try:
        article = container.find('a').text.strip()
    except:
        article = None
    try:
        brand = container.find_all('div')[2].find('a').text
    except:
        brand = None

    for div in container:
        label = div.find('label')
        if type(label) != int:
            try:
                if label.text == 'Вес:':
                    weight = div.text
            except:
                pass

    # из за того что верстка в разных категориях разная сделал новый код для парсинга веса, этот пока не нужен
    # try:
    #     weight = container.find_all('div')[4].text.strip()
    #     white_clear = re.search(r'[0-9.,]+', weight)[0]
    # except:
    #   white_clear = None
    try:
        weight_clear = re.search(r'[0-9.]+', weight)[0]
    except:
        weight_clear = 0

    url = response.url
    Session = sessionmaker(bind=db_engine)
    session = Session()
    new_element = EuroAuto(name, article, brand, weight_clear, url)
    session.add(new_element)
    session.commit()




def main():
    card_list = get_list_url()
    for url in card_list:
        response = get_html(url)
        parser_card(response)





if __name__ == '__main__':
    main()