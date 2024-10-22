from wallet import Wallet
from marketInfo import MarketInformations
from tools import Tools


class Executer:
    def __init__(self, symbol) -> None:
        t = Tools()
        self.mi = MarketInformations(t)
        self.wallets = [Wallet("keys_nathael", False, self.mi)]
        self.amounts = {'BTC/USDT': [0],
                        'SOL/USDT' : [0],
                        'ETH/USDT' : [0],
                        'HNT/USDT' : [0]}
        self.costs = [2] # in USDT

        self.symbol = symbol


    async def start(self):
        await self.mi.init()
        for w in self.wallets:
            await w.init()


    async def end(self):
        await self.mi.account.disconnect()
        for w in self.wallets:
            await w.account.disconnect()


    def market_mode(self, mode):
        for w in self.wallets:
            w.market_mode(mode)


    async def buy(self):
        
        await self.calculate_amounts(self.symbol)
        
        for i in range(len(self.wallets)):
            order = None
            
            while True:
                try:
                    order = await self.wallets[i].buy(
                    self.symbol,
                    self.amounts[self.symbol][i],
                    self.costs[i]
                    )
                except Exception as e:
                    print(f"Le wallet {i} n'a pas réussi à acheter\n{e}")
                
                if order != None:
                    print(f"Achat de {self.amounts[self.symbol][i]} {self.symbol}")
                    break


    async def sell(self):
        for i in range(len(self.wallets)):
            order = None
            
            while True:
                try:
                    order = await self.wallets[i].sell_percentage(self.symbol)
                
                except Exception as e:
                    print(f"Le wallet {i} n'a pas réussi à vendre\n{e}")
                    
                if order != None:
                    print(f"Vente de tout le {self.symbol} du wallet {i}")
                    break


    async def calculate_amounts(self, symbol):
        """Calcule les montants correspondants aux coûts à acheter"""
        price = await self.mi.getPrice(symbol)
        for i in range(len(self.wallets)):
            self.amounts[symbol][i] = self.mi.currency_equivalence(self.costs[i], price)