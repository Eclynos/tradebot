from executer import Executer
from tools import read_symbols
import asyncio
    
async def main():
    e = Executer(read_symbols())

    await e.start()

    await e.positions()
    
    await e.end()
    

if __name__ == "__main__":
    asyncio.run(main())