#парсер сайта криптовалют с пагинацией
from bs4 import BeautifulSoup
import lxml
import requests
import csv
requests.packages.urllib3.disable_warnings()#для исключения ошибок с верификацией на сайте

def get_html(url):#получение текстовой информации с сайта
    r=requests.get(url,verify=False)
    if r.ok:
        return r.text
    print(r.status_code)

def refined(s):#нормализация данных о цене
    result=s.replace(',','')
    return result

def write_csv(data):#запись данных в csv файл
    with open('criptocurrencies2.csv','a', newline = '', encoding='utf=8') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow([data['name'], data['logo'], data['url'], data['price']])

def get_page_data(html):#получение данны о криптовалюте с каждой страницы
    soup=BeautifulSoup(html,'lxml')
    trs = soup.find('table').find('tbody').find_all('tr')#вычленение строки данных с криптовалютами
    i=1
    for tr in trs:
        tds = tr.find_all('td')
        if i<=10:#на 10ой итерации метод парсинга меняется, с 11 строки  вывод на странице по-другому
            try:
                name = tds[2].find('a').find_all('p')[0].text#название криптовалюты
            except:
                name = ''
            try:
                logo = tds[2].find('a').find_all('p')[1].text#логотип криптовалюты
            except:
                logo = ''
            try:
                price = tds[3].find('a').text#курс криптовалюты
            except:
                price = ''
        else:
            try:
                name = tds[2].find('a').find_all('span')[1].text
            except:
                name=''
            try:
                logo = tds[2].find('a').find_all('span')[2].text
            except:
                logo=''
            try:
                price = tds[3].text
            except:
                price = ''
        try:#формирование прямой ссылки на валюту
            url ='https://coinmarketcap.com'+tds[2].find('a').get('href')
        except:
            url = ''

        pr=refined(price[1:])
        data = {'name': name, 'logo': logo, 'url': url, 'price':price}#запись в словарь для отдачи в функцию записи в файл
        write_csv(data)#запись в файл строки с данными
        i+=1

def main():
    url = 'https://coinmarketcap.com/'
#    get_page_data(get_html(url))
    while True:#
        get_page_data(get_html(url))
        soup = BeautifulSoup(get_html(url), 'lxml')
        try:
            url='https://coinmarketcap.com'+soup.find('ul', class_='pagination').find('li',class_='next').find('a').get('href')
            print(url)
        except:
            break

if __name__=='__main__':
    main()