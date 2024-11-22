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
    instruction_file = open("instruction", "w+")

    symbols = read_symbols()
    keys = ["date", "open", "high", "low", "price", "volume"]
    e = Executer(symbols)
    s = {symbol: Strategy() for symbol in symbols}

    if not ping_test():
        print("Not connected to internet")
        return

    await e.start()

    timeFrame = "5m" # in minutes
    timeLoop = time_frame_to_s(timeFrame)

    is_open_since = {symbol: 0 for symbol in symbols}
    has_been_closed = {symbol: False for symbol in symbols}

    start_time = time.time()
    
    if start_time % (60 * timeLoop) > 60 * (timeLoop - 1) + 26:
        wait_next_frame(timeLoop)

    start_time = time.time()

    for i, symbol in enumerate(symbols):
        s[symbol].candles = [dict(zip(keys, candle)) for candle in await e.mi.fetch_candles_amount(symbol, timeFrame, 2001, start_time)]
        s[symbol].candles = s[symbol].candles[:-1]

    execution_time = time.time() - start_time
    execution_logger.info(f"Start : {execution_time}")

    if execution_time > 30:
        raise ValueError(f"Too long candles fetching time: {execution_time}")

    wait_next_frame(timeLoop)

    while True:
        start_time = time.time()

        is_open_since = {k: v + 1 if v > 0 else v for k, v in is_open_since.items()}

        try:
            fetch_tasks = [e.mi.before_last_candle(symbol, timeFrame, floor(start_time * 1000)) for symbol in symbols]
            new_candles = await asyncio.gather(*fetch_tasks)
        except:
            new_candles = [await e.mi.before_last_candle(symbol, timeFrame, floor(start_time * 1000)) for symbol in symbols]

        for i, symbol in enumerate(symbols):
            s[symbol].candles = s[symbol].candles[1:]
            s[symbol].candles.append(dict(zip(keys, new_candles[i])))
            s[symbol].updateLists()
            if is_open_since[symbol]:
                if s[symbol].sellingEvaluation(is_open_since[symbol]):
                    if await e.sell_swap(symbol):
                        trade_logger.info(f"Sell {symbol}")
                        has_been_closed[symbol] = True
                    else:
                        trade_logger.info(f"Failed selling {symbol}")
            else:
                if s[symbol].buyingEvaluation():
                    message = await e.buy_swap(symbol)
                    if message == None:
                        trade_logger.info(f"Buy {symbol}")
                        is_open_since[symbol] = 1
                    elif message == "spot":
                        pass
                    else:
                        trade_logger.info(f"Failed buying {symbol}\n{message}")

        for symbol in symbols:
            if has_been_closed[symbol]:
                trade_logger.info(await e.last_trades(symbol))
                is_open_since[symbol] = 0
                has_been_closed[symbol] = False

        await e.update_available_cost()

        if (start_time // 60) % 120 == 0:
            for symbol in symbols:
                s[symbol].clean()
                execution_logger.info("Lists cleaned")

        execution_logger.info(time.time() - start_time) # execution time

        if instruction_file.readline() == "stop":
            execution_logger.info("Stopping bot")
            break

        wait_next_frame(timeLoop)

    opened = True

    while opened:
        start_time = time.time()

        is_open_since = {k: v + 1 if v > 0 else v for k, v in is_open_since.items()}

        try:
            fetch_tasks = [e.mi.before_last_candle(symbol, timeFrame, floor(start_time * 1000)) for symbol in symbols]
            new_candles = await asyncio.gather(*fetch_tasks)
        except:
            new_candles = [await e.mi.before_last_candle(symbol, timeFrame, floor(start_time * 1000)) for symbol in symbols]

        for i, symbol in enumerate(symbols):
            s[symbol].candles = s[symbol].candles[1:]
            s[symbol].candles.append(dict(zip(keys, new_candles[i])))
            s[symbol].updateLists()
            if is_open_since[symbol]:
                if s[symbol].sellingEvaluation(is_open_since[symbol]):
                    if await e.sell_swap(symbol):
                        trade_logger.info(f"Sell {symbol}")
                        has_been_closed[symbol] = True
                    else:
                        trade_logger.info(f"Failed selling {symbol}")

        opened = False
        for symbol in symbols:
            if has_been_closed[symbol]:
                trade_logger.info(await e.last_trades(symbol))
                is_open_since[symbol] = 0
                has_been_closed[symbol] = False
            if is_open_since[symbol]:
                opened = True

        await e.update_available_cost()

        if (start_time // 60) % 120 == 0:
            for symbol in symbols:
                s[symbol].clean()
                execution_logger.info("Lists cleaned")          

        execution_logger.info(time.time() - start_time) # execution time

        wait_next_frame(timeLoop)
    
    await e.end()

    execution_logger.info("Bot stopped")

    instruction_file.close()

if __name__ == "__main__":
    asyncio.run(main())

# gerer les tradable costs -> creer un etat de retour "pas assez de moula dans le wallet" à buy_swap
# gerer les min amounts