import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()


def uniqlo_prices(article):
    codes = ('vn', 'th',)

    try:
        product = int(article)
    except ValueError:
        return 'Введите номер товара, он состоит только из цифр.'

    try:
        response = requests.get(
            'https://api.apilayer.com/currency_data/live',
            headers={'apikey': os.getenv('TOKEN_CUR')}
        )
        if response.status_code != 200:
            return 'Нет соединения с сервером.'
        content = json.loads(response.content)
        rates = {codes[0]: content['quotes']['USDVND'],
                 codes[1]: content['quotes']['USDTHB']}
    except ConnectionError:
        return 'Нет соединения с сервером.'

    product_name = ''
    prices = ''

    for code in codes:
        res = requests.get(
            f'https://www.uniqlo.com/{code}/api/'
            f'commerce/v3/en/products/E{product}-000',
            headers={'User-Agent': 'PostmanRuntime/7.29.2',
                     'cookie': os.getenv('COOKIE')}
        )

        layout = json.loads(res.content)

        if layout['status'] == 'nok':
            return 'Кажется, такого товара нет.'

        prices_set = {(x['color']['name'],
                       x['prices']['base']['value'],
                       x['prices']['base']['currency']['symbol'])
                      if x['prices']['promo'] is None
                      else (x['color']['name'],
                            x['prices']['promo']['value'],
                            x['prices']['base']['currency']['symbol'])
                      for x in layout['result']['items'][0]['l2s']}
        prices += f'{code}\n'
        prices += ''.join(
            element[0] + ': ' + element[1] + element[2] + '\n'
            for element in prices_set)

        calc = lambda num: round(float(num) / float(rates[code]), 2)

        prcies_total = {(x[1],
                         str(calc(x[1])))
                        for x in prices_set}

        prices += ''.join(elem[0] + ': ' + elem[1] + ' USD' + '\n'
                          for elem in prcies_total)

        product_name = layout['result']['items'][0]['name']
    return product_name, prices
