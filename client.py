import xmlrpc.client
import requests
import datetime

s = xmlrpc.client.ServerProxy('http://149.248.58.98:8000')

def get_ticker_list():
    ticker_list = []
    url = 'https://fapi.binance.com/fapi/v1/exchangeInfo'
    data = requests.get(url)
    candles = data.json()
    for i in candles['symbols']:
        ticker_list.append(i['pair'])
    return ticker_list

def scan_market():
    ticker_list = get_ticker_list()
    now = datetime.datetime.now()
    timestamp = datetime.datetime.timestamp(now)
    with open('outfile.txt', 'a') as fp:
        fp.write(str(timestamp)+'\n')
        fp.close()
    #symbol = input('Type your symbol: \n')
    for symbol in ticker_list:
        results = s.check_ob_imbalance(symbol)
        best_bid, best_ask = s.check_price(symbol)
        try:
            if results > 2 or results < 0.5:
                if results > 2:
                    print(symbol, 'going down. Ratio:', str(0-results), (best_bid+best_ask)/2)
                if results < 0.5:
                    print(symbol, 'going up. Ratio:', str(1/results), (best_bid+best_ask)/2)

                #print(results, symbol, (best_bid+best_ask)/2)
            with open('outfile.txt', 'a') as fp:
                fp.write(symbol+' '+str(results)+'\n')
                fp.close()
        except Exception as E:
            print(symbol, E)
            pass
while True:
    #choice = input('Choose 1 2 3 4')
    choice = '1'
    if choice == '1':
        scan_market()
    if choice == '12':
        symbol = input('Choose a symbol to buy')
        #send order
        #confirm position
    if choice == '13':
        symbol = input('Choose a symbol to sell')
        #send order
        #confirm position
    if choice == '10':
        #close all position
        pass
    if choice == '22':
        symbol = input('Choose a symbol to buy short') 
    if choice == '23':
        symbol = input('Choose a symbol to sell short')
