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

url = 'https://www.google.com'
browser = webdriver.Chrome(executable_path='C:/Users/Hydra18/Pictures/chromedriver/chromedriver.exe', chrome_options=option)
browser.execute_cdp_cmd("Page.setGeolocationOverride", params)
browser.maximize_window()
browser.get(url)
browser.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').click()
browser.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').clear()
browser.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys('shazam')
browser.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[3]/center/input[1]').click()
browser.implicitly_wait(10)
time.sleep(1)




def LyricsCrawler():
    with open('C:/Users/Hydra18/Desktop/텍스트이해와인공지능/Project/Dataset/Top_Songs_Lyrics3.csv', 'w', encoding='utf-8-sig', newline='') as file:
        csvfile = csv.writer(file)
        temp = []
        for k in range(len(total_song_lists)):
            temp_list = []
            
            browser.find_element_by_xpath('//*[@id="tsf"]/div[1]/div[1]/div[2]/div/div[2]/input').click()
            browser.find_element_by_xpath('//*[@id="tsf"]/div[1]/div[1]/div[2]/div/div[2]/input').clear()
            browser.find_element_by_xpath('//*[@id="tsf"]/div[1]/div[1]/div[2]/div/div[2]/input').send_keys( 'lyrics ' + total_song_lists['Full'][k])
            browser.find_element_by_xpath('//*[@id="tsf"]/div[1]/div[1]/div[2]/button').click()
            
            try:
                browser.find_elements_by_xpath('//*[@id="rso"]/div[1]/div/div/div[1]/a/h3')[0].click()
                
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
                lyrics = document.select('p.lyrics')[0].text
                line_by_lyrics = lyrics.split('\n')
                line_by_lyrics = str(line_by_lyrics).replace("\'", '').replace('"','').replace(",",'').replace('(',' ').replace(')',' ').replace('[','').replace(']','').replace('  ', ' ')
            
                song = ''
                song = document.select('h1.title.line-clamp-2')[0].text
                           
                try:
                    artist = ''
                    artist = document.find('a', attrs = {'data-shz-beacon-id': 'track.ue-trackheader-artist'}).text
                except AttributeError:
                    artist = ''
                    artist = document.find('meta', attrs = {'itemprop' : 'name'}).text
                          
                try:
                    genre = ''
                    genre = document.find('h3', attrs = {'class': 'genre'}).text
                except AttributeError:
                    genre = 'Unknown'
            
                temp_list.append([song, artist, lyrics, genre, total_song_lists['Full'][k]])
                                
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
