from wallet import Wallet
from marketInfo import MarketInformations
from tools import Tools


class Executer:
    def __init__(self) -> None:
        t = Tools()
        self.mi = MarketInformations(t)
        self.wallets = [Wallet("keys_nathael", False, self.mi)]
        self.amounts = {'BTC/USDT': [0],
                        'SOL/USDT' : [0],
                        'ETH/USDT' : [0],
                        'HNT/USDT' : [0]}
        self.costs = [3] # in USDT

        self.symbols = ['BTC/USDT',
                        'SOL/USDT',
                        'ETH/USDT',
                        'HNT/USDT']
        
        self.factor_list = [1]


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


    async def buy_spot(self, symbol):
        
        await self.calculate_amounts(symbol)
        
        for i, w in enumerate(self.wallets):
            order = None
            
            for i in range(5):
                try:
                    order = await w.buy(
                    symbol,
                    self.amounts[symbol][i],
                    self.costs[i]
                    )
                except Exception as e:
                    print(f"Le wallet {i} n'a pas réussi à acheter\n{e}")
                
                if order != None:
                    print(f"Achat de {self.amounts[symbol][i]} {symbol}")
                    break


    async def sell_spot(self, symbol):
        for i, w in enumerate(self.wallets):
            order = None
            
            for i in range(5):
                try:
                    order = await w.sell_percentage(symbol)
                
                except Exception as e:
                    print(f"Le wallet {i} n'a pas réussi à vendre\n{e}")
                    
                if order != None:
                    print(f"Vente de tout le {symbol} du wallet {i}")
                    break


    async def buy_swap(self, symbol):
        
        await self.calculate_amounts(symbol)
        
        for i, w in enumerate(self.wallets):
            order = None
            
            try:
                order = await w.open_swap(
                    symbol,
                    self.amounts[symbol][i],
                    'buy')
            except Exception as e:
                print(f"Le wallet {i} n'a pas réussi à acheter en swap\n{e}")
            
            if order != None:
                print(f"Achat swap de {self.amounts[symbol][i]} {symbol}")
    
    
    async def sell_swap(self, symbol):
        for i, w in enumerate(self.wallets):
            order = None
            
            try:
                base_currency = symbol.split('/')[0]
                balance = await w.exchange.fetch_balance()
                
                if base_currency not in balance['free']:
                    raise ValueError(f"Pas de {base_currency}")
                amount = balance['free'].get(base_currency, 0)
                
                order = await w.close_swap(
                    symbol,
                    amount,
                    'sell')
            
            except Exception as e:
                print(f"Le wallet {i} n'a pas réussi à vendre\n{e}")
                
            if order != None:
                print(f"Vente de tout le {symbol} du wallet {i}")


    async def calculate_amounts(self, symbol):
        """Calcule les montants correspondants aux coûts à acheter"""
        price = await self.mi.getPrice(symbol)
        for i in range(len(self.wallets)):
            self.amounts[symbol][i] = self.mi.currency_equivalence(self.costs[i], price)
        print(self.amounts[symbol][i])
        print(self.amounts[symbol][i] * price)


    async def leverage(self, factor_list):
        for symbol in self.symbols:
            for i, w in enumerate(self.wallets):
                await w.leverage(factor_list[i], symbol)


# fonction pour check le prix dispo en USDT pour pouvoir investir
# gestion des achats, rearrangement des listes amounts et symbols