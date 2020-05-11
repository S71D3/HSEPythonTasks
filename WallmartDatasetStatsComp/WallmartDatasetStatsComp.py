# -*- coding: utf-8 -*-
"""
Created on Mon May 11 19:15:52 2020

@author: S11De
"""

import pandas as pd #работаем с датафреймами
import os #для пути загрузки сета
from datetime import datetime #работа с ячейками с датой
import matplotlib #работа с визуализацией графиками

CSVNAME = 'walmart.csv' #название исходника с датасетом
PERCENTDELETION = 0.6 #сколько процентов пропуска допустимо для переменной

def DownloadDS():
    df = pd.read_csv(os.getcwd()+'/'+CSVNAME) #загрузка по пути запуска исходника
    return df #загружаем дс в датафрейм

def PreWork(df):
    print('Общая информация:')
    print ('Первые 5 записей:\n' + df.head() + '\n') #первые 5, можно было как и последние 5 через илокейт
    print ('Последние 5 записей:\n' + df.iloc[len(df)-5:len(df)] + '\n') #последние 5
    print ('Кол-во наблюдений:\n' + len(df)) #кол-во наблюдений
    
    print('Названия и типы переменных:\n')
    print(df.dtypes) #выводим название и тип
    print('\n')
    
def DateToDate(df):
    print('Изменяем тип переменной даты:')
    df['Date'] = df['Date'].apply(lambda st: datetime.strptime(st, '%Y-%m-%d').date()) #меняем тип через apply с помощью лямбда-функции
    
    #print('Получившийся тип первой ячейки - ' + type(df['Date'][0])) #смотрим тип первого
    #print('Получившийся тип последней ячейки - ' + type(df['Date'][len(df)-1])) #и тип последнего элемента в столбце даты
    #оба выводит datetime.date
    
    print('\n')
    return df #получаем датафрейм со столбцом даты, имеющий тип datatime.date
    
def MissingFields(df):
    print('Информация о пустых полях:')
    
    for column in df: #цикл по столбцам вроде можно
        emptyFCount = df[column].isnull().sum()
        #print('У переменной ' + column + ' ' + str(emptyFCount) + ' пустых полей') #выводим информацию о пропусках
        if (emptyFCount/len(df) > PERCENTDELETION): #если кол-во пустых строк больше PERCENTDELETION процентов, то удаляем столбец
            del df[column]
    
    print('\n')
    return df

def Sampling(df):
    print('Информация о выборке:')
    
    print('Магазинов в датасете ' + str(df.Store.value_counts().size)) #кол-во магазинов
    print('Отделов в датасете ' + str(df.Dept.value_counts().size)) #кол-во отделов
    print('Охватывается промежуток в ' + str((df.Date.max()-df.Date.min()).days) + ' дней') #разница между максимальной и минимальной датами

    print('\n')


def Dynamics(df):
    
    
    
def main():
    df = DownloadDS() #Загружаем датасет в датафрейм
    #PreWork(df) #Первые\последние 5 наблюдений, сколько наблюдений, какой формат переменных
    df = DateToDate(df) #привести Date к формату даты
    df = MissingFields(df) #удаляем переменные, имеющие более 60% пропущенных полей
    #Sampling(df) #работа с выборкой. сколько магазинов и отделов, за какой период времени
    Dynamics() #динамика продаж, график - по оси Х - дата, по оси Y - продажи всей сети
    # Corr() #матрица корреляции числовых показателей
    # Top5() #топ5 самых больших магазинов по сумм. за все время + динамика продаж на одном графике
    # Top10() #топ10 самых больших ОТДЕЛОВ по сумм. за 2011(!) год среди магазинов типа А (!) + столбчатая диаграмма для них

main()