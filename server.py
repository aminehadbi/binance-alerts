from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import requests
# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Create server
with SimpleXMLRPCServer(('0.0.0.0', 8000),
                        requestHandler=RequestHandler,
                        logRequests=False) as server:

    def check_price(symbol):
       try:
           url = 'https://fapi.binance.com/fapi/v1/depth?symbol='+symbol+'&limit=10'
           #print(url)
           data = requests.get(url)
           data = data.json()
           ob_bid = []
           ob_ask = []
           total_bids = 0
           total_asks = 0

           for i in data['bids']:
               ob_bid.append(float(i[0])*float(i[1]))
               total_bids += float(i[1])

           for i in data['asks']:
               ob_ask.append(float(i[0])*float(i[1]))
               total_asks += float(i[1])

           best_ask = sum(ob_ask)/total_asks
           best_bid = sum(ob_bid)/total_bids

           print(symbol,best_bid, best_ask)
           return best_bid, best_ask
       except Exception as E:
           print(E)
           return 0, 0

    def check_ob_imbalance(symbol):
       try:
           url = 'https://fapi.binance.com/fapi/v1/depth?symbol='+symbol+'&limit=100'
           #print(url)
           data = requests.get(url)
           data = data.json()
           ob_bid = []
           ob_ask = []

           for i in data['bids']:
               ob_bid.append(float(i[0])*float(i[1]))
           for i in data['asks']:
               ob_ask.append(float(i[0])*float(i[1]))
           ob_imbalance = sum(ob_ask)/sum(ob_bid)

           if ob_imbalance > 1:
               print(symbol, ob_imbalance)
           return ob_imbalance
       except Exception as E:
           print(E)
           return symbol

    server.register_function(check_price, 'check_price')
    server.register_function(check_ob_imbalance, 'check_ob_imbalance')

    # Run the server's main loop
    server.serve_forever()
