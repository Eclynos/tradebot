from executer import Executer
from strategyStandardDevPump import Strategy
from tools import *
from math import floor
import asyncio, time
    
async def main():
    symbols = read_symbols()
    keys = ["date", "open", "high", "low", "price", "volume"]
    e = Executer(symbols)
    s = Strategy()

    if not ping_test():
        print("erreur")
        return
    
    symbol = "BTC/USDT"

    await e.start()

    await e.buy_swap(symbol)

    time.sleep(16)

    await e.sell_swap(symbol)

    await e.end()
    

if __name__ == "__main__":
    asyncio.run(main())