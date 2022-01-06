import random

def easy_pass(s):
    hash = random.sample('1234567890qwertyuiopasdfghjklzxcvbnm', s)
    pwd = ''.join(hash)
    return pwd

def medium_pass(s):
    hash = random.sample('1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM', s)
    pwd = ''.join(hash)
    return pwd


def hard_pass(s):
    hash = random.sample('1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM!?-_@#$%&<>', s)
    pwd = ''.join(hash)
    return pwd