import re
import requests
from requests_html import HTML
from base64 import b64decode as b64d
from time import sleep
from math import ceil, floor


class Parser():
	def __init__(self, host):
		self.host = host
		self.s = requests.Session()
		self.s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'


	def get_proxies_on_page(self, html, ip_selector, port_selector=None):
		ips = html.find(ip_selector)

		if port_selector:
			ports = html.find(port_selector)
			return [f'@{ips[i].text}:{ports[i].text}' for i in range(len(ips))]

		return list(map(lambda i: '@'+i.text, ips))


class FreeProxy(Parser):
	host = 'http://free-proxy.cz'

	def __init__(self):
		super(FreeProxy, self).__init__(self.host)


	def get_proxies(self):
		def decode(proxy):
			splitted = proxy.split(':')

			splitted[0] = re.search(r'"(.+)"', splitted[0])[0]
			splitted[0] = b64d(splitted[0]).decode()

			return '@' + ':'.join(splitted)


		proxies = []

		location = 'en/proxylist/country/all/socks5/ping/all'
		html = HTML(html=self.s.get(f'{self.host}/{location}').text)

		pages = int(html.find('div.paginator a')[-2].text)

		for p in range(pages):
			page = HTML(html=self.s.get(f'{self.host}/{location}/{str(p+1)}').text)
			proxies += self.get_proxies_on_page(page, 'td.left[style]', 'span.fport')

		return list(map(decode, proxies))


class SpysOne(Parser):
	host = 'http://spys.one'

	def __init__(self):
		super(SpysOne, self).__init__(self.host)
	

	def get_proxies(self):
		def get_assignments(p, r, o, x, y, s):
			def to_string(num, base):
				chars = '0123456789abcdefghijklmnopqrstuvwxyz'
				rests = []

				curr = num

				while 1:
					rest = curr%base
					rests.append(chars[rest])
					curr = floor(curr/base)

					if curr < base:
						rests.append(chars[curr%base])
						break

				return ''.join(list(map(str, rests[::-1])))


			def y(c):
				if c%r > 35: a = chr(c+29)
				else: a = re.sub(r'^0+', '', to_string(c, 36))

				return a


			x += ['']*(o-len(x))
			for i in range(o):
				s[y(i)] = x[i] or y(i)

			s['0'] = '0'

			p = list(p)
			for i in range(len(p)):
				if re.fullmatch(r'\w', p[i]):
					p[i] = s[ p[i] ]


			return re.sub(r'(^;)|(;$)', '', ''.join(p))



		proxies = []

		location = 'proxies'
		html = HTML(html=self.s.get(f'{self.host}/{location}').text)

		xx0 = html.find('input[name=xx0]')[0].attrs['value']

		data = {
			'xx0':xx0,
			'xpp':5,
			'tldc':0,
			'xf1':0,
			'xf2':0,
			'xf4':0,
			'xf5':2
		}

		location += '/'
		html = HTML(html=self.s.post(f'{self.host}/{location}', data=data).text)

		open('spys.html', 'wb').write(html.html.encode())

		script = html.find('script')[3].text
		args = re.search(r'(?<=})\(.+\)(?=\)$)', script)[0]
		
		assignments = get_assignments(*eval(args))
		exec(assignments)
		
		assignments = list(map(lambda a: a.split('='), assignments.split(';')))

		locals_ = locals()

		scope = {a[0]:locals_[ a[0] ] for a in assignments}

		trs = html.find('tr.spy1xx, tr.spy1x')[2:]

		ips = list(map(lambda t: re.search(r'(\d+\.?){4}', t.find('td font')[0].text)[0], trs))

		ports = list(map(lambda t: re.findall(r'\([\d\w^]+\)', t.find('script')[0].text), trs))
		ports = list(map(lambda p: eval('+'.join(p).replace('(', 'str('), scope), ports))

		delays = list(map(lambda t: float(t.find('td')[5].find('font')[0].text), trs))

		proxies = [[ips[i], ports[i], delays[i]] for i in range(len(ips))]
		proxies = list(filter(lambda p: p[2]<3, proxies))

		return [f'@{p[0]}:{p[1]}' for p in proxies]


class ProxyDocker(Parser):

	def __init__(self):
		super(ProxyDocker, self).__init__('https://www.proxydocker.com')


	def get_proxies(self):
		mainpage = self.s.get(self.host + '/ru/socks5-list/')
		mainpage_html = HTML(html=mainpage.text)

		token = mainpage_html.find('meta[name="_token"]')[0].attrs['content']

		data = {
			'token':token,
			'country':'all',
			'city':'all',
			'state':'all',
			'port':'all',
			'type':'socks5',
			'anonymity':'all',
			'need':'all',
		}

		page = 0
		out = []
		while 1:
			data['page'] = str(page+1)
			proxies = self.s.post(self.host + '/ru/api/proxylist/', data=data).json()['proxies']

			if not proxies:
				break

			for p in proxies:
				if p['timeout'] <= 5:
					out.append(f'@{p["ip"]}:{p["port"]}')

			page += 1

		return out



def get_proxies():
	return [*ProxyDocker().get_proxies()]