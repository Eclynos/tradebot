from wallet import Wallet
from marketInfo import MarketInformations
from tools import Tools
import asyncio, time


async def main():
    t = Tools()
    mi = MarketInformations(t)
    #w = Wallet("keys_nathael", False, mi)
    
    """
    if not t.ping_test():
        print("erreur")
        return;
    """

    #await w.init()
    #w.market_mode("future")
    await mi.init()

    await mi.candlestick_visualisation("BTC/USDT", "5m", t.time_frame_to_ms("5h"))

    #await w.account.disconnect()
    await mi.account.disconnect()


if __name__ == "__main__":
    asyncio.run(main())





"""
Trouver le moyen de faire des shorts -> ou au moins de faire des futures
Trouver un moyen de tracer la courbe des derniers temps en récupérant les dernières bougies
lier les stratégies pour pouvoir les tester (sur la courbe + rendement) sur les dernières bougies récupérées
Gérer les contrats futures pour diminuer les frais de transactions
https://stackoverflow.com/questions/70568934/create-contract-order-with-take-profit-and-stop-loss-with-ccxt
"""