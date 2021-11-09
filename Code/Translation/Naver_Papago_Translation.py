# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 17:34:42 2021

@author: Hydra18
"""

import urllib.request
import json
import pandas as pd
import csv

client_id = "<생략>"           # 네이버 파파고 번역기 Client API
client_secret = "<생략>"       # 네이버 파파고 번역기 Client Secret Code

# 번역할 CSV파일 불러오기
songs = pd.read_csv('C:/Users/Hydra18/Desktop/텍스트이해와인공지능/Project/Dataset/Translation/Sample.csv', encoding = 'utf-8-sig') # <--- !! 경로 주위 !! 각 컴퓨터별 경로가 다름


# 번역한 CSV파일 저장하기
with open('C:/Users/Hydra18/Desktop/텍스트이해와인공지능/Project/Dataset/Translation/Translated.csv', 'w',  newline = '', encoding = 'utf-8-sig') as file: # <--- !! 경로 주위 !! 각 컴퓨터별 경로가 다름
    csvfile = csv.writer(file)
    for i in range(len(songs)):
        temp_list = []
        
        title = ''
        title = songs['title'][i]
        
        artist = ''
        artist = songs['artist'][i]
    
        lyrics = ''
        lyrics = songs['lyric'][i]
        
        genre = ''
        genre = songs['genre'][i]
        
        translate = ''
        translate = songs['lyric'][i]

        encText = urllib.parse.quote(translate)
        data = "source=ko&target=en&text=" + encText
        url = "https://openapi.naver.com/v1/papago/n2mt"
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", client_id)
        request.add_header("X-Naver-Client-Secret", client_secret)
        response = urllib.request.urlopen(request, data = data.encode("utf-8"))
        rescode = response.getcode()
        
        if(rescode==200):
            response_body = response.read()
            res = json.loads(response_body.decode('utf-8'))

            # 각 가사별 행마다 기록
            temp_list.append([title, artist, lyrics, genre, res['message']['result']['translatedText']])
            
            for row in temp_list:
                csvfile.writerow(row)

        else:
            print("Error Code:" + rescode)
            print("Not able to translate song:" + title)
