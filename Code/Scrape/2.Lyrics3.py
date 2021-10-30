# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 00:10:19 2021

@author: Hydra18
"""

from bs4 import BeautifulSoup
import pandas as pd
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


total_song_lists = pd.read_csv('C:/Users/Hydra18/Desktop/텍스트이해와인공지능/Project/Dataset/test2.csv', encoding = 'utf-8')
total_song_lists

total_song_lists['Full'] = total_song_lists['Song'] + ' ' + total_song_lists['Artist']
total_song_lists['Full']

browser_locale = 'en'
option = Options()
option.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
option.add_argument("--lang={}".format(browser_locale))
option.add_argument("disable-infobars")
option.add_argument("disable-extensions")
option.add_argument('disable-gpu')
#option.add_argument('headless')
#option.add_argument('enable-automation')
#option.add_argument('disable-dev-shm-usage')
#option.add_argument('disable-browser-side-navigation')

params = {
    "latitude": 37.774929,
    "longitude": -122.419416,
    "accuracy": 100
}

url = 'http://www.songlyrics.com/index.php?section=search&searchW=Beautiful+Life++%09Nick+Fradiani&submit=Search&searchIn1=artist&searchIn3=songgoogle.com'
browser = webdriver.Chrome(executable_path='C:/Users/Hydra18/Pictures/chromedriver/chromedriver.exe', chrome_options=option)
browser.execute_cdp_cmd("Page.setGeolocationOverride", params)
browser.maximize_window()
browser.get(url)
browser.find_element_by_xpath('//*[@id="header_search"]/form/fieldset/input').click()
browser.find_element_by_xpath('//*[@id="header_search"]/form/fieldset/input').clear()
browser.find_element_by_xpath('//*[@id="header_search"]/form/fieldset/input').send_keys('shazam')
browser.find_element_by_xpath('//*[@id="header_search"]/form/fieldset/div/input').click()
browser.implicitly_wait(10)
time.sleep(1)




def LyricsCrawler():
    with open('C:/Users/Hydra18/Desktop/텍스트이해와인공지능/Project/Dataset/Top_Songs_Lyrics5.csv', 'w', encoding='utf-8-sig', newline='') as file:
        csvfile = csv.writer(file)
        temp = []
        for k in range(len(total_song_lists)):
            temp_list = []
            
            browser.find_element_by_xpath('//*[@id="wrapper"]/div[3]/div[2]/form/input[2]').click()
            browser.find_element_by_xpath('//*[@id="wrapper"]/div[3]/div[2]/form/input[2]').clear()
            browser.find_element_by_xpath('//*[@id="wrapper"]/div[3]/div[2]/form/input[2]').send_keys(total_song_lists['Full'][k])
            browser.find_element_by_xpath('//*[@id="wrapper"]/div[3]/div[2]/form/div[1]/input').click()
            
            try:
                browser.find_element_by_xpath('//*[@id="wrapper"]/div[3]/div[2]/div[3]/a/img').click()
                
            except:
                try:
                    browser.find_element_by_xpath('//*[@id="rso"]/div[1]/div/div/div[1]/div/div/div/div[1]/a/h3').click()
                    
                except:
                    try:
                        browser.find_element_by_xpath('//*[@id="rso"]/div[1]/div/div/div/div[1]/a/h3').click()
                        
                    except:
                        pass
            
            browser.implicitly_wait(10)
            time.sleep(1)

            html1 = browser.page_source
            document = BeautifulSoup(html1, 'lxml')
            
            try:
                lyrics = ''
                lyrics = document.find('p', attrs  = {'id': 'songLyricsDiv'}).text
                line_by_lyrics = lyrics.split('\n')
                line_by_lyrics = str(line_by_lyrics).replace("\'", '').replace('"','').replace(",",'').replace('(',' ').replace(')',' ').replace('[','').replace(']','').replace('  ', ' ')
                
                if total_song_lists['Artist'][k] in document.select('div > h1')[0].text:
                    song = ''
                    song = total_song_lists['Song'][k]
                           
                    artist = ''
                    artist = total_song_lists['Artist'][k]

                    temp_list.append([song, artist, lyrics, total_song_lists['Full'][k]])
                                
                    for row in temp_list:
                        csvfile.writerow(row)
                
                browser.execute_script("window.history.go(-1)")
                browser.implicitly_wait(10)
                time.sleep(1)
            
            except IndexError:
                print(total_song_lists['Full'][k])
                temp.append(total_song_lists['Full'][k])
                browser.execute_script("window.history.go(-1)")
                browser.implicitly_wait(10)
                time.sleep(1)

LyricsCrawler()
