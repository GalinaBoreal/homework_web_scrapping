# Поиск вакансий по заданным параметрам
## В рамках домашнего задания «Web-scrapping»

Попробуем получать интересующие вакансии на сайте [headhunter](https://spb.hh.ru/).

Реализовано:
1. Необходимо парсить страницу со свежими вакансиями с поиском по "Python" и городами "Москва" и "Санкт-Петербург". Эти параметры задаются по [ссылке](https://spb.hh.ru/search/vacancy?text=python&area=1&area=2)
2. Нужно выбрать те вакансии, у которых в описании есть ключевые слова "Django" и "Flask".
3. Записать в json информацию о каждой вакансии - ссылка, вилка зп, название компании, город.  

 

Функции на Python для поиска вакансий:

- get_headers() - Получеение заголовка для имитация действий пользователя в браузере
- get_html(url) - Получение HTML-кода из указанной ссылки
- get_links_from_page(html_data) - Получение пакета ссылок на вакансии с одной страницы
- get_all_pages(url) - Получение всех ссылок на вакансии со всех страниц
- read_vacancy(url) - Выборка вакансий по ключевым словам Django и Flask, подготовка словаря для записи в json - файл
- result_in_json(url) - Запись полученного результата в файл

Изучить результат: read_json.py