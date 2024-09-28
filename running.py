from wallet import Wallet, ping_test
from api_keys import Keys
import asyncio
    
    
async def main():
    k = Keys()
    w = Wallet(k.access_key, k.secret_key, k.passphrase, False)

    if not ping_test():
        print("erreur")
        return;

    await w.connect()
    
    w.market_mode('spot')
    
    w.getPrice("BTC", "EUR")

    await w.disconnect()

if __name__ == "__main__":
    asyncio.run(main())

















"""
import aiofiles
async with aiofiles.open('symbolsID', 'w') as fichier:
    for symbol in reversed(symbols):
        await fichier.write(symbol + "\n")
"""