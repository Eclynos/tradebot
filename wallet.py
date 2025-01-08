import time
from account import Account
from tools import left

class Wallet:
    def __init__(self, key_file, sandbox_mode, mi):
        self.account = Account(key_file)
        self.sandbox_mode = sandbox_mode
        self.transaction_file = "trade_logs/" + self.account.access_key[:11]
        self.orders = []
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
            self.exchange.options['type'] = mode
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
        try:
            await self.exchange.set_leverage(factor, symbol, params={"marginCoin": "USDT"})
        except Exception as e:
            raise ValueError(e)


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


    async def transfer_spot_to_swap(self, amount):
        """ Transfer USDT from Spot to Swap market """
        try:
            result = await self.exchange.transfer(
                code='USDT',
                amount=amount,
                fromAccount='spot',
                toAccount='swap'
            )

            return result

        except Exception as e:
            print(f"Error transferring {amount} USDT from spot to swap: {e}")
            return None


    async def transfer_swap_to_spot(self, amount):
        """ Transfer USDT from Swap to Spot market """
        try:
            result = await self.exchange.transfer(
                code='USDT',
                amount=amount,
                fromAccount='swap',
                toAccount='spot'
            )

            return result

        except Exception as e:
            print(f"Error transferring {amount} USDT from swap to spot: {e}")
            return None


# ORDER MANAGING


    async def limitOrder(self, symbol, BuyorSell, amount, price):
        """Place un ordre d'acheter ou vendre lorsque la crypto atteint un certain prix"""

        order = None
        order_id = str(time.time() * 1000)
        
        params = {
                "newClientOrderId" : "{}_limit_{}".format(order_id, BuyorSell),
                "timeInForceValue": 'normal',
                'type': self.exchange.options['defaultType']
        }

        try:
            order = await self.exchange.create_order(symbol, 'limit', BuyorSell, amount, price)
        except Exception as e:
            print(f"Erreur lors du placement de l'ordre de {symbol} :\n{e}")
            
        return order
        
        
    async def cancelOrder(self, symbol, order_id):
        """Tente de supprimer un ordre (!= vendre une position)"""
        try:
            response = await self.exchange.cancel_order(order_id, symbol)
            if response == None:
                print(f"Error deleting {order_id} order")
            else:
                print(f"{symbol} : {order_id} as been cancelled")
        except Exception as e:
            print("Order cancelling failed")
            print(e)
            
            
    async def cancelAllOrders(self, symbol):
        """Tente de supprimer tous les ordres (!= vendre toutes les positions)"""
        try:
            response = await self.exchange.cancel_all_orders(symbol)
            if response == None:
                print(f"Error deleting {symbol} order")
            else:
                print(f"All {symbol} orders as been cancelled")
        except Exception as e:
            print(e)


    async def buy(self, symbol, amount, cost):
        """Achète directement une quantité d'une crypto en spot"""
        
        try:
            order = await self.exchange.create_market_buy_order(
                symbol,
                amount,
                params = {'type': 'spot',
                          'cost': cost}
            )
            
            return order
            
        except Exception as e:
            print(f"Erreur lors de l'achat de {symbol} :\n{e}")


    async def buy_and_transfer(self, symbol, amount, cost):
        """Achète directement une quantité d'une crypto en spot puis transfère en swap"""

        try:
            order = await self.exchange.create_market_buy_order(
                symbol,
                amount,
                params = {'type': 'spot',
                          'cost': cost}
            )

            result = await self.exchange.transfer(
                code=left(symbol),
                amount=amount,
                fromAccount='spot',
                toAccount='swap'
            )

            print(result)

            return order


        except Exception as e:
            print(f"Erreur lors de l'achat et transfer de {symbol} :\n{e}")
        
    
    async def sell(self, symbol, amount):
        """Vend directement un nombre d'une crypto"""

        try:
            order = await self.exchange.create_order(symbol, 'market', 'sell', amount,
                                                     params={'type': 'spot'})
            
            return order

        except Exception as e:
            print(f"Erreur lors de la vente de {symbol} :\n{e}")


    async def sell_full(self, symbol):
        """Vend l'entièreté d'une position en spot et retourne le nombre vendu"""

        try:
            self.market_mode('spot')
            balance = await self.exchange.fetch_balance()
            amount = balance['free'][left(symbol)]

            order = await self.exchange.create_order(
                symbol=symbol,
                type='market',
                side='sell',
                amount=amount,
                params={'reduceOnly': True, 'type': 'spot'}
            )

            return order, amount
        
        except Exception as e:
            print(f"Erreur lors de la vente totale {amount} {symbol} :\n{e}")



    async def sell_percentage(self, symbol, percentage=100): #broken DONT USE
        """Vend directement un pourcentage d'une crypto possédée"""

        try:
            base_currency = left(symbol)
            balance = await self.exchange.fetch_balance()
            
            if base_currency not in balance['free']:
                raise ValueError(f"Pas de {base_currency}")

            available_amount = balance['free'].get(base_currency, 0)
            amount = available_amount * (percentage / 100)
            
            order = await self.exchange.create_order(symbol, 'market', 'sell', amount, params={'reduceOnly':True, 'type': 'spot'})
            
            return order

        except Exception as e:
            print(f"Erreur lors de la vente de {symbol} :\n{e}")
    
    
    async def sell_all(self):
        """Vend directement tout le capital en USDT -> fonction de sécurité"""
        
        try:
            balance = await self.exchange.fetch_balance()
            for coin in balance['total'].keys():
                if coin != "EUR" and coin != "USDT" and await self.mi.actual_crypto_equivalence(coin + "/USDT", balance['total'][coin]) > 0.15:
                    await self.exchange.create_market_sell_order(coin + "/USDT", balance['total'][coin])
            
        except Exception as e:
            print(f"Erreur lors de la vente de tous les actifs:\n{e}")


    async def openp(self, symbol, amount, direction):
        """ Open a future/swap position """
        try:

            order = await self.exchange.create_order(
                symbol = symbol + ':USDT',
                type = 'market',
                side = direction,
                amount = amount,
                params = {'type': 'swap', 
                          "oneWayMode": False}
            )
            return order

        except Exception as e:
            print(f"Error opening swap position: {e}")


    async def closep(self, symbol):
        """ Close a futures/swap position """
        try:
            order = await self.exchange.close_position(
                symbol = symbol + ':USDT',
                params = {'type': 'swap'}
            )
            
            return order
            
        except Exception as e:
            print(f"Error closing swap position: {e}")


    async def close_all_p(self):
        """Ferme toutes les positions existantes"""
        
        try:
            await self.exchange.close_all_positions()
            
        except Exception as e:
            print(f"Erreur lors de la fermeture de toutes les positions :\n{e}")


    async def save_and_print_positions(self, symbol, nb=None):
        """Sauvegarde la position dans le fichier des positions"""
        trades = await self.exchange.fetch_my_trades(symbol, limit=nb)
        
        with open(self.transaction_file, "a") as f:
            for trade in trades:
                f.write(f"{symbol}  {self.exchange.iso8601(trade['timestamp'])}\n")
                f.write(f"ID: {trade['id']}, {trade['side']}\nPrice: {trade['price']}")
                f.write(f"\nQuantity: {trade['amount']} = {self.mi.crypto_equivalence(trade['amount'], trade['price'])} €")
                f.write(f"\nCost: {trade['cost']} Fees: {trade['fee']['cost']:.9f} {trade['fee']['currency']}\n\n")


# WATCH WALLET INFORMATIONS



    async def get_crossed_max_available(self):
        free = await self.exchange.fetch_free_balance()
        return free['USDT']
        """
        balance = await self.exchange.fetch_balance()
        return float(balance['info'][0]['crossedMaxAvailable'])
        """


    async def get_crossed_total_available(self):
        total = await self.exchange.fetch_total_balance()
        return total['USDT']


    async def checkPositions(self): # À tester 
        """Vérifie les positions ouvertes sur le compte.
        Les positions peuvent être les achats en future / margin / swap
        ou les ordres d'achat / vente qui n'ont pas encore abouti"""
        try:
            positions = await self.exchange.fetch_positions()
            if positions:
                print("Positions ouvertes :")
                for p in positions:
                    print(f"{p['entryPrice']} {p['symbol']}")
                    print(f"ID: {p['id']}, {p['side']}")
                    print(f"Leverage: {p['leverage']}, LiquidationPrice: {p['liquidationPrice']}")
                    print(f"Pnl: {p['unrealizedPnl']}") #PnL = Profit and Loss
            else:
                print("Aucune position ouverte.")
        except Exception as e:
            print(f"Erreur lors de la récupération des positions actuelles : {e}")


    async def positionsHistory(self, symbol, limit=20):
        """Retourne l'historique des positions prises en swap / future"""

        h = ""

        try:
            positions = await self.exchange.fetch_position_history(
                symbol=symbol+':USDT',
                limit=limit
            )

            for p in positions:
                h += f"{p['symbol']} {p['side']}\n"
                #h += f"{p['datetime']}\n"
                h += f"{p['info']['openTotalPos']} {symbol}\n"
                h += f"Open: {p['info']['openAvgPrice']} Close: {p['info']['closeAvgPrice']}\n"
                h += f"Pnl: {p['info']['pnl']} netProfit: {p['info']['netProfit']}\n"
                h += f"Openfee: {p['info']['openFee']} Closefee: {p['info']['closeFee']}\n Funding fee: {p['info']['totalFunding']}"

            return h

        except Exception as e:
            print(f"Erreur lors de la récupération de l'historique des positions : {e}")


    async def last_position(self, symbol, timestamp):
        """Retourne une position et son pnl %"""

        h = ""

        try:
            positions = await self.exchange.fetch_position_history(
                symbol=symbol+':USDT',
                limit=1
            )

            if positions == []:
                return "", 0

            for p in positions:
                if int(p['timestamp']) < timestamp - 300:
                    print("too old position")
                    return "", 0
                h += f"{p['symbol']} {p['side']}\n"
                #h += f"{p['datetime']}\n"
                h += f"{p['info']['openTotalPos']} {symbol}\n"
                h += f"Open: {p['info']['openAvgPrice']} Close: {p['info']['closeAvgPrice']}\n"
                h += f"Pnl: {p['info']['pnl']} netProfit: {p['info']['netProfit']}\n"
                h += f"Openfee: {p['info']['openFee']} Closefee: {p['info']['closeFee']}\n Funding fee: {p['info']['totalFunding']}"

            open_price = float(p['info']['openAvgPrice'])
            close_price = float(p['info']['closeAvgPrice'])
            percentage_pnl = (close_price - open_price) / open_price - (close_price * float(p['info']['closeFee']) + open_price * float(p['info']['openFee']))
            return h, percentage_pnl

        except Exception as e:
            print(f"Erreur lors de la récupération de la dernière position : {e}")
            return "", 0


    async def transactionHistory(self, symbol, limit=None):
        """Donne l'historique des trades sur une paire en spot"""
        trades = await self.exchange.fetch_my_trades(symbol, limit = limit)
        print('\n' + symbol + " History : " + str(len(trades)))
        
        for trade in trades:
            print(f"ID: {trade['id']}, {trade['side']}\nPrice: {trade['price']}")
            print(f"Quantity: {trade['amount']} = {await self.mi.actual_crypto_equivalence(symbol, trade['amount'])} €")
            if trade['fee']['currency'] != 'EUR':
                print(f"Fees: {trade['fee']['cost']} {trade['fee']['currency']} = {await self.mi.actual_crypto_equivalence(trade['fee']['currency']+'/EUR', trade['fee']['cost'])} €")
            else:
                print(f"Fees: {trade['fee']['cost']} {trade['fee']['currency']}")
            print(f"Date: {self.exchange.iso8601(trade['timestamp'])}\n")


    async def walletInformations(self):
        """Donne les montants possédés dans chaque cryptomonnaie en spot"""
        
        if self.exchange.options['defaultType'] == "spot":
            balance = await self.exchange.fetch_balance()
            print("Wallet informations in spot:")
            for elt in balance["info"]:
                if elt['coin'] == 'EUR':
                    print(f"{elt['coin']}: {elt['available']} €")
                elif elt['coin'] != 'USDT':
                    print(f"{elt['coin']}: {elt['available']} = {await self.mi.actual_crypto_equivalence(elt['coin'] + '/USDT', float(elt['available']))} USDT")
                else:
                    print(f"{elt['coin']}: {elt['available']} = {await self.mi.actual_crypto_equivalence('USDT/EUR', float(elt['available']))} €")
        elif self.exchange.options['defaultType'] in ["future", "swap"]:
            balance = await self.exchange.fetch_balance()
            print(f"Wallet informations in {self.exchange.options['defaultType']}:")
            for elt in balance["info"]:
                print(f"{elt['marginCoin']}: {elt['available']}\naccountEquity: {elt['accountEquity']}\nusdtEquity: {elt['usdtEquity']}")       
        else:
            print("Wrong market mode for wallet informations")