from backtestTools import *

def isWorthBuying(t, data, currentTime, minFrame, l):
        
        dataW = t.getCoinData(data, "7D", currentTime)

        

        return (True, 0)

def sellAllTrades(allData, tradesList, euroPerTrade, maxHoldSecond):
    profit = 0
    for point in allData:
        for trade in tradesList:
            changePercentage = (float(point["close"]) - trade["price"]) / trade["price"]

            if point["date"]-trade["time"] < 0:
                break

            if point["date"]-trade["time"] > maxHoldSecond:
                profit += euroPerTrade * changePercentage
                tradesList.remove(trade)

            elif changePercentage > 0.02:
                profit += euroPerTrade * changePercentage
                tradesList.remove(trade) 
    
    return profit



if __name__ == "__main__":
    t = Tools()
    threadList = []

    allData = t.readFile("BTC") # Il faut avoir téléchargé le fichier avec Backtest-Tools-V2 au préalable et le placer dans ./Database/
    for i in range(len(allData)):
        allData[i]["date"] = int(allData[i]["date"])//1000
    startDate = int(allData[0]["date"])

    blockSize = 30000
    endDate = 1720000000

    fracturedData = t.fractureData(startDate, allData)

    buyingFunction = isWorthBuying

    allTradesList = t.allTradesInTimeFrame(fracturedData, startDate, endDate, blockSize, buyingFunction, 32000000)

    for x in allTradesList:
        print(x, end='\t')

    print(len(allTradesList))

    print(sellAllTrades(allData, allTradesList, 5, 200000))

