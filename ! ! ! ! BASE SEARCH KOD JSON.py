import urllib.parse

# Создаем базовый URL для поиска автомобилей на Avito
base_url = 'https://www.avito.ru/js/catalog?'
base_url3 = 'https://www.avito.ru/?'
# Создаем словарь с параметрами запроса

# 'categoryId': '101',
# 'categoryId': '',
# 'locationId': '0',
# 'locationId': '652000',

params = {
    'categoryId': '101',
    'params[price][from]': '3000', #json
    'params[price][to]': '8000', #json
    #'priceMin': '3000', #HTML
    #'priceMax': '8000', #HTML
    'q': 'E-MU 1616'
}
#'query': 'E-MU 1616'
# Кодируем параметры запроса и добавляем их к базовому URL
if 'locationId' not in params:
    base_url3 = 'https://www.avito.ru/all/?'
    #base_url = 'https://www.avito.ru/js/catalog?'

encoded_params = urllib.parse.urlencode(params)
search_url = base_url + encoded_params

print(search_url) #открываем в браузере полученый адрес

'''

Адрес https://www.avito.ru/js/catalog представляет собой URL-адрес, по которому можно получить данные каталога с использованием JavaScript. Этот адрес является частью API Avito, который предоставляет доступ к различным функциям и данным платформы.

В дополнение к https://www.avito.ru/js/catalog, существует несколько других возможностей для получения данных с помощью API Avito:

1. https://www.avito.ru/api/1/items: URL-адрес для получения данных о товарах или объявлениях на Avito.
2. https://www.avito.ru/api/9/items: URL-адрес для получения данных о транспортных средствах на Avito (автомобили, мотоциклы и т. д.).
3. https://www.avito.ru/api/2/items: URL-адрес для получения данных о недвижимости на Avito (квартиры, дома, земельные участки и т. д.).
4. https://www.avito.ru/api/3/items: URL-адрес для получения данных о услугах на Avito.

Каждый из этих URL-адресов предоставляет доступ к определенной категории данных на Avito, и вы можете использовать их в своих запросах для получения соответствующих результатов.

Важно отметить, что доступ к данным через API Avito может быть ограничен и требовать авторизации или использования API-ключа. Для получения более подробной информации о возможностях и условиях использования API Avito, рекомендуется обратиться к официальной документации Avito или связаться с их службой поддержки.


5. https://www.avito.ru/api/1/personal/items: URL-адрес для получения данных о товарах или объявлениях из личного кабинета пользователя на Avito.
6. https://www.avito.ru/api/2/personal/items: URL-адрес для получения данных о недвижимости из личного кабинета пользователя на Avito.
7. https://www.avito.ru/api/3/personal/items: URL-адрес для получения данных о услугах из личного кабинета пользователя на Avito.
8. https://www.avito.ru/api/1/profile/accounts: URL-адрес для получения данных об учетной записи пользователя на Avito.
9. https://www.avito.ru/api/1/profile/ads: URL-адрес для получения данных об объявлениях пользователя на Avito.
10. https://www.avito.ru/api/2/categories: URL-адрес для получения данных о категориях товаров и услуг на Avito.
11. https://www.avito.ru/api/2/geo/address: URL-адрес для получения данных о географических адресах на Avito.

'''