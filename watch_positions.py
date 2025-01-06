from manager import Manager
from tools import read_symbols, ping_test
import asyncio, time, json

with open('settings.json', 'r') as f:
    settings = json.load(f)

async def main():

    symbols = read_symbols()
    if not ping_test():
        print("Not connected to internet")
        return

    m = Manager(symbols, settings)

    await m.start()

    print(await m.wallets["nicolas"].exchange.fetch_positions())
    
    await m.end()
    

if __name__ == "__main__":
    asyncio.run(main())