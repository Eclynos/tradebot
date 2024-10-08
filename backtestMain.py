from strategyGCDrop import *
from dataAnalysis import *
from tools import *
import copy


if __name__ == "__main__":
    s = Strategy()
    da = DataAnalysis()
    t = Tools()

    allData = t.readFile("BTC") # Il faut avoir téléchargé le fichier avec Backtest-Tools-V2 au préalable et le placer dans ./data/

    usableData = []
    for i in range(len(allData)):
        usableData.append({"date": int(allData[i]["date"])//1000, "price": float(allData[i]["close"]), "index" :i})

    print("data ready : start of buying evaluation")
    tradeList = []
    for i in range(len(usableData)//2, len(usableData)):
        if s.buyingEvaluation(usableData[i-75:i+1], usableData[i]["date"]) and (len(tradeList) == 0 or usableData[i]["date"] > tradeList[-1]["date"] + t.time_frame_to_s("30m")):
            tradeList.append(usableData[i])
        
        if i%1000 == 0:
            print("buying progress :", 100*i/len(usableData), "%")

    print(s.sellingEvaluation(usableData, tradeList, "7d"))


