import requests
import json
import time
import numpy
import ccxt

class Tools:
    def __init__(self, IDDico) -> None:
        self.codeToIDDico = IDDico

    def getCoinData(self, coinCode : str, timeFrame : str) -> list:

        if timeFrame not in ("1D", "7D", "1M", "1Y", "All"):
            print("Invalid Time Frame")
            return {}

        r = requests.get(f'https://api.coinmarketcap.com/data-api/v3/cryptocurrency/detail/chart?id={self.codeToIDDico[coinCode]}&range={timeFrame}')
        try:
            r = r.json()
        except:
            return []
        
        r = r["data"]
        if "points" not in r.keys():
            print(f"ERROR [{coinCode}] :", r)
        r = r["points"]
        l = []
        for k in r.keys():
            l.append({"key" : k, "price" : r[k]["v"][0], "volume" : r[k]["v"][1], "mc" : r[k]["v"][2]})

        l.sort(key= lambda item : int(item["key"])) #normalement pas nécessaire mais on sait jamais

        return l
    
    def getMathLocalMins(self, baseList : list) -> list:
        """Determine les minimums locaux de la chart : valeur précédent > valeur actuelle < valeur suivante"""
        returnList = []

        for k in range(len(baseList)):
            try:
                if baseList[k]["price"] < baseList[k+1]["price"] and baseList[k]["price"] < baseList[k-1]["price"]:
                    returnList.append({"key": baseList[k]["key"], "price" : baseList[k]["price"]})
                    k += 1
            except:
                returnList.append({"key": baseList[k]["key"] , "price" : baseList[k]["price"] })
        return returnList 

    def getRealMins(self, baseList : list, minFrame : int) -> list:
        """Détermine les retracements à partir de la liste des minimums locaux"""
        returnList = []

        for i in range(len(baseList)):
            isMin = True
            for j in range(len(baseList)):
                if abs(int(baseList[i]["key"]) - int(baseList[j]["key"])) < minFrame and baseList[i]["price"] > baseList[j]["price"]:
                    isMin = False
                    break
            
            if isMin:
                returnList.append(baseList[i])
        
        return returnList

    def minDepth(self, baseDict, minFrame):
        """Détermine les vrais dip à partir de la liste des retracements"""
        totalMins = self.getMathLocalMins(baseDict)
        interestingMins = self.getRealMins(totalMins, minFrame)
        minList = []

        for x in interestingMins:
            dropMax = 0
            for y in totalMins:
                if int(x["key"]) - int(y["key"]) > 0 and int(x["key"]) - int(y["key"]) < minFrame and dropMax < 1-x["price"]/y["price"]:
                    dropMax = 1 - x["price"] / y["price"]

            minList.append({"key" : x["key"], "price" : x["price"], "drop" : dropMax})
        return minList

    def average(self, dataList):
        total = 0
        numberOfEntries = len(dataList)
        for i in range(numberOfEntries):
            total += float(dataList[i]["price"])
        
        return total/numberOfEntries
    
    def nthDegreeRegression(self, dataList, degree):
        # Extrapolation des calculcs matriciels trouvés ici :
        # https://www.varsitytutors.com/hotmath/hotmath_help/topics/quadratic-regression

        numberOfEntries = len(dataList)

        minX = int(dataList[0]["key"])
        
        A = []
        for _ in range(degree +1):
            A.append([0 for __ in range(degree+1)])
        
        B = [0 for _ in range(degree +1)]

        for i in range(numberOfEntries):
            for l in range(degree + 1):
                for c in range(l, degree + 1):
                    A[l][c] += (int(dataList[i]["key"])-minX)**(2 * degree - l - c)
        
        for l in range(degree + 1):
            for c in range(l):
                A[l][c] = A[c][l]

        for i in range(degree + 1):
            for j in range(degree + 1):
                A[i][j] = float(A[i][j])

        for i in range(numberOfEntries):
            for l in range(degree+1):
                B[l] += (int(dataList[i]["key"]) - minX)**(degree - l) * float(dataList[i]["price"])

        X = numpy.linalg.solve(A,B)
        return X


    def isWorthBuying(self, coinCode, minFrame):
        weeklyTotalCoinData = self.getCoinData(coinCode, "7D")
        if len(weeklyTotalCoinData) == 0: # Si ça a buggué
            print(f"BUG (Weekly) {coinCode} \t")
            return (False, 1)
        
        drops = self.minDepth(weeklyTotalCoinData, minFrame)
        lastDrop = drops[-1]
        
        minDropPourcentage = 0.05
        releventTimeFrame=900 
        maxDescentPourcentage=0.02
        maxFreefallPourcentage = 0.04


        if time.time()-int(lastDrop["key"]) > releventTimeFrame: # drop trop vieux
            return (False, 0)
        if lastDrop["drop"] < minDropPourcentage: # drop pas assez important
            return (False, 0)     
               
        dailyTotalCoinData = self.getCoinData(coinCode, "1D")
        if len(dailyTotalCoinData) == 0: # Si ça a buggué
            print(f"BUG (Daily) {coinCode} \t")
            return (False, 1)
        dailyAvgPrice = self.average(dailyTotalCoinData)
        weeklyAvgPrice = self.average(weeklyTotalCoinData)

        if (weeklyAvgPrice - dailyAvgPrice) / weeklyAvgPrice > maxDescentPourcentage: # si la crypto descend trop en général (on peut considérer qu'elle s'effondre)
            return (False, 0)
        
        
        if (float(weeklyTotalCoinData[-2]["price"])-float(weeklyTotalCoinData[-1]["price"])) / float(weeklyTotalCoinData[-2]["price"]) > maxFreefallPourcentage: 
            #si la crypto est en chute libre (en si elle descend à la verticale)
            return (False, 0)
        
        if (float(weeklyTotalCoinData[-3]["price"])-float(weeklyTotalCoinData[-1]["price"])) / float(weeklyTotalCoinData[-3]["price"]) > maxFreefallPourcentage: 
            #même test sur l'index d'avant juste pour être safe
            return (False, 0)
        
        return (True, 0)


  
class Wallet:
    def __init__(self, access_key, secret_key, passphrase) -> None:
        self.access_key = access_key
        self.secret_key = secret_key
        self.passphrase = passphrase
        self.exchange = ccxt.bitget({ # etablie la connexion au compte
        'apiKey': access_key,
        'secret': secret_key,
        'password': passphrase,
        })
        self.exchange.set_sandbox_mode(True) # Le mode sandbox permet de tester des stratégies de trading ou d'effectuer des opérations fictives dans un environnement de simulation sans engager de fonds réels. À utiliser pour tester l'api
        balance = self.exchange.fetch_balance() # effectuer les opérations dans l'environnement test (sandbox)
        self.exchange.verbose = True # pour le debug
        
    async def place_order(self, coinCode, BuyorSell, amount, price):
        await self.exchange.load_markets() # met en cache toutes les informations sur les paires de trading disponibles avant d'effectuer des opérations de trading
        orders = await self.exchange.create_orders({
                'symbol': ''+'/USDT:USDT', # trouver quelque chose pour remplir les symboles, le but est d'obtenir par exemple : 'ETH/USDT:USDT'
                'type': 'limit',
                'side': BuyorSell,
                'amount': amount,
                'price': price,
            })
        print(orders)
    
    async def buy(self, coinCode, amount):
        await self.exchange.load_markets() # met en cache toutes les informations sur les paires de trading disponibles avant d'effectuer des opérations de trading
        orders = await self.exchange.create_orders({
                'symbol': ''+'/USDT:USDT', # trouver quelque chose pour remplir les symboles, le but est d'obtenir par exemple : 'ETH/USDT:USDT'
                'type': 'market',
                'side': 'buy',
                'amount': amount,
            })
        print(orders)
    
    async def sell(self, coinCode, amount): # on pourra faire en sorte de sell un pourcentage et pas un amount
        await self.exchange.load_markets() # met en cache toutes les informations sur les paires de trading disponibles avant d'effectuer des opérations de trading
        orders = await self.exchange.create_orders({
            'symbol': ''+'/USDT:USDT', # trouver quelque chose pour remplir les symboles, le but est d'obtenir par exemple : 'ETH/USDT:USDT'
            'type': 'market',
            'side': 'sell',
            'amount': amount,
        })
        print(orders)
        
    def disconnect(self): # à faire à la fin de l'utilisation, à la fin du code
        self.exchange.close()