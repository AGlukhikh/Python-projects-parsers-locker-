#парсинг информации о плагинах с WordPress 'https://wordpress.org/plugins/'
from bs4 import BeautifulSoup
import lxml
import requests
import csv

requests.packages.urllib3.disable_warnings()
def get_html(url):#получение содержимого сайта по url
    r=requests.get(url,verify=False)
    return r.text

def refined(s):#приведение параметра "рейтинг" к численному виду содержимого сайта по url
    reit=s.split()[0]
    result=reit.replace(',','')
    return result

def write_csv(data):#запись в файл результатов построково
    with open('plugins.csv','a') as f:
        writer=csv.writer(f)
        writer.writerow((data['name'],data['url'], data['rewievs']))

def get_data(html):#непосредственное извлечение даннных
    soup=BeautifulSoup(html,'lxml')
    popular=soup.find_all('section')[3]
    plugins=popular.find_all('article')

    for plugin in plugins:
        name=plugin.find('h3').text#название плагина
        url=plugin.find('h3').find('a').get('href')#ссылка на плагин
        re=plugin.find('span',class_='rating-count').find('a').text#рейтинг
        rating= refined(re)

        data={'name':name, 'url':url, 'rewievs':rating}#упаковывание данных в словарь для записи в файл
        write_csv(data)

def main():
    url = 'https://wordpress.org/plugins/'
    print(get_data(get_html(url)))

if __name__=='__main__':
    main()