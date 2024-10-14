from wallet import Wallet
from marketInfo import MarketInformations
from tools import Tools
import asyncio, time
    
    
async def main():
    run = True
    t = Tools()
    mi = MarketInformations()
    w = [Wallet("keys", False, mi)]

    if not t.ping_test():
        print("erreur")
        return;

    await w[0].init()
    await mi.init()
    
    nb = 0
    
    while run:
        candles =  await mi.fetch_candles("BTC/USDT", "1m", t.time_frame_to_ms("2m"))
        for candle in candles:
            print(candle[0] + "\n" + candle[1])
        nb += 1
        time.sleep(1)
        if nb > 2:
            run = False
        
    if not run:
        for wallet in w:
            await wallet.check_positions()
            
    await w[0].sell_all()
    
    await w[0].account.disconnect()
    await mi.account.disconnect()
    

if __name__ == "__main__":
    asyncio.run(main())