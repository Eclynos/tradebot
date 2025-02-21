import torch
import time
from ptStrategyStandardDevPump import *
from ptDataAnalysis import *
from tools import *

SAMPLE_SIZE = 2000
LAUNCH_SAMPLE_SIZE = 2104

NB_POINTS_TESTES_ENTRE_BORNES = 2
NB_RECURSIONS = 2
REDUCTION_PAR_ETAPE = 0.5
START_TIME = "8M"
END_TIME = "6M"
FLOAT_TYPE = torch.float64

coinCodes = [
    "SOL"
]

data = [readFile(coinCode, "bitget") for coinCode in coinCodes]

currentDate = time.time() * 1000
SEindex = [getDataIndexFromPeriod(currentDate, START_TIME, END_TIME, coinData, LAUNCH_SAMPLE_SIZE) for coinData in data]

data = [data[i][SEindex[i][0]:SEindex[i][1]] for i in range(len(coinCodes))]
data = [[{"date": int(data[i][j]["date"]) // 1000, "price": float(data[i][j]["close"]), "index" :j} for j in range(len(data[i]))] for i in range(len(coinCodes))]

STRATEGY_NAME = "dip"
PERCENTAGE_TRADED = 0.25

INSTANCES_BOUNDS = {
    "power1": [torch.tensor(0.8, dtype=FLOAT_TYPE), torch.tensor(1.0, dtype=FLOAT_TYPE)],
    "power2": [torch.tensor(0.8, dtype=FLOAT_TYPE), torch.tensor(1.0, dtype=FLOAT_TYPE)],
    "buyingBollinger": [torch.tensor(0.0, dtype=FLOAT_TYPE), torch.tensor(3.0, dtype=FLOAT_TYPE)],
    "sellingBollinger1": [torch.tensor(-1.0, dtype=FLOAT_TYPE), torch.tensor(1.0, dtype=FLOAT_TYPE)],
    "sellingBollinger2": [torch.tensor(0.0, dtype=FLOAT_TYPE), torch.tensor(3.0, dtype=FLOAT_TYPE)]
}

s = {cc: None for cc in coinCodes}

def bestPoint(cc, nb_points_testes, bornes, s, data):
    """Return best_params and best_yield"""
    best_params = {}
    best_yield = -1000

    for p1 in torch.linspace(bornes["power1"][0], bornes["power1"][1], nb_points_testes):
        for p2 in torch.linspace(bornes["power2"][0], bornes["power2"][1], nb_points_testes):
            for bb in torch.linspace(bornes["buyingBollinger"][0], bornes["buyingBollinger"][1], nb_points_testes):
                for sb1 in torch.linspace(bornes["sellingBollinger1"][0], bornes["sellingBollinger1"][1], nb_points_testes):
                    for sb2 in torch.linspace(bornes["sellingBollinger2"][0], bornes["sellingBollinger2"][1], nb_points_testes):

                        s[cc].modifyParams(p1.item(), p2.item(), bb.item(), sb1.item(), sb2.item())

                        s[cc].candles = data[cc]
                        tradeTimeList = s[cc].batchBuyingEvaluation()

                        tradeList = [data[cc][timeStampToIndex(data[cc], timeStamp)] for timeStamp in tradeTimeList]

                        s[cc].candles = data[cc][100:]
                        result = s[cc].batchSellingEvaluation(tradeList, PERCENTAGE_TRADED)

                        if result[1] > best_yield:
                            best_params = {"power1": p1.item(), "power2": p2.item(), "buyingBollinger": bb.item(), "sellingBollinger1" : sb1.item(), "sellingBollinger2": sb2.item()}
                            best_yield = result[1]

    return best_params, best_yield

def main():
    st = time.time()
    bounds_copy = INSTANCES_BOUNDS.copy()
    for cc in range(len(coinCodes)):
        s[cc] = Strategy(100, SAMPLE_SIZE)
        for recursion in range(NB_RECURSIONS):
            meilleurParam, meilleurYield = bestPoint(cc, NB_POINTS_TESTES_ENTRE_BORNES, bounds_copy, s, data)
            for param in meilleurParam:
                bounds_copy[param][0] = meilleurParam[param] - REDUCTION_PAR_ETAPE * (bounds_copy[param][1]-bounds_copy[param][0])
                if param in ["power1", "power2"]:
                    bounds_copy[param][1] = min(1, meilleurParam[param] + REDUCTION_PAR_ETAPE * (bounds_copy[param][1]-bounds_copy[param][0]))
                else:
                    bounds_copy[param][1] = meilleurParam[param] + REDUCTION_PAR_ETAPE * (bounds_copy[param][1]-bounds_copy[param][0])
            print(recursion)

        print(f"The best params for {coinCodes[cc]} are:\n{str(meilleurParam)}\nyield: {meilleurYield}\nCalculation time: {time.time() - st}")

if __name__ == "__main__":
    main()