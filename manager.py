from wallet import Wallet
from marketInfo import MarketInformations
from tools import *
import asyncio


class Manager:
    def __init__(self, symbols, settings) -> None:
        """Initialise l'instance de la classe
        Initialise le grand dictionnaire à partir des données du fichier json"""
        self.mi = MarketInformations()

        self.symbols = symbols
        self.min_amounts = {}
        self.infos = {}
        self.wallets = {}
        self.margin_mode = settings["margin_mode"]

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
        """Connecte tous les comptes et initialise les paramètres généraux"""
        try:
            await self.mi.init()
            for w in self.wallets.values():
                await w.init()
                await w.exchange.set_position_mode(hedged=True)
                w.leverage_mode(self.margin_mode)
            await self.calculate_min_amounts()
            await self.update_cost_datas()
            #await self.leverage()
        except Exception as e:
            raise ValueError(e)


    async def end(self):
        """Déconnecte tous les comptes"""
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
        Avec l'amount si l'équivalent en USDT est supérieur à 5$ancienne
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


    async def leverage(self):
        """Défini l'effet de levier sur un compte à partir de la donnée contenue dans le grand dictionnaire"""
        for key, w in self.wallets.items():
            for symbol in self.symbols:
                await w.leverage(self.infos[key]['factor'], symbol, self.margin_mode)
    

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
        
        await self.update_cost_datas()
        #await self.leverage()
    

    async def load_positions(self, timeLoop):
        """Charge les positions ouvertes sur les comptes
        Crée les dico is_open_since et bought_type
        """
        is_open_since = {symbol: 0 for symbol in self.symbols}
        bought_type = {symbol: "" for symbol in self.symbols}

        for key, w in self.wallets.items():
            positions = await w.exchange.fetch_positions()
            for p in positions:
                symbol = p['symbol'].split(":")[0]
                self.infos[key]['buyed?'][symbol] = True
                bought_type[symbol] = "dip"
                if is_open_since[symbol] < ((time.time() * 1000) - p['timestamp']) // (timeLoop * 60000):
                    is_open_since[symbol] = int(((time.time() * 1000) - p['timestamp']) // (timeLoop * 60000))
        return is_open_since, bought_type


    async def update_cost_datas(self):
        """Met à jour les coûts contenus dans le grand dictionnaire"""
        try:
            availables = await asyncio.gather(*(w.get_crossed_max_available() for w in self.wallets.values()))
            for key, cost in zip(self.wallets.keys(), availables):
                self.infos[key]['available'] = cost * 0.995
            await asyncio.sleep(1)
            totals = await asyncio.gather(*(w.get_crossed_total_available() for w in self.wallets.values()))
            for key, cost in zip(self.wallets.keys(), totals):
                self.infos[key]['total'] = cost * 0.995
        except Exception as e:
            print(e)


# ORDER MANAGEMENT


    async def buy_spot(self, symbol):
        """Achète une crypto en spot sur tous les comptes"""
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
        """Vend tout le montant possédé d'une crypto en spot sur tous les comptes"""
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
        names = []
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
                        names.append(key)
                        self.infos[key]['buyed?'][symbol] = True

                except Exception as e:
                    print(f"Le wallet {key} n'a pas réussi à acheter en swap\n{e}")
            else:
                print("Insufficient amount")
            
        return names
    
    
    async def close_swap(self, symbol):
        """Essaie de vendre une crypto en swap sur tous les wallets
        Renvoie le nombre de ventes effectués avec succès"""
        names = []
        for key, w in self.wallets.items():
            order = None
            
            if self.infos[key]['buyed?'][symbol]:
                try:
                    order = await w.closep(symbol)

                    if order != None:
                        names.append(key)
                        self.infos[key]['buyed?'][symbol] = False
                
                except Exception as e:
                    print(f"Le wallet {key} n'a pas réussi à vendre\n{e}")
            
        return names


# INFORMATIONS GIVERS


    async def tell_positions(self):
        """Donne les positions actuelles ouvertes sur les wallets"""
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


    async def last_trades(self, symbol, timestamp):
        """
        Renvoie deux chaînes de caractères :
        - une contenant des informations sur le dernier trade effectué sur tous les comptes
        - une contenant les pourcentages effectués lors de ce trade
        """
        try:
            positions = ""
            pnls = ""
            for w in self.wallets:
                position, pnl = await self.wallets[w].last_position(symbol, timestamp)
                if position != "":
                    positions += f"{w}\n{position}\n"
                if pnl != 0:
                    pnls += f"{w} {str(pnl)}\n"
            if len(positions) > 0:
                positions = positions[:-1]
            if len(pnls) > 0:
                pnls = pnls[:-1]
            return positions, pnls
        except Exception as e:
            print(f"last trades error\n{e}")


    async def balances(self):
        """Renvoie une chaîne de caractères contenant le montant possédé sur chaque portefeuille"""
        chain = ""
        for key, w in self.wallets.items():
            total = await w.exchange.fetch_total_balance()
            used = await w.exchange.fetch_used_balance()
            chain += f"{key}: Total:{total} Used:{used}\n"