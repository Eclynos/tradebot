from wallet import Wallet
from marketInfo import MarketInformations
from tools import Tools
import asyncio, time


class Executer:
    def __init__(self) -> None:
        t = Tools()
        self.mi = MarketInformations()
        self.wallets = [Wallet("keys", False, self.mi)]

        self.symbol = "BTC/USDT"


    async def start(self):
        await self.mi.init()
        for w in self.wallets:
            await w.init()


    async def end(self):
        await self.mi.disconnect()
        for w in self.wallets:
            await w.disconnect()


    async def buy(self):
        for w in self.wallets:
            w.buy()
