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

data = [data[i][SEindex[i][0]:SEindex[i][1]] for i in range(len(coinCodes))]
data = [[{"date": int(data[i][j]["date"]) // 1000, "price": float(data[i][j]["close"]), "index" :j} for j in range(len(data[i]))] for i in range(len(coinCodes))]

NB_INSTANCES_PER_PARAM = 1
NB_PARAMS = 5
STRATEGY_NAME = "dip"
PERCENTAGE_TRADED = 0.5
CANDLES_IN_PERIOD = SEindex[0][1] - SEindex[0][0]

s = Strategy(100, SAMPLE_SIZE, 0.92, 0.92, 1.5, 0, 1, 100)

INSTANCES = {
    "power1": [0.94],
    "power2": [0.94],
    "buyingBollinger": [1.5],
    "sellingBollinger1": [0],
    "sellingBollinger2": [1]
}

for cc in range(len(coinCodes)):

    best_params = {}
    best_yield = -1000

    start_time = time.time()

    for power1 in INSTANCES["power1"]:
        for power2 in INSTANCES["power2"]:
            for buyingBollinger in INSTANCES["buyingBollinger"]:
                for sellingBollinger1 in INSTANCES["sellingBollinger1"]:
                    for sellingBollinger2 in INSTANCES["sellingBollinger2"]:
                        execution_time = time.time()
                        s.modifyParams(power1, power2, buyingBollinger, sellingBollinger1, sellingBollinger2)

                        s.candles = data[cc]
                        tradeTimeList = s.batchBuyingEvaluation()

                        tradeList = []
                        j = 0
                        for i in range(CANDLES_IN_PERIOD):
                            if data[cc][i]["date"] == tradeTimeList[j]:
                                tradeList.append(data[cc][i])
                                j += 1
                                if j >= len(tradeTimeList):
                                    break

                        s.candles = data[cc][100:]
                        result = s.batchSellingEvaluation(tradeList, PERCENTAGE_TRADED)

                        if result[1] > best_yield:
                            best_params = {"power1": power1, "power2": power2, "buyingBollinger": buyingBollinger, "sellingBollinger1" : sellingBollinger1, "sellingBollinger2": sellingBollinger2}
                            best_yield = result[1]

                        print(len(tradeTimeList))
                        print(time.time() - execution_time)
                    
    print(f"The best params for {coinCodes[cc]} are:\n{str(best_params)}\nyield: {best_yield}\nCalculation time: {time.time() - start_time}")