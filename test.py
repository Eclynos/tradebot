from executer import Executer
from tools import read_symbols
import asyncio, time
    
    
async def main():
    e = Executer(read_symbols())

    await e.start()

    await e.buy_swap('SOL/USDT')

    time.sleep(8)

    await e.positions()

    await e.sell_swap('SOL/USDT')

    await e.positions()

    await e.history(0, "SOL/USDT", 1)
    
    await e.end()
    

if __name__ == "__main__":
    asyncio.run(main())