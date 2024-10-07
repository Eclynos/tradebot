from strategyGCDrop import *
from dataAnalysis import *
from tools import *
import copy


if __name__ == "__main__":
    s = Strategy()
    da = DataAnalysis()
    t = Tools()

    allData = t.readFile("DOGE") # Il faut avoir téléchargé le fichier avec Backtest-Tools-V2 au préalable et le placer dans ./Database/
    for i in range(len(allData)):
        allData[i]["date"] = int(allData[i]["date"])//1000

    print(da.allGoldenCrosses(allData[1000: 2000], 5, 20, 50))


