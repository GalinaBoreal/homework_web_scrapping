import time
import sys
import json

import requests
import bs4
from fake_headers import Headers


def get_headers():
    """Получеение заголовка для имитация действий пользователя в браузере"""
    return Headers(browser="firefox", os="win").generate()


def get_html(url):
    """Получение HTML-кода из указанной ссылки"""
    headers = get_headers()
    html_data = requests.get(url=url, headers=headers)
    print('Получение HTML-кода из ', url)
    return html_data


def get_links_from_page(html_data):
    """Получение пакета ссылок на вакансии с одной страницы"""
    all_vacancy = []

    soup = bs4.BeautifulSoup(html_data, "lxml")
    span_teg = soup.find_all("a", class_="serp-item__title")
    for description in span_teg:
        try:
            link = description.get('href')
            all_vacancy.append(link)
        except Exception:
            error = sys.exc_info()[1]
            print(f'Ошибка: {error.args[0]}')
    return all_vacancy


def get_all_pages(url):
    """Получеение всех ссылок на вакансии со всех страниц"""
    all_links = []
    page = 0
    page_is_empty = True

    while page_is_empty:
        url_page = '&page='
        url_base = url + url_page + str(page)
        html_data = get_html(url_base)
        if html_data.status_code != 200:
            print('Страницы закончились')
            page_is_empty = False
        else:
            time.sleep(.5)
            html_data = html_data.text
            try:
                links = get_links_from_page(html_data)
                all_links = all_links+links
            except Exception:
                error = sys.exc_info()[1]
                print(f'Ошибка: {error.args[0]}')
            finally:
                page += 1

    return all_links


def read_vacancy(url):
    """Выборка вакансий по ключевым словам Django и Flask,
    подготовка словаря для записи в json - файл"""
    all_vacancy = {'vacancies': []}

    links = get_all_pages(url)
    for link in links:
        try:
            html_data = get_html(link).text
            soup = bs4.BeautifulSoup(html_data, "lxml")

            desc_teg = soup.find(attrs={"data-qa": "vacancy-description"})
            pay_teg = soup.find(attrs={"data-qa": "vacancy-salary-compensation-type-net"})
            city_teg = soup.find(attrs={"data-qa": "vacancy-view-location"})
            company_teg = soup.find(attrs={"data-qa": "bloko-header-2"})

            description = desc_teg.text
            if 'Django' in description and 'Flask' in description:

                if pay_teg is not None:
                    pay = pay_teg.text
                    pay = pay.replace("\xa0", " ")
                else:
                    pay = ""

                if city_teg is not None:
                    city = city_teg.text
                else:
                    city = ""

                if company_teg is not None:
                    company = company_teg.text
                    company = company.replace("\xa0", " ")
                else:
                    company = ""

                all_vacancy['vacancies'].append({
                    "link": link,
                    "salary": pay,
                    "company": company,
                    "city": city
                })

        except Exception:
            error = sys.exc_info()[1]
            print(f'Что то пошло не так с просмотром этой вакансии: {link}. Ошибка: {error.args[0]}')


    return all_vacancy


def result_in_json(url):
    """Запись полученного результата в файл """
    data = read_vacancy(url)
    data_json = json.dumps(data, ensure_ascii=False)

    with open("vacancies.json", "w", encoding='utf-8') as my_file:
        my_file.write(data_json)


if __name__ == "__main__":
    url = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
    result_in_json(url)


