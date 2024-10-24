from executer import Executer
import asyncio
    
    
async def main():
    e = Executer()

    await e.start()
    
    await e.buy_swap("BTC/USDT")
    
    await asyncio.sleep(4)
    
    await e.wallets[0].walletInformations()
    
    #asyncio.sleep(9)
    
    #await e.sell_swap("BTC/USDT")
    
    await e.end()
    

if __name__ == "__main__":
    asyncio.run(main())