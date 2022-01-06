from time import time
from sys import exit
from db import update_proxies
import _parser_
from cfg import parsing_interval


def parse():
	f = open('last_parsing.txt')
	last_parsing = float(f.read())
	f.close()

	if not last_parsing:
		last_parsing = 0

	if last_parsing + parsing_interval*60 <= time():
		print('asfd')
		f = open('last_parsing.txt', 'w')
		f.write(str(time()))
		f.close()

		parsed = _parser_.get_proxies() 
		update_proxies(parsed)

	exit()