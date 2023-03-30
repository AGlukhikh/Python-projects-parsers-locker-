#парсер данных об играх на STEAM
import requests
import csv
from bs4 import BeautifulSoup
import re
from time import sleep

requests.packages.urllib3.disable_warnings()#для исключения ошибок с верификацией на сайте

def write_csv(data):#запись в CSV-файл
    with open('STEAM_pars2.csv','a', newline = '', encoding='utf=8') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow([data['title'], data['reviews'], data['released'], data['tags']])

def get_html(url):#запрос содержимого по url без верификации
    response=requests.get(url,verify=False)
    if not response.ok:
        print(f'Code:{response.status_code}, url:{url}')
    return response.text

def get_games(html):#нахождение содержимого, соответствующего контенту с названием игр
    soup=BeautifulSoup(html,'lxml')
    pattern=r'^https://store.steampowered.com/app/'
    games=soup.find_all('a',href=re.compile(pattern))
    return games

def get_particular_data(id):#сбор конкретной информации из контента с играми
    url='https://store.steampowered.com/apphoverpublic/'+str(id)+'?review_score_preference=0&l=english&pagev6=true'
    html=get_html(url)
    soup=BeautifulSoup(html,'lxml')
    try:#название
        title=soup.find('h4',class_='hover_title').text.strip()
    except:
        title=''
    print(url)
    try:#дата релиза
        released=soup.find('div',class_='hover_release').span.text.split(':')[-1]
    except:
        released=''

    try:#суммарный рейтинг по отзывам
        reviews=soup.find('div',class_='hover_review_summary').text
        pattern = r'\d+'
        rev=int(''.join(re.findall(pattern,reviews)))
    except:
        rev=''

    try:#теги
        ts=soup.find_all('div',class_='app_tag')
        tag=[x.text for x in ts]
        tags=' ,'.join(tag)
    except:
        tags=''

    data={'title':title,'released':released,'reviews':rev,'tags':tags}#упаковывание данных в словарь для записи в файл
    write_csv(data)

def main():
    allgames=[]
    start=0
    url='https://store.steampowered.com/search/results/?query&start='+str(start)+'count=50&tags=1702'
    while True:
        games=get_games(get_html(url))
        if games:
            allgames.extend(games)
            start+=50
            url = 'https://store.steampowered.com/search/results/?query&start=' + str(start) + 'count=50&tags=1702'

        else:break
        for game in allgames:#получение ID игры из контента с играми
            id=game.get('data-ds-appid')
            get_particular_data(id)

if __name__=='__main__':
    main()