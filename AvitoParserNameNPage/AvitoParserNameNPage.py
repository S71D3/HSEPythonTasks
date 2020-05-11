# -*- coding: utf-8 -*-
"""
Created on Mon May 11 03:51:39 2020

@author: S11De
"""

import requests #парсинг HTML и XML документов
from bs4 import BeautifulSoup as bs#делаем красивенько)

def GetData():    
    # print('введите поисковой запрос: ')
    # search = input()
    # print('введите страницу для поиска: ')
    # page = int(input())
    # return [search, page]
    return ['пиво', 100]

def Parse(search, page):    
    page = requests.get('https://www.avito.ru/moskva?q='+search+'&p='+str(page)) #переход на нужную страницу нужного запроса
    soup = bs(page.text, "lxml") #собираем суп страницы для работы
    soup.prettify() #перегоняем в красивый вид
    
    trade_list = soup.find_all('div', {'class': 'item_table-wrapper'}) #получаем список из объявлений
    #print(len(trade_list)) #кол-во объявлений на странице
    
    for i in trade_list: #работаем с блоками каждого объявления отдельно
        title = i.find('div', class_ = 'snippet-title-row').find('a', class_='snippet-link')['title'] #название объявления
        link = i.find('div', class_='snippet-title-row').find('a', class_='snippet-link')['href'] #ссылка без начала, надо начало в глобалы
        price = i.find('span', class_='snippet-price').text #цена в сыром виде, потом почистим сплитом
        
        try:
            metro = i.find('span', class_='item-address-georeferences-item__content').text #метро (добавить эксепшн?) #добавили
            try:
                metroDist = i.find('span', class_='item-address-georeferences-item__after').text #дистанция до метро в сыром виде
            except (TypeError, AttributeError): #проверка на наличие расстояния до метро
                metroDist = 'None'
        except (TypeError, AttributeError): #проверка на наличие метро
            metro = 'None'

        print(title + ' ' + price + ' ' + metro + ' ' + metroDist)
        print('\n')
    
    return soup

def Output(result):
    # #print(result)
    # f = open('text.txt', 'w')
    # # for sub_heading in result.find_all('h3'):
    # #     print(sub_heading.text)
    
    
    # temp = result.select('.item-address-georeferences-item__content') #название метро
    # #temp = result.select('h3') #цена
    
    # #print(temp)
    
    # for i in temp:
    #     # f.write(str(i))
    #     # f.write('\n')
    #     print(i)
    #     print('\n')
    
    # f.close()
    
    return 0

def main():
    
    data = GetData()
    result = Parse(data[0], data[1])
    Output(result)
    return 0

main()