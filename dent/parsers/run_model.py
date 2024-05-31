import json
import requests
import time

with open('aveldent-2024-05-27.json', 'r', encoding='utf8') as rocada:
    data = json.load(rocada)
    sum = 0
    for k in data:
        sum += len(data[k])
    for k in data: # /anesteziologiya
        for el in data[k]: # el is name
            sum -= 1
            print(sum)
            to_db = {'name':el, 'articul' :data[k][el]['product_code'], 'price':data[k][el]['price'], 'site':'AD'}
            r = requests.post('http://127.0.0.1:8000/api/products/', data=to_db)
            #print(r.status_code)


    """    for k in data:
        sum += len(data[k])
    print(sum)"""