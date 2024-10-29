from executer import Executer
import asyncio
    
    
async def main():
    e = Executer()

    await e.start()

    #await e.leverage(e.factors)
    
    #await e.buy_swap("SOL/USDT")
    
    #await asyncio.sleep(5)

    #e.wallets[0].market_mode('spot')
    
    #await e.wallets[0].walletInformations()
    
    #await asyncio.sleep(9)
    
    await e.sell_swap("SOL/USDT")

    e.wallets[0].market_mode('spot')
    
    await e.wallets[0].walletInformations()
    
    await e.end()
    

if __name__ == "__main__":
    asyncio.run(main())