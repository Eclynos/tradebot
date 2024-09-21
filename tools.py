import requests
import json
import time

class Tools:
    def __init__(self) -> None:
        self.codeToIDDico = {}

        with open('./codeToID.json','r') as json_File :
            self.codeToIDDico=json.load(json_File)

    def getCoinData(self, coinCode : str, timeFrame : str) -> list:

        if timeFrame not in ("1D", "7D", "1M", "1Y", "All"):
            print("Invalid Time Frame")
            return {}

        r = requests.get(f'https://api.coinmarketcap.com/data-api/v3/cryptocurrency/detail/chart?id={self.codeToIDDico[coinCode]}&range={timeFrame}')
        r=r.json()
        r=r["data"]["points"]
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
            descMin = 1
            for y in totalMins:
                if int(x["key"]) - int(y["key"]) > 0 and int(x["key"]) - int(y["key"]) < minFrame and descMin > x["price"]/y["price"]:
                    descMin = x["price"]/y["price"]

            minList.append({"key" : x["key"], "price" : x["price"], "drop" : descMin})
        return minList
    
    def isInDrop(self, coinCode, timeFrame, minFrame):
        allGoodDrops = self.minDepth(self.getCoinData(coinCode , timeFrame), minFrame) 
        return time.time() - int(allGoodDrops[-1]["key"]) < 1000
        
    def average(self, dataDict):
        total = 0
        numberOfEntries = len(list(dataDict.keys()))
        for k in dataDict.keys():
            total += dataDict[k]["price"]
        
        return total/numberOfEntries

    def isWorthBuying(self, coinCode, minFrame):
        drops = self.minDepth(self.getCoinData(coinCode , "7D"), minFrame)
        lastDrop = drops[-1]
        
        minDropPourcentage = 0.95
        releventTimeFrame=900 


        if time.time()-int(lastDrop["key"]) > releventTimeFrame: # drop trop vieux
            return False
        if lastDrop["drop"] > minDropPourcentage: # drop pas assez important
            return False            
        if 

        print(drops)

        return