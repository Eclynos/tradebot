from strategyGCDrop import *
from dataAnalysis import *
from tools import *
import copy
import time


if __name__ == "__main__":
    s = Strategy()
    da = DataAnalysis()
    t = Tools()
    coinCode = "DOGE"

    allData = t.readFile(coinCode) # Il faut avoir téléchargé le fichier avec Backtest-Tools-V2 au préalable et le placer dans ./data/

    usableData = []
    for i in range(len(allData)):
        usableData.append({"date": int(allData[i]["date"])//1000, "price": float(allData[i]["close"]), "index" :i})

    tradeList = []
    startIndex = 6 * len(usableData) // 10
    endIndex = 7 * len(usableData) // 10
    for i in range(startIndex, endIndex):
        if (s.buyingEvaluation(usableData[i-30:i+1], usableData[i]["date"]) 
            and (len(tradeList) == 0 or usableData[i]["date"] > tradeList[-1]["date"] + t.time_frame_to_s("30m"))):
            tradeList.append(usableData[i])
        
        if i%10000 == 0:
            print("buying progress :", 100*i/len(usableData), "%")


    # sell = s.sellingEvaluation(usableData, tradeList)
    # print("profit % :", 100*sell[1], "\t % of positive trades", 100*sell[2], "\t number of trades :", sell[3])
    # totalTradeTime = usableData[endIndex-1]["date"] - usableData[startIndex]["date"]
    # print(totalTradeTime, "sec. =", totalTradeTime / 60, "min. =", totalTradeTime / 3600, "h. =", totalTradeTime / 86400, "jours =", totalTradeTime / 604800, "sem. =", totalTradeTime / (365.25 * 86400), "ans")

    # da.visualisation(coinCode, usableData[startIndex:endIndex], "curve", sell[0], "buy-sell")

    ma = da.simpleMovingAverage(usableData[startIndex:endIndex], 120)
    sd = da.standardDeviation(usableData[startIndex:endIndex], ma, 120)
    bb1 = [{"date" : ma[i]["date"], "price" : ma[i]["price"] + 2 * sd[i]["price"]} for i in range(len(ma))]
    bb2 = [{"date" : ma[i]["date"], "price" : ma[i]["price"] - 2 * sd[i]["price"]} for i in range(len(ma))]
    minP = da.minPrice(usableData[startIndex:endIndex])
    diff = [{"date" : bb1[i]["date"], "price" : minP*0.99 + bb1[i]["price"]-bb2[i]["price"]} for i in range(len(bb1))]

    da.visualisation(coinCode, usableData[startIndex:endIndex], "curve", bb1, "curve", bb2, "curve", ma, "curve", diff, "curve")

