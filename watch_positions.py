from executer import Executer
from tools import read_symbols, ping_test
import asyncio, time
    
async def main():

    if not ping_test():
        print("Not connected to internet")
        return

    e = Executer(read_symbols())

    await e.start()

    #print(await e.history(0, "SUI/USDT", 1))

    """

    print(await e.buy_swap("SUI/USDT"))

    await e.positions()

    await e.wallets[0].walletInformations()

    await e.update_available_cost()

    time.sleep(19)

    await e.sell_swap("SUI/USDT")
    """

    print(await e.history(0, "SUI/USDT", 1))
    
    await e.end()
    

if __name__ == "__main__":
    asyncio.run(main())