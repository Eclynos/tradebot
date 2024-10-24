from strategyStandardDevPump import *
from dataAnalysis import *
from tools import *
import copy
import time


if __name__ == "__main__":
    s = Strategy()
    da = DataAnalysis()
    t = Tools()
    coinCode = "XRP"

    allData = t.readFile(coinCode) # Il faut avoir téléchargé le fichier avec Backtest-Tools-V2 au préalable et le placer dans ./data/

    usableData = []
    for i in range(len(allData)):
        usableData.append({"date": int(allData[i]["date"])//1000, "price": float(allData[i]["close"]), "index" :i})



    tradeList = []
    startIndex = -1
    endIndex = -1
    currentDate = int(time.time())
    for i in range(len(usableData)):
        if startIndex != -1 and endIndex != -1:
            break
        if currentDate - usableData[i]["date"] < t.time_frame_to_s("9M") and endIndex == -1:
            endIndex = i 
        if currentDate - usableData[i]["date"] < t.time_frame_to_s("1y") and startIndex == -1:
            startIndex = i

    if endIndex == -1:
        endIndex = len(usableData) -1

    if startIndex < 2000:
        print(f"Pas assez de données sur la coin {coinCode} !")
        exit(0)

    print("début des fonctions")
    startTime = time.time()
    ma = da.exponentialMovingAverage(usableData[startIndex:endIndex], 100)
    print("ma in :", time.time()-startTime)
    startTime = time.time()
    sd = da.expoStandardDeviation(usableData[startIndex:endIndex], ma, 100)
    print("sd in :", time.time()-startTime)
    startTime = time.time()
    avgsd = da.simpleWeightedAverage(sd, 2000)
    print("avgsd in :", time.time()-startTime)
    exit(0)

    for i in range(startIndex, endIndex-1):
        if (s.buyingEvaluation(usableData[i-2000:i+1], usableData[i]["date"]) 
            and (len(tradeList) == 0 or usableData[i]["date"] > tradeList[-1]["date"] + t.time_frame_to_s("0m"))):
            tradeList.append(usableData[i])
        
        if i%10000 == 0:
            print("buying progress :", 100*(i-startIndex)/(endIndex-startIndex), "%")

    print(len(tradeList))

    sell = s.sellingEvaluation(usableData[startIndex: endIndex], tradeList)

    print("\n")
    print("profit w fees deducted :", 100*(sell[1]-1), "%\t % of positive trades", 100*sell[2], "\t number of trades :", sell[3])
    totalTradeTime = usableData[endIndex-1]["date"] - usableData[startIndex]["date"]
    print(totalTradeTime, "sec. =", totalTradeTime / 60, "min. =", totalTradeTime / 3600, "h. =", totalTradeTime / 86400, "jours =", totalTradeTime / 604800, "sem. =", totalTradeTime / (365.25 * 86400), "ans")
    print("starting price :", usableData[startIndex]["price"], "\t finish price :", usableData[endIndex-1]["price"], "\t diff :", 100*(usableData[endIndex-1]["price"]-usableData[startIndex]["price"])/(usableData[startIndex]["price"]), "%")

    # ma = da.exponentialMovingAverage(usableData[startIndex:endIndex], 100)
    # sd = da.expoStandardDeviation(usableData[startIndex:endIndex], ma, 100)

    # mp = da.minPrice(usableData[startIndex:endIndex])
    # bb15 = da.bollinger(ma, sd, 1.5)
    # showsd = [{"date":sd [i]["date"], "price": mp + sd[i]["price"]} for i in range(len(sd))]
    # avgsd = da.simpleWeightedAverage(sd, 1000)
    # showavgsd = [{"date":avgsd[i]["date"], "price" : mp + avgsd[i]["price"]} for i in range(len(avgsd))]

    # da.visualisation(coinCode, usableData[startIndex: endIndex], "curve",
    #                            ma, "curve",
    #                            bb15, "curve",
    #                            showsd, "curve",
    #                            showavgsd, "curve",
    #                            sell[0], "buy-sell")