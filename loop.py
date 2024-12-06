import logging, json
from executer import Executer
from strategyStandardDevPump import Strategy
from tools import *
from math import floor
from os import remove, path
import asyncio, time


with open('settings.json', 'r') as f:
    settings = json.load(f)

for name in settings["file_names"]:
    if path.exists(name):
        remove(name)

logging.basicConfig(level=logging.INFO)
trade_logger = logging.getLogger('trade_logger')
execution_logger = logging.getLogger('execution_logger')

trade_handler = logging.FileHandler(settings["file_names"]["trade"])
execution_handler = logging.FileHandler(settings["file_names"]["execution"])

trade_handler.setLevel(logging.INFO)
execution_handler.setLevel(logging.INFO)

trade_formatter = logging.Formatter('%(asctime)s - %(message)s')
execution_formatter = logging.Formatter('%(asctime)s - %(message)s')

trade_handler.setFormatter(trade_formatter)
execution_handler.setFormatter(execution_formatter)

trade_logger.addHandler(trade_handler)
execution_logger.addHandler(execution_handler)



async def main():
    global settings
    instruction_file = open(settings["file_names"]["instruction"], "a+")
    instruction_file.seek(0)

    symbols = read_symbols()
    keys = ["date", "open", "high", "low", "price", "volume"]
    e = Executer(symbols, settings)
    s = {symbol: Strategy() for symbol in symbols}

    if not ping_test():
        print("Not connected to internet")
        return

    await e.start()

    timeFrame = "5m" # in minutes
    timeLoop = int(timeFrame[:-1])

    is_open_since = {symbol: 0 for symbol in symbols}
    has_been_closed = {symbol: False for symbol in symbols}

    start_time = time.time()
    
    if start_time % (60 * timeLoop) > 60 * (timeLoop - 1) + 20:
        wait_next_frame(timeLoop)

    start_time = time.time()

    for symbol in symbols:
        s[symbol].candles = [dict(zip(keys, candle)) for candle in await e.mi.fetch_candles_amount(symbol, timeFrame, 2104, start_time)]
        s[symbol].candles = s[symbol].candles[:-1]

    execution_time = time.time() - start_time
    execution_logger.info(f"Start : {execution_time}")

    if execution_time > 37:
        raise ValueError(f"Too long candles fetching time: {execution_time}")
    
    for symbol in symbols:
        s[symbol].createLists()
        s[symbol].candles = s[symbol].candles[-2001:]

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
                    trade_logger.info(f"Sell {symbol}")
                    has_been_closed[symbol] = True
                    #nb = await e.sell_swap(symbol)
                    #trade_logger.info(f"{nb} wallets sold {symbol}")
            else:
                if s[symbol].buyingEvaluation():
                    trade_logger.info(f"Buy {symbol}")
                    is_open_since[symbol] = 1
                    #nb = await e.buy_swap(symbol)
                    #trade_logger.info(f"{nb} wallets bought {symbol}")

        for symbol in symbols:
            if has_been_closed[symbol]:
                #trade_logger.info(await e.last_trades(symbol))
                is_open_since[symbol] = 0
                has_been_closed[symbol] = False

        await e.update_available_cost()

        if (start_time // 60) % 120 == 0:
            for symbol in symbols:
                s[symbol].clean()
            execution_logger.info("Lists cleaned")

        execution_logger.info(time.time() - start_time) # execution time
        
        execution_logger.info(instruction_file.readline())

        if instruction_file.readline().strip() == "stop":
            execution_logger.info("Stopping bot")
            break

        wait_next_frame(timeLoop)

    opened = False
    for symbol in symbols:
        if is_open_since[symbol]:
            opened = True
            break

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
            if is_open_since[symbol] and s[symbol].sellingEvaluation(is_open_since[symbol]):
                trade_logger.info(f"Sell {symbol}")
                has_been_closed[symbol] = True
                #nb = await e.sell_swap(symbol)
                #trade_logger.info(f"{nb} wallets sold {symbol}")

        opened = False
        for symbol in symbols:
            if has_been_closed[symbol]:
                #trade_logger.info(await e.last_trades(symbol))
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

# gestion des coûts
# acheter en swap uniquement si on a assez sur le wallet -> faire une liste des wallets qui ont acheté ou pas
# il reste à update cette liste et gérer les coûts en pourcentage
# faire en sorte que le bot détecte les positions ouvertes et leur donne suite si elles sont ouvertes lorsqu'on lance le bot