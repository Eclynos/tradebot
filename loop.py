import logging, json
from manager import Manager
from strategyStandardDevPump import Strategy
from tools import *
from os import remove, path
import asyncio, time


with open('settings.json', 'r') as f:
    settings = json.load(f)

for name in settings["file_names"].values():
    if path.exists(name):
        remove(name)

with open(settings["file_names"]["instruction"], "a+", encoding="utf-8") as f:
    f.write("")


logging.basicConfig(level=logging.INFO)
trade_logger = logging.getLogger('trade_logger')
execution_logger = logging.getLogger('execution_logger')
percentage_logger = logging.getLogger('percentage_logger')

trade_handler = logging.FileHandler(settings["file_names"]["trade"])
execution_handler = logging.FileHandler(settings["file_names"]["execution"])
percentage_handler = logging.FileHandler(settings["file_names"]["percentage"])

trade_handler.setLevel(logging.INFO)
execution_handler.setLevel(logging.INFO)
percentage_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(message)s')
trade_handler.setFormatter(formatter)
execution_handler.setFormatter(formatter)
percentage_handler.setFormatter(formatter)

trade_logger.addHandler(trade_handler)
execution_logger.addHandler(execution_handler)
percentage_logger.addHandler(percentage_handler)



async def main():
    global settings
    instruction_file = open(settings["file_names"]["instruction"], "r+", encoding='utf-8')
    instruction_file.truncate(0)
    instruction_file.seek(0)

    symbols = read_symbols() # nombre max de symboles : 21
    keys = ["date", "open", "high", "low", "price", "volume"]
    m = Manager(symbols, settings)
    s = {symbol: Strategy() for symbol in symbols}

    if not ping_test():
        print("Not connected to internet")
        return

    await m.start()

    timeFrame = "5m" # in minutes
    timeLoop = int(timeFrame[:-1])

    has_been_closed = {symbol: False for symbol in symbols}

    start_time = time.time()
    
    if start_time % (60 * timeLoop) > 60 * (timeLoop - 1) + 20:
        wait_next_frame(timeLoop)

    start_time = time.time()

    for symbol in symbols:
        s[symbol].candles = [dict(zip(keys, candle)) for candle in await m.mi.fetch_candles_amount(symbol, timeFrame, 2104, start_time)]
        s[symbol].candles = s[symbol].candles[:-1]

    is_open_since, bought_type = await m.load_positions(timeLoop)

    execution_time = time.time() - start_time

    execution_logger.info(f"Start : {execution_time}")

    if execution_time > 37:
        raise ValueError(f"Too long candles fetching time: {execution_time}")
    
    for symbol in symbols:
        s[symbol].createLists()
        s[symbol].candles = s[symbol].candles[-2001:]

    wait_next_frame(timeLoop)

    while True:
        time.sleep(1)
        start_time = time.time()

        is_open_since = {k: v + 1 if v > 0 else v for k, v in is_open_since.items()}

        try:
            fetch_tasks = [m.mi.before_last_candle(symbol, timeFrame, start_time) for symbol in symbols]
            new_candles = await asyncio.gather(*fetch_tasks)
        except:
            try:
                new_candles = [await m.mi.before_last_candle(symbol, timeFrame, start_time) for symbol in symbols]
            except:
                execution_logger.info("No connection")
                time.sleep(timeLoop/5)
                try:
                    new_candles = [await m.mi.before_last_candle(symbol, timeFrame, start_time) for symbol in symbols]
                except:
                    execution_logger.info("Totally disconnected")

        if len(new_candles) == len(symbols):
            for i, symbol in enumerate(symbols):
                s[symbol].candles = s[symbol].candles[1:]
                s[symbol].candles.append(dict(zip(keys, new_candles[i])))
                s[symbol].updateLists()
                if is_open_since[symbol] != 0:
                    if s[symbol].sellingEvaluation(is_open_since[symbol], bought_type[symbol]):
                        trade_logger.info(f"Close {symbol} at {await m.mi.getPrice(symbol)} | strategy used : {bought_type[symbol]}")
                        has_been_closed[symbol] = True
                        nb = await m.close_swap(symbol)
                        trade_logger.info(f"{nb} wallets closed {symbol}")
                else:
                    if s[symbol].buyingEvaluation("dip"):
                        trade_logger.info(f"Buy {symbol} at {await m.mi.getPrice(symbol)} | strategy used : dip")
                        is_open_since[symbol] = 1
                        bought_type[symbol] = "dip"
                        nb = await m.long_swap(symbol)
                        trade_logger.info(f"{nb} wallets bought {symbol}")
                    """
                    elif s[symbol].buyingEvaluation("pump"):
                        trade_logger.info(f"Buy {symbol} at {await m.mi.getPrice(symbol)} | strategy used : pump")
                        is_open_since[symbol] = 1
                        bought_type[symbol] = "pump"
                        nb = await m.long_swap(symbol)
                        trade_logger.info(f"{nb} wallets bought {symbol}")
                    """

        for symbol in symbols:
            if has_been_closed[symbol]:
                trades, percentage = await m.last_trades(symbol)
                trade_logger.info(trades)
                percentage_logger.info(f"{symbol}\n{percentage}")
                is_open_since[symbol] = 0
                has_been_closed[symbol] = False

        if (start_time // 60) % 120 == 0:
            for symbol in symbols:
                s[symbol].clean()
            with open('settings.json', 'r') as f:
                await m.update_settings(json.load(f))
            execution_logger.info("Lists cleaned and settings updated")
        elif (start_time // 60) % 120 == 60:
            await m.calculate_min_amounts()
            execution_logger.info("Min amounts updated")

        await m.update_cost_datas()

        execution_logger.info(time.time() - start_time)

        instruction_file.seek(0)
        if instruction_file.read().strip().lower() == "stop":
            execution_logger.info("Stopping bot")
            break

        wait_next_frame(timeLoop)

    opened = False
    for symbol in symbols:
        if is_open_since[symbol]:
            opened = True
            break

    while opened:
        time.sleep(1)
        start_time = time.time()

        is_open_since = {k: v + 1 if v > 0 else v for k, v in is_open_since.items()}

        try:
            fetch_tasks = [m.mi.before_last_candle(symbol, timeFrame, start_time) for symbol in symbols]
            new_candles = await asyncio.gather(*fetch_tasks)
        except:
            try:
                new_candles = [await m.mi.before_last_candle(symbol, timeFrame, start_time) for symbol in symbols]
            except:
                execution_logger.info("No connection")
                time.sleep(timeLoop/5)
                try:
                    new_candles = [await m.mi.before_last_candle(symbol, timeFrame, start_time) for symbol in symbols]
                except:
                    execution_logger.info("Totally disconnected")

        if len(new_candles) == len(symbols):
            for i, symbol in enumerate(symbols):
                s[symbol].candles = s[symbol].candles[1:]
                s[symbol].candles.append(dict(zip(keys, new_candles[i])))
                s[symbol].updateLists()
                if is_open_since[symbol] != 0 and s[symbol].sellingEvaluation(is_open_since[symbol], bought_type[symbol]):
                    trade_logger.info(f"Close {symbol} at {await m.mi.getPrice(symbol)} | strategy used : {bought_type[symbol]}")
                    has_been_closed[symbol] = True
                    nb = await m.close_swap(symbol)
                    trade_logger.info(f"{nb} wallets closed {symbol}")

        opened = False
        for symbol in symbols:
            if has_been_closed[symbol]:
                trades, percentage = await m.last_trades(symbol)
                trade_logger.info(trades)
                percentage_logger.info(f"{symbol}\n{percentage}")
                is_open_since[symbol] = 0
                has_been_closed[symbol] = False
            if is_open_since[symbol]:
                opened = True

        if (start_time // 60) % 120 == 0:
            for symbol in symbols:
                s[symbol].clean()
            with open('settings.json', 'r') as f:
                await m.update_settings(json.load(f))
            execution_logger.info("Lists cleaned and settings updated")
        elif (start_time // 60) % 120 == 60:
            await m.calculate_min_amounts()
            execution_logger.info("Min amounts updated")

        await m.update_cost_datas()    

        execution_logger.info(time.time() - start_time)

        wait_next_frame(timeLoop)
    
    await m.end()

    execution_logger.info("Bot stopped")

    instruction_file.close()

if __name__ == "__main__":
    asyncio.run(main())