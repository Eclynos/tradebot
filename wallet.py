import ccxt.pro as ccxt
from account import Account
from marketInfo import MarketInformations

class Wallet:
    def __init__(self, key_file, sandbox_mode, mi, transaction_file):
        self.account = Account(key_file)
        self.sandbox_mode = sandbox_mode
        self.transaction_file = transaction_file
        self.positions = []
        self.mi = mi


    async def init(self):
        await self.account.connect()
        self.exchange = self.account.exchange

        if self.sandbox_mode:
            self.exchange.set_sandbox_mode(True)



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


    async def place_order(self, symbol, BuyorSell, amount, price, SL, TP):
        """Place un ordre d'acheter ou vendre lorsque la crypto atteint un certain prix"""
        
        try:
            order = await self.exchange.create_order(
                    symbol = symbol,
                    type = 'limit',
                    side = BuyorSell,
                    amount = amount,
                    price = price,
                    params = {
                        
                    }
                )
            
            await self.save_and_print_position(symbol, 1)
            
        except Exception as e:
            print(f"Erreur lors du placement de l'ordre de {symbol} : {e}")


    async def change_order(self, ID, amount, price, SL, TP):
        pass
        
        
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


    async def buy(self, symbol, amount, maxCost):
        """Achète directement une quantité d'une crypto"""
        
        try:
            order = await self.exchange.create_order(
                    symbol = symbol,
                    type = 'market',
                    side = 'buy',
                    amount = amount,
                    params = {"cost" : maxCost}
                )
            
            await self.save_and_print_position(symbol, 1)
            
        except Exception as e:
            print(f"Erreur lors de l'achat de {symbol} : {e}")
        
    
    async def sell(self, symbol, amount): # tested
        """Vend directement un nombre d'une crypto"""

        try:
            order = await self.exchange.create_order(
                symbol = symbol,
                type = 'market',
                side = 'sell',
                amount = amount,
            )
            
            await self.save_and_print_position(symbol, 1)

        except Exception as e:
            print(f"Erreur lors de la vente de {symbol} : {e}")


    async def close_all_positions(self): # not tested
        """Vend toutes les positions existantes"""
        
        try:
            order = await self.exchange.close_all_positions()
            
        except Exception as e:
            print(f"Erreur lors de la fermeture de toutes les positions : {e}")


    async def sell_percentage(self, symbol, percentage=100): # tested
        """Vend directement un pourcentage d'une crypto possédée"""

        try:
            base_currency = symbol.split('/')[0]
            balance = await self.exchange.fetch_balance()
            
            if base_currency not in balance['free']:
                print(f"Pas de {base_currency}")
                return

            available_amount = balance['free'].get(base_currency, 0)
            amount = available_amount * (percentage / 100)
            
            order = await self.exchange.create_order(
                symbol = symbol,
                type = 'market',
                side = 'sell',
                amount = amount,
            )
            
            print(order)

            await self.save_and_print_position(symbol, 1)

        except Exception as e:
            print(f"Erreur lors de la vente de {symbol} : {e}")



    async def save_and_print_positions(self, symbol, nb):
        """Sauvegarde la position dans la liste des positions et print les informations"""
        trades = await self.exchange.fetch_my_trades(symbol, limit=nb)
        
        with open(self.transaction_file, "a") as f:
            for trade in trades:
                f.write(f"{symbol}  {self.exchange.iso8601(trade['timestamp'])}\n")
                f.write(f"ID: {trade["id"]}, {trade["side"]}\nPrice: {trade['price']}")
                f.write(f"\nQuantity: {trade['amount']} = {self.mi.crypto_equivalence(trade['amount'], trade['price'])} €")
                f.write(f"\nCost: {trade['cost']} Fees: {trade['fee']['cost']} {trade['fee']['currency']}\n\n")
            
        
        
    


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
        trades = await self.exchange.fetch_my_trades(symbol, limit=1)
        print('\n' + symbol + " History : " + str(len(trades)))
        
        for trade in trades:
            print(f"ID: {trade['id']}, {trade['side']}\nPrice: {trade['price']}")
            print(f"Quantity: {trade['amount']} = {await self.mi.actual_crypto_equivalence(symbol, trade['amount'])} €")
            if trade['fee']['currency'] != 'EUR':
                print(f"Fees: {trade['fee']['cost']} {trade['fee']['currency']} = {await self.mi.actual_crypto_equivalence(trade['fee']['currency']+'/EUR', trade['fee']['cost'])} €")
            else:
                print(f"Fees: {trade['fee']['cost']} {trade['fee']['currency']}")
            print(f"Date: {self.exchange.iso8601(trade['timestamp'])}\n")


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
                    print(f"{elt['coin']}: {elt['available']} = {await self.mi.actual_crypto_equivalence(elt['coin'] + '/EUR', float(elt['available']))} €")
                else:
                    print(f"{elt['coin']}: {elt['available']} €")
        elif self.exchange.options['defaultType'] in ["future", "swap"]:
            balance = await self.exchange.fetch_balance()
            print(f"Wallet informations in {self.exchange.options['defaultType']}:")
            for elt in balance["info"]:
                print(f"{elt['marginCoin']}: {elt['available']}\naccountEquity: {elt['accountEquity']}\nusdtEquity: {elt['usdtEquity']}")       
        else:
            print("Wrong market mode for wallet informations")