import time
import numpy as np
from multiprocessing import Pool, cpu_count
from tools import *

class Strategy:
    def __init__(self, candles, ma_size=100, wAvgSize=2000, power1=0.94, power2=0.94, buyingBollinger=1.5, sellingBollinger1=0, sellingBollinger2=1):
        self.MA_SIZE = ma_size
        self.wAvgSize = wAvgSize
        self.power1 = power1
        self.power2 = power2
        self.buyingBollinger = buyingBollinger
        self.sellingBollinger1 = sellingBollinger1
        self.sellingBollinger2 = sellingBollinger2
        self.candles = np.array(candles)
        self.ma = np.zeros(len(candles) - ma_size)
        self.sd = np.zeros(len(candles) - ma_size)
        self.avg = np.zeros(len(candles) - ma_size - wAvgSize)
        self.bbb = np.zeros(len(candles) - ma_size)

    def modifyParams(self, power1=0.94, power2=0.94, buyingBollinger=1.5, sellingBollinger1=0, sellingBollinger2=1):
        self.power1 = power1
        self.power2 = power2
        self.buyingBollinger = buyingBollinger
        self.sellingBollinger1 = sellingBollinger1
        self.sellingBollinger2 = sellingBollinger2

    def trend(self, data, cutoff=0.5):
        milieu = int(len(data) * cutoff)
        hh1 = np.max(data[:milieu])
        hh2 = np.max(data[milieu:])
        ll1 = np.min(data[:milieu])
        ll2 = np.min(data[milieu:])

        if hh2 > hh1 and ll2 > ll1:
            return 1
        elif hh2 < hh1 and ll2 < ll1:
            return -1
        else:
            return 0

    def batchBuyingEvaluation(self):
        normalisationFactor = self.MA_SIZE if self.power1 == 1 else round((1 - self.power1 ** self.MA_SIZE) / (1 - self.power1), 6)
        sdc = np.zeros(5)  # sd coefficients
        avgPrice = 0

        # Initialisation des coefficients sdc
        power1_range = self.power1 ** np.arange(self.MA_SIZE - 1, -1, -1)
        power2_range = self.power2 ** np.arange(self.MA_SIZE - 1, -1, -1)

        sdc[0] = np.sum(power1_range * self.candles[:self.MA_SIZE] ** 2)
        sdc[1] = np.sum(power1_range * self.candles[:self.MA_SIZE])
        sdc[2] = np.sum(power2_range * self.candles[:self.MA_SIZE])
        sdc[3] = np.sum(power1_range)
        sdc[4] = np.sum(power2_range)

        avgPrice = np.sum(power1_range * self.candles[:self.MA_SIZE])

        for i in range(self.MA_SIZE, len(self.candles)):
            self.ma[i-self.MA_SIZE] = avgPrice / normalisationFactor
            avgPrice = avgPrice * self.power1 - self.power1 ** self.MA_SIZE * self.candles[i-self.MA_SIZE] + self.candles[i]

        variance = (sdc[0] - 2/sdc[4] * sdc[1] * sdc[2] + sdc[3]/(sdc[4]*sdc[4]) * sdc[2] * sdc[2]) / sdc[3]
        if variance >= 0:
            self.sd[0] = np.sqrt(variance)
        else:
            self.sd[0] = 0  # ou une autre valeur par défaut

        self.bbb[0] = self.ma[0] + self.sd[0] * -self.buyingBollinger

        for i in range(1, len(self.candles) - self.MA_SIZE):
            sdc[0] = self.power1 * sdc[0] - self.power1 ** self.MA_SIZE * self.candles[i-1] ** 2 + self.candles[i + self.MA_SIZE - 1] ** 2
            sdc[1] = self.power1 * sdc[1] - self.power1 ** self.MA_SIZE * self.candles[i-1] + self.candles[i + self.MA_SIZE - 1]
            sdc[2] = self.power2 * sdc[2] - self.power2 ** self.MA_SIZE * self.candles[i-1] + self.candles[i + self.MA_SIZE - 1]

            variance = (sdc[0] - 2/sdc[4] * sdc[1] * sdc[2] + sdc[3]/(sdc[4]*sdc[4]) * sdc[2] * sdc[2]) / sdc[3]
            if variance >= 0:
                self.sd[i] = np.sqrt(variance)
            else:
                self.sd[i] = 0  # ou une autre valeur par défaut

            self.bbb[i] = self.ma[i] + self.sd[i] * -self.buyingBollinger

        total = np.sum(self.sd[:self.wAvgSize] ** 3)
        denom = np.sum(self.sd[:self.wAvgSize] ** 2)
        self.avg[0] = total / denom

        for i in range(1, len(self.sd) - self.wAvgSize):
            total += self.sd[i + self.wAvgSize] ** 3 - self.sd[i - 1] ** 3
            denom += self.sd[i + self.wAvgSize] ** 2 - self.sd[i - 1] ** 2
            self.avg[i] = total / denom

        return [i for i in range(self.wAvgSize + self.MA_SIZE, len(self.candles) - 2) if (
            self.sd[i - self.MA_SIZE] > self.avg[i - self.wAvgSize - self.MA_SIZE + 1] and
            self.sd[i - self.MA_SIZE - 1] < self.avg[i - self.wAvgSize - self.MA_SIZE] and
            self.trend(self.candles[i - self.MA_SIZE + 1:i + 1], 0.5) == -1 and
            self.candles[i] < self.bbb[i - self.MA_SIZE]
        )]

    def batchSellingEvaluation(self, buyIndexes, percentage_traded):
        profit = 1.0

        bb = self.ma + self.sd * -self.sellingBollinger1
        bb2 = self.ma + self.sd * self.sellingBollinger2

        for index in buyIndexes:
            has_passed_under_0 = False
            for j in range(index - self.MA_SIZE, len(self.candles) - self.MA_SIZE):
                if self.candles[j+self.MA_SIZE] > bb[j]:
                    has_passed_under_0 = True
                if ((j - self.wAvgSize > 0 and self.sd[j] < self.avg[j - self.wAvgSize] and self.sd[j - 1] > self.avg[j - self.wAvgSize - 1])
                    or (has_passed_under_0 and self.candles[j+self.MA_SIZE] > bb2[j])):
                    break
            profit += profit * percentage_traded * ((self.candles[j+self.MA_SIZE] / self.candles[index] - 1) - 0.0008)

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

    for power1 in np.linspace(bounds["power1"][0], bounds["power1"][1], nb_points_testes):
        for power2 in np.linspace(bounds["power2"][0], bounds["power2"][1], nb_points_testes):
            for buyingBollinger in np.linspace(bounds["buyingBollinger"][0], bounds["buyingBollinger"][1], nb_points_testes):
                for sellingBollinger1 in np.linspace(bounds["sellingBollinger1"][0], bounds["sellingBollinger1"][1], nb_points_testes):
                    for sellingBollinger2 in np.linspace(bounds["sellingBollinger2"][0], bounds["sellingBollinger2"][1], nb_points_testes):

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
    s[cc] = Strategy(data[cc])
    for recursion in range(NB_RECURSIONS):
        meilleurParam, meilleurYield = bestPoint(NB_POINTS_TESTES, bounds, s[cc])
        for param in meilleurParam:
            bounds[param][0] = meilleurParam[param] - REDUCTION_PAR_ETAPE * (bounds[param][1]-bounds[param][0])
            if param in ["power1", "power2"]:
                bounds[param][1] = min(1, meilleurParam[param] + REDUCTION_PAR_ETAPE * (bounds[param][1]-bounds[param][0]))
            else:
                bounds[param][1] = meilleurParam[param] + REDUCTION_PAR_ETAPE * (bounds[param][1]-bounds[param][0])
        print(f"{coinCodes[cc]} :{recursion}")

    print(f"The best params for {coinCodes[cc]} are:\n{str(meilleurParam)}\nyield: {meilleurYield}\nCalculation time: {time.time() - st}")

if __name__ == "__main__":
    if NB_THREADS > cpu_count():
        raise ValueError(f"Can't process on {NB_THREADS} threads, cpu has only {cpu_count()} threads.")

    with Pool(processes=NB_THREADS) as pool:
        pool.map(process_function, range(len(coinCodes)))
