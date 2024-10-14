from wallet import Wallet
from marketInfo import MarketInformations
from tools import Tools
import asyncio, time
    
    
async def main():
    t = Tools()
    mi = MarketInformations()
    w = Wallet("keys", False, mi)

    """
    if not t.ping_test():
        print("erreur")
        return;
    """

    await w.init()
    await mi.init()

    await w.walletInformations()

    symbol = "SOL/USDT"
    amount = await mi.actual_currency_equivalence(symbol, 3.5)
    #print(amount)
    
    order = await w.sell_all()
    print(order)

    
    await w.walletInformations()
    #time.sleep(13)

    #order = await w.buy(symbol, amount, 3.5)
    #print(order)
    
    #await w.cancel_all_orders("BTC/USDT")
    
    #time.sleep(3)

    #await w.walletInformations()
    
    await w.account.disconnect()
    await mi.account.disconnect()
    

if __name__ == "__main__":
    asyncio.run(main())







"""
Continuer à améliorer gestion des ordres
Trouver un moyen de tracer la courbe des derniers temps en récupérant les dernières bougies
Gérer les contrats futures pour diminuer les frais de transactions

faire une class de gestion de toutes les class pour faciliter les actions
ex: m.buy() fait acheter tous les wallets
on pourra facilement modifier les paramètres pour modifier la crypto, les montants etc
"""