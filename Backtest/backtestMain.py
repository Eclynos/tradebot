from backtestTools import *
import threading
import time

if __name__ == "__main__":
    t = Tools()
    
    allData = t.readFile("BTC") # Il faut avoir téléchargé le fichier avec Backtest-Tools-V2 au préalable et le placer dans ./Database/
    startDate = int(allData[0]["date"])//1000

    fracturedData = t.fractureData(startDate, allData, 86400)

    buyingFunction = t.isWorthBuying

    print(t.allTradesInTimeFrame(fracturedData, startDate, 1720000000, 86400, buyingFunction))
