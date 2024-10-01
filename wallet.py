import ccxt.pro as ccxt
import requests


def ping_test(url="http://www.google.com", timeout=5):
    try:
        response = requests.get(url, timeout=timeout)
        return True if response.status_code == 200 else False
    except (requests.ConnectionError, requests.Timeout):
        return False
    

class Wallet:
    def __init__(self, access_key, secret_key, passphrase) -> None:
        self.access_key = access_key
        self.secret_key = secret_key
        self.passphrase = passphrase
        
        self.exchange = None
        
        
    async def connect(self):
        """Connect account with api keys to python"""
        self.exchange = ccxt.bitget({ # etablie la connexion au compte
            'apiKey': self.access_key,
            'secret': self.secret_key,
            'password': self.passphrase,
        })
        
        # balance = await self.exchange.fetch_balance() # Recupere les informations sur le wallet utilise
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
        
        if mode == 'hedge' or mode == 'one-way':
            await self.exchange.set_position_mode(mode, symbol)
        else:
            print("Wrong position mode")
    


# ORDER MANAGING


    async def place_order(self, symbol, BuyorSell, amount, price): # À MODIFIER
        """Place un ordre d'acheter ou vendre lorsque la crypto atteint un certain prix"""
        await self.exchange.load_markets() # met en cache toutes les informations sur les paires de trading disponibles avant d'effectuer des opérations de trading
        
        try:
            order = await self.exchange.create_order(
                    symbol = symbol,
                    type = 'limit',
                    side = BuyorSell,
                    amount = amount,
                    price = price,
                )
            print(order)
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
        """Achète directement une crypto"""
        await self.exchange.load_markets() # met en cache toutes les informations sur les paires de trading disponibles avant d'effectuer des opérations de trading
        
        try:
            order = await self.exchange.create_order(
                    symbol = symbol,
                    type = 'market',
                    side = 'buy',
                    amount = amount,
                )
            print(order)
        except Exception as e:
            print(f"Erreur lors de l'achat de {symbol} : {e}")
        
    
    async def sell(self, symbol, amount): 
        """Vend directement un nombre d'une crypto"""
        await self.exchange.load_markets()  # Met en cache les informations sur les paires disponibles

        try:
            balance = await self.exchange.fetch_balance()
            available_amount = balance['free'].get(symbol, 0)
            print(f"Solde disponible de {symbol}: {available_amount}")

            if available_amount < amount:
                print("Solde insuffisant pour effectuer cette vente.")
                return

            market_info = self.exchange.markets[symbol]
            min_amount = market_info['limits']['amount']['min']
            if amount < min_amount:
                print(f"Le montant est inférieur au montant minimum requis ({min_amount}).")
                return

            # Crée l'ordre de vente
            order = await self.exchange.create_order(
                symbol = symbol,
                type = 'market',
                side = 'sell',
                amount = amount,
            )
            print(order)

        except Exception as e:
            print(f"Erreur lors de la vente de {symbol} : {e}")


    async def sell_percentage(self, symbol, percentage): # pas testé
        """Vend directement un pourcentage d'une crypto possédée"""
        await self.exchange.load_markets()  # Met en cache les informations sur les paires disponibles

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
            print(order)

        except Exception as e:
            print(f"Erreur lors de la vente de {symbol} : {e}")


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
        
        for trade in trades:
            print(f"ID: {trade['id']}, {trade['side']}\nPrix: {trade['price']}, Quantité: {trade['amount']} = {await self.crypto_equivalence(symbol, trade['amount'])} €\nDate: {self.exchange.iso8601(trade['timestamp'])}\n")
        
    
    async def walletInformations(self):
        """"""
        balance = await self.exchange.fetch_balance()
        
        for element in balance["info"]:
            if element['coin'] != 'EUR':
                print(f"{element['coin']}: {element['available']} = {await self.crypto_equivalence(element['coin'] + '/EUR', float(element['available']))} €")
            else:
                print(f"{element['coin']}: {element['available']} €")
        
        
        
# WATCH MARKET INFORMATIONS

        
    async def getAllSymbols(self):
        """Récupère et affiche tous les paires de trading disponibles sur l'échange"""
        await self.exchange.load_markets()
        markets = self.exchange.markets
        symbols = list(markets.keys())
        return symbols
    
    
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


    async def currency_equivalence(self, symbol, amount):
        """Calcule le montant équivalent d'une crypto à une monnaie

        Args:
            symbol ('BTC/EUR'): Symbole de la paire de trading Crypto / monnaie d'échange
            amount: montant de la monnaie d'échange à calculer
        """
        price = await self.getPrice(symbol)
        return round(amount / price, 13)


    async def crypto_equivalence(self, symbol, amount):
        """Calcule le montant équivalent d'une monnaie à une crypto

        Args:
            symbol ('BTC/EUR'): Symbole de la paire de trading Crypto / monnaie d'échange
            amount: montant de la monnaie d'échange à calculer
        """
        price = await self.getPrice(symbol)
        return amount * price