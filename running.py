from wallet import Wallet
from marketInfo import MarketInformations
from tools import Tools
import asyncio, time, requests
    
    
async def main():
    t = Tools()
    mi = MarketInformations()
    w = Wallet("keys", False, mi)


    if not t.ping_test():
        print("erreur")
        return;


    await w.init()
    await mi.init()

    await w.walletInformations()
    
    #await w.transactionHistory("BTC/USDT")
    
    if not t.ping_test():
        print("erreur")
        return;

    await w.buy("BTC/USDT", 2)
    #await w.sell("BTC/USDT", amount)
    
    #print(w.positions)
    
    await w.walletInformations()

    
    await w.account.disconnect()
    await mi.account.disconnect()
    

if __name__ == "__main__":
    asyncio.run(main())



"""
while True:
    ask=exchange.fetch_order_book(sym)
    pr=ask['asks'][0][0]
    if exchange.fetch_positions()==[]:
        break
    elif exchange.fetch_positions()[0]['info']['unrealisedRoePcnt']*-100>=sl:
        exchange.create_order(sym, 'limit', 'sell', amount, pr)
    elif exchange.fetch_positions()[0]['info']['unrealisedRoePcnt']*100>=tp:
        exchange.create_order(sym, 'limit', 'sell', amount, pr)
    sleep(1)
https://stackoverflow.com/questions/70568934/create-contract-order-with-take-profit-and-stop-loss-with-ccxt
"""