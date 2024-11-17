from marketInfo import MarketInformations
from wallet import Wallet
from tools import time_frame_to_ms,  ping_test, wait_next_frame, read_symbols
import asyncio, time


async def main():
    symbols = read_symbols()
    mi = MarketInformations()
    
    if not ping_test():
        print("erreur")
        return;

    await mi.init()

    #await mi.chart_visualisation("RENDER/USDT", "15m", time_frame_to_ms("12h"), 2)

    print((time.time()//60) % (120))

    """
    await mi.exchange.load_markets()

    for symbol in symbols:
        market = mi.exchange.market(symbol + ':USDT')
        print(symbol)
        print(market['limits']['amount']['min'])
        print(await mi.actual_crypto_equivalence(symbol, market['limits']['amount']['min']))
        print(market['limits']['cost']['min'])
    """

    await mi.account.disconnect()


if __name__ == "__main__":
    asyncio.run(main())

# tester les mins de trading swap en changeant les paramètres