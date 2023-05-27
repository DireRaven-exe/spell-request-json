import requests
import json
from bs4 import BeautifulSoup
import re

def get_json_data_spell(url):
    print("ok")
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
    except:
        print('Failed to retrieve page')
        exit()

    element = soup.find('h2', class_='card-title')
    if element:
        name_element = element.find('span', {'data-copy': True})
        if name_element:
            name = name_element.text.strip()
            print(name)
        else:
            print('Name element not found')
    else:
        print('Title element not found')


    level_and_school = soup.find('li', {'class': 'size-type-alignment'}).text.strip()
    match = re.search(r'^([^,]+)(?:,\s+(.*))?$', level_and_school)
    if match:
        level = match.group(1).strip()
        school = match.group(2).strip() if match.group(2) else ""
        if level == 'Заговор':
            level = 'Заговор'
        elif 'уровень' in level:
            level = level.replace(' уровень', 'й уровень')
    else:
        level = level_and_school.strip()
        school = ""

    level_int = int(re.search(r'\d+', level).group()) if level != 'Заговор' else 0

    ritual = ''
    casting_time = ''
    range_ = ''
    components = ''
    duration = ''
    description = ''
    higher_level = ''
    material = ''
    classes = ''
    archetypes = ''

    if ' (ритуал)' in school:
        school = school.replace(' (ритуал)', '')
        ritual = 'да'
    else:
        ritual = 'нет'
    school = re.sub(r'\([^)]*\)', '', school)
    school = school.replace(' ', '')

    params_list = soup.find('div', {'class': 'card-body'}).find_all('li')
    for param in params_list:
        param_text = param.text.strip()
        if 'Время накладывания:' in param_text:
            casting_time = param_text.replace('Время накладывания:', '').strip()
        elif 'Дистанция:' in param_text:
            range_ = param_text.replace('Дистанция:', '').strip()
        elif 'Компоненты:' in param_text:
            components = param_text.replace('Компоненты:', '').strip()
            # Проверка наличия скобок в components и перенос текста из скобок в material
            if '(' in components and ')' in components:
                start_index = components.find('(')
                end_index = components.find(')')
                material = components[start_index + 1:end_index]
                components = components[:start_index] + components[end_index + 1:].strip()
                components = components.rstrip()
        elif 'Длительность:' in param_text:
            duration = param_text.replace('Длительность:', '').strip()
        elif 'Классы:' in param_text:
            classes = param_text.replace('Классы:', '').strip()
            classes = ', '.join([c.strip().capitalize().replace('tce', '') for c in classes.split(',')])
        elif 'Архетипы:' in param_text:
            archetypes = param_text.replace('Архетипы:', '').strip()

    description = soup.find('div', {'itemprop': 'description'}).text.strip()

    # Проверка наличия текста "На больших уровнях" в описании и перенос в переменную "higher_level"
    if 'На больших уровнях' in description:
        description_parts = description.split('На больших уровнях', 1)
        description = description_parts[0].strip()
        higher_level = description_parts[1].strip()
        higher_level = higher_level[2:]  # Удаление первые два символа

    # Обработка slug
    slug = url.replace('https://dnd.su/spells/', '')
    for i, char in enumerate(slug):
        if char.isalpha():
            slug = slug[i:]
            break
    slug = slug.replace('_', '-')
    slug = slug.rstrip('/')

    # Очистка name
    name = re.sub(r'\[.*?\]', '', name).strip()

    # Создание словаря с данными
    spell_data = {
        "slug": slug,
        "name": name,
        "desc": description,
        "higher_level": higher_level,
        "range": range_,
        "components": components,
        "material": material,
        "ritual": ritual,
        "duration": duration,
        "casting_time": casting_time,
        "level": level,
        "level_int": level_int,
        "school": school,
        "dnd_class": classes,
        "archetype": archetypes,
        "circles": "",
        "document__slug": "wotc-srd",
        "document__title": "Systems Reference Document",
        "document__license_url": "https://open5e.com/legal"
    }

    # Преобразование в JSON
    # открыть файл JSON и загрузить его содержимое
    with open('spells.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Получить список 'results' из данных
    results = data['results']

    # Добавить полученный объект в список 'results'
    results.append(spell_data)

    # Записать обновленные данные обратно в файл JSON
    with open('spells.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    # Вывод объекта на экран
    print(json.dumps(spell_data, ensure_ascii=False, indent=4))
