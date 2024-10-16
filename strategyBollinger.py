from dataAnalysis import DataAnalysis
from tools import Tools

class Strategy: 
    def __init__(self) -> None:
        self.dA = DataAnalysis()
        self.t = Tools()        
    
    def buyingEvaluation(self, data, time):
        movingAverageSize = 100
        maxLatestGCTimeAgo = "5m"

        ma = self.dA.exponentialMovingAverage(data, movingAverageSize)
        sd = self.dA.standardDeviation(data, ma, movingAverageSize)
        bb = self.dA.bollinger(ma, sd, -2)
        wentUnderBB = False
        for i in range(len(data)-1, movingAverageSize-1, -1):
            if (bb[i-movingAverageSize]["price"] > data[i]["price"] 
                and time - data[i]["date"] < self.t.time_frame_to_s(maxLatestGCTimeAgo)):
                wentUnderBB = True
                break
        
        if wentUnderBB:
            return True

        return False
    
    def sellingEvaluation(self, data, tradeList):
        numberOfTrades = len(tradeList)
        movingAverageSize = 100
        eurosPerTrade = 1
        sellRes = []
        numberOfPositive = 0
        profit = 0
        maxHoldTime = "7d"
        ma = self.dA.exponentialMovingAverage(data, movingAverageSize)
        sd = self.dA.standardDeviation(data, ma, movingAverageSize)
        bb = self.dA.bollinger(ma, sd, 1)

        for i in range(numberOfTrades):
            for j in range(tradeList[0]["index"], tradeList[0]["index"] + self.t.time_frame_to_s(maxHoldTime)//300 + 1):
                if data[j]["date"] > tradeList[0]["date"] and data[j]["price"] > bb[j-movingAverageSize]["price"]:
                    buyCandidate = j
                    break
            
            if j >= len(data) -1:
                buyCandidate = len(data) -1

            if data[buyCandidate]["date"] - tradeList[0]["date"] > 806400:
                print("too long")
                buyCandidate = min(tradeList[0]["index"] + (806400 // 300) - data[0]["index"], len(data)-1)

            sellRes.append([tradeList[0]['date'], data[buyCandidate]['date'], tradeList[0]['price'], data[buyCandidate]['price']])
            increase = data[buyCandidate]["price"] / tradeList[0]["price"] -1

            profit += eurosPerTrade * increase

            if increase > 0:
                numberOfPositive += 1
            tradeList.pop(0)

        return (sellRes, profit, numberOfPositive/numberOfTrades, numberOfTrades)  