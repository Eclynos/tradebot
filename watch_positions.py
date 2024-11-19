from executer import Executer
from tools import read_symbols
import asyncio
    
async def main():
    e = Executer(read_symbols())

    await e.start()

    #await e.positions()

    e.wallets[0].market_mode('swap')

    #e.buy_swap("SUI/USDT")

    #await e.wallets[0].walletInformations()

    #e.sell_swap("SUI/USDT")

    print(await e.wallets[0].exchange.fetch_balance())
    
    await e.end()
    

if __name__ == "__main__":
    asyncio.run(main())