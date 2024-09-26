from wallet import Wallet
from api_keys import Keys
import asyncio
import time
    
async def main():
    k = Keys()
    w = Wallet(k.access_key, k.secret_key, k.passphrase)
    
    await w.connect()
    
    positions = await w.watchAllPositions()
    print(positions)
    
    await w.disconnect()

if __name__ == "__main__":
    asyncio.run(main())