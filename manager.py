from wallet import Wallet
from marketInfo import MarketInformations
from tools import *
import asyncio


class Manager:
    def __init__(self, symbols, settings) -> None:
        self.mi = MarketInformations()

        self.symbols = symbols
        self.min_amounts = {}
        self.infos = {}
        self.wallets = {}

        for key, w in settings["wallets"].items():
            self.infos[key] = {}
            self.wallets[key] = Wallet(w["key_file"], False, self.mi)
            self.infos[key]['cost'] = w["cost"] # % of wallet to spend at each trade in USDT
            self.infos[key]['factor'] = w["factor"] # preset leverage factor
            self.infos[key]['amounts'] = {symbol: 0 for symbol in self.symbols}
            self.infos[key]['buyed?'] = {symbol: False for symbol in self.symbols}
            self.infos[key]['total'] = 0 # total amount in swap
            self.infos[key]['available'] = 0 # amount available


    async def start(self):
        try:
            await self.mi.init()
            for w in self.wallets.values():
                await w.init()
            await self.calculate_min_amounts()
            await self.update_cost_datas()
        except Exception as e:
            raise ValueError(e)


    async def end(self):
        try:
            await self.mi.account.disconnect()
            for w in self.wallets.values():
                await w.account.disconnect()
        except Exception as e:
            raise ValueError(e)


# OPTIONS / CALCULATIONS


    def market_mode(self, mode):
        """Change les modes de marché de tous les wallets"""
        for w in self.wallets.values():
            w.market_mode(mode)


    async def calculate_amounts(self, symbol):
        """Calcule les montants correspondants aux coûts à acheter"""
        try:
            price = await self.mi.getPrice(symbol)
            for key in self.wallets:
                self.infos[key]['amounts'][symbol] = self.mi.currency_equivalence(self.infos[key]['cost'], price)
        except Exception as e:
            print(e)


    async def calculate_min_amounts(self):
        """Rempli le dictionnaire des montants de trading minimums:
        Avec l'amount si l'équivalent en USDT est supérieur à 5$
        avec None sinon
        """
        try:
            await self.mi.exchange.load_markets()
            for symbol in self.symbols:
                market = self.mi.exchange.market(symbol + ':USDT')
                if await self.mi.actual_crypto_equivalence(symbol, market['limits']['amount']['min']) > 6:
                    self.min_amounts[symbol] = market['limits']['amount']['min']
                else:
                    self.min_amounts[symbol] = 0
        except Exception as e:
            print(e)


    async def leverage(self, factor_list):
        for key, w in self.wallets.items():
            for symbol in self.symbols:
                await w.leverage(factor_list[key], symbol)
    

    async def update_settings(self, settings):
        """Met à jour les paramètres des wallets a partir du fichier json"""
        for key in self.infos:
            if key not in self.infos:
                self.infos.pop(key)

        for key, w in settings["wallets"].items():
            if key in self.infos:
                self.infos[key]['cost'] = w["cost"]
                self.infos[key]['factor'] = w["factor"]
            else:
                self.infos[key] = {}
                self.wallets[key] = Wallet(w["key_file"], False, self.mi)
                self.infos[key]['cost'] = w["cost"] # % of wallet to spend at each trade in USDT
                self.infos[key]['factor'] = w["factor"] # preset leverage factor
                self.infos[key]['amounts'] = {symbol: 0 for symbol in self.symbols}
                self.infos[key]['buyed?'] = {symbol: False for symbol in self.symbols}
    

    async def load_positions(self, timeLoop):
        is_open_since = {symbol: 0 for symbol in self.symbols}

        for key, w in self.wallets.items():
            positions = await w.exchange.fetch_positions()
            for p in positions:
                symbol = p['symbol'].split(":")[0]
                self.infos[key]['buyed?'][symbol] = True
                if is_open_since[symbol] < ((time.time() * 1000) - p['timestamp']) // (timeLoop * 60000):
                    is_open_since[symbol] = int(((time.time() * 1000) - p['timestamp']) // (timeLoop * 60000))
        return is_open_since


    async def update_cost_datas(self):
        try:
            availables = await asyncio.gather(*(w.get_crossed_max_available() for w in self.wallets.values()))
            for key, cost in zip(self.wallets.keys(), availables):
                self.infos[key]['available'] = cost * 0.99
            await asyncio.sleep(1)
            totals = await asyncio.gather(*(w.get_crossed_total_available() for w in self.wallets.values()))
            for key, cost in zip(self.wallets.keys(), totals):
                self.infos[key]['total'] = cost * 0.99
        except Exception as e:
            print(e)


# ORDER MANAGEMENT


    async def buy_spot(self, symbol):
        
        await self.calculate_amounts(symbol)
        
        for key, w in self.wallets.items():
            order = None

            try:
                order = await w.buy(
                symbol,
                self.infos[key]['amounts'][symbol],
                self.infos[key]['cost']
                )
            except Exception as e:
                print(f"Le wallet {key} n'a pas réussi à acheter\n{e}")
            
            if order != None:
                print(f"Achat de {self.infos[key]['amounts'][symbol]} {symbol}")
                break


    async def sell_spot(self, symbol):
        for key, w in self.wallets.items():
            order = None
            
            for i in range(5):
                try:
                    order = await w.sell_percentage(symbol)
                
                except Exception as e:
                    print(f"Le wallet {key} n'a pas réussi à vendre\n{e}")
                    
                if order != None:
                    print(f"Vente de tout le {symbol} du wallet {key}")
                    break


    async def long_swap(self, symbol):
        """Essaie d'acheter une crypto en swap sur tous les wallets
        Renvoie le nombre d'achats effectués avec succès"""
        purchases = 0
        price = await self.mi.getPrice(symbol)

        for key, w in self.wallets.items():

            if self.infos[key]['available'] > self.infos[key]['total'] * self.infos[key]['cost']:
                amount = self.mi.currency_equivalence(self.infos[key]['cost'] * self.infos[key]['total'], price)
            else:
                amount = self.mi.currency_equivalence(self.infos[key]['available'], price)

            if self.infos[key]["available"] > 5 and amount > self.min_amounts[symbol]:
                order = None
                try:
                    order = await w.openp(
                        symbol,
                        amount,
                        'buy')
                    
                    if order != None:
                        purchases += 1
                        self.infos[key]['buyed?'][symbol] = True

                except Exception as e:
                    print(f"Le wallet {key} n'a pas réussi à acheter en swap\n{e}")
            
        return purchases
    
    
    async def close_swap(self, symbol):
        """Essaie de vendre une crypto en swap sur tous les wallets
        Renvoie le nombre de ventes effectués avec succès"""
        sales = 0
        for key, w in self.wallets.items():
            order = None
            
            if self.infos[key]['buyed?'][symbol]:
                try:
                    order = await w.closep(symbol)

                    if order != None:
                        sales += 1
                        self.infos[key]['buyed?'][symbol] = False
                
                except Exception as e:
                    print(f"Le wallet {key} n'a pas réussi à vendre\n{e}")
            
            return sales


# INFORMATIONS GIVERS


    async def tell_positions(self):
        positions = [None] * len(self.wallets)

        try:
            for key, w in self.wallets.items():
                positions[key] = await w.exchange.fetch_positions()
        except Exception as e:
            print(f"Error fetching positions of wallet {key}\n{e}")

        for key in self.wallets:
            if positions[key] != []:
                print(f"Positions of wallet {key}:")
                for p in positions[key]:
                    print(f"Entry Price: {p['entryPrice']}, Symbol: {p['symbol']}")
                    print(f"ID: {p['id']}, Side: {p['side']}")
                    print(f"Leverage: {p['leverage']}, Liquidation Price: {p['liquidationPrice']}")
                    print(f"Pnl: {p['unrealizedPnl']}")
                    print(f"{p['datetime']}")
            else:
                print(f"No positions are open on wallet {key}")


    async def history(self, wallet, symbol, limit=20):
        """Donne l'historique des trades en effectuant une requête au serveur"""
        print(await self.wallets[wallet].positionsHistory(symbol, limit))


    async def last_trades(self, symbol):
        return '\n'.join([await self.wallets[w].positionsHistory(symbol, 1) for w in self.wallets])


    async def balances(self):
        """Renvoie une chaîne de caractères contenant le montant possédé sur chaque portefeuille"""
        chain = ""
        for key, w in self.wallets.items():
            total = await w.exchange.fetch_total_balance()
            used = await w.exchange.fetch_used_balance()
            chain += f"{key}: Total:{total} Used:{used}\n"
