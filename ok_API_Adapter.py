#URL https://habr.com/ru/post/537834/
import json
import requests
import sys
import time
#import datetime
from random import randint
#from fake_useragent import UserAgent
import ssl
from requests.adapters import HTTPAdapter
#from requests.packages.urllib3.poolmanager import PoolManager
from urllib3.poolmanager import PoolManager
#from requests.packages.urllib3.util import ssl_
from urllib3.util import ssl_

CIPHERS = """ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-SHA256:AES256-SHA"""

class TlsAdapter(HTTPAdapter):

    def __init__(self, ssl_options=0, **kwargs):
        self.ssl_options = ssl_options
        super(TlsAdapter, self).__init__(**kwargs)

    def init_poolmanager(self, *pool_args, **pool_kwargs):
        ctx = ssl_.create_urllib3_context(ciphers=CIPHERS, cert_reqs=ssl.CERT_REQUIRED, options=self.ssl_options)
        self.poolmanager = PoolManager(*pool_args, ssl_context=ctx, **pool_kwargs)


#af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir
key = 'af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir' # ключ, с которым всё работает, не разбирался где его брать, но похоже он статичен, т.к. гуглится на различных форумах
cookie = '__cfduid=da6b6b5b9f01fd022f219ed53ac3935791610912291; sessid=ef757cc130c5cd228be88e869369c654.1610912291; _ga=GA1.2.559434019.1610912292; _gid=GA1.2.381990959.1610912292; _fbp=fb.1.1610912292358.1831979940; u=2oiycodt.1oaavs8.dyu0a4x7fxw0; v=1610912321; buyer_laas_location=641780; buyer_location_id=641780; luri=novosibirsk; buyer_selected_search_radius4=0_general; buyer_local_priority_v2=0; sx=H4sIAAAAAAACAxXLQQqAIBAF0Lv8dYvRLEdvU0MIBU0iKCHePXr71zGfefd1W5RLYick2kSakiB2VETclpf85n19RJMSp4vJOSlM%2F2BMOBDNaigE9taM8QH0oydNVAAAAA%3D%3D; dfp_group=100; _ym_uid=1610912323905107257; _ym_d=1610912323; _ym_visorc_34241905=b; _ym_isad=2; _ym_visorc_419506=w; _ym_visorc_188382=w; __gads=ID=2cff056a4e50a953-22d0341a94b900a6:T=1610912323:S=ALNI_MZMbOe0285QjW7EVvsYtSa-RA_Vpg; f=5.8696cbce96d2947c36b4dd61b04726f1a816010d61a371dda816010d61a371dda816010d61a371dda816010d61a371ddbb0992c943830ce0bb0992c943830ce0bb0992c943830ce0a816010d61a371dd2668c76b1faaa358c08fe24d747f54dc0df103df0c26013a0df103df0c26013a2ebf3cb6fd35a0ac0df103df0c26013a8b1472fe2f9ba6b978e38434be2a23fac7b9c4258fe3658d831064c92d93c3903815369ae2d1a81d04dbcad294c152cb0df103df0c26013a20f3d16ad0b1c5462da10fb74cac1eab2da10fb74cac1eab3c02ea8f64acc0bdf0c77052689da50d2da10fb74cac1eab2da10fb74cac1eab2da10fb74cac1eab2da10fb74cac1eab91e52da22a560f5503c77801b122405c48ab0bfc8423929a6d7a5083cc1669877def5708993e2ca678f1dc04f891d61e35b0929bad7c1ea5dec762b46b6afe81f200c638bc3d18ce60768b50dd5e12c30e37135e8f7c6b64dc9f90003c0354a346b8ae4e81acb9fa46b8ae4e81acb9fa02c68186b443a7acf8b817f3dc0c3f21c1eac53cc61955882da10fb74cac1eab2da10fb74cac1eab5e5aa47e7d07c0f95e1e792141febc9cb841da6c7dc79d0b' \
# Если забанили, то добавьте свои куки, это не боевой код но он делает то, что надо
search = 'suzuki+gsx-r'     # Строка поиска на сайте и ниже параметры выбора города, радиуса разброса цены и т.п.
categoryId = 14
locationId = 641780         # Новосибирск
searchRadius = 200
priceMin = 100000
priceMax = 200000
sort = 'priceDesc'
withImagesOnly = 'true'     # Только с фото
limit_page = 50     # Количество объявлений на странице 50 максимум

def except_error(res): # Эту функцию можно дополнить, например обработку капчи
    #ok print(res.status_code, res.text)
    sys.exit(1)
    UA1 = UserAgent().random
s = requests.Session()                          # Будем всё делать в рамках одной сессии
# Задаем заголовки:
proxiess = {'http': '185.170.215.228:80'} #79.143.225.152:60517
proxiess = {'http': '79.143.225.152:60517'} #79.143.225.152:60517

# 'user-agent': UserAgent().random, #'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Mobile Safari/537.36',
# 'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Mobile Safari/537.36',
# 'user-agent': 'Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36'
#str(UA1),

s = requests.session()
adapter = TlsAdapter(ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1)
s.mount("https://", adapter)
#UA 	Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0
#'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Mobile Safari/537.36',
#Host	m.avito.ru
#'authority': 'm.avito.ru'
headers = { 'Host': 'm.avito.ru',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0',
            'accept':  'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'ru-RU,ru;q=0.9',}
if cookie:                                      # Добавим куки, если есть внешние куки
    headers['cookie'] = cookie
print(f'куки = {cookie}')
s.headers.update(headers)                       # Сохраняем заголовки в сессию
#proxiess = {'http': '176.9.75.42:3128'}
#proxiess = {'http': '207.154.231.208:3128'}
#UA = UserAgent().random
s.get('https://m.avito.ru/', proxies = proxiess)#, useragent = UA) #   useragent = str(UA)                 # Делаем запрос на мобильную версию.
url_api_9 = 'https://m.avito.ru/api/9/items'    # Урл первого API, позволяет получить id и url объявлений по заданным фильтрам
                                                # Тут уже видно цену и название объявлений
#uag = useragent.Random()

# Print user agent
#print(f'UAG {uag}')

params = {
    'key': 'af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir',
    'categoryId': 14,
    'params[30]': 4969,
    'locationId': locationId,
    'searchRadius': searchRadius,
    'priceMin': priceMin,
    'priceMax': priceMax,
    'params[110275]': 426645,
    'sort': sort,
    'withImagesOnly': withImagesOnly,
    'lastStamp': 1660975970,
    'display': 'list',
    'limit': limit_page,
    'query': search,
}
cicle_stop = True       # Переменная для остановки цикла
cikle = 0               # Переменная для перебора страниц с объявлениями
items = []              # Список, куда складываем объявления
#params['key'] = key
while cicle_stop:
    cikle += 1          # Так как страницы начинаются с 1, то сразу же итерируем
    params['page'] = cikle
    #print(params)

    res = s.get(url_api_9, params=params, proxies = proxiess) #, useragent = UA) #, useragent = str(UA))
    #print(f'PROXIIESS {proxiess} Agent {UA} \n HEADERS {headers}')
    # OK!!! print(f'################################################# \n{res.json()}')

    try:
        res = res.json()
        #ok!!! print(f'res= {res}')

    except json.decoder.JSONDecodeError: #{'code': 403, 'error': {'message': 'Доступ с вашего IP-адреса временно ограничен', 'link': 'ru.avito://1/info/ipblock/show'}}
        except_error(res)

 #   if res['status'] != 'ok':
 #           print(res['result'])
 #           sys.exit(1)


    if res['status'] != 'ok':
            #print(f'''result = {res['result']}''')
            print(f'''result = NON''')
            sys.exit(1)
    if res['status'] == 'ok':
        items_page = int(len(res['result']['items']))
        lastStamp =  int(res['result']['lastStamp'])
        print(f"res['status'] == 'ok': lastStamp {lastStamp}")

        if items_page > limit_page: # проверка на "snippet"
            items_page = items_page - 1

        for item in res['result']['items']:
            if item['type'] == 'item':
                items.append(item)
                print('items.append(item)')
        if items_page < limit_page:
            cicle_stop = False
####################################################################
#key = 'af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir'
#params = {'key': key}
print(f'!!!!! ПОЛУЧИЛИ ИТЕМС') # {items}')
index = 1
for i in items: # Теперь идем по ябъявлениям:
    ad_id = str(i['value']['id'])
    val = i['value']
    print(f'val  {val}')
    category = val['category']
    print(f'category  {category}')
    time = val['time']
    print(f'time  {time}')
    title = val['title']
    print(f'title  {title}')
    images = ''
    price = val['price']
    print(f'price  {price}')
    address = val['address']
    print(f'address  {address}')
    coords = val['coords']
    print(f'coords  {coords}')
    uri = val['uri']
    print(f'uri  {uri}')
    uri_mweb = val['uri_mweb']
    print(f'uri_mweb  {uri_mweb}')




#https://www.avito.ru/rostovskaya_oblast/avtomobili?cd=1&f=ASgBAQECAkTyCrCKAeC2DaSKNANA5rYNJL63KMy3KPC2DRTutyj2xA0UvrA6AUWMFBl7ImZyb20iOjE0NzY4LCJ0byI6MTQ3NzN9

    ''')

    #args = [city, categories, subcategory, 1, district_or_metro, direction]
    #url = "https://avito.ru/{}/{}/{}?p={}&{}={}".format(*args)

    # url_more_data_1 = 'https://m.avito.ru/api/1/rmp/show/' + ad_id  # more_data_1 = s.get(url_more_data_1, params=params).json() # Тут тоже моного информации, можете посмотреть
    # URL API OK https://m.avito.ru/api/9/items?key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir&categoryId=9&params[1283]=14756&locationId=640000&params[110000]=329273&withImagesOnly=1&page=1&lastStamp=1611316560&display=list&limit=30
    url_more_data_2 = 'https://m.avito.ru/api/15/items/' + ad_id
    #https://m.avito.ru/api/14/items/{add_id}?key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir
    ####https://m.avito.ru/api/14/items/2467534891?key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir
    #2467534891
    url_more_data_2 = 'https://m.avito.ru/api/9/items/' + ad_id
    #url_more_data_2 = 'https://m.avito.ru/api/9/items/'
    print(f'url_more_data_2 +ad_id {url_more_data_2}')
    print(i)
    print('=======================================================\n')
    #uri_mweb

    # more_data_2 = s.get(url_more_data_2, params=params).json()
    # #more_data_2 = s.get(url_more_data_2, params=params, proxies = {'http': '176.9.119.170:8080'}).json()
    # print(f'1.) URL url_more_data_2 {url_more_data_2}',end='\n')
    # print(f'1.) more_data_2 json {more_data_2}', end='\n')
    # if not 'error' in more_data_2:
    #     '''#print(f'2.) more_data_2 = {more_data_2}',end='\n')            # В more_data_2 есть всё, что надо, я вывел на принт наиболее интересные для наглядности:
    #     # more_data_2 = {'id': 2032588517, 'categoryId': 14, 'locationId': 641780, 'metroId': 2024, 'metroType': 'text', 'districtId': 808, 'sharing': {'fb': 'https://www.avito.ru/novosibirsk/mototsikly_i_mototehnika/suzuki_gsxr_600_k7_2032588517?utm_campaign=fb&utm_medium=item_page_mavnew&utm_source=soc_sharing', 'gp': 'https://www.avito.ru/novosibirsk/mototsikly_i_mototehnika/suzuki_gsxr_600_k7_2032588517?utm_campaign=gp&utm_medium=item_page_mavnew&utm_source=soc_sharing', 'lj': 'https://www.avito.ru/novosibirsk/mototsikly_i_mototehnika/suzuki_gsxr_600_k7_2032588517?utm_campaign=lj&utm_medium=item_page_mavnew&utm_source=soc_sharing', 'mm': 'https://www.avito.ru/novosibirsk/mototsikly_i_mototehnika/suzuki_gsxr_600_k7_2032588517?utm_campaign=mm&utm_medium=item_page_mavnew&utm_source=soc_sharing', 'native': 'https://www.avito.ru/novosibirsk/mototsikly_i_mototehnika/suzuki_gsxr_600_k7_2032588517?utm_campaign=native&utm_medium=item_page_mavnew&utm_source=soc_sharing', 'ok': 'https://www.avito.ru/novosibirsk/mototsikly_i_mototehnika/suzuki_gsxr_600_k7_2032588517?utm_campaign=ok&utm_medium=item_page_mavnew&utm_source=soc_sharing', 'tw': 'https://www.avito.ru/novosibirsk/mototsikly_i_mototehnika/suzuki_gsxr_600_k7_2032588517?utm_campaign=tw&utm_medium=item_page_mavnew&utm_source=soc_sharing', 'vk': 'https://www.avito.ru/novosibirsk/mototsikly_i_mototehnika/suzuki_gsxr_600_k7_2032588517?utm_campaign=vk&utm_medium=item_page_mavnew&utm_source=soc_sharing', 'url': 'https://www.avito.ru/novosibirsk/mototsikly_i_mototehnika/suzuki_gsxr_600_k7_2032588517'}, 'coords': {'lat': 54.9760095778691, 'lng': 82.870258256977}, 'shouldShowMapPreview': True, 'address': 'Новосибирская область, Новосибирск, Степная ул., 45', 'geoReferences': [{'content': 'Площадь Маркса', 'after': ' 1,6 км', 'colors': ['#CD0505']}], 'title': 'Suzuki gsxr 600 K7', 'userType': 'private', 'time': 1625643723,
    #     #time.sleep(randint(6,14))'''
    #
    #     time.sleep((randint(6,14)) if index % 10 != 0 else 20)
    #     index += 1
    #     URLs=more_data_2['sharing']
    #     URLs_fb=URLs['fb']
    #     print(f'''3.) sharing {URLs}    ''') #more_data_2['sharing']
    #     print(f'''3.1) sharing fb {URLs_fb}    ''')  # more_data_2['sharing']
    #     print(f'''4.) price {more_data_2['price']}   Addres ''')
    #     print(f'''5.) PPrice2 {more_data_2['price']['value']}  ''')
    #     print(f'''6.) Addres {more_data_2['address']}''')
    #     url_get_phone = 'https://m.avito.ru/api/1/items/' + ad_id + '/phone'    # URL для получения телефона https://m.avito.ru/api/1/items/2005420126/phone
    #     print(f'''6.1) ПАРСИНГ ТЕЛЕФОНА url_get_phone {url_get_phone}''')
    #     phone = s.get(url_get_phone, params=params).json()                      # Сам запрос
    #     print(f'''6.2) ПАРСИНГ ТЕЛЕФОНА phone = s.get(url_get_phone {phone}''')
    #     print(f'''6.3) ПАРИНГ ТЕЛЕФОНА phone_number = requests.utils.unquote(phone['result']['action']['uri'].split('number=')[1])''')
    #     if phone['status'] == 'ok':
    #         phone_number = requests.utils.unquote(phone['result']['action']['uri'].split('number=')[1]) # Прверка на наличие телефона, такой странный синтсксис, чтоб уместиться в 100 сторочек кода)))
    #     else: phone_number = phone['result']['message']
    #     print(f'7.) телефон {phone_number}')
    #     print(f'''8.) seller {more_data_2['seller']}''')
    #     print(f'''9.) Name {more_data_2['seller']['name']}''')
    #     regtime = more_data_2['seller']['registrationTime']
    #     #parse_date(item=absolute_date)
    #     print(f'''10.) registrationTime {more_data_2['seller']['registrationTime']}''')
    #     print(f'''10.1) regTime {regtime}''')
    #
    #     #connection пропускаю пока
    #     print(f'''11.) link {more_data_2['seller']['link']}''')


        # print(f'''12.) description {more_data_2['description']}''') # Скрыл, т.к. много букв
        #print('=======================================================\n')


#https: // rest - app.net / api / ad?login = ваш_логин & token = ваш_ключ & id = 685674499

'''
{'type': 'item', 
    'value': {'id': 2548812127, 
            'category': {'id': 14, 'name': 'Мотоциклы и мототехника'}, 
            'time': 1660975970, 
            'title': 'Suzuki GSX-R 1000 K7', 
            'images': {'count': 8, 
                'main': {'140x140': 'https://53.img.avito.st/image/1/1.hKWRfLa5KEy_3bJMlWbdnkrfLkYvRyjWJd8qSC3dIk4.9ZG7xufqONsHYiOTRkYvUe_-03sfNndj43Eez8FfHFY', 
                        '278x278': 'https://53.img.avito.st/image/1/1.hKWRfLa5KEyL24ZKlWbdnkrfLkYvcy7iI98qSC3dIk4.sCSaVxmjtA6f57EeAVhJdfRjRUpmcYwKjKfyLNm_uhs', 
                        '339x339': 'https://53.img.avito.st/image/1/1.hKWRfLa5KEyB2oxLlWbdnkrfLkYveS_oIt8qSC3dIk4.H9FHbDhH6dAPY-4_KDO7v03lJKbiTslUFWiKSmWB_Ts', 
                        '372x372': 'https://53.img.avito.st/image/1/1.hKWRfLa5KEzP2sJLlWbdnkrfLkYvNy-mIt8qSC3dIk4.OrpM3PXzIcfF61Xpi1hObOzdr16-gTVA4M8dS2s2d1s', 
                        '507x507': 'https://53.img.avito.st/image/1/1.hKWRfLa5KEzR2NxJlWbdnkrfLkYvKS24IN8qSC3dIk4.yfzZEpiMfcF-b_hBV78jA6erkvtlvy9dpVQkvmWEMps', 
                        '558x558': 'https://53.img.avito.st/image/1/1.hKWRfLa5KEz71_ZGlWbdnkrfLkYvAyKSL98qSC3dIk4.-BSYdw1NcKZXtN3kWCFHPs8hx_G_mnUcxCVwx4oIulU', 
                        '678x678': 'https://53.img.avito.st/image/1/1.hKWRfLa5KEzr1eZElWbdnkrfLkYvEyCCLd8qSC3dIk4.LyT1Fq3dryovf2N4oawzB44-fLRae_RcslTeYkmEFMg'
                         }
                       },
             'price': '390 000 ₽', 
             'isFavorite': False, 
             'geoReferences': [{'content': 'Барнаул'}],
             'location': 'Барнаул', 
             'address': '', 
             'coords': {'lat': '53.3410076816952', 'lng': '83.6719359047852'}, 
             'userType': 'private', 
             'hasVideo': False, 
             'hasRealtyLayout': False, 
             'isVerified': False, 
             'contactlessView': False, 
             'uri': 'ru.avito://1/item/show?context=H4sIAAAAAAAA_0q0MrSqLrYytFKqULIutjI2tFLKKrFMyrUstUgrN8lNLDcvNTXMzTQtzigvMM4yTE2vULKuBQQAAP__3VzYajUAAAA&itemId=2548812127', 
             'uri_mweb': '/barnaul/mototsikly_i_mototehnika/suzuki_gsx-r_1000_k7_2548812127?context=H4sIAAAAAAAA_0q0MrSqLrYytFKqULIutjI2tFLKKrFMyrUstUgrN8lNLDcvNTXMzTQtzigvMM4yTE2vULKuBQQAAP__3VzYajUAAAA'}
             }
'''

# https://m.avito.ru/api//1/item/show?key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir&context=H4sIAAAAAAAA_0q0MrSqLrYytFKqULIutjI2tFLKKrFMyrUstUgrN8lNLDcvNTXMzTQtzigvMM4yTE2vULKuBQQAAP__3VzYajUAAAA&itemId=2548812127'
# https://m.avito.ru/api/14/items/2467534891?key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir
#f'lastStamp={time}&parameters[locationId]={region_id}&parameters[categoryId]={category_id}'