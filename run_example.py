from executer import Executer
import asyncio, time
    
    
async def main():
    e = Executer("SOL/USDT")
    await e.start()
    
    await e.buy()
    
    time.sleep(6)
    
    await e.sell()
    
    await e.end()
    

if __name__ == "__main__":
    asyncio.run(main())