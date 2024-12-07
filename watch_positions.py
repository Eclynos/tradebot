from manager import Manager
from tools import read_symbols, ping_test
import asyncio, time
    
async def main():

    if not ping_test():
        print("Not connected to internet")
        return

    m = Manager(read_symbols())

    await m.start()

    print(await m.history(0, "SUI/USDT", 1))
    
    await m.end()
    

if __name__ == "__main__":
    asyncio.run(main())