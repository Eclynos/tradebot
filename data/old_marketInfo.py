import matplotlib.pyplot as plt
import pandas as pd
import mplfinance as mpf
from matplotlib.animation import FuncAnimation
from tools import *
from account import Account
from math import floor


class MarketInformations:
    def __init__(self) -> None:
        self.account = Account("info_keys")
        self.axlist = None
        self.running = True

        self.custom_style = mpf.make_mpf_style(
        base_mpf_style='charles',
        marketcolors=mpf.make_marketcolors(
            up='#1f77b4',
            down='#d62728',
            wick={'up': '#1f77b4', 'down': '#d62728'},
            edge={'up': '#1f77b4', 'down': '#d62728'},
            volume={'up': '#1f77b4', 'down': '#d62728'}
        )
        )


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
            ticker = await self.exchange.fetch_ticker(symbol + ":USDT")
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
            current_since = last_timestamp + time_frame_to_ms(timeFrame)

            if current_since >= timestamp:
                break
        
        return candles


    async def fetch_candles_amount(self, symbol, timeFrame, amount, time):
        """Récupère les dernières "amount" bougies d'une paire de trading d'une fréquence donnée
        renvoie [timestamp, open, high, low, close, volume]"""

        candles = []
        timestamp = floor(time * 1000)
        time_ago = timestamp - time_frame_to_ms(timeFrame) * amount
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
            current_since = last_timestamp + time_frame_to_ms(timeFrame)

            if current_since >= timestamp:
                break
        
        return candles
    

    async def before_last_candle(self, symbol, timeFrame, time): # time in ms
        """Fetch before last candle to fill a list of candles"""
        try:
            candles = await self.exchange.fetch_ohlcv(symbol, timeFrame, floor(time * 1000) - 2*time_frame_to_ms(timeFrame))
            if len(candles) == 1 or len(candles) == 2:
                return candles[0]
            elif len(candles) == 3:
                return candles[1]
            else:
                raise ValueError(candles, time)
        except Exception as e:
            raise ValueError(f"Error fetching candle\n{e}")


    async def two_before_last_candles(self, symbol, timeFrame, time): # time in ms
        """Fetch before last candle to fill a list of candles"""
        try:
            candles = await self.exchange.fetch_ohlcv(symbol, timeFrame, floor(time * 1000) - 3*time_frame_to_ms(timeFrame))
            if len(candles) == 2:
                return candles
            elif len(candles) == 3:
                return candles[:-1]
            elif len(candles) == 4:
                return candles[1:-1]
            else:
                raise ValueError(candles, time)
        except Exception as e:
            raise ValueError(f"Error fetching candle\n{e}")


    
    async def curve_visualisation(self, symbol, timeFrame, since):
        """Affiche la courbe d'une timeFrame depuis un temps donné"""
        
        c = await self.fetch_candles(symbol, timeFrame, since)
        x = []
        y = []
        
        for candle in c:
            x.append(candle[0])
            y.append(candle[4])
        
        plt.plot(x, y, 'r--', label=symbol)
        
        plt.title(f"{symbol} curve visualisation")
        
        plt.xlabel('Time')
        plt.ylabel('Price')
        plt.legend()
        plt.grid()
        plt.show()


    async def candlestick_visualisation(self, symbol, timeFrame, since):
            """Affiche les bougies d'une timeFrame depuis un temps donné"""
            
            candles = await self.fetch_candles(symbol, timeFrame, since)

            df = pd.DataFrame(candles, columns=['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])
            df['Date'] = pd.to_datetime(df['Timestamp'], unit='ms')
            df['Date'] = df['Date'] + pd.Timedelta(hours=2)
            df.set_index('Date', inplace=True)
            df.drop(columns='Timestamp', inplace=True)

            last_price = df['Close'].iloc[-1]

            fig, axlist = mpf.plot(df,
                                   type='candle',
                                   style='charles',
                                   volume=True,
                                   title=symbol,
                                   ylabel='Prix',
                                   returnfig=True
            )                      
            ax = axlist[0]

            ax.axhline(last_price, color='red', linestyle='--', linewidth=0.5)

            ax.annotate(f'{last_price}', 
                        xy=(0, last_price), 
                        xycoords=('axes fraction', 'data'), 
                        xytext=(10, 0), textcoords='offset points',
                        color='red', fontsize=12, 
                        verticalalignment='center')

            plt.show()


    async def fetch_and_update(self, symbol, timeFrame):
        """Récupère les bougies et met à jour les données"""

        new = await self.exchange.fetch_ohlcv(symbol,
                                              timeFrame,
                                              await self.exchange.fetch_time() - time_frame_to_ms(str(2 * int(timeFrame[:-1])) + timeFrame[-1]),
                                              2)

        if new[0][0] != self.candles[-2][0]:
            self.candles[-1] = new[0]
            self.candles.append(new[1])
        else:
            self.candles[-1] = new[1]
        
        self.df = pd.DataFrame(self.candles, columns=['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])
        self.df['Date'] = pd.to_datetime(self.df['Timestamp'], unit='ms')
        self.df['Date'] = self.df['Date'] + pd.Timedelta(hours=2)
        self.df.set_index('Date', inplace=True)
        self.df.drop(columns='Timestamp', inplace=True)


    def handle_close(self, event):
        """Gestionnaire d'événement pour arrêter la boucle lorsque la fenêtre est fermée"""
        self.running = False


    def update_chart(self, frame, symbol, timeFrame, since):
        """Met à jour le graphique"""

        if self.df is not None:
            last_price = self.df['Close'].iloc[-1]
            last_open = self.df['Open'].iloc[-1]
            line_color = '#1f77b4' if last_price > last_open else '#d62728'
            self.axlist[0].clear()

            mpf.plot(self.df, type='candle', style=self.custom_style, ax=self.axlist[0], volume=self.axlist[2])

            self.axlist[0].axhline(last_price, color=line_color, linestyle='--', linewidth=0.5)
            self.axlist[0].annotate(f'{last_price:.2f}', xy=(0, last_price), xycoords=('axes fraction', 'data'),
                                    xytext=(10, 0), textcoords='offset points', color=line_color, fontsize=12, verticalalignment='center')


    async def chart_visualisation(self, symbol, timeFrame, since, refresh_rate):
        """Montre en temps réel le graphique d'un symbole"""

        self.candles = await self.fetch_candles(symbol, timeFrame, since)
        
        self.df = pd.DataFrame(self.candles, columns=['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume'])
        self.df['Date'] = pd.to_datetime(self.df['Timestamp'], unit='ms')
        self.df['Date'] = self.df['Date'] + pd.Timedelta(hours=2)
        self.df.set_index('Date', inplace=True)
        self.df.drop(columns='Timestamp', inplace=True)

        refresh_rate = int(refresh_rate)
        last_price = self.df['Close'].iloc[-1]
        last_open = self.df['Open'].iloc[-1]
        line_color = '#1f77b4' if last_price > last_open else '#d62728'

        fig, self.axlist = mpf.plot(self.df,
                                    type='candle',
                                    style=self.custom_style,
                                    volume=True,
                                    title=symbol,
                                    ylabel='Prix',
                                    returnfig=True)
        
        fig.canvas.manager.set_window_title(f'{symbol} - Graphique en Temps Réel')
        fig.canvas.mpl_connect('close_event', self.handle_close)

        self.axlist[0].axhline(last_price, color=line_color, linestyle='--', linewidth=0.5)
        self.axlist[0].annotate(f'{last_price}', 
                                xy=(0, last_price),
                                xycoords=('axes fraction', 'data'),
                                xytext=(10, 0), textcoords='offset points',
                                color=line_color, fontsize=12,
                                verticalalignment='center')

        A = FuncAnimation(fig, self.update_chart, fargs=(symbol, timeFrame, since), interval=1000 * refresh_rate, cache_frame_data=False)

        while self.running:
            try:
                await self.fetch_and_update(symbol, timeFrame)
            except Exception as e:
                print(e)
            plt.pause(refresh_rate)

        plt.close()
