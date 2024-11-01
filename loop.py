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
    symbols = ['BTC/USDT','SOL/USDT','ETH/USDT','HNT/USDT']
    keys = ["date", "open", "high", "low", "price", "volume"]
    e = Executer()
    s = Strategy()

    if not ping_test():
        print("erreur")
        return;

    await e.start()

    run = True
    timeFrame = "5m"
    timeLoop = time_frame_to_s(timeFrame)

    candles_dict = list(len(symbols))
    is_open = {symbol: False for symbol in symbols}

    wait_next_minute(time.time(), e)

    while run:
        start_time = time.time()

        fetch_tasks = [e.mi.fetch_candles(symbol, timeFrame, time_frame_to_ms("167h"), 2000) for symbol in symbols]
        candles_list = await asyncio.gather(*fetch_tasks)
        candles_dict = [dict(zip(keys, candle)) for candle in candles_list]

        for i, symbol in enumerate(symbols):
            if is_open[symbol]:
                if s.sellingEvaluation(candles_dict[i]):
                    await e.sell_swap(symbol)
                    is_open[symbol] = False
            else:
                if s.buyingEvaluation(candles_dict[i]):
                    await e.buy_swap(symbol)
                    is_open[symbol] = True

        execution_time = time.time() - start_time

        if execution_time < 58:
            sleep_time = timeLoop - execution_time - 3

            time.sleep(floor(sleep_time))

            await wait_next_minute(start_time, e)
    
    await e.end()
    

if __name__ == "__main__":
    asyncio.run(main())


# tester futures car swap = spot fees -> try futures
# tester leverage
# close positions et pas créer un short -> modifier close_swap

#time.time en s != fetch_time en ms