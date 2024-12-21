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

    await m.start()

    start_time = time.time()
    try:
        fetch_tasks = [m.mi.before_last_candle(symbol, "5m", start_time) for symbol in symbols]
        new_candles = await asyncio.gather(*fetch_tasks)
        print(time.time() - start_time)
    except Exception as e:
        print(e)

    time.sleep(3)

    await m.end()
    

if __name__ == "__main__":
    asyncio.run(main())