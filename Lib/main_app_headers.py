#import psycopg2
#import asyncio
#import threading
#import logging
#import datetime
#import json
import httpx
import ssl
from lxml import html

#ssl_context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_CLIENT)  # +PROTOCOL_TLS_CLIENT) #PROTOCOL_TLS)#
ssl_context = httpx.create_ssl_context()
# ssl.PROTOCOL_TLS - Selects the highest protocol version that both the client and server support.
# Despite the name, this option can select both "SSL" and "TLS" protocols.

# set protocol to use
ssl_context.set_alpn_protocols(["h2"])


class AvitoScraperHead():
    def __init__(self):
        self.ssl_context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_CLIENT)
        self.ssl_context = httpx.create_ssl_context()
        self.ssl_context.set_alpn_protocols(["h2"])
        self.key = 'af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir'
        CIPHERS = 'ECDH+AESGCM:ECDH+CHACHA20:DH+AESGCM:DH+CHACHA20:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:ECDH+HIGH:DH+HIGH:RSA+AESGCM:RSA+AES:RSA+HIGH:!aNULL:!eNULL:!MD5:!3DES'
        self.ssl_context.set_ciphers(CIPHERS)

        url_api_10 = 'https://m.avito.ru/api/10/items'
        url_api_web1 = 'https://www.avito.ru/web/1/main/items'
        self.url_0 = str(
            'https://www.avito.ru/rostovskaya_oblast/mototsikly_i_mototehnika?cd=1&q=скутер&f=ASgCAgECAUXGmgwXeyJmcm9tIjoyMDAwLCJ0byI6NzAwMH0')

        # self.url = url_api_web1
        self.url = self.url_0

    def parse_xml(self, resp_text):
        html_txt = resp_text  # response.text
        #    with open('test.html', 'w') as output_file:
        #        output_file.write(html_txt.text.encode('cp1251'))
        # doc = lxml.html.fromstring(resp_text.content)
        print('doc############################################')
        path_url_canonical = './/head//link[@rel="canonical"]//@href'  # './/head/link[@rel="canonical"]' <link data-rh="true" rel="canonical" href="https://www.avito.ru/rostovskaya_oblast/mototsikly_i_mototehnika?q=%D1%81%D0%BA%D1%83%D1%82%D0%B5%D1%80">
        path_url_alternate1 = './/head//link[@rel="alternate"]//@href'  # <link data-rh="true" rel="alternate" media="only screen and (max-width: 640px)" href="https://m.avito.ru/rostovskaya_oblast/mototsikly_i_mototehnika?q=%D1%81%D0%BA%D1%83%D1%82%D0%B5%D1%80">
        path_url_alternate2 = './/head//link[substring(@href,1,7)="android"]//@href'  # <link data-rh="true" rel="alternate" href="android-app://com.avito.android/ru.avito/1/items?categoryId=14&amp;locationId=651110&amp;priceMax=7000&amp;priceMin=2000&amp;query=%D1%81%D0%BA%D1%83%D1%82%D0%B5%D1%80">
        path_url_alternate3 = './/head//link[substring(@href,1,7)="ios-app"]//@href'  # <link data-rh="true" rel="alternate" href="ios-app://417281773/ru.avito/1/items?categoryId=14&amp;locationId=651110&amp;priceMax=7000&amp;priceMin=2000&amp;query=%D1%81%D0%BA%D1%83%D1%82%D0%B5%D1%80">
        # //div[substring(@class,1,13) ="iva-item-text"]'

        path_title = './/div[substring(@class,1,13) ="iva-item-desc"]//text()'
        path_name = './/h3[@itemprop="name"]/text()'
        path_price_long = './/div[@elementtiming="bx.catalog.container"]//div[@data-item-id]//meta[@itemprop="price"]'

        path_price_old = './/meta[@itemprop="price"]'
        # path_price = './/meta[@itemprop="price"]//content'
        path_trader_long = './/div[@elementtiming="bx.catalog.container"]//div[@data-item-id]//div[@data-marker="item-line"]//a'
        path_trader = './/div[@data-marker="item-line"]//a/text()'
        # preceding-sibling
        # path_descrip_full = './/div[@elementtiming="bx.catalog.container"]//div[@data-item-id]//div[@data-marker="item-line"]//preceding-sibling::div[1]//div/text()'
        path_descrip = './/preceding-sibling::div[1]//div/text()'

        ##!!!!!!!####!!!!!!###!!!!#БОМБА ## БОМБА ## БОМБА ## БОМБА ## БОМБА ## БОМБА ## БОМБА ## БОМБА
        # substring(@class,1,13) ="iva-item-text"
        path_descrip_full = './/div[@elementtiming="bx.catalog.container"]//div[@data-item-id]//div[substring(@class,1,13) ="iva-item-text"]'
        # path_descrip_full_text ='.//div[@elementtiming="bx.catalog.container"]//div[@data-item-id]//div[substring(@class,1,13) ="iva-item-text"]//text()'

        # //h1[contains(text(),’ Log in to’)] Когда если известна часть постоянно видимого текста или атрибута. https://habr.com/ru/company/otus/blog/533354/
        # path_descrip_full_text ='.//div[@elementtiming="bx.catalog.container"]//div[@data-item-id]//div[contains(@class,"iva-item-text")]//text()'

        # //h1[starts-with(text(),’Log in ’)] если известна ПЕРВАЯ часть постоянно видимого текста или атрибута.
        # path_descrip_full_text = './/div[@elementtiming="bx.catalog.container"]//div[@data-item-id]//div[starts-with(@class,"iva-item-text")]//text()'

        # starts-with(string, string) https://habr.com/ru/company/otus/blog/533354/
        path_descrip_full_text = './/div[@elementtiming="bx.catalog.container"]//div[@data-item-id]//div[starts-with(@class,"iva-item-text")]//text()'
        path_descrip = './/div[starts-with(@class,"iva-item-text")]//text()'
        path_time_old = './/div[@elementtiming="bx.catalog.container"]//div[@data-item-id]//div[@data-marker="item-date"]/text()'
        # following-sibling
        path_location = './/div[@elementtiming="bx.catalog.container"]//div[@data-item-id]//div[@data-marker="item-line"]//following-sibling::div[2]//span'

        # tree = html.fromstring(text)
        #    path_container = './/div[@elementtiming="bx.catalog.container"]//div[@data-marker="catalog-serp"]'
        path_container = './/div[@id="app"]//div[@data-marker="catalog-serp"]'  # //div[@id="app"]

        path_item_full = './/div[@id="app"]//div[@data-marker="catalog-serp"]//div[@data-marker="item"]'
        path_item = '//div[@data-marker="item"]'
        path_item_url = '//a[@href]'
        path_id = ".//@id"
        path_price = './/meta[@itemprop="price"]//@content'
        # path_pages = '//div[contains(@class, "pagination-root")]'
        # path_pages ='//div[contains(@class, "pagination-page")]/a/@href'
        # path_pages = '//div[contains(@class, "pagination-page")]/a[last()]/text()'
        # OK! path_pages = '//div[contains(@class, "pagination-page")]/a[last()-1]/text()'
        # path_pages = '//div[contains(@class, "pagination-page")]/a[last()-1]/text()'
        path_pages = '//div[contains(@class, "pagination-root")]/span[last()-1]/text()'
        # !Не наша деревня поиска OK! path_location = './/span[contains(@class, "geo-addr")]/span/text()'
        path_location_free = './/span[contains(@class, "geo-addr")]/span/text()'
        path_location = './/div[contains(@class, "geo-geo")]/span/span/text()'

        # tree = etree.fromstring(html, etree.HTMLParser())
        # tree = etree.fromstring(html_txt, etree.HTMLParser())
        # print(html_txt)

        tree = html.fromstring(html_txt)
        count_page = tree.xpath(path_pages)

        if count_page:
            count_page = int(count_page[0])
            print(f'Pages count === {count_page}')
        else:
            count_page = 1  # int(tree.xpath(path_pages)[0])
            print(f'Pages count === {count_page}')
        #
        tree = html.fromstring(html_txt)
        index = 0
        #    print("tree.xpath(path_item) №№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№")
        print('tree.xpath(path_url_canonical) !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print(tree.xpath(path_url_canonical)[0])
        print('tree.xpath(path_url_alternate1) !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print(tree.xpath(path_url_alternate1)[0])
        print('tree.xpath(path_url_alternate2) !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print(tree.xpath(path_url_alternate2)[0])
        print('tree.xpath(path_url_alternate3) !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print(tree.xpath(path_url_alternate3)[0])
        # url_canonical =

        for item in tree.xpath(path_item):  # .getall():
            # for item in tree.xpath(path_location):  # .getall():

            # del item_id = item.xpath(".//@id")
            item_id = item.xpath(path_id)
            print(f'ITEM_ID {item.xpath(path_id)[0]} type{type(item_id)} {item.xpath(path_id)[0]}')
            name = item.xpath(path_name)[0]
            price = item.xpath(path_price)
            location = item.xpath(path_location)
            location_free = item.xpath(path_location_free)

            print(location_free)
            print(f'!!!!!!!!!!!!NAME {name} @@@@ ЦЕНА {price} Location {location}')
            # count_p2 = item.xpath(path_pages)#int(tree.xpath(path_pages)[-1])
            # print(f'Pages count === {count_p2}')

            index += 1
            description = ""
            # description = item.xpath('//div[substring(@class,1,13) ="iva-item-text"]//text()')
            # path_title = './/div[substring(@class,1,13) ="iva-item-desc"]//text()'
            title = item.xpath(path_title)[0]
            # title = item.xpath('.//div[@class="iva-item-descriptionStep-QGE8Y"]//text()')[0]

            # .//link[@rel = "canonical"]
            # description = item.xpath('./div[@class="description"]/text()')
            #        if index < 10:
            # print(etree.tostring(item), name, description)
            print(f' {index} title = {title}')
            # index +=1
            # print(index)

    ####################################################################################
    def get_url(self, url):
        print('def get_url(self):')
        self.url_0 = url
        r = httpx.get(self.url_0, verify=self.ssl_context)
        # response = httpx.get(url, verify=ssl_context)
        #print(r.text)
        self.parse_xml(r.text)
        #parse_xml_1(r.text)



# class test():
#     def say(self) -> str:
#         print('start_')


# class Command(BaseCommand):
#     # help = 'The Zen of Python'
#     #
#     # def handle(self, *args, **options):
#     #     import this
#     help = 'Парсинг Avito'
#
#     def handle(self, *args, **options):
#         # p = AvitoParser()
#         # p.parse_all()
#         s = test()
#         s.say()


if __name__ == '__main__':
    head_list = AvitoScraperHead()
    url_get = "https://www.avito.ru/rostovskaya_oblast/bytovaya_elektronika?cd=1&q=e-mu+1616"
    head_list.get_url(url_get)  # parse_xml()
    #start_main()
################################################################################################
'''
def start_main():
    # con = create_db_sql()
    # print(con)

    # CIPHERS = """ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-SHA256:AES256-SHA"""
    # session = requests.session()
    # session = HTMLSession()
    # adapter = TlsAdapter(ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1)
    # session.mount("https://", adapter)

    try:
        url_api_9 = 'https://m.avito.ru/api/9/items'  # Урл первого API, позволяет получить id и url объявлений по заданным фильтрам
        url_0 = 'https://www.avito.ru/rostov-na-donu/mototsikly_i_mototehnika/mopedy_i_skutery-ASgBAgICAUQ82gE?f=ASgBAgECAUQ82gEBRcaaDBZ7ImZyb20iOjMwMCwidG8iOjcwMDB9&q=%D1%81%D0%BA%D1%83%D1%82%D0%B5%D1%80&radius=100'
        # url_0 = 'https://www.avito.ru/rostov-na-donu/mototsikly_i_mototehnika/mopedy_i_skutery-ASgBAgICAUQ82gE?f=ASgBAgECAUQ82gEBRcaaDBZ7ImZyb20iOjMwMCwidG8iOjgwMDB9&q=скутер&radius=100'
        # https://www.avito.ru/rostov-na-donu/mototsikly_i_mototehnika/mopedy_i_skutery-ASgBAgICAUQ82gE?f=ASgBAgECAUQ82gEBRcaaDBR7ImZyb20iOjAsInRvIjoxMDAwfQ&q=скутер?pmax=7000&pmin=2000&radius=100
        # ?pmax=7000&pmin=2000
        # &forceLocation=1&localPriority=1
        url_0 = 'https://www.avito.ru/rostov-na-donu/mototsikly_i_mototehnika/mopedy_i_skutery/?radius=100&p=2&forceLocation=1&localPriority=1&pmin=1000&pmax=10000'
        url_0 = 'https://www.avito.ru/rostovskaya_oblast/mototsikly_i_mototehnika?cd=1&q=скутер&forceLocation=1&localPriority=1&pmax=7000&pmin=2000&s=1'
        url_0 = str(
            'https://www.avito.ru/rostovskaya_oblast/mototsikly_i_mototehnika?cd=1&q=скутер&s=1&f=ASgCAgECAUXGmgwXeyJmcm9tIjoyMDAwLCJ0byI6NzAwMH0')
        # &q' + '=скутер&s=1')
        # url_0 = 'https://www.avito.ru/rostov-na-donu?cd=1&q=e-mu+1616'
        url_av_1 = 'https://www.avito.ru/novosibirsk/muzykalnye_instrumenty/midi-klaviatura_cme_u-key_2521013620'
        url_av = url_0
        print(f'url_av = _{str(url_av)}')
        url_api = 'https://m.avito.ru/api/10/items?key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir&categoryId=9&params%5B1283%5D=14756&locationId=640000&params%5B110000%5D=329273&withImagesOnly=1&page=1&lastStamp=1611316560&display=list&limit=30'
        # url_av = url_api

        # url_av = 'https://m.avito.ru/api/9/items'
        # https://www.avito.ru
        # r = session.request('GET', url_av)
        r = httpx.get(url_av, verify=ssl_context)
        # response = httpx.get(url, verify=ssl_context)
        # print(r.text)
        parse_xml(r.text)
    #        parse_xml(url)
    #        print(r.text)#[1000])#[1000]
    #        parse_xml(url)
    except Exception as exception:
        print(exception)
        
        
'''
'''
def parse_xml_1(resp_text):
    html_txt = resp_text  # response.text
    #    with open('test.html', 'w') as output_file:
    #        output_file.write(html_txt.text.encode('cp1251'))
    # doc = lxml.html.fromstring(resp_text.content)
    print('doc############################################')
    path_url_canonical = './/head//link[@rel="canonical"]//@href'  # './/head/link[@rel="canonical"]' <link data-rh="true" rel="canonical" href="https://www.avito.ru/rostovskaya_oblast/mototsikly_i_mototehnika?q=%D1%81%D0%BA%D1%83%D1%82%D0%B5%D1%80">
    path_url_alternate1 = './/head//link[@rel="alternate"]//@href'  # <link data-rh="true" rel="alternate" media="only screen and (max-width: 640px)" href="https://m.avito.ru/rostovskaya_oblast/mototsikly_i_mototehnika?q=%D1%81%D0%BA%D1%83%D1%82%D0%B5%D1%80">
    path_url_alternate2 = './/head//link[substring(@href,1,7)="android"]//@href'  # <link data-rh="true" rel="alternate" href="android-app://com.avito.android/ru.avito/1/items?categoryId=14&amp;locationId=651110&amp;priceMax=7000&amp;priceMin=2000&amp;query=%D1%81%D0%BA%D1%83%D1%82%D0%B5%D1%80">
    path_url_alternate3 = './/head//link[substring(@href,1,7)="ios-app"]//@href'  # <link data-rh="true" rel="alternate" href="ios-app://417281773/ru.avito/1/items?categoryId=14&amp;locationId=651110&amp;priceMax=7000&amp;priceMin=2000&amp;query=%D1%81%D0%BA%D1%83%D1%82%D0%B5%D1%80">
    # //div[substring(@class,1,13) ="iva-item-text"]'

    path_title = './/div[substring(@class,1,13) ="iva-item-desc"]//text()'
    path_name = './/h3[@itemprop="name"]/text()'
    path_price_long = './/div[@elementtiming="bx.catalog.container"]//div[@data-item-id]//meta[@itemprop="price"]'

    path_price_old = './/meta[@itemprop="price"]'
    # path_price = './/meta[@itemprop="price"]//content'
    path_trader_long = './/div[@elementtiming="bx.catalog.container"]//div[@data-item-id]//div[@data-marker="item-line"]//a'
    path_trader = './/div[@data-marker="item-line"]//a/text()'
    # preceding-sibling
    # path_descrip_full = './/div[@elementtiming="bx.catalog.container"]//div[@data-item-id]//div[@data-marker="item-line"]//preceding-sibling::div[1]//div/text()'
    path_descrip = './/preceding-sibling::div[1]//div/text()'

    ##!!!!!!!####!!!!!!###!!!!#БОМБА ## БОМБА ## БОМБА ## БОМБА ## БОМБА ## БОМБА ## БОМБА ## БОМБА
    # substring(@class,1,13) ="iva-item-text"
    path_descrip_full = './/div[@elementtiming="bx.catalog.container"]//div[@data-item-id]//div[substring(@class,1,13) ="iva-item-text"]'
    # path_descrip_full_text ='.//div[@elementtiming="bx.catalog.container"]//div[@data-item-id]//div[substring(@class,1,13) ="iva-item-text"]//text()'

    # //h1[contains(text(),’ Log in to’)] Когда если известна часть постоянно видимого текста или атрибута. https://habr.com/ru/company/otus/blog/533354/
    # path_descrip_full_text ='.//div[@elementtiming="bx.catalog.container"]//div[@data-item-id]//div[contains(@class,"iva-item-text")]//text()'

    # //h1[starts-with(text(),’Log in ’)] если известна ПЕРВАЯ часть постоянно видимого текста или атрибута.
    # path_descrip_full_text = './/div[@elementtiming="bx.catalog.container"]//div[@data-item-id]//div[starts-with(@class,"iva-item-text")]//text()'

    # starts-with(string, string) https://habr.com/ru/company/otus/blog/533354/
    path_descrip_full_text = './/div[@elementtiming="bx.catalog.container"]//div[@data-item-id]//div[starts-with(@class,"iva-item-text")]//text()'
    path_descrip = './/div[starts-with(@class,"iva-item-text")]//text()'
    path_time_old = './/div[@elementtiming="bx.catalog.container"]//div[@data-item-id]//div[@data-marker="item-date"]/text()'
    # following-sibling
    path_location = './/div[@elementtiming="bx.catalog.container"]//div[@data-item-id]//div[@data-marker="item-line"]//following-sibling::div[2]//span'

    # tree = html.fromstring(text)
    #    path_container = './/div[@elementtiming="bx.catalog.container"]//div[@data-marker="catalog-serp"]'
    path_container = './/div[@id="app"]//div[@data-marker="catalog-serp"]'  # //div[@id="app"]

    path_item_full = './/div[@id="app"]//div[@data-marker="catalog-serp"]//div[@data-marker="item"]'
    path_item = '//div[@data-marker="item"]'
    path_item_url = '//a[@href]'
    path_id = ".//@id"
    path_price = './/meta[@itemprop="price"]//@content'
    # path_pages = '//div[contains(@class, "pagination-root")]'
    # path_pages ='//div[contains(@class, "pagination-page")]/a/@href'
    # path_pages = '//div[contains(@class, "pagination-page")]/a[last()]/text()'
    # OK! path_pages = '//div[contains(@class, "pagination-page")]/a[last()-1]/text()'
    # path_pages = '//div[contains(@class, "pagination-page")]/a[last()-1]/text()'
    path_pages = '//div[contains(@class, "pagination-root")]/span[last()-1]/text()'
    # !Не наша деревня поиска OK! path_location = './/span[contains(@class, "geo-addr")]/span/text()'
    path_location_free = './/span[contains(@class, "geo-addr")]/span/text()'
    path_location = './/div[contains(@class, "geo-geo")]/span/span/text()'

    # tree = etree.fromstring(html, etree.HTMLParser())
    # tree = etree.fromstring(html_txt, etree.HTMLParser())
    # print(html_txt)

    tree = html.fromstring(html_txt)
    count_page = tree.xpath(path_pages)

    if count_page:
        count_page = int(count_page[0])
        print(f'Pages count === {count_page}')
    else:
        count_page = 1  # int(tree.xpath(path_pages)[0])
        print(f'Pages count === {count_page}')
    #
    tree = html.fromstring(html_txt)
    index = 0
    #    print("tree.xpath(path_item) №№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№")
    print('tree.xpath(path_url_canonical) !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    print(tree.xpath(path_url_canonical)[0])
    print('tree.xpath(path_url_alternate1) !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    print(tree.xpath(path_url_alternate1)[0])
    print('tree.xpath(path_url_alternate2) !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    print(tree.xpath(path_url_alternate2)[0])
    print('tree.xpath(path_url_alternate3) !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    print(tree.xpath(path_url_alternate3)[0])
    # url_canonical =

    for item in tree.xpath(path_item):  # .getall():
        # for item in tree.xpath(path_location):  # .getall():

        # del item_id = item.xpath(".//@id")
        item_id = item.xpath(path_id)
        print(f'ITEM_ID {item.xpath(path_id)[0]} type{type(item_id)} {item.xpath(path_id)[0]}')
        name = item.xpath(path_name)[0]
        price = item.xpath(path_price)
        location = item.xpath(path_location)
        location_free = item.xpath(path_location_free)

        print(location_free)
        print(f'!!!!!!!!!!!!NAME {name} @@@@ ЦЕНА {price} Location {location}')
        # count_p2 = item.xpath(path_pages)#int(tree.xpath(path_pages)[-1])
        # print(f'Pages count === {count_p2}')

        index += 1
        description = ""
        # description = item.xpath('//div[substring(@class,1,13) ="iva-item-text"]//text()')
        # path_title = './/div[substring(@class,1,13) ="iva-item-desc"]//text()'
        title = item.xpath(path_title)[0]
        # title = item.xpath('.//div[@class="iva-item-descriptionStep-QGE8Y"]//text()')[0]

        # .//link[@rel = "canonical"]
        # description = item.xpath('./div[@class="description"]/text()')
        #        if index < 10:
        # print(etree.tostring(item), name, description)
        print(f' {index} title = {title}')
        # index +=1
        # print(index)

    # list_lxml = tree.xpath(path)[0]
    # items_lxml = list_lxml.xpath('//div[@class = "iva-item-descriptionStep-QGE8Y"]//text()')
    # for item_lxml in items_lxml:
    #     desript = item_lxml.xpath('//meta[@itemprop="description"]')
    # print(desript)
    #     # getting movie id
    #     movie_link = item_lxml.xpath('.//div[@class = "nameRus"]/a/@href')[0]


'''


################################################################################################
# ad_id = str(i['value']['id'])
# val = i['value']
# print(f'val  {val}')
# category = val['category']
# print(f'category  {category}')
# time = val['time']
# print(f'time  {time}')
# title = val['title']
# print(f'title  {title}')
# images = ''
# price = val['price']
# print(f'price  {price}')
# address = val['address']
# print(f'address  {address}')
# coords = val['coords']
# print(f'coords  {coords}')
# uri = val['uri']
# print(f'uri  {uri}')
# uri_mweb = val['uri_mweb']
# print(f'uri_mweb  {uri_mweb}')
