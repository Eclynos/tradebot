from executer import Executer
from math import floor
import asyncio, time
    
    
async def main():
    e = Executer()

    await e.start()

    start_time = time.time()
    
    while True:
        time.sleep(0.1)
        start = floor(start_time) // 60
        actual = await e.mi.exchange.fetch_time() // 60000
        print(actual)
        if actual > start:
            break
    
    await e.end()
    

if __name__ == "__main__":
    asyncio.run(main())