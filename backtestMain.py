from strategyBollinger import *
from dataAnalysis import *
from tools import *
import copy
import time


if __name__ == "__main__":
    s = Strategy()
    da = DataAnalysis()
    t = Tools()
    coinCode = "ETH"

    allData = t.readFile(coinCode) # Il faut avoir téléchargé le fichier avec Backtest-Tools-V2 au préalable et le placer dans ./data/

    usableData = []
    for i in range(len(allData)):
        usableData.append({"date": int(allData[i]["date"])//1000, "price": float(allData[i]["close"]), "index" :i})

    tradeList = []
    startIndex = 60 * len(usableData) // 100
    endIndex = 62 * len(usableData) // 100
    bigma = da.exponentialMovingAverage(usableData[startIndex-1000:endIndex+1], 1000, 0.99)
    for i in range(startIndex, endIndex):
        if (s.buyingEvaluation(usableData[i-110:i+1], usableData[i]["date"]) 
            and (len(tradeList) == 0 or usableData[i]["date"] > tradeList[-1]["date"] + t.time_frame_to_s("30m"))):
            tradeList.append(usableData[i])
        
        if i%1000 == 0:
            print("buying progress :", 100*i/len(usableData), "%")


    print(tradeList)

    sell = s.sellingEvaluation(usableData, tradeList)
    print("\n")
    print("profit % :", 100*sell[1], "\t % of positive trades", 100*sell[2], "\t number of trades :", sell[3], "\t % w/ fees deducted :", 100*(sell[1]-0.001*sell[3]))
    totalTradeTime = usableData[endIndex-1]["date"] - usableData[startIndex]["date"]
    print(totalTradeTime, "sec. =", totalTradeTime / 60, "min. =", totalTradeTime / 3600, "h. =", totalTradeTime / 86400, "jours =", totalTradeTime / 604800, "sem. =", totalTradeTime / (365.25 * 86400), "ans")


    ma = da.exponentialMovingAverage(usableData[startIndex:endIndex], 100)
    sd = da.standardDeviation(usableData[startIndex:endIndex], ma, 100)
    bbm2 = da.bollinger(ma, sd, -2)
    bb2 = da.bollinger(ma, sd, 2)

    da.visualisation(coinCode, usableData[startIndex: endIndex], "curve", 
                               bbm2, "curve", 
                               bb2, "curve",
                               bigma, "curve",
                               sell[0], "buy-sell")