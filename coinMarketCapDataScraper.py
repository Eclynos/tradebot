from tools import *
import threading

def testWorth(key, t):
    print(key, " : ", t.isWorthBuying(key, 50000))

if __name__ == "__main__":
    codeToIDDico = {}
    with open('./codeToID.json','r') as json_File :
        codeToIDDico=json.load(json_File)

    numberOfCryptos = len(list(codeToIDDico.keys()))

    t = Tools(codeToIDDico)
    threadList = []

    for k in codeToIDDico.keys():
        threadList.append(threading.Thread(target=testWorth, args=(k,t)))

    for i in range(numberOfCryptos):
        threadList[i].start()

    # print(t.getRealMins(t.getMathLocalyMins(t.getCoinData("ETH", "7D"), "7D"), 50000))
    # print(t.isInDrop("KAS", "7D", 50000))
    # print(t.isWorthBuying("SOL", 50000))
    # print(t.getCoinData("KAS", "7D"))
    # print(t.getMathLocalMins(t.getCoinData("KAS", "7D")))
    # print(t.getRealMins(t.getCoinData("KAS", "7D"), 50000))