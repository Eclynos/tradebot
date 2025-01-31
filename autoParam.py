from strategyStandardDevPump import *
from dataAnalysis import *
from tools import *
import time

da = DataAnalysis()

coinCodes = [
    "BTC"
]

allData = [readFile(coinCode) for coinCode in coinCodes]

AreAnyCandlesMissing(allData[0])

#currentDate = time.time() * 1000
#SEindex = [getDataIndex(currentDate, "18M", "6M", coinData) for coinData in allData]