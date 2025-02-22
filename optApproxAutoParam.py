import torch, time
from tools import *

FLOAT_TYPE = torch.float32
DEVICE = torch.device("cpu")

class Strategy:
    def __init__(self, power1=0.94, power2=0.94, buyingBollinger=1.5, sellingBollinger1=0, sellingBollinger2=1):
        self.MA_SIZE = 100
        self.wAvgSize = 2000
        self.power1 = power1
        self.power2 = power2
        self.buyingBollinger = buyingBollinger
        self.sellingBollinger1 = sellingBollinger1
        self.sellingBollinger2 = sellingBollinger2
        self.candles = None
        self.ma = None
        self.sd = None
        self.avg = None

    def modifyParams(self, power1=0.94, power2=0.94, buyingBollinger=1.5, sellingBollinger1=0, sellingBollinger2=1):
        self.power1 = power1
        self.power2 = power2
        self.buyingBollinger = buyingBollinger
        self.sellingBollinger1 = sellingBollinger1
        self.sellingBollinger2 = sellingBollinger2


    def trend(self, data, cutoff=1 / 2):
        milieu = int(len(data) * cutoff)
        hh1 = torch.max(data[:milieu])
        hh2 = torch.max(data[milieu:])
        ll1 = torch.min(data[:milieu])
        ll2 = torch.min(data[milieu:])

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

        self.ma = torch.empty(len(self.candles) - self.MA_SIZE, dtype=FLOAT_TYPE)
        self.sd = torch.zeros(len(self.candles) - self.MA_SIZE, dtype=FLOAT_TYPE)
        self.avg = torch.empty(len(self.candles) - self.MA_SIZE, dtype=FLOAT_TYPE)
        sdc = torch.zeros(5, dtype=FLOAT_TYPE) # sd coefficients
        wac = torch.zeros(2, dtype=FLOAT_TYPE) # WeightedAverage coefficients
        avgPrice = torch.tensor(0.0, dtype=FLOAT_TYPE)

        for i in range(len(self.candles)):
            if i >= self.MA_SIZE:
                self.ma[i - self.MA_SIZE] = avgPrice / normalisationFactor
                avgPrice -= 0.95 * (100 - 1) * self.candles[i - 100]
            avgPrice = avgPrice * 0.95 + self.candles[i]

        for i in range(self.MA_SIZE-1, -1, -1):
            sdc.add(torch.tensor([
                self.power1 ** i * self.candles[i] ** 2,
                self.power1 ** i * self.candles[i],
                self.power2 ** i * self.candles[i],
                self.power1 ** i,
                self.power2 ** i
            ]))
            wac.add(torch.tensor([torch.pow(self.candles[self.MA_SIZE - i - 1], self.wAvgSize + 1), torch.pow(self.candles[self.MA_SIZE - i - 1], self.wAvgSize)]))

        for i in range(len(self.candles) - self.MA_SIZE):
            self.sd[i] = sdc[0] - 2 / sdc[1] * sdc[2] * sdc[4] + sdc[3] / (torch.square_(sdc[4]) * torch.square_(sdc[2]))
            sdc[0] = self.power1 * sdc[0] - self.power1 ** self.MA_SIZE * torch.square_(self.candles[i]) + torch.square_(self.candles[i + self.MA_SIZE])
            sdc[1] = self.power1 * sdc[1] - self.power1 ** self.MA_SIZE * self.candles[i] + self.candles[i + self.MA_SIZE]
            sdc[2] = self.power2 * sdc[2] - self.power2 ** self.MA_SIZE * self.candles[i] + self.candles[i + self.MA_SIZE]
            self.avg[i] = wac[0] / wac[1]
            wac.add(torch.tensor([
                torch.pow(self.candles[i + self.MA_SIZE], self.wAvgSize+1) - torch.pow(self.candles[i-1], self.wAvgSize+1),
                torch.pow(self.candles[i + self.MA_SIZE], self.wAvgSize) - torch.pow(self.candles[i-1], self.wAvgSize)
            ]))
        
        torch.sqrt(self.sd)
        torch.div(self.sd, sdc[3], out=self.sd)

        self.bb = torch.add(self.ma, torch.mul(self.sd, -self.buyingBollinger))

        # buyIndexes
        return [i for i in range(self.wAvgSize + self.MA_SIZE, len(self.candles) - 2) if ((self.sd[i - self.MA_SIZE] > self.avg[i - self.wAvgSize - self.MA_SIZE + 1] and self.sd[i - self.MA_SIZE - 1] < self.avg[i - self.avg - self.wAvgSize] and self.trend(self.candles[i - self.wAvgSize + 1:i + 1], 1 / 2) == -1 and self.candles[i] < self.bb[i - self.wAvgSize]))]


    def batchSellingEvaluation(self, buyIndexes, percentage_traded):
        profit = torch.tensor(1.0)

        bb2 = torch.add(self.ma, torch.mul(self.sd, self.buyingBollinger))
        unclosed_trades = 0

        for index in buyIndexes:
            has_passed_under_0 = False 
            for j in range(index, len(self.candles)):
                if self.candles[j] > self.bb[j]:
                    has_passed_under_0 = True
                if (j - self.wAvgSize > 0 and self.sd[j] < self.avg[j - self.wAvgSize] and self.sd[j - 1] > self.avg[j - self.wAvgSize - 1]) or (has_passed_under_0 and self.candles[j] > bb2[j]):
                    break

            if j == len(self.candles) - 1:
                unclosed_trades += 1

            torch.add_(profit * percentage_traded * (self.candles[j] / self.candles[index] - 1) - 0.0008)

        print(unclosed_trades)

        return profit



SAMPLE_SIZE = 2000
LAUNCH_SAMPLE_SIZE = 2104

NB_POINTS_TESTES = 2
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
bounds = INSTANCES_BOUNDS
best_params = {}
st = time.time()

for cc in range(len(coinCodes)):
    s[cc] = Strategy()
    s[cc].candles = data[cc]
    for recursion in range(NB_RECURSIONS):

        best_yield = -100
        for p1 in torch.linspace(bounds["power1"][0], bounds["power1"][1], NB_POINTS_TESTES):
            for p2 in torch.linspace(bounds["power2"][0], bounds["power2"][1], NB_POINTS_TESTES):
                for bb in torch.linspace(bounds["buyingBollinger"][0], bounds["buyingBollinger"][1], NB_POINTS_TESTES):
                    for sb1 in torch.linspace(bounds["sellingBollinger1"][0], bounds["sellingBollinger1"][1], NB_POINTS_TESTES):
                        for sb2 in torch.linspace(bounds["sellingBollinger2"][0], bounds["sellingBollinger2"][1], NB_POINTS_TESTES):

                            s[cc].modifyParams(p1.item(), p2.item(), bb.item(), sb1.item(), sb2.item())
                            buyIndexes = s[cc].batchBuyingEvaluation()
                            profit = s[cc].batchSellingEvaluation(buyIndexes, PERCENTAGE_TRADED)

                            if profit > best_yield:
                                best_params = {"power1": p1.item(), "power2": p2.item(), "buyingBollinger": bb.item(), "sellingBollinger1" : sb1.item(), "sellingBollinger2": sb2.item()}
                                best_yield = profit
        
        for param in best_params:
            bounds[param][0] = best_params[param] - REDUCTION_PAR_ETAPE * (bounds[param][1] - bounds[param][0])
            if param in ["power1", "power2"]:
                bounds[param][1] = min(1, best_params[param] + REDUCTION_PAR_ETAPE) * (bounds[param][1] - bounds[param][0])
            else:
                bounds[param][1] = best_params[param] + REDUCTION_PAR_ETAPE * (bounds[param][1] - bounds[param][0])
    
    print(f"The best params for {coinCodes[cc]} are:\n{str(best_params)}\nyield: {profit}\nCalculation time: {time.time() - st}")



 # regarder sur nvtop si les calculs se font pas mal sur la cg
 # sinon, plusieurs options pour forcer les calculs sur la cg (ex : ajouter .cuda entre tous les tensors)
 # Tensor.is_cuda   Is True if the Tensor is stored on the GPU, False otherwise.
 # ajouter un underscore à la plupart des fonctions de calcul permet de les mettre en "in-place" -> plus opti en temps et (surtout) en mémoire