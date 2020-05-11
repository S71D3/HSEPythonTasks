# -*- coding: utf-8 -*-
"""
Created on Sun May 10 20:32:03 2020

@author: S11De
"""

import vk_api #работа с самим апи
import pandas as pd #в основном для датафреймов
import matplotlib.pyplot as plt #визуализация графика

#не пригодились
import time #в теории пригодится для работы с idle апи
import math #работа с матаном на всякий случай

USRCOUNT = 10000 #ориентировочное кол-во пользователей для отбора
USRSTEP = 1000 #шаг проверки пользователей, от 1 до 1000
                #погрешность на кол-во итоговых пользователей после фильтрации (меньше - дольше)
                #при =1 в итоге будет ровно USRCOUNT юзеров, если столько найдется в группе
BDAYCHECKS = 3 #сколько различных комбинаций из 50-и человек проверяем на совпадение дней рождения

def TokenLogin(): #вход с помощью токена
    print('...token authorization...\n')
    
    #https://oauth.vk.com/authorize?client_id=*тутАйДиПриложения*&display=page&scope=friends,news,groups&response_type=token&v=5.103&state=123456
    # как собрать токен тут: https://devman.org/qna/63/kak-poluchit-token-polzovatelja-dlja-vkontakte/
    #можно добавить логин по лог::пасс
    link = '139923997' #id паблика (это femalememes...)
    
    print('input token')
    tokenstring = input() #строка токена, вводить самостоятельно
    
    vk_session = vk_api.VkApi(token=tokenstring)
    return [vk_session.get_api(), link] #получили сессию, авторизировавшись через токен, и айди группы

def ReadAndFilter(vk, groupname, df):
    print('...reading and filtration...\n')
    
    offs= 0 #отступ для последовательного чтения
    thatsall = 0 #не закончили осмотр списка
    maxcount = vk.groups.getById(group_id = groupname, fields = 'members_count')[0]['members_count'] #сколько всего юзеров в группе
    dfsize = 0
    
    while thatsall != 1:
        temp = vk.groups.getMembers(group_id=groupname, offset = offs, count = USRSTEP) #берем USRSTEP ай-дишников пользователей
        offs += USRSTEP
        
        usrDict = vk.users.get(user_ids = temp['items'], fields = 'bdate') #берем нужные данные по ай-ди
        for i in usrDict:
            if ('bdate' in i): #фильтруем по наличию ДР 
                fulldate = i['bdate'].split('.')
                df = df.append({'name': i['first_name'], 'surname':i['last_name'], 'id':i['id'], 'bdateday':fulldate[0], 'bdatemonth':fulldate[1]}, ignore_index=True)
                #добавляем в итоговый датафрейм данные тех, у кого указан ДР
                dfsize +=1 #почему-то с прямым обращением к методу косячит
                
        if (dfsize >= USRCOUNT or offs >= maxcount): #смотрим на выход за границы тестируемого множества или кол-ва участников
            thatsall = 1
    return df #получили датафрейм из USRCOUNT +-USRSTEP юзеров, имеющих дату рождения

def GetUsersList(vk, groupname): #получаем сет пользователей
    print('...getting users...\n')
    
    column_names = ['name', 'surname', 'id','bdateday','bdatemonth']
    df = pd.DataFrame(columns = column_names) #сделали нулевой фрейм
    df = ReadAndFilter(vk, groupname, df) #получаем ПРИМЕРНО usrcount юзеров в лист в обход ограничения + фильтруем (так проще)
                                        #можно сделать ровно usrcount, но уйдет намного больше времени на перебор     
    #print(df.to_string()) #вывод в консоль
    return df #получили датафрейм из USRCOUNT +-USRSTEP юзеров, имеющих дату рождения

def UsersStats(df): #гистограмма, посмотреть похоже ли на равномерное распределение
    print('...stats solving...\n')
    
    lstats = []
    for i in range(12):
        lstats.append(0) #обнуляем лист счетчиков
    
    for i in df['bdatemonth']:
        lstats[int(i)-1] +=1 #считаем кол-во родившихся в каждом месяце
        
    plt.figure() #инициализируем поле
    plt.bar([1,2,3,4,5,6,7,8,9,10,11,12], lstats) #гистограмму нарисовали, на нее посмотрели, на равномерное распределение похоже)
    #построили гистограмму распределения ДР по месяцам

def UsersProbab(df): #вероятность совпадения дней рождения из 50-и произвольных людей
    print('...probability solving...\n')
    
    counter = 0 #счетчик совпадений
    matchlist = [] #список совпавших айдишников
    
    k = 0
    while k != BDAYCHECKS:
        df = df.sample(frac=1).reset_index(drop=True) #перемешиваем строки для обновления первых 50-и записей
        i = 0
        while i != 49:
            j=i+2
            while j != 50:
                if (df['bdatemonth'][i]==df['bdatemonth'][j] and df['bdateday'][i]==df['bdateday'][j]):
                    if not ([df['id'][i], df['id'][j]] in matchlist or [df['id'][j], df['id'][i]] in matchlist):
                        matchlist.append([df['id'][i], df['id'][j]])
                        counter+=1
                j+=1
            i+=1 
        k+=1 #простой перебор всех пар, возможно словарь с поиском был бы быстрее 
    
    print('в ', BDAYCHECKS, ' экспериментах произошло ', counter, ' совпадений дней рождения у пользователей с id:')
    for i in matchlist:
        print(i[0], ' и ', i[1], '\n')

def main():
    session = TokenLogin() #авторизация по токену
    usrdf = GetUsersList(session[0], session[1]) #получаем сет пользователей
    UsersStats(usrdf) #гистограмма, посмотреть похоже ли на равномерное распределение
    UsersProbab(usrdf) #вероятность совпадения дней рождения из 50-и произвольных людей

main()