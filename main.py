import time
from collections import deque

import requests


ENDPOINT = 'https://fapi.binance.com/fapi/v1/ticker/24hr?symbol=XRPUSDT'
TIME_DELTA = 3600

dq = deque()
while True:
    price = float(requests.get(ENDPOINT).json()['lastPrice'])
    cur_time = time.time()
    while True:
        if len(dq) == 0:
            break
        elem = dq.popleft()
        if cur_time - elem['time'] < TIME_DELTA:
            dq.appendleft(elem)
            break
    if len(dq) > 0:
        max_price = max(list(dq), key=lambda x: x['price'])['price']
        if 1 - price / max_price > 0.01:
            print('Цена упала на 1% от максимальной цены за последний час.')
    dq.append({'price': price, 'time': cur_time})
