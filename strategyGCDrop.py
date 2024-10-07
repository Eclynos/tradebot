from dataAnalysis import DataAnalysis

class Strategy:
    def __init__(self) -> None:
        self.dA = DataAnalysis()

    def buyingEvaluation(self, data):
        longMATime = 20    #Nombre de bougies du MA
        shortMATime = 5
        noCrossZone = 50

        if(len(data) <= longMATime + noCrossZone):
            print("longueur de data trop petite")
            return False
        longMA = self.dA.movingAverage(data, longMATime)
        shortMA = self.dA.movingAverage(data, shortMATime)

        hasCrossedBefore = False
        for i in range(noCrossZone):
            if shortMA[i+1] >= longMA[i+1]:
                hasCrossedBefore = True
                break

        if hasCrossedBefore:
            return False
        # else
        


    def sellingEvaluation(self):
        pass 

    
