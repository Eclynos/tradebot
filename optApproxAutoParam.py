import torch, time
from tools import *

FLOAT_TYPE = torch.float64
DEVICE = torch.device("cpu")

class Strategy:
    def __init__(self, power1=0.94, power2=0.94, buyingBollinger=1.5, sellingBollinger1=0, sellingBollinger2=1):
        self.MA_SIZE = 100
        self.power1 = power1
        self.power2 = power2
        self.buyingBollinger = buyingBollinger
        self.sellingBollinger1 = sellingBollinger1
        self.sellingBollinger2 = sellingBollinger2
        self.candles = []

    def modifyParams(self, power1=0.94, power2=0.94, buyingBollinger=1.5, sellingBollinger1=0, sellingBollinger2=1):
        self.power1 = power1
        self.power2 = power2
        self.buyingBollinger = buyingBollinger
        self.sellingBollinger1 = sellingBollinger1
        self.sellingBollinger2 = sellingBollinger2

    def exponentialMovingAverage(self):
        # comprendre pour remplacer par des matrices
        ma = torch.zeros(len(self.candles) - self.MA_SIZE, dtype=FLOAT_TYPE)
        normalisationFactor = (1 - torch.pow(self.power1, self.MA_SIZE)) / (1 - self.power1)

        avgPrice = torch.zeros((len(self.candles)), dtype=FLOAT_TYPE)
        for torch.pow()


        # for i in range(len(self.candles)):
        #     if i >= self.MA_SIZE:
        #         ma.append((avgPrice / normalisationFactor).item())
        #         avgPrice -= torch.pow(self.power1, self.MA_SIZE - 1) * self.candles[i - self.MA_SIZE]
        #     avgPrice *= self.power1 + self.candles[i]

        return ma



    def batchBuyingEvaluation(self):
        pass
        #la bollinger peut être fait tellement + vite
    

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

data = [readFileToTensor(coinCode, "bitget", FLOAT_TYPE) for coinCode in coinCodes]

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

st = time.time()
for cc in range(len(coinCodes)):
    s[cc] = Strategy()