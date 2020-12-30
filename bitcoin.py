import requests      #for making HTTP requests
import json          #for handling json data
import time          #for sleep operation
from boltiot import Bolt
import conf          #configuration file


def get_bitcoin_price():
    URL="https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD"
    response = requests.request("GET",URL,verify=False)
    response = json.loads(response.text)
    print("response is",response)
    current_price = response["USD"]
    return current_price
print(get_bitcoin_price())
trade_price=20000
mybolt=Bolt(conf.API_KEY,conf.DEVICE_ID)

while True:
      sale_price=get_bitcoin_price()
      try:
         print("Current sale price is", sale_price)
         print("Your selling price is", trade_price)
         if sale_price>trade_price:
            print("Turning on LED for 5 seconds")
            response_1=mybolt.digitalWrite('0','HIGH')
            print(response_1)
            time.sleep(5)
            response_1=mybolt.digitalWrite('0','LOW')
            print(response_1)
            time.sleep(5)


      except Exception as e:
             print("ERROR OCCURRED")
             print(e)

      time.sleep(60)
