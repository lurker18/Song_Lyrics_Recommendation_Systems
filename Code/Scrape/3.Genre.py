# -*- coding: utf-8 -*-
"""
Created on Sat Oct 30 13:44:50 2021

@author: Hydra18
"""

from bs4 import BeautifulSoup
import pandas as pd
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


total_song_lists = pd.read_csv('C:/Users/Hydra18/Desktop/텍스트이해와인공지능/Project/Dataset/test.csv', encoding = 'utf-8')
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

url = 'https://www.last.fm/music/Coldplay/_/My+Universe'
browser = webdriver.Chrome(executable_path='C:/Users/Hydra18/Pictures/chromedriver/chromedriver.exe', chrome_options=option)
browser.execute_cdp_cmd("Page.setGeolocationOverride", params)
browser.maximize_window()
browser.get(url)

def GenreCrawler():
    with open('C:/Users/Hydra18/Desktop/텍스트이해와인공지능/Project/Dataset/Top_Songs_Genres.csv', 'a', encoding='utf-8-sig', newline='') as file:
        csvfile = csv.writer(file)
        temp = []
        
        for i in range(45, len(total_song_lists['Full'])):
            temp_list = []
            
            browser.find_element_by_class_name('masthead-search-toggle').click()
            browser.find_element_by_xpath('//*[@id="masthead-search-field"]').click()
            browser.find_element_by_xpath('//*[@id="masthead-search-field"]').clear()
            browser.find_element_by_xpath('//*[@id="masthead-search-field"]').send_keys(total_song_lists['Full'][i])
            browser.find_element_by_xpath('//*[@id="masthead-search"]/div/button').click()
            time.sleep(4)
            browser.find_element_by_xpath('/html/body/div[5]/div[4]/div[5]/div[2]/div/div[3]/nav/ul/li[4]/a').click()
            time.sleep(3)
            browser.find_element_by_xpath('/html/body/div[5]/div[4]/div[5]/div[3]/div/div[1]/table/tbody/tr[1]/td[4]/a').click()
            time.sleep(3)

            try:
                temp_list.append([total_song_lists['Song'][i], total_song_lists['Artist'][i]])
                
                if "hip-hop" in browser.find_element_by_class_name('tags-list--global').text:
                    hip_hop = 'Hip-Hop'
                    temp_list.append([hip_hop])
                if "rap" in browser.find_element_by_class_name('tags-list--global').text:
                    rap = 'Rap'
                    temp_list.append([rap])
                if "pop" in browser.find_element_by_class_name('tags-list--global').text:
                    pop = 'Pop'
                    temp_list.append([pop])
                if "soul" in browser.find_element_by_class_name('tags-list--global').text:
                    soul = 'Soul'
                    temp_list.append([soul])
                if "country" in browser.find_element_by_class_name('tags-list--global').text:
                    country = 'Country'
                    temp_list.append([country])
                if "blues" in browser.find_element_by_class_name('tags-list--global').text:
                    blues = 'Blues'
                    temp_list.append([blues])
                if "electronic" in browser.find_element_by_class_name('tags-list--global').text:
                    electronic = 'Electronic'
                    temp_list.append([electronic])
                if "rock" in browser.find_element_by_class_name('tags-list--global').text:
                    rock = 'Rock'
                    temp_list.append([rock])
                if "r&b" in browser.find_element_by_class_name('tags-list--global').text:
                    rb = 'R&B'
                    temp_list.append([rb])
                if "alternative" in browser.find_element_by_class_name('tags-list--global').text:
                    alternative = 'Alternative'
                    temp_list.append([alternative])
                if "k-pop" in browser.find_element_by_class_name('tags-list--global').text:
                    kpop = 'K-Pop'
                    temp_list.append([kpop])
                if "house" in browser.find_element_by_class_name('tags-list--global').text:
                    house = 'House'
                    temp_list.append([house])
                if "bass" in browser.find_element_by_class_name('tags-list--global').text:
                    bass = 'Bass'
                    temp_list.append([bass])
                if "classical" in browser.find_element_by_class_name('tags-list--global').text or "classic" in browser.find_element_by_class_name('tags-list--global').text:
                    classical = 'Classical'
                    temp_list.append([classical])
                if "soundtrack" in browser.find_element_by_class_name('tags-list--global').text:
                    soundtrack = 'Soundtrack'
                    temp_list.append([soundtrack])
                if "holiday" in browser.find_element_by_class_name('tags-list--global').text:
                    holiday = 'Holiday'
                    temp_list.append([holiday])
                else:
                    none = 'Unknown'
                    temp_list.append([none])
                        

                csvfile.writerow(temp_list)
                    
                browser.execute_script("window.history.go(-1)")
                time.sleep(3)

            except:
                print(total_song_lists['Full'][i])
                temp.append([total_song_lists['Full'][i]])
                browser.execute_script("window.history.go(-1)")
                time.sleep(3)

   

GenreCrawler()

