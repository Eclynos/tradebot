from wallet import Wallet
from marketInfo import MarketInformations
from tools import *


class Executer:
    def __init__(self, symbols) -> None:
        self.mi = MarketInformations()
        self.wallets = [Wallet("keys_nathael", False, self.mi)]
        
        self.costs = [5] # cost to spend at each trade in USDT

        self.symbols = symbols
        self.min_amounts = {}
        
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
        await self.calculate_min_amounts()
        await self.update_tradable_cost()


    async def end(self):
        await self.mi.account.disconnect()
        for w in self.wallets:
            await w.account.disconnect()


# OPTIONS / CALCULATIONS


    def market_mode(self, mode):
        for w in self.wallets:
            w.market_mode(mode)


    async def calculate_amounts(self, symbol):
        """Calcule les montants correspondants aux coûts à acheter"""
        price = await self.mi.getPrice(symbol)
        for i in range(len(self.wallets)):
            self.infos[i]['amounts'][symbol] = self.mi.currency_equivalence(self.infos[i]['cost'], price)


    async def calculate_min_amounts(self):
        """Rempli le dictionnaire des montants de trading minimums:
        Avec l'amount si l'équivalent en USDT est supérieur à 5$
        avec None sinon
        """
        await self.mi.exchange.load_markets()
        for symbol in self.symbols:
            market = self.mi.exchange.market(symbol + ':USDT')
            if await self.mi.actual_crypto_equivalence(symbol, market['limits']['amount']['min']) > 6:
                self.min_amounts[symbol] = market['limits']['amount']['min']
            else:
                self.min_amounts[symbol] = None


    async def leverage(self, factor_list):
        for i, w in enumerate(self.wallets):
            for symbol in self.symbols:
                await w.leverage(factor_list[i], symbol)


    async def update_tradable_cost(self):
        pass


# ORDER MANAGEMENT


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
                    'buy')

            except Exception as e:
                print(f"Le wallet {i} n'a pas réussi à acheter en swap\n{e}")
                return False
            
            if order != None:
                return True
    
    
    async def sell_swap(self, symbol):
        for i, w in enumerate(self.wallets):
            order = None
            
            try:
                order = await w.closep(symbol)
            
            except Exception as e:
                print(f"Le wallet {i} n'a pas réussi à vendre\n{e}")
                return False
            
            if order != None:
                return True


# INFORMATIONS GIVERS


    async def positions(self):
        size = len(self.wallets)
        positions = [None] * size

        try:
            for i, w in enumerate(self.wallets):
                positions[i] = await w.exchange.fetch_positions()
        except Exception as e:
            print(f"Error fetching positions of wallet {i}\n{e}")

        for i in range(size):
            if positions[i] != []:
                print(f"Positions of wallet {i}:")
                for p in positions[i]:
                    print(f"Entry Price: {p['entryPrice']}, Symbol: {p['symbol']}")
                    print(f"ID: {p['id']}, Side: {p['side']}")
                    print(f"Leverage: {p['leverage']}, Liquidation Price: {p['liquidationPrice']}")
                    print(f"Pnl: {p['unrealizedPnl']}")
            else:
                print(f"No positions are open on wallet {i}")


    async def history(self, wallet, symbol, limit=20):
        """Donne l'historique des trades en effectuant une requête au serveur"""
        print(await self.wallets[wallet].positionsHistory(symbol, limit))


    async def last_trades(self, symbol):
        return '\n'.join(await self.wallets[w].positionsHistory(symbol, 1) for w in range(self.wallets))
