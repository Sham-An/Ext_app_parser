import main_app_headers as head1
import aapp_get_headers as head2

head_list1 = head1.AvitoScraperHead()
head_list2 = head2.AvitoScraperHead()
##
#    head_list = AvitoScraperHead()
#    url_get = "https://www.avito.ru/rostovskaya_oblast/bytovaya_elektronika?cd=1&q=e-mu+1616"
#    head_list.get_url(url_get)  # parse_xml()
#url = "https://www.avito.ru/rostovskaya_oblast/bytovaya_elektronika?cd=1&q=e-mu+1616"

url0 = "https://www.avito.ru/rostovskaya_oblast?cd=1&q=e-mu+1616&s=1"
url = "https://www.avito.ru/all?cd=1&q=e-mu+1616&s=1"
url2 = "https://www.avito.ru/all/bytovaya_elektronika?q=emu+1212&s=1"
#https://www.avito.ru/web/1/main/items?forceLocation=false&locationId=621540&lastStamp=1611639754&limit=30&offset=30

print('11111111111111111111111111111111111111111111')
#head_list1.get_url(url)

print('2222222222222222222222222222222222222222222')
head_list2.get_url(url2)
