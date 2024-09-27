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
        
        self.mode_sandbox = False
        
        self.exchange = None
        
        
    async def connect(self):
        """Connect account with api keys to python"""
        self.exchange = ccxt.bitget({ # etablie la connexion au compte
        'apiKey': self.access_key,
        'secret': self.secret_key,
        'password': self.passphrase,
        })
        
        if self.mode_sandbox:
            self.exchange.set_sandbox_mode(True) # Le mode sandbox permet de tester des stratégies de trading ou d'effectuer des opérations fictives dans un environnement de simulation sans engager de fonds réels. À utiliser pour tester l'api
        
        balance = await self.exchange.fetch_balance() # effectuer les opérations dans l'environnement test (sandbox)
        self.exchange.verbose = True # pour le debug
        print(f"Connected! Balance: {balance}")
        
        
    async def place_order(self, coinCode, BuyorSell, amount, price):
        """Place un ordre d'acheter ou vendre lorsque la crypto atteint un certain prix"""
        await self.exchange.load_markets() # met en cache toutes les informations sur les paires de trading disponibles avant d'effectuer des opérations de trading
        
        try:
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
        """Tente de supprimer un ordre"""
        try:
            response = await self.exchange.cancel_order(order_id, coinCode)
            print(response)
        except Exception as e:
            print("Order cancelling failed")
            print(e)
            
            
    async def cancel_all_orders(self):
        """Tente de supprimer tous les ordres (!= toutes les positions)"""
        try:
            response = await self.exchange.cancel_all_orders()
            print(response)
        except Exception as e:
            print(e)
        
    
    async def buy(self, coinCode, amount):
        """Achète directement une crypto"""
        await self.exchange.load_markets() # met en cache toutes les informations sur les paires de trading disponibles avant d'effectuer des opérations de trading
        
        try:
            symbol = 'S' + coinCode + '/SUSDT:SUSDT' if self.mode_sandbox else coinCode + '/USDT:USDT'
            
            order = await self.exchange.create_order(
                    symbol = symbol,
                    type = 'market',
                    side = 'buy',
                    amount = amount,
                )
            print(order)
        except Exception as e:
            print(f"Erreur lors de l'achat de {coinCode} : {e}")
        
    
    async def sell(self, coinCode, amount): # on pourra faire en sorte de sell un pourcentage et pas un amount
        """Vend directement une crypto"""
        await self.exchange.load_markets() # met en cache toutes les informations sur les paires de trading disponibles avant d'effectuer des opérations de trading
        
        try:
            symbol = 'S' + coinCode + '/SUSDT:SUSDT' if self.mode_sandbox else coinCode + '/USDT:USDT'
            
            order = await self.exchange.create_order(
                symbol = symbol,
                type = 'market',
                side = 'sell',
                amount = amount,
            )
            print(order)
        except Exception as e:
            print(f"Erreur lors de la vente de {coinCode} : {e}")
        
    
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
      
      
    async def watchPositions(self, coinCode):
        """Regarde les positions actuelles pour un symbole"""
        trades = await self.exchange.watch_positions(coinCode + '/USDT:USDT') # si l'argument est None, donne toutes les positions sur chaque symbole
        return trades
    
        
    async def transactionHistory(self, coinCode):
        """Donne l'historique des trades sur un symbole (crypto)"""
        trades = await self.exchange.fetch_my_trades(coinCode + '/USDT')
        
        for trade in trades:
            print(f"Trade ID: {trade['id']}, Type: {trade['side']}, Prix: {trade['price']}, Quantité: {trade['amount']}, Date: {self.exchange.iso8601(trade['timestamp'])}")
    
       
    async def orderBook(self, coinCode):
        """Donne l'order book des trades sur un symbole"""
        orderbook = await self.exchange.watch_order_book_for_symbols(coinCode + '/USDT')
        print(orderbook['symbol'], orderbook['asks'][0], orderbook['bids'][0], orderbook["datetime"])
        
        
    async def getAllSymbols(self):
        """Récupère et affiche tous les symboles de trading disponibles sur l'échange"""
        await self.exchange.load_markets()
        markets = self.exchange.markets
        symbols = list(markets.keys())
        print("ok")
        return symbols


        
    async def disconnect(self): # à faire à la fin de l'utilisation du compte, à la fin du code
        """Déconnecte le compte lié"""
        try:
            await self.exchange.close()
            print("Disconnected")
        except Exception as e:
            print("Failed disconnecting")
            print(e)