# import the Binance client from python-binance module
from binance.client import Client
import time


# define your API key and secret
API_KEY = ""     #enter your own api key
API_SECRET = ""  #enter your own api secret

# define the client
client = Client (API_KEY, API_SECRET)

# create a variable that will hold the value of USDT in your account
get_usdt_balance = client.get_asset_balance(asset="USDT")
get_btc_balance = client.get_asset_balance(asset="BTC")
#orders = client.get_all_orders(symbol='BTCUSDT', limit=1)
#info = client.get_account()
get_my_last_trades = client.get_my_trades(symbol='BTCUSDT', limit=1)
prices = client.get_all_tickers()

last_buy_price = float(prices[11]['price'])
last_sell_price = float(prices[11]['price'])
buy_multiplier = 10
sell_multiplier =  10
qty = 0.001
counter = 0
trailing = 0
stop_trail = 0
market_side = ""


def shift_trade():
    global last_buy_price, last_sell_price, buy_multiplier, sell_multiplier,qty, counter, trailing, stop_trail, market_side

    get_my_last_trades = client.get_my_trades(symbol='BTCUSDT', limit=1)
    get_usdt_balance = client.get_asset_balance(asset="USDT")
    get_btc_balance = client.get_asset_balance(asset="BTC")
    #avg_price = client.get_avg_price(symbol='BTCUSDT')
    prices = client.get_all_tickers()

    print("-----------------------------------------------")
    print("--------------------------------------")
    print("|  USDT BALANCE     : " + str(get_usdt_balance['free']) )
    print("|  BTC BALANCE      : " + str(get_btc_balance['free']) )
    print("--------------------------------------")
    print(" *  My last price   : " + str(get_my_last_trades[0]['price']))
    print(" *  Market price    : " + str(prices[11]['price']))

    """if (get_my_last_trades[0]['isBuyer'] == True):
      print(" *  Last Action     : Buy")
    else:
      print(" *  Last Action     : sell")"""
    
    print(" *  Last Action     : " + market_side)
    print(" *  Last Buy Price  : " + str(last_buy_price))
    print(" *  Last Sell Price : " + str(last_sell_price))
    print(" *  Buy Multiplier  : " + str(buy_multiplier))
    print(" *  Sell Multiplier : " + str(sell_multiplier))
    print(" *  Error counter   : " + str(counter))
    print("")


    if (float(prices[11]['price'])  >= (float(last_buy_price) + float(sell_multiplier))) \
        and (buy_multiplier > sell_multiplier):

            trailing = float(prices[11]['price'])
            stop_trail = float(prices[11]['price'])
            trailing_sell()
                
                

            print("")
            print("Selling 1")
            print("******************************************")
            print("placing order for sell")
            
            
            sell_order =  client.order_market_sell(
                symbol='BTCUSDT',
                quantity=qty,
              )

            last_sell_price = float(sell_order['fills'][0]['price'])
            market_side = sell_order['side']
            
            
            sell_multiplier *= 2
            buy_multiplier = 10
            counter = 0
            trailing = 0

            print("******************************************")
            print("current_price : " + str(float(prices[11]['price'])))
            print("last_trade_price : " + str(get_my_last_trades[0]['price']))
            print("is last transaction buy : " + str((get_my_last_trades[0]['isBuyer'])))


    
    if (float(prices[11]['price'])  >= (float(last_sell_price) + float(sell_multiplier))):

            trailing = float(prices[11]['price'])
            stop_trail = float(prices[11]['price'])
            trailing_sell()
                
        
            print("")
            print("Selling 2")
            print("******************************************")
            print("placing order for sell")

            sell_order =  client.order_market_sell(
                symbol='BTCUSDT',
                quantity=qty,
              )

            last_sell_price = float(sell_order['fills'][0]['price'])
            market_side = sell_order['side']
            
            sell_multiplier *= 2
            buy_multiplier = 10
            counter = 0
            trailing = 0

            print("******************************************")
            print("current_price : " + str(float(prices[11]['price'])))
            print("last_trade_price : " + str(get_my_last_trades[0]['price']))
            print("is last transaction buy : " + str((get_my_last_trades[0]['isBuyer'])))


    if (float(prices[11]['price'])  <= (float(last_sell_price) - float(buy_multiplier))) \
        and (sell_multiplier > buy_multiplier):

          trailing = float(prices[11]['price'])
          stop_trail = float(prices[11]['price'])
          trailing_buy()
                
    
          print("")
          print("Buying 1")
          print("******************************************")
          print("placing order for buy")

          buy_order =  client.order_market_buy(
                symbol='BTCUSDT',
                quantity=qty,
              )

          last_buy_price = float(buy_order['fills'][0]['price'])
          market_side = buy_order['side']
          buy_multiplier *= 2
          sell_multiplier = 10
          counter = 0
          trailing = 0
          

          print("******************************************")
          print("Current Price    : " + str(float(prices[11]['price'])))
          print("Last Trade Price : " + str(get_my_last_trades[0]['price']))
          print("Last Trade Type  : " + market_side)
          print("")

    

    #- float(buy_multiplier))
    if (float(prices[11]['price'])  <= (float(last_buy_price) - float(buy_multiplier))) :
       #if float(get_usdt_balance['free']) > 14:

          trailing = float(prices[11]['price'])
          stop_trail = float(prices[11]['price'])
          trailing_buy()      
         
          print("")
          print("Buying 2")
          print("******************************************")
          print("placing order for buy")
          
          
          buy_order =  client.order_market_buy(
                symbol='BTCUSDT',
                quantity=qty,
              )

          last_buy_price = float(buy_order['fills'][0]['price'])
          market_side = buy_order['side'] 
          buy_multiplier *= 2
          sell_multiplier = 10
          counter = 0
          trailing = 0
          

          print("******************************************")
          print("current_price : " + str(float(prices[11]['price'])))
          print("last_trade_price : " + str(get_my_last_trades[0]['price']))
          print("is last transaction buy : " + str((get_my_last_trades[0]['isBuyer'])))
          print("")


def trailing_buy():
    global trailing, stop_trail, prices, qty
    
    prices = client.get_all_tickers()

    print("--------------------------------------")
    print("Decreasing trailing buy" )
    print("--------------------------------------")
    print("|  TRAILING BUY       : " + str(trailing))
    print("|  CURRENT PRICE      : " + str(prices[11]['price']))
    print("--------------------------------------")

    if float(prices[11]['price']) <= (trailing + 2):
            trailing = float(prices[11]['price'])
            #time.sleep(2)
            trailing_buy()    
    
   


def trailing_sell():
    global trailing, prices, stop_trail, qty

    prices = client.get_all_tickers()

    print("--------------------------------------")
    print("Increasing trailing sell" )
    print("--------------------------------------")
    print("|  TRAILING SELL      : " + str(trailing))
    print("|  CURRENT PRICE      : " + str(prices[11]['price']))
    print("--------------------------------------")

    
    if float(prices[11]['price']) >= (trailing - 2):
      trailing = float(prices[11]['price'])
      #time.sleep(2)
      trailing_sell()
    
    


def cancel_all_order():
  OpenOrder = client.get_open_orders(symbol='BTCUSDT')
  print("")
  print("Deleting all open Order")
  print("******************************************")
  print("Symbol    Side   Qauntity    Price")
  print("------------------------------------------")

  for pendingOrder in OpenOrder:
    print (pendingOrder['symbol'] + "   " + pendingOrder['side'] + "   " + pendingOrder['origQty'] + "   "+pendingOrder['price'])
    client.cancel_order(
      symbol='BTCUSDT',
      orderId= pendingOrder['orderId']
    )
  
  print("******************************************")
  print("")





def main():
  global last_buy_price, last_sell_price, buy_multiplier, sell_multiplier,qty,counter 
  while True:
    try: 
      print("")
      print("BTCUSDT Spot Market Scanning...")
      time.sleep(5)
      shift_trade()
      
    except Exception as e:
      print(e)
      counter += 1
      #if "insufficient balance" in str(e):
      if counter == 10:
        print("Insufficient balance... Shifting to new position")
        print("waiting for 10 sec before re-initializing trade values")
        time.sleep(10)
        
        buy_multiplier = 10
        sell_multiplier = 10
        counter = 0

        cancel_all_order()
        prices = client.get_all_tickers()
        last_buy_price = float(prices[11]['price'])
        last_sell_price = float(prices[11]['price'])

        main()


if __name__ == '__main__':
  main()


