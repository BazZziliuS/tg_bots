import configparser
import os
import time

path = 'config.cfg'

def create_config():

    config = configparser.ConfigParser()
    config.add_section("Settings")
    config.set("Settings", "bot_token", "ТУТ ТОКЕН")
    config.set("Settings", "admin_id_own", "0:АЙДИ_АДМИНА")
    config.set("Settings", "admin_id_manager", "0:АЙДИ_АДМИНА") # типо 0:485238409
    config.set("Settings", "qiwi_number", "КИВИ НОМЕР")
    config.set("Settings", "qiwi_token", "КИВИ ТОКЕН") #qiwi.com/api
    config.set("Settings", "commission_percent", "10")
    config.set("Settings", "min_bank", "50") # МИНИМУМ пополнения
    config.set("Settings", "min_withdraw_sum", "200") # минимум вывод
    config.set("Settings", "ref_reward", "1") # цена за одного нового реферала
    
    with open(path, "w") as config_file:
        config.write(config_file)

def check_config_file():
    if not os.path.exists(path):
        create_config()
        
        print('Config created')
        time.sleep(3)
        exit(0)


def config(what):
    
    config = configparser.ConfigParser()
    config.read(path)

    value = config.get("Settings", what)

    return value

check_config_file()