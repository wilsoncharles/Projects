#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 26 15:54:20 2022

@author: wilson
"""

from AQI_average import avg_pm25
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import csv

def table_html(year,month):
    
    html_file = open("Data/Html_data/{}/{}.html".format(year,month),'rb')
    plain_text = html_file.read()
    all_value = []
    final_value = []
    soup = BeautifulSoup(plain_text,'html.parser')
    for table in soup.findAll('table',{'class':"medias mensuales numspan"}):
        #print(table)
        for tbody in table:
            for tr in tbody:
                value= tr.get_text()
                all_value.append(value)
    #print(all_value)
    
                
    rows= len(all_value)/15
    
    for times in range(round(rows)):
        newtemp = []
        for i in range(15):
            newtemp.append(all_value[0])
            all_value.pop(0)
        final_value.append(newtemp)
    
    length=len(final_value)
    final_value.pop(length-1)
    final_value.pop(0)
    
    for i in range(len(final_value)):
        final_value[i].pop(14)
        final_value[i].pop(13)
        final_value[i].pop(12)
        final_value[i].pop(11)
        final_value[i].pop(10)
        final_value[i].pop(4)
        final_value[i].pop(0)
    
    #print(final_value[1][4])
    #print(final_value[1][10])
    #print(final_value[1][11])
    #print(final_value[1][12])
    #print(final_value[1][13])
    #print(final_value[1][14])
    #print(final_value[1][0])
    
    #print(final_value)
    return final_value

def combine_data(year,cs):
    for a in pd.read_csv('Data/Real-Data/real_'+str(year)+'.csv',chunksize=cs):
        df = pd.DataFrame(data=a)
        mylist = df.values.tolist()
        #print(mylist)
    return mylist

if __name__ == '__main__':
    if not os.path.exists("Data/Real-Data"):
        os.makedirs("Data/Real-Data")
    for year in range(2013,2019):
        final_data = []
        with open('Data/Real-Data/real_'+str(year)+'.csv','w') as csvfile:
            wr = csv.writer(csvfile,dialect='excel')
            wr.writerow(['T', 'TM', 'Tm', 'SLP', 'H', 'VV', 'V', 'VM', 'PM 2.5'])
        
        for month in range(1,13):
            tablev = table_html(year,month)
            final_data = final_data + tablev
        
        pm = avg_pm25(year)
        
        for i in range(len(final_data)-1):
            final_data[i].insert(8,pm[i])
        
        
        with open('Data/Real-Data/real_'+str(year)+'.csv','a') as csvfile:
            wr = csv.writer(csvfile, dialect = 'excel')
            for row in final_data:
                flag=0
                for elem in row:
                    if elem =="" or elem =="-":
                        flag = 1
                if flag !=1:
                    wr.writerow(row)
        
    data_2013 = combine_data(2013, 600)
    data_2014 = combine_data(2014, 600)
    data_2015 = combine_data(2015, 600)
    data_2016 = combine_data(2016, 600)
    data_2017 = combine_data(2017, 600)
    data_2018 = combine_data(2018, 600)
    
    total = data_2013+data_2014+data_2015+data_2016+data_2017+data_2018
    #print(total)
    
    with open('Data/Real-Data/Combined_Data.csv','w') as csvfile:
        wr = csv.writer(csvfile, dialect='excel')
        wr.writerow(['T', 'TM', 'Tm', 'SLP', 'H', 'VV', 'V', 'VM', 'PM 2.5'])
        wr.writerows(total)
    
    df=pd.read_csv('Data/Real-Data/Combined_Data.csv')
    
