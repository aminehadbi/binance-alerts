import matplotlib.pyplot as plt
import requests 

def return_ticker_list():
    ticker_list = []
    url = 'https://fapi.binance.com/fapi/v1/exchangeInfo'
    data = requests.get(url)
    candles = data.json()
    for i in candles['symbols']:
        ticker_list.append(i['pair'])
    return ticker_list


def get_close_serie(ticker, interval, range):
    url = "".join(('https://fapi.binance.com/fapi/v1/continuousKlines?pair=',ticker,'&interval=',interval,'&limit=',str(range),'&contractType=PERPETUAL'))
    data = requests.get(url)
    candles = data.json()
    volume_list = []
    total_vol = 0
    for i in candles:
        volume_list.append(float(i[4]))
    #print(volume_list)
    return volume_list

tickers = return_ticker_list()
for ticker in tickers:
    price = get_close_serie(ticker, '1m', 500)
    pltaa = plt.plot(price)
    plt.suptitle(ticker)
    plt.savefig('./plot/'+ticker+'.png')
    plt.clf()