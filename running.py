from marketInfo import MarketInformations
from wallet import Wallet
from tools import *
import asyncio, time, datetime


async def main():
    symbols = read_symbols()
    mi = MarketInformations()
    w = Wallet("keys_nathael", False, mi)
    
    if not ping_test():
        print("erreur")
        return

    await mi.init()
    #await w.init()

    await mi.chart_visualisation("RENDER/USDT", "1m", time_frame_to_ms("2h"), 3)

    await mi.account.disconnect()
    #await w.account.disconnect()


if __name__ == "__main__":
    asyncio.run(main())

# tester les mins de trading swap en changeant les paramètres