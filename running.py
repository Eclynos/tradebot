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

    symbol = "BTC/USDT:USDT"

    #print(await mi.actual_currency_equivalence(symbol, 2))

    #order = await w.buy_and_transfer(symbol, await mi.actual_currency_equivalence(symbol, 2), 2)
    #print(order)

    #await w.checkPositions()

    #order = await w.closep(symbol)
    #print(order)

    #time.sleep(7)

    #order = await w.exchange.close_position(symbol, "long", params={'type': 'swap'})
    #print(order)

    rate = await w.exchange.fetch_used_balance()
    print(rate)

    await mi.account.disconnect()
    await w.account.disconnect()


if __name__ == "__main__":
    asyncio.run(main())


# await mi.chart_visualisation("RENDER/USDT", "1m", time_frame_to_ms("2h"), 3)


# fetch_free_balance() donne le coût restant de toutes les cryptos -> super pratique
# pareil pour total_balance
# regarder used_balance aussi