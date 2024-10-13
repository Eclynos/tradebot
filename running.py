from wallet import Wallet
from marketInfo import MarketInformations
from tools import Tools
import asyncio, time
    
    
async def main():
    t = Tools()
    mi = MarketInformations()
    w = Wallet("keys", False, mi)

    """
    if not t.ping_test():
        print("erreur")
        return;
    """

    await w.init()
    await mi.init()

    w.market_mode('swap')

    symbol = "BTC/USDT"
    price = await mi.getBidPrice(symbol)
    price *= 0.98
    amount = await mi.actual_currency_equivalence(symbol, 2)
    
    SL = price * 0.99; TP = price * 1.01
    
    order = await w.place_order(symbol, 'buy', amount, price, SL, TP)
    print(order)
    
    time.sleep(7)
    
    await w.cancel_all_orders("BTC/USDT")
    
    w.market_mode('spot')
    await w.walletInformations()
    
    await w.account.disconnect()
    await mi.account.disconnect()
    

if __name__ == "__main__":
    asyncio.run(main())









"""
create_limit_buy_order
Continuer à améliorer gestion des ordres
Trouver un moyen de tracer la courbe des derniers temps en récupérant les dernières bougies


async def place_order(self, symbol, BuyorSell, amount, price, SLprice=None, TPprice=None):
        await self.exchange.load_markets()

        if self.exchange.options['defaultType'] == "spot":
            print("mauvais type d'échange")
            raise ValueError(self.exchange.options['defaultType'])
        
        params = {
            'stopLoss': {
                'triggerPrice': SLprice,
                'price': SLprice * 0.999
            },
            'takeProfit' : {
                'triggerPrice': TPprice,
                'price': TPprice * 0.999
            },
            'type': self.exchange.options['defaultType'],
            'hedged': True
        }

        print(symbol, 'limit', BuyorSell, amount, price, params)

        try:
            order = await self.exchange.create_order(symbol, 'limit', BuyorSell, amount, price, params)
           
        except Exception as e:
            print(f"Erreur lors du placement de l'ordre de {symbol} :\n{e}")
            
        return order

https://stackoverflow.com/questions/70568934/create-contract-order-with-take-profit-and-stop-loss-with-ccxt
"""