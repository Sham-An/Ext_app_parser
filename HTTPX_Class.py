# https://www.python-httpx.org/advanced/
# https://github.com/encode/httpx/tree/master/httpx
# cd avito_parser_django/avito
# python manage.py '!!!!_httpx_class_2'
# python manage.py makemigrations aparser
# python manage.py migrate aparser

import asyncio
import threading
import httpx
import ssl
from lxml import html
import logging
import datetime
# from logging import getLogger

# from django.core.management.base import BaseCommand
# from django.core.management.base import CommandError
# from aparser.models import Product
# from aparser.models import Product
# from aparser.models import Task
from pip._internal.exceptions import CommandError

STATUS_NEW = 1
STATUS_READY = 2
##########################################
CIPHERS = """ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-SHA256:AES256-SHA"""

key = 'af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir'  # ключ, с которым всё работает, не разбирался где его брать, но похоже он статичен, т.к. гуглится на различных форумах
cookie = '__cfduid=da6b6b5b9f01fd022f219ed53ac3935791610912291; sessid=ef757cc130c5cd228be88e869369c654.1610912291; _ga=GA1.2.559434019.1610912292; _gid=GA1.2.381990959.1610912292; _fbp=fb.1.1610912292358.1831979940; u=2oiycodt.1oaavs8.dyu0a4x7fxw0; v=1610912321; buyer_laas_location=641780; buyer_location_id=641780; luri=novosibirsk; buyer_selected_search_radius4=0_general; buyer_local_priority_v2=0; sx=H4sIAAAAAAACAxXLQQqAIBAF0Lv8dYvRLEdvU0MIBU0iKCHePXr71zGfefd1W5RLYick2kSakiB2VETclpf85n19RJMSp4vJOSlM%2F2BMOBDNaigE9taM8QH0oydNVAAAAA%3D%3D; dfp_group=100; _ym_uid=1610912323905107257; _ym_d=1610912323; _ym_visorc_34241905=b; _ym_isad=2; _ym_visorc_419506=w; _ym_visorc_188382=w; __gads=ID=2cff056a4e50a953-22d0341a94b900a6:T=1610912323:S=ALNI_MZMbOe0285QjW7EVvsYtSa-RA_Vpg; f=5.8696cbce96d2947c36b4dd61b04726f1a816010d61a371dda816010d61a371dda816010d61a371dda816010d61a371ddbb0992c943830ce0bb0992c943830ce0bb0992c943830ce0a816010d61a371dd2668c76b1faaa358c08fe24d747f54dc0df103df0c26013a0df103df0c26013a2ebf3cb6fd35a0ac0df103df0c26013a8b1472fe2f9ba6b978e38434be2a23fac7b9c4258fe3658d831064c92d93c3903815369ae2d1a81d04dbcad294c152cb0df103df0c26013a20f3d16ad0b1c5462da10fb74cac1eab2da10fb74cac1eab3c02ea8f64acc0bdf0c77052689da50d2da10fb74cac1eab2da10fb74cac1eab2da10fb74cac1eab2da10fb74cac1eab91e52da22a560f5503c77801b122405c48ab0bfc8423929a6d7a5083cc1669877def5708993e2ca678f1dc04f891d61e35b0929bad7c1ea5dec762b46b6afe81f200c638bc3d18ce60768b50dd5e12c30e37135e8f7c6b64dc9f90003c0354a346b8ae4e81acb9fa46b8ae4e81acb9fa02c68186b443a7acf8b817f3dc0c3f21c1eac53cc61955882da10fb74cac1eab2da10fb74cac1eab5e5aa47e7d07c0f95e1e792141febc9cb841da6c7dc79d0b'
#############################
# cookie = 'u=2tfvnhcb.ctv4iw.tymf98eh5pg0; _ym_d=1660584169; _ym_uid=166058416969271515; _gcl_au=1.1.56989214.1660584169; tmr_lvid=6bb642e099f3f60718329989304e0ddf; tmr_lvidTS=1660584170025; adrcid=Abu-CyKSxNnrOfCzX3o7WJw; buyer_laas_location=652000; uxs_uid=9f96c750-2309-11ed-a6ad-f34fafad57a6; buyer_location_id=652000; luri=rostov-na-donu; _gid=GA1.2.1638777385.1661600246; f=5.cc913c231fb04ced4b5abdd419952845a68643d4d8df96e9a68643d4d8df96e9a68643d4d8df96e9a68643d4d8df96e94f9572e6986d0c624f9572e6986d0c624f9572e6986d0c62ba029cd346349f36c1e8912fd5a48d02c1e8912fd5a48d0246b8ae4e81acb9fa143114829cf33ca746b8ae4e81acb9fa46b8ae4e81acb9fae992ad2cc54b8aa8b175a5db148b56e92157fc552fc06411bc8794f0f6ce82fe915ac1de0d034112dc0d86d9e44006d8143114829cf33ca7143114829cf33ca7c772035eab81f5e1fb0fb526bb39450a87829363e2d856a2b5b87f59517a23f2c772035eab81f5e13de19da9ed218fe23de19da9ed218fe2c772035eab81f5e1143114829cf33ca7172c80659da4d447f1cc8f457244b1a81ac794a8d120d7dc3fa8c565c3a4ea025cc116b628bd61b75d3d12014bda85a4087cf35ba7d977642e1c124e209506cf29aa4cecca288d6b767bc15421a53740cde1c78086b997c046b8ae4e81acb9fa46b8ae4e81acb9fa02c68186b443a7ac4c51f6e3637213638418bac8c3b019882da10fb74cac1eab2da10fb74cac1eabbe1b8fec550f290a09360354b9a5173a3778cee096b7b985bf37df0d1894b088; ft="24CG5tzXFLJmY1UjO4748/U5Wcmjkkpj5FkT7xo1OJOtPxazmZH4rWeEs53H+1m4zGnvXGHl1CG3Bmd7e5oe3VPMAgdQODpzZIXYsqzn4VVeI0PjJZgrr3/niuxjq49Lnjdw6Pf4xPbI6I6F8mC1JpbNVUms1vF9Vz5kj7DeX7tOHeBWSFgRv+VfOvBROhO6"; redirectMav=1; v=1661674970; dfp_group=38; _ym_visorc=b; _ym_isad=2; isCriteoSetNew=true; SEARCH_HISTORY_IDS=0%2C2%2C%2C4; sx=H4sIAAAAAAAC%2F1zRS67iMBBA0b1kzMC%2FqrLfbuwqO%2BSDQ4AkJE%2FsvcWAbtEbOLrS%2FW10KFSUiuAhglUlJbBFWBgVUCyu%2Bflt1uanKQuPotuzB9pwKQyZrnwM%2B%2BHmOvS1OTW5%2BdGImlCjpdepAa2MCTqD0jpp43ymVEwJkQXRGvORRRZn4elcTtOK47G5PDwEbunAeqD%2BJ2PQFv1bdhCVOM%2BmRIksmpOPtmRHpCjn%2BJGXspmB7q6fpjZ1bdwdVczd3HcHX0v71ewpvOWogkrRE2QOolViUYaigozFJs8fud7y0epxEM%2FPYzPVuKTjrtbpnla%2FTV%2Byo3czIiILYQkYAB2GTCnbIASKmSR8ZOpjGR5OXS4tLW7EutZl3ve6DcPTlfk%2F2b5OTUSvFTkqEoUyBLQ5hmTYKrLo2X7kKw28zABFXyzjuR7QcVs1VVplafdvOcDr1IgvBbNkZXSEzNYYCQgcnPJiWMrf5mmO3f0x2a2%2FPQFoefK5P9%2BXwfhuHMPXQRPo9foTAAD%2F%2FwJADIJ3AgAA; abp=0; _ga_9E363E7BES=GS1.1.1661674982.17.1.1661675492.60.0.0; buyer_from_page=catalog; _ga_M29JC28873=GS1.1.1661674982.17.1.1661675492.60.0.0; _ga=GA1.2.1813055663.1660584170; _dc_gtm_UA-2546784-1=1; _buzz_fpc=JTdCJTIycGF0aCUyMiUzQSUyMiUyRiUyMiUyQyUyMmRvbWFpbiUyMiUzQSUyMi53d3cuYXZpdG8ucnUlMjIlMkMlMjJleHBpcmVzJTIyJTNBJTIyTW9uJTJDJTIwMjglMjBBdWclMjAyMDIzJTIwMDglM0EzMSUzQTMyJTIwR01UJTIyJTJDJTIyU2FtZVNpdGUlMjIlM0ElMjJMYXglMjIlMkMlMjJ2YWx1ZSUyMiUzQSUyMiU3QiU1QyUyMnZhbHVlJTVDJTIyJTNBJTVDJTIyY2YzMDY3ZDU1MTc0NDRlZWRmNzMzNDgwZWQ2ZWNmYjglNUMlMjIlMkMlNUMlMjJmcGpzRm9ybWF0JTVDJTIyJTNBdHJ1ZSU3RCUyMiU3RA==; cto_bundle=2JKQZV93UlJZZW1obWZ3Tm1oQkolMkJNVVppZnRYaG95bzlzQ3FJVmIwOUZDdmxLaG4yVUNkam9WZXJmVWdNU05lYmZvRXZIc3N4ZnJhVnhlTDRzV2VXclg0TnFVNTklMkJvJTJCVzlzTkdhMjJyd0pkakQlMkYzbVFrciUyRnAlMkZCbWZSNGxtNVpBb2pDZG5JM1NyV3FNSCUyRnJuNyUyQmh5S3JzYTlRJTNEJTNE; tmr_reqNum=280; tmr_detect=0%7C1661675496313'
'''
Мы также включаем вспомогательную функцию для создания правильно настроенных SSLContextэкземпляров.
>>> context = httpx.create_ssl_context()
Функция create_ssl_contextпринимает тот же набор аргументов конфигурации SSL ( trust_env, verify, certи http2аргументы), что httpx.Clientи илиhttpx.AsyncClient
>>> import httpx
>>> context = httpx.create_ssl_context(verify="/tmp/client.pem")
>>> httpx.get('https://example.org', verify=context)
<Response [200 OK]>
'''
ssl_context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_CLIENT)  # +PROTOCOL_TLS_CLIENT) #PROTOCOL_TLS)#
ssl_context = httpx.create_ssl_context()
ssl_context.set_alpn_protocols(["h2"])
ssl_context.set_ciphers(CIPHERS)
# r = httpx.get(url_av, verify=ssl_context)

# logger = getLogger(__name__)
# logger.setLevel(logging.INFO)

logging.basicConfig(level=logging.INFO)  # , filename="py_log.log") #,filemode="w")
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)  # .setLevel(logging.INFO)
# logging.getLogger().setLevel(logging.INFO)
# logger.setLevel(logging.INFO)
##########################################
# url_0 = str('https://www.avito.ru/rostovskaya_oblast/mototsikly_i_mototehnika?cd=1&f=ASgCAgECAUXGmgwXeyJmcm9tIjoyMDAwLCJ0byI6NzAwMH0&q'+'=скутер&s=1')

# r = httpx.get(url_av, verify=ssl_context)
# # print(r.text)
# parse_xml(r.text)
'''
Настройка аутентификации
При выдаче запросов или создании экземпляра клиента authаргумент может использоваться для передачи используемой схемы аутентификации. Аргумент authможет быть одним из следующих...
Два кортежа username/ passwordдля использования с базовой проверкой подлинности.
Экземпляр 
httpx.BasicAuth() 
или 
httpx.DigestAuth().
Вызываемый объект, принимающий запрос и возвращающий аутентифицированный экземпляр запроса.
Экземпляр подклассов 

httpx.Auth
Наиболее сложным из них является последний, который позволяет создавать потоки аутентификации, включающие один или несколько запросов. Подкласс httpx.Authдолжен реализовывать def auth_flow(request)и выдавать любые запросы, которые необходимо сделать...
'''


# class MyCustomAuth(httpx.Auth): #
class MyCustomAuth:  #
    '''
Пользовательские классы проверки подлинности предназначены для того, чтобы не выполнять никаких операций ввода-вывода,
поэтому их можно использовать как с синхронизирующими, так и с асинхронными экземплярами клиента.
Если вы реализуете схему аутентификации, для которой требуется тело запроса, вам необходимо указать это в классе
с помощью свойства requires_request_body.
После этого вы сможете получить доступ request.contentк .auth_flow()методу.
    '''
    requires_response_body = True
    PAGE_LIMIT = 10

    def __init__(self):  # (self, access_token, refresh_token, refresh_url)

        self.session = httpx.Client()  # requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.2 Safari/605.1.15',
            'Accept-Language': 'ru',
        }
        self.task = None
        self.product = None
        #
        # self.access_token = access_token
        # self.refresh_token = refresh_token
        # self.refresh_url = refresh_url

    def auth_flow(self, request):
        request.headers["X-Authentication"] = self.access_token
        response = yield request

        if response.status_code == 401:
            # If the server issues a 401 response, then issue a request to
            # refresh tokens, and resend the request.
            refresh_response = yield self.build_refresh_request()
            self.update_tokens(refresh_response)

            request.headers["X-Authentication"] = self.access_token
            yield request

    def build_refresh_request(self):
        # Return an `httpx.Request` for refreshing tokens.
        # request = httpx.Request("GET", "https://example.com")
        pass

    def find_task(self):
        pass
        # obj = Task.objects.filter(status=STATUS_NEW).first()
        # if not obj:
        #     raise CommandError('no tasks found')
        # self.task = obj
        # logger.info(f'Работаем над заданием {self.task}')
        # print(f'Работаем над заданием {self.task}')

    def finish_task(self):
        # self.task.status = STATUS_READY
        # self.task.save()
        logger.info(f'Завершили задание')
        # pass

    def get_pagination_limit(self):
        # text = self.get_page()
        # soup = bs4.BeautifulSoup(text, 'lxml')
        #
        # container = soup.select('a.pagination-page')
        # if not container:
        #     return 1
        # last_button = container[-1]
        # href = last_button.get('href')
        # if not href:
        #     return 1
        #
        # r = urllib.parse.urlparse(href)
        # params = urllib.parse.parse_qs(r.query)
        limit = 1
        # return min(int(params['p'][0]), self.PAGE_LIMIT)
        return limit

    def get_page(self, page: int = None):
        params = {
            'radius': 0,
            'user': 1,
        }
        if page and page > 1:
            params['p'] = page

        # url = self.task.url
        url = "https://www.avito.ru/tarasovskiy/mototsikly_i_mototehnika/mopedy_i_skutery-ASgBAgICAUQ82gE?cd=1&f=ASgBAgECAUQ82gEBRcaaDBR7ImZyb20iOjAsInRvIjo0MDAwfQ&q=%D1%81%D0%BA%D1%83%D1%82%D0%B5%D1%80&radius=50&searchRadius=50"
        print(url)
        #r = httpx.get(url, params=params, verify=ssl_context)
        r = httpx.get(url, verify=ssl_context)
        print(r.status_code)
        print(r)
        r.raise_for_status()  # from httpx._models.py
        return r.text

    # def parse_block(self, item):
    #
    #     ''' Выбрать блок со ссылкой '''
    #     date = datetime.datetime.now()
    #
    #     #logger.debug(f'product {p}')

    def get_blocks(self, page: int = None):
        text = self.get_page(page=page)
        html_txt = text
        path_block = '//div[@elementtiming="bx.catalog.container"]'
        path_item = '//div[@data-marker="item"]'
        # category = val['category']
        path_title = './/div[substring(@class,1,13) ="iva-item-desc"]//text()'  # title = val['title']
        # images = '' #<img class="photo-slider-image-YqMGj" itemprop="image" alt="Питбайк kayo basic tt140em 17/14 KRZ" src="https://60.img.avito.st/image/1/1.DYt1KLa2oWJjiBtiY0xhqLyLoWjLK6DYwYuj.0Mcb0dqLEx27rZ5BWe-HjkyKAqBZymk0qXqEJkGD_ts" srcset="https://60.img.avito.st/image/1/1.DYt1KLa2oWJjiBtiY0xhqLyLoWjLK6DYwYuj.0Mcb0dqLEx27rZ5BWe-HjkyKAqBZymk0qXqEJkGD_ts 208w,https://60.img.avito.st/image/1/1.DYt1KLa2oWIbiEFiY0xhqLyLoWjLU6CCwYuj.xfmM82fRRR0LKlct_x_B5x4Knj80jsYPpVI4SSedFBQ 236w,https://60.img.avito.st/image/1/1.DYt1KLa2oWI_j39jY0xhqLyLoWjLd6e8wIuj.Vk6U_mmNsTUisHn1EWMImhqo4NtlHap3BPiSsTAQm2k 318w,https://60.img.avito.st/image/1/1.DYt1KLa2oWJzjGdlY0xhqLyLoWjLO6Skxouj.SESRi0AcfUNspQ7PuNMHVvowrYecXoyIbYsMD3_of6k 472w,https://60.img.avito.st/image/1/1.DYt1KLa2oWI7ghtnY0xhqLyLoWjLc6rYxIuj.kb20j2UV1ycMnY1AQKMZM5z5IR_iVjNyqp2a7wQp5wA 636w"
        path_name = './/h3[@itemprop="name"]/text()'
        path_uri_mweb = './/a[substring(@class,1,20) ="iva-item-sliderLink-"]//@href'  # a class="iva-item-sliderLink-uLz1v"
        path_id = ".//@id"  # ad_id
        path_price = './/meta[@itemprop="price"]//@content'  # price = val['price']
        path_pages = '//div[contains(@class, "pagination-root")]/span[last()-1]/text()'
        # time = val['time']
        path_location_free = './/span[contains(@class, "geo-addr")]/span/text()'  # address = val['address']
        path_location = './/div[contains(@class, "geo-geo")]/span/span/text()'  # coords = val['coords']
        # api https://m.avito.ru/api/19/items/2953844959?key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir
        # uri = val['uri']

        tree = html.fromstring(html_txt)
        count_page = tree.xpath(path_pages)
        # print(count_page[0])

        if count_page:
            count_page = int(count_page[0])
            print(f'Pages count === {count_page}')
        else:
            count_page = 1  # int(tree.xpath(path_pages)[0])
            print(f'Pages count === {count_page}')
        #
        tree = html.fromstring(html_txt)
        index = 0

        for item in tree.xpath(path_item):  # .getall():
            #
            # url_block = uri_mweb
            # if not url_block:
            #     raise CommandError('bad "url_block" css')
            item_id = item.xpath(path_id)  # ad_id

            uri_mweb = (f'https://www.avito.ru{item.xpath(path_uri_mweb)[-1]}')
            url = uri_mweb
            href = uri_mweb  # url_block.get('href')

            # print(f'ITEM_ID {item.xpath(path_id)[0]} type{type(item_id)} {item.xpath(path_id)[0]}')
            print(f'ITEM_ID {item_id[0]} type {type(item_id)}')
            name = item.xpath(path_name)[0]
            price = item.xpath(path_price)[0]
            # price = 111
            currency = 'Руб'
            location = "определить локацию"  # item.xpath(path_location)[0]
            location_free = item.xpath(path_location_free)
            uri_mweb = (f'https://www.avito.ru{item.xpath(path_uri_mweb)[-1]}')
            url_block = uri_mweb
            if not url_block:
                raise CommandError('bad "url_block" css')
            # category
            # time //*[@id="app"]/div/div[2]/div[2]/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div/span/class="text-text-LurtD text-size-s-BxGpL text-color-noaccent-P1Rfs"
            print(uri_mweb)
            print(f'!!!!!!!!!!!!NAME {name} @@@@ ЦЕНА {price} Location {location}')
            # Выбрать блок с датой размещения объявления
            date = "2023-03-25 20:37:16.000"  # None
            absolute_date = None  # date_block.get('data-absolute-date')
            # if absolute_date:
            #     date = self.parse_date(item=absolute_date)
            index += 1
            title_item = item.xpath(path_title)
            # if not title:
            #     raise CommandError(f'no title for item: {url_block}')
            tit = len(title_item)
            if tit < 1:
                title = "Без описания"
                print(f'пропуск {index} {name} id {item_id}')
            else:
                title = title_item[0]
            print(f' Норма {index} title = {title} \n\n')

            # obj = Task.objects.filter(status=STATUS_NEW).first()
            # MyModel.objects.filter(other_variable=0).update(variable='value')
            # MyModel.objects.filter(other_variable=0).update(variable=F('variable') + 1)
            # MyModel.objects.filter(user=user).update(variable='value')

    # ЗАКОМЕНТИРОВАЛ ORM
    # try:
    #     p = Product.objects.get(url=url)
    #     #print(f'##############&&&&&&&&&&&&&&&&  {p.title[:100]} \n\ntask = {self.task}')
    #     # p.task = self.task
    #     p.title = title[:255]
    #     p.price = price
    #     #p.currency = currency
    #     #p.published_date = date,
    #     p.save()
    # except Product.DoesNotExist:
    #     p = Product(
    #         task=self.task,
    #         title=title,
    #         url=url,
    #         price=price,
    #         currency=currency,
    #         published_date=date,
    #     ).save()

    # logger.debug(f'product {p}')

    def parse_all(self):
        # Выбрать какое-нибудь задание
        self.find_task()

        limit = self.get_pagination_limit()
        logger.info(f'Всего страниц: {limit}')
        # print(f'Всего страниц: {limit}')

        for i in range(1, limit + 1):
            logger.info(f'Работаем над страницей {i}')
            # print(f'Работаем над страницей {i}')
            self.get_blocks(page=i)

        # Завершить задание
        self.finish_task()

    def update_tokens(self, response):
        # Update the `.access_token` and `.refresh_token` tokens
        # based on a refresh response.
        data = response.json()

    def test(self):
        say = 'start_'
        # print(say)
        return say


# class test():
#     def say(self):
#         print('start_')

# class Command(BaseCommand):
# help = 'The Zen of Python'
#
# def handle(self, *args, **options):
#     import this
#    help = 'Парсинг Avito'

#    def handle(self, *args, **options):
#        p = MyCustomAuth()
# print(p.test())
# p = AvitoParser()
#        p.parse_all()
# s=test()
# s.say()

if __name__ == "__main__":
    p = MyCustomAuth()
    #print(p.test())
    # p = AvitoParser()
    p.parse_all()
    # s=test()
    # s.say()

# Пользовательские классы проверки подлинности предназначены для того,
# чтобы не выполнять никаких операций ввода-вывода, поэтому их можно использовать
# как с синхронизирующими, так и с асинхронными экземплярами клиента.
# Если вы реализуете схему аутентификации, для которой требуется тело запроса,
# вам необходимо указать это в классе с помощью свойства requires_request_body.

# После этого вы сможете получить доступ request.contentк .auth_flow()методу.
'''
class MyCustomAuth(httpx.Auth):
    requires_request_body = True

    def __init__(self, token):
        self.token = token

    def auth_flow(self, request):
      response = yield request
      if response.status_code == 401:
          # If the server issues a 401 response then resend the request,
          # with a custom `X-Authentication` header.
          request.headers['X-Authentication'] = self.sign_request(...)
          yield request

    def sign_request(self, request):
        # Create a request signature, based on `request.method`, `request.url`,
        # `request.headers`, and `request.content`.
        ...
#Точно так же, если вы реализуете схему, требующую доступа к тексту ответа,
# используйте это requires_response_bodyсвойство. После этого вы сможете получить
# доступ к свойствам и методам тела ответа, таким как response.content, response.text, response.json()и т. д.

class MyCustomAuth(httpx.Auth):
    requires_response_body = True

    def __init__(self, access_token, refresh_token, refresh_url):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.refresh_url = refresh_url

    def auth_flow(self, request):
        request.headers["X-Authentication"] = self.access_token
        response = yield request

        if response.status_code == 401:
            # If the server issues a 401 response, then issue a request to
            # refresh tokens, and resend the request.
            refresh_response = yield self.build_refresh_request()
            self.update_tokens(refresh_response)

            request.headers["X-Authentication"] = self.access_token
            yield request

    def build_refresh_request(self):
        # Return an `httpx.Request` for refreshing tokens.
        ...

    def update_tokens(self, response):
        # Update the `.access_token` and `.refresh_token` tokens
        # based on a refresh response.
        data = response.json()
'''
