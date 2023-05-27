import requests
from bs4 import BeautifulSoup
from request_get_json_data_spell import get_json_data_spell

# URL страницы со списком заклинаний
url = 'https://dnd.su/spells/'

try:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
except:
    print('Failed to retrieve page')
    exit()

# Находим основной контейнер
container = soup.find('div', {'class': 'paper-1 card'})

# Проверяем, что контейнер найден
if container:
    # Находим контейнер с карточками
    card_wrapper = container.find('div', {'class': 'card-wrapper'})

    # Проверяем, что контейнер с карточками найден
    if card_wrapper:
        # Находим список карточек
        card_list = card_wrapper.find('ul', {'class': 'cards-list'})

        # Проверяем, что список карточек найден
        if card_list:
            # Находим все элементы карточек
            card_items = card_list.find_all('li', {'class': 'cards_list__item'})

            # Проходимся по каждому элементу карточки
            for card_item in card_items:
                # Находим ссылку на заклинание
                spell_link = card_item.find('a', {'class': 'cards_list__item-wrapper'})

                # Проверяем, что ссылка найдена
                if spell_link:
                    spell_url = 'https://dnd.su' + spell_link['href']

                    # Вызываем метод для обработки каждого заклинания
                    get_json_data_spell(spell_url)
        else:
            print('Card list not found')
    else:
        print('Card wrapper not found')
else:
    print('Container not found')
