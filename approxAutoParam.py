from strategyStandardDevPump import *
from dataAnalysis import *
from tools import *
import time
from multiprocessing import Pool, cpu_count

SAMPLE_SIZE = 2000
LAUNCH_SAMPLE_SIZE = 2104

NB_THREADS = 8
NB_POINTS_TESTES_ENTRE_BORNES = 2
NB_RECURSIONS = 2
REDUCTION_PAR_ETAPE = 0.5
START_TIME = "8M"
END_TIME = "6M"


if (NB_THREADS > cpu_count()):
    raise ValueError(f"Can't process on {NB_THREADS} threads, cpu has only {cpu_count()} threads")

coinCodes = [
    "HNT"
]

# coinCodes = [
#     "BTC",
#     "ETH",
#     "SOL",
#     "DOGE",
#     "DOT",
#     "BNB",
#     "PEPE",
#     "SUI",
#     "DOGE",
#     "DOT",
#     "TRX",
#     "LTC",
#     "AVAX",
#     "ADA",
#     "XRP",
#     "APE",
#     "FET"
# ]

data = [readFile(coinCode, "bitget") for coinCode in coinCodes]

currentDate = time.time() * 1000
SEindex = [getMaxDataIndex(coinData) for coinData in data]

data = [data[i][SEindex[i][0]:SEindex[i][1]+1] for i in range(len(coinCodes))]
data = [[{"date": int(data[i][j]["date"]) // 1000, "price": float(data[i][j]["close"]), "index" :j} for j in range(len(data[i]))] for i in range(len(coinCodes))]

STRATEGY_NAME = "dip"
PERCENTAGE_TRADED = 0.25

INSTANCES_BOUNDS = {
    "power1" : [0.8, 1],
    "power2" : [0.8, 1],
    "buyingBollinger": [0, 3],
    "sellingBollinger1": [-1, 1],
    "sellingBollinger2": [0, 3]
}

s = {cc: None for cc in coinCodes}

def bestPoint(cc, nb_points_testes, bornes, s, data):
    """Renvoyer best_params et best_yield"""
    best_params = {}
    best_yield = -100

    s[cc].candles = data[cc]
    for power1 in [bornes["power1"][0] + (bornes["power1"][1] - bornes["power1"][0]) / (nb_points_testes - 1) * i for i in range(nb_points_testes)]:
        for power2 in [bornes["power2"][0] + (bornes["power2"][1] - bornes["power2"][0]) / (nb_points_testes - 1) * i for i in range(nb_points_testes)]:
            for buyingBollinger in [bornes["buyingBollinger"][0] + (bornes["buyingBollinger"][1] - bornes["buyingBollinger"][0]) / (nb_points_testes - 1) * i for i in range(nb_points_testes)]:
                for sellingBollinger1 in [bornes["sellingBollinger1"][0] + (bornes["sellingBollinger1"][1] - bornes["sellingBollinger1"][0]) / (nb_points_testes - 1) * i for i in range(nb_points_testes)]:
                    for sellingBollinger2 in [bornes["sellingBollinger2"][0] + (bornes["sellingBollinger2"][1] - bornes["sellingBollinger2"][0]) / (nb_points_testes - 1) * i for i in range(nb_points_testes)]:

                        s[cc].modifyParams(power1, power2, buyingBollinger, sellingBollinger1, sellingBollinger2)

                        s[cc].candles = data[cc]
                        tradeTimeList = s[cc].batchBuyingEvaluation()

                        tradeList = [data[cc][timeStampToIndex(data[cc], timeStamp)] for timeStamp in tradeTimeList]

                        s[cc].candles = data[cc][100:]
                        result = s[cc].batchSellingEvaluation(tradeList, PERCENTAGE_TRADED)

                        if result[1] > best_yield:
                            best_params = {"power1": power1, "power2": power2, "buyingBollinger": buyingBollinger, "sellingBollinger1" : sellingBollinger1, "sellingBollinger2": sellingBollinger2}
                            best_yield = result[1]

    return best_params, best_yield


def process_function(cc):
    st = time.time()
    bounds_copy = INSTANCES_BOUNDS.copy()
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
    with Pool(processes=int(NB_THREADS)) as pool:
        pool.map(process_function, range(len(coinCodes)))