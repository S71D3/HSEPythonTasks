# -*- coding: utf-8 -*-
"""
Created on Mon May 11 03:51:39 2020

@author: S11De
"""

import requests #парсинг HTML и XML документов
from bs4 import BeautifulSoup as bs#делаем красивенько)
import pandas as pd

def GetData():    
    print('введите поисковой запрос: ')
    search = input()
    print('введите страницу для поиска: ')
    page = int(input())
    return [search, page]

def SoupToDB(list):
    column_names = ['title', 'link', 'price','metroName','metroDist']
    df = pd.DataFrame(columns = column_names) #сделали нулевой фрейм
    
    for i in list: #работаем с блоками каждого объявления отдельно
        title = i.find('div', class_ = 'snippet-title-row').find('a', class_='snippet-link')['title'] #название объявления
        link = i.find('div', class_='snippet-title-row').find('a', class_='snippet-link')['href'] #ссылка без начала, надо начало в глобалы
        
        price = i.find('span', class_='snippet-price').text #цена в сыром виде, потом почистим сплитом
        temp = price.split(' ') #вот собственно и чистим)
        price = ''
        for j in temp:
             try:
                 temp2 = int(j) #индикатор провокации вызова эксепшена
                 price+=j #добавлям в поле только числа
             except ValueError:
                 pass
        if (price ==''):
             price = 'None' #если поле было "не указано", "по договоренности" и тп (можно потом добавить)
        
        try:
            metroName = i.find('span', class_='item-address-georeferences-item__content').text #метро (добавить эксепшн?) #добавили
        except (TypeError, AttributeError): #проверка на наличие метро
            metroName = 'None'
            
        try:
            metroDist = i.find('span', class_='item-address-georeferences-item__after').text #дистанция до метро в сыром виде
            #вроде не надо чистить, но если надо - можно как в случае с ценой
        except (TypeError, AttributeError): #проверка на наличие расстояния до метро
            metroDist = 'None'

        df = df.append({'title': title, 'link':link, 'price':price, 'metroName':metroName, 'metroDist':metroDist}, ignore_index=True) #добавляем информацию в датафрейм
        
        #print(title + ' ' + price + ' ' + metroName + ' ' + metroDist) #проверка выводом в консоль  
    
    return df

def Parse(search, page):
    siteTitle = 'https://www.avito.ru/'
    cityLinkTitle = 'moskva'
    page = requests.get(siteTitle + cityLinkTitle + '?q=' + search + '&p=' + str(page)) #переход на нужную страницу нужного запроса
    
    soup = bs(page.text, "lxml") #собираем суп страницы для работы
    soup.prettify() #перегоняем в красивый вид
    
    annList = soup.find_all('div', {'class': 'item_table-wrapper'}) #получаем список из объявлений
    #print(len(trade_list)) #кол-во объявлений на странице
    
    df = SoupToDB(annList) #формируем датафрейм из супа с фильтрацией
      
    return df #получили датафрейм, заполненный данными

def Output(result):
    print(result)

def main(): 
    data = GetData()
    result = Parse(data[0], data[1])
    Output(result)

main()