# https://www.python-httpx.org/advanced/
# https://github.com/encode/httpx/tree/master/httpx
# cd avito_parser_django/avito
# python manage.py 'app_httpx_category_ORM'
# python manage.py 'app_httpx_region_ORM'
# python manage.py makemigrations aparser
# python manage.py migrate aparser
# .\Make reg

import psycopg2
import asyncio
import threading
import httpx
import ssl
from lxml import html
import logging
import datetime
import json
#from django.core.management.base import BaseCommand
#from django.core.management.base import CommandError

# from aparser.models import Product
# from aparser.models import Product
# from aparser.models import Task
# from aparser.models import Region

STATUS_NEW = 1
STATUS_READY = 2

# CIPHERS = """ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-SHA256:AES256-SHA"""
CIPHERS = 'ECDH+AESGCM:ECDH+CHACHA20:DH+AESGCM:DH+CHACHA20:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:ECDH+HIGH:DH+HIGH:RSA+AESGCM:RSA+AES:RSA+HIGH:!aNULL:!eNULL:!MD5:!3DES'

key = 'af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir'  # ключ, с которым всё работает, не разбирался где его брать, но похоже он статичен, т.к. гуглится на различных форумах
cookie = '__cfduid=da6b6b5b9f01fd022f219ed53ac3935791610912291; sessid=ef757cc130c5cd228be88e869369c654.1610912291; _ga=GA1.2.559434019.1610912292; _gid=GA1.2.381990959.1610912292; _fbp=fb.1.1610912292358.1831979940; u=2oiycodt.1oaavs8.dyu0a4x7fxw0; v=1610912321; buyer_laas_location=641780; buyer_location_id=641780; luri=novosibirsk; buyer_selected_search_radius4=0_general; buyer_local_priority_v2=0; sx=H4sIAAAAAAACAxXLQQqAIBAF0Lv8dYvRLEdvU0MIBU0iKCHePXr71zGfefd1W5RLYick2kSakiB2VETclpf85n19RJMSp4vJOSlM%2F2BMOBDNaigE9taM8QH0oydNVAAAAA%3D%3D; dfp_group=100; _ym_uid=1610912323905107257; _ym_d=1610912323; _ym_visorc_34241905=b; _ym_isad=2; _ym_visorc_419506=w; _ym_visorc_188382=w; __gads=ID=2cff056a4e50a953-22d0341a94b900a6:T=1610912323:S=ALNI_MZMbOe0285QjW7EVvsYtSa-RA_Vpg; f=5.8696cbce96d2947c36b4dd61b04726f1a816010d61a371dda816010d61a371dda816010d61a371dda816010d61a371ddbb0992c943830ce0bb0992c943830ce0bb0992c943830ce0a816010d61a371dd2668c76b1faaa358c08fe24d747f54dc0df103df0c26013a0df103df0c26013a2ebf3cb6fd35a0ac0df103df0c26013a8b1472fe2f9ba6b978e38434be2a23fac7b9c4258fe3658d831064c92d93c3903815369ae2d1a81d04dbcad294c152cb0df103df0c26013a20f3d16ad0b1c5462da10fb74cac1eab2da10fb74cac1eab3c02ea8f64acc0bdf0c77052689da50d2da10fb74cac1eab2da10fb74cac1eab2da10fb74cac1eab2da10fb74cac1eab91e52da22a560f5503c77801b122405c48ab0bfc8423929a6d7a5083cc1669877def5708993e2ca678f1dc04f891d61e35b0929bad7c1ea5dec762b46b6afe81f200c638bc3d18ce60768b50dd5e12c30e37135e8f7c6b64dc9f90003c0354a346b8ae4e81acb9fa46b8ae4e81acb9fa02c68186b443a7acf8b817f3dc0c3f21c1eac53cc61955882da10fb74cac1eab2da10fb74cac1eab5e5aa47e7d07c0f95e1e792141febc9cb841da6c7dc79d0b'

# ssl_context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_CLIENT)  # +PROTOCOL_TLS_CLIENT) #PROTOCOL_TLS)#
# ssl_context = httpx.create_ssl_context()
# ssl_context.set_alpn_protocols(["h2"])
# ssl_context.set_ciphers(CIPHERS)

ssl_context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_CLIENT)  # +PROTOCOL_TLS_CLIENT) #PROTOCOL_TLS)#
ssl_context = httpx.create_ssl_context()
ssl_context.set_alpn_protocols(["h2"])
ssl_context.set_ciphers(CIPHERS)
url = 'https://www.avito.ru/tarasovskiy/mototsikly_i_mototehnika?cd=1&radius=50&searchRadius=50'
response = httpx.get(url, verify=ssl_context)

logging.basicConfig(level=logging.INFO)  # , filename="py_log.log") #,filemode="w")
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)  # .setLevel(logging.INFO)



def region_json_to_aparser():
    con = psycopg2.connect(
        database="main_avito_django_bot",
        user="postgres",
        password="postgres",
        # password=input("Пароль"),
        # host="192.168.100.9",
        host="10.10.16.2",
        port="5432"
    )
    cur = con.cursor()
    print("Database opened successfully \n")
    data = open_region_js()
    # print(reglist)
    # data = reglist
    print(f'###################### data {type(data["data"])}')

    all_id = []
    for dataitems in data['data']:
        if dataitems['id'] in all_id:
            print('IIIIDDDD Поймали ДУБЛЯЖ!!!!!!!!!!!!!!!!!!!!!')
            break
        all_id.append(dataitems['id'])
        # Добавляем количество полей для корректного запроса заполнения SQL
        dataitems.setdefault('url_path', 'None')  # , value)
        dataitems.setdefault('url_name', 'None')  # , value)
        dataitems.setdefault('index_post', 'None')  # , value)
        dataitems.setdefault('kod_region', 'None')  # , value)
        # self.check_region(dataitems) #dataitems)
        reg_id = dataitems['id']

        # set_region_SQL(dataitems, cur)
        print(dataitems['id'], dataitems['kod_region'], dataitems['kod_region'], dataitems['name'],
              dataitems['url_path'], dataitems['url_name'], dataitems['index_post'], )

        # values = ({'id': dataitems['id'], 'name': dataitems['name']})
        # cur.execute(
        #    "INSERT INTO APARSER_REGION (id,region_id,kod_region,url_path,url_name,index_post,NAME) VALUES (%(id)s,%(id)s,'00','blank','blank','000000',%(name)s)",
        #    values
        # )

        # cur.execute("INSERT INTO aparser_region ('id', 'name') VALUES (dataitems['id'], dataitems['name'])")
        # cur.execute("INSERT INTO aparser_region ('id', 'region_id', 'kod_region', 'name', 'url_path', 'url_name', 'index_post') VALUES (dataitems['id'], dataitems['kod_region'], dataitems['kod_region'], dataitems['name'], dataitems['url_path'], dataitems['url_name'], dataitems['index_post'])")

    # cur = con.cursor()
    # cur.execute("SELECT id, name from AVITO_REGION")
    # INSERT INTO "aparser_region" ("region_id", "kod_region", "name", "url_path", "url_name", "index_post")
    # VALUES (NULL, '00', '2', 'zero', '', NULL) RETURNING "aparser_region"."id"

    # rows = cur.fetchall()
    # for row in rows:
    #     print("id =", row[0], " NAME =", row[1])
    #     #print("NAME =", row[1])
    #
    # print("Operation done successfully")
    con.close()


def region_list_from_db():
    con = psycopg2.connect(
        database="main_avito_django_bot",
        user="postgres",
        password="postgres",
        # password=input("Пароль"),
        host="192.168.100.9",
        # host="10.10.10.18",
        port="5432"
    )

    print("Database opened successfully")
    cur = con.cursor()
    cur.execute("SELECT id, name from AVITO_REGION")
    # INSERT INTO "aparser_region" ("region_id", "kod_region", "name", "url_path", "url_name", "index_post")
    # VALUES (NULL, '00', '2', 'zero', '', NULL) RETURNING "aparser_region"."id"

    rows = cur.fetchall()
    for row in rows:
        print("id =", row[0], " NAME =", row[1])
        # print("NAME =", row[1])

    print("Operation done successfully")
    con.close()


class Region_set:
    def __init__(self):  # (self, access_token, refresh_token, refresh_url)

        self.session = httpx.Client()  # requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.2 Safari/605.1.15',
            'Accept-Language': 'ru',
        }
        self.task = None
        self.product = None
        self.data = None
        self.region = None

    def find_task(self):
        obj = Task.objects.filter(status=STATUS_NEW).first()
        if not obj:
            raise CommandError('no tasks found')
        self.task = obj
        # logger.info(f'Работаем над заданием {self.task}')
        print(f'Работаем над заданием {self.task}')
        # print(f'Работаем над заданием {self.task}')

    def find_region(self, id):
        id = int(id)
        obj = Region.objects.filter(id).first()
        # obj = Region.objects.filter(pk).first()
        if not obj:
            raise CommandError('no region found')
        self.Region = obj
        logger.info(f'Работаем над заданием {self.task}')
        # print(f'Работаем над заданием {self.task}')

    @staticmethod
    def set_region(reg_list):
        id = int(reg_list['id'])
        name = reg_list['name']
        url_path = reg_list['url_path']
        print(f'Работаем над заданием Region')
        try:
            p = Region.objects.get(region_id=id)
            # p = Region.objects.filter(region_id=id).first()
            print(f'##&& {p.id} {p.name} ')  # task = {self.task}')
            p.id = id
            p.region_id = id
            p.name = name
            p.url_path = url_path
            p.save()
        except Region.DoesNotExist:
            p = Region(
                id=id,
                region_id=id,
                name=name,
                url_path="",
                url_name="",
                index_post=0,
            ).save()

    # @staticmethod
    def check_region(self, reg):
        # print(f'#########################################\n {self.data["data"]}')
        reg1 = reg  # list(self.data["data"]) #reg
        print(self.data is reg1)
        # reg1 = self.data['data']
        # print(self.data)
        print(reg1)
        reg_id = reg1["id"]
        id_int = int(reg1["id"])
        print(f'reg_id {reg_id}')

    def list_region(self):  # , data):
        data = self.data
        print(f'###################### data {type(data["data"])}')

        all_id = []
        for dataitems in data['data']:
            if dataitems['id'] in all_id:
                print('IIIIDDDD Поймали ДУБЛЯЖ!!!!!!!!!!!!!!!!!!!!!')
                break
            all_id.append(dataitems['id'])
            # Добавляем количество полей для корректного запроса заполнения SQL
            dataitems.setdefault('url_path', 'None')  # , value)
            dataitems.setdefault('url_name', 'None')  # , value)
            dataitems.setdefault('index_post', 'None')  # , value)
            dataitems.setdefault('kod_region', 'None')  # , value)
            # self.check_region(dataitems) #dataitems)
            reg_id = dataitems['id']
            self.set_region(dataitems)
            print(dataitems['id'])
        #
        # all_id.sort()
        # print(all_id)

    # @staticmethod
    def open_json_region(self):
        print('start open_json_region')
        with open("Data/avito_region.json", encoding='utf-8') as file:
            self.data = json.load(file)
            # list_dict(data)
        self.list_region()
        # print(f'self.data \n {self.data} \n self.data')
        #     return data


class City:
    pass


class test:
    def say(self):
        print('start_')


def main():
    #     print("Hello")
    # open_region_js()
    region_json_to_aparser()
    # region_list_from_db()


#     pass


#class Command(BaseCommand):
    help = 'Парсинг Avito'
    def handle(self, *args, **options):
        # main()
        # p = MyCustomAuth()
        # print(p.test())
        # p = AvitoParser()
        # p.parse_all()
        # s = Region_set()
        # print(s)
        # s.find_task()
        # s.open_json_region()
        # s.Open_json_region(self)
        region_list_from_db()

if __name__ == '__main__':
    main()
