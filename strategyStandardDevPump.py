from dataAnalysis import DataAnalysis
from tools import Tools

class Strategy: 
    def __init__(self) -> None:
        self.dA = DataAnalysis()
        self.t = Tools()
        self.sd=[]
        self.sdWeightedAvg = []
        self.movingAverageSize = 100
        self.weightedAvgSize = 2000

    def buyingEvaluation(self, data, time):
        ma = self.dA.exponentialMovingAverage(data[-self.movingAverageSize-1:], self.movingAverageSize, 0.95)
        self.sd += self.dA.expoStandardDeviation(data[-self.movingAverageSize-1:], ma, self.movingAverageSize, 0.95)

        bb3 = self.dA.bollinger(ma, self.sd[-1:], 1.5)

        if len(self.sd) > self.weightedAvgSize:
            self.sdWeightedAvg += self.dA.simpleWeightedAverage(self.sd[-self.weightedAvgSize-1:], self.weightedAvgSize)
        
        if (len(self.sdWeightedAvg) > 2 and
            self.sd[-1]["price"] > self.sdWeightedAvg[-1]["price"] and self.sd[-2]["price"] < self.sdWeightedAvg[-2]["price"] 
            and self.dA.trend(data[-self.movingAverageSize:], 1/2) == 1
            and data[-1]["price"] > bb3[-1]["price"]
            ):
            return True
        return False

    def sellingEvaluation(self, data, tradeList):
        numberOfTrades = len(tradeList)
        sellRes = []
        numberOfPositive = 0
        profit = 1

        ma = self.dA.exponentialMovingAverage(data, self.movingAverageSize)
        bb = self.dA.bollinger(ma, self.sd, 0)
        bb2 = self.dA.bollinger(ma, self.sd, 1) 

        for i in range(numberOfTrades):
            hasPassedUnder0 = False
            for j in range(len(data)):
                if (data[j]["date"] > tradeList[0]["date"] and
                    data[j]["price"] < bb[j-self.movingAverageSize]["price"]):
                    hasPassedUnder0 = True
                if (j-self.weightedAvgSize > 0 and
                    data[j]["date"] > tradeList[0]["date"] and
                    self.sd[j]["price"] < self.sdWeightedAvg[j-self.weightedAvgSize]["price"]
                    and self.sd[j-1]["price"] > self.sdWeightedAvg[j-self.weightedAvgSize-1]["price"]
                    
                    or 

                    hasPassedUnder0 and
                    data[j]["date"] > tradeList[0]["date"] and
                    data[j]["price"] > bb2[j-self.movingAverageSize]["price"]
                    ):

                    sellIndex = j
                    break

            sellRes.append([tradeList[0]['date'], data[sellIndex]['date'], tradeList[0]['price'], data[sellIndex]['price']])
            increase = data[sellIndex]["price"] / tradeList[0]["price"] -1

            profit += profit/2 * (increase - 0.0008)

            if increase > 0:
                numberOfPositive += 1
            tradeList.pop(0)
            
        
        return (sellRes, profit, numberOfPositive/numberOfTrades, numberOfTrades)  
