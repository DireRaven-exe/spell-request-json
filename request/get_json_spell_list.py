from playwright.sync_api import sync_playwright
from request_get_json_data_spell import get_json_data_spell
import re

# URL страницы со списком заклинаний
url = 'https://dnd.su/spells/'
# Создаем список для хранения ссылок на заклинания
spell_urls = []

with sync_playwright() as playwright:
    browser = playwright.chromium.launch()
    page = browser.new_page()
    page.goto(url)
    spell_links = page.query_selector_all('.cards_list__item-wrapper')
    for link in spell_links:
        spell_url = link.get_attribute('href')
        spell_urls.append(spell_url)
        print(spell_url)
    browser.close()


# Обрабатываем каждую ссылку на заклинание
for spell_url in spell_urls:
    spell_url = 'https://dnd.su/' + spell_url
    get_json_data_spell(spell_url)
