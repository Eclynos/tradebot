from wallet import Wallet
from marketInfo import MarketInformations
from decimal import Decimal
from tools import Tools
import asyncio, time
    
    
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
    
    
    #await w.sell("HNT/USDT", await mi.actual_currency_equivalence("HNT/USDT", 2))
    
    w.market_mode('spot')
    await w.walletInformations()
    w.market_mode('swap')
    
    price = await mi.getPrice("HNT/USDT") * 1.03
    amount = await mi.actual_currency_equivalence("HNT/USDT", 2)
    
    SL = price * 0.98; TP = price * 1.02
    
    await w.place_order("HNT/USDT", 'buy', amount, price, SL, TP)
    
    time.sleep(7)
    
    await w.cancel_all_orders("HNT/USDT")
    
    w.market_mode('spot')
    await w.walletInformations()
    
    await w.account.disconnect()
    await mi.account.disconnect()
    

if __name__ == "__main__":
    asyncio.run(main())









"""
create_limit_buy_order
Continuer à améliorer gestion des ordres
Trouver un moyen de tracer la courbe des derniers temps en récupérant les dernières bougies

https://stackoverflow.com/questions/70568934/create-contract-order-with-take-profit-and-stop-loss-with-ccxt
"""