from wallet import Wallet, ping_test
from api_keys import Keys
import asyncio, time
    
    
async def main():
    k = Keys()
    w = Wallet(k.access_key, k.secret_key, k.passphrase, True)

    if not ping_test():
        print("erreur")
        return;

    await w.connect()
    
    w.market_mode('spot')
    
    """
    price = await w.getPrice("BTC/USDT")
    print(price)
    
    for i in range(10): # Si le résultat est négatif (< 20), c'est que le BTC est entrain de baisser et inversement
        amount = await w.currency_equivalence("BTC/EUR", 20)
        print(amount)
        currency = await w.crypto_equivalence("BTC/EUR", amount)
        print(currency)
        time.sleep(1)
    """
    
    #await w.walletInformations()
    
    await w.watchPositions("BTC/EUR")
    
    await w.disconnect()
    

if __name__ == "__main__":
    asyncio.run(main())