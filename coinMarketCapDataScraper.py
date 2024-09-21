from tools import *

if __name__ == "__main__":
    t = Tools()

    codeToIDDico = {}
    with open('./codeToID.json','r') as json_File :
        codeToIDDico=json.load(json_File)

    for k in codeToIDDico.keys():
        print(k, " : ", t.isWorthBuying(k, 50000))

    # print(t.getRealMins(t.getMathLocalMins(t.getCoinData("ETH", "7D"), "7D"), 50000))
    # print(t.isInDrop("KAS", "7D", 50000))
    # print(t.isWorthBuying("SOL", 50000))
    # print(t.getCoinData("KAS", "7D"))
    # print(t.getMathLocalMins(t.getCoinData("KAS", "7D")))
    # print(t.getRealMins(t.getCoinData("KAS", "7D"), 50000))