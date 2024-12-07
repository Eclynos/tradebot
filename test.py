from manager import Manager
from strategyStandardDevPump import Strategy
from tools import *
from math import floor
import asyncio, time
    
async def main():
    symbols = read_symbols()
    keys = ["date", "open", "high", "low", "price", "volume"]
    m = Manager(symbols)

    if not ping_test():
        print("erreur")
        return
    
    symbol = "BTC/USDT"

    await m.start()

    await m.buy_swap(symbol)

    time.sleep(16)

    await m.sell_swap(symbol)

    await m.end()
    

if __name__ == "__main__":
    asyncio.run(main())