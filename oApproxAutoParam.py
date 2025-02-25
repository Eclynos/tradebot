import time
from multiprocessing import Pool, cpu_count
from tools import *
from math import sqrt

class Strategy:
    def __init__(self, power1=0.94, power2=0.94, buyingBollinger=1.5, sellingBollinger1=0, sellingBollinger2=1):
        self.MA_SIZE = 100
        self.wAvgSize = 2000
        self.power1 = power1
        self.power2 = power2
        self.buyingBollinger = buyingBollinger
        self.sellingBollinger1 = sellingBollinger1
        self.sellingBollinger2 = sellingBollinger2
        self.candles = []
        self.ma = []
        self.sd = []
        self.avg = []
        self.bb = []

    def modifyParams(self, power1=0.94, power2=0.94, buyingBollinger=1.5, sellingBollinger1=0, sellingBollinger2=1):
        self.power1 = power1
        self.power2 = power2
        self.buyingBollinger = buyingBollinger
        self.sellingBollinger1 = sellingBollinger1
        self.sellingBollinger2 = sellingBollinger2

    def trend(self, data, cutoff=1 / 2):
        milieu = int(len(data) * cutoff)
        hh1 = max(data[:milieu])
        hh2 = max(data[milieu:])
        ll1 = min(data[:milieu])
        ll2 = min(data[milieu:])

        if hh2 > hh1 and ll2 > ll1:
            return 1
        elif hh2 < hh1 and ll2 < ll1:
            return -1
        else:
            return 0

    def batchBuyingEvaluation(self):
        if self.power1 == 1:
            normalisationFactor = self.MA_SIZE
        else:
            normalisationFactor = (1 - self.power1 ** self.MA_SIZE) / (1 - self.power1)

        self.ma = []
        self.sd = []
        self.avg = []
        sdc = [0] * 5  # sd coefficients
        total = 0  # WeightedAverage coefficients
        denom = 0
        avgPrice = 0
        for i in range(len(self.candles)):
            if i >= self.MA_SIZE:
                self.ma.append(avgPrice / normalisationFactor)
                avgPrice -= self.power1 ** (self.MA_SIZE-1) * self.candles[i-self.MA_SIZE]
            avgPrice = avgPrice * self.power1 + self.candles[i]

        for i in range(self.MA_SIZE):
            sdc[0] += self.power1 ** (self.MA_SIZE-i-1) * self.candles[i] ** 2
            sdc[1] += self.power1 ** (self.MA_SIZE-i-1) * self.candles[i]
            sdc[2] += self.power2 ** (self.MA_SIZE-i-1) * self.candles[i]
            sdc[3] += self.power1 ** (self.MA_SIZE-i-1)
            sdc[4] += self.power2 ** (self.MA_SIZE-i-1)

        self.sd.append(sdc[0] - 2/sdc[4] * sdc[1] * sdc[2] + sdc[3]/(sdc[4]*sdc[4]) * sdc[2] * sdc[2])
        for i in range(1, len(self.candles) - self.MA_SIZE):
            sdc[0] = self.power1 * sdc[0] - self.power1 ** self.MA_SIZE * self.candles[i-1] ** 2 + self.candles[i + self.MA_SIZE - 1] ** 2
            sdc[1] = self.power1 * sdc[1] - self.power1 ** self.MA_SIZE * self.candles[i-1] + self.candles[i + self.MA_SIZE - 1]
            sdc[2] = self.power2 * sdc[2] - self.power2 ** self.MA_SIZE * self.candles[i-1] + self.candles[i + self.MA_SIZE - 1]
            self.sd.append(sdc[0] - 2/sdc[4] * sdc[1] * sdc[2] + sdc[3]/(sdc[4]*sdc[4]) * sdc[2] * sdc[2])

        for i in range(len(self.sd)):
            try:
                self.sd[i] = sqrt(self.sd[i]/sdc[3])
            except Exception as e:
                print(self.sd[i], e)
                exit()

        self.bb = [x + y * -self.buyingBollinger for x, y in zip(self.ma, self.sd)]

        for i in range(self.MA_SIZE):
            total += self.sd[i] ** 3
            denom += self.sd[i] ** 2
        self.avg.append(total / denom)
        for i in range(1, len(self.sd) - self.MA_SIZE):
            total += self.sd[i + self.MA_SIZE] ** 3 - self.sd[i - 1] ** 3
            denom += self.sd[i + self.MA_SIZE] ** 2 - self.sd[i - 1] ** 2
            self.avg.append(total / denom)

        print(self.ma[-1], self.bb[-1], self.sd[-1], self.avg[-1])
        print(self.ma[-2], self.bb[-2], self.sd[-2], self.avg[-2])
        exit()
        # buyIndexes
        return [i for i in range(self.wAvgSize + self.MA_SIZE, len(self.candles) - 2) if (
            self.sd[i - self.MA_SIZE] > self.avg[i - self.wAvgSize - self.MA_SIZE + 1] and
            self.sd[i - self.MA_SIZE - 1] < self.avg[i - self.wAvgSize - self.MA_SIZE] and
            self.trend(self.candles[i - self.wAvgSize + 1:i + 1], 1 / 2) == -1 and
            self.candles[i] < self.bb[i - self.wAvgSize]
        )]

    def batchSellingEvaluation(self, buyIndexes, percentage_traded):
        profit = 1.0

        bb2 = [x + y * self.buyingBollinger for x, y in zip(self.ma, self.sd)]

        bougies = self.candles[self.MA_SIZE:]

        for index in buyIndexes:
            has_passed_under_0 = False
            for j in range(index - self.MA_SIZE, len(bougies)):
                if bougies[j] > self.bb[j]:
                    has_passed_under_0 = True
                if (j - self.wAvgSize > 0 and self.sd[j] < self.avg[j - self.wAvgSize] and self.sd[j - 1] > self.avg[j - self.wAvgSize - 1]) or (has_passed_under_0 and bougies[j] > bb2[j]):
                    break
            profit += profit * percentage_traded * (bougies[j] / self.candles[index] - 1) - 0.0008

        return profit

SAMPLE_SIZE = 2000
LAUNCH_SAMPLE_SIZE = 2104

NB_THREADS = 8
NB_POINTS_TESTES = 2
NB_RECURSIONS = 2
REDUCTION_PAR_ETAPE = 0.5

coinCodes = [
    "HNT"
]

data = [readFileToList(coinCode, "bitget") for coinCode in coinCodes]

STRATEGY_NAME = "dip"
PERCENTAGE_TRADED = 0.25

INSTANCES_BOUNDS = {
    "power1": [0.8, 1.0],
    "power2": [0.8, 1.0],
    "buyingBollinger": [0.0, 3.0],
    "sellingBollinger1": [-1.0, 1.0],
    "sellingBollinger2": [0.0, 3.0]
}

s = {cc: None for cc in coinCodes}

def bestPoint(nb_points_testes, bounds, s):
    """Renvoyer best_params et best_yield"""
    best_params = {}
    best_yield = -100

    for power1 in [bounds["power1"][0] + (bounds["power1"][1] - bounds["power1"][0]) / (nb_points_testes - 1) * i for i in range(nb_points_testes)]:
        for power2 in [bounds["power2"][0] + (bounds["power2"][1] - bounds["power2"][0]) / (nb_points_testes - 1) * i for i in range(nb_points_testes)]:
            for buyingBollinger in [bounds["buyingBollinger"][0] + (bounds["buyingBollinger"][1] - bounds["buyingBollinger"][0]) / (nb_points_testes - 1) * i for i in range(nb_points_testes)]:
                for sellingBollinger1 in [bounds["sellingBollinger1"][0] + (bounds["sellingBollinger1"][1] - bounds["sellingBollinger1"][0]) / (nb_points_testes - 1) * i for i in range(nb_points_testes)]:
                    for sellingBollinger2 in [bounds["sellingBollinger2"][0] + (bounds["sellingBollinger2"][1] - bounds["sellingBollinger2"][0]) / (nb_points_testes - 1) * i for i in range(nb_points_testes)]:

                            s.modifyParams(power1, power2, buyingBollinger, sellingBollinger1, sellingBollinger2)
                            buyIndexes = s.batchBuyingEvaluation()
                            profit = s.batchSellingEvaluation(buyIndexes, PERCENTAGE_TRADED)

                            if profit > best_yield:
                                best_params = {"power1": power1, "power2": power2, "buyingBollinger": buyingBollinger, "sellingBollinger1" : sellingBollinger1, "sellingBollinger2": sellingBollinger2}
                                best_yield = profit

    return best_params, best_yield

def process_function(cc):
    st = time.time()
    bounds = INSTANCES_BOUNDS.copy()
    s[cc] = Strategy()
    s[cc].candles = data[cc]
    for recursion in range(NB_RECURSIONS):
        meilleurParam, meilleurYield = bestPoint(NB_POINTS_TESTES, bounds, s[cc])
        for param in meilleurParam:
            bounds[param][0] = meilleurParam[param] - REDUCTION_PAR_ETAPE * (bounds[param][1]-bounds[param][0])
            if param in ["power1", "power2"]:
                bounds[param][1] = min(1, meilleurParam[param] + REDUCTION_PAR_ETAPE * (bounds[param][1]-bounds[param][0]))
            else:
                bounds[param][1] = meilleurParam[param] + REDUCTION_PAR_ETAPE * (bounds[param][1]-bounds[param][0])
        print(recursion)

    print(f"The best params for {coinCodes[cc]} are:\n{str(meilleurParam)}\nyield: {meilleurYield}\nCalculation time: {time.time() - st}")

if __name__ == "__main__":
    if NB_THREADS > cpu_count():
        raise ValueError(f"Can't process on {NB_THREADS} threads, cpu has only {cpu_count()} threads.")

    with Pool(processes=NB_THREADS) as pool:
        pool.map(process_function, range(len(coinCodes)))