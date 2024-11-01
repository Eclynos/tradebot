from strategyStandardDevPump import *
from dataAnalysis import *
from tools import *
import time

if __name__ == "__main__":
    coinCodes = ["ATOM", "BTC", "DOGE", "DOT", "DYM", "ETH", "LINK", "LTC", "SOL"]
    allData = []

    for coinCode in coinCodes:
        allData.append(readFile(coinCode))

    usableData = []
    for j in range(len(coinCodes)):
        usableData.append([])
        for i in range(len(allData[j])):
            usableData[j].append({"date": int(allData[j][i]["date"])//1000, "price": float(allData[j][i]["close"]), "index" :i})
    
    da = DataAnalysis()
    currentDate = int(time.time())
    startIndex = [[binarySearch(usableData[j], currentDate-time_frame_to_s("36M"), "date"),
                   binarySearch(usableData[j], currentDate-time_frame_to_s("33M"), "date"),
                   binarySearch(usableData[j], currentDate-time_frame_to_s("30M"), "date"),
                   binarySearch(usableData[j], currentDate-time_frame_to_s("27M"), "date")]
                   for j in range(len(coinCodes))]
    endIndex = [[binarySearch(usableData[j], currentDate-time_frame_to_s("33M"), "date"),
                 binarySearch(usableData[j], currentDate-time_frame_to_s("30M"), "date"),
                 binarySearch(usableData[j], currentDate-time_frame_to_s("27M"), "date"),
                 binarySearch(usableData[j], currentDate-time_frame_to_s("24M"), "date")]
                 for j in range(len(coinCodes))]
    
    
    resultList = []
    for i in range(100, 101, 10):
        for j in range(2000, 2001, 100):
            startTime = time.time()
            resultList.append([(i, j), 0])
            s = Strategy(i, j, 0.995, 0.99, 1.5)
            for index in range(4):
                for cc in range(len(coinCodes)):
                    if startIndex[cc][index] > i+j:
                    
                        tradeTimeList = s.batchBuyingEvaluation(usableData[cc][startIndex[cc][index]-i:endIndex[cc][index]])
                        tradeList = [usableData[cc][binarySearch(usableData[cc], tradeTimeList[k], "date")] for k in range(len(tradeTimeList))]
                        
                        sell = s.sellingEvaluation(usableData[cc][startIndex[cc][index]: endIndex[cc][index]], tradeList)
                        
                        resultList[-1][1] += sell[1]-1
                
            print(resultList[-1], time.time()-startTime, "s")
    
    print(resultList)
    exit(0)

    # s = Strategy(100, 2000, 0.9, 0.98, 1.5)

    cc=0
    index = 0
    som=0
    for cc in range(len(coinCodes)):
        for index in range(len(startIndex[0])):
            if startIndex[cc][index] > 2100:
                s = Strategy(100, 2000, 0.995, 0.99, 1.5)
                tradeList = []
                for i in range(startIndex[cc][index], endIndex[cc][index]-1):
                    if (s.buyingEvaluation(usableData[cc][i-2000:i+1], usableData[cc][i]["date"]) 
                        and (len(tradeList) == 0 or usableData[cc][i]["date"] > tradeList[-1]["date"] + t.time_frame_to_s("0m"))):
                        tradeList.append(usableData[cc][i])
                    
                    if i%10000 == 0:
                        print("buying progress :", 100*(i-startIndex[cc][index])/(endIndex[cc][index]-startIndex[cc][index]), "%")
              
                sell = s.sellingEvaluation(usableData[cc][startIndex[cc][index]: endIndex[cc][index]], tradeList)

                print()
                print("profit w fees deducted :", 100*(sell[1]-1), "%\t % of positive trades", 100*sell[2], "\t number of trades :", sell[3])
                totalTradeTime = usableData[cc][endIndex[cc][index]-1]["date"] - usableData[cc][startIndex[cc][index]]["date"]
                print(totalTradeTime, "sec. =", totalTradeTime / 60, "min. =", totalTradeTime / 3600, "h. =", totalTradeTime / 86400, "jours =", totalTradeTime / 604800, "sem. =", totalTradeTime / (365.25 * 86400), "ans")
                print("starting price :", usableData[cc][startIndex[cc][index]]["price"], "\t finish price :", usableData[cc][endIndex[cc][index]-1]["price"], "\t diff :", 100*(usableData[cc][endIndex[cc][index]-1]["price"]-usableData[cc][startIndex[cc][index]]["price"])/(usableData[cc][startIndex[cc][index]]["price"]), "%")
                som+=100*(sell[1]-1)
    
    print(som)
    exit(0)
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
    

    # tradeList = []
    # for i in range(startIndex, endIndex-1):
    #     if (s.buyingEvaluation(usableData[i-2000:i+1], usableData[i]["date"]) 
    #         and (len(tradeList) == 0 or usableData[i]["date"] > tradeList[-1]["date"] + t.time_frame_to_s("0m"))):
    #         tradeList.append(usableData[i])
        
    #     if i%10000 == 0:
    #         print("buying progress :", 100*(i-startIndex)/(endIndex-startIndex), "%")