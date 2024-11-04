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

    run = True
    timeFrame = "5m"
    timeLoop = time_frame_to_s(timeFrame)

    log_file = open('trade_logs', 'a')

    candles_dict = list(len(symbols))
    is_open = {symbol: False for symbol in symbols}
    has_been_closed = {symbol: False for symbol in symbols}

    wait_next_minute(time.time(), e)

    start_time = time.time()

    fetch_tasks = [e.mi.fetch_candles(symbol, timeFrame, time_frame_to_ms("167h"), 2000) for symbol in symbols]
    candles_list = await asyncio.gather(*fetch_tasks)
    candles_dict = [dict(zip(keys, candle)) for candle in candles_list]

    for i, symbol in enumerate(symbols):
        if is_open[symbol]:
            if s.sellingEvaluation(candles_dict[i]):
                await e.sell_swap(symbol)
                has_been_closed = True
        else:
            if s.buyingEvaluation(candles_dict[i]):
                await e.buy_swap(symbol)
                is_open[symbol] = True

    for symbol in symbols:
        if has_been_closed[symbol]:
            log_file.write(await e.wallets[0].positionsHistory(symbol, 1))

    execution_time = time.time() - start_time

    if execution_time < 58:
        sleep_time = timeLoop - execution_time - 3

        time.sleep(floor(sleep_time))

        await wait_next_minute(start_time, e)


    while run:
        start_time = time.time()

        fetch_tasks = [e.mi.before_last_candle(symbol, timeFrame, start_time // 1000) for symbol in symbols]
        new_candles = await asyncio.gather(*fetch_tasks)
        candles_dict = [dict(zip(keys, candle)) for candle in candles_list]

        for i, symbol in enumerate(symbols):
            if is_open[symbol]:
                if s.sellingEvaluation(candles_dict[i]):
                    await e.sell_swap(symbol)
                    has_been_closed = True
            else:
                if s.buyingEvaluation(candles_dict[i]):
                    await e.buy_swap(symbol)
                    is_open[symbol] = True

        for symbol in symbols:
            if has_been_closed[symbol]:
                log_file.write(await e.wallets[0].positionsHistory(symbol, 1))

        execution_time = time.time() - start_time

        if execution_time < 58:
            sleep_time = timeLoop - execution_time - 3

            time.sleep(floor(sleep_time))

            await wait_next_minute(start_time, e)
    
    await e.end()

    log_file.close()
    

if __name__ == "__main__":
    asyncio.run(main())