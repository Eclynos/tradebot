import requests
import csv
import threading
import numpy

class Tools:
    def readFile(self, coinCode) -> list:
        with open(f"./Database/{coinCode}-USDT.csv", 'r') as file_csv:
            allData = csv.DictReader(file_csv)
            allData = list(allData)

        return allData
    
    def fractureData(self, startDate, allData)->list:
        fracturedData = [[]]
        fIndex = -1

        for i in range(len(allData)):
            prevFindex = fIndex
            fIndex = ((int(allData[i]["date"])//1000)-startDate)//86400
            if fIndex > 0:
                for _ in range(fIndex - prevFindex):
                    fracturedData.append([])
                fracturedData[fIndex].append(allData[i])

        return fracturedData    

    def allTradesInTimeFrame(self, fracturedData, startDate, endDate, blockSize, buyingFunction):
        tradesList = []
        affichage = 0
        threadList = []

        for i in range(startDate, endDate + 1, blockSize):
            a = fracturedData[(i-startDate)//86400-1] + fracturedData[(i-startDate)//86400] + fracturedData[(i-startDate)//86400+1]

            dataW = self.getCoinData(a, "7D", i)
            dataD = self.getCoinData(a, "1D", i)

            threadList.append(threading.Thread(target=buyingFunction, args=(dataW, dataD, i, blockSize//2, tradesList)))
            affichage+=1

            if affichage!= 0 and affichage%100 == 0:
                # print(threadList)
                for j in range(100):
                    threadList[j].start()
                        
                threadList = []

                affichage = 0
                print(100 * (i-startDate)/(endDate-startDate), "%")

        return tradesList

    def getCoinData(self, allData, timeFrame : str, currentTime) -> list:

        if timeFrame not in ("1D", "7D", "1M", "1Y", "All"):
            print("Invalid Time Frame")
            return {}

        
        newData = []
        for i in range(len(allData)):
            if(currentTime - int(allData[i]["date"])//1000 > 0 and currentTime - int(allData[i]["date"])//1000 < (604800 if timeFrame == "7D" else 86400)):
                newData.append(allData[i])

        l = []
        for ligne in newData:
            l.append({"key" : int(ligne["date"])//1000, "price" : float(ligne["close"]), "volume" : ligne["volume"]})

        l.sort(key= lambda item : int(item["key"])) #normalement pas nécessaire mais on sait jamais

        return l

    def getMathLocalMins(self, baseList : list) -> list:
        """Determine les minimums locaux de la chart : valeur précédent > valeur actuelle < valeur suivante"""
        returnList = []

        for k in range(len(baseList)):
            try:
                if baseList[k]["price"] < baseList[k+1]["price"] and baseList[k]["price"] < baseList[k-1]["price"]:
                    returnList.append({"key": baseList[k]["key"], "price" : baseList[k]["price"]})
                    k += 1
            except:
                returnList.append({"key": baseList[k]["key"] , "price" : baseList[k]["price"] })
        return returnList

    def getRealMins(self, baseList : list, minFrame : int) -> list:
        """Détermine les retracements à partir de la liste des minimums locaux"""
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
        """Détermine les vrais dip à partir de la liste des retracements"""
        totalMins = self.getMathLocalMins(baseDict)
        interestingMins = self.getRealMins(totalMins, minFrame)
        minList = []

        for x in interestingMins:
            dropMax = 0
            for y in totalMins:
                if int(x["key"]) - int(y["key"]) > 0 and int(x["key"]) - int(y["key"]) < minFrame and dropMax < 1-x["price"]/y["price"]:
                    dropMax = 1 - x["price"] / y["price"]

            minList.append({"key" : x["key"], "price" : x["price"], "drop" : dropMax})
        return minList

    def average(self, dataList):
        total = 0
        numberOfEntries = len(dataList)
        for i in range(numberOfEntries):
            total += float(dataList[i]["price"])

        return total/numberOfEntries

    def nthDegreeRegression(self, dataList, degree):
        # Extrapolation des calculcs matriciels trouvés ici :
        # https://www.varsitytutors.com/hotmath/hotmath_help/topics/quadratic-regression

        numberOfEntries = len(dataList)

        minX = int(dataList[0]["key"])

        A = []
        for _ in range(degree +1):
            A.append([0 for __ in range(degree+1)])

        B = [0 for _ in range(degree +1)]

        for i in range(numberOfEntries):
            for l in range(degree + 1):
                for c in range(l, degree + 1):
                    A[l][c] += (int(dataList[i]["key"])-minX)**(2 * degree - l - c)

        for l in range(degree + 1):
            for c in range(l):
                A[l][c] = A[c][l]

        for i in range(degree + 1):
            for j in range(degree + 1):
                A[i][j] = float(A[i][j])

        for i in range(numberOfEntries):
            for l in range(degree+1):
                B[l] += (int(dataList[i]["key"]) - minX)**(degree - l) * float(dataList[i]["price"])

        X = numpy.linalg.solve(A,B)
        return X


    def isWorthBuying(self, weeklyTotalCoinData, dailyTotalCoinData, currentTime, minFrame, l):
        drops = self.minDepth(weeklyTotalCoinData, minFrame)
        if drops == []: 
            print("empty drops")
            return (False, 1)
        lastDrop = drops[-1]

        minDropPourcentage = 0.05
        releventTimeFrame=900
        maxDescentPourcentage=0.02
        maxFreefallPourcentage = 0.04


        if currentTime-int(lastDrop["key"]) > releventTimeFrame: # drop trop vieux
            return (False, 0)
        if lastDrop["drop"] < minDropPourcentage: # drop pas assez important
            return (False, 0)

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

        l.append({"time": currentTime, "price" : lastDrop["price"]})
        return (True, 0)