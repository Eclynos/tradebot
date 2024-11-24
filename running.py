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

    symbol = "HNT/USDT"

    """
    order = await w.buy(symbol, 0.9, 2)
    print(order)

    time.sleep(7)
    """

    order = await w.sell_full(symbol)
    print(order)

    await mi.account.disconnect()
    await w.account.disconnect()


if __name__ == "__main__":
    asyncio.run(main())

# await mi.chart_visualisation("RENDER/USDT", "1m", time_frame_to_ms("2h"), 3)