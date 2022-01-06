import requests
from bs4 import BeautifulSoup


def get_html(site):
    r = requests.get(site)
    return r.text


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    line = soup.find('table', id='theProxyList').find('tbody').find_all('tr')

    for tr in line:
        td = tr.find_all('td')
        ip = td[1].text
        port = td[2].text
        country = td[3].text.replace('\xa0', '')
        anonym = td[4].text.replace('\r\n        ', '')
        types = td[5].text.replace('\r\n\t\t\t\t\t', '').replace('\r\n        ', '')
        time = td[6].text
        t = open('test.txt', 'r+')
        data = f"ip: {ip} | port: {port} | Страна: {country} | тип {types} | время отклика {time}"
        #    for i in t:
        t.write(data + '\n')

        data = {'ip': ip,
                'Порт': port,
                'Страна': country,
                'Анонимность': anonym,
                'Тип': types,
                'Время отклика': time}

        #print(data)


def main():
    url = 'http://foxtools.ru/Proxy'
    get_page_data(get_html(url))


if __name__ == '__main__':
    main()