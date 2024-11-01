from dataAnalysis import DataAnalysis
from tools import *

class Strategy:
    def __init__(self) -> None:
        self.dA = DataAnalysis()

    def buyingEvaluation(self, data, time):
        longMATime = 20    #Nombre de bougies du MA
        shortMATime = 5
        noCrossTime = 2
        maxLatestGCTimeAgo = "30m"

        GCList = self.dA.allGoldenCrosses(data, shortMATime, longMATime, noCrossTime)
        if len(GCList) == 0:
            return False
        lastestGC = GCList[-1]

        if time-lastestGC["date"] > time_frame_to_s(maxLatestGCTimeAgo):
            return False
        if lastestGC["force"] < 1.000:
            return False
        

        i=lastestGC["index"]
        minPrice = data[lastestGC["index"]]["price"]
        secdiff = 4*time_frame_to_s(maxLatestGCTimeAgo)
        
        while lastestGC["date"]-data[i]["date"] < secdiff:
            if minPrice>data[i]["price"]:
                minPrice=data[i]["price"]
            i-=1
        
        
        if data[-1]["price"] < 0.1*minPrice + 0.9*data[lastestGC["index"]]["price"] and self.dA.nthDegreeRegression(data, 1)[0] > 0:
            return True
        
        return False
        
    
    def sellingEvaluation(self, data, tradeList):
        latestdropIndex = 0
        deathCrossList = self.dA.allDeathCrosses(data, 5, 20, 2)
        print(deathCrossList[-1], tradeList[-1], data[-1])
        profit = 0
        numberOfTrades = len(tradeList)
        numberOfPositive = 0
        eurosPerTrade = 1
        sellRes = []
        for i in range(numberOfTrades):

            for j in range(latestdropIndex, len(deathCrossList)):
                if deathCrossList[j]["date"] > tradeList[0]["date"] and data[deathCrossList[j]["index"]]["price"] > tradeList[0]["price"]:
                    buyCandidate = deathCrossList[j]["index"]
                    latestdropIndex = j
                
                    break
            

            if j == len(deathCrossList):
                buyCandidate = len(data) -1

            if data[buyCandidate]["date"] - tradeList[0]["date"] > 806400:
                buyCandidate = min(tradeList[0]["index"] + 806400 // 300, len(data)-1)

            sellRes.append([tradeList[0]['date'], data[buyCandidate]['date'], tradeList[0]['price'], data[buyCandidate]['price']])
            # print(f"DC : {tradeList[0]['date']}->{data[buyCandidate]['date']} | {tradeList[0]['price']}->{data[buyCandidate]['price']}")
            increase = data[buyCandidate]["price"] / tradeList[0]["price"] -1

            profit += eurosPerTrade * increase

            if increase > 0:
                numberOfPositive += 1
            tradeList.pop(0) # si on a pas trouvé de death cross
            
        
        return (sellRes, profit, numberOfPositive/numberOfTrades, numberOfTrades)  

            
    
