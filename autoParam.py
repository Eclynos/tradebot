from strategyStandardDevPump import *
from dataAnalysis import *
from tools import *
import time, threading, sys

SAMPLE_SIZE = 2000
LAUNCH_SAMPLE_SIZE = 2104

coinCodes = [
    "SOL"
]

data = [readFile(coinCode, "bitget") for coinCode in coinCodes]

currentDate = time.time() * 1000
SEindex = [getDataIndex(currentDate, "18M", "6M", coinData, LAUNCH_SAMPLE_SIZE) for coinData in data]

data = [data[i][SEindex[i][0]-LAUNCH_SAMPLE_SIZE:SEindex[i][1]] for i in range(len(coinCodes))]
data = [[{"date": int(data[i][j]["date"]) // 1000, "price": float(data[i][j]["close"]), "index" :j} for j in range(len(data[i]))] for i in range(len(coinCodes))]

NB_INSTANCES_PER_PARAM = 9
NB_PARAMS = 5
STRATEGY_NAME = "dip"
PERCENTAGE_TRADED = 0.5
CANDLES_IN_PERIOD = SEindex[0][1] - SEindex[0][0]

s = Strategy(100, SAMPLE_SIZE, 0.92, 0.92, 1.5, 0, 1, 100)

INSTANCES = {
    "power1": [0.936, 0.937, 0.938, 0.939, 0.94, 0.941, 0.942, 0.943, 0.944],
    "power2": [0.936, 0.937, 0.938, 0.939, 0.94, 0.941, 0.942, 0.943, 0.944],
    "buyingBollinger": [1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9],
    "sellingBollinger1": [0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08],
    "sellingBollinger2": [0.996, 0.997, 0.998, 0.999, 1, 1.01, 1.02, 1.03, 1.04]
}

for cc in range(len(coinCodes)):

    stop_event = threading.Event()
    thread = threading.Thread(target=spinner, args=(stop_event,), daemon=True)
    thread.start()
    start_time = time.time()

    best_params = {}
    best_yield = 0

    for power1 in INSTANCES["power1"]:
        for power2 in INSTANCES["power2"]:
            for buyingBollinger in INSTANCES["buyingBollinger"]:
                for sellingBollinger1 in INSTANCES["sellingBollinger1"]:
                    for sellingBollinger2 in INSTANCES["sellingBollinger2"]:
                        execution_time = time.time()
                        s.modifyParams(power1, power2, buyingBollinger, sellingBollinger1, sellingBollinger2)
                        s.candles = data[cc][0:LAUNCH_SAMPLE_SIZE]
                        s.createLists()
                        s.candles = s.candles[-2001:]

                        wallet = 1
                        nbTrades = 0
                        is_open_since = 0

                        for i in range(LAUNCH_SAMPLE_SIZE, CANDLES_IN_PERIOD + LAUNCH_SAMPLE_SIZE):
                            s.candles = s.candles[1:]
                            s.candles.append(data[cc][i])
                            s.updateLists()
                            if is_open_since:
                                if s.sellingEvaluation(is_open_since, STRATEGY_NAME):
                                    wallet += wallet * PERCENTAGE_TRADED * (s.candles[-1]["price"] - data[cc][-is_open_since]["price"]) / (data[cc][-is_open_since]["price"] - 0.0008)
                                    is_open_since = 0
                                else:
                                    is_open_since += 1
                            elif s.buyingEvaluation(STRATEGY_NAME):
                                    is_open_since = 1
                        
                        if wallet > best_yield:
                            best_params = {"power1": power1, "power2": power2, "buyingBollinger": buyingBollinger, "sellingBollinger1" : sellingBollinger1, "sellingBollinger2": sellingBollinger2}
                            best_yield = wallet
                        print(time.time() - execution_time)

    stop_event.set()
    thread.join()
    sys.stdout.write("\r" + " " * 4 + "\r")
    sys.stdout.flush()
    print(f"The best params for {coinCodes[cc]} are:\n{str(best_params)}\nyield: {best_yield}\nCalculation time: {time.time() - start_time}")



# OBJECTIF : faire un algorithme de test brut
# on pourra améliorer son efficacité plus tard