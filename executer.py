from wallet import Wallet
from marketInfo import MarketInformations
from tools import Tools, left


class Executer:
    def __init__(self, symbols) -> None:
        self.t = Tools()
        self.mi = MarketInformations(self.t)
        self.wallets = [Wallet("keys_nathael", False, self.mi)]
        
        self.costs = [17.1] # cost to spend at each trade in USDT

        self.symbols = symbols
        
        self.factors = [1] # preset leverage factor
        
        self.infos = []
        
        for i in range(len(self.wallets)):
            dico = {}
            dico['cost'] = self.costs[i]
            dico['factor'] = self.factors[i]
            dico['amounts'] = {}
            for symbol in self.symbols:
                dico['amounts'][symbol] = 0
            self.infos.append(dico)


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
                    self.infos[i]['amounts'][symbol],
                    self.infos[i]['cost']
                    )
                except Exception as e:
                    print(f"Le wallet {i} n'a pas réussi à acheter\n{e}")
                
                if order != None:
                    print(f"Achat de {self.infos[i]['amounts'][symbol]} {symbol}")
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

        print(self.infos[0]['amounts'][symbol])

        for i, w in enumerate(self.wallets):
            order = None
            
            try:
                order = await w.openp(
                    symbol,
                    self.infos[i]['amounts'][symbol],
                    'long')

            except Exception as e:
                print(f"Le wallet {i} n'a pas réussi à acheter en swap\n{e}")
            
            if order != None:
                print(f"Achat swap de {self.infos[i]['amounts'][symbol]} {symbol}")
    
    
    async def sell_swap(self, symbol):
        for i, w in enumerate(self.wallets):
            
            try:
                await w.closep(symbol, 'long')
            
            except Exception as e:
                print(f"Le wallet {i} n'a pas réussi à vendre\n{e}")



    async def watch_positions(self):
        positions = list(len(self.wallets))

        try:
            for i, w in enumerate(self.wallets):
                positions[i] = await w.exchange.fetch_positions()
        except Exception as e:
            print(f"Error fetching positions of wallet {i}\n{e}")

        for i in enumerate(self.wallets):
            print(f"Positions of wallet {i}:")
            for p in positions[i]:
                print(f"{p['entryPrice']} {p['symbol']}")
                print(f"ID: {p['id']}, {p['side']}")
                print(f"Leverage: {p['leverage']}, LiquidationPrice: {p['liquidationPrice']}")
                print(f"Pnl: {p['unrealizedPnl']}") #PnL = Profit and Loss



    async def calculate_amounts(self, symbol):
        """Calcule les montants correspondants aux coûts à acheter"""
        price = await self.mi.getPrice(symbol)
        for i in range(len(self.wallets)):
            self.infos[i]['amounts'][symbol] = self.mi.currency_equivalence(self.infos[i]['cost'], price)


    async def leverage(self, factor_list):
        for i, w in enumerate(self.wallets):
            for symbol in self.symbols:
                await w.leverage(factor_list[i], symbol)
