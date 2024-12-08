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

    min_amounts = {}

    await mi.exchange.load_markets()
    for symbol in symbols:
        market = mi.exchange.market(symbol + ':USDT')
        min_amounts[symbol] = market['limits']['amount']['min']
        """
        if await mi.actual_crypto_equivalence(symbol, market['limits']['amount']['min']) > 6:
            min_amounts[symbol] = market['limits']['amount']['min']
        else:
            min_amounts[symbol] = 0
        """

    print(min_amounts)

    await mi.account.disconnect()
    await w.account.disconnect()


if __name__ == "__main__":
    asyncio.run(main())


# await mi.chart_visualisation("RENDER/USDT", "1m", time_frame_to_ms("2h"), 3)