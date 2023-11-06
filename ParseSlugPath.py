#https://www.avito.ru/rostovskaya_oblast_aksay?cd=1&f=ASgCAgECAUXGmgwXeyJmcm9tIjoxMDAwLCJ0byI6NjAwMH0&q=e-mu+1616m&s=1
from urllib.parse import urlparse, parse_qs

#url = "https://www.avito.ru/rostovskaya_oblast_aksay?cd=1&f=ASgCAgECAUXGmgwXeyJmcm9tIjoxMDAwLCJ0byI6NjAwMH0&q=e-mu+1616m&s=1"
#https://www.avito.ru/rostovskaya_oblast_aksay/tovary_dlya_kompyutera/komplektuyuschie-ASgBAgICAUTGB~pm?f=ASgBAgECAUTGB~pmAUXGmgwXeyJmcm9tIjoxMDAwLCJ0byI6NjAwMH0&q=E-MU+1616&s=1
url = "https://www.avito.ru/rostovskaya_oblast_aksay/tovary_dlya_kompyutera/komplektuyuschie-ASgBAgICAUTGB~pm?f=ASgBAgECAUTGB~pmAUXGmgwXeyJmcm9tIjoxMDAwLCJ0byI6NjAwMH0&q=E-MU+1616&s=1"

# Разбиваем адрес на составляющие
parsed_url = urlparse(url)

# Извлекаем составляющие адреса
scheme = parsed_url.scheme
netloc = parsed_url.netloc
path = parsed_url.path
path_parts = parsed_url.path.split("/")
params = parsed_url.params
query = parsed_url.query
fragment = parsed_url.fragment

# Парсим параметры запроса
parsed_query = parse_qs(query)

#Парсим Path
# Выводим результат

#<scheme>://<netloc>/<path>;<params>?<query>#<fragment>
print("Scheme:", scheme)
print("Netloc:", netloc)
print("Path:", path)
print("Path parts:", path_parts)
print("Params:", params)
print("Query:", query)
print("Parsed Query:", parsed_query)
print("Fragment:", fragment)

