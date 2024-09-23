from tools import *
import threading
import time

def testWorth(key, t, l):
    isWorth = t.isWorthBuying(key, 50000)
    if isWorth[0]:
        l.append(key)
    elif isWorth[1] == 1:
        l.append("!") # caractère spécial pour indiquer que le bot est flag comme DDOS

if __name__ == "__main__":
    codeToIDDico = {}
    with open('./codeToID.json','r') as json_File :
        codeToIDDico=json.load(json_File)

    numberOfCryptos = len(list(codeToIDDico.keys()))
    blockSize = 5

    t = Tools(codeToIDDico)
    threadList = []
    interestingCoins = []
    # print(t.minDepth(t.getCoinData("ethereum", "7D"), 50000))

    # print(t.getCoinData("bitcoin", "7D"))
    # print(t.nthDegreeRegression(t.getCoinData("ethereum", "7D"), 2))


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
