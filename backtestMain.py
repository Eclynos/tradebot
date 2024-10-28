from strategyStandardDevPump import *
from dataAnalysis import *
from tools import *
import copy
import time


if __name__ == "__main__":
    s = Strategy()
    da = DataAnalysis()
    t = Tools()
    coinCode = "BTC"

    allData = t.readFile(coinCode) # Il faut avoir téléchargé le fichier avec Backtest-Tools-V2 au préalable et le placer dans ./data/

    usableData = []
    for i in range(len(allData)):
        usableData.append({"date": int(allData[i]["date"])//1000, "price": float(allData[i]["close"]), "index" :i})

    startTime = time.time()
    currentDate = int(time.time())
    startIndex = t.binarySearch(usableData, currentDate-t.time_frame_to_s("6M"), "date")
    endIndex = t.binarySearch(usableData, currentDate-t.time_frame_to_s("3M"), "date")

    if endIndex == -1:
        endIndex = len(usableData) -1

    if startIndex < 2000:
        print(f"Pas assez de données sur la coin {coinCode} !")
        exit(0)

    tradeList = []
    tradeTimeList = s.batchBuyingEvaluation(usableData[startIndex-100:endIndex])
    ttlIndex = 0
    for i in range(startIndex, endIndex):
        if usableData[i]["date"] == tradeTimeList[ttlIndex]:
            tradeList.append(usableData[i])
            ttlIndex += 1
        if ttlIndex == len(tradeTimeList):
            break
    
    # tradeList = []
    # for i in range(startIndex, endIndex-1):
    #     if (s.buyingEvaluation(usableData[i-2000:i+1], usableData[i]["date"]) 
    #         and (len(tradeList) == 0 or usableData[i]["date"] > tradeList[-1]["date"] + t.time_frame_to_s("0m"))):
    #         tradeList.append(usableData[i])
        
    #     if i%10000 == 0:
    #         print("buying progress :", 100*(i-startIndex)/(endIndex-startIndex), "%")

    print(time.time()-startTime, "s")

    sell = s.sellingEvaluation(usableData[startIndex: endIndex], tradeList)
    print(sell)

    print()
    print("profit w fees deducted :", 100*(sell[1]-1), "%\t % of positive trades", 100*sell[2], "\t number of trades :", sell[3])
    totalTradeTime = usableData[endIndex-1]["date"] - usableData[startIndex]["date"]
    print(totalTradeTime, "sec. =", totalTradeTime / 60, "min. =", totalTradeTime / 3600, "h. =", totalTradeTime / 86400, "jours =", totalTradeTime / 604800, "sem. =", totalTradeTime / (365.25 * 86400), "ans")
    print("starting price :", usableData[startIndex]["price"], "\t finish price :", usableData[endIndex-1]["price"], "\t diff :", 100*(usableData[endIndex-1]["price"]-usableData[startIndex]["price"])/(usableData[startIndex]["price"]), "%")
    
    mp = da.minPrice(usableData[startIndex:endIndex])
    bb15 = da.bollinger(s.ma, s.sd, 1.5)
    showsd = [{"date":s.sd[i]["date"], "price": mp + s.sd[i]["price"]} for i in range(len(s.sd))]
    avgsd = da.simpleWeightedAverage(s.sd, 1000)
    showavgsd = [{"date":avgsd[i]["date"], "price" : mp + avgsd[i]["price"]} for i in range(len(avgsd))]

    da.visualisation(coinCode, usableData[startIndex: endIndex], "curve",
                               s.ma, "curve",
                               bb15, "curve",
                               showsd, "curve",
                               showavgsd, "curve",
                               sell[0], "buy-sell")