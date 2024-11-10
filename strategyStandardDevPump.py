from dataAnalysis import DataAnalysis
from tools import *
import time

class Strategy: 
    def __init__(self, maSize=100, wAvgSize=2000, power1=0.995, power2=0.99, buyingBollinger=1.5) -> None:
        self.dA = DataAnalysis()
        self.sd=[]
        self.ma = []
        self.sdWeightedAvg = []
        self.movingAverageSize = maSize
        self.weightedAvgSize = wAvgSize
        self.power1 = power1 
        self.power2 = power2
        self.buyingBollinger=buyingBollinger

    def batchBuyingEvaluation(self, data):
        self.ma = self.dA.exponentialMovingAverage(data, self.movingAverageSize, self.power1)
        self.sd = self.dA.fastExponentialStandardDeviation(data, self.movingAverageSize, self.power1, self.power2)
        self.sdWeightedAvg = self.dA.simpleWeightedAverage(self.sd, self.weightedAvgSize)
        bb = self.dA.bollinger(self.ma, self.sd, self.buyingBollinger)
        
        buyTimes = []
        for i in range(self.weightedAvgSize+self.movingAverageSize, len(data)-2):
            if (self.sd[i-self.movingAverageSize]["price"] > self.sdWeightedAvg[i-self.weightedAvgSize-self.movingAverageSize+1]["price"] 
            and self.sd[i-self.movingAverageSize-1]["price"] < self.sdWeightedAvg[i-self.weightedAvgSize-self.movingAverageSize]["price"] 
            and self.dA.trend(data[i-self.movingAverageSize+1:i+1], 1/2) == 1
            and data[i]["price"] > bb[i-self.movingAverageSize]["price"]
            ):
                buyTimes.append(data[i]["date"])

        return buyTimes
            

    def buyingEvaluation(self, data):
        ma = self.dA.exponentialMovingAverage(data[-self.movingAverageSize-1:], self.movingAverageSize, self.power1)
        self.ma.append(ma[0])
        self.sd += self.dA.expoStandardDeviation(data[-self.movingAverageSize-1:], ma, self.movingAverageSize, self.power2)
        

        bb3 = self.dA.bollinger(ma, self.sd[-1:], self.buyingBollinger)

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

        bb = self.dA.bollinger(self.ma[self.movingAverageSize:], self.sd, 0)
        bb2 = self.dA.bollinger(self.ma[self.movingAverageSize:], self.sd, 1)

        for i in range(numberOfTrades):
            hasPassedUnder0 = False
            for j in range(tradeList[0]["index"]-data[0]["index"], len(data)):
                if j == len(data)-1:
                    sellIndex = j
                    break
                if (data[j]["date"] > tradeList[0]["date"] and
                    data[j]["price"] < bb[j-self.movingAverageSize+1]["price"]):
                    hasPassedUnder0 = True
                if (j-self.weightedAvgSize > 0 and
                    data[j]["date"] > tradeList[0]["date"] and
                    self.sd[j-self.movingAverageSize+1]["price"] < self.sdWeightedAvg[j-self.movingAverageSize-self.weightedAvgSize+2]["price"]
                    and self.sd[j-self.movingAverageSize]["price"] > self.sdWeightedAvg[j-self.movingAverageSize-self.weightedAvgSize+1]["price"]
                    
                    or 

                    hasPassedUnder0 and
                    data[j]["date"] > tradeList[0]["date"] and
                    data[j]["price"] > bb2[j-self.movingAverageSize+1]["price"]
                    ):

                    sellIndex = j
                    break
            

            sellRes.append([tradeList[0]['date'], data[sellIndex]['date'], tradeList[0]['price'], data[sellIndex]['price']])
            increase = data[sellIndex]["price"] / tradeList[0]["price"] -1

            profit += profit/2 * (increase - 0.0008)

            if increase > 0:
                numberOfPositive += 1
            tradeList.pop(0)
            
        if numberOfTrades == 0:
            return (sellRes, profit, 0, 0)
        return (sellRes, profit, numberOfPositive/numberOfTrades, numberOfTrades)  
