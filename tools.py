import requests
import json
import time

class Tools:
    def __init__(self, IDDico) -> None:
        self.codeToIDDico = IDDico

    def getCoinData(self, coinCode : str, timeFrame : str) -> list:

        if timeFrame not in ("1D", "7D", "1M", "1Y", "All"):
            print("Invalid Time Frame")
            return {}

        r = requests.get(f'https://api.coinmarketcap.com/data-api/v3/cryptocurrency/detail/chart?id={self.codeToIDDico[coinCode]}&range={timeFrame}')
        try:
            r=r.json()
        except:
            return []
        
        r=r["data"]
        if "points" not in r.keys():
            print(f"ERROR [{coinCode}] :", r)
        r=r["points"]
        l = []
        for k in r.keys():
            l.append({"key" : k, "price" : r[k]["v"][0], "volume" : r[k]["v"][1], "mc" : r[k]["v"][2]})

        l.sort(key= lambda item : int(item["key"])) #normalement pas nécessaire mais on sait jamais

        return l
    
    def getMathLocalMins(self, baseList : list) -> list:
        returnList = []

        for k in range(len(baseList)):
            try:
                if baseList[k]["price"] < baseList[k+1]["price"] and baseList[k]["price"] < baseList[k-1]["price"]:
                    returnList.append({"key": baseList[k]["key"], "price" : baseList[k]["price"]})
            except:
                returnList.append({"key": baseList[k]["key"] , "price" : baseList[k]["price"] })
        return returnList 

    def getRealMins(self, baseList : list, minFrame : int) -> list:
        returnList = []

        for i in range(len(baseList)):
            isMin = True
            for j in range(len(baseList)):
                if abs(int(baseList[i]["key"]) - int(baseList[j]["key"])) < minFrame and baseList[i]["price"] > baseList[j]["price"]:
                    isMin = False
                    break
            
            if isMin:
                returnList.append(baseList[i])
        
        return returnList

    def minDepth(self, baseDict, minFrame):
        totalMins = self.getMathLocalMins(baseDict)
        interestingMins = self.getRealMins(totalMins, minFrame)
        minList = []

        for x in interestingMins:
            dropMax = 0
            for y in totalMins:
                if int(x["key"]) - int(y["key"]) > 0 and int(x["key"]) - int(y["key"]) < minFrame and dropMax < 1-x["price"]/y["price"]:
                    dropMax = 1- x["price"]/y["price"]

            minList.append({"key" : x["key"], "price" : x["price"], "drop" : dropMax})
        return minList
    
    def isInDrop(self, coinCode, timeFrame, minFrame):
        allGoodDrops = self.minDepth(self.getCoinData(coinCode , timeFrame), minFrame) 
        return time.time() - int(allGoodDrops[-1]["key"]) < 1000
        
    def average(self, dataList):
        total = 0
        numberOfEntries = len(dataList)
        for i in range(numberOfEntries):
            total += float(dataList[i]["price"])
        
        return total/numberOfEntries



    def linearTrendLine(self, dataList):
        numberOfEntries = len(dataList)
        # https://math.stackexchange.com/questions/204020/what-is-the-equation-used-to-calculate-a-linear-trendline
        sumOfX = 0
        sumOfXsquared = 0
        sumOfY = 0
        sumOfXY = 0
        for i in range(numberOfEntries):
            sumOfX += int(dataList[i]["key"])
            sumOfXsquared += int(dataList[i]["key"])**2
            sumOfY += float(dataList[i]["price"])
            sumofXY += int(dataList[i]["key"]) * float(dataList[i]["price"])

        slope = (numberOfEntries * sumOfXY - sumOfX*sumOfY) / (numberOfEntries * sumOfXsquared - (sumOfX)**2) 

        offset = (sumOfY - slope * sumOfX) / numberOfEntries

        return (slope, offset)
        


    def isWorthBuying(self, coinCode, minFrame):
        weeklyTotalCoinData = self.getCoinData(coinCode, "7D")
        if len(weeklyTotalCoinData) == 0: # Si ça a buggué
            print(f"BUG (Weekly) {coinCode} \t")
            return (False, 1)
        
        drops = self.minDepth(weeklyTotalCoinData, minFrame)
        lastDrop = drops[-1]
        
        minDropPourcentage = 0.05
        releventTimeFrame=900 
        maxDescentPourcentage=0.02
        maxFreefallPourcentage = 0.04


        if time.time()-int(lastDrop["key"]) > releventTimeFrame: # drop trop vieux
            return (False, 0)
        if lastDrop["drop"] < minDropPourcentage: # drop pas assez important
            return (False, 0)     
               
        dailyTotalCoinData = self.getCoinData(coinCode, "1D")
        if len(dailyTotalCoinData) == 0: # Si ça a buggué
            print(f"BUG (Daily) {coinCode} \t")
            return (False, 1)
        dailyAvgPrice = self.average(dailyTotalCoinData)
        weeklyAvgPrice = self.average(weeklyTotalCoinData)

        if (weeklyAvgPrice - dailyAvgPrice) / weeklyAvgPrice > maxDescentPourcentage: # si la crypto descend trop en général (on peut considérer qu'elle s'effondre)
            return (False, 0)
        
        
        if (float(weeklyTotalCoinData[-2]["price"])-float(weeklyTotalCoinData[-1]["price"])) / float(weeklyTotalCoinData[-2]["price"]) > maxFreefallPourcentage: 
            #si la crypto est en chute libre (en si elle descend à la verticale)
            return (False, 0)
        
        if (float(weeklyTotalCoinData[-3]["price"])-float(weeklyTotalCoinData[-1]["price"])) / float(weeklyTotalCoinData[-3]["price"]) > maxFreefallPourcentage: 
            #même test sur l'index d'avant juste pour être safe
            return (False, 0)
        
        return (True, 0)
    
