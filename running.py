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
    
    if not t.ping_test():
        print("erreur")
        return;
    
    w.market_mode('spot')
    
    #await w.sell("SOL/USDT", await mi.actual_currency_equivalence("SOL/USDT", 2))
    
    await w.walletInformations()
    
    #price = await mi.getPrice("HNT/USDT") * 1.03
    
    #await w.place_order("HNT/USDT", 'buy', await mi.actual_currency_equivalence("HNT/USDT", 2), price, price * 0.98, price * 1.02)

    #await w.walletInformations()
    
    
    await w.account.disconnect()
    await mi.account.disconnect()
    

if __name__ == "__main__":
    asyncio.run(main())









"""
Continuer à améliorer gestion des ordres
Trouver un moyen de tracer la courbe des derniers temps en récupérant les dernières bougies

https://stackoverflow.com/questions/70568934/create-contract-order-with-take-profit-and-stop-loss-with-ccxt
"""