from backtestTools import *
import copy



def isWorthBuying(t, data, currentTime, l):
        noCrossDuration=2
        
        dataW = t.getCoinData(data, "7D", currentTime)
        if len(dataW) <= 1500:
            print("Bugged dataW")
            return (False, 1)
        # print(len(dataW))

        longMA = t.movingAverage(dataW, 28)
        shortMA = t.movingAverage(dataW, 14)

        isLongAboveShortInPast = True
        for i in range(1, noCrossDuration):
            if shortMA[i] > longMA[i]:
                isLongAboveShortInPast = False
                break
        
        if isLongAboveShortInPast and shortMA[0] > longMA[0]:
            l.append({"time": currentTime, "price":float(dataW[-1]["price"])})
            return (True, 0)
        
        return (False, 0)

def sellAllTrades(allData, tradesList, euroPerTrade, startDate, endDate):
    profit = 0
    td = copy.deepcopy(tradesList)

    noCrossDuration=2
    
    
    for i in range(len(allData)):
        currentTime = allData[i]["date"]
        doNotCheck = False


        for trade in td:
            for i in range(trade["time"], endDate, 300):
                dataW = t.getCoinData(allData, "7D", i)
                if len(dataW) <= 1500:
                    print("Bugged dataW")
                    return (False, 1)
                
                changePercentage = (float(dataW[-1]["close"]) - trade["price"])/trade["price"]

                longMA = t.movingAverage(dataW, 28)
                shortMA = t.movingAverage(dataW, 14)

                isLongAboveShortInPast = True
                for i in range(1, noCrossDuration):
                    if shortMA[i] < longMA[i]:
                        isLongAboveShortInPast = False
                        break
                
                if isLongAboveShortInPast and shortMA[0] < longMA[0] and currentTime>trade["time"]:
                    profit += euroPerTrade * changePercentage
                    td.remove(trade) 
                
            print(len(td))
    return profit



if __name__ == "__main__":
    t = Tools()
    threadList = []

    allData = t.readFile("DOGE") # Il faut avoir téléchargé le fichier avec Backtest-Tools-V2 au préalable et le placer dans ./Database/
    for i in range(len(allData)):
        allData[i]["date"] = int(allData[i]["date"])//1000


    blockSize = 300
    endDate = allData[-1]["date"]
    offset = 10000000
    startDate = endDate-1500000-offset

    fracturedData = t.fractureData(startDate, allData)

    buyingFunction = isWorthBuying

    allTradesList = t.allTradesInTimeFrame(fracturedData, startDate, endDate, blockSize, buyingFunction, offset)

    for x in allTradesList:
        print(x, end='\t')

    print(len(allTradesList))

    for i in range(1):
        print(sellAllTrades(allData, allTradesList, 100, startDate, endDate))

