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
    
    symbol = "BGB/USDT"
    await m.start()
    who = "nathael"
    price = await m.mi.getPrice(symbol)
    print(price)
    amount = m.mi.currency_equivalence(8, price)
    print(amount)

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
        price * 0.95
    )
    """

    """
    order = await m.wallets[who].exchange.create_order(symbol + ':USDT', 'market', 'buy', amount, params = {'stopLossPrice': price * 0.95})
    print(order)
    """
    #print(order[''])

    order = await m.wallets[who].exchange.edit_order('1265584352184901633', symbol + ':USDT', 'market', 'buy', amount, price=price, params = {'stopLossPrice': price * 0.96})
    print(order)

    await m.end()
    

if __name__ == "__main__":
    asyncio.run(main())