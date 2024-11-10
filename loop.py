import logging
from executer import Executer
from strategyStandardDevPump import Strategy
from tools import *
from math import floor
import asyncio, time


logging.basicConfig(level=logging.INFO)
trade_logger = logging.getLogger('trade_logger')
execution_logger = logging.getLogger('execution_logger')

trade_handler = logging.FileHandler('trade_logs.log')
execution_handler = logging.FileHandler('execution_logs.log')

trade_handler.setLevel(logging.INFO)
execution_handler.setLevel(logging.INFO)

trade_formatter = logging.Formatter('%(asctime)s - %(message)s')
execution_formatter = logging.Formatter('%(asctime)s - %(message)s')

trade_handler.setFormatter(trade_formatter)
execution_handler.setFormatter(execution_formatter)

trade_logger.addHandler(trade_handler)
execution_logger.addHandler(execution_handler)


async def main():
    symbols = read_symbols()
    keys = ["date", "open", "high", "low", "price", "volume"]
    e = Executer(symbols)
    s = Strategy()

    if not ping_test():
        print("Not connected to internet")
        return;

    await e.start()

    run = True
    timeFrame = "1m"
    timeLoop = time_frame_to_s(timeFrame)

    is_open = {symbol: False for symbol in symbols}
    has_been_closed = is_open
    candles_dict = [[] for _ in range(len(symbols))]

    await wait_next_minute(time.time(), e)

    start_time = time.time()

    fetch_tasks = [e.mi.fetch_candles_amount(symbol, timeFrame, 2000) for symbol in symbols]
    candles_list = await asyncio.gather(*fetch_tasks)
    for i in range(len(symbols)):
        candles_dict[i] = [dict(zip(keys, candle)) for candle in candles_list[i]]

    print(time.time() - start_time)

    for i, symbol in enumerate(symbols):
        if s.buyingEvaluation(candles_dict[i]):
            #await e.buy_swap(symbol)
            print("buy")
            is_open[symbol] = True

    execution_time = time.time() - start_time
    execution_logger.info(execution_time)

    await e.end()
    return;

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
                trade_logger.info(await e.wallets[0].positionsHistory(symbol, 1))

        execution_time = time.time() - start_time
        execution_logger.info(execution_time)

        if execution_time < 58:
            sleep_time = timeLoop - execution_time - 3
            time.sleep(floor(sleep_time))

            await wait_next_minute(start_time, e)
    
    await e.end()

if __name__ == "__main__":
    asyncio.run(main())