import random
import requests
import json
import threading

from loguru import logger
from time import sleep
from threading import Thread
from web3 import Web3

from better_proxy import Proxy
proxy_list = Proxy.from_file('proxies.txt')
def get_random_proxy():
    
    proxy = (random.choice(proxy_list)).as_proxies_dict
    return proxy

def check(address):
    while True:
        try:
            url = f'https://www.blastbera.fun/api/check-eligibility?address={address}'

            headers = {
                'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
                'referer':'https://www.blastbera.fun/',
            }

            resp = requests.get(url, headers=headers, proxies=get_random_proxy())
            if resp.status_code == 200:
                a = json.loads(resp.text)
                isEligible = a['isEligible']
                if isEligible == True:
                    rawAllocation = int(a['rawAllocation'])
                    return rawAllocation
                
                else: return False
            
            else: sleep(5)
        except Exception as e:
            logger.error(f'[{address}] Error: {e}')
            sleep(5)
        
def start(address):
    address = Web3.to_checksum_address(address)
    rawAllocation = check(address)
    
    if rawAllocation != False:

        with open(f'success.txt', 'a', encoding='utf-8') as f:
            f.write(f'{address};{rawAllocation}\n')
        logger.success(f'[{address}] {rawAllocation}')

    else:
        logger.info(f'[{address}] {rawAllocation}')

THREADS = int(input(f'Введите кол-во потоков: '))

file_name = 'wallets'
accs_list = open(file_name + '.txt', 'r').read().splitlines()

for el in accs_list:
    splited_data = el.split(';')
    address = splited_data[0]

    while threading.active_count() >= 50:
        sleep(1)

    Thread(target=start, args=(address, )).start()
    sleep(0.01)
