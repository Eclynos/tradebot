from manager import Manager
from strategyStandardDevPump import Strategy
from tools import *
from math import floor
import asyncio, time, json

with open('settings.json', 'r') as f:
    settings = json.load(f)
    
async def main():
    symbols = read_symbols()
    keys = ["date", "open", "high", "low", "price", "volume"]
    m = Manager(symbols, settings)

    if not ping_test():
        print("erreur")
        return
    
    symbol = "BGB/USDT"

    await m.start()

    positions = await m.wallets["nathael"].exchange.fetch_position_history(
        symbol=symbol+':USDT',
        limit=5
    )

    print(positions)

    await m.end()
    

if __name__ == "__main__":
    asyncio.run(main())