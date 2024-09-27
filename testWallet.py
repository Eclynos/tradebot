from wallet import Wallet
from api_keys import Keys
import asyncio
import time
    
    
async def main():
    k = Keys()
    w = Wallet(k.access_key, k.secret_key, k.passphrase)
    
    await w.connect()
    
    positions = await w.check_positions()
    
    await w.buy("BTC", 0.005)
    
    positions = await w.check_positions()
    
    await w.disconnect()

if __name__ == "__main__":
    asyncio.run(main())