from bs4 import BeautifulSoup as bs
import requests

url = 'https://euroauto.ru/zapchasti/dvigatel/absorber_filtr_ugolniy/?page='
MAIN_CARD_URL = 'https://euroauto.ru'




for i in range(1, 57):
    response = requests.get(url + str(i))
    soup = bs(response.content, 'html.parser')
    card_list = soup.find_all('div', class_='snippet-card fx-box')
    print(response.status_code)
    for card in card_list:
        href = card.find('a', class_='lightweight-item-desc desc-item--link')['href']
        print(MAIN_CARD_URL + href)


