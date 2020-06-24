from bs4 import BeautifulSoup as bs
import requests
import re
import csv
url = 'https://euroauto.ru/zapchasti/'
MAIN_CARD_URL = 'https://euroauto.ru'


def read_input():
    cat_url_list = []
    with open('input.txt', 'r') as r:
        for row in r:
            cat_url_list.append(r.readline().strip('\n'))
    return cat_url_list

cat_url_list = read_input()
print(cat_url_list)


