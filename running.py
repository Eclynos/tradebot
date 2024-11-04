from marketInfo import MarketInformations
from wallet import Wallet
from tools import time_frame_to_ms,  ping_test
import asyncio


async def main():
    mi = MarketInformations()
    w = Wallet("keys_nathael", False, mi)
    
    if not ping_test():
        print("erreur")
        return;

    #await w.init()
    await mi.init()

    candles = await mi.fetch_candles_amount("SOL/USDT", "1m", 2)
    print(await mi.exchange.fetch_time())
    print(candles[1][0])

    #await w.account.disconnect()
    await mi.account.disconnect()


if __name__ == "__main__":
    asyncio.run(main())