import ccxt.pro as ccxt
    

class Wallet:
    def __init__(self, api_keys, sandbox_mode) -> None:
        self.keys = api_keys
        self.sandbox_mode = sandbox_mode
        self.exchange = None
        self.positions = []
        
        
    async def connect(self):
        """Connect account with api keys to python"""
        self.exchange = ccxt.bitget({ # etablie la connexion au compte
            'apiKey': self.keys.access_key,
            'secret': self.keys.secret_key,
            'password': self.keys.passphrase,
        })
        
        if self.sandbox_mode:
            self.exchange.set_sandbox_mode(True)
        
        self.exchange.verbose = False # pour le debug si True
        print("Connected")
        
        
    async def disconnect(self): # à faire à la fin de l'utilisation du compte, à la fin du code
        """Déconnecte le compte lié"""
        try:
            await self.exchange.close()
            print("Disconnected")
        except Exception as e:
            print("Failed disconnecting")
            print(e)


# SETTING OPTIONS


    def market_mode(self, mode):
        """Défini le marché sur lequel on veut échanger
        
        Args:
            mode('spot'): trading "classique" où les cryptos sont achetées ou vendues immédiatement au prix actuel du marché.
            mode('swap'): trading de contrats à terme perpétuels. Ces contrats n'ont pas de date d'expiration, contrairement aux futures classiques.
            mode('future'): trading de contrats à terme (futures) qui ont une date d'expiration. Ces contrats permettent de spéculer sur le prix d'une crypto à une date ultérieure.
            mode('margin'): trading sur marge, où tu empruntes des fonds pour acheter ou vendre une crypto, ce qui te permet d'avoir un effet de levier sur tes transactions.
        """
        
        if mode in ['spot', 'swap', 'future', 'margin']:
            self.exchange.options['defaultType'] = mode
        else:
            print("Wrong market mode")
        
            
    def leverage_mode(self, mode):
        """Défini le mode de gestion du risque

        Args:
            mode ('isolated'): sépare la marge utilisée pour chaque position
            mode ('cross'): toutes les positions partagent le même solde disponible pour éviter la liquidation -> plus dangereux
        """
        if mode == 'isolated' or mode == 'cross':
            self.exchange.options['marginMode'] = mode
        else:
            print("Wrong leverage mode")
   

    async def leverage(self, factor, symbol):
        """Défini le taux d'effet de levier à utiliser"""
        await self.exchange.set_leverage(factor, symbol)


    async def position_mode(self, mode, symbol):
        """Configure le mode de gestion des positions
        (On va presque toujours utiliser hedge parce que one-way empêche de mettre des SL par exemple)
        
        Args:
            mode('hedge'): ouvrir à la fois des positions longues et courtes simultanément pour un même actif
            mode('one-way'): avoir qu'une seule position ouverte sur une paire de trading à un moment donné.
        """
        
        if mode == 'hedge':
            await self.exchange.set_position_mode(True, symbol)
        elif mode == "one-way":
            await self.exchange.set_position_mode(False, symbol)
        else:
            print("Wrong position mode")


# ORDER MANAGING


    async def place_order(self, symbol, BuyorSell, amount, price): # À MODIFIER
        """Place un ordre d'acheter ou vendre lorsque la crypto atteint un certain prix"""
        
        try:
            order = await self.exchange.create_order(
                    symbol = symbol,
                    type = 'limit',
                    side = BuyorSell,
                    amount = amount,
                    price = price,
                )
            
            self.save_and_print_position(order)
            
        except Exception as e:
            print(f"Erreur lors du placement de l'ordre de {symbol} : {e}")
            
        
        
    async def cancel_order(self, symbol, order_id): # pas testé
        """Tente de supprimer un ordre (!= vendre une position)"""
        try:
            response = await self.exchange.cancel_order(order_id, symbol)
            print(response)
        except Exception as e:
            print("Order cancelling failed")
            print(e)
            
            
    async def cancel_all_orders(self, symbol): # pas testé
        """Tente de supprimer tous les ordres (!= vendre toutes les positions)"""
        try:
            response = await self.exchange.cancel_all_orders(symbol)
            print(response)
        except Exception as e:
            print(e)


    async def buy(self, symbol, amount):
        """Achète directement une quantité d'une crypto"""
        
        try:
            order = await self.exchange.create_order(
                    symbol = symbol,
                    type = 'market',
                    side = 'buy',
                    amount = amount,
                )
            
            self.save_and_print_position(order)
            
        except Exception as e:
            print(f"Erreur lors de l'achat de {symbol} : {e}")


    async def buy_with_cost(self, symbol, cost):
        """Achète directement une quantité d'une crypto avec un coût en fiat"""
        
        try:
            order = await self.exchange.create_market_buy_order_with_cost(
                    symbol = symbol,
                    cost = cost,
                )
            
            self.save_and_print_position(order)
            
        except Exception as e:
            print(f"Erreur lors de l'achat de {symbol} : {e}")
        
    
    async def sell(self, symbol, amount): 
        """Vend directement un nombre d'une crypto"""

        try:
            order = await self.exchange.create_order(
                symbol = symbol,
                type = 'market',
                side = 'sell',
                amount = amount,
            )
            
            self.save_and_print_position(order)

        except Exception as e:
            print(f"Erreur lors de la vente de {symbol} : {e}")


    async def close_all_positions(self): # pas testée
        """Vend toutes les positions existantes"""
        
        try:
            order = await self.exchange.close_all_positions()
            
            self.save_and_print_position(order)
            
        except Exception as e:
            print(f"Erreur lors de la fermeture de toutes les positions : {e}")
        
            
            
    async def sell_with_cost(self, symbol, cost):
        """Vend directement une quantité d'une crypto avec un coût en fiat"""
        
        try:
            order = await self.exchange.create_market_sell_order_with_cost(
                    symbol = symbol,
                    cost = cost,
                )
            
            self.save_and_print_position(order)
            
        except Exception as e:
            print(f"Erreur lors de la vente de {symbol} : {e}")


    async def sell_percentage(self, symbol, percentage=100): # pas testé
        """Vend directement un pourcentage d'une crypto possédée"""

        try:
            balance = await self.exchange.fetch_balance()
            available_amount = balance['free'].get(symbol, 0)
            amount = available_amount * (percentage/100)
            
            order = await self.exchange.create_order(
                symbol = symbol,
                type = 'market',
                side = 'sell',
                amount = amount,
            )
            
            self.save_and_print_position(order)

        except Exception as e:
            print(f"Erreur lors de la vente de {symbol} : {e}")


    def save_and_print_position(self, order):
        """Sauvegarde la position dans la liste des positions et print les informations"""
        
        print(f"ID: {order["id"]}, {order["side"]}\nPrice: {order['average']}")
        print(f"Quantity: {order['filled']} = {self.crypto_equivalence(order['filled'], order['average'])} €")
        print(f"Cost: {order['cost']}\nFees: {order['fee']['cost']} {order['fee']['currency']}\nFee rate: {order['fee']['rate']}")
        
        self.positions.append(order)


# WATCH WALLET INFORMATIONS


    async def check_positions(self):
        """Vérifie les positions ouvertes sur le compte.
        Les positions peuvent être les achats en future / margin / swap
        ou les ordres d'achat / vente qui n'ont pas encore abouti"""
        try:
            positions = await self.exchange.fetch_positions(params={'type': 'spot'})
            if positions:
                print("Positions ouvertes :")
                for position in positions:
                    print(position)
                return positions
            else:
                print("Aucune position ouverte.")
        except Exception as e:
            print(f"Erreur lors de la récupération des positions : {e}")
      
        
    async def watchOrders(self): # ne fonctionne pas encore
        """Regarde les ordres en temps réel."""
        try:
            while True:
                order = await self.exchange.watch_orders()
                print("Nouvel ordre : ", order)
        except Exception as e:
            print(f"Erreur lors de la surveillance des ordres : {e}")


    async def transactionHistory(self, symbol):
        """Donne l'historique des trades sur une paire"""
        trades = await self.exchange.fetch_my_trades(symbol)
        print('\n' + symbol + " History")
        
        for trade in trades:
            print(f"ID: {trade['id']}, {trade['side']}\nPrice: {trade['price']}\nQuantity: {trade['amount']} = {await self.actual_crypto_equivalence(symbol, trade['amount'])} €\nDate: {self.exchange.iso8601(trade['timestamp'])}\n")


    async def orderBook(self, symbol):
        """Donne l'order book des trades sur une paire"""
        try:
            orderbook = await self.exchange.watch_order_book(symbol)
            print(f"Order Book for {symbol}:")
            print(f"Asks: {orderbook['asks'][0]}")
            print(f"Bids: {orderbook['bids'][0]}")
            print(f"Date: {orderbook['datetime']}")
        except Exception as e:
            print(f"Erreur lors de la récupération de l'order book de {symbol} : {e}")


    async def walletInformations(self):
        """Recupère les informations sur les positions dans un type de marché"""
        
        if self.exchange.options['defaultType'] == "spot":
            balance = await self.exchange.fetch_balance()
            print("Wallet informations in spot:")
            for elt in balance["info"]:
                if elt['coin'] != 'EUR':
                    print(f"{elt['coin']}: {elt['available']} = {await self.actual_crypto_equivalence(elt['coin'] + '/EUR', float(elt['available']))} €")
                else:
                    print(f"{elt['coin']}: {elt['available']} €")
        elif self.exchange.options['defaultType'] in ["future", "swap"]:
            balance = await self.exchange.fetch_balance()
            print(f"Wallet informations in {self.exchange.options['defaultType']}:")
            for elt in balance["info"]:
                print(f"{elt['marginCoin']}: {elt['available']}\naccountEquity: {elt['accountEquity']}\nusdtEquity: {elt['usdtEquity']}")       
        else:
            print("Wrong market mode for wallet informations")



class MarketInformations:
    def __init__(self, api_keys, tools) -> None:
        self.keys = api_keys
        self.tools = tools


    async def connect(self):
        self.exchange = ccxt.bitget({
            'apiKey': self.keys.access_key,
            'secret': self.keys.secret_key,
            'password': self.keys.passphrase,
        })
        
        if self.sandbox_mode:
            self.exchange.set_sandbox_mode(True)
        
        self.exchange.verbose = False
        print("Connected")
        
        
    async def disconnect(self):
        try:
            await self.exchange.close()
            print("Disconnected")
        except Exception as e:
            print("Failed disconnecting")
            print(e)


    async def getAllSymbols(self):
        """Récupère et affiche tous les paires de trading disponibles sur l'échange"""
        await self.exchange.load_markets()
        markets = self.exchange.markets
        symbols = list(markets.keys())
        return symbols


    async def getPrice(self, symbol):
        """Donne le prix instantané d'un symbole par rapport à une monnaie.
        
        Args:
            symbol ('BTC/EUR'): le symbole de la paire de trading
            
        Returns:
            Le prix actuel de la paire de trading sous forme de float.
        """
        try:
            ticker = await self.exchange.fetch_ticker(symbol)
            price = ticker['last']  # Récupère le prix de la dernière transaction sur la blockchain
            return price
        except Exception as e:
            print(f"Erreur lors de la récupération du prix de {symbol} : {e}")


    async def actual_currency_equivalence(self, symbol, amount):
        """Calcule le montant équivalent d'une crypto à une monnaie en temps réel

        Args:
            symbol ('BTC/EUR'): Symbole de la paire de trading Crypto / monnaie d'échange
            amount: montant de la monnaie d'échange à calculer
        """
        price = await self.getPrice(symbol)
        return round(amount / price, 13)


    async def actual_crypto_equivalence(self, symbol, amount):
        """Calcule le montant équivalent d'une monnaie à une crypto en temps réel

        Args:
            symbol ('BTC/EUR'): Symbole de la paire de trading Crypto / monnaie d'échange
            amount: montant de la monnaie d'échange à calculer
        """
        price = await self.getPrice(symbol)
        return amount * price
    
    
    def currency_equivalence(self, amount, price):
        """Calcule le montant équivalent d'une crypto à une monnaie"""
        return round(amount / price, 13)


    def crypto_equivalence(self, amount, price):
        """Calcule le montant équivalent d'une monnaie à une crypto"""
        return amount * price
    
    
    def time_frame_to_ms(self, time_frame):
        """Calcule le bon nombre de ms pour une time_frame donnée"""
        unit = time_frame[-1]
        amount = int(time_frame[:-1])
        if unit == 'm':
            return amount * 60 * 1000
        elif unit == 'h':
            return amount * 60 * 60 * 1000
        elif unit == 'd':
            return amount * 24 * 60 * 60 * 1000
        else:
            print("Mauvais time_frame")

   
    async def fetch_candles(self, symbol, timeFrame, since):
        """Récupère les bougies d'une paire de trading d'une fréquence depuis un temps donné en SECONDES
        https://www.bitget.com/api-doc/contract/market/Get-Candle-Data
        """

        candles = []
        timestamp = await self.exchange.fetch_time()
        time_ago = timestamp - int(since)
        current_since = time_ago
        
        while current_since < timestamp:
            try:
                ohclv = await self.exchange.fetch_ohlcv(symbol, timeFrame, current_since, 1000)
            except Exception as e:
                print(e)
                break

            if not ohclv:
                break

            candles.extend(ohclv)
            last_timestamp = ohclv[-1][0]
            current_since = last_timestamp + self.tools.time_frame_to_ms(timeFrame)

            if current_since >= timestamp:
                break
        
        return candles