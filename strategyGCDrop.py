from dataAnalysis import DataAnalysis
from tools import Tools

class Strategy:
    def __init__(self) -> None:
        self.dA = DataAnalysis()
        self.t = Tools()

    def buyingEvaluation(self, data, time):
        longMATime = 20    #Nombre de bougies du MA
        shortMATime = 5
        noCrossTime = 50
        maxLatestGCTimeAgo = "30m"

        GCList = self.dA.allGoldenCrosses(data, shortMATime, longMATime, noCrossTime)
        if len(GCList) == 0:
            return False
        lastestGC = GCList[-1]

        if time-lastestGC["date"] > self.t.time_frame_to_s(maxLatestGCTimeAgo):
            return False

        i=lastestGC["index"]
        minPrice = data[lastestGC["index"]]["price"]
        secdiff = 4*self.t.time_frame_to_s(maxLatestGCTimeAgo)
        
        while lastestGC["date"]-data[i]["date"] < secdiff:
            if minPrice>data[i]["price"]:
                minPrice=data[i]["price"]
            i-=1
        
        
        if data[-1]["price"] < 0.8*minPrice + 0.2*data[lastestGC["index"]]["price"]:
            return True
        return False
        
    
    def sellingEvaluation(self, data, tradeList, maxHoldTime):
        latestdropIndex = 0
        deathCrossList = self.dA.allGoldenCrosses(data, 10, 40, 50)
        profit = 0
        numberOfTrades = len(tradeList)
        numberOfPositive = 0
        eurosPerTrade = 1
        for i in range(len(tradeList)):
            for j in range(latestdropIndex, len(deathCrossList)):
                if deathCrossList[j]["date"] > tradeList[0]["date"]:

                    print(tradeList[0]["date"], "->", deathCrossList[j]["date"],  " | ", tradeList[0]["price"], "->", data[deathCrossList[j]["index"]]["price"], sep="")
                    
                    increase = data[deathCrossList[j]["index"]]["price"] / tradeList[0]["price"] - 1
                    profit += eurosPerTrade * increase

                    if increase > 0:
                        numberOfPositive += 1

                    latestdropIndex = j
                    tradeList.pop(0)
                    break
            
            if j == len(deathCrossList):
                tradeList.pop(0) # si on a pas trouvé de death cross
            
        
        return (profit, numberOfPositive/numberOfTrades)  

            
    
