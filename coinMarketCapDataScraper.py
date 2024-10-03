from tools import *
import threading
import time

def testWorth(key, t, l):
    isWorth = t.isWorthBuying(key, 50000)
    if isWorth[0]:
        l.append(key)
    elif isWorth[1] == 1:
        l.append("!") # caractère spécial pour indiquer que le bot est flag comme DDOS

def showWorthCoins(codeToIDDico):
    numberOfCryptos = len(list(codeToIDDico.keys()))
    blockSize = 5
    threadList = []
    interestingCoins = []
    for k in codeToIDDico.keys():
        threadList.append(threading.Thread(target=testWorth, args=(k, t, interestingCoins)))


    for i in range(500): # on teste que sur les 1000 plus grosses cryptos
        threadList[i].start()

        
        if i%blockSize == 0:
            time.sleep(1)
            isFlagged = False
            for j in range(len(interestingCoins)-1, max(len(interestingCoins) - blockSize, 0)-1, -1):
                if interestingCoins[j] == "!":
                    interestingCoins.pop(j)
                    isFlagged = True

            if isFlagged:
                time.sleep(30)

            print(interestingCoins)


if __name__ == "__main__":
    codeToIDDico = {}
    with open('./data/codeToID.json','r') as json_File :
        codeToIDDico=json.load(json_File)

    t = Tools(codeToIDDico)

    data = t.getCoinData("ethereum", "7D")
    print(t.movingAverage(data, 20))
    # print(t.nthDegreeRegression(data, 2))



