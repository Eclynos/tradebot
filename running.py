from marketInfo import MarketInformations
from wallet import Wallet
from tools import Tools
import asyncio


async def main():
    t = Tools()
    mi = MarketInformations(t)
    w = Wallet("keys_nathael", False, mi)
    
    if not t.ping_test():
        print("erreur")
        return;

    await w.init()
    await mi.init()

    #await mi.chart_visualisation("ETH/USDT", "1m", t.time_frame_to_ms("2h"), 2)
    #await mi.candlestick_visualisation("BTC/USDT", "15m", t.time_frame_to_ms("14h"))
    #candles = await mi.fetch_candles("SOL/USDT", '5m', t.time_frame_to_ms("14d"))
    #print(len(candles))
    
    balance = await w.exchange.fetch_balance()
    
    print(balance)
    print(balance['free'])
    

    await w.account.disconnect()
    await mi.account.disconnect()


if __name__ == "__main__":
    asyncio.run(main())