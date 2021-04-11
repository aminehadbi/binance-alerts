import requests
import sys
from multiprocessing import Process
from datetime import datetime
import io
from numba import guvectorize, njit

def get_ticker_list():
    ticker_list = []
    url = 'https://fapi.binance.com/fapi/v1/exchangeInfo'
    data = requests.get(url)
    candles = data.json()
    for i in candles['symbols']:
        ticker_list.append(i['symbol'])
    return ticker_list


def get_candles(ticker, range, interval='1m'):
    url = "".join(('https://fapi.binance.com/fapi/v1/klines?symbol=',ticker,'&interval=',interval,'&limit=',str(range)))
    data = requests.get(url)
    candles = data.json()
    volume_list = []
    total_vol = 0
    for i in candles:
        volume_list.append(float(i[5]))
    total_vol = sum(volume_list)
    current_volume = float(candles[-1][5])
    return total_vol, current_volume


def scan_market(ticker, interval='1m', range='15'):
    results = {}
    #print(ticker, interval, range)
    total_vol, current_volume =  get_candles(ticker, range, interval)
    current_ratio, current_volume = get_rel_vol(total_vol, current_volume, range, interval)

    if current_ratio > 10:
            print('Current Ratio:', current_ratio, 'Current Volume:', current_volume, interval, ticker)
            results[interval] = current_ratio
    return [current_ratio, current_volume, interval]

@njit
def calculate_ratios(total_vol, current_volume):
    current_ratio = round(100*float(current_volume)/float(total_vol),2)
    return current_ratio

def get_rel_vol(total_vol, current_volume, range=15, interval='1m'):
    try:
        current_ratio = calculate_ratios(total_vol, current_volume)
        return current_ratio, current_volume

    except Exception as E:
        print(E)
        return 1, 1







def scan_all_markets(ticker_list):
    filter_list = ['1m', '5m', '15m', '1h', '4h']
    #print(filter_list, ticker_list)
    for ticker in ticker_list:
        results = []
        #print('!!!', ticker)
        for i in filter_list:
            a =  scan_market(ticker, i, 15)
            results.append(a[0])
        ressum = sum(results)
        print(ticker, results, round(ressum))
        with open('your_file.txt', 'a') as f:
            f.write(str(ticker)+" "+str(results)+'\n')


def main(value, ticker_list):
  
    results_list = []
    try:
         scan_all_markets(ticker_list)
    except Exception as E:
        print('Error!', E)
        pass


if __name__ == "__main__":
    now = datetime.now()

    timestamp = datetime.timestamp(now)
    with open('your_file.txt', 'a') as f:
        dt_object = datetime.fromtimestamp(timestamp)
        f.write(str(dt_object)+ '\n')
    counter = 8
    ticker_list = get_ticker_list()
    length = len(ticker_list)//2
    print('Tickers list downloaded')
    #io.run(main('a', ticker_list))
    ticker_list_rev = ticker_list.reverse()
    print(ticker_list)
    while counter < len(ticker_list):
        p1 = Process(target=main, args=('a', ticker_list[counter-2:counter-1]))
        p1.start()
        p2 = Process(target=main, args=('a', ticker_list[counter-4:counter-3]))
        p2.start()
        
        p3 = Process(target=main, args=('a', ticker_list[counter-6:counter-5]))
        p3.start()
        p4 = Process(target=main, args=('a', ticker_list[counter-8:counter-7]))
        p4.start()        
        p1.join()
        p2.join()
        p3.join()
        p4.join()

        counter+=8
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    with open('your_file.txt', 'a') as f:
        dt_object = datetime.fromtimestamp(timestamp)
        f.write(str(dt_object)+'\n')
