from wallet import Wallet, ping_test
from api_keys import Keys
import asyncio
    
    
async def main():
    k = Keys()
    w = Wallet(k.access_key, k.secret_key, k.passphrase, True)

    if not ping_test():
        print("erreur")
        return;

    await w.connect()
    
    w.market_mode('spot')
    
    # await w.buy('BTC/EUR', amount)
    
    price = await w.getPrice("BTC", "USD")
    print(price)

    await w.disconnect()

if __name__ == "__main__":
    asyncio.run(main())