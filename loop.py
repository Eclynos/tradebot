from executer import Executer
import asyncio
    
    
async def main():
    e = Executer()

    await e.start()

    e.wallets[0].market_mode('swap')

    await e.leverage(e.factors)
    
    #await e.buy_swap("BTC/USDT")
    
    #await asyncio.sleep(5)
    
    #await e.wallets[0].walletInformations()
    
    #asyncio.sleep(9)
    
    #await e.sell_swap("BTC/USDT")
    
    await e.end()
    

if __name__ == "__main__":
    asyncio.run(main())


# faire fonctionner les buy/sell swap
# faire fonctionner la loop, check toutes les minutes