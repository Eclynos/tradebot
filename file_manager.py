from wallet import Wallet, ping_test
from tools import Tools
from api_keys import Keys
import asyncio, json, time
    
    
async def main():
    k = Keys()
    codeToIDDico = {}
    with open('./data/codeToID.json','r') as json_File:
        codeToIDDico=json.load(json_File)

    t = Tools(codeToIDDico)
    w = Wallet(k.access_key, k.secret_key, k.passphrase, False)

    start_time = time.time()
    
    await w.connect()
    
    w.market_mode('spot')

    await t.fetch_candles(w.exchange, "BTC/EUR", "15m", 1209600000)
    
    await w.disconnect()

    print(time.time() - start_time)

    
if __name__ == "__main__":
    asyncio.run(main())