# -*- coding: utf-8 -*-
"""
Created on Sat Nov 13 16:57:23 2021

@author: Hydra18
"""

from bs4 import BeautifulSoup
import pandas as pd
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

melon = pd.read_csv('C:/Users/Hydra18/Desktop/텍스트이해와인공지능/Project/Dataset/Samples.csv', encoding = 'utf-8')
melon.head()

option = Options()
option.add_argument("disable-infobars")
option.add_argument("disable-extensions")
option.add_argument('disable-gpu')
option.add_argument('headless')
option.add_argument('enable-automation')
option.add_argument('disable-dev-shm-usage')
option.add_argument('dns-prefetch-disable')
option.add_argument('no-sandbox')
option.add_argument('disable-browser-side-navigation')

def LyricsTranslator():
    with open('C:/Users/Hydra18/Desktop/텍스트이해와인공지능/Project/Dataset/Translation/KR-EN/Translated-Kor-Eng.csv', 'w', encoding='utf-8-sig', newline='') as file:
        csvfile = csv.writer(file)
        
        url = 'https://papago.naver.com/?sk=ko&tk=en' # 한글 --> 영어로 
        
        browser = webdriver.Chrome(executable_path='C:/Users/Hydra18/Pictures/chromedriver/chromedriver.exe', chrome_options=option)
        browser.maximize_window()
        browser.get(url)
        browser.implicitly_wait(10)
        time.sleep(10)
        
        for i in range(101): # 음악 곡 갯수만큼 변경이 필요함 
            temp_list = []
            browser.find_element_by_xpath('/html/body/div/div/div[1]/section/div/div[1]/div[1]/div/div[3]/label/textarea').click()
            time.sleep(3)
            browser.find_element_by_xpath('/html/body/div/div/div[1]/section/div/div[1]/div[1]/div/div[3]/label/textarea').clear()
            time.sleep(5)
            browser.find_element_by_xpath('/html/body/div/div/div[1]/section/div/div[1]/div[1]/div/div[3]/label/textarea').send_keys(melon['Lyrics'][i])
            time.sleep(5)
            browser.find_element_by_xpath('/html/body/div/div/div[1]/section/div/div[1]/div[1]/div/div[4]/div/button/span[1]').click()
            browser.implicitly_wait(10)
            time.sleep(10)
    
            html = browser.page_source
            document = BeautifulSoup(html, 'lxml')
    
            title = ''
            title = melon['Title'][i]   # 곡 제목
    
            artist = ''
            artist = melon['Artist'][i] # 가수 명
    
            lyrics = ''
            lyrics = melon['Lyrics'][i] # 가사 
    
            genre = ''
            genre = melon['Genre'][i] # 장르
    
            year = ''
            year = melon['Year'][i] # 날짜
    
            translated = ''
            translated = document.select('div#txtTarget')[0].text # 번역본
    
            temp_list.append([title, artist, lyrics, genre, year, translated])
    
            for row in temp_list:
                csvfile.writerow(row)
                

LyricsTranslator()