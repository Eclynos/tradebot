from executer import Executer
import asyncio
    
    
async def main():
    e = Executer()

    await e.start()


    
    await e.end()
    

if __name__ == "__main__":
    asyncio.run(main())


# tester futures car swap = spot fees -> try futures
# tester leverage
# faire fonctionner la loop, check toutes les minutes