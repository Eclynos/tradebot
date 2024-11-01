from executer import Executer
from strategyStandardDevPump import Strategy
from math import floor
import asyncio, time
    
    
async def main():
    e = Executer()
    s = Strategy()
    await e.start()

    run = True
    timeFrame = "1m"
    timeLoop = e.t.time_frame_to_s(timeFrame)

    is_open = {}
    candles = {}
    for symbol in e.symbols:
        is_open[symbol] = False
        candles[symbol] = []

    while run:
        start_time = time.time()

        for symbol in e.symbols:
            await e.mi.fetch_candles(symbol, timeFrame, e.t.time_frame_to_ms("30d"))

        for symbol in e.symbols:
            if is_open[symbol]:
                if s.sellingEvaluation(candles[symbol]):
                    await e.sell_swap(symbol)
                    is_open[symbol] = False
            else:
                if s.buyingEvaluation(candles[symbol]):
                    await e.buy_swap(symbol)
                    is_open[symbol] = True

        execution_time = time.time() - start_time

        if execution_time < 58:
            sleep_time = timeLoop - execution_time - 3

            time.sleep(floor(sleep_time))

            while True:
                time.sleep(0.1) # prevents serv ddos
                start = floor(start_time) // 60
                actual = await e.mi.exchange.fetch_time() // 60000
                if actual > start:
                    break
    
    await e.end()
    

if __name__ == "__main__":
    asyncio.run(main())


# tester futures car swap = spot fees -> try futures
# tester leverage
# close positions et pas créer un short -> modifier close_swap

#time.time en s != fetch_time en ms