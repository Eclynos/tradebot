from executer import Executer
from strategyStandardDevPump import Strategy
from tools import *
from math import floor
import asyncio, time


async def wait_next_minute(start_time, e):
    """Teste si on a changé de minute"""
    while True:
        time.sleep(0.1) # prevents serv ddos
        start = floor(start_time) // 60
        actual = await e.mi.exchange.fetch_time() // 60000 #request
        if actual > start:
            break

    
async def main():
    symbols = read_symbols()
    keys = ["date", "open", "high", "low", "price", "volume"]
    e = Executer(symbols)
    s = Strategy()

    if not ping_test():
        print("erreur")
        return;

    await e.start()

    timeFrame = "5m"

    log_file = open('trade_logs', 'a')

    candles_dict = [[] for _ in range(len(symbols))]
    is_open = {symbol: False for symbol in symbols}

    fetch_tasks = [e.mi.fetch_candles_amount(symbol, timeFrame, 2) for symbol in symbols]
    candles_list = await asyncio.gather(*fetch_tasks)
    for i in range(len(symbols)):
        candles_dict[i] = [dict(zip(keys, candle)) for candle in candles_list[i]]

    print(candles_dict)

    await e.end()

    log_file.close()
    

if __name__ == "__main__":
    asyncio.run(main())