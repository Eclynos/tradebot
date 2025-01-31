from manager import Manager
from strategyStandardDevPump import Strategy
from tools import *
from math import floor
import asyncio, time, json

with open('settings.json', 'r') as f:
    settings = json.load(f)
    
async def main():
    symbols = read_symbols()
    keys = ["date", "open", "high", "low", "price", "volume"]
    m = Manager(symbols, settings)

    if not ping_test():
        print("erreur")
        return
    
    symbol = "HNT/USDT"
    await m.start()
    who = "nathael"
    price = await m.mi.getPrice(symbol)
    amount = m.mi.currency_equivalence(8, price)

    """
    order = await m.wallets[who].openp(
        symbol,
        amount,
        'buy')
    
    print(order)
    """

    """
    order = await m.wallets[who].stopLoss(
        symbol,
        price * 0.95,
        amount * 2
    )
    """

    #orderid = order['orderId']
    #print(order)
    #'1266646161638887425'
    #'1266645498068615180'

    #print(symbol + ':USDT', 'market', 'buy', amount, price, price * 0.97)
    #order = await m.wallets[who].exchange.edit_order('1266646161638887425', symbol + ':USDT', 'market', 'buy', amount, price=price, params = {'stopLossPrice': price * 0.97})
    #print(order)

    try:
        order = await m.wallets[who].exchange.cancel_order('1266646161638887425', symbol + ':USDT')
        print(order)
    except Exception as e:
        print(e)

    orderbook = await m.wallets[who].exchange.fetch_orders(symbol + ':USDT')
    print(orderbook)

    await m.end()
    

if __name__ == "__main__":
    asyncio.run(main())

#createOrdersssss