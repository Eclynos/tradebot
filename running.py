from wallet import Wallet
from marketInfo import MarketInformations
from tools import Tools
import asyncio, time, requests
    
    
async def main():
    t = Tools()
    mi = MarketInformations()
    w = Wallet("keys", False, mi)


    if not t.ping_test():
        print("erreur")
        return;


    await w.init()
    await mi.init()

    await w.transactionHistory("BTC/USDT")
    
    await w.account.disconnect()
    await mi.account.disconnect()
    

if __name__ == "__main__":
    asyncio.run(main())









"""
Continuer à améliorer gestion des ordres

https://stackoverflow.com/questions/70568934/create-contract-order-with-take-profit-and-stop-loss-with-ccxt
"""