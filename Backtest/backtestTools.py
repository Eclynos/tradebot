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
        print(allData[-1]["date"])
        fracturedData = [[]]
        fIndex = -1

        for i in range(len(allData)):
            prevFindex = fIndex
            fIndex = (allData[i]["date"]-startDate)//604800

            if fIndex > 0:
                for _ in range(fIndex - prevFindex):
                    fracturedData.append([])
                fracturedData[fIndex].append(allData[i])

        print(len(fracturedData))
        return fracturedData

    def allTradesInTimeFrame(self, fracturedData, startDate, endDate, blockSize, buyingFunction, startDateOffset):
        """Lance 100 threads de buyingFuction à la fois, met la fonction en situation de startDate à endDate, tous les blockSize secondes"""
        tradesList = []
        affichage = 0
        threadList = []
        data = fracturedData[0] + fracturedData[1] + fracturedData[2]
        previ = 0
        for i in range(startDate+startDateOffset, endDate + 1, blockSize):
            if previ != i:
                data = fracturedData[(i-startDate)//604800-1] + fracturedData[(i-startDate)//604800-0]

            threadList.append(threading.Thread(target=buyingFunction, args=(self, data, i, tradesList)))
            affichage+=1
            previ = i

            if affichage!= 0 and affichage%100 == 0:
                for j in range(100):
                    threadList[j].start()
                
                threadList = []

                affichage = 0
                print("buying progress :", 100 * (i-startDate - startDateOffset)/(endDate-startDate - startDateOffset), "%")


        return tradesList

    def getCoinData(self, allData, timeFrame : str, currentTime) -> list:

        if timeFrame not in ("1D", "7D", "1M", "1Y", "All"):
            print("Invalid Time Frame")
            return {}

        startFlag = -1
        endFlag = -1

        for i in range(len(allData)-1,-1,-1 ):
            if(currentTime - allData[i]["date"] > 0 and endFlag == -1):
                endFlag = i  
                break

        for i in range(endFlag-1, -1, -1):
            if(currentTime - allData[i]["date"] > (604800 if timeFrame == "7D" else 86400) and startFlag == -1):
                startFlag = i
                break

        newData = allData[startFlag:endFlag]
        # print(len(newData))
        l = []
        for ligne in newData:
            l.append({"key" : int(ligne["date"]), "price" : float(ligne["close"]), "volume" : ligne["volume"]})

        # l.sort(key= lambda item : int(item["key"])) #normalement pas nécessaire mais on sait jamais

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
    
    def movingAverage(self, dataList, MAsize):
        numberOfData = len(dataList)
        l = []
        avgPrice = 0
        for i in range(numberOfData):
            if i >= MAsize:
                l.append(avgPrice/MAsize)
                avgPrice -= dataList[numberOfData - 1 - i + MAsize]["price"]
            avgPrice += dataList[numberOfData - 1 - i]["price"]
        
        return l
