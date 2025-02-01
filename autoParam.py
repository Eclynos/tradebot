from strategyStandardDevPump import *
from dataAnalysis import *
from tools import *
import time

SAMPLE_SIZE = 2000
LAUNCH_SAMPLE_SIZE = 2104

coinCodes = [
    "SOL"
]

data = [readFile(coinCode, "bitget") for coinCode in coinCodes]

currentDate = time.time() * 1000
SEindex = [getDataIndex(currentDate, "18M", "6M", coinData) for coinData in data]

data = [data[i][SEindex[i][0]-LAUNCH_SAMPLE_SIZE:SEindex[i][1]] for i in range(len(coinCodes))]
data = [[{"date": int(data[i][j]["date"]) // 1000, "price": float(data[i][j]["close"]), "index" :j} for j in range(len(data[i]))] for i in range(len(coinCodes))]


NB_INSTANCES_PARAMS = 100
STRATEGY_NAME = "dip"
PERCENTAGE_TRADED = 0.5
CANDLES_IN_PERIOD = SEindex[0][1] - SEindex[0][0]

s = Strategy(100, SAMPLE_SIZE, 0.92, 0.92, 1.5, 0, 1, 100)

for cc in range(len(coinCodes)):

    s.modifyParams("MODIFICATION")
    s.candles = data[cc][SEindex[cc][0]:SEindex[cc][0]+LAUNCH_SAMPLE_SIZE]
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
        else:
            if s.buyingEvaluation():
                is_open_since = 1





# OBJECTIF : faire un algorithme de test brut
# on pourra améliorer son efficacité plus tard

# vérifier les erreurs causées par le 2104, is_open_since -> CHIANT