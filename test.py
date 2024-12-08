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

    result = await m.buy_swap(symbol)
    print(result)

    time.sleep(16)

    result = await m.sell_swap(symbol)
    print(result)

    last_trade = await m.last_trades(symbol)
    print(last_trade)

    await m.end()
    

if __name__ == "__main__":
    asyncio.run(main())