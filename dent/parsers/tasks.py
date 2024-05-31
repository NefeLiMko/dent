from data import cocks
import requests
import time


url = 'https://w-stom.ru/'
while True:
    r = requests.get(url)
    time.sleep(3)
    print(r.cookies['__cap_'])
    if r.cookies['__cap_'] in cocks:
        print('success')
        break
