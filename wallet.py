import ccxt.pro as ccxt
import requests


def ping_test(url="http://www.google.com", timeout=5):
    try:
        response = requests.get(url, timeout=timeout)
        return True if response.status_code == 200 else False
    except (requests.ConnectionError, requests.Timeout):
        return False
    

class Wallet:
    def __init__(self, access_key, secret_key, passphrase, sandbox_mode) -> None:
        self.access_key = access_key
        self.secret_key = secret_key
        self.passphrase = passphrase
        
        self.sandbox_mode = sandbox_mode
        
        self.exchange = None
        
        
    async def connect(self):
        """Connect account with api keys to python"""
        self.exchange = ccxt.bitget({ # etablie la connexion au compte
            'apiKey': self.access_key,
            'secret': self.secret_key,
            'password': self.passphrase,
        })
        
        if self.sandbox_mode:
            self.exchange.set_sandbox_mode(True) # Le mode sandbox permet de tester des stratégies de trading ou d'effectuer des opérations fictives dans un environnement de simulation sans engager de fonds réels. À utiliser pour tester l'api
        
        balance = await self.exchange.fetch_balance() # Recupere les informations sur le wallet utilise
        self.exchange.verbose = False # pour le debug si True
        print(f"Connected! Balance: {balance}")
        
        
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
   

    async def leverage(self, factor, coinCode, currency):
        """Défini le taux d'effet de levier à utiliser"""
        await self.exchange.set_leverage(factor, coinCode + '/' + currency)


    async def position_mode(self, mode, coinCode, currency):
        """Configure le mode de gestion des positions
        (On va presque toujours utiliser hedge parce que one-way empêche de mettre des SL par exemple)
        
        Args:
            mode('hedge'): ouvrir à la fois des positions longues et courtes simultanément pour un même actif
            mode('one-way'): avoir qu'une seule position ouverte sur une paire de trading à un moment donné.
        """
        
        if mode == 'hedge' or mode == 'one-way':
            await self.exchange.set_position_mode(mode, coinCode + '/' + currency)
        else:
            print("Wrong position mode")
    


# ORDER MANAGING


    async def place_order(self, coinCode, BuyorSell, amount, price, currency):
        """Place un ordre d'acheter ou vendre lorsque la crypto atteint un certain prix"""
        await self.exchange.load_markets() # met en cache toutes les informations sur les paires de trading disponibles avant d'effectuer des opérations de trading
        
        try:
            if currency == "USDT":
                symbol = 'S' + coinCode + '/SUSDT:SUSDT' if self.sandbox_mode else coinCode + '/USDT:USDT'
            elif currency == "EUR":
                symbol = print("No sandbox for eur") if self.sandbox_mode else coinCode + '/EUR'
            else:
                print("Wrong buy currency")
                return
            
            order = await self.exchange.create_order(
                    symbol = coinCode +'/USDT:USDT', # trouver quelque chose pour remplir les symboles, le but est d'obtenir par exemple : 'ETH/USDT:USDT'
                    type = 'limit',
                    side = BuyorSell,
                    amount = amount,
                    price = price,
                )
            print(order)
        except Exception as e:
            print(f"Erreur lors du placement de l'ordre de {coinCode} : {e}")
            
        
        
    async def cancel_order(self, coinCode, order_id):
        """Tente de supprimer un ordre (!= vendre une position)"""
        try:
            response = await self.exchange.cancel_order(order_id, coinCode)
            print(response)
        except Exception as e:
            print("Order cancelling failed")
            print(e)
            
            
    async def cancel_all_orders(self):
        """Tente de supprimer tous les ordres (!= vendre toutes les positions)"""
        try:
            response = await self.exchange.cancel_all_orders()
            print(response)
        except Exception as e:
            print(e)
        
    
    async def buy(self, coinCode, amount, currency="EUR"):
        """Achète directement une crypto"""
        await self.exchange.load_markets() # met en cache toutes les informations sur les paires de trading disponibles avant d'effectuer des opérations de trading
        
        try:
            if currency == "USDT":
                symbol = 'S' + coinCode + '/SUSDT:SUSDT' if self.sandbox_mode else coinCode + '/USDT:USDT'
            elif currency == "EUR":
                symbol = print("No sandbox for eur") if self.sandbox_mode else coinCode + '/EUR'
            else:
                print("Wrong buy currency")
                return
            
            order = await self.exchange.create_order(
                    symbol = symbol,
                    type = 'market',
                    side = 'buy',
                    amount = amount,
                )
            print(order)
        except Exception as e:
            print(f"Erreur lors de l'achat de {coinCode} : {e}")
        
    
    async def sell(self, coinCode, amount, currency="EUR"): 
        """Vend directement une crypto"""
        await self.exchange.load_markets()  # Met en cache les informations sur les paires disponibles

        try:
            if currency == "USDT":
                symbol = 'S' + coinCode + '/SUSDT:SUSDT' if self.sandbox_mode else coinCode + '/USDT:USDT'
            elif currency == "EUR":
                if self.sandbox_mode:
                    print("No sandbox for EUR")
                    return
                symbol = coinCode + '/EUR'
            else:
                print("Wrong sell currency")
                return

            # Vérifie le solde disponible
            balance = await self.exchange.fetch_balance()
            available_amount = balance['free'].get(coinCode, 0)
            print(f"Solde disponible de {coinCode}: {available_amount}")

            if available_amount < amount:
                print("Solde insuffisant pour effectuer cette vente.")
                return

            # Vérifie le montant minimum requis
            market_info = self.exchange.markets[symbol]
            min_amount = market_info['limits']['amount']['min']
            if amount < min_amount:
                print(f"Le montant est inférieur au montant minimum requis ({min_amount}).")
                return

            # Crée l'ordre de vente
            order = await self.exchange.create_order(
                symbol=symbol,
                type='market',
                side='sell',
                amount=amount,
            )
            print(order)

        except Exception as e:
            print(f"Erreur lors de la vente de {coinCode} : {e}")


# WATCH WALLET INFORMATIONS


    async def check_positions(self):
        """Vérifie les positions ouvertes sur le compte."""
        try:
            positions = await self.exchange.fetch_positions()
            if positions:
                print("Positions ouvertes :")
                for position in positions:
                    print(position)
                return positions
            else:
                print("Aucune position ouverte.")
        except Exception as e:
            print(f"Erreur lors de la récupération des positions : {e}")
      
      
    async def watchPositions(self, coinCode, currency):
        """Regarde les positions actuelles pour une paire de trading"""
        trades = await self.exchange.watch_positions_for_symbols(coinCode + '/EUR') # si l'argument est None, donne toutes les positions sur chaque symbole
        return trades
    
        
    async def transactionHistory(self, coinCode, currency):
        """Donne l'historique des trades sur une paire"""
        trades = await self.exchange.fetch_my_trades(coinCode + '/' + currency)
        
        for trade in trades:
            print(f"Trade ID: {trade['id']}, Type: {trade['side']}, Prix: {trade['price']}, Quantité: {trade['amount']}, Date: {self.exchange.iso8601(trade['timestamp'])}")
    
       
    async def orderBook(self, coinCode):
        """Donne l'order book des trades sur une paire"""
        orderbook = await self.exchange.watch_order_book_for_symbols(coinCode + '/USDT')
        print(orderbook['symbol'], orderbook['asks'][0], orderbook['bids'][0], orderbook["datetime"])
        
        
# WATCH MARKET INFORMATIONS

        
    async def getAllSymbols(self):
        """Récupère et affiche tous les paires de trading disponibles sur l'échange"""
        await self.exchange.load_markets()
        markets = self.exchange.markets
        symbols = list(markets.keys())
        return symbols
    
    
    async def getPrice(self, coinCode, currency):
        """Donne le prix instantané d'un symbole par rapport à une monnaie.
        
        Args:
            coinCode: La crypto-monnaie dont on veut connaître le prix, par exemple 'BTC'.
            currency: La devise par rapport à laquelle on veut connaître le prix, par exemple 'USDT' ou 'EUR'.
            
        Returns:
            Le prix actuel de la paire de trading sous forme de float.
        """
        try:
            await self.exchange.load_markets()
            if currency == "USDT":
                symbol = 'S' + coinCode + '/SUSDT:SUSDT' if self.sandbox_mode else coinCode + '/USDT:USDT'
            elif currency == "EUR":
                if self.sandbox_mode:
                    print("No sandbox for EUR")
                    return
                symbol = coinCode + '/EUR'
            else:
                print("Wrong currency specified")
                return

            ticker = await self.exchange.fetch_ticker(symbol)
            price = ticker['last']  # Récupère le prix de la dernière transaction sur la blockchain
            print(f"Le prix actuel de {coinCode}/{currency} est : {price}")
            return price
        except Exception as e:
            print(f"Erreur lors de la récupération du prix de {coinCode}/{currency} : {e}") 