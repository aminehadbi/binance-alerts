import requests
import json
import ast

def look_for_liquid_pairs:
    data = requests.get('https://tradeogre.com/api/v1/markets')
    data = ast.literal_eval(data.text)
    for i in data:
        symbol = i.keys()
        result = i.values()
        for i in result:
            try:
                spread = 100*(float(i['ask'])-float(i['bid']))/float(i['ask'])
                if spread < 1:
                    print(symbol, spread)
                else:
                    pass
            except:
                print(symbol, 'no market')
