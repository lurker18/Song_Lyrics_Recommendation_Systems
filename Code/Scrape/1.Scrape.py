# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 11:15:35 2021

@author: Hydra18
"""

from bs4 import BeautifulSoup
import pandas as pd
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

option = Options()
option.add_argument("disable-infobars")
option.add_argument("disable-extensions")
option.add_argument('disable-gpu')
option.add_argument('headless')
option.add_argument('enable-automation')
option.add_argument('disable-dev-shm-usage')
option.add_argument('disable-browser-side-navigation')

weekly_dates = pd.date_range('2015-07-05', '2021-10-23', freq='W-SAT')
week_dates = weekly_dates.map(lambda x: x.strftime('%Y-%m-%d'))


"""
//*[@id="charts"]/div/div[7]/div/ol/li[1]/button/span[2]
//*[@id="charts"]/div/div[7]/div/ol/li[2]/button/span[2]
//*[@id="charts"]/div/div[7]/div/ol/li[3]/button/span[2]
"""


def SongCrawler():
    with open('C:/Users/Hydra18/Desktop/텍스트이해와인공지능/Project/Dataset/Top_Songs_2015_2021.csv', 'w', encoding='utf-8-sig', newline='') as file:    
        csvfile = csv.writer(file)
        
        for x in week_dates:
            temp_list = []
            url = 'https://www.billboard.com/charts/hot-100/' + x
        
            browser = webdriver.Chrome(executable_path='C:/Users/Hydra18/Pictures/chromedriver/chromedriver.exe', options = option)
            browser.maximize_window()
            browser.get(url)
            browser.implicitly_wait(15)
            time.sleep(3)

            for i in range(100):
                html = browser.page_source
                document = BeautifulSoup(html, 'lxml')
            
                song_title = ''
                song_title = document.select('span.chart-element__information__song.text--truncate.color--primary')[i].text
                
                song_artist = ''
                song_artist = document.select('span.chart-element__information__artist.text--truncate.color--secondary')[i].text
                
                temp_list.append([x, song_title, song_artist])
    
            for row in temp_list:
                csvfile.writerow(row)


#========================================================================================================#
SongCrawler()
