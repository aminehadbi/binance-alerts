import requests
import sys
import multiprocessing
from datetime import datetime

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
    return candles

def calculate_rel_vol(candles):
    total_vol = 0
    for i in candles:
        total_vol += float(i[5])
    current_ratio = round(100*float(candles[-1][5])/float(total_vol),2)
    current_volume = float(candles[-1][5])
    return current_ratio, current_volume

def get_rel_vol(ticker, range, interval='1m'):
    try:
        candles = get_candles(ticker, range, interval)
        current_ratio, current_volume = calculate_rel_vol(candles)
        return current_ratio, current_volume
    except Exception:
        print(Exception)
        return 1, 1


def scan_market(ticker, interval='1m', range='15'):
    results = {}
    #print(ticker, interval, range)
    current_ratio, current_volume = get_rel_vol(ticker, range, interval)
    if current_ratio > 10:
            print('Current Ratio:', current_ratio, 'Current Volume:', current_volume, interval)
    #        results[interval] = current_ratio
    return [current_ratio, current_volume, interval]



def main(value):
    ticker_list = get_ticker_list()
    print('Tickers list downloaded')
    results_list = []
    try:
        processes = []
        p = multiprocessing.Process(target=scan_all_markets, args=(ticker_list,))
        processes.append(p)
        p.start()
        for process in processes:
            process.join()
    except:
        pass


def scan_all_markets(ticker_list):
    filter_list = ['1m', '5m', '15m', '1h', '4h']
    #print(filter_list, ticker_list)
    for ticker in ticker_list:
        results = []
        #print('!!!', ticker)
        for i in filter_list:
            a = scan_market(ticker, i, 15)
            results.append(a[0])
        ressum = sum(results)
        print(ticker, results, round(ressum))
        with open('your_file.txt', 'a') as f:
            f.write(str(ticker)+" "+str(results)+'\n')



if __name__ == "__main__":
    now = datetime.now()

    timestamp = datetime.timestamp(now)
    with open('your_file.txt', 'a') as f:
        dt_object = datetime.fromtimestamp(timestamp)
        f.write(str(dt_object)+ '\n')

    main('a')

    now = datetime.now()
    timestamp = datetime.timestamp(now)
    with open('your_file.txt', 'a') as f:
        dt_object = datetime.fromtimestamp(timestamp)
        f.write(str(dt_object)+'\n')
