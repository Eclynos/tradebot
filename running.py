from marketInfo import MarketInformations
from wallet import Wallet
from tools import time_frame_to_ms,  ping_test, wait_next_frame
import asyncio, time


async def main():
    mi = MarketInformations()
    w = Wallet("keys_nathael", False, mi)
    
    if not ping_test():
        print("erreur")
        return;

    #await w.init()
    await mi.init()

    print("yo")
    wait_next_frame(5)
    print("ok")
    #await mi.chart_visualisation("SOL/USDT", "15m", time_frame_to_ms("12h"), 2)

    #await w.account.disconnect()
    await mi.account.disconnect()


if __name__ == "__main__":
    asyncio.run(main())