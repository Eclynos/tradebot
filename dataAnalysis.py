import numpy
import matplotlib.pyplot as plt
import copy

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


    def average(self, data):
        total = 0
        numberOfEntries = len(data)
        for i in range(numberOfEntries):
            total += float(data[i]["price"])
        
        return total/numberOfEntries


    def nthDegreeRegression(self, data, degree):
        # Extrapolation des calculcs matriciels trouvés ici :
        # https://www.varsitytutors.com/hotmath/hotmath_help/topics/quadratic-regression

        numberOfEntries = len(data)

        minX = int(data[0]["date"])
        
        A = []
        for _ in range(degree +1):
            A.append([0 for __ in range(degree+1)])
        
        B = [0 for _ in range(degree +1)]

        for i in range(numberOfEntries):
            for l in range(degree + 1):
                for c in range(l, degree + 1):
                    A[l][c] += (int(data[i]["date"])-minX)**(2 * degree - l - c)
        
        for l in range(degree + 1):
            for c in range(l):
                A[l][c] = A[c][l]

        for i in range(degree + 1):
            for j in range(degree + 1):
                A[i][j] = float(A[i][j])

        for i in range(numberOfEntries):
            for l in range(degree+1):
                B[l] += (int(data[i]["date"]) - minX)**(degree - l) * float(data[i]["price"])

        X = numpy.linalg.solve(A,B)
        return X

    def simpleMovingAverage(self, data, MAsize):
        ma = []
        avgPrice = 0
        for i in range(len(data)):
            if i >= MAsize:
                ma.append({"date" : data[i]["date"], "price" : avgPrice/MAsize})
                avgPrice -= data[i-MAsize]["price"]
            avgPrice += data[i]["price"]
        return ma
    
    def exponentialMovingAverage(self, data, MAsize, powerMultiplier=0.95):
        ma = []
        normalisationFactor = 0
        for i in range(MAsize):
            normalisationFactor += powerMultiplier**i 

        avgPrice = 0
        for i in range(len(data)):
            if i >= MAsize:
                ma.append({"date" : data[i]["date"], "price" : avgPrice/normalisationFactor})
                avgPrice -= powerMultiplier**(MAsize-1) * data[i-MAsize]["price"]
            avgPrice *= powerMultiplier
            avgPrice += data[i]["price"]
        return ma

    
    def standardDeviation(self, data, MA, popSize):
        sd = copy.deepcopy(MA)
        for i in range(len(MA)):
            seum = 0
            for j in range(popSize):
                seum += (data[i+j]["price"] - MA[i]["price"])**2
            
            sd[i]["price"] = (seum / (popSize-1))**0.5
        
        return sd
    
    def trend(self, data):
        """renvoie :\n
            1 -> trend haussière\n
            -1 -> trend baissière\n
            0 -> trend sideways
        """
        milieu = len(data)//2
        hh1 = self.maxPrice(data[milieu:])
        hh2 = self.maxPrice(data[:milieu])
        ll1 = self.minPrice(data[milieu:])
        ll2 = self.minPrice(data[:milieu])

        if hh2 > hh1 and ll2 > ll1:
            return 1
        elif hh2 < hh1 and ll2 < ll1:
            return -1
        else:
            return 0

    def allGoldenCrosses(self, data, shortMATime, longMATime, noCrossTime):
        n = len(data)
        if(n <= longMATime + noCrossTime):
            print("longueur de data trop petite")
            return []
        
        longMA = self.simpleMovingAverage(data, longMATime)
        shortMA = self.simpleMovingAverage(data, shortMATime)
        l = []

        for i in range(noCrossTime+longMATime, n):
            hasCrossedBefore = False
            for j in range(i-noCrossTime, i):
                if shortMA[n-(j+1)]["price"] >= longMA[n-(j+1)]["price"]:
                    hasCrossedBefore = True
                    break

            if not hasCrossedBefore and shortMA[n-(i+1)]["price"] > longMA[n-(i+1)]["price"]:
                l.append({"date" : data[i]["date"], "force" : (shortMA[n-(i+1)]["price"]/longMA[n-(i+1)]["price"]) / (shortMA[n-i]["price"]/longMA[n-i]["price"]), "index":i})
        
        return l
    
    def allDeathCrosses(self, data, shortMATime, longMATime, noCrossTime):
        n = len(data)
        if(n <= longMATime + noCrossTime):
            print("longueur de data trop petite")
            return []
        
        longMA = self.simpleMovingAverage(data, longMATime)
        shortMA = self.simpleMovingAverage(data, shortMATime)
        l = []

        for i in range(noCrossTime+longMATime, n):
            hasCrossedBefore = False
            for j in range(i-noCrossTime, i):
                if shortMA[n-(j+1)]["price"] <= longMA[n-(j+1)]["price"]:
                    hasCrossedBefore = True
                    break

            if not hasCrossedBefore and shortMA[n-(i+1)]["price"] < longMA[n-(i+1)]["price"]:
                l.append({"date" : data[i]["date"], "force" : (shortMA[n-(i+1)]["price"]/longMA[n-(i+1)]["price"]) / (shortMA[n-i]["price"]/longMA[n-i]["price"]), "index":i})
        
        return l
    
    def maxPrice(self, data):
        maximum = 0
        for d in data:
            if d["price"] > maximum:
                maximum = d["price"]
        return maximum
    
    def minPrice(self, data):
        minimum = data[0]["price"]
        for d in data:
            if d["price"] < minimum:
                minimum = d["price"]
        return minimum
    
    def bollinger(self, ma, sd, standardDevFactor):
        return [{"date" : ma[i]["date"], "price" : ma[i]["price"] + standardDevFactor * sd[i]["price"]} for i in range(len(ma))]

    def visualisation(self, coinCode, *args):
        plt.figure(figsize=(500,100), dpi=80)
        plt.xticks(range(args[0][0]["date"], args[0][-1]["date"], (args[0][-1]["date"] - args[0][0]["date"]) // 500))
        # plt.yticks(range(self.minPrice(args[0]), self.maxPrice(args[0]), int(self.maxPrice(args[0]) - self.minPrice(args[0])) // 100))
        for i in range(0, len(args), 2):
            if args[i+1] == "curve":
                plt.plot([args[i][j]["date"] for j in range(len(args[i]))], [args[i][j]["price"] for j in range(len(args[i]))])
            elif args[i+1] == "buy-sell":
                plt.scatter([args[i][j][0] for j in range(len(args[i]))], [args[i][j][2] for j in range(len(args[i]))],  color="black", s=1000, marker="x")
                plt.scatter([args[i][j][1] for j in range(len(args[i]))], [args[i][j][3] for j in range(len(args[i]))],  color="black", s=1000, marker="x")
                for j in range(len(args[i])):
                    plt.plot([args[i][j][0], args[i][j][1]], [args[i][j][2], args[i][j][3]], color=("green" if args[i][j][2] < args[i][j][3] else "red"), lw=3)
        plt.grid()
        plt.savefig(f"backtest-images/{coinCode}.jpg")
            



