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
    
    await w.walletInformations()
    
    #await w.buy("SBTC/SUSD:SUSDC", 0.002)
    
    #await w.exchange.watch_positions("BTC/EUR")
    #positions = await w.exchange.fetch_positions()
    #print(positions)
    
    #await w.transactionHistory("BTC/EUR")
    
    #await w.sell_percentage("BTC/EUR", 100)
    
    await w.disconnect()
    

if __name__ == "__main__":
    asyncio.run(main())



"""
w.market_mode('spot')

price = await w.getPrice("BTC/USDT")
print(price)

for i in range(10): # Si le résultat est négatif (< 20), c'est que le BTC est entrain de baisser et inversement
    amount = await w.actual_currency_equivalence("BTC/EUR", 20)
    print(amount)
    currency = await w.actual_crypto_equivalence("BTC/EUR", amount)
    print(currency)
    time.sleep(1)

await w.walletInformations()

await w.orderBook("BTC/EUR")

#await w.place_order("BTC/EUR", 'buy', await w.actual_currency_equivalence("BTC/EUR", 5), 59000)
"""