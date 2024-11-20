from dataAnalysis import DataAnalysis
from tools import *
import time

class Strategy: 
    def __init__(self, maSize=100, wAvgSize=2000, power1=0.995, power2=0.99, buyingBollinger=1.5, sellingBollinger1 = 0, sellingBollinger2=1) -> None:
        self.dA = DataAnalysis()
        self.sd = []
        self.ma = []
        self.sdWeightedAvg = []
        self.movingAverageSize = maSize
        self.weightedAvgSize = wAvgSize
        self.power1 = power1 
        self.power2 = power2
        self.buyingBollinger = buyingBollinger
        self.sellingBollinger1 = sellingBollinger1
        self.sellingBollinger2 = sellingBollinger2

        self.candles = [] # liste de dict de bougies

    def generateLists(self):
        self.ma.append(self.dA.exponentialMovingAverage(self.candles[-self.movingAverageSize-1:], self.movingAverageSize, self.power1)[0])
        self.sd += self.dA.expoStandardDeviation(self.candles[-self.movingAverageSize-1:], self.ma[-1], self.movingAverageSize, self.power2)
        if len(self.sd) > self.weightedAvgSize:
            self.sdWeightedAvg += self.dA.simpleWeightedAverage(self.sd[-self.weightedAvgSize-1:], self.weightedAvgSize)
        
    def batchBuyingEvaluation(self):
        self.ma = self.dA.exponentialMovingAverage(self.candles, self.movingAverageSize, self.power1)
        self.sd = self.dA.fastExponentialStandardDeviation(self.candles, self.movingAverageSize, self.power1, self.power2)
        self.sdWeightedAvg = self.dA.simpleWeightedAverage(self.sd, self.weightedAvgSize)
        bb = self.dA.bollinger(self.ma, self.sd, self.buyingBollinger)
        
        buyTimes = []
        for i in range(self.weightedAvgSize+self.movingAverageSize, len(self.candles)-2):
            if (self.sd[i-self.movingAverageSize]["price"] > self.sdWeightedAvg[i-self.weightedAvgSize-self.movingAverageSize+1]["price"] 
            and self.sd[i-self.movingAverageSize-1]["price"] < self.sdWeightedAvg[i-self.weightedAvgSize-self.movingAverageSize]["price"] 
            and self.dA.trend(self.candles[i-self.movingAverageSize+1:i+1], 1/2) == 1
            and self.candles[i]["price"] > bb[i-self.movingAverageSize]["price"]
            ):
                buyTimes.append(self.candles[i]["date"])

        return buyTimes
            

    def buyingEvaluation(self):
        bb = self.dA.bollinger(self.ma[-1], self.sd[-1:], self.buyingBollinger)
        
        if (len(self.sdWeightedAvg) > 2 and
            self.sd[-1]["price"] > self.sdWeightedAvg[-1]["price"] and self.sd[-2]["price"] < self.sdWeightedAvg[-2]["price"] 
            and self.dA.trend(self.candles[-self.movingAverageSize:], 1/2) == 1
            and self.candles[-1]["price"] > bb[-1]["price"]
            ):
            return True
        return False

    def sellingEvaluation(self, numberOfIndexBoughtAgo):
        if len(self.sd) < 2 or numberOfIndexBoughtAgo < 0:
            return False
        
        bbBas = self.dA.bollinger(self.ma[-numberOfIndexBoughtAgo-numberOfIndexBoughtAgo:], self.sd[-numberOfIndexBoughtAgo-numberOfIndexBoughtAgo:], self.sellingBollinger1)
        bbHaut = self.dA.bollinger(self.ma[-numberOfIndexBoughtAgo-1:], self.sd[-numberOfIndexBoughtAgo-1:], self.sellingBollinger2)

        wentUnderLowBB = False
        for i in range(1, numberOfIndexBoughtAgo):
            if self.candles[-i]["price"] < bbBas[-i]["price"]:
                wentUnderLowBB = True 
        
        if (self.sd[-2]["price"] > self.sdWeightedAvg[-2]["price"]
            and self.sd[-1]["price"] < self.sdWeightedAvg[-1]["price"]
            or 
            wentUnderLowBB
            and self.candles[-1]["price"] > bbHaut[-1]["price"]):

            return True
        
        else :
            return False



    def batchSellingEvaluation(self, tradeList):
        numberOfTrades = len(tradeList)
        sellRes = []
        numberOfPositive = 0
        profit = 1

        bb = self.dA.bollinger(self.ma, self.sd, self.sellingBollinger1)
        bb2 = self.dA.bollinger(self.ma, self.sd, self.sellingBollinger2)

        for i in range(numberOfTrades):
            hasPassedUnder0 = False
            for j in range(tradeList[0]["index"]-self.candles[0]["index"], len(self.candles)):
                # print(self.candles[j], self.sd[j], self.sdWeightedAvg[j-self.weightedAvgSize])
                if j == len(self.candles)-1:
                    sellIndex = j
                    break
                if (self.candles[j]["date"] > tradeList[0]["date"] and
                    self.candles[j]["price"] < bb[j]["price"]):
                    hasPassedUnder0 = True
                if (j-self.weightedAvgSize > 0 and
                    self.candles[j]["date"] > tradeList[0]["date"] and
                    self.sd[j]["price"] < self.sdWeightedAvg[j-self.weightedAvgSize]["price"]
                    and self.sd[j-1]["price"] > self.sdWeightedAvg[j-self.weightedAvgSize-1]["price"]):

                    # print(self.sd[j], self.sdWeightedAvg[j-self.weightedAvgSize], "- normal")
                    sellIndex = j
                    break
                

                if (hasPassedUnder0 and
                    self.candles[j]["date"] > tradeList[0]["date"] and
                    self.candles[j]["price"] > bb2[j]["price"]
                    ):

                    # print("- SL")
                    sellIndex = j
                    break
            

            sellRes.append([tradeList[0]['date'], self.candles[sellIndex]['date'], tradeList[0]['price'], self.candles[sellIndex]['price']])
            increase = self.candles[sellIndex]["price"] / tradeList[0]["price"] -1

            profit += profit/2 * (increase - 0.0012)

            if increase > 0:
                numberOfPositive += 1
            tradeList.pop(0)
            
        if numberOfTrades == 0:
            return (sellRes, profit, 0, 0)
        return (sellRes, profit, numberOfPositive/numberOfTrades, numberOfTrades)  
    
    def clean(self):
        if len(self.ma) > 5000:
            self.ma = self.ma[-5000:]
        
        if len(self.sd) > 5000:
            self.sd = self.sd[-5000:]
        
        if len(self.sdWeightedAvg)>5000:
            self.sdWeightedAvg = self.sdWeightedAvg[-5000:]
