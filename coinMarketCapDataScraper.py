from tools import *
import threading
import time

def testWorth(key, t, l):
    if t.isWorthBuying(key, 50000):
        l.append(key)

if __name__ == "__main__":
    codeToIDDico = {}
    with open('./codeToID.json','r') as json_File :
        codeToIDDico=json.load(json_File)

    numberOfCryptos = len(list(codeToIDDico.keys()))

    t = Tools(codeToIDDico)
    threadList = []
    interestingCoins = []

    for k in codeToIDDico.keys():
        threadList.append(threading.Thread(target=testWorth, args=(k, t, interestingCoins)))



    for i in range(1000): # on teste que sur les 1000 plus grosses cryptos
        threadList[i].start()
        if i%5 == 0:
            time.sleep(1)

            print(interestingCoins)
            

    # print(t.getRealMins(t.getMathLocalyMins(t.getCoinData("ETH", "7D"), "7D"), 50000))
    # print(t.isInDrop("KAS", "7D", 50000))
    # print(t.isWorthBuying("SOL", 50000))
    # print(t.getCoinData("KAS", "7D"))
    # print(t.getMathLocalMins(t.getCoinData("KAS", "7D")))
    # print(t.getRealMins(t.getCoinData("KAS", "7D"), 50000))