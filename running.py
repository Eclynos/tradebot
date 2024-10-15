from wallet import Wallet
from marketInfo import MarketInformations
from tools import Tools
import asyncio, time
    
    
async def main():
    t = Tools()
    mi = MarketInformations()
    w = Wallet("keys_nathael", False, mi)
    
    if not t.ping_test():
        print("erreur")
        return;
    

    await w.init()
    await mi.init()
    
    """
    await w.walletInformations()
    
    symbol = "BTC/USDT"
    amount = await mi.actual_currency_equivalence(symbol, 2)
    await w.shortOrder(symbol, amount)
    """
    
    await w.sell_all()
    
    await w.account.disconnect()
    await mi.account.disconnect()
    

if __name__ == "__main__":
    asyncio.run(main())







"""
Trouver le moyen de faire des shorts
Trouver un moyen de tracer la courbe des derniers temps en récupérant les dernières bougies
Gérer les contrats futures pour diminuer les frais de transactions
"""