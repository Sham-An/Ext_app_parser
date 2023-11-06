#!/usr/bin/python

# -*- coding: UTF-8 -*-
#<link data-rh="true"
# rel="canonical"
# href="https://www.avito.ru/rostovskaya_oblast/mototsikly_i_mototehnika/mopedy_i_skutery-ASgBAgICAUQ82gE?q=%D1%81%D0%BA%D1%83%D1%82%D0%B5%D1%80"/>
#
#<link data-rh="true"
# rel="alternate"
# media="only screen and (max-width: 640px)"
# href="https://m.avito.ru/rostovskaya_oblast/mototsikly_i_mototehnika/mopedy_i_skutery-ASgBAgICAUQ82gE?q=%D1%81%D0%BA%D1%83%D1%82%D0%B5%D1%80"/>
#
# <link data-rh="true" rel="alternate"
# href="android-app://com.avito.android/ru.avito/1/items?categoryId=14&amp;locationId=651110&amp;params%5B30%5D=109&amp;priceMax=6000&amp;priceMin=2000&amp;query=%D1%81%D0%BA%D1%83%D1%82%D0%B5%D1%80"/>
# items?
# categoryId=14&amp;
# locationId=651110&amp;
# params%5B30%5D=109&amp; params[30]=109
# priceMax=6000&amp;
# priceMin=2000&amp;
# query=%D1%81%D0%BA%D1%83%D1%82%D0%B5%D1%80"/>
#
# <link data-rh="true"
# rel="alternate"
# href="ios-app://417281773/ru.avito/1/items?categoryId=14&amp;locationId=651110&amp;params%5B30%5D=109&amp;priceMax=6000&amp;priceMin=2000&amp;query=%D1%81%D0%BA%D1%83%D1%82%D0%B5%D1%80"/><link data-rh="true" rel="dns-prefetch" href="//tube.buzzoola.com/"/><link data-rh="true" nonce="sTS3e+K8hGPNTV2B9FcHGw==" rel="preload" href="//tube.buzzoola.com/new/build/buzzlibrary.js" as="script"/>
# items?
# categoryId=14&amp;
# locationId=651110&amp;
# params%5B30%5D=109&amp; params[30]=109
# priceMax=6000&amp;
# priceMin=2000&amp;
# query=%D1%81%D0%BA%D1%83%D1%82%D0%B5%D1%80"/>
#
# <link data-rh="true"
# rel="dns-prefetch"
# href="//tube.buzzoola.com/"/>
# <link data-rh="true" nonce="sTS3e+K8hGPNTV2B9FcHGw==" rel="preload" href="//tube.buzzoola.com/new/build/buzzlibrary.js" as="script"/>
#import urllib2

from requests import Request, Session

import demjson

import sys

#reload(sys)

#sys.setdefaultencoding('utf-8')


def writeLine(file, content):
    file.write(content)


def getAppInfo(appid):
    url = "http://itunes.apple.com/lookup?id=%d&country=cn" % (appid)
    s = Session()
    req = Request('GET', url) #, data=data, headers=headers)
#    req = urllib2.Request(url);
#    prepped = s.prepare_request(req)
#    resdata = urllib2.urlopen(req)
    resdata = s.prepare_request(req)
    #print(resdata.conte)

    res = resdata.read()

    json = demjson.decode(res)

    file = "%d.txt" % (appid)

    f = open(file, "w+")

    writeLine(f, ('=====appid=====:\n' + (str)(json['results'][0]['trackId'])) + '\n')

    writeLine(f, ('=====trackName=====:\n' + json['results'][0]['trackName']) + '\n')

    writeLine(f, ('=====description=====:\n' + json['results'][0]['description'] + '\n'))

    writeLine(f, ('=====link=====:\n' + json['results'][0]['trackViewUrl'] + '\n'))

    writeLine(f, ('=====bundleId=====:\n' + (str)(json['results'][0]['bundleId']) + '\n'))

    writeLine(f, ('=====releaseAt=====:\n' + json['results'][0]['currentVersionReleaseDate'] + '\n'))

    writeLine(f, ('=====releaseNotes=====:\n' + json['results'][0]['releaseNotes'] + '\n'))

    writeLine(f, ('=====icon=====:\n' + json['results'][0]['artworkUrl100'] + '\n'))

    writeLine(f, ('=====fileSizeBytes=====:\n' + (str)(json['results'][0]['fileSizeBytes']) + '\n'))

    f.close()


getAppInfo(1102002763);