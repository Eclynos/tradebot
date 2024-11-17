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
    timeFrame = "5m" # in minutes
    timeLoop = time_frame_to_s(timeFrame)

    is_open = {symbol: False for symbol in symbols}
    has_been_closed = is_open
    candles_dict = [[] for _ in range(len(symbols))]

    start_time = time.time()
    
    if start_time % (60 * timeLoop) > 60 * (timeLoop - 1) + 26:
        wait_next_frame(timeLoop)

    start_time = time.time()

    for i, symbol in enumerate(symbols):
        candles_dict[i] = [dict(zip(keys, candle)) for candle in await e.mi.fetch_candles_amount(symbol, timeFrame, 2001, start_time)]
        candles_dict[i] = candles_dict[i][:-1]

    execution_time = time.time() - start_time
    execution_logger.info(execution_time)

    if execution_time > 30:
        raise ValueError(f"Too long candles fetching time: {execution_time}")

    sleep_time = timeLoop - execution_time - 2
    time.sleep(floor(sleep_time))

    wait_next_frame(timeLoop)

    while run:
        start_time = time.time()

        try:
            fetch_tasks = [e.mi.before_last_candle(symbol, timeFrame, floor(start_time * 1000)) for symbol in symbols]
            new_candles = await asyncio.gather(*fetch_tasks)
        except:
            new_candles = []
            for symbol in symbols:
                new_candles.append(e.mi.before_last_candle(symbol, timeFrame, floor(start_time * 1000)))

        for i in range(len(symbols)):
            candles_dict[i] = candles_dict[i][1:]
            candles_dict[i].append(dict(zip(keys, new_candles[i])))

        for i, symbol in enumerate(symbols):
            if is_open[symbol]:
                if s.sellingEvaluation(candles_dict[i]):
                    trade_logger.info(f"sell {symbol}")
                    #await e.sell_swap(symbol)
                    has_been_closed[symbol] = True
            else:
                if s.buyingEvaluation(candles_dict[i]):
                    trade_logger.info(f"buy {symbol}")
                    #await e.buy_swap(symbol) ajouter des différents cas de logs en fonction d'echec ou de reussite de l'achat
                    is_open[symbol] = True

        for symbol in symbols:
            if has_been_closed[symbol]:
                #trade_logger.info(await e.last_trades(symbol))
                is_open[symbol] = False
                has_been_closed[symbol] = False

        if (start_time//60) % 120 == 0:
            s.clean()

        execution_time = time.time() - start_time
        execution_logger.info(execution_time)

        time.sleep(timeLoop * 60 - execution_time)
    
    await e.end()

if __name__ == "__main__":
    asyncio.run(main())