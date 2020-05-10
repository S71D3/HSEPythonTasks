# -*- coding: utf-8 -*-
"""
Created on Mon May 11 03:51:39 2020

@author: S11De
"""

import requests
import bs4 #парсинг HTML и XML документов

def GetData():    
    print('введите поисковой запрос: ')
    search = input()
    print('введите страницу для поиска: ')
    page = int(input())
    return [search, page]

def Parse(search, page):
#    s = requests.get('https://www.avito.ru/moskva?q='+search)
#    b = bs4.BeautifulSoup(s.text, "html.parser")
#    p3 = b.select('.item-params-list .item-params-label')
#    f1 = p3[0].getText()
#    return f1
    
    
    s = requests.get('https://www.avito.ru/tobolsk/avtomobili/toyota_camry_2010_1343073375')
    b = bs4.BeautifulSoup(s.text, "html.parser")
    p3 = b.select('.item-params-list .item-params-label')
    f1 = p3[0].getText()
    return f1

def Output(result):
    print(result)
    return 0

def main():
    
    data = GetData()
    result = Parse(data[0], data[1])
    Output(result)
    return 0

main()