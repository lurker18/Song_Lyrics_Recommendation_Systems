# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 14:58:14 2021

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

"""
//*[@id="/search/results/"]/ul[1]/li[1]
//*[@id="/search/results/"]/ul[1]/li[2]
//*[@id="/search/results/"]/ul[1]/li[3]
"""

browser_locale = 'en'
option = Options()
option.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
option.add_argument("--lang={}".format(browser_locale))
option.add_argument("disable-infobars")
option.add_argument("disable-extensions")
option.add_argument('disable-gpu')
url = 'https://www.shazam.com/en'
browser = webdriver.Chrome(executable_path='C:/Users/Hydra18/Pictures/chromedriver/chromedriver.exe', chrome_options=option)
browser.maximize_window()
browser.get(url)
browser.implicitly_wait(15)
time.sleep(5)

def LyricsCrawler():
    with open('C:/Users/Hydra18/Desktop/텍스트이해와인공지능/Project/Dataset/Top_Songs_Lyrics3.csv', 'w', encoding='utf-8-sig', newline='') as file:
        csvfile = csv.writer(file)
        
        for k in range(len(total_song_lists)):

            browser.find_element_by_xpath('//*[@id="search-input"]').click()
            browser.find_element_by_xpath('//*[@id="search-input"]').clear()
            browser.find_element_by_xpath('//*[@id="search-input"]').send_keys(total_song_lists['Full'][k])
            browser.find_element_by_xpath('//*[@id="search-input"]').click()
            browser.implicitly_wait(15)
            time.sleep(3)
            browser.find_element_by_xpath('//*[@id="search-results-songs-showmore"]').click()
            time.sleep(3)
            browser.find_element_by_xpath('//*[@id="search-results-songs-showmore"]').click()
            time.sleep(3)
            browser.find_element_by_xpath('//*[@id="search-results-songs-showmore"]').click()
            time.sleep(3)
            browser.find_element_by_xpath('//*[@id="search-results-songs-showmore"]').click()

            html1 = browser.page_source
            document = BeautifulSoup(html1, 'lxml')

            try:
                for i in range(1,11):
                    if i == 1:
                        temp_list = []
                        browser.find_element_by_xpath('//*[@id="/search/results/"]/ul[1]/li[' + str(i) + ']').click()
                        browser.implicitly_wait(15)
                        time.sleep(3)
                        html2 = browser.page_source
                        document = BeautifulSoup(html2, 'lxml')
                        
                        if total_song_lists['Artist'][k] == document.find('a', attrs = {'data-shz-beacon-id': 'track.ue-trackheader-artist'}).text:
                            lyrics = ''
                            lyrics = document.select('p.lyrics')[0].text
                            line_by_lyrics = lyrics.split('\n')
                            line_by_lyrics = str(line_by_lyrics).replace("\'", '').replace('"','').replace(",",'').replace('(',' ').replace(')',' ').replace('[','').replace(']','').replace('  ', ' ')
            
                            song = ''
                            song = document.select('h1.title.line-clamp-2')[0].text
                                
                            artist = ''
                            artist = document.find('a', attrs = {'data-shz-beacon-id': 'track.ue-trackheader-artist'}).text
                            
                            genre = ''
                            genre = document.find('h3', attrs = {'class': 'genre'}).text
            
                            temp_list.append([song, artist, lyrics, genre, total_song_lists['Song'][k]])
                                
                        for row in temp_list:
                            csvfile.writerow(row)
                
                            browser.execute_script("window.history.go(-1)")
                            time.sleep(3)

                        else:
                            browser.execute_script("window.history.go(-1)")
                            time.sleep(3)
                            browser.find_element_by_xpath('//*[@id="search-input"]').click()
                            time.sleep(3)

                    else:
                        temp_list = []
                        browser.find_element_by_xpath('//*[@id="/search/results/"]/ul[1]/li[' + str(i) + ']').click()
                        browser.implicitly_wait(15)
                        time.sleep(3)
                        html3 = browser.page_source
                        document = BeautifulSoup(html3, 'lxml')
                        
                        temp_list = []
                        browser.find_element_by_xpath('//*[@id="/search/results/"]/ul[1]/li[' + str(i) + ']').click()
                        browser.implicitly_wait(15)
                        time.sleep(3)
                        html2 = browser.page_source
                        document = BeautifulSoup(html2, 'lxml')
                        if total_song_lists['Artist'][k] == document.find('a', attrs = {'data-shz-beacon-id': 'track.ue-trackheader-artist'}).text:
                            
                            lyrics = ''
                            lyrics = document.select('p.lyrics')[0].text
                            line_by_lyrics = lyrics.split('\n')
                            line_by_lyrics = str(line_by_lyrics).replace("\'", '').replace('"','').replace(",",'').replace('(',' ').replace(')',' ').replace('[','').replace(']','').replace('  ', ' ')
            
                            song = ''
                            song = document.select('h1.title.line-clamp-2')[0].text
            
                            artist = ''
                            artist = document.find('a', attrs = {'data-shz-beacon-id': 'track.ue-trackheader-artist'}).text
            
                            genre = ''
                            genre = document.find('h3', attrs = {'class': 'genre'}).text
            
                            temp_list.append([song, artist, lyrics, genre, total_song_lists['Song'][k]])
            
                        for row in temp_list:
                            csvfile.writerow(row)
                
                            browser.execute_script("window.history.go(-1)")
                            time.sleep(3)
                            browser.find_element_by_xpath('//*[@id="search-input"]').click()
                            time.sleep(3)
                        
                        else:
                            browser.execute_script("window.history.go(-1)")
                            time.sleep(3)
                            browser.find_element_by_xpath('//*[@id="search-input"]').click()
                            time.sleep(3)

            except:
                #browser.execute_script("window.history.go(-1)")
                time.sleep(3)


LyricsCrawler()
