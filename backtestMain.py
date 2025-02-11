from strategyStandardDevPump import *
from dataAnalysis import *
from tools import *
import time

if __name__ == "__main__":
    coinCodes = [
        "SOL"
    ]

    allData = []

    for coinCode in coinCodes:
        allData.append(readFile(coinCode, "bitget"))

    usableData = []
    for j in range(len(coinCodes)):
        usableData.append([])
        for i in range(len(allData[j])):
            usableData[j].append({"date": int(allData[j][i]["date"])//1000, "price": float(allData[j][i]["close"]), "index" :i})
    
    da = DataAnalysis()
    currentDate = int(time.time())
    startIndex = [[binarySearch(usableData[j], currentDate-time_frame_to_s("18M"), "date")]
                  for j in range(len(coinCodes))]
    endIndex = [[binarySearch(usableData[j], currentDate-time_frame_to_s("6M"), "date")]
                 for j in range(len(coinCodes))]
        
    

    # resultList = []
    # for i in range(100, 101, 10):
    #     for j in range(2000, 2001, 100):
    #         for k in range(-20, 21, 5):
    #             for l in range(-20, 21, 5):
    #                 startTime = time.time()
    #                 resultList.append([(k/10, l/10), 1])
    #                 s = Strategy(i, j, 0.995, 0.99, 1.5, k/10, l/10)
    #                 for index in range(len(startIndex[0])):
    #                     for cc in range(len(coinCodes)):
    #                         s.candles = usableData[cc]

    #                         if startIndex[cc][index] > i+j:
                            
    #                             tradeTimeList = s.batchBuyingEvaluation()
    #                             tradeList = [usableData[cc][binarySearch(usableData[cc], tradeTimeList[k], "date")] for k in range(len(tradeTimeList))]
                                
    #                             sell = s.batchSellingEvaluation(usableData[cc][startIndex[cc][index]: endIndex[cc][index]], tradeList)
                                
    #                             resultList[-1][1] *= sell[1]
                    
    #                 print(resultList[-1], time.time()-startTime, "s")
    
    # print(resultList)
    # exit(0)

    som=1
    nbOfTrades=0
    for cc in range(len(coinCodes)):
        for index in range(len(startIndex[0])):
            avgHoldTime=0
            solList = []
            wallet = 1
            if startIndex[cc][index] > 2100:
                nbIndexBoughtAgo = -1
                s = Strategy(100, 2000, 0.94, 0.94, 1.5, 0, 1, 100)
                tradeList = []

                s.candles = usableData[cc][startIndex[cc][index]-2104:startIndex[cc][index]+1]
                s.createLists()

                for i in range(startIndex[cc][index], endIndex[cc][index]-1):
                    s.candles = usableData[cc][i-2000:i+1]
                    s.updateLists()

                    if (s.buyingEvaluation("dip") and nbIndexBoughtAgo == -1):
                        tradeList.append(usableData[cc][i])
                        nbIndexBoughtAgo = 0
                        buyType = "dip"
                    # elif (s.buyingEvaluation("pump") and nbIndexBoughtAgo == -1):
                    #     tradeList.append(usableData[cc][i])
                    #     nbIndexBoughtAgo = 0
                    #     buyType = "pump"
                    
                    if nbIndexBoughtAgo != -1 and s.sellingEvaluation(nbIndexBoughtAgo, "pump"):
                        wallet += 0.25*wallet * ((usableData[cc][i]["price"] - tradeList[0]["price"]) / tradeList[0]["price"] - 0.0008)
                        solList.append([tradeList[0]["date"], usableData[cc][i]["date"], usableData[cc][tradeList[0]["index"]]["price"], usableData[cc][i]["price"]])
                        tradeList.pop()
                        nbIndexBoughtAgo = -1

                    if nbIndexBoughtAgo != -1:
                        nbIndexBoughtAgo+=1
        
            for a in range(len(solList)):
                avgHoldTime += (solList[a][1]-solList[a][0])/len(solList)

            print(coinCodes[cc], "| wallet after coin :", wallet, "| avg Hold Time :", avgHoldTime)

            nbOfTrades += len(solList)
            som*=wallet

    print([solList[a][0] for a in range(len(solList))])
    print(som, nbOfTrades)
    exit()
    som=0
    
    # for cc in range(len(coinCodes)):
    #     for index in range(len(startIndex[0])):
    #         if startIndex[cc][index] > 2100:
    #             s = Strategy(100, 2000, 0.995, 0.99, 1.5, 0,  1)
    #             tradeList = []
    #             print(startIndex[cc][index])
    #             for i in range(startIndex[cc][index], endIndex[cc][index]-1):
    #                 if (s.buyingEvaluation(usableData[cc][i-2000:i+1], "dip") 
    #                     and (len(tradeList) == 0 or usableData[cc][i]["date"] > tradeList[-1]["date"] + time_frame_to_s("0m"))):
    #                     tradeList.append(usableData[cc][i])
    #                     # print("bought : ", i)
                    
                    
    #                 if i%10000 == 0:
    #                     print("buying progress :", 100*(i-startIndex[cc][index])/(endIndex[cc][index]-startIndex[cc][index]), "%")

              
    #             sell = s.batchSellingEvaluation(usableData[cc][startIndex[cc][index]: endIndex[cc][index]], tradeList)

    #             som += 100*(sell[1]-1)
    #             print(sell)

    # print(som)


    exit(0)
    mp = da.minPrice(usableData[-1][startIndex[-1][0]:endIndex[-1][0]])
    bb15 = da.bollinger(s.ma, s.sd, 1.5)
    showsd = [{"date":s.sd[i]["date"], "price": mp + s.sd[i]["price"]} for i in range(len(s.sd))]
    showavgsd = [{"date":s.sdWeightedAvg[i]["date"], "price" : mp + s.sdWeightedAvg[i]["price"]} for i in range(len(s.sdWeightedAvg))]

    da.visualisation(coinCode, usableData[-1][startIndex[-1][0]: endIndex[-1][0]], "curve",
                               s.ma, "curve",
                               bb15, "curve",
                               showsd, "curve",
                               showavgsd, "curve",
                               solList, "buy-sell")
    

    # tradeList = []
    # for i in range(startIndex, endIndex-1):
    #     if (s.buyingEvaluation(usableData[i-2000:i+1], usableData[i]["date"]) 
    #         and (len(tradeList) == 0 or usableData[i]["date"] > tradeList[-1]["date"] + t.time_frame_to_s("0m"))):
    #         tradeList.append(usableData[i])
        
    #     if i%10000 == 0:
    #         print("buying progress :", 100*(i-startIndex)/(endIndex-startIndex), "%")

    # print()
                # print("profit w fees deducted :", 100*(sell[1]-1), "%\t % of positive trades", 100*sell[2], "\t number of trades :", sell[3])
                # totalTradeTime = usableData[cc][endIndex[cc][index]-1]["date"] - usableData[cc][startIndex[cc][index]]["date"]
                # print(totalTradeTime, "sec. =", totalTradeTime / 60, "min. =", totalTradeTime / 3600, "h. =", totalTradeTime / 86400, "jours =", totalTradeTime / 604800, "sem. =", totalTradeTime / (365.25 * 86400), "ans")
                # print("starting price :", usableData[cc][startIndex[cc][index]]["price"], "\t finish price :", usableData[cc][endIndex[cc][index]-1]["price"], "\t diff :", 100*(usableData[cc][endIndex[cc][index]-1]["price"]-usableData[cc][startIndex[cc][index]]["price"])/(usableData[cc][startIndex[cc][index]]["price"]), "%")