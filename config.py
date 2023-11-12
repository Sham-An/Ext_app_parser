import os
import ssl
import httpx

url_get = "https://www.avito.ru/all?cd=1&d=1&f=ASgCAgECAUXGmgwXeyJmcm9tIjoxMDAwLCJ0byI6ODAwMH0&q=e-mu+1616&s=1"  # 'locationId': ['621540']
url_get1 = 'https://www.avito.ru/rostovskaya_oblast/mototsikly_i_mototehnika?cd=1&q=скутер&f=ASgCAgECAUXGmgwXeyJmcm9tIjoyMDAwLCJ0byI6NzAwMH0'
url_get2 = 'https://www.avito.ru/rostovskaya_oblast?cd=1&d=1&f=ASgCAgECAUXGmgwXeyJmcm9tIjoxMDAwLCJ0byI6ODAwMH0&q=e-mu+1616&s=1'  # 'locationId': ['651110']
url_get3 = 'https://www.avito.ru/rostovskaya_oblast_aksay/bytovaya_elektronika?cd=1&d=1&q=e-mu+1212&s=1'  # 'locationId': ['651130']

host = '192.168.100.9'
#host = '10.10.16.2'
user = 'postgres'
password = 'postgres'
bd_name = 'main_avito_django_bot'
port = '5432'

CIPHERS = 'ECDH+AESGCM:ECDH+CHACHA20:DH+AESGCM:DH+CHACHA20:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:ECDH+HIGH:DH+HIGH:RSA+AESGCM:RSA+AES:RSA+HIGH:!aNULL:!eNULL:!MD5:!3DES'
avito_key = 'af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir'
name_column_1 = [
    'id', 'title', 'url', 'status', 'category_kod', 'city_kod', 'reg_kod', 'search_filter', 'search_key',
    'search_memo',
    'search_parametrs_api', 'search_parametrs_web', 'slug_category', 'slug_city', 'slug_reg', 'priceMax',
    'priceMin']

name_column_2 = [
    'id', 'title', 'url_canonical', 'url_alternate1', 'url_alternate2', 'status', 'category_kod', 'city_kod',
    'reg_kod', 'search_filter', 'search_key', 'search_memo', 'search_parametrs_api', 'search_parametrs_web',
    'slug_category', 'slug_city', 'slug_reg', 'priceMax', 'priceMin']


params = {
    'host': '192.168.100.9',
    #'host': '10.10.16.2',
    'port': 5432,
    'dbname': 'main_avito_django_bot',
    'user': 'postgres',
    'password': 'postgres'
}

xpath_mapping = {
    'path_url_canonical': './/head//link[@rel="canonical"]//@href',
    'path_url_alternate1': './/head//link[@rel="alternate"]//@href',
    'path_url_alternate2': './/head//link[substring(@href,1,7)="android"]//@href',
    'path_url_alternate3': './/head//link[substring(@href,1,7)="ios-app"]//@href',
    'path_title': './/div[substring(@class,1,13) ="iva-item-desc"]//text()',
    'path_name': './/h3[@itemprop="name"]/text()',
    'path_descrip': './/preceding-sibling::div[1]//div/text()',
    #'path_container': './/div[@id="app"]//div[@data-marker="catalog-serp"]',
    #'path_item_full': './/div[@id="app"]//div[@data-marker="catalog-serp"]//div[@data-marker="item"]',
    #'path_location': './/div[@elementtiming="bx.catalog.container"]//div[@data-item-id]//div[@data-marker="item-line"]//following-sibling::div[2]//span',
    #'path_item': '//div[@data-marker="item"]',
    #'path_item_url': '//a[@href]',
    #'path_id': ".//@id",
    #'path_price': './/meta[@itemprop="price"]//@content',
    #'path_pages': '//div[contains(@class, "pagination-root")]/span[last()-1]/text()',
    #'path_location_free': './/span[contains(@class, "geo-addr")]/span/text()',
    #'path_location': './/div[contains(@class, "geo-geo")]/span/span/text()'
}
'''
    'path_price_long': './/div[@elementtiming="bx.catalog.container"]//div[@data-item-id]//meta[@itemprop="price"]',
    'path_price_old': './/meta[@itemprop="price"]',
    'path_trader_long': './/div[@elementtiming="bx.catalog.container"]//div[@data-item-id]//div[@data-marker="item-line"]//a',
    'path_trader': './/div[@data-marker="item-line"]//a/text()',
    'path_descrip_full': './/div[starts-with(@class,"iva-item-text")]',
    'path_descrip_full_text': './/div[starts-with(@class,"iva-item-text")]//text()',
    'path_time_old': './/div[@elementtiming="bx.catalog.container"]//div[@data-item-id]//div[@data-marker="item-date"]/text()',

'''

def get_ssl_context():
    ssl_context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_CLIENT)
    ssl_context = httpx.create_ssl_context()
    ssl_context.set_alpn_protocols(["h2"])
    return ssl_context


# api_reg = os.getenv("API_BOT_161")#.split(":")
# api_bot_reg = api_reg.split(":")
# bot_login = api_bot_reg[0]
# api_key = api_bot_reg[1]
# token = api_reg
# chat_id = bot_login

# config(
# dbname = bd_name,
# user = user,
# host = host,
# password = password
#  )

# config = {
#     'host': host,
#     'user': user,
#     'password': password,
#     'database': bd_name,
#     'token': api_reg,
# }


"""
sql:

CREATE DATABASE realty
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;
"""

#import os
#from urllib.parse import urlparse
#import urllib
#print(os.getenv("API_BOT_161"))
#print(os.environ.get("API_BOT_161"))

# api_reg = os.getenv("API_BOT_161")#.split(":")
# api_bot_reg = api_reg.split(":")
# bot_login = api_bot_reg[0]
# api_key = api_bot_reg[1]
#print(f"login {bot_login}, api {api_key}")
#print(f"token {token}, api {api_key}, chat_id {chat_id}")


