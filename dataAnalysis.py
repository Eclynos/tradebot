import numpy
import matplotlib.pyplot as plt

class DataAnalysis:
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

        minX = int(dataList[0]["date"])
        
        A = []
        for _ in range(degree +1):
            A.append([0 for __ in range(degree+1)])
        
        B = [0 for _ in range(degree +1)]

        for i in range(numberOfEntries):
            for l in range(degree + 1):
                for c in range(l, degree + 1):
                    A[l][c] += (int(dataList[i]["date"])-minX)**(2 * degree - l - c)
        
        for l in range(degree + 1):
            for c in range(l):
                A[l][c] = A[c][l]

        for i in range(degree + 1):
            for j in range(degree + 1):
                A[i][j] = float(A[i][j])

        for i in range(numberOfEntries):
            for l in range(degree+1):
                B[l] += (int(dataList[i]["date"]) - minX)**(degree - l) * float(dataList[i]["price"])

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
    
    def allGoldenCrosses(self, data, shortMATime, longMATime, noCrossTime):
        n = len(data)
        if(n <= longMATime + noCrossTime):
            print("longueur de data trop petite")
            return []
        
        longMA = self.movingAverage(data, longMATime)
        shortMA = self.movingAverage(data, shortMATime)
        l = []

        for i in range(noCrossTime+longMATime, n):
            hasCrossedBefore = False
            for j in range(i-noCrossTime, i):
                if shortMA[n-(j+1)] >= longMA[n-(j+1)]:
                    hasCrossedBefore = True
                    break

            if not hasCrossedBefore and shortMA[n-(i+1)] > longMA[n-(i+1)]:
                l.append({"date" : data[i]["date"], "force" : (shortMA[n-(i+1)]/longMA[n-(i+1)]) / (shortMA[n-i]/longMA[n-i]), "index":i})
        
        return l
    
    def allDeathCrosses(self, data, shortMATime, longMATime, noCrossTime):
        n = len(data)
        if(n <= longMATime + noCrossTime):
            print("longueur de data trop petite")
            return []
        
        longMA = self.movingAverage(data, longMATime)
        shortMA = self.movingAverage(data, shortMATime)
        l = []

        for i in range(noCrossTime+longMATime, n):
            hasCrossedBefore = False
            for j in range(i-noCrossTime, i):
                if shortMA[n-(j+1)] <= longMA[n-(j+1)]:
                    hasCrossedBefore = True
                    break

            if not hasCrossedBefore and shortMA[n-(i+1)] < longMA[n-(i+1)]:
                l.append({"date" : data[i]["date"], "force" : (shortMA[n-(i+1)]/longMA[n-(i+1)]) / (shortMA[n-i]/longMA[n-i]), "index":i})
        
        return l
    
    def savePlot(self, data, coinCode, trades):
        plt.figure(figsize=(500,100), dpi=80)
        plt.xticks(range(data[0]["date"], data[-1]["date"], 30000))
        plt.yticks([0.001*i for i in range(1000)])
        plt.plot([data[i]["date"] for i in range(len(data))], [data[i]["price"] for i in range(len(data))])
        plt.scatter([trades[0][i][0] for i in range(len(trades[0]))], [trades[0][i][2] for i in range(len(trades[0]))],  color="black", s=1000, marker="x")
        plt.scatter([trades[0][i][1] for i in range(len(trades[0]))], [trades[0][i][3] for i in range(len(trades[0]))],  color="black", s=1000, marker="x")
        for i in range(len(trades[0])):
            plt.plot([trades[0][i][0], trades[0][i][1]], [trades[0][i][2], trades[0][i][3]], color=("green" if trades[0][i][2] < trades[0][i][3] else "red"), lw=3)
        plt.grid()
        plt.savefig(f"{coinCode}.jpg")

