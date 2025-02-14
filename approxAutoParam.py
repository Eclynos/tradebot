from strategyStandardDevPump import *
from dataAnalysis import *
from tools import *
import time, threading, sys

SAMPLE_SIZE = 2000
LAUNCH_SAMPLE_SIZE = 2104

coinCodes = [
    "SOL",
]

data = [readFile(coinCode, "bitget") for coinCode in coinCodes]

currentDate = time.time() * 1000
SEindex = [getDataIndex(currentDate, "8M", "4M", coinData, LAUNCH_SAMPLE_SIZE) for coinData in data]

data = [data[i][SEindex[i][0]:SEindex[i][1]] for i in range(len(coinCodes))]
data = [[{"date": int(data[i][j]["date"]) // 1000, "price": float(data[i][j]["close"]), "index" :j} for j in range(len(data[i]))] for i in range(len(coinCodes))]


STRATEGY_NAME = "dip"
PERCENTAGE_TRADED = 0.25
CANDLES_IN_PERIOD = SEindex[0][1] - SEindex[0][0]

s = Strategy(100, SAMPLE_SIZE, 0.92, 0.92, 1.5, 0, 1, 100)

"""
INSTANCES = {
    "power1": [0.936, 0.937, 0.938, 0.939, 0.94, 0.941, 0.942, 0.943, 0.944],
    "power2": [0.936, 0.937, 0.938, 0.939, 0.94, 0.941, 0.942, 0.943, 0.944],
    "buyingBollinger": [1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9],
    "sellingBollinger1": [0, 0.01, 0.02, 0.03],
    "sellingBollinger2": [0.998, 0.999, 1, 1.01, 1.02]
}
"""

INSTANCES_BOUNDS = {
    "power1" : [0.8, 1],
    "power2" : [0.8, 1],
    "buyingBollinger": [0, 3],
    "sellingBollinger1": [-1, 1],
    "sellingBollinger2": [0, 3]
}

NB_POINTS_TESTES_ENTRE_BORNES = 3
NB_RECURSIONS = 5
REDUCTION_PAR_ETAPE = 0.25

def bestPoint(cc, nb_points_testes, bornes):
    """Renvoyer best_params et best_yield"""
    best_params = {}
    best_yield = -1000

    s.candles = data[cc]
    for power1 in [bornes["power1"][0] + (bornes["power1"][1] - bornes["power1"][0]) / (nb_points_testes - 1) * i for i in range(nb_points_testes)]:
        for power2 in [bornes["power2"][0] + (bornes["power2"][1] - bornes["power2"][0]) / (nb_points_testes - 1) * i for i in range(nb_points_testes)]:
            for buyingBollinger in [bornes["buyingBollinger"][0] + (bornes["buyingBollinger"][1] - bornes["buyingBollinger"][0]) / (nb_points_testes - 1) * i for i in range(nb_points_testes)]:
                for sellingBollinger1 in [bornes["sellingBollinger1"][0] + (bornes["sellingBollinger1"][1] - bornes["sellingBollinger1"][0]) / (nb_points_testes - 1) * i for i in range(nb_points_testes)]:
                    for sellingBollinger2 in [bornes["sellingBollinger2"][0] + (bornes["sellingBollinger2"][1] - bornes["sellingBollinger2"][0]) / (nb_points_testes - 1) * i for i in range(nb_points_testes)]:

                        s.modifyParams(power1, power2, buyingBollinger, sellingBollinger1, sellingBollinger2)

                        s.candles = data[cc]
                        tradeTimeList = s.batchBuyingEvaluation("dip")

                        tradeList = [data[cc][timeStampToIndex(data[cc], timeStamp)] for timeStamp in tradeTimeList]

                        s.candles = data[cc][100:]
                        result = s.batchSellingEvaluation(tradeList, PERCENTAGE_TRADED)

                        if result[1] > best_yield:
                            best_params = {"power1": power1, "power2": power2, "buyingBollinger": buyingBollinger, "sellingBollinger1" : sellingBollinger1, "sellingBollinger2": sellingBollinger2}
                            best_yield = result[1]

    return best_params, best_yield


for cc in range(len(coinCodes)):
    st = time.time()

    bounds_copy = INSTANCES_BOUNDS.copy()
    for _ in range(NB_RECURSIONS):
        meilleurParam, meilleurYield = bestPoint(cc, NB_POINTS_TESTES_ENTRE_BORNES, bounds_copy)
        for param in meilleurParam:
            bounds_copy[param][0] = meilleurParam[param] - REDUCTION_PAR_ETAPE * (bounds_copy[param][1]-bounds_copy[param][0])
            if param in ["power1", "power2"]:
                bounds_copy[param][1] = min(1, meilleurParam[param] + REDUCTION_PAR_ETAPE * (bounds_copy[param][1]-bounds_copy[param][0]))
            else:
                bounds_copy[param][1] = meilleurParam[param] + REDUCTION_PAR_ETAPE * (bounds_copy[param][1]-bounds_copy[param][0])
    
    print(f"The best params for {coinCodes[cc]} are:\n{str(meilleurParam)}\nyield: {meilleurYield}\nCalculation time: {time.time() - st}")


"""
Test SOL 18M 6M 14/02/2025-12:38 (fin)
14580 instances of params
Average time: 0.29249216257626465
The best params for SOL are:
{'power1': 0.936, 'power2': 0.936, 'buyingBollinger': 1.2, 'sellingBollinger1': 0, 'sellingBollinger2': 0.998}
yield: 1.096746777979021
Calculation time: 4264.564913272858
"""