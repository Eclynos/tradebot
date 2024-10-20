import matplotlib.pyplot as plt
import pandas as pd
import mplfinance as mpf
from account import Account
from tools import Tools


class MarketInformations:
    def __init__(self, tools) -> None:
        self.account = Account('info_keys')
        self.tools = tools


    async def init(self):
        await self.account.connect()
        self.exchange = self.account.exchange


    async def getAllSymbols(self):
        """Récupère et affiche tous les paires de trading disponibles sur l'échange"""
        await self.exchange.load_markets()
        markets = self.exchange.markets
        symbols = list(markets.keys())
        return symbols
    

    async def getBidPrice(self, symbol):
        try:
            ticker = await self.exchange.fetch_ticker(symbol)
            return ticker['bid']
            
        except Exception as e:
            print(f"Erreur lors de la récupération du prix de {symbol} : {e}")
            
            
    async def getAskPrice(self, symbol):
        try:
            ticker = await self.exchange.fetch_ticker(symbol)
            return ticker['ask']
            
        except Exception as e:
            print(f"Erreur lors de la récupération du prix de {symbol} : {e}")


    async def getPrice(self, symbol):
        """Donne le prix instantané d'un symbole par rapport à une monnaie."""
        try:
            ticker = await self.exchange.fetch_ticker(symbol)
            return ticker['last']
        except Exception as e:
            print(f"Erreur lors de la récupération du prix de {symbol} : {e}")


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


    async def actual_currency_equivalence(self, symbol, amount):
        """Calcule le montant équivalent d'une crypto à une monnaie en temps réel

        Args:
            symbol ('BTC/EUR'): Symbole de la paire de trading Crypto / monnaie d'échange
            amount: montant de la monnaie d'échange à calculer
        """
        price = await self.getPrice(symbol)
        return round(amount / price, 12)


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
        return round(amount / price, 9)


    def crypto_equivalence(self, amount, price):
        """Calcule le montant équivalent d'une monnaie à une crypto"""
        return amount * price
    

    async def fee(self, symbol):
        """Renvoie les prix de fees supposés donnés par bitget pour le type de market actuel sur un symbole"""
        fee = await self.exchange.fetch_trading_fee(symbol)
        print(f"{fee['symbol']} fee, maker: {fee['maker']} taker: {fee['taker']}")

   
    async def fetch_candles(self, symbol, timeFrame, since):
        """Récupère les bougies d'une paire de trading d'une fréquence depuis un temps donné en ms
        renvoie [timestamp, open, high, low, close, volume]"""

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
    
    
    async def curve_visualisation(self, symbol, timeFrame, since):
        """Affiche la courbe d'une timeFrame depuis un temps donné"""
        
        c = await self.fetch_candles(symbol, timeFrame, since)
        #plt.figure(figsize=(500,100), dpi=40)
        x = []
        y = []
        
        for candle in c:
            x.append(candle[0])
            y.append(candle[4])
        
        plt.plot(x, y, 'rs-', label=symbol)
        
        plt.title(f"{symbol} curve visualisation")
        
        plt.xlabel('Time')
        plt.ylabel('Price')
        plt.legend()
        plt.grid()
        plt.show()
        #plt.savefig(f"{symbol}.jpg")


    async def candlestick_visualisation(self, symbol, timeFrame, since):
            """Affiche les bougies d'une timeFrame depuis un temps donné"""
            
            candles = await self.fetch_candles(symbol, timeFrame, since)

            df = pd.DataFrame(candles, columns=['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])
            df['Date'] = pd.to_datetime(df['Timestamp'], unit='ms')
            df['Date'] = df['Date'] + pd.Timedelta(hours=2)
            df.set_index('Date', inplace=True)
            df.drop(columns='Timestamp', inplace=True)


            last_price = df['Close'].iloc[-1]
            apdict = mpf.make_addplot([last_price]*len(df), color='red', linestyle='--', secondary_y=False)

            fig, axlist = mpf.plot(df,
                                   type='candle',
                                   style='charles',
                                   volume=True,
                                   title=symbol,
                                   addplot=apdict,
                                   ylabel='Prix',
                                   returnfig=True
            )                      
            ax = axlist[0]

            ax.annotate(f'{last_price}', 
                        xy=(1, last_price), 
                        xycoords=('axes fraction', 'data'), 
                        xytext=(10, 0), textcoords='offset points',
                        color='red', fontsize=12, 
                        verticalalignment='center')

            plt.show()