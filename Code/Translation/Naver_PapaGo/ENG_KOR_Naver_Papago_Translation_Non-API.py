# -*- coding: utf-8 -*-
"""
Created on Sat Nov 13 17:06:04 2021

@author: Hydra18
"""


from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


option = Options()
option.add_argument("disable-infobars")
option.add_argument("disable-extensions")
option.add_argument('disable-gpu')
option.add_argument('enable-automation')
option.add_argument('disable-dev-shm-usage')
option.add_argument('dns-prefetch-disable')
option.add_argument('headless')
option.add_argument('no-sandbox')
option.add_argument('disable-browser-side-navigation')

songs = pd.read_csv('C:/Users/Hydra18/Desktop/3000-4000.csv', encoding = 'utf-8-sig')
songs['Translated'] = None

def LyricsTranslator():
    with open('C:/Users/Hydra18/Desktop/텍스트이해와인공지능/Project/Dataset/Translation/EN-KR/Translated-Eng-Kor[3000-4000]700_799까지.csv', 'w', encoding = 'utf-8-sig', newline = '') as file:
        csvfile = csv.writer(file)
        
        url = 'https://papago.naver.com/?sk=en&tk=ko&hn=0' # 영어 --> 한글로 
        
        browser = webdriver.Chrome(executable_path='C:/Users/Hydra18/Pictures/chromedriver/chromedriver.exe', chrome_options = option)
        browser.maximize_window()
        browser.get(url)
        browser.implicitly_wait(10)
        time.sleep(6)
        
        
        for rows in range(700, 800):
            store = []
            for i in range(0, len(songs['Lyrics'][rows].split('\n'))):
                if songs['Lyrics'][rows].split('\n')[i] == '':
                    pass
                else:
                    store.append(songs['Lyrics'][rows].split('\n')[i])
        
            line_by_line = []
            for j in range(0, len(store)):
                x = ''
                x = store[j]
    
                browser.find_element_by_xpath('/html/body/div/div/div[1]/section/div/div[1]/div[1]/div/div[3]/label/textarea').click()
                time.sleep(1)
                browser.find_element_by_xpath('/html/body/div/div/div[1]/section/div/div[1]/div[1]/div/div[3]/label/textarea').clear()
                time.sleep(1)
                browser.find_element_by_xpath('/html/body/div/div/div[1]/section/div/div[1]/div[1]/div/div[3]/label/textarea').send_keys(x)
                time.sleep(3)
                browser.find_element_by_xpath('/html/body/div/div/div[1]/section/div/div[1]/div[1]/div/div[4]/div/button/span[1]').click()
                browser.implicitly_wait(10)
                time.sleep(5)
    
                html = browser.page_source
                document = BeautifulSoup(html, 'lxml')
    
                translated = ''
                translated = document.select('div#txtTarget')[0].text # 번역본
    
                line_by_line.append([translated])
                
            l2 = np.array(line_by_line)
            l3 = l2.reshape(-1)
            l4 = [','.join(l3)]
            songs['Translated'][rows] = l4
            csvfile.writerow(songs['Translated'][rows])
            
            print("Success! ----> " + str(rows))
            
LyricsTranslator()


