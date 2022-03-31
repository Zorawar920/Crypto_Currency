import re
import xml
from datetime import timedelta

import requests
import json

from django.utils.datetime_safe import date
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from django.shortcuts import render


# Create your views here.
def chart(request):
    api_data = requests.get('https://api.coingecko.com/api/v3/search/trending')
    data = json.loads(api_data.content)
    labels = []
    price_btc = []
    for key, values in data.items():
        for item in values:
            for k, v in item.items():
                for _, _ in v.items():
                    if v['name'] not in labels:
                        labels.append(v['name'])
                    if v['market_cap_rank'] not in price_btc:
                        price_btc.append(v['market_cap_rank'])

    return render(request, 'chart.html', {'data': data, 'labels': labels, 'chartData': price_btc})


def coinDetail(request, id, current_price, market_cap):
    context = {}
    lowercaseId = id.lower()
    api_data = requests.get("https://api.coingecko.com/api/v3/coins/"+lowercaseId+"")
    data = json.loads(api_data.content)
    api_chart = requests.get("https://api.coingecko.com/api/v3/coins/"+lowercaseId+"/market_chart?vs_currency=usd&days=12")
    chart_data = json.loads(api_chart.content)
    market_cap_val = []
    if 'image' in data:
        for key, value in data['image'].items():
            if key == 'small':
                img_val = value
        for key, value in data['description'].items():
            if key == 'en':
                desc = value
        for key, values in chart_data.items():
            if key == 'prices':
                for inner_value in values:
                    market_cap_val.append(inner_value[1])
        cleanExpression = re.compile('<.*?>')
        cleantext = re.sub(cleanExpression, '', desc)
        context['market_cap_val'] = market_cap_val
        context['labels'] = ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7', 'Day 8','Day 9','Day 10','Day 11','Day 12']
        context['desc'] = cleantext
        context['img_val'] = img_val
        context['market_cap_rank'] = data['market_cap_rank']
        context['liquidity_score'] = data['liquidity_score']
        context['coin_id'] = id
        context['current_price'] = current_price
        context['market_cap_size'] = market_cap
    return render(request, 'detail.html', context)


def index(request):
    global active_cryptocurrencies, market_cap_change_percentage_24h_usd
    market_cap_value = 0
    d_list = {}
    api_baseData = requests.get("https://api.coingecko.com/api/v3/global")
    api_data = requests.get(
        "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false&price_change_percentage=1h")
    data = json.loads(api_data.content)
    baseData = json.loads(api_baseData.content)

    for key, values in baseData.items():
        for inner_Key, inner_val in values.items():
            d_list[inner_Key] = inner_val
    active_cryptocurrencies = d_list['active_cryptocurrencies']
    market_cap_change_percentage_24h_usd = d_list['market_cap_change_percentage_24h_usd']

    for key, value in d_list['total_market_cap'].items():
        market_cap_value += value

    return render(request, 'index.html', {'api_data': data, 'active_cryptocurrencies': active_cryptocurrencies,
                                          'market_cap_change_percentage_24h_usd': market_cap_change_percentage_24h_usd,
                                          'total_market_cap': market_cap_value})
