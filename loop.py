from executer import Executer
import asyncio
    
    
async def main():
    e = Executer()

    await e.start()


    
    await e.end()
    

if __name__ == "__main__":
    asyncio.run(main())


# faire fonctionner les buy/sell swap -> amount = amount in USDT
# faire fonctionner la loop, check toutes les minutes