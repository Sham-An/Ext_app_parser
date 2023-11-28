import requests

url = 'https://www.avito.ru/api/2/categories'

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    # Обрабатываем полученные данные
    # Например, выводим список категорий
    categories = data['data']
    for category in categories:
        print(f"ID: {category['id']}, Название: {category['name']}")
else:
    print(f"Ошибка {response.status_code}: Произошла ошибка при получении данных.")
