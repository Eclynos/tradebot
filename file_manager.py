from wallet import Wallet, ping_test
from api_keys import Keys
import asyncio, time
    
    
async def main():
    k = Keys()
    w = Wallet(k.access_key, k.secret_key, k.passphrase, False)

    if not ping_test():
        print("erreur")
        return;
    
    await w.connect()
    
    w.market_mode('spot')
    
    timestamp = await w.exchange.fetch_time()
    nb_hours = 1
    hours_ago = timestamp - int(nb_hours * 3600 * 1000)
    
    candle_list = await w.exchange.fetch_ohlcv("BTC/EUR", '1h', hours_ago, 1000)
    print(len(candle_list))
    
    
    await w.disconnect()


    
if __name__ == "__main__":
    asyncio.run(main())