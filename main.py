import requests
import sys

def get_rel_vol(ticker, range, interval='1m'):
    try:
        total_vol = 0
        url = 'https://fapi.binance.com/fapi/v1/klines?symbol='+ticker+'&interval='+interval+'&limit='+str(range)
        data = requests.get(url)
        candles = data.json()
        for i in candles:
            total_vol += float(i[5])
        #print(candles[-1])
        current_ratio = round(100*float(candles[-1][5])/total_vol,2)
        current_volume = float(candles[-1][5])
        #print('Current Ratio:', current_ratio,'%', 'Current Volume:', current_volume)
        return current_ratio, current_volume
    except Exception as E:
        print(E, ticker)
        return 0, 0

def get_ticker_list():
    ticker_list = []
    url = 'https://fapi.binance.com/fapi/v1/exchangeInfo'
    data = requests.get(url)
    candles = data.json()
    for i in candles['symbols']:
        #print(i)
        ticker_list.append(i['symbol'])
    return ticker_list


def scan_market(ticker, interval='15m'):

    results = {}
        #print(i)
    current_ratio, current_volume = get_rel_vol(ticker, 15, interval)
    if current_ratio > 10:
            print('Current Ratio:', current_ratio,'%', 'Current Volume:', current_volume, interval)
            results[interval] = current_ratio

    sorted_values = sorted(results.values()) # Sort the values
    sorted_dict = {}

    for i in sorted_values:
        for k in results.keys():
            if results[k] == i:
                sorted_dict[k] = results[k]
                break
    return sorted_dict


def main(value):
    filter_list = ['1m', '5m', '15m', '1h', '4h']
    ticker_list = get_ticker_list()

    results_list = []
    if value in filter_list:
        results = scan_market(value)
    else:
       for j in ticker_list: 
            for i in filter_list:
                results = scan_market(j, i)
                results_list.append(results)


if __name__ == "__main__":
    main(sys.argv[1])
