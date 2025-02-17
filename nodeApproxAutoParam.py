import tensorflow as tf
from strategyStandardDevPump import *
from dataAnalysis import *
from tools import *
import time

SAMPLE_SIZE = 2000
LAUNCH_SAMPLE_SIZE = 2104

NB_POINTS_TESTES_ENTRE_BORNES = 2
NB_RECURSIONS = 2
REDUCTION_PAR_ETAPE = 0.5
START_TIME = "8M"
END_TIME = "6M"

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
    "power1" : [0.8, 1],
    "power2" : [0.8, 1],
    "buyingBollinger": [0, 3],
    "sellingBollinger1": [-1, 1],
    "sellingBollinger2": [0, 3]
}


s = {cc: None for cc in coinCodes}


def bestPoint(cc, nb_points_testes, bornes, s, data):
    """Return best_params and best_yield"""
    best_params = {}
    best_yield = -1000

    s[cc].candles = data[cc]

    power1 = tf.Variable(bornes["power1"][0], dtype=tf.float32)
    power2 = tf.Variable(bornes["power2"][0], dtype=tf.float32)
    buyingBollinger = tf.Variable(bornes["buyingBollinger"][0], dtype=tf.float32)
    sellingBollinger1 = tf.Variable(bornes["sellingBollinger1"][0], dtype=tf.float32)
    sellingBollinger2 = tf.Variable(bornes["sellingBollinger2"][0], dtype=tf.float32)

    power1_values = tf.linspace(bornes["power1"][0], bornes["power1"][1], nb_points_testes)
    power2_values = tf.linspace(bornes["power2"][0], bornes["power2"][1], nb_points_testes)
    buyingBollinger_values = tf.linspace(bornes["buyingBollinger"][0], bornes["buyingBollinger"][1], nb_points_testes)
    sellingBollinger1_values = tf.linspace(bornes["sellingBollinger1"][0], bornes["sellingBollinger1"][1], nb_points_testes)
    sellingBollinger2_values = tf.linspace(bornes["sellingBollinger2"][0], bornes["sellingBollinger2"][1], nb_points_testes)

    for p1 in power1_values:
        for p2 in power2_values:
            for bb in buyingBollinger_values:
                for sb1 in sellingBollinger1_values:
                    for sb2 in sellingBollinger2_values:
                        power1.assign(tf.cast(p1, tf.float32))
                        power2.assign(tf.cast(p2, tf.float32))
                        buyingBollinger.assign(tf.cast(bb, tf.float32))
                        sellingBollinger1.assign(tf.cast(sb1, tf.float32))
                        sellingBollinger2.assign(tf.cast(sb2, tf.float32))

                        s[cc].modifyParams(power1.numpy(), power2.numpy(), buyingBollinger.numpy(), sellingBollinger1.numpy(), sellingBollinger2.numpy())

                        s[cc].candles = data[cc]
                        tradeTimeList = s[cc].batchBuyingEvaluation()

                        tradeList = [data[cc][timeStampToIndex(data[cc], timeStamp)] for timeStamp in tradeTimeList]

                        s[cc].candles = data[cc][100:]
                        result = s[cc].batchSellingEvaluation(tradeList, PERCENTAGE_TRADED)

                        if result[1] > best_yield:
                            best_params = {"power1": p1.numpy(), "power2": p2.numpy(), "buyingBollinger": bb.numpy(), "sellingBollinger1" : sb1.numpy(), "sellingBollinger2": sb2.numpy()}
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
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        try:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
        except RuntimeError as e:
            print(e)

    main()