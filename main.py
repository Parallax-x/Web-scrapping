import requests
import bs4
import fake_headers
import json
import time
from unicodedata import normalize

# main class="vacancy-serp-content" - список вакансий
# div data-qa="vacancy-serp__results" - список вакансий
# div class="serp-item" - каждая вакансия
# h3 data-qa="bloko-header-3" - ссылка
# span data-page-analytics-event="vacancy_search_suitable_item" - ссылка
# a class="serp-item__title" - ссылка
# span data-qa="vacancy-serp__vacancy-compensation" - зп
# div class="vacancy-serp-item__meta-info-company" - название компании
# div class="bloko-text" - город
# div "g-user-content" - описание

headers = fake_headers.Headers(browser='chrome', os='win')
url = ('https://spb.hh.ru/search/vacancy?text=python+django+flask&from=suggest_post&salary=&ored_clusters=true&area=1&'
       'area=2')
response = requests.get(url, headers=headers.generate())
main_html = response.text

main_soup = bs4.BeautifulSoup(main_html, 'lxml')

div_vacancy_list_tag = main_soup.find('main', class_='vacancy-serp-content')

vacancy_tags = div_vacancy_list_tag.find_all('div', class_='serp-item')

parsed_data = []
for vacancy_tag in vacancy_tags:
    time.sleep(0.1)
    link_tag = vacancy_tag.find('a', class_='serp-item__title')
    link = link_tag['href']
    zp_tag = vacancy_tag.find('span', class_='bloko-header-section-2')
    company_name_tag = vacancy_tag.find('div', class_='vacancy-serp-item__meta-info-company')
    company_name = normalize('NFKD', company_name_tag.text)
    city_tag = vacancy_tag.find(attrs={'data-qa': 'vacancy-serp__vacancy-address'})
    city = city_tag.text.split(',')[0]
    if zp_tag is not None:
        parsed_data.append({'link': link,
                            'salary': normalize('NFKD', zp_tag.text),
                            'company name': company_name,
                            'city': city})
    else:
        parsed_data.append({'link': link,
                            'salary': 'Не указана',
                            'company name': company_name,
                            'city': city})

with open('vacancy.json', 'w', encoding='utf-8') as f:
    json.dump(parsed_data, f, indent=2, ensure_ascii=False)
