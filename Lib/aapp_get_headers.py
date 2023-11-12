# from urllib.parse import urlparse, parse_qs
import httpx
from lxml import html
from urllib.parse import urlparse, parse_qs
from config import get_ssl_context, xpath_mapping, CIPHERS, avito_key, name_column_1, name_column_2, url_get, url_get1, \
    url_get2, url_get3


class AvitoScraperHead:
    def __init__(self):
        #############################################
        self.ssl_context = get_ssl_context()
        self.key = avito_key  # 'af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir'
        self.ssl_context.set_ciphers(CIPHERS)
        ############################################

    def get_attr_dict(self):
        my_dict = {name: None for name in name_column_1}
        return my_dict

    def get_head_attr_dict(self):
        my_dict = {name: None for name in name_column_2}
        return my_dict

    def parse_slug(self, url_parse):
        parsed_url = urlparse(url_parse[0])
        scheme = parsed_url.scheme
        netloc = parsed_url.netloc
        path = parsed_url.path
        path_parts = parsed_url.path.split("/")
        params = parsed_url.params
        query = parsed_url.query
        fragment = parsed_url.fragment
        parsed_query = parse_qs(query)

        print(
            f'    parse_slug: \nScheme: {scheme},  Netloc: {netloc}, Path: {path}, Path parts: {path_parts}, Params: {params}'
            f'Query: {query}, Parsed Query: {parsed_query}, Fragment: {fragment}\n')
        return parsed_query
        # dict_attr = self.get_attr_dict()
        # dict_head_attr = self.get_head_attr_dict()
        # print('dict_attr', dict_attr)
        # print('dict_head_attr', dict_head_attr)

    def parse_xml(self, resp_text):
        html_txt = resp_text
        tree = html.fromstring(html_txt)
        result = {}

        for key, xpath in xpath_mapping.items():
            value = tree.xpath(xpath)
            result[key] = value
            print(key, "=====", result[key])

        url_canonical = result.get('path_url_canonical', None)
        print(url_canonical)
        if url_canonical:
            # self.parse_slug(url_canonical)
            parsed_url = urlparse(url_canonical[0])
            print(f"\n \nurl_canonical: {url_canonical}\n parsed_url path.split {parsed_url.path.split('/')}")
        # dict_head_attr
        # {'id': None, 'title': None, 'url_canonical': None, 'url_alternate1': None, 'url_alternate2': None,
        #  'status': None, 'category_kod': None, 'city_kod': None, 'reg_kod': None, 'search_filter': None,
        #  'search_key': None, 'search_memo': None, 'search_parametrs_api': None, 'search_parametrs_web': None,
        #  'slug_category': None, 'slug_city': None, 'slug_reg': None, 'priceMax': None, 'priceMin': None}

        url_alternate1 = result.get('path_url_alternate1', None)
        #print(f'\nurl_alternate1========={url_alternate1}')
        if url_alternate1:
            #print(f"url_alternate1: {url_alternate1}")
            #self.parse_slug(url_alternate1)
            parsed_url = urlparse(url_alternate1[0])
            print(f"url_alternate1: {url_alternate1}\n parsed_url path.split {parsed_url.path.split('/')}")


        url_alternate2 = result.get('path_url_alternate2', None)
        print(f'\nurl_alternate2========={url_alternate2}')

        if url_alternate2:
            #print(f"url_alternate2: {url_alternate2}")
            self.parse_slug(url_alternate2)
            parsed_url = urlparse(url_alternate2[0])
            query = parsed_url.query
            parsed_query = parse_qs(query)

            # print(
            #     f'    parse_slug: \nScheme: {scheme},  Netloc: {netloc}, Path: {path}, Path parts: {path_parts}, Params: {params}'
            #     f'Query: {query}, Parsed Query: {parsed_query}, Fragment: {fragment}\n')
            print(f"url_alternate2: {url_alternate2}\n parsed_url.parsed_query {parsed_query}")



        url_alternate3 = result.get('path_url_alternate3', None)
        print(f'\nurl_alternate3========={url_alternate3}')
        if url_alternate3:
            print(f"url_alternate3: {url_alternate3}")
            ParsQuer = self.parse_slug(url_alternate3)  #
            print(ParsQuer)

    def get_url(self, url):
        self.url_0 = url
        response = httpx.get(url, verify=self.ssl_context)
        self.parse_xml(response.text)


if __name__ == '__main__':
    head_list = AvitoScraperHead()
    head_list.get_url(url_get3)  # parse_xml()
    # From config.py
    # url_get = "https://www.avito.ru/all?cd=1&d=1&f=ASgCAgECAUXGmgwXeyJmcm9tIjoxMDAwLCJ0byI6ODAwMH0&q=e-mu+1616&s=1"  # 'locationId': ['621540']
    # url_get2 = 'https://www.avito.ru/rostovskaya_oblast?cd=1&d=1&f=ASgCAgECAUXGmgwXeyJmcm9tIjoxMDAwLCJ0byI6ODAwMH0&q=e-mu+1616&s=1'  # 'locationId': ['651110']
    # url_get3 = 'https://www.avito.ru/rostovskaya_oblast_aksay/bytovaya_elektronika?cd=1&d=1&q=e-mu+1212&s=1'  # 'locationId': ['651130']

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
