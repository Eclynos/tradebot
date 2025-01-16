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

    amount = await m.mi.actual_currency_equivalence(symbol, 6)

    order = await m.wallets[who].openp(symbol, amount, 'buy')
    print(order)

    time.sleep(18)

    order = await m.wallets[who].closep(symbol)
    print(order)

    time.sleep(3)

    await m.end()
    

if __name__ == "__main__":
    asyncio.run(main())



