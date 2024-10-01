from backtestTools import *
import threading
import time

if __name__ == "__main__":
    t = Tools()
    threadList = []

    allData = t.readFile("BTC") # Il faut avoir téléchargé le fichier avec Backtest-Tools-V2 au préalable et le placer dans ./Database/
    startDate = int(allData[0]["date"])//1000
    blockSize = 9000
    endDate = 1720000000

    fracturedData = t.fractureData(startDate, allData)

    buyingFunction = t.isWorthBuying

    print(t.allTradesInTimeFrame(fracturedData, startDate, endDate, blockSize, buyingFunction))