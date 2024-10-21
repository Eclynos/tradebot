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

    await mi.chart_visualisation("BTC/USDT", "1m", t.time_frame_to_ms("1h"), 1)

    #await w.account.disconnect()
    await mi.account.disconnect()


if __name__ == "__main__":
    asyncio.run(main())