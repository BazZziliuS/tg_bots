import requests
from bs4 import BeautifulSoup

choice = "1"
headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_1 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A402 Safari/604.1'
}
f = open('proxy.txt', 'wb')
try:
    r = requests.get("https://api.proxyscrape.com/?request=displayproxies&proxytype=http&country=all",
                    headers=headers,
                    timeout=5)
    f.write(r.content)
    print("Успех!")
except:
    print("Ошибка1!")
    f.close()
try:
    r = requests.get("https://www.proxy-list.download/api/v1/get?type=http", headers=headers, timeout=5)
    f.write(r.content)
    print("Успех!")
except:
    print("Ошибка2!")
    f.close()
try:
    r = requests.get("https://www.proxyscan.io/download?type=http", headers=headers, timeout=5)
    f.write(r.content)
    print("Успех!")
except:
    print("Ошибка3!")
    f.close()
try:
    r = requests.get("https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt", headers=headers, timeout=5)
    f.write(r.content)
    print("Успех!")
except:
    print("Ошибка4!")
    f.close()
try:
    r = requests.get("https://proxy-daily.com/api/getproxylist?apikey=3Rr6lb-yfeQeotZ2-9M76QI&format=ipport&type=http&lastchecked=60", headers=headers, timeout=5)
    f.write(r.content)
    print("Успех!")
except:
    print("Ошибка!5")
    f.close()
try:
    def get_html(site):
        print("Передали сайт")
        r = requests.get(site, headers=headers, timeout=5)
        return r.text
 
 
    def get_page_data(html):
        print("Начинаю парсинг!")
        soup = BeautifulSoup(html, 'lxml')
        line = soup.find('table', id='theProxyList').find('tbody').find_all('tr')
        ipL = []
        for tr in line:
            td = tr.find_all('td')
            #print(td)
            ip = str(td[0]).replace('<td style="text-align:center"><input class="ch" onclick="SelectProxy(this)" type="checkbox" value="','')
            ip = ip.replace('"/></td>','')
            ipL.append(ip)
            return(ipL)
 
    def main():
        url1 = 'http://foxtools.ru/Proxy'
        url2 = 'http://foxtools.ru/Proxy?page=2'
        url3 = 'http://foxtools.ru/Proxy?page=3'
        ip_list = []
        ip_list.append(get_page_data(get_html(url1)))
        ip_list.append(get_page_data(get_html(url2)))
        ip_list.append(get_page_data(get_html(url3)))
        q = 1
        for i in ip_list:
            for j in i:
                print("Мини успех")
                f.write(f'{j}\n')
                
    if __name__ == '__main__':
        main()
except:
    print("Всо) юзай прокси!")
    f.close()