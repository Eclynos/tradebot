from marketInfo import MarketInformations
from wallet import Wallet
from tools import *
import asyncio, time, datetime, json


async def main():
    symbols = read_symbols()
    mi = MarketInformations()
    w = Wallet("keys_nathael", False, mi)
    
    if not ping_test():
        print("erreur")
        return

    await mi.init()
    await w.init()


    with open('liste.json', 'r+') as f:
        data = json.load(f)
        f.seek(0)
        if not 'liste' in data:
            data['liste'] = []
        price = await mi.getPrice("POPCAT/USDT")
        data['liste'].append(price)
        price = await mi.getPrice("BTC/USDT")
        data['liste'].append(price)
        price = await mi.getPrice("SOL/USDT")
        data['liste'].append(price)
        json.dump(data, f)


    await mi.account.disconnect()
    await w.account.disconnect()


if __name__ == "__main__":
    asyncio.run(main())


# await mi.chart_visualisation("RENDER/USDT", "1m", time_frame_to_ms("2h"), 3)