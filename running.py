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
    await w.init()

    balance = await w.exchange.fetch_balance()
    free = await w.exchange.fetch_free_balance()
    total = await w.exchange.fetch_total_balance()
    used = await w.exchange.fetch_used_balance()
    print(float(balance['info'][0]['crossedMaxAvailable']))
    print(free)
    print(total)
    print(used)
    print(total['USDT'] - used['USDT'])
    print(total['USDT'] - float(balance['info'][0]['crossedMaxAvailable']))

    await mi.account.disconnect()
    await w.account.disconnect()


if __name__ == "__main__":
    asyncio.run(main())


# await mi.chart_visualisation("RENDER/USDT", "1m", time_frame_to_ms("2h"), 3)


# fetch_free_balance() donne le coût restant de toutes les cryptos -> super pratique
# pareil pour total_balance
# regarder used_balance aussi