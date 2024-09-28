from ccxt.base.exchange import Exchange
from ccxt.abstract.bitget import ImplicitAPI
import hashlib
import json
from ccxt.base.types import Balances, Conversion, CrossBorrowRate, Currencies, Currency, FundingHistory, Int, IsolatedBorrowRate, LedgerEntry, Leverage, LeverageTier, Liquidation, MarginMode, MarginModification, Market, Num, Order, OrderBook, OrderRequest, OrderSide, OrderType, Position, Str, Strings, Ticker, Tickers, Trade, TradingFeeInterface, TradingFees, Transaction, TransferEntry
from typing import List
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import PermissionDenied
from ccxt.base.errors import AccountSuspended
from ccxt.base.errors import ArgumentsRequired
from ccxt.base.errors import BadRequest
from ccxt.base.errors import BadSymbol
from ccxt.base.errors import InsufficientFunds
from ccxt.base.errors import InvalidAddress
from ccxt.base.errors import InvalidOrder
from ccxt.base.errors import OrderNotFound
from ccxt.base.errors import NotSupported
from ccxt.base.errors import DDoSProtection
from ccxt.base.errors import RateLimitExceeded
from ccxt.base.errors import ExchangeNotAvailable
from ccxt.base.errors import OnMaintenance
from ccxt.base.errors import InvalidNonce
from ccxt.base.errors import RequestTimeout
from ccxt.base.errors import CancelPending
from ccxt.base.decimal_to_precision import TICK_SIZE
from ccxt.base.precise import Precise


class bitget(Exchange, ImplicitAPI):

    def describe(self):
        return self.deep_extend(super(bitget, self).describe(), {
            'id': 'bitget',
            'name': 'Bitget',
            'countries': ['SG'],
            'version': 'v2',
            'rateLimit': 50,  # up to 3000 requests per 5 minutes ≈ 600 requests per minute ≈ 10 requests per second ≈ 100 ms
            'certified': True,
            'pro': True,
            'has': {
                'CORS': None,
                'spot': True,
                'margin': True,
                'swap': True,
                'future': True,
                'option': False,
                'addMargin': True,
                'borrowCrossMargin': True,
                'borrowIsolatedMargin': True,
                'cancelAllOrders': True,
                'cancelOrder': True,
                'cancelOrders': True,
                'closeAllPositions': True,
                'closePosition': True,
                'createConvertTrade': True,
                'createDepositAddress': False,
                'createMarketBuyOrderWithCost': True,
                'createMarketOrderWithCost': False,
                'createMarketSellOrderWithCost': False,
                'createOrder': True,
                'createOrders': True,
                'createOrderWithTakeProfitAndStopLoss': True,
                'createPostOnlyOrder': True,
                'createReduceOnlyOrder': False,
                'createStopLimitOrder': True,
                'createStopLossOrder': True,
                'createStopMarketOrder': True,
                'createStopOrder': True,
                'createTakeProfitOrder': True,
                'createTrailingAmountOrder': False,
                'createTrailingPercentOrder': True,
                'createTriggerOrder': True,
                'editOrder': True,
                'fetchAccounts': False,
                'fetchBalance': True,
                'fetchBorrowInterest': True,
                'fetchBorrowRateHistories': False,
                'fetchBorrowRateHistory': False,
                'fetchCanceledAndClosedOrders': True,
                'fetchCanceledOrders': True,
                'fetchClosedOrders': True,
                'fetchConvertCurrencies': True,
                'fetchConvertQuote': True,
                'fetchConvertTrade': False,
                'fetchConvertTradeHistory': True,
                'fetchCrossBorrowRate': True,
                'fetchCrossBorrowRates': False,
                'fetchCurrencies': True,
                'fetchDeposit': False,
                'fetchDepositAddress': True,
                'fetchDepositAddresses': False,
                'fetchDeposits': True,
                'fetchDepositsWithdrawals': False,
                'fetchDepositWithdrawFee': 'emulated',
                'fetchDepositWithdrawFees': True,
                'fetchFundingHistory': True,
                'fetchFundingRate': True,
                'fetchFundingRateHistory': True,
                'fetchFundingRates': False,
                'fetchIndexOHLCV': True,
                'fetchIsolatedBorrowRate': True,
                'fetchIsolatedBorrowRates': False,
                'fetchLedger': True,
                'fetchLeverage': True,
                'fetchLeverageTiers': False,
                'fetchLiquidations': False,
                'fetchMarginAdjustmentHistory': False,
                'fetchMarginMode': True,
                'fetchMarketLeverageTiers': True,
                'fetchMarkets': True,
                'fetchMarkOHLCV': True,
                'fetchMyLiquidations': True,
                'fetchMyTrades': True,
                'fetchOHLCV': True,
                'fetchOpenInterest': True,
                'fetchOpenInterestHistory': False,
                'fetchOpenOrders': True,
                'fetchOrder': True,
                'fetchOrderBook': True,
                'fetchOrderBooks': False,
                'fetchOrders': False,
                'fetchOrderTrades': False,
                'fetchPosition': True,
                'fetchPositionHistory': 'emulated',
                'fetchPositionMode': False,
                'fetchPositions': True,
                'fetchPositionsHistory': True,
                'fetchPositionsRisk': False,
                'fetchPremiumIndexOHLCV': False,
                'fetchStatus': False,
                'fetchTicker': True,
                'fetchTickers': True,
                'fetchTime': True,
                'fetchTrades': True,
                'fetchTradingFee': True,
                'fetchTradingFees': True,
                'fetchTransactions': False,
                'fetchTransfer': False,
                'fetchTransfers': True,
                'fetchWithdrawAddresses': False,
                'fetchWithdrawal': False,
                'fetchWithdrawals': True,
                'reduceMargin': True,
                'repayCrossMargin': True,
                'repayIsolatedMargin': True,
                'setLeverage': True,
                'setMargin': False,
                'setMarginMode': True,
                'setPositionMode': True,
                'signIn': False,
                'transfer': True,
                'withdraw': True,
            },
            'timeframes': {
                '1m': '1m',
                '3m': '3m',
                '5m': '5m',
                '15m': '15m',
                '30m': '30m',
                '1h': '1h',
                '2h': '2h',
                '4h': '4h',
                '6h': '6h',
                '12h': '12h',
                '1d': '1d',
                '3d': '3d',
                '1w': '1w',
                '1M': '1m',
            },
            'hostname': 'bitget.com',
            'urls': {
                'logo': 'https://user-images.githubusercontent.com/1294454/195989417-4253ddb0-afbe-4a1c-9dea-9dbcd121fa5d.jpg',
                'api': {
                    'spot': 'https://api.{hostname}',
                    'mix': 'https://api.{hostname}',
                    'user': 'https://api.{hostname}',
                    'p2p': 'https://api.{hostname}',
                    'broker': 'https://api.{hostname}',
                    'margin': 'https://api.{hostname}',
                    'common': 'https://api.{hostname}',
                    'tax': 'https://api.{hostname}',
                    'convert': 'https://api.{hostname}',
                    'copy': 'https://api.{hostname}',
                    'earn': 'https://api.{hostname}',
                },
                'www': 'https://www.bitget.com',
                'doc': [
                    'https://www.bitget.com/api-doc/common/intro',
                    'https://www.bitget.com/api-doc/spot/intro',
                    'https://www.bitget.com/api-doc/contract/intro',
                    'https://www.bitget.com/api-doc/broker/intro',
                    'https://www.bitget.com/api-doc/margin/intro',
                    'https://www.bitget.com/api-doc/copytrading/intro',
                    'https://www.bitget.com/api-doc/earn/intro',
                    'https://bitgetlimited.github.io/apidoc/en/mix',
                    'https://bitgetlimited.github.io/apidoc/en/spot',
                    'https://bitgetlimited.github.io/apidoc/en/broker',
                    'https://bitgetlimited.github.io/apidoc/en/margin',
                ],
                'fees': 'https://www.bitget.cc/zh-CN/rate?tab=1',
                'referral': 'https://www.bitget.com/expressly?languageType=0&channelCode=ccxt&vipCode=tg9j',
            },
            'api': {
                'public': {
                    'common': {
                        'get': {
                            'v2/public/annoucements': 1,
                            'v2/public/time': 1,
                        },
                    },
                    'spot': {
                        'get': {
                            'spot/v1/notice/queryAllNotices': 1,  # 20 times/1s(IP) => 20/20 = 1
                            'spot/v1/public/time': 1,
                            'spot/v1/public/currencies': 6.6667,  # 3 times/1s(IP) => 20/3 = 6.6667
                            'spot/v1/public/products': 1,
                            'spot/v1/public/product': 1,
                            'spot/v1/market/ticker': 1,
                            'spot/v1/market/tickers': 1,
                            'spot/v1/market/fills': 2,  # 10 times/1s(IP) => 20/10 = 2
                            'spot/v1/market/fills-history': 2,
                            'spot/v1/market/candles': 1,
                            'spot/v1/market/depth': 1,
                            'spot/v1/market/spot-vip-level': 2,
                            'spot/v1/market/merge-depth': 1,
                            'spot/v1/market/history-candles': 1,
                            'spot/v1/public/loan/coinInfos': 2,  # 10 times/1s(IP) => 20/10 = 2
                            'spot/v1/public/loan/hour-interest': 2,  # 10 times/1s(IP) => 20/10 = 2
                            'v2/spot/public/coins': 6.6667,
                            'v2/spot/public/symbols': 1,
                            'v2/spot/market/vip-fee-rate': 2,
                            'v2/spot/market/tickers': 1,
                            'v2/spot/market/merge-depth': 1,
                            'v2/spot/market/orderbook': 1,
                            'v2/spot/market/candles': 1,
                            'v2/spot/market/history-candles': 1,
                            'v2/spot/market/fills': 2,
                            'v2/spot/market/fills-history': 2,
                        },
                    },
                    'mix': {
                        'get': {
                            'mix/v1/market/contracts': 1,
                            'mix/v1/market/depth': 1,
                            'mix/v1/market/ticker': 1,
                            'mix/v1/market/tickers': 1,
                            'mix/v1/market/contract-vip-level': 2,
                            'mix/v1/market/fills': 1,
                            'mix/v1/market/fills-history': 2,
                            'mix/v1/market/candles': 1,
                            'mix/v1/market/index': 1,
                            'mix/v1/market/funding-time': 1,
                            'mix/v1/market/history-fundRate': 1,
                            'mix/v1/market/current-fundRate': 1,
                            'mix/v1/market/open-interest': 1,
                            'mix/v1/market/mark-price': 1,
                            'mix/v1/market/symbol-leverage': 1,
                            'mix/v1/market/queryPositionLever': 1,
                            'mix/v1/market/open-limit': 1,
                            'mix/v1/market/history-candles': 1,
                            'mix/v1/market/history-index-candles': 1,
                            'mix/v1/market/history-mark-candles': 1,
                            'mix/v1/market/merge-depth': 1,
                            'v2/mix/market/vip-fee-rate': 2,
                            'v2/mix/market/merge-depth': 1,
                            'v2/mix/market/ticker': 1,
                            'v2/mix/market/tickers': 1,
                            'v2/mix/market/fills': 1,
                            'v2/mix/market/fills-history': 2,
                            'v2/mix/market/candles': 1,
                            'v2/mix/market/history-candles': 1,
                            'v2/mix/market/history-index-candles': 1,
                            'v2/mix/market/history-mark-candles': 1,
                            'v2/mix/market/open-interest': 1,
                            'v2/mix/market/funding-time': 1,
                            'v2/mix/market/symbol-price': 1,
                            'v2/mix/market/history-fund-rate': 1,
                            'v2/mix/market/current-fund-rate': 1,
                            'v2/mix/market/contracts': 1,
                            'v2/mix/market/query-position-lever': 2,
                        },
                    },
                    'margin': {
                        'get': {
                            'margin/v1/cross/public/interestRateAndLimit': 2,  # 10 times/1s(IP) => 20/10 = 2
                            'margin/v1/isolated/public/interestRateAndLimit': 2,  # 10 times/1s(IP) => 20/10 = 2
                            'margin/v1/cross/public/tierData': 2,  # 10 times/1s(IP) => 20/10 = 2
                            'margin/v1/isolated/public/tierData': 2,  # 10 times/1s(IP) => 20/10 = 2
                            'margin/v1/public/currencies': 1,  # 20 times/1s(IP) => 20/20 = 1
                            'v2/margin/currencies': 2,
                        },
                    },
                    'earn': {
                        'get': {
                            'v2/earn/loan/public/coinInfos': 2,
                            'v2/earn/loan/public/hour-interest': 2,
                        },
                    },
                },
                'private': {
                    'spot': {
                        'get': {
                            'spot/v1/wallet/deposit-address': 4,
                            'spot/v1/wallet/withdrawal-list': 1,
                            'spot/v1/wallet/deposit-list': 1,
                            'spot/v1/account/getInfo': 20,
                            'spot/v1/account/assets': 2,
                            'spot/v1/account/assets-lite': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'spot/v1/account/transferRecords': 1,  # 20 times/1s(UID) => 20/20 = 1
                            'spot/v1/convert/currencies': 2,
                            'spot/v1/convert/convert-record': 2,
                            'spot/v1/loan/ongoing-orders': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'spot/v1/loan/repay-history': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'spot/v1/loan/revise-history': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'spot/v1/loan/borrow-history': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'spot/v1/loan/debts': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'v2/spot/trade/orderInfo': 1,
                            'v2/spot/trade/unfilled-orders': 1,
                            'v2/spot/trade/history-orders': 1,
                            'v2/spot/trade/fills': 2,
                            'v2/spot/trade/current-plan-order': 1,
                            'v2/spot/trade/history-plan-order': 1,
                            'v2/spot/account/info': 20,
                            'v2/spot/account/assets': 2,
                            'v2/spot/account/subaccount-assets': 2,
                            'v2/spot/account/bills': 2,
                            'v2/spot/account/transferRecords': 1,
                            'v2/account/funding-assets': 2,
                            'v2/account/bot-assets': 2,
                            'v2/account/all-account-balance': 20,
                            'v2/spot/wallet/deposit-address': 2,
                            'v2/spot/wallet/deposit-records': 2,
                            'v2/spot/wallet/withdrawal-records': 2,
                        },
                        'post': {
                            'spot/v1/wallet/transfer': 4,
                            'spot/v1/wallet/transfer-v2': 4,
                            'spot/v1/wallet/subTransfer': 10,
                            'spot/v1/wallet/withdrawal': 4,
                            'spot/v1/wallet/withdrawal-v2': 4,
                            'spot/v1/wallet/withdrawal-inner': 4,
                            'spot/v1/wallet/withdrawal-inner-v2': 4,
                            'spot/v1/account/sub-account-spot-assets': 200,
                            'spot/v1/account/bills': 2,
                            'spot/v1/trade/orders': 2,
                            'spot/v1/trade/batch-orders': 4,
                            'spot/v1/trade/cancel-order': 2,
                            'spot/v1/trade/cancel-order-v2': 2,
                            'spot/v1/trade/cancel-symbol-order': 2,
                            'spot/v1/trade/cancel-batch-orders': 4,
                            'spot/v1/trade/cancel-batch-orders-v2': 4,
                            'spot/v1/trade/orderInfo': 1,
                            'spot/v1/trade/open-orders': 1,
                            'spot/v1/trade/history': 1,
                            'spot/v1/trade/fills': 1,
                            'spot/v1/plan/placePlan': 1,
                            'spot/v1/plan/modifyPlan': 1,
                            'spot/v1/plan/cancelPlan': 1,
                            'spot/v1/plan/currentPlan': 1,
                            'spot/v1/plan/historyPlan': 1,
                            'spot/v1/plan/batchCancelPlan': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'spot/v1/convert/quoted-price': 4,
                            'spot/v1/convert/trade': 4,
                            'spot/v1/loan/borrow': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'spot/v1/loan/repay': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'spot/v1/loan/revise-pledge': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'spot/v1/trace/order/orderCurrentList': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'spot/v1/trace/order/orderHistoryList': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'spot/v1/trace/order/closeTrackingOrder': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'spot/v1/trace/order/updateTpsl': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'spot/v1/trace/order/followerEndOrder': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'spot/v1/trace/order/spotInfoList': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'spot/v1/trace/config/getTraderSettings': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'spot/v1/trace/config/getFollowerSettings': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'spot/v1/trace/user/myTraders': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'spot/v1/trace/config/setFollowerConfig': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'spot/v1/trace/user/myFollowers': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'spot/v1/trace/config/setProductCode': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'spot/v1/trace/user/removeTrader': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'spot/v1/trace/getRemovableFollower': 2,
                            'spot/v1/trace/user/removeFollower': 2,
                            'spot/v1/trace/profit/totalProfitInfo': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'spot/v1/trace/profit/totalProfitList': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'spot/v1/trace/profit/profitHisList': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'spot/v1/trace/profit/profitHisDetailList': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'spot/v1/trace/profit/waitProfitDetailList': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'spot/v1/trace/user/getTraderInfo': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'v2/spot/trade/place-order': 2,
                            'v2/spot/trade/cancel-order': 2,
                            'v2/spot/trade/batch-orders': 20,
                            'v2/spot/trade/batch-cancel-order': 2,
                            'v2/spot/trade/cancel-symbol-order': 4,
                            'v2/spot/trade/place-plan-order': 1,
                            'v2/spot/trade/modify-plan-order': 1,
                            'v2/spot/trade/cancel-plan-order': 1,
                            'v2/spot/trade/batch-cancel-plan-order': 2,
                            'v2/spot/wallet/transfer': 2,
                            'v2/spot/wallet/subaccount-transfer': 2,
                            'v2/spot/wallet/withdrawal': 2,
                            'v2/spot/wallet/cancel-withdrawal': 2,
                            'v2/spot/wallet/modify-deposit-account': 2,
                        },
                    },
                    'mix': {
                        'get': {
                            'mix/v1/account/account': 2,
                            'mix/v1/account/accounts': 2,
                            'mix/v1/position/singlePosition': 2,
                            'mix/v1/position/singlePosition-v2': 2,
                            'mix/v1/position/allPosition': 4,  # 5 times/1s(UID) => 20/5 = 4
                            'mix/v1/position/allPosition-v2': 4,  # 5 times/1s(UID) => 20/5 = 4
                            'mix/v1/position/history-position': 1,
                            'mix/v1/account/accountBill': 2,
                            'mix/v1/account/accountBusinessBill': 4,
                            'mix/v1/order/current': 1,  # 20 times/1s(UID) => 20/20 = 1
                            'mix/v1/order/marginCoinCurrent': 1,  # 20 times/1s(UID) => 20/20 = 1
                            'mix/v1/order/history': 2,
                            'mix/v1/order/historyProductType': 4,  # 5 times/1s(UID) => 20/5 = 4
                            'mix/v1/order/detail': 2,
                            'mix/v1/order/fills': 2,
                            'mix/v1/order/allFills': 2,
                            'mix/v1/plan/currentPlan': 1,  # 20 times/1s(UID) => 20/20 = 1
                            'mix/v1/plan/historyPlan': 2,
                            'mix/v1/trace/currentTrack': 2,
                            'mix/v1/trace/followerOrder': 2,
                            'mix/v1/trace/followerHistoryOrders': 2,
                            'mix/v1/trace/historyTrack': 2,
                            'mix/v1/trace/summary': 1,  # 20 times/1s(UID) => 20/20 = 1
                            'mix/v1/trace/profitSettleTokenIdGroup': 1,  # 20 times/1s(UID) => 20/20 = 1
                            'mix/v1/trace/profitDateGroupList': 1,  # 20 times/1s(UID) => 20/20 = 1
                            'mix/v1/trade/profitDateList': 2,
                            'mix/v1/trace/waitProfitDateList': 1,  # 20 times/1s(UID) => 20/20 = 1
                            'mix/v1/trace/traderSymbols': 1,  # 20 times/1s(UID) => 20/20 = 1
                            'mix/v1/trace/traderList': 2,
                            'mix/v1/trace/traderDetail': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'mix/v1/trace/queryTraceConfig': 2,
                            'v2/mix/account/account': 2,
                            'v2/mix/account/accounts': 2,
                            'v2/mix/account/sub-account-assets': 200,
                            'v2/mix/account/open-count': 2,
                            'v2/mix/account/bill': 2,
                            'v2/mix/market/query-position-lever': 2,
                            'v2/mix/position/single-position': 2,
                            'v2/mix/position/all-position': 4,
                            'v2/mix/position/history-position': 1,
                            'v2/mix/order/detail': 2,
                            'v2/mix/order/fills': 2,
                            'v2/mix/order/fill-history': 2,
                            'v2/mix/order/orders-pending': 2,
                            'v2/mix/order/orders-history': 2,
                            'v2/mix/order/orders-plan-pending': 2,
                            'v2/mix/order/orders-plan-history': 2,
                        },
                        'post': {
                            'mix/v1/account/sub-account-contract-assets': 200,  # 0.1 times/1s(UID) => 20/0.1 = 200
                            'mix/v1/account/open-count': 1,
                            'mix/v1/account/setLeverage': 4,  # 5 times/1s(UID) => 20/5 = 4
                            'mix/v1/account/setMargin': 4,  # 5 times/1s(UID) => 20/5 = 4
                            'mix/v1/account/setMarginMode': 4,  # 5 times/1s(UID) => 20/5 = 4
                            'mix/v1/account/setPositionMode': 4,  # 5 times/1s(UID) => 20/5 = 4
                            'mix/v1/order/placeOrder': 2,
                            'mix/v1/order/batch-orders': 2,
                            'mix/v1/order/cancel-order': 2,
                            'mix/v1/order/cancel-batch-orders': 2,
                            'mix/v1/order/modifyOrder': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'mix/v1/order/cancel-symbol-orders': 2,
                            'mix/v1/order/cancel-all-orders': 2,
                            'mix/v1/order/close-all-positions': 20,
                            'mix/v1/plan/placePlan': 2,
                            'mix/v1/plan/modifyPlan': 2,
                            'mix/v1/plan/modifyPlanPreset': 2,
                            'mix/v1/plan/placeTPSL': 2,
                            'mix/v1/plan/placeTrailStop': 2,
                            'mix/v1/plan/placePositionsTPSL': 2,
                            'mix/v1/plan/modifyTPSLPlan': 2,
                            'mix/v1/plan/cancelPlan': 2,
                            'mix/v1/plan/cancelSymbolPlan': 2,
                            'mix/v1/plan/cancelAllPlan': 2,
                            'mix/v1/trace/closeTrackOrder': 2,
                            'mix/v1/trace/modifyTPSL': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'mix/v1/trace/closeTrackOrderBySymbol': 2,
                            'mix/v1/trace/setUpCopySymbols': 2,
                            'mix/v1/trace/followerSetBatchTraceConfig': 2,
                            'mix/v1/trace/followerCloseByTrackingNo': 2,
                            'mix/v1/trace/followerCloseByAll': 2,
                            'mix/v1/trace/followerSetTpsl': 2,
                            'mix/v1/trace/cancelCopyTrader': 4,  # 5 times/1s(UID) => 20/5 = 4
                            'mix/v1/trace/traderUpdateConfig': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'mix/v1/trace/myTraderList': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'mix/v1/trace/myFollowerList': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'mix/v1/trace/removeFollower': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'mix/v1/trace/public/getFollowerConfig': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'mix/v1/trace/report/order/historyList': 2,  # 10 times/1s(IP) => 20/10 = 2
                            'mix/v1/trace/report/order/currentList': 2,  # 10 times/1s(IP) => 20/10 = 2
                            'mix/v1/trace/queryTraderTpslRatioConfig': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'mix/v1/trace/traderUpdateTpslRatioConfig': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'v2/mix/account/set-leverage': 4,
                            'v2/mix/account/set-margin': 4,
                            'v2/mix/account/set-margin-mode': 4,
                            'v2/mix/account/set-position-mode': 4,
                            'v2/mix/order/place-order': 2,
                            'v2/mix/order/click-backhand': 20,
                            'v2/mix/order/batch-place-order': 20,
                            'v2/mix/order/modify-order': 2,
                            'v2/mix/order/cancel-order': 2,
                            'v2/mix/order/batch-cancel-orders': 2,
                            'v2/mix/order/close-positions': 20,
                            'v2/mix/order/place-tpsl-order': 2,
                            'v2/mix/order/place-plan-order': 2,
                            'v2/mix/order/modify-tpsl-order': 2,
                            'v2/mix/order/modify-plan-order': 2,
                            'v2/mix/order/cancel-plan-order': 2,
                        },
                    },
                    'user': {
                        'get': {
                            'user/v1/fee/query': 2,
                            'user/v1/sub/virtual-list': 2,
                            'user/v1/sub/virtual-api-list': 2,
                            'user/v1/tax/spot-record': 1,
                            'user/v1/tax/future-record': 1,
                            'user/v1/tax/margin-record': 1,
                            'user/v1/tax/p2p-record': 1,
                            'v2/user/virtual-subaccount-list': 2,
                            'v2/user/virtual-subaccount-apikey-list': 2,
                        },
                        'post': {
                            'user/v1/sub/virtual-create': 4,
                            'user/v1/sub/virtual-modify': 4,
                            'user/v1/sub/virtual-api-batch-create': 20,  # 1 times/1s(UID) => 20/1 = 20
                            'user/v1/sub/virtual-api-create': 4,
                            'user/v1/sub/virtual-api-modify': 4,
                            'v2/user/create-virtual-subaccount': 4,
                            'v2/user/modify-virtual-subaccount': 4,
                            'v2/user/batch-create-subaccount-and-apikey': 20,
                            'v2/user/create-virtual-subaccount-apikey': 4,
                            'v2/user/modify-virtual-subaccount-apikey': 4,
                        },
                    },
                    'p2p': {
                        'get': {
                            'p2p/v1/merchant/merchantList': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'p2p/v1/merchant/merchantInfo': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'p2p/v1/merchant/advList': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'p2p/v1/merchant/orderList': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'v2/p2p/merchantList': 2,
                            'v2/p2p/merchantInfo': 2,
                            'v2/p2p/orderList': 2,
                            'v2/p2p/advList': 2,
                        },
                    },
                    'broker': {
                        'get': {
                            'broker/v1/account/info': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'broker/v1/account/sub-list': 20,  # 1 times/1s(UID) => 20/1 = 20
                            'broker/v1/account/sub-email': 20,  # 1 times/1s(UID) => 20/1 = 20
                            'broker/v1/account/sub-spot-assets': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'broker/v1/account/sub-future-assets': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'broker/v1/account/subaccount-transfer': 1,  # unknown
                            'broker/v1/account/subaccount-deposit': 1,  # unknown
                            'broker/v1/account/subaccount-withdrawal': 1,  # unknown
                            'broker/v1/account/sub-api-list': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'v2/broker/account/info': 2,
                            'v2/broker/account/subaccount-list': 20,
                            'v2/broker/account/subaccount-email': 2,
                            'v2/broker/account/subaccount-spot-assets': 2,
                            'v2/broker/account/subaccount-future-assets': 2,
                            'v2/broker/manage/subaccount-apikey-list': 2,
                        },
                        'post': {
                            'broker/v1/account/sub-create': 20,  # 1 times/1s(UID) => 20/1 = 20
                            'broker/v1/account/sub-modify': 20,  # 1 times/1s(UID) => 20/1 = 20
                            'broker/v1/account/sub-modify-email': 20,  # 1 times/1s(UID) => 20/1 = 20
                            'broker/v1/account/sub-address': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'broker/v1/account/sub-withdrawal': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'broker/v1/account/sub-auto-transfer': 4,  # 5 times/1s(UID) => 20/5 = 4
                            'broker/v1/account/sub-api-create': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'broker/v1/account/sub-api-modify': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'v2/broker/account/modify-subaccount-email': 2,
                            'v2/broker/account/create-subaccount': 20,
                            'v2/broker/account/modify-subaccount': 20,
                            'v2/broker/account/subaccount-address': 2,
                            'v2/broker/account/subaccount-withdrawal': 2,
                            'v2/broker/account/set-subaccount-autotransfer': 2,
                            'v2/broker/manage/create-subaccount-apikey': 2,
                            'v2/broker/manage/modify-subaccount-apikey': 2,
                        },
                    },
                    'margin': {
                        'get': {
                            'margin/v1/cross/account/riskRate': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'margin/v1/cross/account/maxTransferOutAmount': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'margin/v1/isolated/account/maxTransferOutAmount': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'margin/v1/isolated/order/openOrders': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'margin/v1/isolated/order/history': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'margin/v1/isolated/order/fills': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'margin/v1/isolated/loan/list': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'margin/v1/isolated/repay/list': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'margin/v1/isolated/interest/list': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'margin/v1/isolated/liquidation/list': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'margin/v1/isolated/fin/list': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'margin/v1/cross/order/openOrders': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'margin/v1/cross/order/history': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'margin/v1/cross/order/fills': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'margin/v1/cross/loan/list': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'margin/v1/cross/repay/list': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'margin/v1/cross/interest/list': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'margin/v1/cross/liquidation/list': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'margin/v1/cross/fin/list': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'margin/v1/cross/account/assets': 2,  # 10 times/1s(IP) => 20/10 = 2
                            'margin/v1/isolated/account/assets': 2,  # 10 times/1s(IP) => 20/10 = 2
                            'v2/margin/crossed/borrow-history': 2,
                            'v2/margin/crossed/repay-history': 2,
                            'v2/margin/crossed/interest-history': 2,
                            'v2/margin/crossed/liquidation-history': 2,
                            'v2/margin/crossed/financial-records': 2,
                            'v2/margin/crossed/account/assets': 2,
                            'v2/margin/crossed/account/risk-rate': 2,
                            'v2/margin/crossed/account/max-borrowable-amount': 2,
                            'v2/margin/crossed/account/max-transfer-out-amount': 2,
                            'v2/margin/crossed/interest-rate-and-limit': 2,
                            'v2/margin/crossed/tier-data': 2,
                            'v2/margin/crossed/open-orders': 2,
                            'v2/margin/crossed/history-orders': 2,
                            'v2/margin/crossed/fills': 2,
                            'v2/margin/isolated/borrow-history': 2,
                            'v2/margin/isolated/repay-history': 2,
                            'v2/margin/isolated/interest-history': 2,
                            'v2/margin/isolated/liquidation-history': 2,
                            'v2/margin/isolated/financial-records': 2,
                            'v2/margin/isolated/account/assets': 2,
                            'v2/margin/isolated/account/risk-rate': 2,
                            'v2/margin/isolated/account/max-borrowable-amount': 2,
                            'v2/margin/isolated/account/max-transfer-out-amount': 2,
                            'v2/margin/isolated/interest-rate-and-limit': 2,
                            'v2/margin/isolated/tier-data': 2,
                            'v2/margin/isolated/open-orders': 2,
                            'v2/margin/isolated/history-orders': 2,
                            'v2/margin/isolated/fills': 2,
                        },
                        'post': {
                            'margin/v1/cross/account/borrow': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'margin/v1/isolated/account/borrow': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'margin/v1/cross/account/repay': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'margin/v1/isolated/account/repay': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'margin/v1/isolated/account/riskRate': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'margin/v1/cross/account/maxBorrowableAmount': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'margin/v1/isolated/account/maxBorrowableAmount': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'margin/v1/isolated/account/flashRepay': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'margin/v1/isolated/account/queryFlashRepayStatus': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'margin/v1/cross/account/flashRepay': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'margin/v1/cross/account/queryFlashRepayStatus': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'margin/v1/isolated/order/placeOrder': 4,  # 5 times/1s(UID) => 20/5 = 4
                            'margin/v1/isolated/order/batchPlaceOrder': 4,  # 5 times/1s(UID) => 20/5 = 4
                            'margin/v1/isolated/order/cancelOrder': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'margin/v1/isolated/order/batchCancelOrder': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'margin/v1/cross/order/placeOrder': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'margin/v1/cross/order/batchPlaceOrder': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'margin/v1/cross/order/cancelOrder': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'margin/v1/cross/order/batchCancelOrder': 2,  # 10 times/1s(UID) => 20/10 = 2
                            'v2/margin/crossed/account/borrow': 2,
                            'v2/margin/crossed/account/repay': 2,
                            'v2/margin/crossed/account/flash-repay': 2,
                            'v2/margin/crossed/account/query-flash-repay-status': 2,
                            'v2/margin/crossed/place-order': 2,
                            'v2/margin/crossed/batch-place-order': 2,
                            'v2/margin/crossed/cancel-order': 2,
                            'v2/margin/crossed/batch-cancel-order': 2,
                            'v2/margin/isolated/account/borrow': 2,
                            'v2/margin/isolated/account/repay': 2,
                            'v2/margin/isolated/account/flash-repay': 2,
                            'v2/margin/isolated/account/query-flash-repay-status': 2,
                            'v2/margin/isolated/place-order': 2,
                            'v2/margin/isolated/batch-place-order': 2,
                            'v2/margin/isolated/cancel-order': 2,
                            'v2/margin/isolated/batch-cancel-order': 2,
                        },
                    },
                    'copy': {
                        'get': {
                            'v2/copy/mix-trader/order-current-track': 2,
                            'v2/copy/mix-trader/order-history-track': 2,
                            'v2/copy/mix-trader/order-total-detail': 2,
                            'v2/copy/mix-trader/profit-history-summarys': 1,
                            'v2/copy/mix-trader/profit-history-details': 1,
                            'v2/copy/mix-trader/profit-details': 1,
                            'v2/copy/mix-trader/profits-group-coin-date': 1,
                            'v2/copy/mix-trader/config-query-symbols': 1,
                            'v2/copy/mix-trader/config-query-followers': 2,
                            'v2/copy/mix-follower/query-current-orders': 2,
                            'v2/copy/mix-follower/query-history-orders': 1,
                            'v2/copy/mix-follower/query-settings': 2,
                            'v2/copy/mix-follower/query-traders': 2,
                            'v2/copy/mix-follower/query-quantity-limit': 2,
                            'v2/copy/mix-broker/query-traders': 2,
                            'v2/copy/mix-broker/query-history-traces': 2,
                            'v2/copy/mix-broker/query-current-traces': 2,
                            'v2/copy/spot-trader/profit-summarys': 2,
                            'v2/copy/spot-trader/profit-history-details': 2,
                            'v2/copy/spot-trader/profit-details': 2,
                            'v2/copy/spot-trader/order-total-detail': 2,
                            'v2/copy/spot-trader/order-history-track': 2,
                            'v2/copy/spot-trader/order-current-track': 2,
                            'v2/copy/spot-trader/config-query-settings': 2,
                            'v2/copy/spot-trader/config-query-followers': 2,
                            'v2/copy/spot-follower/query-traders': 2,
                            'v2/copy/spot-follower/query-trader-symbols': 2,
                            'v2/copy/spot-follower/query-settings': 2,
                            'v2/copy/spot-follower/query-history-orders': 2,
                            'v2/copy/spot-follower/query-current-orders': 2,
                        },
                        'post': {
                            'v2/copy/mix-trader/order-modify-tpsl': 2,
                            'v2/copy/mix-trader/order-close-positions': 2,
                            'v2/copy/mix-trader/config-setting-symbols': 2,
                            'v2/copy/mix-trader/config-setting-base': 2,
                            'v2/copy/mix-trader/config-remove-follower': 2,
                            'v2/copy/mix-follower/setting-tpsl': 1,
                            'v2/copy/mix-follower/settings': 2,
                            'v2/copy/mix-follower/close-positions': 2,
                            'v2/copy/mix-follower/cancel-trader': 4,
                            'v2/copy/spot-trader/order-modify-tpsl': 2,
                            'v2/copy/spot-trader/order-close-tracking': 2,
                            'v2/copy/spot-trader/config-setting-symbols': 2,
                            'v2/copy/spot-trader/config-remove-follower': 2,
                            'v2/copy/spot-follower/stop-order': 2,
                            'v2/copy/spot-follower/settings': 2,
                            'v2/copy/spot-follower/setting-tpsl': 2,
                            'v2/copy/spot-follower/order-close-tracking': 2,
                            'v2/copy/spot-follower/cancel-trader': 2,
                        },
                    },
                    'tax': {
                        'get': {
                            'v2/tax/spot-record': 20,
                            'v2/tax/future-record': 20,
                            'v2/tax/margin-record': 20,
                            'v2/tax/p2p-record': 20,
                        },
                    },
                    'convert': {
                        'get': {
                            'v2/convert/currencies': 2,
                            'v2/convert/quoted-price': 2,
                            'v2/convert/convert-record': 2,
                            'v2/convert/bgb-convert-coin-list': 2,
                            'v2/convert/bgb-convert-records': 2,
                        },
                        'post': {
                            'v2/convert/trade': 2,
                            'v2/convert/bgb-convert': 2,
                        },
                    },
                    'earn': {
                        'get': {
                            'v2/earn/savings/product': 2,
                            'v2/earn/savings/account': 2,
                            'v2/earn/savings/assets': 2,
                            'v2/earn/savings/records': 2,
                            'v2/earn/savings/subscribe-info': 2,
                            'v2/earn/savings/subscribe-result': 2,
                            'v2/earn/savings/redeem-result': 2,
                            'v2/earn/sharkfin/product': 2,
                            'v2/earn/sharkfin/account': 2,
                            'v2/earn/sharkfin/assets': 2,
                            'v2/earn/sharkfin/records': 2,
                            'v2/earn/sharkfin/subscribe-info': 2,
                            'v2/earn/sharkfin/subscribe-result': 4,
                            'v2/earn/loan/ongoing-orders': 2,
                            'v2/earn/loan/repay-history': 2,
                            'v2/earn/loan/revise-history': 2,
                            'v2/earn/loan/borrow-history': 2,
                            'v2/earn/loan/debts': 2,
                            'v2/earn/loan/reduces': 2,
                            'v2/earn/account/assets': 2,
                        },
                        'post': {
                            'v2/earn/savings/subscribe': 2,
                            'v2/earn/savings/redeem': 2,
                            'v2/earn/sharkfin/subscribe': 2,
                            'v2/earn/loan/borrow': 2,
                            'v2/earn/loan/repay': 2,
                            'v2/earn/loan/revise-pledge': 2,
                        },
                    },
                    'common': {
                        'get': {
                            'v2/common/trade-rate': 2,
                        },
                    },
                },
            },
            'fees': {
                'spot': {
                    'taker': self.parse_number('0.002'),
                    'maker': self.parse_number('0.002'),
                },
                'swap': {
                    'taker': self.parse_number('0.0006'),
                    'maker': self.parse_number('0.0004'),
                },
            },
            'requiredCredentials': {
                'apiKey': True,
                'secret': True,
                'password': True,
            },
            'exceptions': {
                # http error codes
                # 400 Bad Request — Invalid request format
                # 401 Unauthorized — Invalid API Key
                # 403 Forbidden — You do not have access to the requested resource
                # 404 Not Found
                # 500 Internal Server Error — We had a problem with our server
                'exact': {
                    '1': ExchangeError,  # {"code": 1, "message": "System error"}
                    # undocumented
                    'failure to get a peer from the ring-balancer': ExchangeNotAvailable,  # {"message": "failure to get a peer from the ring-balancer"}
                    '4010': PermissionDenied,  # {"code": 4010, "message": "For the security of your funds, withdrawals are not permitted within 24 hours after changing fund password  / mobile number / Google Authenticator settings "}
                    # common
                    # '0': ExchangeError,  # 200 successful,when the order placement / cancellation / operation is successful
                    '4001': ExchangeError,  # no data received in 30s
                    '4002': ExchangeError,  # Buffer full. cannot write data
                    # --------------------------------------------------------
                    '30001': AuthenticationError,  # {"code": 30001, "message": 'request header "OK_ACCESS_KEY" cannot be blank'}
                    '30002': AuthenticationError,  # {"code": 30002, "message": 'request header "OK_ACCESS_SIGN" cannot be blank'}
                    '30003': AuthenticationError,  # {"code": 30003, "message": 'request header "OK_ACCESS_TIMESTAMP" cannot be blank'}
                    '30004': AuthenticationError,  # {"code": 30004, "message": 'request header "OK_ACCESS_PASSPHRASE" cannot be blank'}
                    '30005': InvalidNonce,  # {"code": 30005, "message": "invalid OK_ACCESS_TIMESTAMP"}
                    '30006': AuthenticationError,  # {"code": 30006, "message": "invalid OK_ACCESS_KEY"}
                    '30007': BadRequest,  # {"code": 30007, "message": 'invalid Content_Type, please use "application/json" format'}
                    '30008': RequestTimeout,  # {"code": 30008, "message": "timestamp request expired"}
                    '30009': ExchangeError,  # {"code": 30009, "message": "system error"}
                    '30010': AuthenticationError,  # {"code": 30010, "message": "API validation failed"}
                    '30011': PermissionDenied,  # {"code": 30011, "message": "invalid IP"}
                    '30012': AuthenticationError,  # {"code": 30012, "message": "invalid authorization"}
                    '30013': AuthenticationError,  # {"code": 30013, "message": "invalid sign"}
                    '30014': DDoSProtection,  # {"code": 30014, "message": "request too frequent"}
                    '30015': AuthenticationError,  # {"code": 30015, "message": 'request header "OK_ACCESS_PASSPHRASE" incorrect'}
                    '30016': ExchangeError,  # {"code": 30015, "message": "you are using v1 apiKey, please use v1 endpoint. If you would like to use v3 endpoint, please subscribe to v3 apiKey"}
                    '30017': ExchangeError,  # {"code": 30017, "message": "apikey's broker id does not match"}
                    '30018': ExchangeError,  # {"code": 30018, "message": "apikey's domain does not match"}
                    '30019': ExchangeNotAvailable,  # {"code": 30019, "message": "Api is offline or unavailable"}
                    '30020': BadRequest,  # {"code": 30020, "message": "body cannot be blank"}
                    '30021': BadRequest,  # {"code": 30021, "message": "Json data format error"}, {"code": 30021, "message": "json data format error"}
                    '30022': PermissionDenied,  # {"code": 30022, "message": "Api has been frozen"}
                    '30023': BadRequest,  # {"code": 30023, "message": "{0} parameter cannot be blank"}
                    '30024': BadSymbol,  # {"code":30024,"message":"\"instrument_id\" is an invalid parameter"}
                    '30025': BadRequest,  # {"code": 30025, "message": "{0} parameter category error"}
                    '30026': DDoSProtection,  # {"code": 30026, "message": "requested too frequent"}
                    '30027': AuthenticationError,  # {"code": 30027, "message": "login failure"}
                    '30028': PermissionDenied,  # {"code": 30028, "message": "unauthorized execution"}
                    '30029': AccountSuspended,  # {"code": 30029, "message": "account suspended"}
                    '30030': ExchangeError,  # {"code": 30030, "message": "endpoint request failed. Please try again"}
                    '30031': BadRequest,  # {"code": 30031, "message": "token does not exist"}
                    '30032': BadSymbol,  # {"code": 30032, "message": "pair does not exist"}
                    '30033': BadRequest,  # {"code": 30033, "message": "exchange domain does not exist"}
                    '30034': ExchangeError,  # {"code": 30034, "message": "exchange ID does not exist"}
                    '30035': ExchangeError,  # {"code": 30035, "message": "trading is not hasattr(self, supported) website"}
                    '30036': ExchangeError,  # {"code": 30036, "message": "no relevant data"}
                    '30037': ExchangeNotAvailable,  # {"code": 30037, "message": "endpoint is offline or unavailable"}
                    # '30038': AuthenticationError,  # {"code": 30038, "message": "user does not exist"}
                    '30038': OnMaintenance,  # {"client_oid":"","code":"30038","error_code":"30038","error_message":"Matching engine is being upgraded. Please try in about 1 minute.","message":"Matching engine is being upgraded. Please try in about 1 minute.","order_id":"-1","result":false}
                    # futures
                    '32001': AccountSuspended,  # {"code": 32001, "message": "futures account suspended"}
                    '32002': PermissionDenied,  # {"code": 32002, "message": "futures account does not exist"}
                    '32003': CancelPending,  # {"code": 32003, "message": "canceling, please wait"}
                    '32004': ExchangeError,  # {"code": 32004, "message": "you have no unfilled orders"}
                    '32005': InvalidOrder,  # {"code": 32005, "message": "max order quantity"}
                    '32006': InvalidOrder,  # {"code": 32006, "message": "the order price or trigger price exceeds USD 1 million"}
                    '32007': InvalidOrder,  # {"code": 32007, "message": "leverage level must be the same for orders on the same side of the contract"}
                    '32008': InvalidOrder,  # {"code": 32008, "message": "Max. positions to open(cross margin)"}
                    '32009': InvalidOrder,  # {"code": 32009, "message": "Max. positions to open(fixed margin)"}
                    '32010': ExchangeError,  # {"code": 32010, "message": "leverage cannot be changed with open positions"}
                    '32011': ExchangeError,  # {"code": 32011, "message": "futures status error"}
                    '32012': ExchangeError,  # {"code": 32012, "message": "futures order update error"}
                    '32013': ExchangeError,  # {"code": 32013, "message": "token type is blank"}
                    '32014': ExchangeError,  # {"code": 32014, "message": "your number of contracts closing is larger than the number of contracts available"}
                    '32015': ExchangeError,  # {"code": 32015, "message": "margin ratio is lower than 100% before opening positions"}
                    '32016': ExchangeError,  # {"code": 32016, "message": "margin ratio is lower than 100% after opening position"}
                    '32017': ExchangeError,  # {"code": 32017, "message": "no BBO"}
                    '32018': ExchangeError,  # {"code": 32018, "message": "the order quantity is less than 1, please try again"}
                    '32019': ExchangeError,  # {"code": 32019, "message": "the order price deviates from the price of the previous minute by more than 3%"}
                    '32020': ExchangeError,  # {"code": 32020, "message": "the price is not in the range of the price limit"}
                    '32021': ExchangeError,  # {"code": 32021, "message": "leverage error"}
                    '32022': ExchangeError,  # {"code": 32022, "message": "self function is not supported in your country or region according to the regulations"}
                    '32023': ExchangeError,  # {"code": 32023, "message": "self account has outstanding loan"}
                    '32024': ExchangeError,  # {"code": 32024, "message": "order cannot be placed during delivery"}
                    '32025': ExchangeError,  # {"code": 32025, "message": "order cannot be placed during settlement"}
                    '32026': ExchangeError,  # {"code": 32026, "message": "your account is restricted from opening positions"}
                    '32027': ExchangeError,  # {"code": 32027, "message": "cancelled over 20 orders"}
                    '32028': AccountSuspended,  # {"code": 32028, "message": "account is suspended and liquidated"}
                    '32029': ExchangeError,  # {"code": 32029, "message": "order info does not exist"}
                    '32030': InvalidOrder,  # The order cannot be cancelled
                    '32031': ArgumentsRequired,  # client_oid or order_id is required.
                    '32038': AuthenticationError,  # User does not exist
                    '32040': ExchangeError,  # User have open contract orders or position
                    '32044': ExchangeError,  # {"code": 32044, "message": "The margin ratio after submitting self order is lower than the minimum requirement({0}) for your tier."}
                    '32045': ExchangeError,  # str of commission over 1 million
                    '32046': ExchangeError,  # Each user can hold up to 10 trade plans at the same time
                    '32047': ExchangeError,  # system error
                    '32048': InvalidOrder,  # Order strategy track range error
                    '32049': ExchangeError,  # Each user can hold up to 10 track plans at the same time
                    '32050': InvalidOrder,  # Order strategy rang error
                    '32051': InvalidOrder,  # Order strategy ice depth error
                    '32052': ExchangeError,  # str of commission over 100 thousand
                    '32053': ExchangeError,  # Each user can hold up to 6 ice plans at the same time
                    '32057': ExchangeError,  # The order price is zero. Market-close-all function cannot be executed
                    '32054': ExchangeError,  # Trade not allow
                    '32055': InvalidOrder,  # cancel order error
                    '32056': ExchangeError,  # iceberg per order average should between {0}-{1} contracts
                    '32058': ExchangeError,  # Each user can hold up to 6 initiative plans at the same time
                    '32059': InvalidOrder,  # Total amount should exceed per order amount
                    '32060': InvalidOrder,  # Order strategy type error
                    '32061': InvalidOrder,  # Order strategy initiative limit error
                    '32062': InvalidOrder,  # Order strategy initiative range error
                    '32063': InvalidOrder,  # Order strategy initiative rate error
                    '32064': ExchangeError,  # Time Stringerval of orders should set between 5-120s
                    '32065': ExchangeError,  # Close amount exceeds the limit of Market-close-all(999 for BTC, and 9999 for the rest tokens)
                    '32066': ExchangeError,  # You have open orders. Please cancel all open orders before changing your leverage level.
                    '32067': ExchangeError,  # Account equity < required hasattr(self, margin) setting. Please adjust your leverage level again.
                    '32068': ExchangeError,  # The margin for self position will fall short of the required hasattr(self, margin) setting. Please adjust your leverage level or increase your margin to proceed.
                    '32069': ExchangeError,  # Target leverage level too low. Your account balance is insufficient to cover the margin required. Please adjust the leverage level again.
                    '32070': ExchangeError,  # Please check open position or unfilled order
                    '32071': ExchangeError,  # Your current liquidation mode does not support self action.
                    '32072': ExchangeError,  # The highest available margin for your order’s tier is {0}. Please edit your margin and place a new order.
                    '32073': ExchangeError,  # The action does not apply to the token
                    '32074': ExchangeError,  # The number of contracts of your position, open orders, and the current order has exceeded the maximum order limit of self asset.
                    '32075': ExchangeError,  # Account risk rate breach
                    '32076': ExchangeError,  # Liquidation of the holding position(s) at market price will require cancellation of all pending close orders of the contracts.
                    '32077': ExchangeError,  # Your margin for self asset in futures account is insufficient and the position has been taken over for liquidation.(You will not be able to place orders, close positions, transfer funds, or add margin during self period of time. Your account will be restored after the liquidation is complete.)
                    '32078': ExchangeError,  # Please cancel all open orders before switching the liquidation mode(Please cancel all open orders before switching the liquidation mode)
                    '32079': ExchangeError,  # Your open positions are at high risk.(Please add margin or reduce positions before switching the mode)
                    '32080': ExchangeError,  # Funds cannot be transferred out within 30 minutes after futures settlement
                    '32083': ExchangeError,  # The number of contracts should be a positive multiple of %%. Please place your order again
                    # token and margin trading
                    '33001': PermissionDenied,  # {"code": 33001, "message": "margin account for self pair is not enabled yet"}
                    '33002': AccountSuspended,  # {"code": 33002, "message": "margin account for self pair is suspended"}
                    '33003': InsufficientFunds,  # {"code": 33003, "message": "no loan balance"}
                    '33004': ExchangeError,  # {"code": 33004, "message": "loan amount cannot be smaller than the minimum limit"}
                    '33005': ExchangeError,  # {"code": 33005, "message": "repayment amount must exceed 0"}
                    '33006': ExchangeError,  # {"code": 33006, "message": "loan order not found"}
                    '33007': ExchangeError,  # {"code": 33007, "message": "status not found"}
                    '33008': InsufficientFunds,  # {"code": 33008, "message": "loan amount cannot exceed the maximum limit"}
                    '33009': ExchangeError,  # {"code": 33009, "message": "user ID is blank"}
                    '33010': ExchangeError,  # {"code": 33010, "message": "you cannot cancel an order during session 2 of call auction"}
                    '33011': ExchangeError,  # {"code": 33011, "message": "no new market data"}
                    '33012': ExchangeError,  # {"code": 33012, "message": "order cancellation failed"}
                    '33013': InvalidOrder,  # {"code": 33013, "message": "order placement failed"}
                    '33014': OrderNotFound,  # {"code": 33014, "message": "order does not exist"}
                    '33015': InvalidOrder,  # {"code": 33015, "message": "exceeded maximum limit"}
                    '33016': ExchangeError,  # {"code": 33016, "message": "margin trading is not open for self token"}
                    '33017': InsufficientFunds,  # {"code": 33017, "message": "insufficient balance"}
                    '33018': ExchangeError,  # {"code": 33018, "message": "self parameter must be smaller than 1"}
                    '33020': ExchangeError,  # {"code": 33020, "message": "request not supported"}
                    '33021': BadRequest,  # {"code": 33021, "message": "token and the pair do not match"}
                    '33022': InvalidOrder,  # {"code": 33022, "message": "pair and the order do not match"}
                    '33023': ExchangeError,  # {"code": 33023, "message": "you can only place market orders during call auction"}
                    '33024': InvalidOrder,  # {"code": 33024, "message": "trading amount too small"}
                    '33025': InvalidOrder,  # {"code": 33025, "message": "base token amount is blank"}
                    '33026': ExchangeError,  # {"code": 33026, "message": "transaction completed"}
                    '33027': InvalidOrder,  # {"code": 33027, "message": "cancelled order or order cancelling"}
                    '33028': InvalidOrder,  # {"code": 33028, "message": "the decimal places of the trading price exceeded the limit"}
                    '33029': InvalidOrder,  # {"code": 33029, "message": "the decimal places of the trading size exceeded the limit"}
                    '33034': ExchangeError,  # {"code": 33034, "message": "You can only place limit order after Call Auction has started"}
                    '33035': ExchangeError,  # This type of order cannot be canceled(This type of order cannot be canceled)
                    '33036': ExchangeError,  # Exceeding the limit of entrust order
                    '33037': ExchangeError,  # The buy order price should be lower than 130% of the trigger price
                    '33038': ExchangeError,  # The sell order price should be higher than 70% of the trigger price
                    '33039': ExchangeError,  # The limit of callback rate is 0 < x <= 5%
                    '33040': ExchangeError,  # The trigger price of a buy order should be lower than the latest transaction price
                    '33041': ExchangeError,  # The trigger price of a sell order should be higher than the latest transaction price
                    '33042': ExchangeError,  # The limit of price variance is 0 < x <= 1%
                    '33043': ExchangeError,  # The total amount must be larger than 0
                    '33044': ExchangeError,  # The average amount should be 1/1000 * total amount <= x <= total amount
                    '33045': ExchangeError,  # The price should not be 0, including trigger price, order price, and price limit
                    '33046': ExchangeError,  # Price variance should be 0 < x <= 1%
                    '33047': ExchangeError,  # Sweep ratio should be 0 < x <= 100%
                    '33048': ExchangeError,  # Per order limit: Total amount/1000 < x <= Total amount
                    '33049': ExchangeError,  # Total amount should be X > 0
                    '33050': ExchangeError,  # Time interval should be 5 <= x <= 120s
                    '33051': ExchangeError,  # cancel order number not higher limit: plan and track entrust no more than 10, ice and time entrust no more than 6
                    '33059': BadRequest,  # {"code": 33059, "message": "client_oid or order_id is required"}
                    '33060': BadRequest,  # {"code": 33060, "message": "Only fill in either parameter client_oid or order_id"}
                    '33061': ExchangeError,  # Value of a single market price order cannot exceed 100,000 USD
                    '33062': ExchangeError,  # The leverage ratio is too high. The borrowed position has exceeded the maximum position of self leverage ratio. Please readjust the leverage ratio
                    '33063': ExchangeError,  # Leverage multiple is too low, there is insufficient margin in the account, please readjust the leverage ratio
                    '33064': ExchangeError,  # The setting of the leverage ratio cannot be less than 2, please readjust the leverage ratio
                    '33065': ExchangeError,  # Leverage ratio exceeds maximum leverage ratio, please readjust leverage ratio
                    # account
                    '21009': ExchangeError,  # Funds cannot be transferred out within 30 minutes after swap settlement(Funds cannot be transferred out within 30 minutes after swap settlement)
                    '34001': PermissionDenied,  # {"code": 34001, "message": "withdrawal suspended"}
                    '34002': InvalidAddress,  # {"code": 34002, "message": "please add a withdrawal address"}
                    '34003': ExchangeError,  # {"code": 34003, "message": "sorry, self token cannot be withdrawn to xx at the moment"}
                    '34004': ExchangeError,  # {"code": 34004, "message": "withdrawal fee is smaller than minimum limit"}
                    '34005': ExchangeError,  # {"code": 34005, "message": "withdrawal fee exceeds the maximum limit"}
                    '34006': ExchangeError,  # {"code": 34006, "message": "withdrawal amount is lower than the minimum limit"}
                    '34007': ExchangeError,  # {"code": 34007, "message": "withdrawal amount exceeds the maximum limit"}
                    '34008': InsufficientFunds,  # {"code": 34008, "message": "insufficient balance"}
                    '34009': ExchangeError,  # {"code": 34009, "message": "your withdrawal amount exceeds the daily limit"}
                    '34010': ExchangeError,  # {"code": 34010, "message": "transfer amount must be larger than 0"}
                    '34011': ExchangeError,  # {"code": 34011, "message": "conditions not met"}
                    '34012': ExchangeError,  # {"code": 34012, "message": "the minimum withdrawal amount for NEO is 1, and the amount must be an integer"}
                    '34013': ExchangeError,  # {"code": 34013, "message": "please transfer"}
                    '34014': ExchangeError,  # {"code": 34014, "message": "transfer limited"}
                    '34015': ExchangeError,  # {"code": 34015, "message": "subaccount does not exist"}
                    '34016': PermissionDenied,  # {"code": 34016, "message": "transfer suspended"}
                    '34017': AccountSuspended,  # {"code": 34017, "message": "account suspended"}
                    '34018': AuthenticationError,  # {"code": 34018, "message": "incorrect trades password"}
                    '34019': PermissionDenied,  # {"code": 34019, "message": "please bind your email before withdrawal"}
                    '34020': PermissionDenied,  # {"code": 34020, "message": "please bind your funds password before withdrawal"}
                    '34021': InvalidAddress,  # {"code": 34021, "message": "Not verified address"}
                    '34022': ExchangeError,  # {"code": 34022, "message": "Withdrawals are not available for sub accounts"}
                    '34023': PermissionDenied,  # {"code": 34023, "message": "Please enable futures trading before transferring your funds"}
                    '34026': ExchangeError,  # transfer too frequently(transfer too frequently)
                    '34036': ExchangeError,  # Parameter is incorrect, please refer to API documentation
                    '34037': ExchangeError,  # Get the sub-account balance interface, account type is not supported
                    '34038': ExchangeError,  # Since your C2C transaction is unusual, you are restricted from fund transfer. Please contact our customer support to cancel the restriction
                    '34039': ExchangeError,  # You are now restricted from transferring out your funds due to abnormal trades on C2C Market. Please transfer your fund on our website or app instead to verify your identity
                    # swap
                    '35001': ExchangeError,  # {"code": 35001, "message": "Contract does not exist"}
                    '35002': ExchangeError,  # {"code": 35002, "message": "Contract settling"}
                    '35003': ExchangeError,  # {"code": 35003, "message": "Contract paused"}
                    '35004': ExchangeError,  # {"code": 35004, "message": "Contract pending settlement"}
                    '35005': AuthenticationError,  # {"code": 35005, "message": "User does not exist"}
                    '35008': InvalidOrder,  # {"code": 35008, "message": "Risk ratio too high"}
                    '35010': InvalidOrder,  # {"code": 35010, "message": "Position closing too large"}
                    '35012': InvalidOrder,  # {"code": 35012, "message": "Incorrect order size"}
                    '35014': InvalidOrder,  # {"code": 35014, "message": "Order price is not within limit"}
                    '35015': InvalidOrder,  # {"code": 35015, "message": "Invalid leverage level"}
                    '35017': ExchangeError,  # {"code": 35017, "message": "Open orders exist"}
                    '35019': InvalidOrder,  # {"code": 35019, "message": "Order size too large"}
                    '35020': InvalidOrder,  # {"code": 35020, "message": "Order price too high"}
                    '35021': InvalidOrder,  # {"code": 35021, "message": "Order size exceeded current tier limit"}
                    '35022': ExchangeError,  # {"code": 35022, "message": "Contract status error"}
                    '35024': ExchangeError,  # {"code": 35024, "message": "Contract not initialized"}
                    '35025': InsufficientFunds,  # {"code": 35025, "message": "No account balance"}
                    '35026': ExchangeError,  # {"code": 35026, "message": "Contract settings not initialized"}
                    '35029': OrderNotFound,  # {"code": 35029, "message": "Order does not exist"}
                    '35030': InvalidOrder,  # {"code": 35030, "message": "Order size too large"}
                    '35031': InvalidOrder,  # {"code": 35031, "message": "Cancel order size too large"}
                    '35032': ExchangeError,  # {"code": 35032, "message": "Invalid user status"}
                    '35037': ExchangeError,  # No last traded price in cache
                    '35039': ExchangeError,  # {"code": 35039, "message": "Open order quantity exceeds limit"}
                    '35040': InvalidOrder,  # {"error_message":"Invalid order type","result":"true","error_code":"35040","order_id":"-1"}
                    '35044': ExchangeError,  # {"code": 35044, "message": "Invalid order status"}
                    '35046': InsufficientFunds,  # {"code": 35046, "message": "Negative account balance"}
                    '35047': InsufficientFunds,  # {"code": 35047, "message": "Insufficient account balance"}
                    '35048': ExchangeError,  # {"code": 35048, "message": "User contract is frozen and liquidating"}
                    '35049': InvalidOrder,  # {"code": 35049, "message": "Invalid order type"}
                    '35050': InvalidOrder,  # {"code": 35050, "message": "Position settings are blank"}
                    '35052': InsufficientFunds,  # {"code": 35052, "message": "Insufficient cross margin"}
                    '35053': ExchangeError,  # {"code": 35053, "message": "Account risk too high"}
                    '35055': InsufficientFunds,  # {"code": 35055, "message": "Insufficient account balance"}
                    '35057': ExchangeError,  # {"code": 35057, "message": "No last traded price"}
                    '35058': ExchangeError,  # {"code": 35058, "message": "No limit"}
                    '35059': BadRequest,  # {"code": 35059, "message": "client_oid or order_id is required"}
                    '35060': BadRequest,  # {"code": 35060, "message": "Only fill in either parameter client_oid or order_id"}
                    '35061': BadRequest,  # {"code": 35061, "message": "Invalid instrument_id"}
                    '35062': InvalidOrder,  # {"code": 35062, "message": "Invalid match_price"}
                    '35063': InvalidOrder,  # {"code": 35063, "message": "Invalid order_size"}
                    '35064': InvalidOrder,  # {"code": 35064, "message": "Invalid client_oid"}
                    '35066': InvalidOrder,  # Order interval error
                    '35067': InvalidOrder,  # Time-weighted order ratio error
                    '35068': InvalidOrder,  # Time-weighted order range error
                    '35069': InvalidOrder,  # Time-weighted single transaction limit error
                    '35070': InvalidOrder,  # Algo order type error
                    '35071': InvalidOrder,  # Order total must be larger than single order limit
                    '35072': InvalidOrder,  # Maximum 6 unfulfilled time-weighted orders can be held at the same time
                    '35073': InvalidOrder,  # Order price is 0. Market-close-all not available
                    '35074': InvalidOrder,  # Iceberg order single transaction average error
                    '35075': InvalidOrder,  # Failed to cancel order
                    '35076': InvalidOrder,  # LTC 20x leverage. Not allowed to open position
                    '35077': InvalidOrder,  # Maximum 6 unfulfilled iceberg orders can be held at the same time
                    '35078': InvalidOrder,  # Order amount exceeded 100,000
                    '35079': InvalidOrder,  # Iceberg order price variance error
                    '35080': InvalidOrder,  # Callback rate error
                    '35081': InvalidOrder,  # Maximum 10 unfulfilled trail orders can be held at the same time
                    '35082': InvalidOrder,  # Trail order callback rate error
                    '35083': InvalidOrder,  # Each user can only hold a maximum of 10 unfulfilled stop-limit orders at the same time
                    '35084': InvalidOrder,  # Order amount exceeded 1 million
                    '35085': InvalidOrder,  # Order amount is not in the correct range
                    '35086': InvalidOrder,  # Price exceeds 100 thousand
                    '35087': InvalidOrder,  # Price exceeds 100 thousand
                    '35088': InvalidOrder,  # Average amount error
                    '35089': InvalidOrder,  # Price exceeds 100 thousand
                    '35090': ExchangeError,  # No stop-limit orders available for cancelation
                    '35091': ExchangeError,  # No trail orders available for cancellation
                    '35092': ExchangeError,  # No iceberg orders available for cancellation
                    '35093': ExchangeError,  # No trail orders available for cancellation
                    '35094': ExchangeError,  # Stop-limit order last traded price error
                    '35095': BadRequest,  # Instrument_id error
                    '35096': ExchangeError,  # Algo order status error
                    '35097': ExchangeError,  # Order status and order ID cannot exist at the same time
                    '35098': ExchangeError,  # An order status or order ID must exist
                    '35099': ExchangeError,  # Algo order ID error
                    # option
                    '36001': BadRequest,  # Invalid underlying index.
                    '36002': BadRequest,  # Instrument does not exist.
                    '36005': ExchangeError,  # Instrument status is invalid.
                    '36101': AuthenticationError,  # Account does not exist.
                    '36102': PermissionDenied,  # Account status is invalid.
                    '36103': AccountSuspended,  # Account is suspended due to ongoing liquidation.
                    '36104': PermissionDenied,  # Account is not enabled for options trading.
                    '36105': PermissionDenied,  # Please enable the account for option contract.
                    '36106': AccountSuspended,  # Funds cannot be transferred in or out, is suspended.
                    '36107': PermissionDenied,  # Funds cannot be transferred out within 30 minutes after option exercising or settlement.
                    '36108': InsufficientFunds,  # Funds cannot be transferred in or out, of the account is less than zero.
                    '36109': PermissionDenied,  # Funds cannot be transferred in or out during option exercising or settlement.
                    '36201': PermissionDenied,  # New order function is blocked.
                    '36202': PermissionDenied,  # Account does not have permission to short option.
                    '36203': InvalidOrder,  # Invalid format for client_oid.
                    '36204': ExchangeError,  # Invalid format for request_id.
                    '36205': BadRequest,  # Instrument id does not match underlying index.
                    '36206': BadRequest,  # Order_id and client_oid can not be used at the same time.
                    '36207': InvalidOrder,  # Either order price or fartouch price must be present.
                    '36208': InvalidOrder,  # Either order price or size must be present.
                    '36209': InvalidOrder,  # Either order_id or client_oid must be present.
                    '36210': InvalidOrder,  # Either order_ids or client_oids must be present.
                    '36211': InvalidOrder,  # Exceeding max batch size for order submission.
                    '36212': InvalidOrder,  # Exceeding max batch size for oder cancellation.
                    '36213': InvalidOrder,  # Exceeding max batch size for order amendment.
                    '36214': ExchangeError,  # Instrument does not have valid bid/ask quote.
                    '36216': OrderNotFound,  # Order does not exist.
                    '36217': InvalidOrder,  # Order submission failed.
                    '36218': InvalidOrder,  # Order cancellation failed.
                    '36219': InvalidOrder,  # Order amendment failed.
                    '36220': InvalidOrder,  # Order is pending cancel.
                    '36221': InvalidOrder,  # Order qty is not valid multiple of lot size.
                    '36222': InvalidOrder,  # Order price is breaching highest buy limit.
                    '36223': InvalidOrder,  # Order price is breaching lowest sell limit.
                    '36224': InvalidOrder,  # Exceeding max order size.
                    '36225': InvalidOrder,  # Exceeding max open order count for instrument.
                    '36226': InvalidOrder,  # Exceeding max open order count for underlying.
                    '36227': InvalidOrder,  # Exceeding max open size across all orders for underlying
                    '36228': InvalidOrder,  # Exceeding max available qty for instrument.
                    '36229': InvalidOrder,  # Exceeding max available qty for underlying.
                    '36230': InvalidOrder,  # Exceeding max position limit for underlying.
                    # --------------------------------------------------------
                    # swap
                    '400': BadRequest,  # Bad Request
                    '401': AuthenticationError,  # Unauthorized access
                    '403': PermissionDenied,  # Access prohibited
                    '404': BadRequest,  # Request address does not exist
                    '405': BadRequest,  # The HTTP Method is not supported
                    '415': BadRequest,  # The current media type is not supported
                    '429': DDoSProtection,  # Too many requests
                    '500': ExchangeNotAvailable,  # System busy
                    '1001': RateLimitExceeded,  # The request is too frequent and has been throttled
                    '1002': ExchangeError,  # {0} verifications within 24 hours
                    '1003': ExchangeError,  # You failed more than {0} times today, the current operation is locked, please try again in 24 hours
                    # '00000': ExchangeError,  # success
                    '40001': AuthenticationError,  # ACCESS_KEY cannot be empty
                    '40002': AuthenticationError,  # SECRET_KEY cannot be empty
                    '40003': AuthenticationError,  # Signature cannot be empty
                    '40004': InvalidNonce,  # Request timestamp expired
                    '40005': InvalidNonce,  # Invalid ACCESS_TIMESTAMP
                    '40006': AuthenticationError,  # Invalid ACCESS_KEY
                    '40007': BadRequest,  # Invalid Content_Type
                    '40008': InvalidNonce,  # Request timestamp expired
                    '40009': AuthenticationError,  # sign signature error
                    '40010': AuthenticationError,  # sign signature error
                    '40011': AuthenticationError,  # ACCESS_PASSPHRASE cannot be empty
                    '40012': AuthenticationError,  # apikey/password is incorrect
                    '40013': ExchangeError,  # User status is abnormal
                    '40014': PermissionDenied,  # Incorrect permissions
                    '40015': ExchangeError,  # System is abnormal, please try again later
                    '40016': PermissionDenied,  # The user must bind the phone or Google
                    '40017': ExchangeError,  # Parameter verification failed
                    '40018': PermissionDenied,  # Invalid IP
                    '40019': BadRequest,  # {"code":"40019","msg":"Parameter QLCUSDT_SPBL cannot be empty","requestTime":1679196063659,"data":null}
                    '40031': AccountSuspended,  # The account has been cancelled and cannot be used again
                    '40037': AuthenticationError,  # Apikey does not exist
                    '40102': BadRequest,  # Contract configuration does not exist, please check the parameters
                    '40103': BadRequest,  # Request method cannot be empty
                    '40104': ExchangeError,  # Lever adjustment failure
                    '40105': ExchangeError,  # Abnormal access to current price limit data
                    '40106': ExchangeError,  # Abnormal get next settlement time
                    '40107': ExchangeError,  # Abnormal access to index price data
                    '40108': InvalidOrder,  # Wrong order quantity
                    '40109': OrderNotFound,  # The data of the order cannot be found, please confirm the order number
                    '40200': OnMaintenance,  # Server upgrade, please try again later
                    '40201': InvalidOrder,  # Order number cannot be empty
                    '40202': ExchangeError,  # User information cannot be empty
                    '40203': BadRequest,  # The amount of adjustment margin cannot be empty or negative
                    '40204': BadRequest,  # Adjustment margin type cannot be empty
                    '40205': BadRequest,  # Adjusted margin type data is wrong
                    '40206': BadRequest,  # The direction of the adjustment margin cannot be empty
                    '40207': BadRequest,  # The adjustment margin data is wrong
                    '40208': BadRequest,  # The accuracy of the adjustment margin amount is incorrect
                    '40209': BadRequest,  # The current page number is wrong, please confirm
                    '40300': ExchangeError,  # User does not exist
                    '40301': PermissionDenied,  # Permission has not been obtained yet. If you need to use it, please contact customer service
                    '40302': BadRequest,  # Parameter abnormality
                    '40303': BadRequest,  # Can only query up to 20,000 data
                    '40304': BadRequest,  # Parameter type is abnormal
                    '40305': BadRequest,  # Client_oid length is not greater than 50, and cannot be Martian characters
                    '40306': ExchangeError,  # Batch processing orders can only process up to 20
                    '40308': OnMaintenance,  # The contract is being temporarily maintained
                    '40309': BadSymbol,  # The contract has been removed
                    '40400': ExchangeError,  # Status check abnormal
                    '40401': ExchangeError,  # The operation cannot be performed
                    '40402': BadRequest,  # The opening direction cannot be empty
                    '40403': BadRequest,  # Wrong opening direction format
                    '40404': BadRequest,  # Whether to enable automatic margin call parameters cannot be empty
                    '40405': BadRequest,  # Whether to enable the automatic margin call parameter type is wrong
                    '40406': BadRequest,  # Whether to enable automatic margin call parameters is of unknown type
                    '40407': ExchangeError,  # The query direction is not the direction entrusted by the plan
                    '40408': ExchangeError,  # Wrong time range
                    '40409': ExchangeError,  # Time format error
                    '40500': InvalidOrder,  # Client_oid check error
                    '40501': ExchangeError,  # Channel name error
                    '40502': ExchangeError,  # If it is a copy user, you must pass the copy to whom
                    '40503': ExchangeError,  # With the single type
                    '40504': ExchangeError,  # Platform code must pass
                    '40505': ExchangeError,  # Not the same type
                    '40506': AuthenticationError,  # Platform signature error
                    '40507': AuthenticationError,  # Api signature error
                    '40508': ExchangeError,  # KOL is not authorized
                    '40509': ExchangeError,  # Abnormal copy end
                    '40600': ExchangeError,  # Copy function suspended
                    '40601': ExchangeError,  # Followers cannot be KOL
                    '40602': ExchangeError,  # The number of copies has reached the limit and cannot process the request
                    '40603': ExchangeError,  # Abnormal copy end
                    '40604': ExchangeNotAvailable,  # Server is busy, please try again later
                    '40605': ExchangeError,  # Copy type, the copy number must be passed
                    '40606': ExchangeError,  # The type of document number is wrong
                    '40607': ExchangeError,  # Document number must be passed
                    '40608': ExchangeError,  # No documented products currently supported
                    '40609': ExchangeError,  # The contract product does not support copying
                    '40700': BadRequest,  # Cursor parameters are incorrect
                    '40701': ExchangeError,  # KOL is not authorized
                    '40702': ExchangeError,  # Unauthorized copying user
                    '40703': ExchangeError,  # Bill inquiry start and end time cannot be empty
                    '40704': ExchangeError,  # Can only check the data of the last three months
                    '40705': BadRequest,  # The start and end time cannot exceed 90 days
                    '40706': InvalidOrder,  # Wrong order price
                    '40707': BadRequest,  # Start time is greater than end time
                    '40708': BadRequest,  # Parameter verification is abnormal
                    '40709': ExchangeError,  # There is no hasattr(self, position) position, and no automatic margin call can be set
                    '40710': ExchangeError,  # Abnormal account status
                    '40711': InsufficientFunds,  # Insufficient contract account balance
                    '40712': InsufficientFunds,  # Insufficient margin
                    '40713': ExchangeError,  # Cannot exceed the maximum transferable margin amount
                    '40714': ExchangeError,  # No direct margin call is allowed
                    '40762': InsufficientFunds,  # {"code":"40762","msg":"The order amount exceeds the balance","requestTime":1716572156622,"data":null}
                    '40768': OrderNotFound,  # Order does not exist
                    '40808': InvalidOrder,  # {"code":"40808","msg":"Parameter verification exception size checkBDScale error value=2293.577 checkScale=2","requestTime":1725638500052,"data":null}
                    '41103': InvalidOrder,  # {"code":"41103","msg":"param price scale error error","requestTime":1725635883561,"data":null}
                    '41114': OnMaintenance,  # {"code":"41114","msg":"The current trading pair is under maintenance, please refer to the official announcement for the opening time","requestTime":1679196062544,"data":null}
                    '43011': InvalidOrder,  # The parameter does not meet the specification executePrice <= 0
                    '43012': InsufficientFunds,  # {"code":"43012","msg":"Insufficient balance","requestTime":1711648951774,"data":null}
                    '43025': InvalidOrder,  # Plan order does not exist
                    '43115': OnMaintenance,  # {"code":"43115","msg":"The current trading pair is opening soon, please refer to the official announcement for the opening time","requestTime":1688907202434,"data":null}
                    '45110': InvalidOrder,  # {"code":"45110","msg":"less than the minimum amount 5 USDT","requestTime":1669911118932,"data":null}
                    # spot
                    'invalid sign': AuthenticationError,
                    'invalid currency': BadSymbol,  # invalid trading pair
                    'invalid symbol': BadSymbol,
                    'invalid period': BadRequest,  # invalid Kline type
                    'invalid user': ExchangeError,
                    'invalid amount': InvalidOrder,
                    'invalid type': InvalidOrder,  # {"status":"error","ts":1595700344504,"err_code":"invalid-parameter","err_msg":"invalid type"}
                    'invalid orderId': InvalidOrder,
                    'invalid record': ExchangeError,
                    'invalid accountId': BadRequest,
                    'invalid address': BadRequest,
                    'accesskey not None': AuthenticationError,  # {"status":"error","ts":1595704360508,"err_code":"invalid-parameter","err_msg":"accesskey not null"}
                    'illegal accesskey': AuthenticationError,
                    'sign not null': AuthenticationError,
                    'req_time is too much difference from server time': InvalidNonce,
                    'permissions not right': PermissionDenied,  # {"status":"error","ts":1595704490084,"err_code":"invalid-parameter","err_msg":"permissions not right"}
                    'illegal sign invalid': AuthenticationError,  # {"status":"error","ts":1595684716042,"err_code":"invalid-parameter","err_msg":"illegal sign invalid"}
                    'user locked': AccountSuspended,
                    'Request Frequency Is Too High': RateLimitExceeded,
                    'more than a daily rate of cash': BadRequest,
                    'more than the maximum daily withdrawal amount': BadRequest,
                    'need to bind email or mobile': ExchangeError,
                    'user forbid': PermissionDenied,
                    'User Prohibited Cash Withdrawal': PermissionDenied,
                    'Cash Withdrawal Is Less Than The Minimum Value': BadRequest,
                    'Cash Withdrawal Is More Than The Maximum Value': BadRequest,
                    'the account with in 24 hours ban coin': PermissionDenied,
                    'order cancel fail': BadRequest,  # {"status":"error","ts":1595703343035,"err_code":"bad-request","err_msg":"order cancel fail"}
                    'base symbol error': BadSymbol,
                    'base date error': ExchangeError,
                    'api signature not valid': AuthenticationError,
                    'gateway internal error': ExchangeError,
                    'audit failed': ExchangeError,
                    'order queryorder invalid': BadRequest,
                    'market no need price': InvalidOrder,
                    'limit need price': InvalidOrder,
                    'userid not equal to account_id': ExchangeError,
                    'your balance is low': InsufficientFunds,  # {"status":"error","ts":1595594160149,"err_code":"invalid-parameter","err_msg":"invalid size, valid range: [1,2000]"}
                    'address invalid cointype': ExchangeError,
                    'system exception': ExchangeError,  # {"status":"error","ts":1595711862763,"err_code":"system exception","err_msg":"system exception"}
                    '50003': ExchangeError,  # No record
                    '50004': BadSymbol,  # The transaction pair is currently not supported or has been suspended
                    '50006': PermissionDenied,  # The account is forbidden to withdraw. If you have any questions, please contact customer service.
                    '50007': PermissionDenied,  # The account is forbidden to withdraw within 24 hours. If you have any questions, please contact customer service.
                    '50008': RequestTimeout,  # network timeout
                    '50009': RateLimitExceeded,  # The operation is too frequent, please try again later
                    '50010': ExchangeError,  # The account is abnormally frozen. If you have any questions, please contact customer service.
                    '50014': InvalidOrder,  # The transaction amount under minimum limits
                    '50015': InvalidOrder,  # The transaction amount exceed maximum limits
                    '50016': InvalidOrder,  # The price can't be higher than the current price
                    '50017': InvalidOrder,  # Price under minimum limits
                    '50018': InvalidOrder,  # The price exceed maximum limits
                    '50019': InvalidOrder,  # The amount under minimum limits
                    '50020': InsufficientFunds,  # Insufficient balance
                    '50021': InvalidOrder,  # Price is under minimum limits
                    '50026': InvalidOrder,  # Market price parameter error
                    'invalid order query time': ExchangeError,  # start time is greater than end time; or the time interval between start time and end time is greater than 48 hours
                    'invalid start time': BadRequest,  # start time is a date 30 days ago; or start time is a date in the future
                    'invalid end time': BadRequest,  # end time is a date 30 days ago; or end time is a date in the future
                    '20003': ExchangeError,  # operation failed, {"status":"error","ts":1595730308979,"err_code":"bad-request","err_msg":"20003"}
                    '01001': ExchangeError,  # order failed, {"status":"fail","err_code":"01001","err_msg":"系统异常，请稍后重试"}
                    '43111': PermissionDenied,  # {"code":"43111","msg":"参数错误 address not in address book","requestTime":1665394201164,"data":null}
                },
                'broad': {
                    'invalid size, valid range': ExchangeError,
                },
            },
            'precisionMode': TICK_SIZE,
            'commonCurrencies': {
                'APX': 'AstroPepeX',
                'DEGEN': 'DegenReborn',
                'JADE': 'Jade Protocol',
                'OMNI': 'omni',  # conflict with Omni Network
                'TONCOIN': 'TON',
            },
            'options': {
                'timeDifference': 0,  # the difference between system clock and Binance clock
                'adjustForTimeDifference': False,  # controls the adjustment logic upon instantiation
                'timeframes': {
                    'spot': {
                        '1m': '1min',
                        '5m': '5min',
                        '15m': '15min',
                        '30m': '30min',
                        '1h': '1h',
                        '4h': '4h',
                        '6h': '6Hutc',
                        '12h': '12Hutc',
                        '1d': '1Dutc',
                        '3d': '3Dutc',
                        '1w': '1Wutc',
                        '1M': '1Mutc',
                    },
                    'swap': {
                        '1m': '1m',
                        '3m': '3m',
                        '5m': '5m',
                        '15m': '15m',
                        '30m': '30m',
                        '1h': '1H',
                        '2h': '2H',
                        '4h': '4H',
                        '6h': '6Hutc',
                        '12h': '12Hutc',
                        '1d': '1Dutc',
                        '3d': '3Dutc',
                        '1w': '1Wutc',
                        '1M': '1Mutc',
                    },
                },
                'fetchMarkets': [
                    'spot',
                    'swap',  # there is future markets but they use the same endpoints
                ],
                'defaultType': 'spot',  # 'spot', 'swap', 'future'
                'defaultSubType': 'linear',  # 'linear', 'inverse'
                'createMarketBuyOrderRequiresPrice': True,
                'broker': 'p4sve',
                'withdraw': {
                    'fillResponseFromRequest': True,
                },
                'fetchOHLCV': {
                    'spot': {
                        'method': 'publicSpotGetV2SpotMarketCandles',  # publicSpotGetV2SpotMarketCandles or publicSpotGetV2SpotMarketHistoryCandles
                    },
                    'swap': {
                        'method': 'publicMixGetV2MixMarketCandles',  # publicMixGetV2MixMarketCandles or publicMixGetV2MixMarketHistoryCandles or publicMixGetV2MixMarketHistoryIndexCandles or publicMixGetV2MixMarketHistoryMarkCandles
                    },
                    'maxDaysPerTimeframe': {
                        '1m': 30,
                        '3m': 30,
                        '5m': 30,
                        '10m': 52,
                        '15m': 52,
                        '30m': 52,
                        '1h': 83,
                        '2h': 120,
                        '4h': 240,
                        '6h': 360,
                        '12h': 360,
                        '1d': 360,
                        '3d': 1000,
                        '1w': 1000,
                        '1M': 1000,
                    },
                },
                'fetchTrades': {
                    'spot': {
                        'method': 'publicSpotGetV2SpotMarketFillsHistory',  # or publicSpotGetV2SpotMarketFills
                    },
                    'swap': {
                        'method': 'publicMixGetV2MixMarketFillsHistory',  # or publicMixGetV2MixMarketFills
                    },
                },
                'accountsByType': {
                    'spot': 'spot',
                    'cross': 'crossed_margin',
                    'isolated': 'isolated_margin',
                    'swap': 'usdt_futures',
                    'usdc_swap': 'usdc_futures',
                    'future': 'coin_futures',
                    'p2p': 'p2p',
                },
                'accountsById': {
                    'spot': 'spot',
                    'crossed_margin': 'cross',
                    'isolated_margin': 'isolated',
                    'usdt_futures': 'swap',
                    'usdc_futures': 'usdc_swap',
                    'coin_futures': 'future',
                    'p2p': 'p2p',
                },
                'sandboxMode': False,
                'networks': {
                    'TRX': 'TRC20',
                    'ETH': 'ERC20',
                    'BEP20': 'BSC',
                    'ZKSYNC': 'zkSyncEra',
                    'STARKNET': 'Starknet',
                    'OPTIMISM': 'Optimism',
                    'ARBITRUM': 'Arbitrum',
                    'APT': 'APTOS',
                    'MATIC': 'POLYGON',
                    'VIC': 'VICTION',
                },
                'networksById': {
                },
                'fetchPositions': {
                    'method': 'privateMixGetV2MixPositionAllPosition',  # or privateMixGetV2MixPositionHistoryPosition
                },
                'defaultTimeInForce': 'GTC',  # 'GTC' = Good To Cancel(default), 'IOC' = Immediate Or Cancel
            },
        })

    def set_sandbox_mode(self, enabled):
        self.options['sandboxMode'] = enabled

    def convert_symbol_for_sandbox(self, symbol):
        if symbol.startswith('S'):
            # handle using the exchange specified sandbox symbols
            return symbol
        convertedSymbol = None
        if symbol.find('/') > -1:
            if symbol.find(':') == -1:
                raise NotSupported(self.id + ' sandbox supports swap and future markets only')
            splitBase = symbol.split('/')
            previousBase = self.safe_string(splitBase, 0)
            previousQuoteSettleExpiry = self.safe_string(splitBase, 1)
            splitQuote = previousQuoteSettleExpiry.split(':')
            previousQuote = self.safe_string(splitQuote, 0)
            previousSettleExpiry = self.safe_string(splitQuote, 1)
            splitSettle = previousSettleExpiry.split('-')
            previousSettle = self.safe_string(splitSettle, 0)
            expiry = self.safe_string(splitSettle, 1)
            convertedSymbol = 'S' + previousBase + '/S' + previousQuote + ':S' + previousSettle
            if expiry is not None:
                convertedSymbol = convertedSymbol + '-' + expiry
        else:
            # handle using a market id instead of a unified symbol
            base = symbol[0:3]
            remaining = symbol[3:]
            convertedSymbol = 'S' + base + 'S' + remaining
        return convertedSymbol

    def handle_product_type_and_params(self, market=None, params={}):
        subType = None
        subType, params = self.handle_sub_type_and_params('handleProductTypeAndParams', None, params)
        defaultProductType = None
        if (subType is not None) and (market is None):
            # set default only if subType is defined and market is not defined, since there is also USDC productTypes which are also linear
            sandboxMode = self.safe_bool(self.options, 'sandboxMode', False)
            if sandboxMode:
                defaultProductType = 'SUSDT-FUTURES' if (subType == 'linear') else 'SCOIN-FUTURES'
            else:
                defaultProductType = 'USDT-FUTURES' if (subType == 'linear') else 'COIN-FUTURES'
        productType = self.safe_string(params, 'productType', defaultProductType)
        if (productType is None) and (market is not None):
            settle = market['settle']
            if settle == 'USDT':
                productType = 'USDT-FUTURES'
            elif settle == 'USDC':
                productType = 'USDC-FUTURES'
            elif settle == 'SUSDT':
                productType = 'SUSDT-FUTURES'
            elif settle == 'SUSDC':
                productType = 'SUSDC-FUTURES'
            elif (settle == 'SBTC') or (settle == 'SETH') or (settle == 'SEOS'):
                productType = 'SCOIN-FUTURES'
            else:
                productType = 'COIN-FUTURES'
        if productType is None:
            raise ArgumentsRequired(self.id + ' requires a productType param, one of "USDT-FUTURES", "USDC-FUTURES", "COIN-FUTURES", "SUSDT-FUTURES", "SUSDC-FUTURES" or "SCOIN-FUTURES"')
        params = self.omit(params, 'productType')
        return [productType, params]

    def fetch_time(self, params={}):
        """
        fetches the current integer timestamp in milliseconds from the exchange server
        :see: https://www.bitget.com/api-doc/common/public/Get-Server-Time
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns int: the current integer timestamp in milliseconds from the exchange server
        """
        response = self.publicCommonGetV2PublicTime(params)
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1700111073740,
        #         "data": {
        #             "serverTime": "1700111073740"
        #         }
        #     }
        #
        data = self.safe_value(response, 'data', {})
        return self.safe_integer(data, 'serverTime')

    def fetch_markets(self, params={}) -> List[Market]:
        """
        retrieves data on all markets for bitget
        :see: https://www.bitget.com/api-doc/spot/market/Get-Symbols
        :see: https://www.bitget.com/api-doc/contract/market/Get-All-Symbols-Contracts
        :see: https://www.bitget.com/api-doc/margin/common/support-currencies
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict[]: an array of objects representing market data
        """
        if self.options['adjustForTimeDifference']:
            self.load_time_difference()
        sandboxMode = self.safe_bool(self.options, 'sandboxMode', False)
        types = self.safe_value(self.options, 'fetchMarkets', ['spot', 'swap'])
        if sandboxMode:
            types = ['swap']
        promises = []
        fetchMargins = False
        for i in range(0, len(types)):
            type = types[i]
            if (type == 'swap') or (type == 'future'):
                subTypes = None
                if sandboxMode:
                    # the following are simulated trading markets ['SUSDT-FUTURES', 'SCOIN-FUTURES', 'SUSDC-FUTURES']
                    subTypes = ['SUSDT-FUTURES', 'SCOIN-FUTURES', 'SUSDC-FUTURES']
                else:
                    subTypes = ['USDT-FUTURES', 'COIN-FUTURES', 'USDC-FUTURES']
                for j in range(0, len(subTypes)):
                    promises.append(self.publicMixGetV2MixMarketContracts(self.extend(params, {
                        'productType': subTypes[j],
                    })))
            elif type == 'spot':
                promises.append(self.publicSpotGetV2SpotPublicSymbols(params))
                fetchMargins = True
                promises.append(self.publicMarginGetV2MarginCurrencies(params))
            else:
                raise NotSupported(self.id + ' does not support ' + type + ' market')
        results = promises
        markets = []
        self.options['crossMarginPairsData'] = []
        self.options['isolatedMarginPairsData'] = []
        for i in range(0, len(results)):
            res = self.safe_dict(results, i)
            data = self.safe_list(res, 'data', [])
            firstData = self.safe_dict(data, 0, {})
            isBorrowable = self.safe_string(firstData, 'isBorrowable')
            if fetchMargins and isBorrowable is not None:
                keysList = list(self.index_by(data, 'symbol').keys())
                self.options['crossMarginPairsData'] = keysList
                self.options['isolatedMarginPairsData'] = keysList
            else:
                markets = self.array_concat(markets, data)
        result = []
        for i in range(0, len(markets)):
            result.append(self.parse_market(markets[i]))
        return result

    def parse_market(self, market: dict) -> Market:
        #
        # spot
        #
        #     {
        #         "symbol": "TRXUSDT",
        #         "baseCoin": "TRX",
        #         "quoteCoin": "USDT",
        #         "minTradeAmount": "0",
        #         "maxTradeAmount": "10000000000",
        #         "takerFeeRate": "0.002",
        #         "makerFeeRate": "0.002",
        #         "pricePrecision": "6",
        #         "quantityPrecision": "4",
        #         "quotePrecision": "6",
        #         "status": "online",
        #         "minTradeUSDT": "5",
        #         "buyLimitPriceRatio": "0.05",
        #         "sellLimitPriceRatio": "0.05"
        #     }
        #
        # swap and future
        #
        #     {
        #         "symbol": "BTCUSDT",
        #         "baseCoin": "BTC",
        #         "quoteCoin": "USDT",
        #         "buyLimitPriceRatio": "0.01",
        #         "sellLimitPriceRatio": "0.01",
        #         "feeRateUpRatio": "0.005",
        #         "makerFeeRate": "0.0002",
        #         "takerFeeRate": "0.0006",
        #         "openCostUpRatio": "0.01",
        #         "supportMarginCoins": ["USDT"],
        #         "minTradeNum": "0.001",
        #         "priceEndStep": "1",
        #         "volumePlace": "3",
        #         "pricePlace": "1",
        #         "sizeMultiplier": "0.001",
        #         "symbolType": "perpetual",
        #         "minTradeUSDT": "5",
        #         "maxSymbolOrderNum": "200",
        #         "maxProductOrderNum": "400",
        #         "maxPositionNum": "150",
        #         "symbolStatus": "normal",
        #         "offTime": "-1",
        #         "limitOpenTime": "-1",
        #         "deliveryTime": "",
        #         "deliveryStartTime": "",
        #         "deliveryPeriod": "",
        #         "launchTime": "",
        #         "fundInterval": "8",
        #         "minLever": "1",
        #         "maxLever": "125",
        #         "posLimit": "0.05",
        #         "maintainTime": ""
        #     }
        #
        marketId = self.safe_string(market, 'symbol')
        quoteId = self.safe_string(market, 'quoteCoin')
        baseId = self.safe_string(market, 'baseCoin')
        quote = self.safe_currency_code(quoteId)
        base = self.safe_currency_code(baseId)
        supportMarginCoins = self.safe_value(market, 'supportMarginCoins', [])
        settleId = None
        if self.in_array(baseId, supportMarginCoins):
            settleId = baseId
        elif self.in_array(quoteId, supportMarginCoins):
            settleId = quoteId
        else:
            settleId = self.safe_string(supportMarginCoins, 0)
        settle = self.safe_currency_code(settleId)
        symbol = base + '/' + quote
        type = None
        swap = False
        spot = False
        future = False
        contract = False
        pricePrecision = None
        amountPrecision = None
        linear = None
        inverse = None
        expiry = None
        expiryDatetime = None
        symbolType = self.safe_string(market, 'symbolType')
        marginModes = None
        isMarginTradingAllowed = False
        if symbolType is None:
            type = 'spot'
            spot = True
            pricePrecision = self.parse_number(self.parse_precision(self.safe_string(market, 'pricePrecision')))
            amountPrecision = self.parse_number(self.parse_precision(self.safe_string(market, 'quantityPrecision')))
            hasCrossMargin = self.in_array(marketId, self.options['crossMarginPairsData'])
            hasIsolatedMargin = self.in_array(marketId, self.options['isolatedMarginPairsData'])
            marginModes = {
                'cross': hasCrossMargin,
                'isolated': hasIsolatedMargin,
            }
            isMarginTradingAllowed = hasCrossMargin or hasCrossMargin
        else:
            if symbolType == 'perpetual':
                type = 'swap'
                swap = True
                symbol = symbol + ':' + settle
            elif symbolType == 'delivery':
                expiry = self.safe_integer(market, 'deliveryTime')
                expiryDatetime = self.iso8601(expiry)
                expiryParts = expiryDatetime.split('-')
                yearPart = self.safe_string(expiryParts, 0)
                dayPart = self.safe_string(expiryParts, 2)
                year = yearPart[2:4]
                month = self.safe_string(expiryParts, 1)
                day = dayPart[0:2]
                expiryString = year + month + day
                type = 'future'
                future = True
                symbol = symbol + ':' + settle + '-' + expiryString
            contract = True
            inverse = (base == settle)
            linear = not inverse
            priceDecimals = self.safe_integer(market, 'pricePlace')
            amountDecimals = self.safe_integer(market, 'volumePlace')
            priceStep = self.safe_string(market, 'priceEndStep')
            amountStep = self.safe_string(market, 'minTradeNum')
            precisePrice = Precise(priceStep)
            precisePrice.decimals = max(precisePrice.decimals, priceDecimals)
            precisePrice.reduce()
            priceString = str(precisePrice)
            pricePrecision = self.parse_number(priceString)
            preciseAmount = Precise(amountStep)
            preciseAmount.decimals = max(preciseAmount.decimals, amountDecimals)
            preciseAmount.reduce()
            amountString = str(preciseAmount)
            amountPrecision = self.parse_number(amountString)
            marginModes = {
                'cross': True,
                'isolated': True,
            }
        status = self.safe_string_2(market, 'status', 'symbolStatus')
        active = None
        if status is not None:
            active = ((status == 'online') or (status == 'normal'))
        minCost = None
        if quote == 'USDT':
            minCost = self.safe_number(market, 'minTradeUSDT')
        contractSize = 1 if contract else None
        return {
            'id': marketId,
            'symbol': symbol,
            'base': base,
            'quote': quote,
            'settle': settle,
            'baseId': baseId,
            'quoteId': quoteId,
            'settleId': settleId,
            'type': type,
            'spot': spot,
            'margin': spot and isMarginTradingAllowed,
            'marginModes': marginModes,
            'swap': swap,
            'future': future,
            'option': False,
            'active': active,
            'contract': contract,
            'linear': linear,
            'inverse': inverse,
            'taker': self.safe_number(market, 'takerFeeRate'),
            'maker': self.safe_number(market, 'makerFeeRate'),
            'contractSize': contractSize,
            'expiry': expiry,
            'expiryDatetime': expiryDatetime,
            'strike': None,
            'optionType': None,
            'precision': {
                'amount': amountPrecision,
                'price': pricePrecision,
            },
            'limits': {
                'leverage': {
                    'min': self.safe_number(market, 'minLever'),
                    'max': self.safe_number(market, 'maxLever'),
                },
                'amount': {
                    'min': self.safe_number_2(market, 'minTradeNum', 'minTradeAmount'),
                    'max': self.safe_number(market, 'maxTradeAmount'),
                },
                'price': {
                    'min': None,
                    'max': None,
                },
                'cost': {
                    'min': minCost,
                    'max': None,
                },
            },
            'created': self.safe_integer(market, 'launchTime'),
            'info': market,
        }

    def fetch_currencies(self, params={}) -> Currencies:
        """
        fetches all available currencies on an exchange
        :see: https://www.bitget.com/api-doc/spot/market/Get-Coin-List
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict: an associative dictionary of currencies
        """
        response = self.publicSpotGetV2SpotPublicCoins(params)
        #
        #     {
        #         "code": "00000",
        #         "data": [
        #             {
        #                 "chains": [
        #                     {
        #                         "browserUrl": "https://blockchair.com/bitcoin/transaction/",
        #                         "chain": "BTC",
        #                         "depositConfirm": "1",
        #                         "extraWithdrawFee": "0",
        #                         "minDepositAmount": "0.0001",
        #                         "minWithdrawAmount": "0.005",
        #                         "needTag": "false",
        #                         "rechargeable": "true",
        #                         "withdrawConfirm": "1",
        #                         "withdrawFee": "0.0004",
        #                         "withdrawable": "true"
        #                     },
        #                 ],
        #                 "coin": "BTC",
        #                 "coinId": "1",
        #                 "transfer": "true""
        #             }
        #         ],
        #         "msg": "success",
        #         "requestTime": "1700120731773"
        #     }
        #
        result: dict = {}
        data = self.safe_value(response, 'data', [])
        for i in range(0, len(data)):
            entry = data[i]
            id = self.safe_string(entry, 'coin')  # we don't use 'coinId' has no use. it is 'coin' field that needs to be used in currency related endpoints(deposit, withdraw, etc..)
            code = self.safe_currency_code(id)
            chains = self.safe_value(entry, 'chains', [])
            networks: dict = {}
            deposit = False
            withdraw = False
            minWithdrawString = None
            minDepositString = None
            minWithdrawFeeString = None
            for j in range(0, len(chains)):
                chain = chains[j]
                networkId = self.safe_string(chain, 'chain')
                network = self.network_id_to_code(networkId, code)
                if network is not None:
                    network = network.upper()
                withdrawEnabled = self.safe_string(chain, 'withdrawable')
                canWithdraw = withdrawEnabled == 'true'
                withdraw = canWithdraw if (canWithdraw) else withdraw
                depositEnabled = self.safe_string(chain, 'rechargeable')
                canDeposit = depositEnabled == 'true'
                deposit = canDeposit if (canDeposit) else deposit
                networkWithdrawFeeString = self.safe_string(chain, 'withdrawFee')
                if networkWithdrawFeeString is not None:
                    minWithdrawFeeString = networkWithdrawFeeString if (minWithdrawFeeString is None) else Precise.string_min(networkWithdrawFeeString, minWithdrawFeeString)
                networkMinWithdrawString = self.safe_string(chain, 'minWithdrawAmount')
                if networkMinWithdrawString is not None:
                    minWithdrawString = networkMinWithdrawString if (minWithdrawString is None) else Precise.string_min(networkMinWithdrawString, minWithdrawString)
                networkMinDepositString = self.safe_string(chain, 'minDepositAmount')
                if networkMinDepositString is not None:
                    minDepositString = networkMinDepositString if (minDepositString is None) else Precise.string_min(networkMinDepositString, minDepositString)
                networks[network] = {
                    'info': chain,
                    'id': networkId,
                    'network': network,
                    'limits': {
                        'withdraw': {
                            'min': self.parse_number(networkMinWithdrawString),
                            'max': None,
                        },
                        'deposit': {
                            'min': self.parse_number(networkMinDepositString),
                            'max': None,
                        },
                    },
                    'active': canWithdraw and canDeposit,
                    'withdraw': canWithdraw,
                    'deposit': canDeposit,
                    'fee': self.parse_number(networkWithdrawFeeString),
                    'precision': None,
                }
            result[code] = {
                'info': entry,
                'id': id,
                'code': code,
                'networks': networks,
                'type': None,
                'name': None,
                'active': deposit and withdraw,
                'deposit': deposit,
                'withdraw': withdraw,
                'fee': self.parse_number(minWithdrawFeeString),
                'precision': None,
                'limits': {
                    'amount': {
                        'min': None,
                        'max': None,
                    },
                    'withdraw': {
                        'min': self.parse_number(minWithdrawString),
                        'max': None,
                    },
                    'deposit': {
                        'min': self.parse_number(minDepositString),
                        'max': None,
                    },
                },
                'created': None,
            }
        return result

    def fetch_market_leverage_tiers(self, symbol: str, params={}) -> List[LeverageTier]:
        """
        retrieve information on the maximum leverage, and maintenance margin for trades of varying trade sizes for a single market
        :see: https://www.bitget.com/api-doc/contract/position/Get-Query-Position-Lever
        :see: https://www.bitget.com/api-doc/margin/cross/account/Cross-Tier-Data
        :see: https://www.bitget.com/api-doc/margin/isolated/account/Isolated-Tier-Data
        :param str symbol: unified market symbol
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :param str [params.marginMode]: for spot margin 'cross' or 'isolated', default is 'isolated'
        :param str [params.code]: required for cross spot margin
        :param str [params.productType]: *contract only* 'USDT-FUTURES', 'USDC-FUTURES', 'COIN-FUTURES', 'SUSDT-FUTURES', 'SUSDC-FUTURES' or 'SCOIN-FUTURES'
        :returns dict: a `leverage tiers structure <https://docs.ccxt.com/#/?id=leverage-tiers-structure>`
        """
        self.load_markets()
        sandboxMode = self.safe_bool(self.options, 'sandboxMode', False)
        market = None
        if sandboxMode:
            sandboxSymbol = self.convert_symbol_for_sandbox(symbol)
            market = self.market(sandboxSymbol)
        else:
            market = self.market(symbol)
        request: dict = {}
        response = None
        marginMode = None
        marginMode, params = self.handle_margin_mode_and_params('fetchMarketLeverageTiers', params, 'isolated')
        if (market['swap']) or (market['future']):
            productType = None
            productType, params = self.handle_product_type_and_params(market, params)
            request['productType'] = productType
            request['symbol'] = market['id']
            response = self.publicMixGetV2MixMarketQueryPositionLever(self.extend(request, params))
        elif marginMode == 'isolated':
            request['symbol'] = market['id']
            response = self.privateMarginGetV2MarginIsolatedTierData(self.extend(request, params))
        elif marginMode == 'cross':
            code = self.safe_string(params, 'code')
            if code is None:
                raise ArgumentsRequired(self.id + ' fetchMarketLeverageTiers() requires a code argument')
            params = self.omit(params, 'code')
            currency = self.currency(code)
            request['coin'] = currency['id']
            response = self.privateMarginGetV2MarginCrossedTierData(self.extend(request, params))
        else:
            raise BadRequest(self.id + ' fetchMarketLeverageTiers() symbol does not support market ' + market['symbol'])
        #
        # swap and future
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1700290724614,
        #         "data": [
        #             {
        #                 "symbol": "BTCUSDT",
        #                 "level": "1",
        #                 "startUnit": "0",
        #                 "endUnit": "150000",
        #                 "leverage": "125",
        #                 "keepMarginRate": "0.004"
        #             },
        #         ]
        #     }
        #
        # isolated
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1700291531894,
        #         "data": [
        #             {
        #                 "tier": "1",
        #                 "symbol": "BTCUSDT",
        #                 "leverage": "10",
        #                 "baseCoin": "BTC",
        #                 "quoteCoin": "USDT",
        #                 "baseMaxBorrowableAmount": "2",
        #                 "quoteMaxBorrowableAmount": "24000",
        #                 "maintainMarginRate": "0.05",
        #                 "initRate": "0.1111"
        #             },
        #         ]
        #     }
        #
        # cross
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1700291818831,
        #         "data": [
        #             {
        #                 "tier": "1",
        #                 "leverage": "3",
        #                 "coin": "BTC",
        #                 "maxBorrowableAmount": "26",
        #                 "maintainMarginRate": "0.1"
        #             }
        #         ]
        #     }
        #
        result = self.safe_value(response, 'data', [])
        return self.parse_market_leverage_tiers(result, market)

    def parse_market_leverage_tiers(self, info, market: Market = None) -> List[LeverageTier]:
        #
        # swap and future
        #
        #     {
        #         "symbol": "BTCUSDT",
        #         "level": "1",
        #         "startUnit": "0",
        #         "endUnit": "150000",
        #         "leverage": "125",
        #         "keepMarginRate": "0.004"
        #     }
        #
        # isolated
        #
        #     {
        #         "tier": "1",
        #         "symbol": "BTCUSDT",
        #         "leverage": "10",
        #         "baseCoin": "BTC",
        #         "quoteCoin": "USDT",
        #         "baseMaxBorrowableAmount": "2",
        #         "quoteMaxBorrowableAmount": "24000",
        #         "maintainMarginRate": "0.05",
        #         "initRate": "0.1111"
        #     }
        #
        # cross
        #
        #     {
        #         "tier": "1",
        #         "leverage": "3",
        #         "coin": "BTC",
        #         "maxBorrowableAmount": "26",
        #         "maintainMarginRate": "0.1"
        #     }
        #
        tiers = []
        minNotional = 0
        for i in range(0, len(info)):
            item = info[i]
            minimumNotional = self.safe_number(item, 'startUnit')
            if minimumNotional is not None:
                minNotional = minimumNotional
            maxNotional = self.safe_number_n(item, ['endUnit', 'maxBorrowableAmount', 'baseMaxBorrowableAmount'])
            marginCurrency = self.safe_string_2(item, 'coin', 'baseCoin')
            currencyId = marginCurrency if (marginCurrency is not None) else market['base']
            tiers.append({
                'tier': self.safe_integer_2(item, 'level', 'tier'),
                'currency': self.safe_currency_code(currencyId),
                'minNotional': minNotional,
                'maxNotional': maxNotional,
                'maintenanceMarginRate': self.safe_number_2(item, 'keepMarginRate', 'maintainMarginRate'),
                'maxLeverage': self.safe_number(item, 'leverage'),
                'info': item,
            })
            minNotional = maxNotional
        return tiers

    def fetch_deposits(self, code: Str = None, since: Int = None, limit: Int = None, params={}) -> List[Transaction]:
        """
        fetch all deposits made to an account
        :see: https://www.bitget.com/api-doc/spot/account/Get-Deposit-Record
        :param str code: unified currency code
        :param int [since]: the earliest time in ms to fetch deposits for
        :param int [limit]: the maximum number of deposits structures to retrieve
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :param int [params.until]: end time in milliseconds
        :param str [params.idLessThan]: return records with id less than the provided value
        :param boolean [params.paginate]: default False, when True will automatically paginate by calling self endpoint multiple times. See in the docs all the [available parameters](https://github.com/ccxt/ccxt/wiki/Manual#pagination-params)
        :returns dict[]: a list of `transaction structures <https://docs.ccxt.com/#/?id=transaction-structure>`
        """
        self.load_markets()
        paginate = False
        paginate, params = self.handle_option_and_params(params, 'fetchDeposits', 'paginate')
        if paginate:
            return self.fetch_paginated_call_cursor('fetchDeposits', None, since, limit, params, 'idLessThan', 'idLessThan', None, 100)
        if code is None:
            raise ArgumentsRequired(self.id + ' fetchDeposits() requires a `code` argument')
        currency = self.currency(code)
        if since is None:
            since = self.milliseconds() - 7776000000  # 90 days
        request: dict = {
            'coin': currency['id'],
            'startTime': since,
            'endTime': self.milliseconds(),
        }
        if limit is not None:
            request['limit'] = limit
        request, params = self.handle_until_option('endTime', request, params)
        response = self.privateSpotGetV2SpotWalletDepositRecords(self.extend(request, params))
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1700528340608,
        #         "data": [
        #             {
        #                 "orderId": "1083832260799930368",
        #                 "tradeId": "35bf0e588a42b25c71a9d45abe7308cabdeec6b7b423910b9bd4743d3a9a9efa",
        #                 "coin": "BTC",
        #                 "type": "deposit",
        #                 "size": "0.00030000",
        #                 "status": "success",
        #                 "toAddress": "1BfZh7JESJGBUszCGeZnzxbVVvBycbJSbA",
        #                 "dest": "on_chain",
        #                 "chain": "BTC",
        #                 "fromAddress": null,
        #                 "cTime": "1694131668281",
        #                 "uTime": "1694131680247"
        #             }
        #         ]
        #     }
        #
        rawTransactions = self.safe_list(response, 'data', [])
        return self.parse_transactions(rawTransactions, currency, since, limit)

    def withdraw(self, code: str, amount: float, address: str, tag=None, params={}):
        """
        make a withdrawal
        :see: https://www.bitget.com/api-doc/spot/account/Wallet-Withdrawal
        :param str code: unified currency code
        :param float amount: the amount to withdraw
        :param str address: the address to withdraw to
        :param str tag:
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :param str [params.chain]: the blockchain network the withdrawal is taking place on
        :returns dict: a `transaction structure <https://docs.ccxt.com/#/?id=transaction-structure>`
        """
        self.check_address(address)
        chain = self.safe_string_2(params, 'chain', 'network')
        params = self.omit(params, 'network')
        if chain is None:
            raise ArgumentsRequired(self.id + ' withdraw() requires a chain parameter or a network parameter')
        self.load_markets()
        currency = self.currency(code)
        networkId = self.network_code_to_id(chain)
        request: dict = {
            'coin': currency['id'],
            'address': address,
            'chain': networkId,
            'size': amount,
            'transferType': 'on_chain',
        }
        if tag is not None:
            request['tag'] = tag
        response = self.privateSpotPostV2SpotWalletWithdrawal(self.extend(request, params))
        #
        #     {
        #          "code":"00000",
        #          "msg":"success",
        #          "requestTime":1696784219602,
        #          "data": {
        #              "orderId":"1094957867615789056",
        #              "clientOid":"64f1e4ce842041d296b4517df1b5c2d7"
        #          }
        #      }
        #
        data = self.safe_value(response, 'data', {})
        result: dict = {
            'id': self.safe_string(data, 'orderId'),
            'info': response,
            'txid': None,
            'timestamp': None,
            'datetime': None,
            'network': None,
            'addressFrom': None,
            'address': None,
            'addressTo': None,
            'amount': None,
            'type': 'withdrawal',
            'currency': None,
            'status': None,
            'updated': None,
            'tagFrom': None,
            'tag': None,
            'tagTo': None,
            'comment': None,
            'fee': None,
        }
        withdrawOptions = self.safe_value(self.options, 'withdraw', {})
        fillResponseFromRequest = self.safe_bool(withdrawOptions, 'fillResponseFromRequest', True)
        if fillResponseFromRequest:
            result['currency'] = code
            result['timestamp'] = self.milliseconds()
            result['datetime'] = self.iso8601(self.milliseconds())
            result['amount'] = amount
            result['tag'] = tag
            result['address'] = address
            result['addressTo'] = address
            result['network'] = chain
        return result

    def fetch_withdrawals(self, code: Str = None, since: Int = None, limit: Int = None, params={}) -> List[Transaction]:
        """
        fetch all withdrawals made from an account
        :see: https://www.bitget.com/api-doc/spot/account/Get-Withdraw-Record
        :param str code: unified currency code
        :param int [since]: the earliest time in ms to fetch withdrawals for
        :param int [limit]: the maximum number of withdrawals structures to retrieve
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :param int [params.until]: end time in milliseconds
        :param str [params.idLessThan]: return records with id less than the provided value
        :param boolean [params.paginate]: default False, when True will automatically paginate by calling self endpoint multiple times. See in the docs all the [available parameters](https://github.com/ccxt/ccxt/wiki/Manual#pagination-params)
        :returns dict[]: a list of `transaction structures <https://docs.ccxt.com/#/?id=transaction-structure>`
        """
        self.load_markets()
        paginate = False
        paginate, params = self.handle_option_and_params(params, 'fetchWithdrawals', 'paginate')
        if paginate:
            return self.fetch_paginated_call_cursor('fetchWithdrawals', None, since, limit, params, 'idLessThan', 'idLessThan', None, 100)
        if code is None:
            raise ArgumentsRequired(self.id + ' fetchWithdrawals() requires a `code` argument')
        currency = self.currency(code)
        if since is None:
            since = self.milliseconds() - 7776000000  # 90 days
        request: dict = {
            'coin': currency['id'],
            'startTime': since,
            'endTime': self.milliseconds(),
        }
        request, params = self.handle_until_option('endTime', request, params)
        if limit is not None:
            request['limit'] = limit
        response = self.privateSpotGetV2SpotWalletWithdrawalRecords(self.extend(request, params))
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1700528340608,
        #         "data": [
        #             {
        #                 "orderId": "1083832260799930368",
        #                 "tradeId": "35bf0e588a42b25c71a9d45abe7308cabdeec6b7b423910b9bd4743d3a9a9efa",
        #                 "clientOid": "123",
        #                 "coin": "BTC",
        #                 "type": "withdraw",
        #                 "size": "0.00030000",
        #                 "fee": "-1.0000000",
        #                 "status": "success",
        #                 "toAddress": "1BfZh7JESJGBUszCGeZnzxbVVvBycbJSbA",
        #                 "dest": "on_chain",
        #                 "chain": "BTC",
        #                 "confirm": "100",
        #                 "fromAddress": null,
        #                 "cTime": "1694131668281",
        #                 "uTime": "1694131680247"
        #             }
        #         ]
        #     }
        #
        rawTransactions = self.safe_list(response, 'data', [])
        return self.parse_transactions(rawTransactions, currency, since, limit)

    def parse_transaction(self, transaction: dict, currency: Currency = None) -> Transaction:
        #
        # fetchDeposits
        #
        #     {
        #         "orderId": "1083832260799930368",
        #         "tradeId": "35bf0e588a42b25c71a9d45abe7308cabdeec6b7b423910b9bd4743d3a9a9efa",
        #         "coin": "BTC",
        #         "type": "deposit",
        #         "size": "0.00030000",
        #         "status": "success",
        #         "toAddress": "1BfZh7JESJGBUszCGeZnzxbVVvBycbJSbA",
        #         "dest": "on_chain",
        #         "chain": "BTC",
        #         "fromAddress": null,
        #         "cTime": "1694131668281",
        #         "uTime": "1694131680247"
        #     }
        #
        # fetchWithdrawals
        #
        #     {
        #         "orderId": "1083832260799930368",
        #         "tradeId": "35bf0e588a42b25c71a9d45abe7308cabdeec6b7b423910b9bd4743d3a9a9efa",
        #         "clientOid": "123",
        #         "coin": "BTC",
        #         "type": "withdraw",
        #         "size": "0.00030000",
        #         "fee": "-1.0000000",
        #         "status": "success",
        #         "toAddress": "1BfZh7JESJGBUszCGeZnzxbVVvBycbJSbA",
        #         "dest": "on_chain",
        #         "chain": "BTC",
        #         "confirm": "100",
        #         "fromAddress": null,
        #         "cTime": "1694131668281",
        #         "uTime": "1694131680247"
        #     }
        #
        currencyId = self.safe_string(transaction, 'coin')
        code = self.safe_currency_code(currencyId, currency)
        timestamp = self.safe_integer(transaction, 'cTime')
        networkId = self.safe_string(transaction, 'chain')
        status = self.safe_string(transaction, 'status')
        tag = self.safe_string(transaction, 'tag')
        feeCostString = self.safe_string(transaction, 'fee')
        feeCostAbsString = Precise.string_abs(feeCostString)
        fee = None
        amountString = self.safe_string(transaction, 'size')
        if feeCostAbsString is not None:
            fee = {'currency': code, 'cost': self.parse_number(feeCostAbsString)}
            amountString = Precise.string_sub(amountString, feeCostAbsString)
        return {
            'id': self.safe_string(transaction, 'orderId'),
            'info': transaction,
            'txid': self.safe_string(transaction, 'tradeId'),
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'network': self.network_id_to_code(networkId),
            'addressFrom': self.safe_string(transaction, 'fromAddress'),
            'address': self.safe_string(transaction, 'toAddress'),
            'addressTo': self.safe_string(transaction, 'toAddress'),
            'amount': self.parse_number(amountString),
            'type': self.safe_string(transaction, 'type'),
            'currency': code,
            'status': self.parse_transaction_status(status),
            'updated': self.safe_integer(transaction, 'uTime'),
            'tagFrom': None,
            'tag': tag,
            'tagTo': tag,
            'comment': None,
            'internal': None,
            'fee': fee,
        }

    def parse_transaction_status(self, status: Str):
        statuses: dict = {
            'success': 'ok',
            'Pending': 'pending',
            'pending_review': 'pending',
            'pending_review_fail': 'failed',
            'reject': 'failed',
        }
        return self.safe_string(statuses, status, status)

    def fetch_deposit_address(self, code: str, params={}):
        """
        fetch the deposit address for a currency associated with self account
        :see: https://www.bitget.com/api-doc/spot/account/Get-Deposit-Address
        :param str code: unified currency code
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict: an `address structure <https://docs.ccxt.com/#/?id=address-structure>`
        """
        self.load_markets()
        networkCode = self.safe_string_2(params, 'chain', 'network')
        params = self.omit(params, 'network')
        networkId = None
        if networkCode is not None:
            networkId = self.network_code_to_id(networkCode, code)
        currency = self.currency(code)
        request: dict = {
            'coin': currency['id'],
        }
        if networkId is not None:
            request['chain'] = networkId
        response = self.privateSpotGetV2SpotWalletDepositAddress(self.extend(request, params))
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1700532244807,
        #         "data": {
        #             "coin": "BTC",
        #             "address": "1BfZh7JESJGBUszCGeZnzxbVVvBycbJSbA",
        #             "chain": "",
        #             "tag": null,
        #             "url": "https://blockchair.com/bitcoin/transaction/"
        #         }
        #     }
        #
        data = self.safe_dict(response, 'data', {})
        return self.parse_deposit_address(data, currency)

    def parse_deposit_address(self, depositAddress, currency: Currency = None):
        #
        #     {
        #         "coin": "BTC",
        #         "address": "1BfZh7JESJGBUszCGeZnzxbVVvBycbJSbA",
        #         "chain": "",
        #         "tag": null,
        #         "url": "https://blockchair.com/bitcoin/transaction/"
        #     }
        #
        currencyId = self.safe_string(depositAddress, 'coin')
        networkId = self.safe_string(depositAddress, 'chain')
        parsedCurrency = self.safe_currency_code(currencyId, currency)
        network = None
        if networkId is not None:
            network = self.network_id_to_code(networkId, parsedCurrency)
        return {
            'currency': parsedCurrency,
            'address': self.safe_string(depositAddress, 'address'),
            'tag': self.safe_string(depositAddress, 'tag'),
            'network': network,
            'info': depositAddress,
        }

    def fetch_order_book(self, symbol: str, limit: Int = None, params={}) -> OrderBook:
        """
        fetches information on open orders with bid(buy) and ask(sell) prices, volumes and other data
        :see: https://www.bitget.com/api-doc/spot/market/Get-Orderbook
        :see: https://www.bitget.com/api-doc/contract/market/Get-Merge-Depth
        :param str symbol: unified symbol of the market to fetch the order book for
        :param int [limit]: the maximum amount of order book entries to return
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict: A dictionary of `order book structures <https://docs.ccxt.com/#/?id=order-book-structure>` indexed by market symbols
        """
        self.load_markets()
        sandboxMode = self.safe_bool(self.options, 'sandboxMode', False)
        market = None
        if sandboxMode:
            sandboxSymbol = self.convert_symbol_for_sandbox(symbol)
            market = self.market(sandboxSymbol)
        else:
            market = self.market(symbol)
        request: dict = {
            'symbol': market['id'],
        }
        if limit is not None:
            request['limit'] = limit
        response = None
        if market['spot']:
            response = self.publicSpotGetV2SpotMarketOrderbook(self.extend(request, params))
        else:
            productType = None
            productType, params = self.handle_product_type_and_params(market, params)
            request['productType'] = productType
            response = self.publicMixGetV2MixMarketMergeDepth(self.extend(request, params))
        #
        #     {
        #       "code": "00000",
        #       "msg": "success",
        #       "requestTime": 1645854610294,
        #       "data": {
        #         "asks": [["39102", "11.026"]],
        #         "bids": [['39100.5', "1.773"]],
        #         "ts": "1645854610294"
        #       }
        #     }
        #
        data = self.safe_value(response, 'data', {})
        timestamp = self.safe_integer(data, 'ts')
        return self.parse_order_book(data, market['symbol'], timestamp)

    def parse_ticker(self, ticker: dict, market: Market = None) -> Ticker:
        #
        # spot: fetchTicker, fetchTickers
        #
        #     {
        #         "open": "37202.46",
        #         "symbol": "BTCUSDT",
        #         "high24h": "37744.75",
        #         "low24h": "36666",
        #         "lastPr": "37583.69",
        #         "quoteVolume": "519127705.303",
        #         "baseVolume": "13907.0386",
        #         "usdtVolume": "519127705.302908",
        #         "ts": "1700532903261",
        #         "bidPr": "37583.68",
        #         "askPr": "37583.69",
        #         "bidSz": "0.0007",
        #         "askSz": "0.0829",
        #         "openUtc": "37449.4",
        #         "changeUtc24h": "0.00359",
        #         "change24h": "0.00321"
        #     }
        #
        # swap and future: fetchTicker
        #
        #     {
        #         "symbol": "BTCUSDT",
        #         "lastPr": "37577.2",
        #         "askPr": "37577.3",
        #         "bidPr": "37577.2",
        #         "bidSz": "3.679",
        #         "askSz": "0.02",
        #         "high24h": "37765",
        #         "low24h": "36628.9",
        #         "ts": "1700533070359",
        #         "change24h": "0.00288",
        #         "baseVolume": "108606.181",
        #         "quoteVolume": "4051316303.9608",
        #         "usdtVolume": "4051316303.9608",
        #         "openUtc": "37451.5",
        #         "changeUtc24h": "0.00336",
        #         "indexPrice": "37574.489253",
        #         "fundingRate": "0.0001",
        #         "holdingAmount": "53464.529",
        #         "deliveryStartTime": null,
        #         "deliveryTime": null,
        #         "deliveryStatus": "",
        #         "open24h": "37235.7"
        #     }
        #
        # swap and future: fetchTickers
        #
        #     {
        #         "open": "14.9776",
        #         "symbol": "LINKUSDT",
        #         "high24h": "15.3942",
        #         "low24h": "14.3457",
        #         "lastPr": "14.3748",
        #         "quoteVolume": "7008612.4299",
        #         "baseVolume": "469908.8523",
        #         "usdtVolume": "7008612.42986561",
        #         "ts": "1700533772309",
        #         "bidPr": "14.375",
        #         "askPr": "14.3769",
        #         "bidSz": "50.004",
        #         "askSz": "0.7647",
        #         "openUtc": "14.478",
        #         "changeUtc24h": "-0.00713",
        #         "change24h": "-0.04978"
        #     }
        #
        marketId = self.safe_string(ticker, 'symbol')
        close = self.safe_string(ticker, 'lastPr')
        timestamp = self.safe_integer_omit_zero(ticker, 'ts')  # exchange bitget provided 0
        change = self.safe_string(ticker, 'change24h')
        open24 = self.safe_string(ticker, 'open24')
        open = self.safe_string(ticker, 'open')
        symbol: str
        openValue: str
        if open is None:
            symbol = self.safe_symbol(marketId, market, None, 'contract')
            openValue = open24
        else:
            symbol = self.safe_symbol(marketId, market, None, 'spot')
            openValue = open
        return self.safe_ticker({
            'symbol': symbol,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'high': self.safe_string(ticker, 'high24h'),
            'low': self.safe_string(ticker, 'low24h'),
            'bid': self.safe_string(ticker, 'bidPr'),
            'bidVolume': self.safe_string(ticker, 'bidSz'),
            'ask': self.safe_string(ticker, 'askPr'),
            'askVolume': self.safe_string(ticker, 'askSz'),
            'vwap': None,
            'open': openValue,
            'close': close,
            'last': close,
            'previousClose': None,
            'change': change,
            'percentage': Precise.string_mul(change, '100'),
            'average': None,
            'baseVolume': self.safe_string(ticker, 'baseVolume'),
            'quoteVolume': self.safe_string(ticker, 'quoteVolume'),
            'info': ticker,
        }, market)

    def fetch_ticker(self, symbol: str, params={}) -> Ticker:
        """
        fetches a price ticker, a statistical calculation with the information calculated over the past 24 hours for a specific market
        :see: https://www.bitget.com/api-doc/spot/market/Get-Tickers
        :see: https://www.bitget.com/api-doc/contract/market/Get-Ticker
        :param str symbol: unified symbol of the market to fetch the ticker for
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict: a `ticker structure <https://docs.ccxt.com/#/?id=ticker-structure>`
        """
        self.load_markets()
        sandboxMode = self.safe_bool(self.options, 'sandboxMode', False)
        market = None
        if sandboxMode:
            sandboxSymbol = self.convert_symbol_for_sandbox(symbol)
            market = self.market(sandboxSymbol)
        else:
            market = self.market(symbol)
        request: dict = {
            'symbol': market['id'],
        }
        response = None
        if market['spot']:
            response = self.publicSpotGetV2SpotMarketTickers(self.extend(request, params))
        else:
            productType = None
            productType, params = self.handle_product_type_and_params(market, params)
            request['productType'] = productType
            response = self.publicMixGetV2MixMarketTicker(self.extend(request, params))
        #
        # spot
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1700532903782,
        #         "data": [
        #             {
        #                 "open": "37202.46",
        #                 "symbol": "BTCUSDT",
        #                 "high24h": "37744.75",
        #                 "low24h": "36666",
        #                 "lastPr": "37583.69",
        #                 "quoteVolume": "519127705.303",
        #                 "baseVolume": "13907.0386",
        #                 "usdtVolume": "519127705.302908",
        #                 "ts": "1700532903261",
        #                 "bidPr": "37583.68",
        #                 "askPr": "37583.69",
        #                 "bidSz": "0.0007",
        #                 "askSz": "0.0829",
        #                 "openUtc": "37449.4",
        #                 "changeUtc24h": "0.00359",
        #                 "change24h": "0.00321"
        #             }
        #         ]
        #     }
        #
        # swap and future
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1700533070357,
        #         "data": [
        #             {
        #                 "symbol": "BTCUSDT",
        #                 "lastPr": "37577.2",
        #                 "askPr": "37577.3",
        #                 "bidPr": "37577.2",
        #                 "bidSz": "3.679",
        #                 "askSz": "0.02",
        #                 "high24h": "37765",
        #                 "low24h": "36628.9",
        #                 "ts": "1700533070359",
        #                 "change24h": "0.00288",
        #                 "baseVolume": "108606.181",
        #                 "quoteVolume": "4051316303.9608",
        #                 "usdtVolume": "4051316303.9608",
        #                 "openUtc": "37451.5",
        #                 "changeUtc24h": "0.00336",
        #                 "indexPrice": "37574.489253",
        #                 "fundingRate": "0.0001",
        #                 "holdingAmount": "53464.529",
        #                 "deliveryStartTime": null,
        #                 "deliveryTime": null,
        #                 "deliveryStatus": "",
        #                 "open24h": "37235.7"
        #             }
        #         ]
        #     }
        #
        data = self.safe_list(response, 'data', [])
        return self.parse_ticker(data[0], market)

    def fetch_tickers(self, symbols: Strings = None, params={}) -> Tickers:
        """
        fetches price tickers for multiple markets, statistical information calculated over the past 24 hours for each market
        :see: https://www.bitget.com/api-doc/spot/market/Get-Tickers
        :see: https://www.bitget.com/api-doc/contract/market/Get-All-Symbol-Ticker
        :param str[]|None symbols: unified symbols of the markets to fetch the ticker for, all market tickers are returned if not assigned
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :param str [params.subType]: *contract only* 'linear', 'inverse'
        :param str [params.productType]: *contract only* 'USDT-FUTURES', 'USDC-FUTURES', 'COIN-FUTURES', 'SUSDT-FUTURES', 'SUSDC-FUTURES' or 'SCOIN-FUTURES'
        :returns dict: a dictionary of `ticker structures <https://docs.ccxt.com/#/?id=ticker-structure>`
        """
        self.load_markets()
        market = None
        if symbols is not None:
            symbol = self.safe_value(symbols, 0)
            sandboxMode = self.safe_bool(self.options, 'sandboxMode', False)
            if sandboxMode:
                sandboxSymbol = self.convert_symbol_for_sandbox(symbol)
                market = self.market(sandboxSymbol)
            else:
                market = self.market(symbol)
        response = None
        request: dict = {}
        type = None
        type, params = self.handle_market_type_and_params('fetchTickers', market, params)
        # Calls like `.fetchTickers(None, {subType:'inverse'})` should be supported for self exchange, so
        # as "options.defaultSubType" is also set in exchange options, we should consider `params.subType`
        # with higher priority and only default to spot, if `subType` is not set in params
        passedSubType = self.safe_string(params, 'subType')
        productType = None
        productType, params = self.handle_product_type_and_params(market, params)
        # only if passedSubType and productType is None, then use spot
        if type == 'spot' and passedSubType is None:
            response = self.publicSpotGetV2SpotMarketTickers(self.extend(request, params))
        else:
            request['productType'] = productType
            response = self.publicMixGetV2MixMarketTickers(self.extend(request, params))
        #
        # spot
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1700532903782,
        #         "data": [
        #             {
        #                 "open": "37202.46",
        #                 "symbol": "BTCUSDT",
        #                 "high24h": "37744.75",
        #                 "low24h": "36666",
        #                 "lastPr": "37583.69",
        #                 "quoteVolume": "519127705.303",
        #                 "baseVolume": "13907.0386",
        #                 "usdtVolume": "519127705.302908",
        #                 "ts": "1700532903261",
        #                 "bidPr": "37583.68",
        #                 "askPr": "37583.69",
        #                 "bidSz": "0.0007",
        #                 "askSz": "0.0829",
        #                 "openUtc": "37449.4",
        #                 "changeUtc24h": "0.00359",
        #                 "change24h": "0.00321"
        #             }
        #         ]
        #     }
        #
        # swap and future
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1700533773477,
        #         "data": [
        #             {
        #                 "open": "14.9776",
        #                 "symbol": "LINKUSDT",
        #                 "high24h": "15.3942",
        #                 "low24h": "14.3457",
        #                 "lastPr": "14.3748",
        #                 "quoteVolume": "7008612.4299",
        #                 "baseVolume": "469908.8523",
        #                 "usdtVolume": "7008612.42986561",
        #                 "ts": "1700533772309",
        #                 "bidPr": "14.375",
        #                 "askPr": "14.3769",
        #                 "bidSz": "50.004",
        #                 "askSz": "0.7647",
        #                 "openUtc": "14.478",
        #                 "changeUtc24h": "-0.00713",
        #                 "change24h": "-0.04978"
        #             },
        #         ]
        #     }
        #
        data = self.safe_list(response, 'data', [])
        return self.parse_tickers(data, symbols)

    def parse_trade(self, trade: dict, market: Market = None) -> Trade:
        #
        # spot, swap and future: fetchTrades
        #
        #     {
        #         "tradeId": "1075199767891652609",
        #         "price": "29376.5",
        #         "size": "6.035",
        #         "side": "Buy",
        #         "ts": "1692073521000",
        #         "symbol": "BTCUSDT"
        #     }
        #
        # spot: fetchMyTrades
        #
        #     {
        #         "userId": "7264631750",
        #         "symbol": "BTCUSDT",
        #         "orderId": "1098394344925597696",
        #         "tradeId": "1098394344974925824",
        #         "orderType": "market",
        #         "side": "sell",
        #         "priceAvg": "28467.68",
        #         "size": "0.0002",
        #         "amount": "5.693536",
        #         "feeDetail": {
        #             "deduction": "no",
        #             "feeCoin": "USDT",
        #             "totalDeductionFee": "",
        #             "totalFee": "-0.005693536"
        #         },
        #         "tradeScope": "taker",
        #         "cTime": "1697603539699",
        #         "uTime": "1697603539754"
        #     }
        #
        # spot margin: fetchMyTrades
        #
        #     {
        #         "orderId": "1099353730455318528",
        #         "tradeId": "1099353730627092481",
        #         "orderType": "market",
        #         "side": "sell",
        #         "priceAvg": "29543.7",
        #         "size": "0.0001",
        #         "amount": "2.95437",
        #         "tradeScope": "taker",
        #         "feeDetail": {
        #             "deduction": "no",
        #             "feeCoin": "USDT",
        #             "totalDeductionFee": "0",
        #             "totalFee": "-0.00295437"
        #         },
        #         "cTime": "1697832275063",
        #         "uTime": "1697832275150"
        #     }
        #
        # swap and future: fetchMyTrades
        #
        #     {
        #         "tradeId": "1111468664328269825",
        #         "symbol": "BTCUSDT",
        #         "orderId": "1111468664264753162",
        #         "price": "37271.4",
        #         "baseVolume": "0.001",
        #         "feeDetail": [
        #             {
        #                 "deduction": "no",
        #                 "feeCoin": "USDT",
        #                 "totalDeductionFee": null,
        #                 "totalFee": "-0.02236284"
        #             }
        #         ],
        #         "side": "buy",
        #         "quoteVolume": "37.2714",
        #         "profit": "-0.0007",
        #         "enterPointSource": "web",
        #         "tradeSide": "close",
        #         "posMode": "hedge_mode",
        #         "tradeScope": "taker",
        #         "cTime": "1700720700342"
        #     }
        #
        marketId = self.safe_string(trade, 'symbol')
        symbol = self.safe_symbol(marketId, market)
        timestamp = self.safe_integer_2(trade, 'cTime', 'ts')
        fee = None
        feeDetail = self.safe_value(trade, 'feeDetail')
        posMode = self.safe_string(trade, 'posMode')
        feeStructure = feeDetail[0] if (posMode is not None) else feeDetail
        if feeStructure is not None:
            currencyCode = self.safe_currency_code(self.safe_string(feeStructure, 'feeCoin'))
            fee = {
                'currency': currencyCode,
            }
            feeCostString = self.safe_string(feeStructure, 'totalFee')
            deduction = self.safe_string(feeStructure, 'deduction') is True if 'yes' else False
            if deduction:
                fee['cost'] = feeCostString
            else:
                fee['cost'] = Precise.string_neg(feeCostString)
        return self.safe_trade({
            'info': trade,
            'id': self.safe_string(trade, 'tradeId'),
            'order': self.safe_string(trade, 'orderId'),
            'symbol': symbol,
            'side': self.safe_string_lower(trade, 'side'),
            'type': self.safe_string(trade, 'orderType'),
            'takerOrMaker': self.safe_string(trade, 'tradeScope'),
            'price': self.safe_string_2(trade, 'priceAvg', 'price'),
            'amount': self.safe_string_2(trade, 'baseVolume', 'size'),
            'cost': self.safe_string_2(trade, 'quoteVolume', 'amount'),
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'fee': fee,
        }, market)

    def fetch_trades(self, symbol: str, since: Int = None, limit: Int = None, params={}) -> List[Trade]:
        """
        get the list of most recent trades for a particular symbol
        :see: https://www.bitget.com/api-doc/spot/market/Get-Recent-Trades
        :see: https://www.bitget.com/api-doc/spot/market/Get-Market-Trades
        :see: https://www.bitget.com/api-doc/contract/market/Get-Recent-Fills
        :see: https://www.bitget.com/api-doc/contract/market/Get-Fills-History
        :param str symbol: unified symbol of the market to fetch trades for
        :param int [since]: timestamp in ms of the earliest trade to fetch
        :param int [limit]: the maximum amount of trades to fetch
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :param int [params.until]: *only applies to publicSpotGetV2SpotMarketFillsHistory and publicMixGetV2MixMarketFillsHistory* the latest time in ms to fetch trades for
        :param boolean [params.paginate]: *only applies to publicSpotGetV2SpotMarketFillsHistory and publicMixGetV2MixMarketFillsHistory* default False, when True will automatically paginate by calling self endpoint multiple times
        :returns Trade[]: a list of `trade structures <https://docs.ccxt.com/#/?id=public-trades>`
        """
        self.load_markets()
        paginate = False
        paginate, params = self.handle_option_and_params(params, 'fetchTrades', 'paginate')
        if paginate:
            return self.fetch_paginated_call_cursor('fetchTrades', symbol, since, limit, params, 'idLessThan', 'idLessThan')
        sandboxMode = self.safe_bool(self.options, 'sandboxMode', False)
        market = None
        if sandboxMode:
            sandboxSymbol = self.convert_symbol_for_sandbox(symbol)
            market = self.market(sandboxSymbol)
        else:
            market = self.market(symbol)
        request: dict = {
            'symbol': market['id'],
        }
        if limit is not None:
            if market['contract']:
                request['limit'] = min(limit, 1000)
            else:
                request['limit'] = limit
        options = self.safe_value(self.options, 'fetchTrades', {})
        response = None
        if market['spot']:
            spotOptions = self.safe_value(options, 'spot', {})
            defaultSpotMethod = self.safe_string(spotOptions, 'method', 'publicSpotGetV2SpotMarketFillsHistory')
            spotMethod = self.safe_string(params, 'method', defaultSpotMethod)
            params = self.omit(params, 'method')
            if spotMethod == 'publicSpotGetV2SpotMarketFillsHistory':
                request, params = self.handle_until_option('endTime', request, params)
                if since is not None:
                    request['startTime'] = since
                response = self.publicSpotGetV2SpotMarketFillsHistory(self.extend(request, params))
            elif spotMethod == 'publicSpotGetV2SpotMarketFills':
                response = self.publicSpotGetV2SpotMarketFills(self.extend(request, params))
        else:
            swapOptions = self.safe_value(options, 'swap', {})
            defaultSwapMethod = self.safe_string(swapOptions, 'method', 'publicMixGetV2MixMarketFillsHistory')
            swapMethod = self.safe_string(params, 'method', defaultSwapMethod)
            params = self.omit(params, 'method')
            productType = None
            productType, params = self.handle_product_type_and_params(market, params)
            request['productType'] = productType
            if swapMethod == 'publicMixGetV2MixMarketFillsHistory':
                request, params = self.handle_until_option('endTime', request, params)
                if since is not None:
                    request['startTime'] = since
                response = self.publicMixGetV2MixMarketFillsHistory(self.extend(request, params))
            elif swapMethod == 'publicMixGetV2MixMarketFills':
                response = self.publicMixGetV2MixMarketFills(self.extend(request, params))
        #
        # spot
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1692073693562,
        #         "data": [
        #             {
        #                 "symbol": "BTCUSDT_SPBL",
        #                 "tradeId": "1075200479040323585",
        #                 "side": "Sell",
        #                 "price": "29381.54",
        #                 "size": "0.0056",
        #                 "ts": "1692073691000"
        #             },
        #         ]
        #     }
        #
        # swap
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1692073522689,
        #         "data": [
        #             {
        #                 "tradeId": "1075199767891652609",
        #                 "price": "29376.5",
        #                 "size": "6.035",
        #                 "side": "Buy",
        #                 "ts": "1692073521000",
        #                 "symbol": "BTCUSDT_UMCBL"
        #             },
        #         ]
        #     }
        #
        data = self.safe_list(response, 'data', [])
        return self.parse_trades(data, market, since, limit)

    def fetch_trading_fee(self, symbol: str, params={}) -> TradingFeeInterface:
        """
        fetch the trading fees for a market
        :see: https://www.bitget.com/api-doc/common/public/Get-Trade-Rate
        :param str symbol: unified market symbol
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :param str [params.marginMode]: 'isolated' or 'cross', for finding the fee rate of spot margin trading pairs
        :returns dict: a `fee structure <https://docs.ccxt.com/#/?id=fee-structure>`
        """
        self.load_markets()
        market = self.market(symbol)
        request: dict = {
            'symbol': market['id'],
        }
        marginMode = None
        marginMode, params = self.handle_margin_mode_and_params('fetchTradingFee', params)
        if market['spot']:
            if marginMode is not None:
                request['businessType'] = 'margin'
            else:
                request['businessType'] = 'spot'
        else:
            request['businessType'] = 'contract'
        response = self.privateCommonGetV2CommonTradeRate(self.extend(request, params))
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1700549524887,
        #         "data": {
        #             "makerFeeRate": "0.001",
        #             "takerFeeRate": "0.001"
        #         }
        #     }
        #
        data = self.safe_value(response, 'data', {})
        return self.parse_trading_fee(data, market)

    def fetch_trading_fees(self, params={}) -> TradingFees:
        """
        fetch the trading fees for multiple markets
        :see: https://www.bitget.com/api-doc/spot/market/Get-Symbols
        :see: https://www.bitget.com/api-doc/contract/market/Get-All-Symbols-Contracts
        :see: https://www.bitget.com/api-doc/margin/common/support-currencies
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :param str [params.productType]: *contract only* 'USDT-FUTURES', 'USDC-FUTURES', 'COIN-FUTURES', 'SUSDT-FUTURES', 'SUSDC-FUTURES' or 'SCOIN-FUTURES'
        :param boolean [params.margin]: set to True for spot margin
        :returns dict: a dictionary of `fee structures <https://docs.ccxt.com/#/?id=fee-structure>` indexed by market symbols
        """
        self.load_markets()
        response = None
        marginMode = None
        marketType = None
        marginMode, params = self.handle_margin_mode_and_params('fetchTradingFees', params)
        marketType, params = self.handle_market_type_and_params('fetchTradingFees', None, params)
        if marketType == 'spot':
            margin = self.safe_bool(params, 'margin', False)
            params = self.omit(params, 'margin')
            if (marginMode is not None) or margin:
                response = self.publicMarginGetV2MarginCurrencies(params)
            else:
                response = self.publicSpotGetV2SpotPublicSymbols(params)
        elif (marketType == 'swap') or (marketType == 'future'):
            productType = None
            productType, params = self.handle_product_type_and_params(None, params)
            params['productType'] = productType
            response = self.publicMixGetV2MixMarketContracts(params)
        else:
            raise NotSupported(self.id + ' does not support ' + marketType + ' market')
        #
        # spot and margin
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1700102364653,
        #         "data": [
        #             {
        #                 "symbol": "TRXUSDT",
        #                 "baseCoin": "TRX",
        #                 "quoteCoin": "USDT",
        #                 "minTradeAmount": "0",
        #                 "maxTradeAmount": "10000000000",
        #                 "takerFeeRate": "0.002",
        #                 "makerFeeRate": "0.002",
        #                 "pricePrecision": "6",
        #                 "quantityPrecision": "4",
        #                 "quotePrecision": "6",
        #                 "status": "online",
        #                 "minTradeUSDT": "5",
        #                 "buyLimitPriceRatio": "0.05",
        #                 "sellLimitPriceRatio": "0.05"
        #             },
        #         ]
        #     }
        #
        # swap and future
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1700102364709,
        #         "data": [
        #             {
        #                 "symbol": "BTCUSDT",
        #                 "baseCoin": "BTC",
        #                 "quoteCoin": "USDT",
        #                 "buyLimitPriceRatio": "0.01",
        #                 "sellLimitPriceRatio": "0.01",
        #                 "feeRateUpRatio": "0.005",
        #                 "makerFeeRate": "0.0002",
        #                 "takerFeeRate": "0.0006",
        #                 "openCostUpRatio": "0.01",
        #                 "supportMarginCoins": ["USDT"],
        #                 "minTradeNum": "0.001",
        #                 "priceEndStep": "1",
        #                 "volumePlace": "3",
        #                 "pricePlace": "1",
        #                 "sizeMultiplier": "0.001",
        #                 "symbolType": "perpetual",
        #                 "minTradeUSDT": "5",
        #                 "maxSymbolOrderNum": "200",
        #                 "maxProductOrderNum": "400",
        #                 "maxPositionNum": "150",
        #                 "symbolStatus": "normal",
        #                 "offTime": "-1",
        #                 "limitOpenTime": "-1",
        #                 "deliveryTime": "",
        #                 "deliveryStartTime": "",
        #                 "deliveryPeriod": "",
        #                 "launchTime": "",
        #                 "fundInterval": "8",
        #                 "minLever": "1",
        #                 "maxLever": "125",
        #                 "posLimit": "0.05",
        #                 "maintainTime": ""
        #             },
        #         ]
        #     }
        #
        data = self.safe_value(response, 'data', [])
        result: dict = {}
        for i in range(0, len(data)):
            entry = data[i]
            marketId = self.safe_string(entry, 'symbol')
            symbol = self.safe_symbol(marketId, None, None, marketType)
            market = self.market(symbol)
            fee = self.parse_trading_fee(entry, market)
            result[symbol] = fee
        return result

    def parse_trading_fee(self, data, market: Market = None):
        marketId = self.safe_string(data, 'symbol')
        return {
            'info': data,
            'symbol': self.safe_symbol(marketId, market),
            'maker': self.safe_number(data, 'makerFeeRate'),
            'taker': self.safe_number(data, 'takerFeeRate'),
            'percentage': None,
            'tierBased': None,
        }

    def parse_ohlcv(self, ohlcv, market: Market = None) -> list:
        #
        #     [
        #         "1645911960000",
        #         "39406",
        #         "39407",
        #         "39374.5",
        #         "39379",
        #         "35.526",
        #         "1399132.341"
        #     ]
        #
        return [
            self.safe_integer(ohlcv, 0),
            self.safe_number(ohlcv, 1),
            self.safe_number(ohlcv, 2),
            self.safe_number(ohlcv, 3),
            self.safe_number(ohlcv, 4),
            self.safe_number(ohlcv, 5),
        ]

    def fetch_ohlcv(self, symbol: str, timeframe='1m', since: Int = None, limit: Int = None, params={}) -> List[list]:
        """
        fetches historical candlestick data containing the open, high, low, and close price, and the volume of a market
        :see: https://www.bitget.com/api-doc/spot/market/Get-Candle-Data
        :see: https://www.bitget.com/api-doc/spot/market/Get-History-Candle-Data
        :see: https://www.bitget.com/api-doc/contract/market/Get-Candle-Data
        :see: https://www.bitget.com/api-doc/contract/market/Get-History-Candle-Data
        :see: https://www.bitget.com/api-doc/contract/market/Get-History-Index-Candle-Data
        :see: https://www.bitget.com/api-doc/contract/market/Get-History-Mark-Candle-Data
        :param str symbol: unified symbol of the market to fetch OHLCV data for
        :param str timeframe: the length of time each candle represents
        :param int [since]: timestamp in ms of the earliest candle to fetch
        :param int [limit]: the maximum amount of candles to fetch
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :param int [params.until]: timestamp in ms of the latest candle to fetch
        :param boolean [params.paginate]: default False, when True will automatically paginate by calling self endpoint multiple times. See in the docs all the [available parameters](https://github.com/ccxt/ccxt/wiki/Manual#pagination-params)
        :param str [params.price]: *swap only* "mark"(to fetch mark price candles) or "index"(to fetch index price candles)
        :returns int[][]: A list of candles ordered, open, high, low, close, volume
        """
        self.load_markets()
        defaultLimit = 100  # default 100, max 1000
        maxLimitForRecentEndpoint = 1000
        maxLimitForHistoryEndpoint = 200  # note, max 1000 bars are supported for "recent-candles" endpoint, but "historical-candles" support only max 200
        paginate = False
        paginate, params = self.handle_option_and_params(params, 'fetchOHLCV', 'paginate')
        if paginate:
            return self.fetch_paginated_call_deterministic('fetchOHLCV', symbol, since, limit, timeframe, params, maxLimitForHistoryEndpoint)
        sandboxMode = self.safe_bool(self.options, 'sandboxMode', False)
        market = None
        if sandboxMode:
            sandboxSymbol = self.convert_symbol_for_sandbox(symbol)
            market = self.market(sandboxSymbol)
        else:
            market = self.market(symbol)
        marketType = 'spot' if market['spot'] else 'swap'
        timeframes = self.options['timeframes'][marketType]
        msInDay = 86400000
        duration = self.parse_timeframe(timeframe) * 1000
        request: dict = {
            'symbol': market['id'],
            'granularity': self.safe_string(timeframes, timeframe, timeframe),
        }
        until = self.safe_integer(params, 'until')
        limitDefined = limit is not None
        sinceDefined = since is not None
        untilDefined = until is not None
        params = self.omit(params, ['until'])
        response = None
        now = self.milliseconds()
        # retrievable periods listed here:
        # - https://www.bitget.com/api-doc/spot/market/Get-Candle-Data#request-parameters
        # - https://www.bitget.com/api-doc/contract/market/Get-Candle-Data#description
        ohlcOptions = self.safe_dict(self.options, 'fetchOHLCV', {})
        retrievableDaysMap = self.safe_dict(ohlcOptions, 'maxDaysPerTimeframe', {})
        maxRetrievableDaysForRecent = self.safe_integer(retrievableDaysMap, timeframe, 30)  # default to safe minimum
        endpointTsBoundary = now - maxRetrievableDaysForRecent * msInDay
        if limitDefined:
            limit = min(limit, maxLimitForRecentEndpoint)
            request['limit'] = limit
        else:
            limit = defaultLimit
        limitMultipliedDuration = limit * duration
        # exchange aligns from endTime, so it's important, not startTime
        # startTime is supported only on "recent" endpoint, not on "historical" endpoint
        calculatedStartTime = None
        calculatedEndTime = None
        if sinceDefined:
            calculatedStartTime = since
            request['startTime'] = since
            if not untilDefined:
                calculatedEndTime = self.sum(calculatedStartTime, limitMultipliedDuration)
                request['endTime'] = calculatedEndTime
        if untilDefined:
            calculatedEndTime = until
            request['endTime'] = calculatedEndTime
            if not sinceDefined:
                calculatedStartTime = calculatedEndTime - limitMultipliedDuration
                # we do not need to set "startTime" here
        historicalEndpointNeeded = (calculatedStartTime is not None) and (calculatedStartTime <= endpointTsBoundary)
        if historicalEndpointNeeded:
            # only for "historical-candles" - ensure we use correct max limit
            if limitDefined:
                request['limit'] = min(limit, maxLimitForHistoryEndpoint)
        # make request
        if market['spot']:
            # checks if we need history endpoint
            if historicalEndpointNeeded:
                response = self.publicSpotGetV2SpotMarketHistoryCandles(self.extend(request, params))
            else:
                response = self.publicSpotGetV2SpotMarketCandles(self.extend(request, params))
        else:
            maxDistanceDaysForContracts = 90  # for contract, maximum 90 days allowed between start-end times
            # only correct the request to fix 90 days if until was auto-calculated
            if sinceDefined:
                if not untilDefined:
                    request['endTime'] = min(calculatedEndTime, self.sum(since, maxDistanceDaysForContracts * msInDay))
                elif calculatedEndTime - calculatedStartTime > maxDistanceDaysForContracts * msInDay:
                    raise BadRequest(self.id + ' fetchOHLCV() between start and end must be less than ' + str(maxDistanceDaysForContracts) + ' days')
            priceType = None
            priceType, params = self.handle_param_string(params, 'price')
            productType = None
            productType, params = self.handle_product_type_and_params(market, params)
            request['productType'] = productType
            extended = self.extend(request, params)
            # todo: mark & index also have their "recent" endpoints, but not priority now.
            if priceType == 'mark':
                response = self.publicMixGetV2MixMarketHistoryMarkCandles(extended)
            elif priceType == 'index':
                response = self.publicMixGetV2MixMarketHistoryIndexCandles(extended)
            else:
                if historicalEndpointNeeded:
                    response = self.publicMixGetV2MixMarketHistoryCandles(extended)
                else:
                    response = self.publicMixGetV2MixMarketCandles(extended)
        if response == '':
            return []  # happens when a new token is listed
        #  [["1645911960000","39406","39407","39374.5","39379","35.526","1399132.341"]]
        data = self.safe_list(response, 'data', response)
        return self.parse_ohlcvs(data, market, timeframe, since, limit)

    def fetch_balance(self, params={}) -> Balances:
        """
        query for balance and get the amount of funds available for trading or funds locked in orders
        :see: https://www.bitget.com/api-doc/spot/account/Get-Account-Assets
        :see: https://www.bitget.com/api-doc/contract/account/Get-Account-List
        :see: https://www.bitget.com/api-doc/margin/cross/account/Get-Cross-Assets
        :see: https://www.bitget.com/api-doc/margin/isolated/account/Get-Isolated-Assets
        :see: https://bitgetlimited.github.io/apidoc/en/margin/#get-cross-assets
        :see: https://bitgetlimited.github.io/apidoc/en/margin/#get-isolated-assets
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :param str [params.productType]: *contract only* 'USDT-FUTURES', 'USDC-FUTURES', 'COIN-FUTURES', 'SUSDT-FUTURES', 'SUSDC-FUTURES' or 'SCOIN-FUTURES'
        :returns dict: a `balance structure <https://docs.ccxt.com/#/?id=balance-structure>`
        """
        self.load_markets()
        request: dict = {}
        marketType = None
        marginMode = None
        response = None
        marketType, params = self.handle_market_type_and_params('fetchBalance', None, params)
        marginMode, params = self.handle_margin_mode_and_params('fetchBalance', params)
        if (marketType == 'swap') or (marketType == 'future'):
            productType = None
            productType, params = self.handle_product_type_and_params(None, params)
            request['productType'] = productType
            response = self.privateMixGetV2MixAccountAccounts(self.extend(request, params))
        elif marginMode == 'isolated':
            response = self.privateMarginGetMarginV1IsolatedAccountAssets(self.extend(request, params))
        elif marginMode == 'cross':
            response = self.privateMarginGetMarginV1CrossAccountAssets(self.extend(request, params))
        elif marketType == 'spot':
            response = self.privateSpotGetV2SpotAccountAssets(self.extend(request, params))
        else:
            raise NotSupported(self.id + ' fetchBalance() does not support ' + marketType + ' accounts')
        # spot
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1700623852854,
        #         "data": [
        #             {
        #                 "coin": "USDT",
        #                 "available": "0.00000000",
        #                 "limitAvailable": "0",
        #                 "frozen": "0.00000000",
        #                 "locked": "0.00000000",
        #                 "uTime": "1699937566000"
        #             }
        #         ]
        #     }
        #
        # swap
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1700625127294,
        #         "data": [
        #             {
        #                 "marginCoin": "USDT",
        #                 "locked": "0",
        #                 "available": "0",
        #                 "crossedMaxAvailable": "0",
        #                 "isolatedMaxAvailable": "0",
        #                 "maxTransferOut": "0",
        #                 "accountEquity": "0",
        #                 "usdtEquity": "0.000000005166",
        #                 "btcEquity": "0",
        #                 "crossedRiskRate": "0",
        #                 "unrealizedPL": "0",
        #                 "coupon": "0",
        #                 "crossedUnrealizedPL": null,
        #                 "isolatedUnrealizedPL": null
        #             }
        #         ]
        #     }
        #
        # isolated margin
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1697501436571,
        #         "data": [
        #             {
        #                 "symbol": "BTCUSDT",
        #                 "coin": "BTC",
        #                 "totalAmount": "0.00021654",
        #                 "available": "0.00021654",
        #                 "transferable": "0.00021654",
        #                 "frozen": "0",
        #                 "borrow": "0",
        #                 "interest": "0",
        #                 "net": "0.00021654",
        #                 "ctime": "1697248128071"
        #             },
        #         ]
        #     }
        #
        # cross margin
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1697515463804,
        #         "data": [
        #             {
        #                 "coin": "BTC",
        #                 "totalAmount": "0.00024996",
        #                 "available": "0.00024996",
        #                 "transferable": "0.00004994",
        #                 "frozen": "0",
        #                 "borrow": "0.0001",
        #                 "interest": "0.00000001",
        #                 "net": "0.00014995",
        #                 "ctime": "1697251265504"
        #             },
        #         ]
        #     }
        #
        data = self.safe_value(response, 'data', [])
        return self.parse_balance(data)

    def parse_balance(self, balance) -> Balances:
        result: dict = {'info': balance}
        #
        # spot
        #
        #     {
        #         "coin": "USDT",
        #         "available": "0.00000000",
        #         "limitAvailable": "0",
        #         "frozen": "0.00000000",
        #         "locked": "0.00000000",
        #         "uTime": "1699937566000"
        #     }
        #
        # swap
        #
        #     {
        #         "marginCoin": "USDT",
        #         "locked": "0",
        #         "available": "0",
        #         "crossedMaxAvailable": "0",
        #         "isolatedMaxAvailable": "0",
        #         "maxTransferOut": "0",
        #         "accountEquity": "0",
        #         "usdtEquity": "0.000000005166",
        #         "btcEquity": "0",
        #         "crossedRiskRate": "0",
        #         "unrealizedPL": "0",
        #         "coupon": "0",
        #         "crossedUnrealizedPL": null,
        #         "isolatedUnrealizedPL": null
        #     }
        #
        # isolated margin
        #
        #     {
        #         "symbol": "BTCUSDT",
        #         "coin": "BTC",
        #         "totalAmount": "0.00021654",
        #         "available": "0.00021654",
        #         "transferable": "0.00021654",
        #         "frozen": "0",
        #         "borrow": "0",
        #         "interest": "0",
        #         "net": "0.00021654",
        #         "ctime": "1697248128071"
        #     }
        #
        # cross margin
        #
        #     {
        #         "coin": "BTC",
        #         "totalAmount": "0.00024995",
        #         "available": "0.00024995",
        #         "transferable": "0.00004993",
        #         "frozen": "0",
        #         "borrow": "0.0001",
        #         "interest": "0.00000001",
        #         "net": "0.00014994",
        #         "ctime": "1697251265504"
        #     }
        #
        for i in range(0, len(balance)):
            entry = balance[i]
            account = self.account()
            currencyId = self.safe_string_2(entry, 'marginCoin', 'coin')
            code = self.safe_currency_code(currencyId)
            borrow = self.safe_string(entry, 'borrow')
            if borrow is not None:
                interest = self.safe_string(entry, 'interest')
                account['free'] = self.safe_string(entry, 'transferable')
                account['total'] = self.safe_string(entry, 'totalAmount')
                account['debt'] = Precise.string_add(borrow, interest)
            else:
                # Use transferable instead of available for swap and margin https://github.com/ccxt/ccxt/pull/19127
                spotAccountFree = self.safe_string(entry, 'available')
                contractAccountFree = self.safe_string(entry, 'maxTransferOut')
                if contractAccountFree is not None:
                    account['free'] = contractAccountFree
                    account['total'] = self.safe_string(entry, 'accountEquity')
                else:
                    account['free'] = spotAccountFree
                    frozen = self.safe_string(entry, 'frozen')
                    locked = self.safe_string(entry, 'locked')
                    account['used'] = Precise.string_add(frozen, locked)
            result[code] = account
        return self.safe_balance(result)

    def parse_order_status(self, status: Str):
        statuses: dict = {
            'new': 'open',
            'init': 'open',
            'not_trigger': 'open',
            'partial_fill': 'open',
            'partially_fill': 'open',
            'partially_filled': 'open',
            'triggered': 'closed',
            'full_fill': 'closed',
            'filled': 'closed',
            'fail_trigger': 'rejected',
            'cancel': 'canceled',
            'cancelled': 'canceled',
            'canceled': 'canceled',
            'live': 'open',
            'fail_execute': 'rejected',
            'executed': 'closed',
        }
        return self.safe_string(statuses, status, status)

    def parse_order(self, order: dict, market: Market = None) -> Order:
        #
        # createOrder, editOrder, closePosition
        #
        #     {
        #         "clientOid": "abe95dbe-6081-4a6f-a2d3-ae49601cd479",
        #         "orderId": null
        #     }
        #
        # createOrders
        #
        #     [
        #         {
        #             "orderId": "1111397214281175046",
        #             "clientOid": "766d3fc3-7321-4406-a689-15c9987a2e75"
        #         },
        #         {
        #             "orderId": "",
        #             "clientOid": "d1b75cb3-cc15-4ede-ad4c-3937396f75ab",
        #             "errorMsg": "less than the minimum amount 5 USDT",
        #             "errorCode": "45110"
        #         },
        #     ]
        #
        # spot, swap, future and spot margin: cancelOrder, cancelOrders
        #
        #     {
        #         "orderId": "1098758604547850241",
        #         "clientOid": "1098758604585598977"
        #     }
        #
        # spot trigger: cancelOrder
        #
        #     {
        #         "result": "success"
        #     }
        #
        # spot: fetchOrder
        #
        #     {
        #         "userId": "7264631750",
        #         "symbol": "BTCUSDT",
        #         "orderId": "1111461743123927040",
        #         "clientOid": "63f95110-93b5-4309-8f77-46339f1bcf3c",
        #         "price": "25000.0000000000000000",
        #         "size": "0.0002000000000000",
        #         "orderType": "limit",
        #         "side": "buy",
        #         "status": "live",
        #         "priceAvg": "0",
        #         "baseVolume": "0.0000000000000000",
        #         "quoteVolume": "0.0000000000000000",
        #         "enterPointSource": "API",
        #         "feeDetail": "",
        #         "orderSource": "normal",
        #         "cTime": "1700719050198",
        #         "uTime": "1700719050198"
        #     }
        #
        # swap and future: fetchOrder
        #
        #     {
        #         "symbol": "BTCUSDT",
        #         "size": "0.001",
        #         "orderId": "1111465253393825792",
        #         "clientOid": "1111465253431574529",
        #         "baseVolume": "0",
        #         "fee": "0",
        #         "price": "27000",
        #         "priceAvg": "",
        #         "state": "live",
        #         "side": "buy",
        #         "force": "gtc",
        #         "totalProfits": "0",
        #         "posSide": "long",
        #         "marginCoin": "USDT",
        #         "presetStopSurplusPrice": "",
        #         "presetStopLossPrice": "",
        #         "quoteVolume": "0",
        #         "orderType": "limit",
        #         "leverage": "20",
        #         "marginMode": "crossed",
        #         "reduceOnly": "NO",
        #         "enterPointSource": "API",
        #         "tradeSide": "open",
        #         "posMode": "hedge_mode",
        #         "orderSource": "normal",
        #         "cTime": "1700719887120",
        #         "uTime": "1700719887120"
        #     }
        #
        # spot: fetchOpenOrders
        #
        #     {
        #         "userId": "7264631750",
        #         "symbol": "BTCUSDT",
        #         "orderId": "1111499608327360513",
        #         "clientOid": "d0d4dad5-18d0-4869-a074-ec40bb47cba6",
        #         "priceAvg": "25000.0000000000000000",
        #         "size": "0.0002000000000000",
        #         "orderType": "limit",
        #         "side": "buy",
        #         "status": "live",
        #         "basePrice": "0",
        #         "baseVolume": "0.0000000000000000",
        #         "quoteVolume": "0.0000000000000000",
        #         "enterPointSource": "WEB",
        #         "orderSource": "normal",
        #         "cTime": "1700728077966",
        #         "uTime": "1700728077966"
        #     }
        #
        # spot stop: fetchOpenOrders, fetchCanceledAndClosedOrders
        #
        #     {
        #         "orderId": "1111503385931620352",
        #         "clientOid": "1111503385910648832",
        #         "symbol": "BTCUSDT",
        #         "size": "0.0002",
        #         "planType": "AMOUNT",
        #         "executePrice": "25000",
        #         "triggerPrice": "26000",
        #         "status": "live",
        #         "orderType": "limit",
        #         "side": "buy",
        #         "triggerType": "fill_price",
        #         "enterPointSource": "API",
        #         "cTime": "1700728978617",
        #         "uTime": "1700728978617"
        #     }
        #
        # spot margin: fetchOpenOrders, fetchCanceledAndClosedOrders
        #
        #     {
        #         "symbol": "BTCUSDT",
        #         "orderType": "limit",
        #         "enterPointSource": "WEB",
        #         "orderId": "1111506377509580801",
        #         "clientOid": "2043a3b59a60445f9d9f7365bf3e960c",
        #         "loanType": "autoLoanAndRepay",
        #         "price": "25000",
        #         "side": "buy",
        #         "status": "live",
        #         "baseSize": "0.0002",
        #         "quoteSize": "5",
        #         "priceAvg": "0",
        #         "size": "0",
        #         "amount": "0",
        #         "force": "gtc",
        #         "cTime": "1700729691866",
        #         "uTime": "1700729691866"
        #     }
        #
        # swap: fetchOpenOrders, fetchCanceledAndClosedOrders
        #
        #     {
        #         "symbol": "BTCUSDT",
        #         "size": "0.002",
        #         "orderId": "1111488897767604224",
        #         "clientOid": "1111488897805352960",
        #         "baseVolume": "0",
        #         "fee": "0",
        #         "price": "25000",
        #         "priceAvg": "",
        #         "status": "live",
        #         "side": "buy",
        #         "force": "gtc",
        #         "totalProfits": "0",
        #         "posSide": "long",
        #         "marginCoin": "USDT",
        #         "quoteVolume": "0",
        #         "leverage": "20",
        #         "marginMode": "crossed",
        #         "enterPointSource": "web",
        #         "tradeSide": "open",
        #         "posMode": "hedge_mode",
        #         "orderType": "limit",
        #         "orderSource": "normal",
        #         "presetStopSurplusPrice": "",
        #         "presetStopLossPrice": "",
        #         "reduceOnly": "NO",
        #         "cTime": "1700725524378",
        #         "uTime": "1700725524378"
        #     }
        #
        # swap stop: fetchOpenOrders
        #
        #     {
        #         "planType": "normal_plan",
        #         "symbol": "BTCUSDT",
        #         "size": "0.001",
        #         "orderId": "1111491399869075457",
        #         "clientOid": "1111491399869075456",
        #         "price": "27000",
        #         "callbackRatio": "",
        #         "triggerPrice": "24000",
        #         "triggerType": "mark_price",
        #         "planStatus": "live",
        #         "side": "buy",
        #         "posSide": "long",
        #         "marginCoin": "USDT",
        #         "marginMode": "crossed",
        #         "enterPointSource": "API",
        #         "tradeSide": "open",
        #         "posMode": "hedge_mode",
        #         "orderType": "limit",
        #         "stopSurplusTriggerPrice": "",
        #         "stopSurplusExecutePrice": "",
        #         "stopSurplusTriggerType": "fill_price",
        #         "stopLossTriggerPrice": "",
        #         "stopLossExecutePrice": "",
        #         "stopLossTriggerType": "fill_price",
        #         "cTime": "1700726120917",
        #         "uTime": "1700726120917"
        #     }
        #
        # spot: fetchCanceledAndClosedOrders
        #
        #     {
        #         "userId": "7264631750",
        #         "symbol": "BTCUSDT",
        #         "orderId": "1111499608327360513",
        #         "clientOid": "d0d4dad5-18d0-4869-a074-ec40bb47cba6",
        #         "price": "25000.0000000000000000",
        #         "size": "0.0002000000000000",
        #         "orderType": "limit",
        #         "side": "buy",
        #         "status": "cancelled",
        #         "priceAvg": "0",
        #         "baseVolume": "0.0000000000000000",
        #         "quoteVolume": "0.0000000000000000",
        #         "enterPointSource": "WEB",
        #         "feeDetail": "",
        #         "orderSource": "normal",
        #         "cTime": "1700728077966",
        #         "uTime": "1700728911471"
        #     }
        #
        # swap stop: fetchCanceledAndClosedOrders
        #
        #     {
        #         "planType": "normal_plan",
        #         "symbol": "BTCUSDT",
        #         "size": "0.001",
        #         "orderId": "1111491399869075457",
        #         "clientOid": "1111491399869075456",
        #         "planStatus": "cancelled",
        #         "price": "27000",
        #         "feeDetail": null,
        #         "baseVolume": "0",
        #         "callbackRatio": "",
        #         "triggerPrice": "24000",
        #         "triggerType": "mark_price",
        #         "side": "buy",
        #         "posSide": "long",
        #         "marginCoin": "USDT",
        #         "marginMode": "crossed",
        #         "enterPointSource": "API",
        #         "tradeSide": "open",
        #         "posMode": "hedge_mode",
        #         "orderType": "limit",
        #         "stopSurplusTriggerPrice": "",
        #         "stopSurplusExecutePrice": "",
        #         "stopSurplusTriggerType": "fill_price",
        #         "stopLossTriggerPrice": "",
        #         "stopLossExecutePrice": "",
        #         "stopLossTriggerType": "fill_price",
        #         "cTime": "1700726120917",
        #         "uTime": "1700727879652"
        #     }
        #
        errorMessage = self.safe_string(order, 'errorMsg')
        if errorMessage is not None:
            return self.safe_order({
                'info': order,
                'id': self.safe_string(order, 'orderId'),
                'clientOrderId': self.safe_string_2(order, 'clientOrderId', 'clientOid'),
                'status': 'rejected',
            }, market)
        isContractOrder = ('posSide' in order)
        marketType = 'contract' if isContractOrder else 'spot'
        if market is not None:
            marketType = market['type']
        marketId = self.safe_string(order, 'symbol')
        market = self.safe_market(marketId, market, None, marketType)
        timestamp = self.safe_integer_2(order, 'cTime', 'ctime')
        updateTimestamp = self.safe_integer(order, 'uTime')
        rawStatus = self.safe_string_2(order, 'status', 'state')
        fee = None
        feeCostString = self.safe_string(order, 'fee')
        if feeCostString is not None:
            # swap
            fee = {
                'cost': self.parse_number(Precise.string_neg(feeCostString)),
                'currency': market['settle'],
            }
        feeDetail = self.safe_value(order, 'feeDetail')
        if feeDetail is not None:
            parsedFeeDetail = json.loads(feeDetail)
            feeValues = list(parsedFeeDetail.values())
            feeObject = None
            for i in range(0, len(feeValues)):
                feeValue = feeValues[i]
                if self.safe_value(feeValue, 'feeCoinCode') is not None:
                    feeObject = feeValue
                    break
            fee = {
                'cost': self.parse_number(Precise.string_neg(self.safe_string(feeObject, 'totalFee'))),
                'currency': self.safe_currency_code(self.safe_string(feeObject, 'feeCoinCode')),
            }
        postOnly = None
        timeInForce = self.safe_string_upper(order, 'force')
        if timeInForce == 'POST_ONLY':
            postOnly = True
            timeInForce = 'PO'
        reduceOnly = None
        reduceOnlyRaw = self.safe_string(order, 'reduceOnly')
        if reduceOnlyRaw is not None:
            reduceOnly = False if (reduceOnlyRaw == 'NO') else True
        price = None
        average = None
        basePrice = self.safe_string(order, 'basePrice')
        if basePrice is not None:
            # for spot fetchOpenOrders, the price is priceAvg and the filled price is basePrice
            price = self.safe_string(order, 'priceAvg')
            average = self.safe_string(order, 'basePrice')
        else:
            price = self.safe_string_2(order, 'price', 'executePrice')
            average = self.safe_string(order, 'priceAvg')
        size = None
        filled = None
        baseSize = self.safe_string(order, 'baseSize')
        if baseSize is not None:
            # for spot margin fetchOpenOrders, the order size is baseSize and the filled amount is size
            size = baseSize
            filled = self.safe_string(order, 'size')
        else:
            size = self.safe_string(order, 'size')
            filled = self.safe_string(order, 'baseVolume')
        side = self.safe_string(order, 'side')
        posMode = self.safe_string(order, 'posMode')
        if posMode == 'hedge_mode' and reduceOnly:
            side = 'sell' if (side == 'buy') else 'buy'
            # on bitget hedge mode if the position is long the side is always buy, and if the position is short the side is always sell
            # so the side of the reduceOnly order is inversed
        return self.safe_order({
            'info': order,
            'id': self.safe_string_2(order, 'orderId', 'data'),
            'clientOrderId': self.safe_string_2(order, 'clientOrderId', 'clientOid'),
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastTradeTimestamp': updateTimestamp,
            'lastUpdateTimestamp': updateTimestamp,
            'symbol': market['symbol'],
            'type': self.safe_string(order, 'orderType'),
            'side': side,
            'price': price,
            'amount': size,
            'cost': self.safe_string_2(order, 'quoteVolume', 'quoteSize'),
            'average': average,
            'filled': filled,
            'remaining': None,
            'timeInForce': timeInForce,
            'postOnly': postOnly,
            'reduceOnly': reduceOnly,
            'stopPrice': self.safe_number(order, 'triggerPrice'),
            'triggerPrice': self.safe_number(order, 'triggerPrice'),
            'takeProfitPrice': self.safe_number_2(order, 'presetStopSurplusPrice', 'stopSurplusTriggerPrice'),
            'stopLossPrice': self.safe_number_2(order, 'presetStopLossPrice', 'stopLossTriggerPrice'),
            'status': self.parse_order_status(rawStatus),
            'fee': fee,
            'trades': None,
        }, market)

    def create_market_buy_order_with_cost(self, symbol: str, cost: float, params={}):
        """
        create a market buy order by providing the symbol and cost
        :see: https://www.bitget.com/api-doc/spot/trade/Place-Order
        :see: https://www.bitget.com/api-doc/margin/cross/trade/Cross-Place-Order
        :see: https://www.bitget.com/api-doc/margin/isolated/trade/Isolated-Place-Order
        :param str symbol: unified symbol of the market to create an order in
        :param float cost: how much you want to trade in units of the quote currency
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict: an `order structure <https://docs.ccxt.com/#/?id=order-structure>`
        """
        self.load_markets()
        market = self.market(symbol)
        if not market['spot']:
            raise NotSupported(self.id + ' createMarketBuyOrderWithCost() supports spot orders only')
        params['createMarketBuyOrderRequiresPrice'] = False
        return self.create_order(symbol, 'market', 'buy', cost, None, params)

    def create_order(self, symbol: str, type: OrderType, side: OrderSide, amount: float, price: Num = None, params={}):
        """
        create a trade order
        :see: https://www.bitget.com/api-doc/spot/trade/Place-Order
        :see: https://www.bitget.com/api-doc/spot/plan/Place-Plan-Order
        :see: https://www.bitget.com/api-doc/contract/trade/Place-Order
        :see: https://www.bitget.com/api-doc/contract/plan/Place-Tpsl-Order
        :see: https://www.bitget.com/api-doc/contract/plan/Place-Plan-Order
        :see: https://www.bitget.com/api-doc/margin/cross/trade/Cross-Place-Order
        :see: https://www.bitget.com/api-doc/margin/isolated/trade/Isolated-Place-Order
        :param str symbol: unified symbol of the market to create an order in
        :param str type: 'market' or 'limit'
        :param str side: 'buy' or 'sell'
        :param float amount: how much you want to trade in units of the base currency
        :param float [price]: the price at which the order is to be fulfilled, in units of the quote currency, ignored in market orders
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :param float [params.cost]: *spot only* how much you want to trade in units of the quote currency, for market buy orders only
        :param float [params.triggerPrice]: *swap only* The price at which a trigger order is triggered at
        :param float [params.stopLossPrice]: *swap only* The price at which a stop loss order is triggered at
        :param float [params.takeProfitPrice]: *swap only* The price at which a take profit order is triggered at
        :param dict [params.takeProfit]: *takeProfit object in params* containing the triggerPrice at which the attached take profit order will be triggered(perpetual swap markets only)
        :param float [params.takeProfit.triggerPrice]: *swap only* take profit trigger price
        :param dict [params.stopLoss]: *stopLoss object in params* containing the triggerPrice at which the attached stop loss order will be triggered(perpetual swap markets only)
        :param float [params.stopLoss.triggerPrice]: *swap only* stop loss trigger price
        :param str [params.timeInForce]: "GTC", "IOC", "FOK", or "PO"
        :param str [params.marginMode]: 'isolated' or 'cross' for spot margin trading
        :param str [params.loanType]: *spot margin only* 'normal', 'autoLoan', 'autoRepay', or 'autoLoanAndRepay' default is 'normal'
        :param str [params.holdSide]: *contract stopLossPrice, takeProfitPrice only* Two-way position: ('long' or 'short'), one-way position: ('buy' or 'sell')
        :param float [params.stopLoss.price]: *swap only* the execution price for a stop loss attached to a trigger order
        :param float [params.takeProfit.price]: *swap only* the execution price for a take profit attached to a trigger order
        :param str [params.stopLoss.type]: *swap only* the type for a stop loss attached to a trigger order, 'fill_price', 'index_price' or 'mark_price', default is 'mark_price'
        :param str [params.takeProfit.type]: *swap only* the type for a take profit attached to a trigger order, 'fill_price', 'index_price' or 'mark_price', default is 'mark_price'
        :param str [params.trailingPercent]: *swap and future only* the percent to trail away from the current market price, rate can not be greater than 10
        :param str [params.trailingTriggerPrice]: *swap and future only* the price to trigger a trailing stop order, default uses the price argument
        :param str [params.triggerType]: *swap and future only* 'fill_price', 'mark_price' or 'index_price'
        :param boolean [params.oneWayMode]: *swap and future only* required to set self to True in one_way_mode and you can leave self in hedge_mode, can adjust the mode using the setPositionMode() method
        :param bool [params.reduceOnly]: True or False whether the order is reduce-only
        :returns dict: an `order structure <https://docs.ccxt.com/#/?id=order-structure>`
        """
        self.load_markets()
        market = self.market(symbol)
        marginParams = self.handle_margin_mode_and_params('createOrder', params)
        marginMode = marginParams[0]
        triggerPrice = self.safe_value_2(params, 'stopPrice', 'triggerPrice')
        stopLossTriggerPrice = self.safe_value(params, 'stopLossPrice')
        takeProfitTriggerPrice = self.safe_value(params, 'takeProfitPrice')
        trailingPercent = self.safe_string_2(params, 'trailingPercent', 'callbackRatio')
        isTrailingPercentOrder = trailingPercent is not None
        isTriggerOrder = triggerPrice is not None
        isStopLossTriggerOrder = stopLossTriggerPrice is not None
        isTakeProfitTriggerOrder = takeProfitTriggerPrice is not None
        isStopLossOrTakeProfitTrigger = isStopLossTriggerOrder or isTakeProfitTriggerOrder
        request = self.create_order_request(symbol, type, side, amount, price, params)
        response = None
        if market['spot']:
            if isTriggerOrder:
                response = self.privateSpotPostV2SpotTradePlacePlanOrder(request)
            elif marginMode == 'isolated':
                response = self.privateMarginPostV2MarginIsolatedPlaceOrder(request)
            elif marginMode == 'cross':
                response = self.privateMarginPostV2MarginCrossedPlaceOrder(request)
            else:
                response = self.privateSpotPostV2SpotTradePlaceOrder(request)
        else:
            if isTriggerOrder or isTrailingPercentOrder:
                response = self.privateMixPostV2MixOrderPlacePlanOrder(request)
            elif isStopLossOrTakeProfitTrigger:
                response = self.privateMixPostV2MixOrderPlaceTpslOrder(request)
            else:
                response = self.privateMixPostV2MixOrderPlaceOrder(request)
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1645932209602,
        #         "data": {
        #             "orderId": "881669078313766912",
        #             "clientOid": "iauIBf#a45b595f96474d888d0ada"
        #         }
        #     }
        #
        data = self.safe_dict(response, 'data', {})
        return self.parse_order(data, market)

    def create_order_request(self, symbol: str, type: OrderType, side: OrderSide, amount: float, price: Num = None, params={}):
        sandboxMode = self.safe_bool(self.options, 'sandboxMode', False)
        market = None
        if sandboxMode:
            sandboxSymbol = self.convert_symbol_for_sandbox(symbol)
            market = self.market(sandboxSymbol)
        else:
            market = self.market(symbol)
        marketType = None
        marginMode = None
        marketType, params = self.handle_market_type_and_params('createOrder', market, params)
        marginMode, params = self.handle_margin_mode_and_params('createOrder', params)
        request: dict = {
            'symbol': market['id'],
            'orderType': type,
        }
        isMarketOrder = type == 'market'
        triggerPrice = self.safe_value_2(params, 'stopPrice', 'triggerPrice')
        stopLossTriggerPrice = self.safe_value(params, 'stopLossPrice')
        takeProfitTriggerPrice = self.safe_value(params, 'takeProfitPrice')
        stopLoss = self.safe_value(params, 'stopLoss')
        takeProfit = self.safe_value(params, 'takeProfit')
        isTriggerOrder = triggerPrice is not None
        isStopLossTriggerOrder = stopLossTriggerPrice is not None
        isTakeProfitTriggerOrder = takeProfitTriggerPrice is not None
        isStopLoss = stopLoss is not None
        isTakeProfit = takeProfit is not None
        isStopLossOrTakeProfitTrigger = isStopLossTriggerOrder or isTakeProfitTriggerOrder
        isStopLossOrTakeProfit = isStopLoss or isTakeProfit
        trailingTriggerPrice = self.safe_string(params, 'trailingTriggerPrice', self.number_to_string(price))
        trailingPercent = self.safe_string_2(params, 'trailingPercent', 'callbackRatio')
        isTrailingPercentOrder = trailingPercent is not None
        if self.sum(isTriggerOrder, isStopLossTriggerOrder, isTakeProfitTriggerOrder, isTrailingPercentOrder) > 1:
            raise ExchangeError(self.id + ' createOrder() params can only contain one of triggerPrice, stopLossPrice, takeProfitPrice, trailingPercent')
        if type == 'limit':
            request['price'] = self.price_to_precision(symbol, price)
        triggerType = self.safe_string(params, 'triggerType', 'mark_price')
        reduceOnly = self.safe_bool(params, 'reduceOnly', False)
        clientOrderId = self.safe_string_2(params, 'clientOid', 'clientOrderId')
        exchangeSpecificTifParam = self.safe_string_2(params, 'force', 'timeInForce')
        postOnly = None
        postOnly, params = self.handle_post_only(isMarketOrder, exchangeSpecificTifParam == 'post_only', params)
        defaultTimeInForce = self.safe_string_upper(self.options, 'defaultTimeInForce')
        timeInForce = self.safe_string_upper(params, 'timeInForce', defaultTimeInForce)
        if postOnly:
            request['force'] = 'post_only'
        elif timeInForce == 'GTC':
            request['force'] = 'GTC'
        elif timeInForce == 'FOK':
            request['force'] = 'FOK'
        elif timeInForce == 'IOC':
            request['force'] = 'IOC'
        params = self.omit(params, ['stopPrice', 'triggerType', 'stopLossPrice', 'takeProfitPrice', 'stopLoss', 'takeProfit', 'postOnly', 'reduceOnly', 'clientOrderId', 'trailingPercent', 'trailingTriggerPrice'])
        if (marketType == 'swap') or (marketType == 'future'):
            request['marginCoin'] = market['settleId']
            request['size'] = self.amount_to_precision(symbol, amount)
            productType = None
            productType, params = self.handle_product_type_and_params(market, params)
            request['productType'] = productType
            if clientOrderId is not None:
                request['clientOid'] = clientOrderId
            if isTriggerOrder or isStopLossOrTakeProfitTrigger or isTrailingPercentOrder:
                request['triggerType'] = triggerType
            if isTrailingPercentOrder:
                if not isMarketOrder:
                    raise BadRequest(self.id + ' createOrder() bitget trailing orders must be market orders')
                if trailingTriggerPrice is None:
                    raise ArgumentsRequired(self.id + ' createOrder() bitget trailing orders must have a trailingTriggerPrice param')
                request['planType'] = 'track_plan'
                request['triggerPrice'] = self.price_to_precision(symbol, trailingTriggerPrice)
                request['callbackRatio'] = trailingPercent
            elif isTriggerOrder:
                request['planType'] = 'normal_plan'
                request['triggerPrice'] = self.price_to_precision(symbol, triggerPrice)
                if price is not None:
                    request['executePrice'] = self.price_to_precision(symbol, price)
                if isStopLoss:
                    slTriggerPrice = self.safe_number_2(stopLoss, 'triggerPrice', 'stopPrice')
                    request['stopLossTriggerPrice'] = self.price_to_precision(symbol, slTriggerPrice)
                    slPrice = self.safe_number(stopLoss, 'price')
                    request['stopLossExecutePrice'] = self.price_to_precision(symbol, slPrice)
                    slType = self.safe_string(stopLoss, 'type', 'mark_price')
                    request['stopLossTriggerType'] = slType
                if isTakeProfit:
                    tpTriggerPrice = self.safe_number_2(takeProfit, 'triggerPrice', 'stopPrice')
                    request['stopSurplusTriggerPrice'] = self.price_to_precision(symbol, tpTriggerPrice)
                    tpPrice = self.safe_number(takeProfit, 'price')
                    request['stopSurplusExecutePrice'] = self.price_to_precision(symbol, tpPrice)
                    tpType = self.safe_string(takeProfit, 'type', 'mark_price')
                    request['stopSurplusTriggerType'] = tpType
            elif isStopLossOrTakeProfitTrigger:
                if not isMarketOrder:
                    raise ExchangeError(self.id + ' createOrder() bitget stopLoss or takeProfit orders must be market orders')
                request['holdSide'] = 'long' if (side == 'buy') else 'short'
                if isStopLossTriggerOrder:
                    request['triggerPrice'] = self.price_to_precision(symbol, stopLossTriggerPrice)
                    request['planType'] = 'pos_loss'
                elif isTakeProfitTriggerOrder:
                    request['triggerPrice'] = self.price_to_precision(symbol, takeProfitTriggerPrice)
                    request['planType'] = 'pos_profit'
            else:
                if isStopLoss:
                    slTriggerPrice = self.safe_value_2(stopLoss, 'triggerPrice', 'stopPrice')
                    request['presetStopLossPrice'] = self.price_to_precision(symbol, slTriggerPrice)
                if isTakeProfit:
                    tpTriggerPrice = self.safe_value_2(takeProfit, 'triggerPrice', 'stopPrice')
                    request['presetStopSurplusPrice'] = self.price_to_precision(symbol, tpTriggerPrice)
            if not isStopLossOrTakeProfitTrigger:
                if marginMode is None:
                    marginMode = 'cross'
                marginModeRequest = 'crossed' if (marginMode == 'cross') else 'isolated'
                request['marginMode'] = marginModeRequest
                hedged = None
                hedged, params = self.handle_param_bool(params, 'hedged', False)
                # backward compatibility for `oneWayMode`
                oneWayMode = None
                oneWayMode, params = self.handle_param_bool(params, 'oneWayMode')
                if oneWayMode is not None:
                    hedged = not oneWayMode
                requestSide = side
                if reduceOnly:
                    if not hedged:
                        request['reduceOnly'] = 'YES'
                    else:
                        # on bitget hedge mode if the position is long the side is always buy, and if the position is short the side is always sell
                        requestSide = 'sell' if (side == 'buy') else 'buy'
                        request['tradeSide'] = 'Close'
                else:
                    if hedged:
                        request['tradeSide'] = 'Open'
                request['side'] = requestSide
        elif marketType == 'spot':
            if isStopLossOrTakeProfitTrigger or isStopLossOrTakeProfit:
                raise InvalidOrder(self.id + ' createOrder() does not support stop loss/take profit orders on spot markets, only swap markets')
            request['side'] = side
            quantity = None
            planType = None
            createMarketBuyOrderRequiresPrice = True
            createMarketBuyOrderRequiresPrice, params = self.handle_option_and_params(params, 'createOrder', 'createMarketBuyOrderRequiresPrice', True)
            if isMarketOrder and (side == 'buy'):
                planType = 'total'
                cost = self.safe_number(params, 'cost')
                params = self.omit(params, 'cost')
                if cost is not None:
                    quantity = self.cost_to_precision(symbol, cost)
                elif createMarketBuyOrderRequiresPrice:
                    if price is None:
                        raise InvalidOrder(self.id + ' createOrder() requires the price argument for market buy orders to calculate the total cost to spend(amount * price), alternatively set the createMarketBuyOrderRequiresPrice option or param to False and pass the cost to spend in the amount argument')
                    else:
                        amountString = self.number_to_string(amount)
                        priceString = self.number_to_string(price)
                        quoteAmount = Precise.string_mul(amountString, priceString)
                        quantity = self.cost_to_precision(symbol, quoteAmount)
                else:
                    quantity = self.cost_to_precision(symbol, amount)
            else:
                planType = 'amount'
                quantity = self.amount_to_precision(symbol, amount)
            if clientOrderId is not None:
                request['clientOid'] = clientOrderId
            if marginMode is not None:
                request['loanType'] = 'normal'
                if isMarketOrder and (side == 'buy'):
                    request['quoteSize'] = quantity
                else:
                    request['baseSize'] = quantity
            else:
                if quantity is not None:
                    request['size'] = quantity
                if triggerPrice is not None:
                    request['planType'] = planType
                    request['triggerType'] = triggerType
                    request['triggerPrice'] = self.price_to_precision(symbol, triggerPrice)
                    if price is not None:
                        request['executePrice'] = self.price_to_precision(symbol, price)
        else:
            raise NotSupported(self.id + ' createOrder() does not support ' + marketType + ' orders')
        return self.extend(request, params)

    def create_orders(self, orders: List[OrderRequest], params={}):
        """
        create a list of trade orders(all orders should be of the same symbol)
        :see: https://www.bitget.com/api-doc/spot/trade/Batch-Place-Orders
        :see: https://www.bitget.com/api-doc/contract/trade/Batch-Order
        :see: https://www.bitget.com/api-doc/margin/isolated/trade/Isolated-Batch-Order
        :see: https://www.bitget.com/api-doc/margin/cross/trade/Cross-Batch-Order
        :param Array orders: list of orders to create, each object should contain the parameters required by createOrder, namely symbol, type, side, amount, price and params
        :param dict [params]: extra parameters specific to the api endpoint
        :returns dict: an `order structure <https://docs.ccxt.com/#/?id=order-structure>`
        """
        self.load_markets()
        ordersRequests = []
        symbol = None
        marginMode = None
        for i in range(0, len(orders)):
            rawOrder = orders[i]
            marketId = self.safe_string(rawOrder, 'symbol')
            if symbol is None:
                symbol = marketId
            else:
                if symbol != marketId:
                    raise BadRequest(self.id + ' createOrders() requires all orders to have the same symbol')
            type = self.safe_string(rawOrder, 'type')
            side = self.safe_string(rawOrder, 'side')
            amount = self.safe_value(rawOrder, 'amount')
            price = self.safe_value(rawOrder, 'price')
            orderParams = self.safe_value(rawOrder, 'params', {})
            marginResult = self.handle_margin_mode_and_params('createOrders', orderParams)
            currentMarginMode = marginResult[0]
            if currentMarginMode is not None:
                if marginMode is None:
                    marginMode = currentMarginMode
                else:
                    if marginMode != currentMarginMode:
                        raise BadRequest(self.id + ' createOrders() requires all orders to have the same margin mode(isolated or cross)')
            orderRequest = self.create_order_request(marketId, type, side, amount, price, orderParams)
            ordersRequests.append(orderRequest)
        sandboxMode = self.safe_bool(self.options, 'sandboxMode', False)
        market = None
        if sandboxMode:
            sandboxSymbol = self.convert_symbol_for_sandbox(symbol)
            market = self.market(sandboxSymbol)
        else:
            market = self.market(symbol)
        request: dict = {
            'symbol': market['id'],
            'orderList': ordersRequests,
        }
        response = None
        if (market['swap']) or (market['future']):
            if marginMode is None:
                marginMode = 'cross'
            marginModeRequest = 'crossed' if (marginMode == 'cross') else 'isolated'
            request['marginMode'] = marginModeRequest
            request['marginCoin'] = market['settleId']
            productType = None
            productType, params = self.handle_product_type_and_params(market, params)
            request['productType'] = productType
            response = self.privateMixPostV2MixOrderBatchPlaceOrder(request)
        elif marginMode == 'isolated':
            response = self.privateMarginPostV2MarginIsolatedBatchPlaceOrder(request)
        elif marginMode == 'cross':
            response = self.privateMarginPostV2MarginCrossedBatchPlaceOrder(request)
        else:
            response = self.privateSpotPostV2SpotTradeBatchOrders(request)
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1700703539416,
        #         "data": {
        #             "successList": [
        #                 {
        #                     "orderId": "1111397214281175046",
        #                     "clientOid": "766d3fc3-7321-4406-a689-15c9987a2e75"
        #                 },
        #             ],
        #             "failureList": [
        #                 {
        #                     "orderId": "",
        #                     "clientOid": "d1b75cb3-cc15-4ede-ad4c-3937396f75ab",
        #                     "errorMsg": "less than the minimum amount 5 USDT",
        #                     "errorCode": "45110"
        #                 },
        #             ]
        #         }
        #     }
        #
        data = self.safe_value(response, 'data', {})
        failure = self.safe_value(data, 'failureList', [])
        orderInfo = self.safe_value(data, 'successList', [])
        both = self.array_concat(orderInfo, failure)
        return self.parse_orders(both, market)

    def edit_order(self, id: str, symbol: str, type: OrderType, side: OrderSide, amount: Num = None, price: Num = None, params={}):
        """
        edit a trade order
        :see: https://www.bitget.com/api-doc/spot/plan/Modify-Plan-Order
        :see: https://www.bitget.com/api-doc/contract/trade/Modify-Order
        :see: https://www.bitget.com/api-doc/contract/plan/Modify-Tpsl-Order
        :see: https://www.bitget.com/api-doc/contract/plan/Modify-Plan-Order
        :param str id: cancel order id
        :param str symbol: unified symbol of the market to create an order in
        :param str type: 'market' or 'limit'
        :param str side: 'buy' or 'sell'
        :param float amount: how much you want to trade in units of the base currency
        :param float [price]: the price at which the order is to be fulfilled, in units of the quote currency, ignored in market orders
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :param float [params.triggerPrice]: the price that a trigger order is triggered at
        :param float [params.stopLossPrice]: *swap only* The price at which a stop loss order is triggered at
        :param float [params.takeProfitPrice]: *swap only* The price at which a take profit order is triggered at
        :param dict [params.takeProfit]: *takeProfit object in params* containing the triggerPrice at which the attached take profit order will be triggered(perpetual swap markets only)
        :param float [params.takeProfit.triggerPrice]: *swap only* take profit trigger price
        :param dict [params.stopLoss]: *stopLoss object in params* containing the triggerPrice at which the attached stop loss order will be triggered(perpetual swap markets only)
        :param float [params.stopLoss.triggerPrice]: *swap only* stop loss trigger price
        :param float [params.stopLoss.price]: *swap only* the execution price for a stop loss attached to a trigger order
        :param float [params.takeProfit.price]: *swap only* the execution price for a take profit attached to a trigger order
        :param str [params.stopLoss.type]: *swap only* the type for a stop loss attached to a trigger order, 'fill_price', 'index_price' or 'mark_price', default is 'mark_price'
        :param str [params.takeProfit.type]: *swap only* the type for a take profit attached to a trigger order, 'fill_price', 'index_price' or 'mark_price', default is 'mark_price'
        :param str [params.trailingPercent]: *swap and future only* the percent to trail away from the current market price, rate can not be greater than 10
        :param str [params.trailingTriggerPrice]: *swap and future only* the price to trigger a trailing stop order, default uses the price argument
        :param str [params.newTriggerType]: *swap and future only* 'fill_price', 'mark_price' or 'index_price'
        :returns dict: an `order structure <https://docs.ccxt.com/#/?id=order-structure>`
        """
        self.load_markets()
        sandboxMode = self.safe_bool(self.options, 'sandboxMode', False)
        market = None
        if sandboxMode:
            sandboxSymbol = self.convert_symbol_for_sandbox(symbol)
            market = self.market(sandboxSymbol)
        else:
            market = self.market(symbol)
        request: dict = {
            'orderId': id,
        }
        isMarketOrder = type == 'market'
        triggerPrice = self.safe_value_2(params, 'stopPrice', 'triggerPrice')
        isTriggerOrder = triggerPrice is not None
        stopLossPrice = self.safe_value(params, 'stopLossPrice')
        isStopLossOrder = stopLossPrice is not None
        takeProfitPrice = self.safe_value(params, 'takeProfitPrice')
        isTakeProfitOrder = takeProfitPrice is not None
        stopLoss = self.safe_value(params, 'stopLoss')
        takeProfit = self.safe_value(params, 'takeProfit')
        isStopLoss = stopLoss is not None
        isTakeProfit = takeProfit is not None
        trailingTriggerPrice = self.safe_string(params, 'trailingTriggerPrice', self.number_to_string(price))
        trailingPercent = self.safe_string_2(params, 'trailingPercent', 'newCallbackRatio')
        isTrailingPercentOrder = trailingPercent is not None
        if self.sum(isTriggerOrder, isStopLossOrder, isTakeProfitOrder, isTrailingPercentOrder) > 1:
            raise ExchangeError(self.id + ' editOrder() params can only contain one of triggerPrice, stopLossPrice, takeProfitPrice, trailingPercent')
        clientOrderId = self.safe_string_2(params, 'clientOid', 'clientOrderId')
        if clientOrderId is not None:
            request['clientOid'] = clientOrderId
        params = self.omit(params, ['stopPrice', 'triggerType', 'stopLossPrice', 'takeProfitPrice', 'stopLoss', 'takeProfit', 'clientOrderId', 'trailingTriggerPrice', 'trailingPercent'])
        response = None
        if market['spot']:
            if triggerPrice is None:
                raise NotSupported(self.id + 'editOrder() only supports plan/trigger spot orders')
            editMarketBuyOrderRequiresPrice = self.safe_bool(self.options, 'editMarketBuyOrderRequiresPrice', True)
            if editMarketBuyOrderRequiresPrice and isMarketOrder and (side == 'buy'):
                if price is None:
                    raise InvalidOrder(self.id + ' editOrder() requires price argument for market buy orders on spot markets to calculate the total amount to spend(amount * price), alternatively set the editMarketBuyOrderRequiresPrice option to False and pass in the cost to spend into the amount parameter')
                else:
                    amountString = self.number_to_string(amount)
                    priceString = self.number_to_string(price)
                    cost = self.parse_number(Precise.string_mul(amountString, priceString))
                    request['size'] = self.price_to_precision(symbol, cost)
            else:
                request['size'] = self.amount_to_precision(symbol, amount)
            request['orderType'] = type
            request['triggerPrice'] = self.price_to_precision(symbol, triggerPrice)
            request['executePrice'] = self.price_to_precision(symbol, price)
            response = self.privateSpotPostV2SpotTradeModifyPlanOrder(self.extend(request, params))
        else:
            if (not market['swap']) and (not market['future']):
                raise NotSupported(self.id + ' editOrder() does not support ' + market['type'] + ' orders')
            request['symbol'] = market['id']
            productType = None
            productType, params = self.handle_product_type_and_params(market, params)
            request['productType'] = productType
            if not isTakeProfitOrder and not isStopLossOrder:
                request['newSize'] = self.amount_to_precision(symbol, amount)
                if (price is not None) and not isTrailingPercentOrder:
                    request['newPrice'] = self.price_to_precision(symbol, price)
            if isTrailingPercentOrder:
                if not isMarketOrder:
                    raise BadRequest(self.id + ' editOrder() bitget trailing orders must be market orders')
                if trailingTriggerPrice is not None:
                    request['newTriggerPrice'] = self.price_to_precision(symbol, trailingTriggerPrice)
                request['newCallbackRatio'] = trailingPercent
                response = self.privateMixPostV2MixOrderModifyPlanOrder(self.extend(request, params))
            elif isTakeProfitOrder or isStopLossOrder:
                request['marginCoin'] = market['settleId']
                request['size'] = self.amount_to_precision(symbol, amount)
                request['executePrice'] = self.price_to_precision(symbol, price)
                if isStopLossOrder:
                    request['triggerPrice'] = self.price_to_precision(symbol, stopLossPrice)
                elif isTakeProfitOrder:
                    request['triggerPrice'] = self.price_to_precision(symbol, takeProfitPrice)
                response = self.privateMixPostV2MixOrderModifyTpslOrder(self.extend(request, params))
            elif isTriggerOrder:
                request['newTriggerPrice'] = self.price_to_precision(symbol, triggerPrice)
                if isStopLoss:
                    slTriggerPrice = self.safe_number_2(stopLoss, 'triggerPrice', 'stopPrice')
                    request['newStopLossTriggerPrice'] = self.price_to_precision(symbol, slTriggerPrice)
                    slPrice = self.safe_number(stopLoss, 'price')
                    request['newStopLossExecutePrice'] = self.price_to_precision(symbol, slPrice)
                    slType = self.safe_string(stopLoss, 'type', 'mark_price')
                    request['newStopLossTriggerType'] = slType
                if isTakeProfit:
                    tpTriggerPrice = self.safe_number_2(takeProfit, 'triggerPrice', 'stopPrice')
                    request['newSurplusTriggerPrice'] = self.price_to_precision(symbol, tpTriggerPrice)
                    tpPrice = self.safe_number(takeProfit, 'price')
                    request['newStopSurplusExecutePrice'] = self.price_to_precision(symbol, tpPrice)
                    tpType = self.safe_string(takeProfit, 'type', 'mark_price')
                    request['newStopSurplusTriggerType'] = tpType
                response = self.privateMixPostV2MixOrderModifyPlanOrder(self.extend(request, params))
            else:
                defaultNewClientOrderId = self.uuid()
                newClientOrderId = self.safe_string_2(params, 'newClientOid', 'newClientOrderId', defaultNewClientOrderId)
                params = self.omit(params, 'newClientOrderId')
                request['newClientOid'] = newClientOrderId
                if isStopLoss:
                    slTriggerPrice = self.safe_value_2(stopLoss, 'triggerPrice', 'stopPrice')
                    request['newPresetStopLossPrice'] = self.price_to_precision(symbol, slTriggerPrice)
                if isTakeProfit:
                    tpTriggerPrice = self.safe_value_2(takeProfit, 'triggerPrice', 'stopPrice')
                    request['newPresetStopSurplusPrice'] = self.price_to_precision(symbol, tpTriggerPrice)
                response = self.privateMixPostV2MixOrderModifyOrder(self.extend(request, params))
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1700708275737,
        #         "data": {
        #             "clientOid": "abe95dbe-6081-4a6f-a2d3-ae49601cd459",
        #             "orderId": null
        #         }
        #     }
        #
        data = self.safe_dict(response, 'data', {})
        return self.parse_order(data, market)

    def cancel_order(self, id: str, symbol: Str = None, params={}):
        """
        cancels an open order
        :see: https://www.bitget.com/api-doc/spot/trade/Cancel-Order
        :see: https://www.bitget.com/api-doc/spot/plan/Cancel-Plan-Order
        :see: https://www.bitget.com/api-doc/contract/trade/Cancel-Order
        :see: https://www.bitget.com/api-doc/contract/plan/Cancel-Plan-Order
        :see: https://www.bitget.com/api-doc/margin/cross/trade/Cross-Cancel-Order
        :see: https://www.bitget.com/api-doc/margin/isolated/trade/Isolated-Cancel-Order
        :param str id: order id
        :param str symbol: unified symbol of the market the order was made in
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :param str [params.marginMode]: 'isolated' or 'cross' for spot margin trading
        :param boolean [params.stop]: set to True for canceling trigger orders
        :param str [params.planType]: *swap only* either profit_plan, loss_plan, normal_plan, pos_profit, pos_loss, moving_plan or track_plan
        :param boolean [params.trailing]: set to True if you want to cancel a trailing order
        :returns dict: An `order structure <https://docs.ccxt.com/#/?id=order-structure>`
        """
        if symbol is None:
            raise ArgumentsRequired(self.id + ' cancelOrder() requires a symbol argument')
        self.load_markets()
        sandboxMode = self.safe_bool(self.options, 'sandboxMode', False)
        market = None
        if sandboxMode:
            sandboxSymbol = self.convert_symbol_for_sandbox(symbol)
            market = self.market(sandboxSymbol)
        else:
            market = self.market(symbol)
        marginMode = None
        response = None
        marginMode, params = self.handle_margin_mode_and_params('cancelOrder', params)
        request: dict = {}
        trailing = self.safe_value(params, 'trailing')
        stop = self.safe_value_2(params, 'stop', 'trigger')
        params = self.omit(params, ['stop', 'trigger', 'trailing'])
        if not (market['spot'] and stop):
            request['symbol'] = market['id']
        if not ((market['swap'] or market['future']) and stop):
            request['orderId'] = id
        if (market['swap']) or (market['future']):
            productType = None
            productType, params = self.handle_product_type_and_params(market, params)
            request['productType'] = productType
            if stop or trailing:
                orderIdList = []
                orderId: dict = {
                    'orderId': id,
                }
                orderIdList.append(orderId)
                request['orderIdList'] = orderIdList
            if trailing:
                planType = self.safe_string(params, 'planType', 'track_plan')
                request['planType'] = planType
                response = self.privateMixPostV2MixOrderCancelPlanOrder(self.extend(request, params))
            elif stop:
                response = self.privateMixPostV2MixOrderCancelPlanOrder(self.extend(request, params))
            else:
                response = self.privateMixPostV2MixOrderCancelOrder(self.extend(request, params))
        elif market['spot']:
            if marginMode is not None:
                if marginMode == 'isolated':
                    response = self.privateMarginPostV2MarginIsolatedCancelOrder(self.extend(request, params))
                elif marginMode == 'cross':
                    response = self.privateMarginPostV2MarginCrossedCancelOrder(self.extend(request, params))
            else:
                if stop:
                    response = self.privateSpotPostV2SpotTradeCancelPlanOrder(self.extend(request, params))
                else:
                    response = self.privateSpotPostV2SpotTradeCancelOrder(self.extend(request, params))
        else:
            raise NotSupported(self.id + ' cancelOrder() does not support ' + market['type'] + ' orders')
        #
        # spot, swap, future and spot margin
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1697690413177,
        #         "data": {
        #             "orderId": "1098758604547850241",
        #             "clientOid": "1098758604585598977"
        #         }
        #     }
        #
        # swap trigger
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1700711311791,
        #         "data": {
        #             "successList": [
        #                 {
        #                     "clientOid": "1111428059067125760",
        #                     "orderId": "1111428059067125761"
        #                 }
        #             ],
        #             "failureList": []
        #         }
        #     }
        #
        # spot trigger
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1700711728063,
        #         "data": {
        #             "result": "success"
        #         }
        #     }
        #
        data = self.safe_value(response, 'data', {})
        order = None
        if (market['swap'] or market['future']) and stop:
            orderInfo = self.safe_value(data, 'successList', [])
            order = orderInfo[0]
        else:
            order = data
        return self.parse_order(order, market)

    def cancel_orders(self, ids, symbol: Str = None, params={}):
        """
        cancel multiple orders
        :see: https://www.bitget.com/api-doc/spot/trade/Batch-Cancel-Orders
        :see: https://www.bitget.com/api-doc/contract/trade/Batch-Cancel-Orders
        :see: https://www.bitget.com/api-doc/contract/plan/Cancel-Plan-Order
        :see: https://www.bitget.com/api-doc/margin/cross/trade/Cross-Batch-Cancel-Order
        :see: https://www.bitget.com/api-doc/margin/isolated/trade/Isolated-Batch-Cancel-Orders
        :param str[] ids: order ids
        :param str symbol: unified market symbol, default is None
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :param str [params.marginMode]: 'isolated' or 'cross' for spot margin trading
        :param boolean [params.stop]: *contract only* set to True for canceling trigger orders
        :returns dict: an array of `order structures <https://docs.ccxt.com/#/?id=order-structure>`
        """
        if symbol is None:
            raise ArgumentsRequired(self.id + ' cancelOrders() requires a symbol argument')
        self.load_markets()
        sandboxMode = self.safe_bool(self.options, 'sandboxMode', False)
        market = None
        if sandboxMode:
            sandboxSymbol = self.convert_symbol_for_sandbox(symbol)
            market = self.market(sandboxSymbol)
        else:
            market = self.market(symbol)
        marginMode = None
        marginMode, params = self.handle_margin_mode_and_params('cancelOrders', params)
        stop = self.safe_value_2(params, 'stop', 'trigger')
        params = self.omit(params, ['stop', 'trigger'])
        orderIdList = []
        for i in range(0, len(ids)):
            individualId = ids[i]
            orderId: dict = {
                'orderId': individualId,
            }
            orderIdList.append(orderId)
        request: dict = {
            'symbol': market['id'],
        }
        if market['spot'] and (marginMode is None):
            request['orderList'] = orderIdList
        else:
            request['orderIdList'] = orderIdList
        response = None
        if market['spot']:
            if marginMode is not None:
                if marginMode == 'cross':
                    response = self.privateMarginPostV2MarginCrossedBatchCancelOrder(self.extend(request, params))
                else:
                    response = self.privateMarginPostV2MarginIsolatedBatchCancelOrder(self.extend(request, params))
            else:
                response = self.privateSpotPostV2SpotTradeBatchCancelOrder(self.extend(request, params))
        else:
            productType = None
            productType, params = self.handle_product_type_and_params(market, params)
            request['productType'] = productType
            if stop:
                response = self.privateMixPostV2MixOrderCancelPlanOrder(self.extend(request, params))
            else:
                response = self.privateMixPostV2MixOrderBatchCancelOrders(self.extend(request, params))
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": "1680008815965",
        #         "data": {
        #             "successList": [
        #                 {
        #                     "orderId": "1024598257429823488",
        #                     "clientOid": "876493ce-c287-4bfc-9f4a-8b1905881313"
        #                 },
        #             ],
        #             "failureList": []
        #         }
        #     }
        #
        data = self.safe_value(response, 'data', {})
        orders = self.safe_list(data, 'successList', [])
        return self.parse_orders(orders, market)

    def cancel_all_orders(self, symbol: Str = None, params={}):
        """
        cancel all open orders
        :see: https://www.bitget.com/api-doc/spot/trade/Cancel-Symbol-Orders
        :see: https://www.bitget.com/api-doc/spot/plan/Batch-Cancel-Plan-Order
        :see: https://www.bitget.com/api-doc/contract/trade/Batch-Cancel-Orders
        :see: https://bitgetlimited.github.io/apidoc/en/margin/#isolated-batch-cancel-orders
        :see: https://bitgetlimited.github.io/apidoc/en/margin/#cross-batch-cancel-order
        :param str symbol: unified market symbol
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :param str [params.marginMode]: 'isolated' or 'cross' for spot margin trading
        :param boolean [params.stop]: *contract only* set to True for canceling trigger orders
        :returns dict[]: a list of `order structures <https://docs.ccxt.com/#/?id=order-structure>`
        """
        if symbol is None:
            raise ArgumentsRequired(self.id + ' cancelAllOrders() requires a symbol argument')
        self.load_markets()
        sandboxMode = self.safe_bool(self.options, 'sandboxMode', False)
        market = None
        if sandboxMode:
            sandboxSymbol = self.convert_symbol_for_sandbox(symbol)
            market = self.market(sandboxSymbol)
        else:
            market = self.market(symbol)
        marginMode = None
        marginMode, params = self.handle_margin_mode_and_params('cancelAllOrders', params)
        request: dict = {
            'symbol': market['id'],
        }
        stop = self.safe_bool_2(params, 'stop', 'trigger')
        params = self.omit(params, ['stop', 'trigger'])
        response = None
        if market['spot']:
            if marginMode is not None:
                if marginMode == 'cross':
                    response = self.privateMarginPostMarginV1CrossOrderBatchCancelOrder(self.extend(request, params))
                else:
                    response = self.privateMarginPostMarginV1IsolatedOrderBatchCancelOrder(self.extend(request, params))
                #
                #     {
                #         "code": "00000",
                #         "msg": "success",
                #         "requestTime": 1700717155622,
                #         "data": {
                #             "resultList": [
                #                 {
                #                     "orderId": "1111453253721796609",
                #                     "clientOid": "2ae7fc8a4ff949b6b60d770ca3950e2d"
                #                 },
                #             ],
                #             "failure": []
                #         }
                #     }
                #
            else:
                if stop:
                    stopRequest: dict = {
                        'symbolList': [market['id']],
                    }
                    response = self.privateSpotPostV2SpotTradeBatchCancelPlanOrder(self.extend(stopRequest, params))
                else:
                    response = self.privateSpotPostV2SpotTradeCancelSymbolOrder(self.extend(request, params))
                #
                #     {
                #         "code": "00000",
                #         "msg": "success",
                #         "requestTime": 1700716953996,
                #         "data": {
                #             "symbol": "BTCUSDT"
                #         }
                #     }
                #
                timestamp = self.safe_integer(response, 'requestTime')
                responseData = self.safe_dict(response, 'data')
                marketId = self.safe_string(responseData, 'symbol')
                return [
                    self.safe_order({
                        'info': response,
                        'symbol': self.safe_symbol(marketId, None, None, 'spot'),
                        'timestamp': timestamp,
                        'datetime': self.iso8601(timestamp),
                    }),
                ]
        else:
            productType = None
            productType, params = self.handle_product_type_and_params(market, params)
            request['productType'] = productType
            if stop:
                response = self.privateMixPostV2MixOrderCancelPlanOrder(self.extend(request, params))
            else:
                response = self.privateMixPostV2MixOrderBatchCancelOrders(self.extend(request, params))
            #     {
            #         "code": "00000",
            #         "msg": "success",
            #         "requestTime": "1680008815965",
            #         "data": {
            #             "successList": [
            #                 {
            #                     "orderId": "1024598257429823488",
            #                     "clientOid": "876493ce-c287-4bfc-9f4a-8b1905881313"
            #                 },
            #             ],
            #             "failureList": []
            #         }
            #     }
        data = self.safe_dict(response, 'data')
        resultList = self.safe_list_2(data, 'resultList', 'successList')
        failureList = self.safe_list_2(data, 'failure', 'failureList')
        responseList = self.array_concat(resultList, failureList)
        return self.parse_orders(responseList)

    def fetch_order(self, id: str, symbol: Str = None, params={}):
        """
        fetches information on an order made by the user
        :see: https://www.bitget.com/api-doc/spot/trade/Get-Order-Info
        :see: https://www.bitget.com/api-doc/contract/trade/Get-Order-Details
        :param str id: the order id
        :param str symbol: unified symbol of the market the order was made in
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict: An `order structure <https://docs.ccxt.com/#/?id=order-structure>`
        """
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchOrder() requires a symbol argument')
        self.load_markets()
        sandboxMode = self.safe_bool(self.options, 'sandboxMode', False)
        market = None
        if sandboxMode:
            sandboxSymbol = self.convert_symbol_for_sandbox(symbol)
            market = self.market(sandboxSymbol)
        else:
            market = self.market(symbol)
        request: dict = {
            'orderId': id,
        }
        response = None
        if market['spot']:
            response = self.privateSpotGetV2SpotTradeOrderInfo(self.extend(request, params))
        elif market['swap'] or market['future']:
            request['symbol'] = market['id']
            productType = None
            productType, params = self.handle_product_type_and_params(market, params)
            request['productType'] = productType
            response = self.privateMixGetV2MixOrderDetail(self.extend(request, params))
        else:
            raise NotSupported(self.id + ' fetchOrder() does not support ' + market['type'] + ' orders')
        #
        # spot
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1700719076263,
        #         "data": [
        #             {
        #                 "userId": "7264631750",
        #                 "symbol": "BTCUSDT",
        #                 "orderId": "1111461743123927040",
        #                 "clientOid": "63f95110-93b5-4309-8f77-46339f1bcf3c",
        #                 "price": "25000.0000000000000000",
        #                 "size": "0.0002000000000000",
        #                 "orderType": "limit",
        #                 "side": "buy",
        #                 "status": "live",
        #                 "priceAvg": "0",
        #                 "baseVolume": "0.0000000000000000",
        #                 "quoteVolume": "0.0000000000000000",
        #                 "enterPointSource": "API",
        #                 "feeDetail": "",
        #                 "orderSource": "normal",
        #                 "cTime": "1700719050198",
        #                 "uTime": "1700719050198"
        #             }
        #         ]
        #     }
        #
        # swap and future
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1700719918781,
        #         "data": {
        #             "symbol": "BTCUSDT",
        #             "size": "0.001",
        #             "orderId": "1111465253393825792",
        #             "clientOid": "1111465253431574529",
        #             "baseVolume": "0",
        #             "fee": "0",
        #             "price": "27000",
        #             "priceAvg": "",
        #             "state": "live",
        #             "side": "buy",
        #             "force": "gtc",
        #             "totalProfits": "0",
        #             "posSide": "long",
        #             "marginCoin": "USDT",
        #             "presetStopSurplusPrice": "",
        #             "presetStopLossPrice": "",
        #             "quoteVolume": "0",
        #             "orderType": "limit",
        #             "leverage": "20",
        #             "marginMode": "crossed",
        #             "reduceOnly": "NO",
        #             "enterPointSource": "API",
        #             "tradeSide": "open",
        #             "posMode": "hedge_mode",
        #             "orderSource": "normal",
        #             "cTime": "1700719887120",
        #             "uTime": "1700719887120"
        #         }
        #     }
        #
        if isinstance(response, str):
            response = json.loads(response)
        data = self.safe_dict(response, 'data')
        if (data is not None):
            if not isinstance(data, list):
                return self.parse_order(data, market)
        dataList = self.safe_list(response, 'data', [])
        first = self.safe_dict(dataList, 0, {})
        return self.parse_order(first, market)
        # first = self.safe_dict(data, 0, data)
        # return self.parse_order(first, market)

    def fetch_open_orders(self, symbol: Str = None, since: Int = None, limit: Int = None, params={}) -> List[Order]:
        """
        fetch all unfilled currently open orders
        :see: https://www.bitget.com/api-doc/spot/trade/Get-Unfilled-Orders
        :see: https://www.bitget.com/api-doc/spot/plan/Get-Current-Plan-Order
        :see: https://www.bitget.com/api-doc/contract/trade/Get-Orders-Pending
        :see: https://www.bitget.com/api-doc/contract/plan/get-orders-plan-pending
        :see: https://www.bitget.com/api-doc/margin/cross/trade/Get-Cross-Open-Orders
        :see: https://www.bitget.com/api-doc/margin/isolated/trade/Isolated-Open-Orders
        :param str symbol: unified market symbol
        :param int [since]: the earliest time in ms to fetch open orders for
        :param int [limit]: the maximum number of open order structures to retrieve
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :param int [params.until]: the latest time in ms to fetch orders for
        :param str [params.planType]: *contract stop only* 'normal_plan': average trigger order, 'profit_loss': opened tp/sl orders, 'track_plan': trailing stop order, default is 'normal_plan'
        :param boolean [params.stop]: set to True for fetching trigger orders
        :param boolean [params.paginate]: default False, when True will automatically paginate by calling self endpoint multiple times. See in the docs all the [available parameters](https://github.com/ccxt/ccxt/wiki/Manual#pagination-params)
        :param str [params.isPlan]: *swap only* 'plan' for stop orders and 'profit_loss' for tp/sl orders, default is 'plan'
        :param boolean [params.trailing]: set to True if you want to fetch trailing orders
        :returns Order[]: a list of `order structures <https://docs.ccxt.com/#/?id=order-structure>`
        """
        self.load_markets()
        sandboxMode = self.safe_bool(self.options, 'sandboxMode', False)
        market = None
        type = None
        request: dict = {}
        marginMode = None
        marginMode, params = self.handle_margin_mode_and_params('fetchOpenOrders', params)
        if symbol is not None:
            if sandboxMode:
                sandboxSymbol = self.convert_symbol_for_sandbox(symbol)
                market = self.market(sandboxSymbol)
            else:
                market = self.market(symbol)
            request['symbol'] = market['id']
            defaultType = self.safe_string_2(self.options, 'fetchOpenOrders', 'defaultType', 'spot')
            marketType = market['type'] if ('type' in market) else defaultType
            type = self.safe_string(params, 'type', marketType)
        else:
            defaultType = self.safe_string_2(self.options, 'fetchOpenOrders', 'defaultType', 'spot')
            type = self.safe_string(params, 'type', defaultType)
        paginate = False
        paginate, params = self.handle_option_and_params(params, 'fetchOpenOrders', 'paginate')
        if paginate:
            cursorReceived = None
            if type == 'spot':
                if marginMode is not None:
                    cursorReceived = 'minId'
            else:
                cursorReceived = 'endId'
            return self.fetch_paginated_call_cursor('fetchOpenOrders', symbol, since, limit, params, cursorReceived, 'idLessThan')
        response = None
        trailing = self.safe_bool(params, 'trailing')
        stop = self.safe_bool_2(params, 'stop', 'trigger')
        planTypeDefined = self.safe_string(params, 'planType') is not None
        isStop = (stop or planTypeDefined)
        params = self.omit(params, ['stop', 'trigger', 'trailing'])
        request, params = self.handle_until_option('endTime', request, params)
        if since is not None:
            request['startTime'] = since
        if limit is not None:
            request['limit'] = limit
        if (type == 'swap') or (type == 'future') or (marginMode is not None):
            clientOrderId = self.safe_string_2(params, 'clientOid', 'clientOrderId')
            params = self.omit(params, 'clientOrderId')
            if clientOrderId is not None:
                request['clientOid'] = clientOrderId
        query = None
        query = self.omit(params, ['type'])
        if type == 'spot':
            if marginMode is not None:
                if since is None:
                    since = self.milliseconds() - 7776000000
                    request['startTime'] = since
                if marginMode == 'isolated':
                    response = self.privateMarginGetV2MarginIsolatedOpenOrders(self.extend(request, query))
                elif marginMode == 'cross':
                    response = self.privateMarginGetV2MarginCrossedOpenOrders(self.extend(request, query))
            else:
                if stop:
                    response = self.privateSpotGetV2SpotTradeCurrentPlanOrder(self.extend(request, query))
                else:
                    response = self.privateSpotGetV2SpotTradeUnfilledOrders(self.extend(request, query))
        else:
            productType = None
            productType, query = self.handle_product_type_and_params(market, query)
            request['productType'] = productType
            if trailing:
                planType = self.safe_string(params, 'planType', 'track_plan')
                request['planType'] = planType
                response = self.privateMixGetV2MixOrderOrdersPlanPending(self.extend(request, query))
            elif isStop:
                planType = self.safe_string(query, 'planType', 'normal_plan')
                request['planType'] = planType
                response = self.privateMixGetV2MixOrderOrdersPlanPending(self.extend(request, query))
            else:
                response = self.privateMixGetV2MixOrderOrdersPending(self.extend(request, query))
        #
        # spot
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1700728123994,
        #         "data": [
        #             {
        #                 "userId": "7264631750",
        #                 "symbol": "BTCUSDT",
        #                 "orderId": "1111499608327360513",
        #                 "clientOid": "d0d4dad5-18d0-4869-a074-ec40bb47cba6",
        #                 "priceAvg": "25000.0000000000000000",
        #                 "size": "0.0002000000000000",
        #                 "orderType": "limit",
        #                 "side": "buy",
        #                 "status": "live",
        #                 "basePrice": "0",
        #                 "baseVolume": "0.0000000000000000",
        #                 "quoteVolume": "0.0000000000000000",
        #                 "enterPointSource": "WEB",
        #                 "orderSource": "normal",
        #                 "cTime": "1700728077966",
        #                 "uTime": "1700728077966"
        #             }
        #         ]
        #     }
        #
        # spot stop
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1700729361609,
        #         "data": {
        #             "nextFlag": False,
        #             "idLessThan": "1111503385931620352",
        #             "orderList": [
        #                 {
        #                     "orderId": "1111503385931620352",
        #                     "clientOid": "1111503385910648832",
        #                     "symbol": "BTCUSDT",
        #                     "size": "0.0002",
        #                     "planType": "AMOUNT",
        #                     "executePrice": "25000",
        #                     "triggerPrice": "26000",
        #                     "status": "live",
        #                     "orderType": "limit",
        #                     "side": "buy",
        #                     "triggerType": "fill_price",
        #                     "enterPointSource": "API",
        #                     "cTime": "1700728978617",
        #                     "uTime": "1700728978617"
        #                 }
        #             ]
        #         }
        #     }
        #
        # spot margin
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1700729887686,
        #         "data": {
        #             "orderList": [
        #                 {
        #                     "symbol": "BTCUSDT",
        #                     "orderType": "limit",
        #                     "enterPointSource": "WEB",
        #                     "orderId": "1111506377509580801",
        #                     "clientOid": "2043a3b59a60445f9d9f7365bf3e960c",
        #                     "loanType": "autoLoanAndRepay",
        #                     "price": "25000",
        #                     "side": "buy",
        #                     "status": "live",
        #                     "baseSize": "0.0002",
        #                     "quoteSize": "5",
        #                     "priceAvg": "0",
        #                     "size": "0",
        #                     "amount": "0",
        #                     "force": "gtc",
        #                     "cTime": "1700729691866",
        #                     "uTime": "1700729691866"
        #                 }
        #             ],
        #             "maxId": "1111506377509580801",
        #             "minId": "1111506377509580801"
        #         }
        #     }
        #
        # swap and future
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1700725609065,
        #         "data": {
        #             "entrustedList": [
        #                 {
        #                     "symbol": "BTCUSDT",
        #                     "size": "0.002",
        #                     "orderId": "1111488897767604224",
        #                     "clientOid": "1111488897805352960",
        #                     "baseVolume": "0",
        #                     "fee": "0",
        #                     "price": "25000",
        #                     "priceAvg": "",
        #                     "status": "live",
        #                     "side": "buy",
        #                     "force": "gtc",
        #                     "totalProfits": "0",
        #                     "posSide": "long",
        #                     "marginCoin": "USDT",
        #                     "quoteVolume": "0",
        #                     "leverage": "20",
        #                     "marginMode": "crossed",
        #                     "enterPointSource": "web",
        #                     "tradeSide": "open",
        #                     "posMode": "hedge_mode",
        #                     "orderType": "limit",
        #                     "orderSource": "normal",
        #                     "presetStopSurplusPrice": "",
        #                     "presetStopLossPrice": "",
        #                     "reduceOnly": "NO",
        #                     "cTime": "1700725524378",
        #                     "uTime": "1700725524378"
        #                 }
        #             ],
        #             "endId": "1111488897767604224"
        #         }
        #     }
        #
        # swap and future stop
        #
        #     {
        #         "code": "00000",\
        #         "msg": "success",
        #         "requestTime": 1700726417495,
        #         "data": {
        #             "entrustedList": [
        #                 {
        #                     "planType": "normal_plan",
        #                     "symbol": "BTCUSDT",
        #                     "size": "0.001",
        #                     "orderId": "1111491399869075457",
        #                     "clientOid": "1111491399869075456",
        #                     "price": "27000",
        #                     "callbackRatio": "",
        #                     "triggerPrice": "24000",
        #                     "triggerType": "mark_price",
        #                     "planStatus": "live",
        #                     "side": "buy",
        #                     "posSide": "long",
        #                     "marginCoin": "USDT",
        #                     "marginMode": "crossed",
        #                     "enterPointSource": "API",
        #                     "tradeSide": "open",
        #                     "posMode": "hedge_mode",
        #                     "orderType": "limit",
        #                     "stopSurplusTriggerPrice": "",
        #                     "stopSurplusExecutePrice": "",
        #                     "stopSurplusTriggerType": "fill_price",
        #                     "stopLossTriggerPrice": "",
        #                     "stopLossExecutePrice": "",
        #                     "stopLossTriggerType": "fill_price",
        #                     "cTime": "1700726120917",
        #                     "uTime": "1700726120917"
        #                 }
        #             ],
        #             "endId": "1111491399869075457"
        #         }
        #     }
        #
        data = self.safe_value(response, 'data')
        if type == 'spot':
            if (marginMode is not None) or stop:
                resultList = self.safe_list(data, 'orderList', [])
                return self.parse_orders(resultList, market, since, limit)
        else:
            result = self.safe_list(data, 'entrustedList', [])
            return self.parse_orders(result, market, since, limit)
        return self.parse_orders(data, market, since, limit)

    def fetch_closed_orders(self, symbol: Str = None, since: Int = None, limit: Int = None, params={}) -> List[Order]:
        """
        fetches information on multiple closed orders made by the user
        :see: https://www.bitget.com/api-doc/spot/trade/Get-History-Orders
        :see: https://www.bitget.com/api-doc/spot/plan/Get-History-Plan-Order
        :see: https://www.bitget.com/api-doc/contract/trade/Get-Orders-History
        :see: https://www.bitget.com/api-doc/contract/plan/orders-plan-history
        :see: https://www.bitget.com/api-doc/margin/cross/trade/Get-Cross-Order-History
        :see: https://www.bitget.com/api-doc/margin/isolated/trade/Get-Isolated-Order-History
        :param str symbol: unified market symbol of the closed orders
        :param int [since]: timestamp in ms of the earliest order
        :param int [limit]: the max number of closed orders to return
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :param int [params.until]: the latest time in ms to fetch entries for
        :param boolean [params.paginate]: default False, when True will automatically paginate by calling self endpoint multiple times. See in the docs all the [available parameters](https://github.com/ccxt/ccxt/wiki/Manual#pagination-params)
        :param str [params.isPlan]: *swap only* 'plan' for stop orders and 'profit_loss' for tp/sl orders, default is 'plan'
        :param str [params.productType]: *contract only* 'USDT-FUTURES', 'USDC-FUTURES', 'COIN-FUTURES', 'SUSDT-FUTURES', 'SUSDC-FUTURES' or 'SCOIN-FUTURES'
        :param boolean [params.trailing]: set to True if you want to fetch trailing orders
        :returns Order[]: a list of `order structures <https://docs.ccxt.com/#/?id=order-structure>`
        """
        self.load_markets()
        orders = self.fetch_canceled_and_closed_orders(symbol, since, limit, params)
        return self.filter_by(orders, 'status', 'closed')

    def fetch_canceled_orders(self, symbol: Str = None, since: Int = None, limit: Int = None, params={}):
        """
        fetches information on multiple canceled orders made by the user
        :see: https://www.bitget.com/api-doc/spot/trade/Get-History-Orders
        :see: https://www.bitget.com/api-doc/spot/plan/Get-History-Plan-Order
        :see: https://www.bitget.com/api-doc/contract/trade/Get-Orders-History
        :see: https://www.bitget.com/api-doc/contract/plan/orders-plan-history
        :see: https://www.bitget.com/api-doc/margin/cross/trade/Get-Cross-Order-History
        :see: https://www.bitget.com/api-doc/margin/isolated/trade/Get-Isolated-Order-History
        :param str symbol: unified market symbol of the canceled orders
        :param int [since]: timestamp in ms of the earliest order
        :param int [limit]: the max number of canceled orders to return
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :param int [params.until]: the latest time in ms to fetch entries for
        :param boolean [params.paginate]: default False, when True will automatically paginate by calling self endpoint multiple times. See in the docs all the [available parameters](https://github.com/ccxt/ccxt/wiki/Manual#pagination-params)
        :param str [params.isPlan]: *swap only* 'plan' for stop orders and 'profit_loss' for tp/sl orders, default is 'plan'
        :param str [params.productType]: *contract only* 'USDT-FUTURES', 'USDC-FUTURES', 'COIN-FUTURES', 'SUSDT-FUTURES', 'SUSDC-FUTURES' or 'SCOIN-FUTURES'
        :param boolean [params.trailing]: set to True if you want to fetch trailing orders
        :returns dict: a list of `order structures <https://docs.ccxt.com/#/?id=order-structure>`
        """
        self.load_markets()
        orders = self.fetch_canceled_and_closed_orders(symbol, since, limit, params)
        return self.filter_by(orders, 'status', 'canceled')

    def fetch_canceled_and_closed_orders(self, symbol: Str = None, since: Int = None, limit: Int = None, params={}):
        """
        :see: https://www.bitget.com/api-doc/spot/trade/Get-History-Orders
        :see: https://www.bitget.com/api-doc/spot/plan/Get-History-Plan-Order
        :see: https://www.bitget.com/api-doc/contract/trade/Get-Orders-History
        :see: https://www.bitget.com/api-doc/contract/plan/orders-plan-history
        :see: https://www.bitget.com/api-doc/margin/cross/trade/Get-Cross-Order-History
        :see: https://www.bitget.com/api-doc/margin/isolated/trade/Get-Isolated-Order-History
        fetches information on multiple canceled and closed orders made by the user
        :param str symbol: unified market symbol of the market orders were made in
        :param int [since]: the earliest time in ms to fetch orders for
        :param int [limit]: the maximum number of order structures to retrieve
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns Order[]: a list of `order structures <https://docs.ccxt.com/#/?id=order-structure>`
        """
        self.load_markets()
        sandboxMode = self.safe_bool(self.options, 'sandboxMode', False)
        market = None
        if sandboxMode:
            if symbol is not None:
                sandboxSymbol = self.convert_symbol_for_sandbox(symbol)
                symbol = sandboxSymbol
        request: dict = {}
        if symbol is not None:
            market = self.market(symbol)
            request['symbol'] = market['id']
        marketType = None
        marketType, params = self.handle_market_type_and_params('fetchCanceledAndClosedOrders', market, params)
        marginMode = None
        marginMode, params = self.handle_margin_mode_and_params('fetchCanceledAndClosedOrders', params)
        paginate = False
        paginate, params = self.handle_option_and_params(params, 'fetchCanceledAndClosedOrders', 'paginate')
        if paginate:
            cursorReceived = None
            if marketType == 'spot':
                if marginMode is not None:
                    cursorReceived = 'minId'
            else:
                cursorReceived = 'endId'
            return self.fetch_paginated_call_cursor('fetchCanceledAndClosedOrders', symbol, since, limit, params, cursorReceived, 'idLessThan')
        response = None
        trailing = self.safe_value(params, 'trailing')
        stop = self.safe_bool_2(params, 'stop', 'trigger')
        params = self.omit(params, ['stop', 'trigger', 'trailing'])
        request, params = self.handle_until_option('endTime', request, params)
        if since is not None:
            request['startTime'] = since
        if limit is not None:
            request['limit'] = limit
        if (marketType == 'swap') or (marketType == 'future') or (marginMode is not None):
            clientOrderId = self.safe_string_2(params, 'clientOid', 'clientOrderId')
            params = self.omit(params, 'clientOrderId')
            if clientOrderId is not None:
                request['clientOid'] = clientOrderId
        now = self.milliseconds()
        if marketType == 'spot':
            if marginMode is not None:
                if since is None:
                    since = now - 7776000000
                    request['startTime'] = since
                if marginMode == 'isolated':
                    response = self.privateMarginGetV2MarginIsolatedHistoryOrders(self.extend(request, params))
                elif marginMode == 'cross':
                    response = self.privateMarginGetV2MarginCrossedHistoryOrders(self.extend(request, params))
            else:
                if stop:
                    if symbol is None:
                        raise ArgumentsRequired(self.id + ' fetchCanceledAndClosedOrders() requires a symbol argument')
                    endTime = self.safe_integer_n(params, ['endTime', 'until'])
                    params = self.omit(params, ['until'])
                    if since is None:
                        since = now - 7776000000
                        request['startTime'] = since
                    if endTime is None:
                        request['endTime'] = now
                    response = self.privateSpotGetV2SpotTradeHistoryPlanOrder(self.extend(request, params))
                else:
                    response = self.privateSpotGetV2SpotTradeHistoryOrders(self.extend(request, params))
        else:
            productType = None
            productType, params = self.handle_product_type_and_params(market, params)
            request['productType'] = productType
            if trailing:
                planType = self.safe_string(params, 'planType', 'track_plan')
                request['planType'] = planType
                response = self.privateMixGetV2MixOrderOrdersPlanHistory(self.extend(request, params))
            elif stop:
                planType = self.safe_string(params, 'planType', 'normal_plan')
                request['planType'] = planType
                response = self.privateMixGetV2MixOrderOrdersPlanHistory(self.extend(request, params))
            else:
                response = self.privateMixGetV2MixOrderOrdersHistory(self.extend(request, params))
        #
        # spot
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1700791085380,
        #         "data": [
        #             {
        #                 "userId": "7264631750",
        #                 "symbol": "BTCUSDT",
        #                 "orderId": "1111499608327360513",
        #                 "clientOid": "d0d4dad5-18d0-4869-a074-ec40bb47cba6",
        #                 "price": "25000.0000000000000000",
        #                 "size": "0.0002000000000000",
        #                 "orderType": "limit",
        #                 "side": "buy",
        #                 "status": "cancelled",
        #                 "priceAvg": "0",
        #                 "baseVolume": "0.0000000000000000",
        #                 "quoteVolume": "0.0000000000000000",
        #                 "enterPointSource": "WEB",
        #                 "feeDetail": "",
        #                 "orderSource": "normal",
        #                 "cTime": "1700728077966",
        #                 "uTime": "1700728911471"
        #             },
        #         ]
        #     }
        #
        # spot stop
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1700792099146,
        #         "data": {
        #             "nextFlag": False,
        #             "idLessThan": "1098757597417775104",
        #             "orderList": [
        #                 {
        #                     "orderId": "1111503385931620352",
        #                     "clientOid": "1111503385910648832",
        #                     "symbol": "BTCUSDT",
        #                     "size": "0.0002",
        #                     "planType": "AMOUNT",
        #                     "executePrice": "25000",
        #                     "triggerPrice": "26000",
        #                     "status": "cancelled",
        #                     "orderType": "limit",
        #                     "side": "buy",
        #                     "triggerType": "fill_price",
        #                     "enterPointSource": "API",
        #                     "cTime": "1700728978617",
        #                     "uTime": "1700729666868"
        #                 },
        #             ]
        #         }
        #     }
        #
        # spot margin
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1700792381435,
        #         "data": {
        #             "orderList": [
        #                 {
        #                     "symbol": "BTCUSDT",
        #                     "orderType": "limit",
        #                     "enterPointSource": "WEB",
        #                     "orderId": "1111456274707001345",
        #                     "clientOid": "41e428dd305a4f668671b7f1ed00dc50",
        #                     "loanType": "autoLoanAndRepay",
        #                     "price": "27000",
        #                     "side": "buy",
        #                     "status": "cancelled",
        #                     "baseSize": "0.0002",
        #                     "quoteSize": "5.4",
        #                     "priceAvg": "0",
        #                     "size": "0",
        #                     "amount": "0",
        #                     "force": "gtc",
        #                     "cTime": "1700717746427",
        #                     "uTime": "1700717780636"
        #                 },
        #             ],
        #             "maxId": "1111456274707001345",
        #             "minId": "1098396464990269440"
        #         }
        #     }
        #
        # swap and future
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1700792674673,
        #         "data": {
        #             "entrustedList": [
        #                 {
        #                     "symbol": "BTCUSDT",
        #                     "size": "0.002",
        #                     "orderId": "1111498800817143808",
        #                     "clientOid": "1111498800850698240",
        #                     "baseVolume": "0",
        #                     "fee": "0",
        #                     "price": "25000",
        #                     "priceAvg": "",
        #                     "status": "canceled",
        #                     "side": "buy",
        #                     "force": "gtc",
        #                     "totalProfits": "0",
        #                     "posSide": "long",
        #                     "marginCoin": "USDT",
        #                     "quoteVolume": "0",
        #                     "leverage": "20",
        #                     "marginMode": "crossed",
        #                     "enterPointSource": "web",
        #                     "tradeSide": "open",
        #                     "posMode": "hedge_mode",
        #                     "orderType": "limit",
        #                     "orderSource": "normal",
        #                     "presetStopSurplusPrice": "",
        #                     "presetStopLossPrice": "",
        #                     "reduceOnly": "NO",
        #                     "cTime": "1700727885449",
        #                     "uTime": "1700727944563"
        #                 },
        #             ],
        #             "endId": "1098397008323575809"
        #         }
        #     }
        #
        # swap and future stop
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1700792938359,
        #         "data": {
        #             "entrustedList": [
        #                 {
        #                     "planType": "normal_plan",
        #                     "symbol": "BTCUSDT",
        #                     "size": "0.001",
        #                     "orderId": "1111491399869075457",
        #                     "clientOid": "1111491399869075456",
        #                     "planStatus": "cancelled",
        #                     "price": "27000",
        #                     "feeDetail": null,
        #                     "baseVolume": "0",
        #                     "callbackRatio": "",
        #                     "triggerPrice": "24000",
        #                     "triggerType": "mark_price",
        #                     "side": "buy",
        #                     "posSide": "long",
        #                     "marginCoin": "USDT",
        #                     "marginMode": "crossed",
        #                     "enterPointSource": "API",
        #                     "tradeSide": "open",
        #                     "posMode": "hedge_mode",
        #                     "orderType": "limit",
        #                     "stopSurplusTriggerPrice": "",
        #                     "stopSurplusExecutePrice": "",
        #                     "stopSurplusTriggerType": "fill_price",
        #                     "stopLossTriggerPrice": "",
        #                     "stopLossExecutePrice": "",
        #                     "stopLossTriggerType": "fill_price",
        #                     "cTime": "1700726120917",
        #                     "uTime": "1700727879652"
        #                 },
        #             ],
        #             "endId": "1098760007867502593"
        #         }
        #     }
        #
        data = self.safe_value(response, 'data', {})
        if marketType == 'spot':
            if (marginMode is not None) or stop:
                return self.parse_orders(self.safe_value(data, 'orderList', []), market, since, limit)
        else:
            return self.parse_orders(self.safe_value(data, 'entrustedList', []), market, since, limit)
        if isinstance(response, str):
            response = json.loads(response)
        orders = self.safe_list(response, 'data', [])
        return self.parse_orders(orders, market, since, limit)

    def fetch_ledger(self, code: Str = None, since: Int = None, limit: Int = None, params={}) -> List[LedgerEntry]:
        """
        fetch the history of changes, actions done by the user or operations that altered the balance of the user
        :see: https://www.bitget.com/api-doc/spot/account/Get-Account-Bills
        :see: https://www.bitget.com/api-doc/contract/account/Get-Account-Bill
        :param str [code]: unified currency code, default is None
        :param int [since]: timestamp in ms of the earliest ledger entry, default is None
        :param int [limit]: max number of ledger entries to return, default is None
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :param int [params.until]: end time in ms
        :param str [params.symbol]: *contract only* unified market symbol
        :param str [params.productType]: *contract only* 'USDT-FUTURES', 'USDC-FUTURES', 'COIN-FUTURES', 'SUSDT-FUTURES', 'SUSDC-FUTURES' or 'SCOIN-FUTURES'
        :param boolean [params.paginate]: default False, when True will automatically paginate by calling self endpoint multiple times. See in the docs all the [available parameters](https://github.com/ccxt/ccxt/wiki/Manual#pagination-params)
        :returns dict: a `ledger structure <https://docs.ccxt.com/#/?id=ledger-structure>`
        """
        self.load_markets()
        symbol = self.safe_string(params, 'symbol')
        params = self.omit(params, 'symbol')
        market = None
        if symbol is not None:
            sandboxMode = self.safe_bool(self.options, 'sandboxMode', False)
            if sandboxMode:
                sandboxSymbol = self.convert_symbol_for_sandbox(symbol)
                market = self.market(sandboxSymbol)
            else:
                market = self.market(symbol)
        marketType = None
        marketType, params = self.handle_market_type_and_params('fetchLedger', market, params)
        paginate = False
        paginate, params = self.handle_option_and_params(params, 'fetchLedger', 'paginate')
        if paginate:
            cursorReceived = None
            if marketType != 'spot':
                cursorReceived = 'endId'
            return self.fetch_paginated_call_cursor('fetchLedger', symbol, since, limit, params, cursorReceived, 'idLessThan')
        currency = None
        request: dict = {}
        if code is not None:
            currency = self.currency(code)
            request['coin'] = currency['id']
        request, params = self.handle_until_option('endTime', request, params)
        if since is not None:
            request['startTime'] = since
        if limit is not None:
            request['limit'] = limit
        response = None
        if marketType == 'spot':
            response = self.privateSpotGetV2SpotAccountBills(self.extend(request, params))
        else:
            if symbol is not None:
                request['symbol'] = market['id']
            productType = None
            productType, params = self.handle_product_type_and_params(market, params)
            request['productType'] = productType
            response = self.privateMixGetV2MixAccountBill(self.extend(request, params))
        #
        # spot
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1700795836415,
        #         "data": [
        #             {
        #                 "billId": "1111506298997215233",
        #                 "coin": "USDT",
        #                 "groupType": "transfer",
        #                 "businessType": "transfer_out",
        #                 "size": "-11.64958799",
        #                 "balance": "0.00000000",
        #                 "fees": "0.00000000",
        #                 "cTime": "1700729673028"
        #             },
        #         ]
        #     }
        #
        # swap and future
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1700795977890,
        #         "data": {
        #             "bills": [
        #                 {
        #                     "billId": "1111499428100472833",
        #                     "symbol": "",
        #                     "amount": "-11.64958799",
        #                     "fee": "0",
        #                     "feeByCoupon": "",
        #                     "businessType": "trans_to_exchange",
        #                     "coin": "USDT",
        #                     "cTime": "1700728034996"
        #                 },
        #             ],
        #             "endId": "1098396773329305606"
        #         }
        #     }
        #
        data = self.safe_value(response, 'data')
        if (marketType == 'swap') or (marketType == 'future'):
            bills = self.safe_value(data, 'bills', [])
            return self.parse_ledger(bills, currency, since, limit)
        return self.parse_ledger(data, currency, since, limit)

    def parse_ledger_entry(self, item: dict, currency: Currency = None) -> LedgerEntry:
        #
        # spot
        #
        #     {
        #         "billId": "1111506298997215233",
        #         "coin": "USDT",
        #         "groupType": "transfer",
        #         "businessType": "transfer_out",
        #         "size": "-11.64958799",
        #         "balance": "0.00000000",
        #         "fees": "0.00000000",
        #         "cTime": "1700729673028"
        #     }
        #
        # swap and future
        #
        #     {
        #         "billId": "1111499428100472833",
        #         "symbol": "",
        #         "amount": "-11.64958799",
        #         "fee": "0",
        #         "feeByCoupon": "",
        #         "businessType": "trans_to_exchange",
        #         "coin": "USDT",
        #         "cTime": "1700728034996"
        #     }
        #
        currencyId = self.safe_string(item, 'coin')
        code = self.safe_currency_code(currencyId, currency)
        currency = self.safe_currency(currencyId, currency)
        timestamp = self.safe_integer(item, 'cTime')
        after = self.safe_number(item, 'balance')
        fee = self.safe_number_2(item, 'fees', 'fee')
        amountRaw = self.safe_string_2(item, 'size', 'amount')
        amount = self.parse_number(Precise.string_abs(amountRaw))
        direction = 'in'
        if amountRaw.find('-') >= 0:
            direction = 'out'
        return self.safe_ledger_entry({
            'info': item,
            'id': self.safe_string(item, 'billId'),
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'direction': direction,
            'account': None,
            'referenceId': None,
            'referenceAccount': None,
            'type': self.parse_ledger_type(self.safe_string(item, 'businessType')),
            'currency': code,
            'amount': amount,
            'before': None,
            'after': after,
            'status': None,
            'fee': {
                'currency': code,
                'cost': fee,
            },
        }, currency)

    def parse_ledger_type(self, type):
        types: dict = {
            'trans_to_cross': 'transfer',
            'trans_from_cross': 'transfer',
            'trans_to_exchange': 'transfer',
            'trans_from_exchange': 'transfer',
            'trans_to_isolated': 'transfer',
            'trans_from_isolated': 'transfer',
            'trans_to_contract': 'transfer',
            'trans_from_contract': 'transfer',
            'trans_to_otc': 'transfer',
            'trans_from_otc': 'transfer',
            'open_long': 'trade',
            'close_long': 'trade',
            'open_short': 'trade',
            'close_short': 'trade',
            'force_close_long': 'trade',
            'force_close_short': 'trade',
            'burst_long_loss_query': 'trade',
            'burst_short_loss_query': 'trade',
            'force_buy': 'trade',
            'force_sell': 'trade',
            'burst_buy': 'trade',
            'burst_sell': 'trade',
            'delivery_long': 'settlement',
            'delivery_short': 'settlement',
            'contract_settle_fee': 'fee',
            'append_margin': 'transaction',
            'adjust_down_lever_append_margin': 'transaction',
            'reduce_margin': 'transaction',
            'auto_append_margin': 'transaction',
            'cash_gift_issue': 'cashback',
            'cash_gift_recycle': 'cashback',
            'bonus_issue': 'rebate',
            'bonus_recycle': 'rebate',
            'bonus_expired': 'rebate',
            'transfer_in': 'transfer',
            'transfer_out': 'transfer',
            'deposit': 'deposit',
            'withdraw': 'withdrawal',
            'buy': 'trade',
            'sell': 'trade',
        }
        return self.safe_string(types, type, type)

    def fetch_my_trades(self, symbol: Str = None, since: Int = None, limit: Int = None, params={}) -> List[Trade]:
        """
        fetch all trades made by the user
        :see: https://www.bitget.com/api-doc/spot/trade/Get-Fills
        :see: https://www.bitget.com/api-doc/contract/trade/Get-Order-Fills
        :see: https://www.bitget.com/api-doc/margin/cross/trade/Get-Cross-Order-Fills
        :see: https://www.bitget.com/api-doc/margin/isolated/trade/Get-Isolated-Transaction-Details
        :param str symbol: unified market symbol
        :param int [since]: the earliest time in ms to fetch trades for
        :param int [limit]: the maximum number of trades structures to retrieve
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :param int [params.until]: the latest time in ms to fetch trades for
        :param boolean [params.paginate]: default False, when True will automatically paginate by calling self endpoint multiple times. See in the docs all the [available parameters](https://github.com/ccxt/ccxt/wiki/Manual#pagination-params)
        :returns Trade[]: a list of `trade structures <https://docs.ccxt.com/#/?id=trade-structure>`
        """
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchMyTrades() requires a symbol argument')
        self.load_markets()
        sandboxMode = self.safe_bool(self.options, 'sandboxMode', False)
        market = None
        if sandboxMode:
            sandboxSymbol = self.convert_symbol_for_sandbox(symbol)
            market = self.market(sandboxSymbol)
        else:
            market = self.market(symbol)
        marginMode = None
        marginMode, params = self.handle_margin_mode_and_params('fetchMyTrades', params)
        paginate = False
        paginate, params = self.handle_option_and_params(params, 'fetchMyTrades', 'paginate')
        if paginate:
            cursorReceived = None
            if market['spot']:
                if marginMode is not None:
                    cursorReceived = 'minId'
            else:
                cursorReceived = 'endId'
            return self.fetch_paginated_call_cursor('fetchMyTrades', symbol, since, limit, params, cursorReceived, 'idLessThan')
        response = None
        request: dict = {
            'symbol': market['id'],
        }
        request, params = self.handle_until_option('endTime', request, params)
        if since is not None:
            request['startTime'] = since
        if limit is not None:
            request['limit'] = limit
        if market['spot']:
            if marginMode is not None:
                if since is None:
                    request['startTime'] = self.milliseconds() - 7776000000
                if marginMode == 'isolated':
                    response = self.privateMarginGetV2MarginIsolatedFills(self.extend(request, params))
                elif marginMode == 'cross':
                    response = self.privateMarginGetV2MarginCrossedFills(self.extend(request, params))
            else:
                response = self.privateSpotGetV2SpotTradeFills(self.extend(request, params))
        else:
            productType = None
            productType, params = self.handle_product_type_and_params(market, params)
            request['productType'] = productType
            response = self.privateMixGetV2MixOrderFills(self.extend(request, params))
        #
        # spot
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1700802995406,
        #         "data": [
        #             {
        #                 "userId": "7264631750",
        #                 "symbol": "BTCUSDT",
        #                 "orderId": "1098394344925597696",
        #                 "tradeId": "1098394344974925824",
        #                 "orderType": "market",
        #                 "side": "sell",
        #                 "priceAvg": "28467.68",
        #                 "size": "0.0002",
        #                 "amount": "5.693536",
        #                 "feeDetail": {
        #                     "deduction": "no",
        #                     "feeCoin": "USDT",
        #                     "totalDeductionFee": "",
        #                     "totalFee": "-0.005693536"
        #                 },
        #                 "tradeScope": "taker",
        #                 "cTime": "1697603539699",
        #                 "uTime": "1697603539754"
        #             }
        #         ]
        #     }
        #
        # spot margin
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1700803176399,
        #         "data": {
        #             "fills": [
        #                 {
        #                     "orderId": "1099353730455318528",
        #                     "tradeId": "1099353730627092481",
        #                     "orderType": "market",
        #                     "side": "sell",
        #                     "priceAvg": "29543.7",
        #                     "size": "0.0001",
        #                     "amount": "2.95437",
        #                     "tradeScope": "taker",
        #                     "feeDetail": {
        #                         "deduction": "no",
        #                         "feeCoin": "USDT",
        #                         "totalDeductionFee": "0",
        #                         "totalFee": "-0.00295437"
        #                     },
        #                     "cTime": "1697832275063",
        #                     "uTime": "1697832275150"
        #                 },
        #             ],
        #             "minId": "1099353591699161118",
        #             "maxId": "1099353730627092481"
        #         }
        #     }
        #
        # swap and future
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1700803357487,
        #         "data": {
        #             "fillList": [
        #                 {
        #                     "tradeId": "1111468664328269825",
        #                     "symbol": "BTCUSDT",
        #                     "orderId": "1111468664264753162",
        #                     "price": "37271.4",
        #                     "baseVolume": "0.001",
        #                     "feeDetail": [
        #                         {
        #                             "deduction": "no",
        #                             "feeCoin": "USDT",
        #                             "totalDeductionFee": null,
        #                             "totalFee": "-0.02236284"
        #                         }
        #                     ],
        #                     "side": "buy",
        #                     "quoteVolume": "37.2714",
        #                     "profit": "-0.0007",
        #                     "enterPointSource": "web",
        #                     "tradeSide": "close",
        #                     "posMode": "hedge_mode",
        #                     "tradeScope": "taker",
        #                     "cTime": "1700720700342"
        #                 },
        #             ],
        #             "endId": "1099351587643699201"
        #         }
        #     }
        #
        data = self.safe_value(response, 'data')
        if (market['swap']) or (market['future']):
            fillList = self.safe_list(data, 'fillList', [])
            return self.parse_trades(fillList, market, since, limit)
        elif marginMode is not None:
            fills = self.safe_list(data, 'fills', [])
            return self.parse_trades(fills, market, since, limit)
        return self.parse_trades(data, market, since, limit)

    def fetch_position(self, symbol: str, params={}):
        """
        fetch data on a single open contract trade position
        :see: https://www.bitget.com/api-doc/contract/position/get-single-position
        :param str symbol: unified market symbol of the market the position is held in
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict: a `position structure <https://docs.ccxt.com/#/?id=position-structure>`
        """
        self.load_markets()
        sandboxMode = self.safe_bool(self.options, 'sandboxMode', False)
        market = None
        if sandboxMode:
            sandboxSymbol = self.convert_symbol_for_sandbox(symbol)
            market = self.market(sandboxSymbol)
        else:
            market = self.market(symbol)
        productType = None
        productType, params = self.handle_product_type_and_params(market, params)
        request: dict = {
            'symbol': market['id'],
            'marginCoin': market['settleId'],
            'productType': productType,
        }
        response = self.privateMixGetV2MixPositionSinglePosition(self.extend(request, params))
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1700807531673,
        #         "data": [
        #             {
        #                 "marginCoin": "USDT",
        #                 "symbol": "BTCUSDT",
        #                 "holdSide": "long",
        #                 "openDelegateSize": "0",
        #                 "marginSize": "3.73555",
        #                 "available": "0.002",
        #                 "locked": "0",
        #                 "total": "0.002",
        #                 "leverage": "20",
        #                 "achievedProfits": "0",
        #                 "openPriceAvg": "37355.5",
        #                 "marginMode": "crossed",
        #                 "posMode": "hedge_mode",
        #                 "unrealizedPL": "0.007",
        #                 "liquidationPrice": "31724.970702417",
        #                 "keepMarginRate": "0.004",
        #                 "markPrice": "37359",
        #                 "marginRatio": "0.029599540355",
        #                 "cTime": "1700807507275"
        #             }
        #         ]
        #     }
        #
        data = self.safe_list(response, 'data', [])
        first = self.safe_dict(data, 0, {})
        return self.parse_position(first, market)

    def fetch_positions(self, symbols: Strings = None, params={}) -> List[Position]:
        """
        fetch all open positions
        :see: https://www.bitget.com/api-doc/contract/position/get-all-position
        :see: https://www.bitget.com/api-doc/contract/position/Get-History-Position
        :param str[] [symbols]: list of unified market symbols
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :param str [params.marginCoin]: the settle currency of the positions, needs to match the productType
        :param str [params.productType]: 'USDT-FUTURES', 'USDC-FUTURES', 'COIN-FUTURES', 'SUSDT-FUTURES', 'SUSDC-FUTURES' or 'SCOIN-FUTURES'
        :param boolean [params.paginate]: default False, when True will automatically paginate by calling self endpoint multiple times. See in the docs all the [available parameters](https://github.com/ccxt/ccxt/wiki/Manual#pagination-params)
        :param boolean [params.useHistoryEndpoint]: default False, when True  will use the historic endpoint to fetch positions
        :param str [params.method]: either(default) 'privateMixGetV2MixPositionAllPosition' or 'privateMixGetV2MixPositionHistoryPosition'
        :returns dict[]: a list of `position structure <https://docs.ccxt.com/#/?id=position-structure>`
        """
        self.load_markets()
        paginate = False
        paginate, params = self.handle_option_and_params(params, 'fetchPositions', 'paginate')
        if paginate:
            return self.fetch_paginated_call_cursor('fetchPositions', None, None, None, params, 'endId', 'idLessThan')
        method = None
        useHistoryEndpoint = self.safe_bool(params, 'useHistoryEndpoint', False)
        if useHistoryEndpoint:
            method = 'privateMixGetV2MixPositionHistoryPosition'
        else:
            method, params = self.handle_option_and_params(params, 'fetchPositions', 'method', 'privateMixGetV2MixPositionAllPosition')
        market = None
        if symbols is not None:
            first = self.safe_string(symbols, 0)
            sandboxMode = self.safe_bool(self.options, 'sandboxMode', False)
            if sandboxMode:
                sandboxSymbol = self.convert_symbol_for_sandbox(first)
                market = self.market(sandboxSymbol)
            else:
                market = self.market(first)
        productType = None
        productType, params = self.handle_product_type_and_params(market, params)
        request: dict = {
            'productType': productType,
        }
        response = None
        isHistory = False
        if method == 'privateMixGetV2MixPositionAllPosition':
            marginCoin = self.safe_string(params, 'marginCoin', 'USDT')
            if symbols is not None:
                marginCoin = market['settleId']
            elif productType == 'USDT-FUTURES':
                marginCoin = 'USDT'
            elif productType == 'USDC-FUTURES':
                marginCoin = 'USDC'
            elif productType == 'SUSDT-FUTURES':
                marginCoin = 'SUSDT'
            elif productType == 'SUSDC-FUTURES':
                marginCoin = 'SUSDC'
            elif (productType == 'SCOIN-FUTURES') or (productType == 'COIN-FUTURES'):
                if marginCoin is None:
                    raise ArgumentsRequired(self.id + ' fetchPositions() requires a marginCoin parameter that matches the productType')
            request['marginCoin'] = marginCoin
            response = self.privateMixGetV2MixPositionAllPosition(self.extend(request, params))
        else:
            isHistory = True
            if market is not None:
                request['symbol'] = market['id']
            response = self.privateMixGetV2MixPositionHistoryPosition(self.extend(request, params))
        #
        # privateMixGetV2MixPositionAllPosition
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1700807810221,
        #         "data": [
        #             {
        #                 "marginCoin": "USDT",
        #                 "symbol": "BTCUSDT",
        #                 "holdSide": "long",
        #                 "openDelegateSize": "0",
        #                 "marginSize": "3.73555",
        #                 "available": "0.002",
        #                 "locked": "0",
        #                 "total": "0.002",
        #                 "leverage": "20",
        #                 "achievedProfits": "0",
        #                 "openPriceAvg": "37355.5",
        #                 "marginMode": "crossed",
        #                 "posMode": "hedge_mode",
        #                 "unrealizedPL": "0.03",
        #                 "liquidationPrice": "31725.023602417",
        #                 "keepMarginRate": "0.004",
        #                 "markPrice": "37370.5",
        #                 "marginRatio": "0.029550120396",
        #                 "cTime": "1700807507275"
        #             }
        #         ]
        #     }
        #
        # privateMixGetV2MixPositionHistoryPosition
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1700808051002,
        #         "data": {
        #             "list": [
        #                 {
        #                     "symbol": "BTCUSDT",
        #                     "marginCoin": "USDT",
        #                     "holdSide": "long",
        #                     "openAvgPrice": "37272.1",
        #                     "closeAvgPrice": "37271.4",
        #                     "marginMode": "crossed",
        #                     "openTotalPos": "0.001",
        #                     "closeTotalPos": "0.001",
        #                     "pnl": "-0.0007",
        #                     "netProfit": "-0.0454261",
        #                     "totalFunding": "0",
        #                     "openFee": "-0.02236326",
        #                     "closeFee": "-0.02236284",
        #                     "utime": "1700720700400",
        #                     "ctime": "1700720651684"
        #                 },
        #             ],
        #             "endId": "1099351653866962944"
        #         }
        #     }
        #
        position = []
        if not isHistory:
            position = self.safe_list(response, 'data', [])
        else:
            data = self.safe_dict(response, 'data', {})
            position = self.safe_list(data, 'list', [])
        result = []
        for i in range(0, len(position)):
            result.append(self.parse_position(position[i], market))
        symbols = self.market_symbols(symbols)
        return self.filter_by_array_positions(result, 'symbol', symbols, False)

    def parse_position(self, position: dict, market: Market = None):
        #
        # fetchPosition
        #
        #     {
        #         "marginCoin": "USDT",
        #         "symbol": "BTCUSDT",
        #         "holdSide": "long",
        #         "openDelegateSize": "0",
        #         "marginSize": "3.73555",
        #         "available": "0.002",
        #         "locked": "0",
        #         "total": "0.002",
        #         "leverage": "20",
        #         "achievedProfits": "0",
        #         "openPriceAvg": "37355.5",
        #         "marginMode": "crossed",
        #         "posMode": "hedge_mode",
        #         "unrealizedPL": "0.007",
        #         "liquidationPrice": "31724.970702417",
        #         "keepMarginRate": "0.004",
        #         "markPrice": "37359",
        #         "marginRatio": "0.029599540355",
        #         "cTime": "1700807507275"
        #     }
        #
        # fetchPositions: privateMixGetV2MixPositionAllPosition
        #
        #     {
        #         "marginCoin": "USDT",
        #         "symbol": "BTCUSDT",
        #         "holdSide": "long",
        #         "openDelegateSize": "0",
        #         "marginSize": "3.73555",
        #         "available": "0.002",
        #         "locked": "0",
        #         "total": "0.002",
        #         "leverage": "20",
        #         "achievedProfits": "0",
        #         "openPriceAvg": "37355.5",
        #         "marginMode": "crossed",
        #         "posMode": "hedge_mode",
        #         "unrealizedPL": "0.03",
        #         "liquidationPrice": "31725.023602417",
        #         "keepMarginRate": "0.004",
        #         "markPrice": "37370.5",
        #         "marginRatio": "0.029550120396",
        #         "cTime": "1700807507275"
        #     }
        #
        # fetchPositionsHistory: privateMixGetV2MixPositionHistoryPosition
        #
        #     {
        #         "symbol": "BTCUSDT",
        #         "marginCoin": "USDT",
        #         "holdSide": "long",
        #         "openAvgPrice": "37272.1",
        #         "closeAvgPrice": "37271.4",
        #         "marginMode": "crossed",
        #         "openTotalPos": "0.001",
        #         "closeTotalPos": "0.001",
        #         "pnl": "-0.0007",
        #         "netProfit": "-0.0454261",
        #         "totalFunding": "0",
        #         "openFee": "-0.02236326",
        #         "closeFee": "-0.02236284",
        #         "utime": "1700720700400",
        #         "ctime": "1700720651684"
        #     }
        #
        # closeAllPositions
        #
        #     {
        #         "orderId": "1120923953904893955",
        #         "clientOid": "1120923953904893956"
        #     }
        #
        marketId = self.safe_string(position, 'symbol')
        market = self.safe_market(marketId, market, None, 'contract')
        symbol = market['symbol']
        timestamp = self.safe_integer_2(position, 'cTime', 'ctime')
        marginMode = self.safe_string(position, 'marginMode')
        collateral = None
        initialMargin = None
        unrealizedPnl = self.safe_string(position, 'unrealizedPL')
        rawCollateral = self.safe_string(position, 'marginSize')
        if marginMode == 'isolated':
            collateral = Precise.string_add(rawCollateral, unrealizedPnl)
        elif marginMode == 'crossed':
            marginMode = 'cross'
            initialMargin = rawCollateral
        holdMode = self.safe_string(position, 'posMode')
        hedged = None
        if holdMode == 'hedge_mode':
            hedged = True
        elif holdMode == 'one_way_mode':
            hedged = False
        side = self.safe_string(position, 'holdSide')
        leverage = self.safe_string(position, 'leverage')
        contractSizeNumber = self.safe_value(market, 'contractSize')
        contractSize = self.number_to_string(contractSizeNumber)
        baseAmount = self.safe_string(position, 'total')
        entryPrice = self.safe_string_2(position, 'openPriceAvg', 'openAvgPrice')
        maintenanceMarginPercentage = self.safe_string(position, 'keepMarginRate')
        openNotional = Precise.string_mul(entryPrice, baseAmount)
        if initialMargin is None:
            initialMargin = Precise.string_div(openNotional, leverage)
        contracts = self.parse_number(Precise.string_div(baseAmount, contractSize))
        if contracts is None:
            contracts = self.safe_number(position, 'closeTotalPos')
        markPrice = self.safe_string(position, 'markPrice')
        notional = Precise.string_mul(baseAmount, markPrice)
        initialMarginPercentage = Precise.string_div(initialMargin, notional)
        liquidationPrice = self.parse_number(self.omit_zero(self.safe_string(position, 'liquidationPrice')))
        calcTakerFeeRate = '0.0006'
        calcTakerFeeMult = '0.9994'
        if (liquidationPrice is None) and (marginMode == 'isolated') and Precise.string_gt(baseAmount, '0'):
            signedMargin = Precise.string_div(rawCollateral, baseAmount)
            signedMmp = maintenanceMarginPercentage
            if side == 'short':
                signedMargin = Precise.string_neg(signedMargin)
                signedMmp = Precise.string_neg(signedMmp)
            mmrMinusOne = Precise.string_sub('1', signedMmp)
            numerator = Precise.string_sub(entryPrice, signedMargin)
            if side == 'long':
                mmrMinusOne = Precise.string_mul(mmrMinusOne, calcTakerFeeMult)
            else:
                numerator = Precise.string_mul(numerator, calcTakerFeeMult)
            liquidationPrice = self.parse_number(Precise.string_div(numerator, mmrMinusOne))
        feeToClose = Precise.string_mul(notional, calcTakerFeeRate)
        maintenanceMargin = Precise.string_add(Precise.string_mul(maintenanceMarginPercentage, notional), feeToClose)
        percentage = Precise.string_mul(Precise.string_div(unrealizedPnl, initialMargin, 4), '100')
        return self.safe_position({
            'info': position,
            'id': self.safe_string(position, 'orderId'),
            'symbol': symbol,
            'notional': self.parse_number(notional),
            'marginMode': marginMode,
            'liquidationPrice': liquidationPrice,
            'entryPrice': self.parse_number(entryPrice),
            'unrealizedPnl': self.parse_number(unrealizedPnl),
            'realizedPnl': self.safe_number(position, 'pnl'),
            'percentage': self.parse_number(percentage),
            'contracts': contracts,
            'contractSize': contractSizeNumber,
            'markPrice': self.parse_number(markPrice),
            'lastPrice': self.safe_number(position, 'closeAvgPrice'),
            'side': side,
            'hedged': hedged,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'lastUpdateTimestamp': self.safe_integer(position, 'utime'),
            'maintenanceMargin': self.parse_number(maintenanceMargin),
            'maintenanceMarginPercentage': self.parse_number(maintenanceMarginPercentage),
            'collateral': self.parse_number(collateral),
            'initialMargin': self.parse_number(initialMargin),
            'initialMarginPercentage': self.parse_number(initialMarginPercentage),
            'leverage': self.parse_number(leverage),
            'marginRatio': self.safe_number(position, 'marginRatio'),
            'stopLossPrice': None,
            'takeProfitPrice': None,
        })

    def fetch_funding_rate_history(self, symbol: Str = None, since: Int = None, limit: Int = None, params={}):
        """
        fetches historical funding rate prices
        :see: https://www.bitget.com/api-doc/contract/market/Get-History-Funding-Rate
        :param str symbol: unified symbol of the market to fetch the funding rate history for
        :param int [since]: timestamp in ms of the earliest funding rate to fetch
        :param int [limit]: the maximum amount of funding rate structures to fetch
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :param boolean [params.paginate]: default False, when True will automatically paginate by calling self endpoint multiple times. See in the docs all the [availble parameters](https://github.com/ccxt/ccxt/wiki/Manual#pagination-params)
        :returns dict[]: a list of `funding rate structures <https://docs.ccxt.com/#/?id=funding-rate-history-structure>`
        """
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchFundingRateHistory() requires a symbol argument')
        self.load_markets()
        paginate = False
        paginate, params = self.handle_option_and_params(params, 'fetchFundingRateHistory', 'paginate')
        if paginate:
            return self.fetch_paginated_call_incremental('fetchFundingRateHistory', symbol, since, limit, params, 'pageNo', 100)
        sandboxMode = self.safe_bool(self.options, 'sandboxMode', False)
        market = None
        if sandboxMode:
            sandboxSymbol = self.convert_symbol_for_sandbox(symbol)
            market = self.market(sandboxSymbol)
        else:
            market = self.market(symbol)
        productType = None
        productType, params = self.handle_product_type_and_params(market, params)
        request: dict = {
            'symbol': market['id'],
            'productType': productType,
            # 'pageSize': limit,  # default 20
            # 'pageNo': 1,
        }
        if limit is not None:
            request['pageSize'] = limit
        response = self.publicMixGetV2MixMarketHistoryFundRate(self.extend(request, params))
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1652406728393,
        #         "data": [
        #             {
        #                 "symbol": "BTCUSDT",
        #                 "fundingRate": "-0.0003",
        #                 "fundingTime": "1652396400000"
        #             },
        #         ]
        #     }
        #
        data = self.safe_value(response, 'data', [])
        rates = []
        for i in range(0, len(data)):
            entry = data[i]
            marketId = self.safe_string(entry, 'symbol')
            symbolInner = self.safe_symbol(marketId, market)
            timestamp = self.safe_integer(entry, 'fundingTime')
            rates.append({
                'info': entry,
                'symbol': symbolInner,
                'fundingRate': self.safe_number(entry, 'fundingRate'),
                'timestamp': timestamp,
                'datetime': self.iso8601(timestamp),
            })
        sorted = self.sort_by(rates, 'timestamp')
        return self.filter_by_symbol_since_limit(sorted, market['symbol'], since, limit)

    def fetch_funding_rate(self, symbol: str, params={}):
        """
        fetch the current funding rate
        :see: https://www.bitget.com/api-doc/contract/market/Get-Current-Funding-Rate
        :param str symbol: unified market symbol
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict: a `funding rate structure <https://docs.ccxt.com/#/?id=funding-rate-structure>`
        """
        self.load_markets()
        sandboxMode = self.safe_bool(self.options, 'sandboxMode', False)
        market = None
        if sandboxMode:
            sandboxSymbol = self.convert_symbol_for_sandbox(symbol)
            market = self.market(sandboxSymbol)
        else:
            market = self.market(symbol)
        if not market['swap']:
            raise BadSymbol(self.id + ' fetchFundingRate() supports swap contracts only')
        productType = None
        productType, params = self.handle_product_type_and_params(market, params)
        request: dict = {
            'symbol': market['id'],
            'productType': productType,
        }
        response = self.publicMixGetV2MixMarketCurrentFundRate(self.extend(request, params))
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1700811542124,
        #         "data": [
        #             {
        #                 "symbol": "BTCUSDT",
        #                 "fundingRate": "0.000106"
        #             }
        #         ]
        #     }
        #
        data = self.safe_value(response, 'data', [])
        return self.parse_funding_rate(data[0], market)

    def parse_funding_rate(self, contract, market: Market = None):
        #
        #     {
        #         "symbol": "BTCUSDT",
        #         "fundingRate": "-0.000182"
        #     }
        #
        marketId = self.safe_string(contract, 'symbol')
        symbol = self.safe_symbol(marketId, market, None, 'swap')
        return {
            'info': contract,
            'symbol': symbol,
            'markPrice': None,
            'indexPrice': None,
            'interestRate': None,
            'estimatedSettlePrice': None,
            'timestamp': None,
            'datetime': None,
            'fundingRate': self.safe_number(contract, 'fundingRate'),
            'fundingTimestamp': None,
            'fundingDatetime': None,
            'nextFundingRate': None,
            'nextFundingTimestamp': None,
            'nextFundingDatetime': None,
            'previousFundingRate': None,
            'previousFundingTimestamp': None,
            'previousFundingDatetime': None,
        }

    def fetch_funding_history(self, symbol: Str = None, since: Int = None, limit: Int = None, params={}) -> List[FundingHistory]:
        """
        fetch the funding history
        :see: https://www.bitget.com/api-doc/contract/account/Get-Account-Bill
        :param str symbol: unified market symbol
        :param int [since]: the starting timestamp in milliseconds
        :param int [limit]: the number of entries to return
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :param int [params.until]: the latest time in ms to fetch funding history for
        :param boolean [params.paginate]: default False, when True will automatically paginate by calling self endpoint multiple times. See in the docs all the [available parameters](https://github.com/ccxt/ccxt/wiki/Manual#pagination-params)
        :returns dict[]: a list of `funding history structures <https://docs.ccxt.com/#/?id=funding-history-structure>`
        """
        self.load_markets()
        if symbol is None:
            raise ArgumentsRequired(self.id + ' fetchFundingHistory() requires a symbol argument')
        paginate = False
        paginate, params = self.handle_option_and_params(params, 'fetchFundingHistory', 'paginate')
        if paginate:
            return self.fetch_paginated_call_cursor('fetchFundingHistory', symbol, since, limit, params, 'endId', 'idLessThan')
        sandboxMode = self.safe_bool(self.options, 'sandboxMode', False)
        market = None
        if sandboxMode:
            sandboxSymbol = self.convert_symbol_for_sandbox(symbol)
            market = self.market(sandboxSymbol)
        else:
            market = self.market(symbol)
        if not market['swap']:
            raise BadSymbol(self.id + ' fetchFundingHistory() supports swap contracts only')
        productType = None
        productType, params = self.handle_product_type_and_params(market, params)
        request: dict = {
            'symbol': market['id'],
            'marginCoin': market['settleId'],
            'businessType': 'contract_settle_fee',
            'productType': productType,
        }
        request, params = self.handle_until_option('endTime', request, params)
        if since is not None:
            request['startTime'] = since
        if limit is not None:
            request['limit'] = limit
        response = self.privateMixGetV2MixAccountBill(self.extend(request, params))
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1700795977890,
        #         "data": {
        #             "bills": [
        #                 {
        #                     "billId": "1111499428100472833",
        #                     "symbol": "BTCUSDT",
        #                     "amount": "-0.004992",
        #                     "fee": "0",
        #                     "feeByCoupon": "",
        #                     "businessType": "contract_settle_fee",
        #                     "coin": "USDT",
        #                     "cTime": "1700728034996"
        #                 },
        #             ],
        #             "endId": "1098396773329305606"
        #         }
        #     }
        #
        data = self.safe_value(response, 'data', {})
        result = self.safe_value(data, 'bills', [])
        return self.parse_funding_histories(result, market, since, limit)

    def parse_funding_history(self, contract, market: Market = None):
        #
        #     {
        #         "billId": "1111499428100472833",
        #         "symbol": "BTCUSDT",
        #         "amount": "-0.004992",
        #         "fee": "0",
        #         "feeByCoupon": "",
        #         "businessType": "contract_settle_fee",
        #         "coin": "USDT",
        #         "cTime": "1700728034996"
        #     }
        #
        marketId = self.safe_string(contract, 'symbol')
        currencyId = self.safe_string(contract, 'coin')
        timestamp = self.safe_integer(contract, 'cTime')
        return {
            'info': contract,
            'symbol': self.safe_symbol(marketId, market, None, 'swap'),
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'code': self.safe_currency_code(currencyId),
            'amount': self.safe_number(contract, 'amount'),
            'id': self.safe_string(contract, 'billId'),
        }

    def parse_funding_histories(self, contracts, market=None, since: Int = None, limit: Int = None) -> List[FundingHistory]:
        result = []
        for i in range(0, len(contracts)):
            contract = contracts[i]
            business = self.safe_string(contract, 'businessType')
            if business != 'contract_settle_fee':
                continue
            result.append(self.parse_funding_history(contract, market))
        sorted = self.sort_by(result, 'timestamp')
        return self.filter_by_since_limit(sorted, since, limit)

    def modify_margin_helper(self, symbol: str, amount, type, params={}) -> MarginModification:
        self.load_markets()
        holdSide = self.safe_string(params, 'holdSide')
        sandboxMode = self.safe_bool(self.options, 'sandboxMode', False)
        market = None
        if sandboxMode:
            sandboxSymbol = self.convert_symbol_for_sandbox(symbol)
            market = self.market(sandboxSymbol)
        else:
            market = self.market(symbol)
        productType = None
        productType, params = self.handle_product_type_and_params(market, params)
        request: dict = {
            'symbol': market['id'],
            'marginCoin': market['settleId'],
            'amount': self.amount_to_precision(symbol, amount),  # positive value for adding margin, negative for reducing
            'holdSide': holdSide,  # long or short
            'productType': productType,
        }
        params = self.omit(params, 'holdSide')
        response = self.privateMixPostV2MixAccountSetMargin(self.extend(request, params))
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1700813444618,
        #         "data": ""
        #     }
        #
        return self.extend(self.parse_margin_modification(response, market), {
            'amount': self.parse_number(amount),
            'type': type,
        })

    def parse_margin_modification(self, data: dict, market: Market = None) -> MarginModification:
        #
        # addMargin/reduceMargin
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1700813444618,
        #         "data": ""
        #     }
        #
        errorCode = self.safe_string(data, 'code')
        status = 'ok' if (errorCode == '00000') else 'failed'
        return {
            'info': data,
            'symbol': market['symbol'],
            'type': None,
            'marginMode': 'isolated',
            'amount': None,
            'total': None,
            'code': market['settle'],
            'status': status,
            'timestamp': None,
            'datetime': None,
        }

    def reduce_margin(self, symbol: str, amount: float, params={}) -> MarginModification:
        """
        remove margin from a position
        :see: https://www.bitget.com/api-doc/contract/account/Change-Margin
        :param str symbol: unified market symbol
        :param float amount: the amount of margin to remove
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict: a `margin structure <https://docs.ccxt.com/#/?id=reduce-margin-structure>`
        """
        if amount > 0:
            raise BadRequest(self.id + ' reduceMargin() amount parameter must be a negative value')
        holdSide = self.safe_string(params, 'holdSide')
        if holdSide is None:
            raise ArgumentsRequired(self.id + ' reduceMargin() requires a holdSide parameter, either long or short')
        return self.modify_margin_helper(symbol, amount, 'reduce', params)

    def add_margin(self, symbol: str, amount: float, params={}) -> MarginModification:
        """
        add margin
        :see: https://www.bitget.com/api-doc/contract/account/Change-Margin
        :param str symbol: unified market symbol
        :param float amount: the amount of margin to add
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict: a `margin structure <https://docs.ccxt.com/#/?id=add-margin-structure>`
        """
        holdSide = self.safe_string(params, 'holdSide')
        if holdSide is None:
            raise ArgumentsRequired(self.id + ' addMargin() requires a holdSide parameter, either long or short')
        return self.modify_margin_helper(symbol, amount, 'add', params)

    def fetch_leverage(self, symbol: str, params={}) -> Leverage:
        """
        fetch the set leverage for a market
        :see: https://www.bitget.com/api-doc/contract/account/Get-Single-Account
        :param str symbol: unified market symbol
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict: a `leverage structure <https://docs.ccxt.com/#/?id=leverage-structure>`
        """
        self.load_markets()
        sandboxMode = self.safe_bool(self.options, 'sandboxMode', False)
        market = None
        if sandboxMode:
            sandboxSymbol = self.convert_symbol_for_sandbox(symbol)
            market = self.market(sandboxSymbol)
        else:
            market = self.market(symbol)
        productType = None
        productType, params = self.handle_product_type_and_params(market, params)
        request: dict = {
            'symbol': market['id'],
            'marginCoin': market['settleId'],
            'productType': productType,
        }
        response = self.privateMixGetV2MixAccountAccount(self.extend(request, params))
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1709366911964,
        #         "data": {
        #             "marginCoin": "USDT",
        #             "locked": "0",
        #             "available": "0",
        #             "crossedMaxAvailable": "0",
        #             "isolatedMaxAvailable": "0",
        #             "maxTransferOut": "0",
        #             "accountEquity": "0",
        #             "usdtEquity": "0.000000009166",
        #             "btcEquity": "0",
        #             "crossedRiskRate": "0",
        #             "crossedMarginLeverage": 20,
        #             "isolatedLongLever": 20,
        #             "isolatedShortLever": 20,
        #             "marginMode": "crossed",
        #             "posMode": "hedge_mode",
        #             "unrealizedPL": "0",
        #             "coupon": "0",
        #             "crossedUnrealizedPL": "0",
        #             "isolatedUnrealizedPL": ""
        #         }
        #     }
        #
        data = self.safe_dict(response, 'data', {})
        return self.parse_leverage(data, market)

    def parse_leverage(self, leverage: dict, market: Market = None) -> Leverage:
        return {
            'info': leverage,
            'symbol': market['symbol'],
            'marginMode': 'isolated',
            'longLeverage': self.safe_integer(leverage, 'isolatedLongLever'),
            'shortLeverage': self.safe_integer(leverage, 'isolatedShortLever'),
        }

    def set_leverage(self, leverage: Int, symbol: Str = None, params={}):
        """
        set the level of leverage for a market
        :see: https://www.bitget.com/api-doc/contract/account/Change-Leverage
        :param int leverage: the rate of leverage
        :param str symbol: unified market symbol
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :param str [params.holdSide]: *isolated only* position direction, 'long' or 'short'
        :returns dict: response from the exchange
        """
        if symbol is None:
            raise ArgumentsRequired(self.id + ' setLeverage() requires a symbol argument')
        self.load_markets()
        sandboxMode = self.safe_bool(self.options, 'sandboxMode', False)
        market = None
        if sandboxMode:
            sandboxSymbol = self.convert_symbol_for_sandbox(symbol)
            market = self.market(sandboxSymbol)
        else:
            market = self.market(symbol)
        productType = None
        productType, params = self.handle_product_type_and_params(market, params)
        request: dict = {
            'symbol': market['id'],
            'marginCoin': market['settleId'],
            'leverage': self.number_to_string(leverage),
            'productType': productType,
            # 'holdSide': 'long',
        }
        response = self.privateMixPostV2MixAccountSetLeverage(self.extend(request, params))
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1700864711517,
        #         "data": {
        #             "symbol": "BTCUSDT",
        #             "marginCoin": "USDT",
        #             "longLeverage": "25",
        #             "shortLeverage": "25",
        #             "crossMarginLeverage": "25",
        #             "marginMode": "crossed"
        #         }
        #     }
        #
        return response

    def set_margin_mode(self, marginMode: str, symbol: Str = None, params={}):
        """
        set margin mode to 'cross' or 'isolated'
        :see: https://www.bitget.com/api-doc/contract/account/Change-Margin-Mode
        :param str marginMode: 'cross' or 'isolated'
        :param str symbol: unified market symbol
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict: response from the exchange
        """
        if symbol is None:
            raise ArgumentsRequired(self.id + ' setMarginMode() requires a symbol argument')
        marginMode = marginMode.lower()
        if marginMode == 'cross':
            marginMode = 'crossed'
        if (marginMode != 'isolated') and (marginMode != 'crossed'):
            raise ArgumentsRequired(self.id + ' setMarginMode() marginMode must be either isolated or crossed(cross)')
        self.load_markets()
        sandboxMode = self.safe_bool(self.options, 'sandboxMode', False)
        market = None
        if sandboxMode:
            sandboxSymbol = self.convert_symbol_for_sandbox(symbol)
            market = self.market(sandboxSymbol)
        else:
            market = self.market(symbol)
        productType = None
        productType, params = self.handle_product_type_and_params(market, params)
        request: dict = {
            'symbol': market['id'],
            'marginCoin': market['settleId'],
            'marginMode': marginMode,
            'productType': productType,
        }
        response = self.privateMixPostV2MixAccountSetMarginMode(self.extend(request, params))
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1700865205552,
        #         "data": {
        #             "symbol": "BTCUSDT",
        #             "marginCoin": "USDT",
        #             "longLeverage": "20",
        #             "shortLeverage": "3",
        #             "marginMode": "isolated"
        #         }
        #     }
        #
        return response

    def set_position_mode(self, hedged: bool, symbol: Str = None, params={}):
        """
        set hedged to True or False for a market
        :see: https://www.bitget.com/api-doc/contract/account/Change-Hold-Mode
        :param bool hedged: set to True to use dualSidePosition
        :param str symbol: not used by bitget setPositionMode()
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :param str [params.productType]: required if symbol is None: 'USDT-FUTURES', 'USDC-FUTURES', 'COIN-FUTURES', 'SUSDT-FUTURES', 'SUSDC-FUTURES' or 'SCOIN-FUTURES'
        :returns dict: response from the exchange
        """
        self.load_markets()
        posMode = 'hedge_mode' if hedged else 'one_way_mode'
        market = None
        if symbol is not None:
            sandboxMode = self.safe_bool(self.options, 'sandboxMode', False)
            if sandboxMode:
                sandboxSymbol = self.convert_symbol_for_sandbox(symbol)
                market = self.market(sandboxSymbol)
            else:
                market = self.market(symbol)
        productType = None
        productType, params = self.handle_product_type_and_params(market, params)
        request: dict = {
            'posMode': posMode,
            'productType': productType,
        }
        response = self.privateMixPostV2MixAccountSetPositionMode(self.extend(request, params))
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1700865608009,
        #         "data": {
        #             "posMode": "hedge_mode"
        #         }
        #     }
        #
        return response

    def fetch_open_interest(self, symbol: str, params={}):
        """
        retrieves the open interest of a contract trading pair
        :see: https://www.bitget.com/api-doc/contract/market/Get-Open-Interest
        :param str symbol: unified CCXT market symbol
        :param dict [params]: exchange specific parameters
        :returns dict} an open interest structure{@link https://docs.ccxt.com/#/?id=open-interest-structure:
        """
        self.load_markets()
        sandboxMode = self.safe_bool(self.options, 'sandboxMode', False)
        market = None
        if sandboxMode:
            sandboxSymbol = self.convert_symbol_for_sandbox(symbol)
            market = self.market(sandboxSymbol)
        else:
            market = self.market(symbol)
        if not market['contract']:
            raise BadRequest(self.id + ' fetchOpenInterest() supports contract markets only')
        productType = None
        productType, params = self.handle_product_type_and_params(market, params)
        request: dict = {
            'symbol': market['id'],
            'productType': productType,
        }
        response = self.publicMixGetV2MixMarketOpenInterest(self.extend(request, params))
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1700866041022,
        #         "data": {
        #             "openInterestList": [
        #                 {
        #                     "symbol": "BTCUSDT",
        #                     "size": "52234.134"
        #                 }
        #             ],
        #             "ts": "1700866041023"
        #         }
        #     }
        #
        data = self.safe_dict(response, 'data', {})
        return self.parse_open_interest(data, market)

    def parse_open_interest(self, interest, market: Market = None):
        #
        #     {
        #         "openInterestList": [
        #             {
        #                 "symbol": "BTCUSDT",
        #                 "size": "52234.134"
        #             }
        #         ],
        #         "ts": "1700866041023"
        #     }
        #
        data = self.safe_value(interest, 'openInterestList', [])
        timestamp = self.safe_integer(interest, 'ts')
        marketId = self.safe_string(data[0], 'symbol')
        return self.safe_open_interest({
            'symbol': self.safe_symbol(marketId, market, None, 'contract'),
            'openInterestAmount': self.safe_number(data[0], 'size'),
            'openInterestValue': None,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'info': interest,
        }, market)

    def fetch_transfers(self, code: Str = None, since: Int = None, limit: Int = None, params={}) -> List[TransferEntry]:
        """
        fetch a history of internal transfers made on an account
        :see: https://www.bitget.com/api-doc/spot/account/Get-Account-TransferRecords
        :param str code: unified currency code of the currency transferred
        :param int [since]: the earliest time in ms to fetch transfers for
        :param int [limit]: the maximum number of transfers structures to retrieve
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :param int [params.until]: the latest time in ms to fetch entries for
        :returns dict[]: a list of `transfer structures <https://docs.ccxt.com/#/?id=transfer-structure>`
        """
        if code is None:
            raise ArgumentsRequired(self.id + ' fetchTransfers() requires a code argument')
        self.load_markets()
        type = None
        type, params = self.handle_market_type_and_params('fetchTransfers', None, params)
        fromAccount = self.safe_string(params, 'fromAccount', type)
        params = self.omit(params, 'fromAccount')
        accountsByType = self.safe_value(self.options, 'accountsByType', {})
        type = self.safe_string(accountsByType, fromAccount)
        currency = self.currency(code)
        request: dict = {
            'coin': currency['id'],
            'fromType': type,
        }
        if since is not None:
            request['startTime'] = since
        if limit is not None:
            request['limit'] = limit
        request, params = self.handle_until_option('endTime', request, params)
        response = self.privateSpotGetV2SpotAccountTransferRecords(self.extend(request, params))
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1700873854651,
        #         "data": [
        #             {
        #                 "coin": "USDT",
        #                 "status": "Successful",
        #                 "toType": "crossed_margin",
        #                 "toSymbol": "",
        #                 "fromType": "spot",
        #                 "fromSymbol": "",
        #                 "size": "11.64958799",
        #                 "ts": "1700729673028",
        #                 "clientOid": "1111506298504744960",
        #                 "transferId": "24930940"
        #             },
        #         ]
        #     }
        #
        data = self.safe_list(response, 'data', [])
        return self.parse_transfers(data, currency, since, limit)

    def transfer(self, code: str, amount: float, fromAccount: str, toAccount: str, params={}) -> TransferEntry:
        """
        transfer currency internally between wallets on the same account
        :see: https://www.bitget.com/api-doc/spot/account/Wallet-Transfer
        :param str code: unified currency code
        :param float amount: amount to transfer
        :param str fromAccount: account to transfer from
        :param str toAccount: account to transfer to
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :param str [params.symbol]: unified CCXT market symbol, required when transferring to or from an account type that is a leveraged position-by-position account
        :param str [params.clientOid]: custom id
        :returns dict: a `transfer structure <https://docs.ccxt.com/#/?id=transfer-structure>`
        """
        self.load_markets()
        currency = self.currency(code)
        accountsByType = self.safe_value(self.options, 'accountsByType', {})
        fromType = self.safe_string(accountsByType, fromAccount)
        toType = self.safe_string(accountsByType, toAccount)
        request: dict = {
            'fromType': fromType,
            'toType': toType,
            'amount': amount,
            'coin': currency['id'],
        }
        symbol = self.safe_string(params, 'symbol')
        params = self.omit(params, 'symbol')
        market = None
        if symbol is not None:
            market = self.market(symbol)
            request['symbol'] = market['id']
        response = self.privateSpotPostV2SpotWalletTransfer(self.extend(request, params))
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1700874302021,
        #         "data": {
        #             "transferId": "1112112916581847040",
        #             "clientOrderId": null
        #         }
        #     }
        #
        data = self.safe_value(response, 'data', {})
        data['ts'] = self.safe_integer(response, 'requestTime')
        return self.parse_transfer(data, currency)

    def parse_transfer(self, transfer: dict, currency: Currency = None) -> TransferEntry:
        #
        # transfer
        #
        #     {
        #         "transferId": "1112112916581847040",
        #         "clientOrderId": null,
        #         "ts": 1700874302021
        #     }
        #
        # fetchTransfers
        #
        #     {
        #         "coin": "USDT",
        #         "status": "Successful",
        #         "toType": "crossed_margin",
        #         "toSymbol": "",
        #         "fromType": "spot",
        #         "fromSymbol": "",
        #         "size": "11.64958799",
        #         "ts": "1700729673028",
        #         "clientOid": "1111506298504744960",
        #         "transferId": "24930940"
        #     }
        #
        timestamp = self.safe_integer(transfer, 'ts')
        status = self.safe_string_lower(transfer, 'status')
        currencyId = self.safe_string(transfer, 'coin')
        fromAccountRaw = self.safe_string(transfer, 'fromType')
        accountsById = self.safe_value(self.options, 'accountsById', {})
        fromAccount = self.safe_string(accountsById, fromAccountRaw, fromAccountRaw)
        toAccountRaw = self.safe_string(transfer, 'toType')
        toAccount = self.safe_string(accountsById, toAccountRaw, toAccountRaw)
        return {
            'info': transfer,
            'id': self.safe_string(transfer, 'transferId'),
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'currency': self.safe_currency_code(currencyId, currency),
            'amount': self.safe_number(transfer, 'size'),
            'fromAccount': fromAccount,
            'toAccount': toAccount,
            'status': self.parse_transfer_status(status),
        }

    def parse_transfer_status(self, status: Str) -> Str:
        statuses: dict = {
            'successful': 'ok',
        }
        return self.safe_string(statuses, status, status)

    def parse_deposit_withdraw_fee(self, fee, currency: Currency = None):
        #
        #     {
        #         "chains": [
        #             {
        #                 "browserUrl": "https://blockchair.com/bitcoin/transaction/",
        #                 "chain": "BTC",
        #                 "depositConfirm": "1",
        #                 "extraWithdrawFee": "0",
        #                 "minDepositAmount": "0.0001",
        #                 "minWithdrawAmount": "0.005",
        #                 "needTag": "false",
        #                 "rechargeable": "true",
        #                 "withdrawConfirm": "1",
        #                 "withdrawFee": "0.0004",
        #                 "withdrawable": "true"
        #             },
        #         ],
        #         "coin": "BTC",
        #         "coinId": "1",
        #         "transfer": "true""
        #     }
        #
        chains = self.safe_value(fee, 'chains', [])
        chainsLength = len(chains)
        result: dict = {
            'info': fee,
            'withdraw': {
                'fee': None,
                'percentage': None,
            },
            'deposit': {
                'fee': None,
                'percentage': None,
            },
            'networks': {},
        }
        for i in range(0, chainsLength):
            chain = chains[i]
            networkId = self.safe_string(chain, 'chain')
            currencyCode = self.safe_string(currency, 'code')
            networkCode = self.network_id_to_code(networkId, currencyCode)
            result['networks'][networkCode] = {
                'deposit': {'fee': None, 'percentage': None},
                'withdraw': {'fee': self.safe_number(chain, 'withdrawFee'), 'percentage': False},
            }
            if chainsLength == 1:
                result['withdraw']['fee'] = self.safe_number(chain, 'withdrawFee')
                result['withdraw']['percentage'] = False
        return result

    def fetch_deposit_withdraw_fees(self, codes: Strings = None, params={}):
        """
        fetch deposit and withdraw fees
        :see: https://www.bitget.com/api-doc/spot/market/Get-Coin-List
        :param str[]|None codes: list of unified currency codes
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict: a list of `fee structures <https://docs.ccxt.com/#/?id=fee-structure>`
        """
        self.load_markets()
        response = self.publicSpotGetV2SpotPublicCoins(params)
        #
        #     {
        #         "code": "00000",
        #         "data": [
        #             {
        #                 "chains": [
        #                     {
        #                         "browserUrl": "https://blockchair.com/bitcoin/transaction/",
        #                         "chain": "BTC",
        #                         "depositConfirm": "1",
        #                         "extraWithdrawFee": "0",
        #                         "minDepositAmount": "0.0001",
        #                         "minWithdrawAmount": "0.005",
        #                         "needTag": "false",
        #                         "rechargeable": "true",
        #                         "withdrawConfirm": "1",
        #                         "withdrawFee": "0.0004",
        #                         "withdrawable": "true"
        #                     },
        #                 ],
        #                 "coin": "BTC",
        #                 "coinId": "1",
        #                 "transfer": "true""
        #             }
        #         ],
        #         "msg": "success",
        #         "requestTime": "1700120731773"
        #     }
        #
        data = self.safe_list(response, 'data', [])
        return self.parse_deposit_withdraw_fees(data, codes, 'coin')

    def borrow_cross_margin(self, code: str, amount: float, params={}):
        """
        create a loan to borrow margin
        :see: https://www.bitget.com/api-doc/margin/cross/account/Cross-Borrow
        :param str code: unified currency code of the currency to borrow
        :param str amount: the amount to borrow
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict: a `margin loan structure <https://docs.ccxt.com/#/?id=margin-loan-structure>`
        """
        self.load_markets()
        currency = self.currency(code)
        request: dict = {
            'coin': currency['id'],
            'borrowAmount': self.currency_to_precision(code, amount),
        }
        response = self.privateMarginPostV2MarginCrossedAccountBorrow(self.extend(request, params))
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1700876470931,
        #         "data": {
        #             "loanId": "1112122013642272769",
        #             "coin": "USDT",
        #             "borrowAmount": "4"
        #         }
        #     }
        #
        data = self.safe_value(response, 'data', {})
        return self.parse_margin_loan(data, currency)

    def borrow_isolated_margin(self, symbol: str, code: str, amount: float, params={}):
        """
        create a loan to borrow margin
        :see: https://www.bitget.com/api-doc/margin/isolated/account/Isolated-Borrow
        :param str symbol: unified market symbol
        :param str code: unified currency code of the currency to borrow
        :param str amount: the amount to borrow
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict: a `margin loan structure <https://docs.ccxt.com/#/?id=margin-loan-structure>`
        """
        self.load_markets()
        currency = self.currency(code)
        market = self.market(symbol)
        request: dict = {
            'coin': currency['id'],
            'borrowAmount': self.currency_to_precision(code, amount),
            'symbol': market['id'],
        }
        response = self.privateMarginPostV2MarginIsolatedAccountBorrow(self.extend(request, params))
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1700877255605,
        #         "data": {
        #             "loanId": "1112125304879067137",
        #             "symbol": "BTCUSDT",
        #             "coin": "USDT",
        #             "borrowAmount": "4"
        #         }
        #     }
        #
        data = self.safe_value(response, 'data', {})
        return self.parse_margin_loan(data, currency, market)

    def repay_isolated_margin(self, symbol: str, code: str, amount, params={}):
        """
        repay borrowed margin and interest
        :see: https://www.bitget.com/api-doc/margin/isolated/account/Isolated-Repay
        :param str symbol: unified market symbol
        :param str code: unified currency code of the currency to repay
        :param str amount: the amount to repay
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict: a `margin loan structure <https://docs.ccxt.com/#/?id=margin-loan-structure>`
        """
        self.load_markets()
        currency = self.currency(code)
        market = self.market(symbol)
        request: dict = {
            'coin': currency['id'],
            'repayAmount': self.currency_to_precision(code, amount),
            'symbol': market['id'],
        }
        response = self.privateMarginPostV2MarginIsolatedAccountRepay(self.extend(request, params))
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1700877518012,
        #         "data": {
        #             "remainDebtAmount": "0",
        #             "repayId": "1112126405439270912",
        #             "symbol": "BTCUSDT",
        #             "coin": "USDT",
        #             "repayAmount": "8.000137"
        #         }
        #     }
        #
        data = self.safe_value(response, 'data', {})
        return self.parse_margin_loan(data, currency, market)

    def repay_cross_margin(self, code: str, amount, params={}):
        """
        repay borrowed margin and interest
        :see: https://www.bitget.com/api-doc/margin/cross/account/Cross-Repay
        :param str code: unified currency code of the currency to repay
        :param str amount: the amount to repay
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict: a `margin loan structure <https://docs.ccxt.com/#/?id=margin-loan-structure>`
        """
        self.load_markets()
        currency = self.currency(code)
        request: dict = {
            'coin': currency['id'],
            'repayAmount': self.currency_to_precision(code, amount),
        }
        response = self.privateMarginPostV2MarginCrossedAccountRepay(self.extend(request, params))
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1700876704885,
        #         "data": {
        #             "remainDebtAmount": "0",
        #             "repayId": "1112122994945830912",
        #             "coin": "USDT",
        #             "repayAmount": "4.00006834"
        #         }
        #     }
        #
        data = self.safe_value(response, 'data', {})
        return self.parse_margin_loan(data, currency)

    def parse_margin_loan(self, info, currency: Currency = None, market: Market = None):
        #
        # isolated: borrowMargin
        #
        #     {
        #         "loanId": "1112125304879067137",
        #         "symbol": "BTCUSDT",
        #         "coin": "USDT",
        #         "borrowAmount": "4"
        #     }
        #
        # cross: borrowMargin
        #
        #     {
        #         "loanId": "1112122013642272769",
        #         "coin": "USDT",
        #         "borrowAmount": "4"
        #     }
        #
        # isolated: repayMargin
        #
        #     {
        #         "remainDebtAmount": "0",
        #         "repayId": "1112126405439270912",
        #         "symbol": "BTCUSDT",
        #         "coin": "USDT",
        #         "repayAmount": "8.000137"
        #     }
        #
        # cross: repayMargin
        #
        #     {
        #         "remainDebtAmount": "0",
        #         "repayId": "1112122994945830912",
        #         "coin": "USDT",
        #         "repayAmount": "4.00006834"
        #     }
        #
        currencyId = self.safe_string(info, 'coin')
        marketId = self.safe_string(info, 'symbol')
        symbol = None
        if marketId is not None:
            symbol = self.safe_symbol(marketId, market, None, 'spot')
        return {
            'id': self.safe_string_2(info, 'loanId', 'repayId'),
            'currency': self.safe_currency_code(currencyId, currency),
            'amount': self.safe_number_2(info, 'borrowAmount', 'repayAmount'),
            'symbol': symbol,
            'timestamp': None,
            'datetime': None,
            'info': info,
        }

    def fetch_my_liquidations(self, symbol: Str = None, since: Int = None, limit: Int = None, params={}) -> List[Liquidation]:
        """
        retrieves the users liquidated positions
        :see: https://www.bitget.com/api-doc/margin/cross/record/Get-Cross-Liquidation-Records
        :see: https://www.bitget.com/api-doc/margin/isolated/record/Get-Isolated-Liquidation-Records
        :param str [symbol]: unified CCXT market symbol
        :param int [since]: the earliest time in ms to fetch liquidations for
        :param int [limit]: the maximum number of liquidation structures to retrieve
        :param dict [params]: exchange specific parameters for the bitget api endpoint
        :param int [params.until]: timestamp in ms of the latest liquidation
        :param str [params.marginMode]: 'cross' or 'isolated' default value is 'cross'
        :param boolean [params.paginate]: default False, when True will automatically paginate by calling self endpoint multiple times. See in the docs all the [available parameters](https://github.com/ccxt/ccxt/wiki/Manual#pagination-params)
        :returns dict: an array of `liquidation structures <https://docs.ccxt.com/#/?id=liquidation-structure>`
        """
        self.load_markets()
        paginate = False
        paginate, params = self.handle_option_and_params(params, 'fetchMyLiquidations', 'paginate')
        if paginate:
            return self.fetch_paginated_call_cursor('fetchMyLiquidations', symbol, since, limit, params, 'minId', 'idLessThan')
        market = None
        if symbol is not None:
            market = self.market(symbol)
        type = None
        type, params = self.handle_market_type_and_params('fetchMyLiquidations', market, params)
        if type != 'spot':
            raise NotSupported(self.id + ' fetchMyLiquidations() supports spot margin markets only')
        request: dict = {}
        request, params = self.handle_until_option('endTime', request, params)
        if since is not None:
            request['startTime'] = since
        else:
            request['startTime'] = self.milliseconds() - 7776000000
        if limit is not None:
            request['limit'] = limit
        response = None
        marginMode = None
        marginMode, params = self.handle_margin_mode_and_params('fetchMyLiquidations', params, 'cross')
        if marginMode == 'isolated':
            if symbol is None:
                raise ArgumentsRequired(self.id + ' fetchMyLiquidations() requires a symbol argument')
            request['symbol'] = market['id']
            response = self.privateMarginGetV2MarginIsolatedLiquidationHistory(self.extend(request, params))
        elif marginMode == 'cross':
            response = self.privateMarginGetV2MarginCrossedLiquidationHistory(self.extend(request, params))
        #
        # isolated
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1698114119193,
        #         "data": {
        #             "resultList": [
        #                 {
        #                     "liqId": "123",
        #                     "symbol": "BTCUSDT",
        #                     "liqStartTime": "1653453245342",
        #                     "liqEndTime": "16312423423432",
        #                     "liqRiskRatio": "1.01",
        #                     "totalAssets": "1242.34",
        #                     "totalDebt": "1100",
        #                     "liqFee": "1.2",
        #                     "uTime": "1668134458717",
        #                     "cTime": "1653453245342"
        #                 }
        #             ],
        #             "maxId": "0",
        #             "minId": "0"
        #         }
        #     }
        #
        # cross
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1698114119193,
        #         "data": {
        #             "resultList": [
        #                 {
        #                     "liqId": "123",
        #                     "liqStartTime": "1653453245342",
        #                     "liqEndTime": "16312423423432",
        #                     "liqRiskRatio": "1.01",
        #                     "totalAssets": "1242.34",
        #                     "totalDebt": "1100",
        #                     "LiqFee": "1.2",
        #                     "uTime": "1668134458717",
        #                     "cTime": "1653453245342"
        #                 }
        #             ],
        #             "maxId": "0",
        #             "minId": "0"
        #         }
        #     }
        #
        data = self.safe_value(response, 'data', {})
        liquidations = self.safe_list(data, 'resultList', [])
        return self.parse_liquidations(liquidations, market, since, limit)

    def parse_liquidation(self, liquidation, market: Market = None):
        #
        # isolated
        #
        #     {
        #         "liqId": "123",
        #         "symbol": "BTCUSDT",
        #         "liqStartTime": "1653453245342",
        #         "liqEndTime": "16312423423432",
        #         "liqRiskRatio": "1.01",
        #         "totalAssets": "1242.34",
        #         "totalDebt": "1100",
        #         "liqFee": "1.2",
        #         "uTime": "1692690126000"
        #         "cTime": "1653453245342"
        #     }
        #
        # cross
        #
        #     {
        #         "liqId": "123",
        #         "liqStartTime": "1653453245342",
        #         "liqEndTime": "16312423423432",
        #         "liqRiskRatio": "1.01",
        #         "totalAssets": "1242.34",
        #         "totalDebt": "1100",
        #         "LiqFee": "1.2",
        #         "uTime": "1692690126000"
        #         "cTime": "1653453245342"
        #     }
        #
        marketId = self.safe_string(liquidation, 'symbol')
        timestamp = self.safe_integer(liquidation, 'liqEndTime')
        liquidationFee = self.safe_string_2(liquidation, 'LiqFee', 'liqFee')
        totalDebt = self.safe_string(liquidation, 'totalDebt')
        quoteValueString = Precise.string_add(liquidationFee, totalDebt)
        return self.safe_liquidation({
            'info': liquidation,
            'symbol': self.safe_symbol(marketId, market),
            'contracts': None,
            'contractSize': None,
            'price': None,
            'baseValue': None,
            'quoteValue': self.parse_number(quoteValueString),
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
        })

    def fetch_isolated_borrow_rate(self, symbol: str, params={}) -> IsolatedBorrowRate:
        """
        fetch the rate of interest to borrow a currency for margin trading
        :see: https://www.bitget.com/api-doc/margin/isolated/account/Isolated-Margin-Interest-Rate-And-Max-Borrowable-Amount
        :param str symbol: unified market symbol
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict: an `isolated borrow rate structure <https://docs.ccxt.com/#/?id=isolated-borrow-rate-structure>`
        """
        self.load_markets()
        market = self.market(symbol)
        request: dict = {
            'symbol': market['id'],
        }
        response = self.privateMarginGetV2MarginIsolatedInterestRateAndLimit(self.extend(request, params))
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1700878692567,
        #         "data": [
        #             {
        #                 "symbol": "BTCUSDT",
        #                 "leverage": "10",
        #                 "baseCoin": "BTC",
        #                 "baseTransferable": True,
        #                 "baseBorrowable": True,
        #                 "baseDailyInterestRate": "0.00007",
        #                 "baseAnnuallyInterestRate": "0.02555",
        #                 "baseMaxBorrowableAmount": "27",
        #                 "baseVipList": [
        #                     {"level":"0","dailyInterestRate":"0.00007","limit":"27","annuallyInterestRate":"0.02555","discountRate":"1"},
        #                     {"level":"1","dailyInterestRate":"0.0000679","limit":"27.81","annuallyInterestRate":"0.0247835","discountRate":"0.97"},
        #                     {"level":"2","dailyInterestRate":"0.0000644","limit":"29.16","annuallyInterestRate":"0.023506","discountRate":"0.92"},
        #                     {"level":"3","dailyInterestRate":"0.0000602","limit":"31.32","annuallyInterestRate":"0.021973","discountRate":"0.86"},
        #                     {"level":"4","dailyInterestRate":"0.0000525","limit":"35.91","annuallyInterestRate":"0.0191625","discountRate":"0.75"},
        #                     {"level":"5","dailyInterestRate":"0.000042","limit":"44.82","annuallyInterestRate":"0.01533","discountRate":"0.6"}
        #                 ],
        #                 "quoteCoin": "USDT",
        #                 "quoteTransferable": True,
        #                 "quoteBorrowable": True,
        #                 "quoteDailyInterestRate": "0.00041095",
        #                 "quoteAnnuallyInterestRate": "0.14999675",
        #                 "quoteMaxBorrowableAmount": "300000",
        #                 "quoteList": [
        #                     {"level":"0","dailyInterestRate":"0.00041095","limit":"300000","annuallyInterestRate":"0.14999675","discountRate":"1"},
        #                     {"level":"1","dailyInterestRate":"0.00039863","limit":"309000","annuallyInterestRate":"0.14549995","discountRate":"0.97"},
        #                     {"level":"2","dailyInterestRate":"0.00037808","limit":"324000","annuallyInterestRate":"0.1379992","discountRate":"0.92"},
        #                     {"level":"3","dailyInterestRate":"0.00035342","limit":"348000","annuallyInterestRate":"0.1289983","discountRate":"0.86"},
        #                     {"level":"4","dailyInterestRate":"0.00030822","limit":"399000","annuallyInterestRate":"0.1125003","discountRate":"0.75"},
        #                     {"level":"5","dailyInterestRate":"0.00024657","limit":"498000","annuallyInterestRate":"0.08999805","discountRate":"0.6"}
        #                 ]
        #             }
        #         ]
        #     }
        #
        timestamp = self.safe_integer(response, 'requestTime')
        data = self.safe_value(response, 'data', [])
        first = self.safe_value(data, 0, {})
        first['timestamp'] = timestamp
        return self.parse_isolated_borrow_rate(first, market)

    def parse_isolated_borrow_rate(self, info: dict, market: Market = None) -> IsolatedBorrowRate:
        #
        #     {
        #         "symbol": "BTCUSDT",
        #         "leverage": "10",
        #         "baseCoin": "BTC",
        #         "baseTransferable": True,
        #         "baseBorrowable": True,
        #         "baseDailyInterestRate": "0.00007",
        #         "baseAnnuallyInterestRate": "0.02555",
        #         "baseMaxBorrowableAmount": "27",
        #         "baseVipList": [
        #             {"level":"0","dailyInterestRate":"0.00007","limit":"27","annuallyInterestRate":"0.02555","discountRate":"1"},
        #             {"level":"1","dailyInterestRate":"0.0000679","limit":"27.81","annuallyInterestRate":"0.0247835","discountRate":"0.97"},
        #             {"level":"2","dailyInterestRate":"0.0000644","limit":"29.16","annuallyInterestRate":"0.023506","discountRate":"0.92"},
        #             {"level":"3","dailyInterestRate":"0.0000602","limit":"31.32","annuallyInterestRate":"0.021973","discountRate":"0.86"},
        #             {"level":"4","dailyInterestRate":"0.0000525","limit":"35.91","annuallyInterestRate":"0.0191625","discountRate":"0.75"},
        #             {"level":"5","dailyInterestRate":"0.000042","limit":"44.82","annuallyInterestRate":"0.01533","discountRate":"0.6"}
        #         ],
        #         "quoteCoin": "USDT",
        #         "quoteTransferable": True,
        #         "quoteBorrowable": True,
        #         "quoteDailyInterestRate": "0.00041095",
        #         "quoteAnnuallyInterestRate": "0.14999675",
        #         "quoteMaxBorrowableAmount": "300000",
        #         "quoteList": [
        #             {"level":"0","dailyInterestRate":"0.00041095","limit":"300000","annuallyInterestRate":"0.14999675","discountRate":"1"},
        #             {"level":"1","dailyInterestRate":"0.00039863","limit":"309000","annuallyInterestRate":"0.14549995","discountRate":"0.97"},
        #             {"level":"2","dailyInterestRate":"0.00037808","limit":"324000","annuallyInterestRate":"0.1379992","discountRate":"0.92"},
        #             {"level":"3","dailyInterestRate":"0.00035342","limit":"348000","annuallyInterestRate":"0.1289983","discountRate":"0.86"},
        #             {"level":"4","dailyInterestRate":"0.00030822","limit":"399000","annuallyInterestRate":"0.1125003","discountRate":"0.75"},
        #             {"level":"5","dailyInterestRate":"0.00024657","limit":"498000","annuallyInterestRate":"0.08999805","discountRate":"0.6"}
        #         ]
        #     }
        #
        marketId = self.safe_string(info, 'symbol')
        symbol = self.safe_symbol(marketId, market, None, 'spot')
        baseId = self.safe_string(info, 'baseCoin')
        quoteId = self.safe_string(info, 'quoteCoin')
        timestamp = self.safe_integer(info, 'timestamp')
        return {
            'symbol': symbol,
            'base': self.safe_currency_code(baseId),
            'baseRate': self.safe_number(info, 'baseDailyInterestRate'),
            'quote': self.safe_currency_code(quoteId),
            'quoteRate': self.safe_number(info, 'quoteDailyInterestRate'),
            'period': 86400000,  # 1-Day
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'info': info,
        }

    def fetch_cross_borrow_rate(self, code: str, params={}) -> CrossBorrowRate:
        """
        fetch the rate of interest to borrow a currency for margin trading
        :see: https://www.bitget.com/api-doc/margin/cross/account/Get-Cross-Margin-Interest-Rate-And-Borrowable
        :param str code: unified currency code
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :param str [params.symbol]: required for isolated margin
        :returns dict: a `borrow rate structure <https://github.com/ccxt/ccxt/wiki/Manual#borrow-rate-structure>`
        """
        self.load_markets()
        currency = self.currency(code)
        request: dict = {
            'coin': currency['id'],
        }
        response = self.privateMarginGetV2MarginCrossedInterestRateAndLimit(self.extend(request, params))
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1700879047861,
        #         "data": [
        #             {
        #                 "coin": "BTC",
        #                 "leverage": "3",
        #                 "transferable": True,
        #                 "borrowable": True,
        #                 "dailyInterestRate": "0.00007",
        #                 "annualInterestRate": "0.02555",
        #                 "maxBorrowableAmount": "26",
        #                 "vipList": [
        #                     {"level":"0","limit":"26","dailyInterestRate":"0.00007","annualInterestRate":"0.02555","discountRate":"1"},
        #                     {"level":"1","limit":"26.78","dailyInterestRate":"0.0000679","annualInterestRate":"0.0247835","discountRate":"0.97"},
        #                     {"level":"2","limit":"28.08","dailyInterestRate":"0.0000644","annualInterestRate":"0.023506","discountRate":"0.92"},
        #                     {"level":"3","limit":"30.16","dailyInterestRate":"0.0000602","annualInterestRate":"0.021973","discountRate":"0.86"},
        #                     {"level":"4","limit":"34.58","dailyInterestRate":"0.0000525","annualInterestRate":"0.0191625","discountRate":"0.75"},
        #                     {"level":"5","limit":"43.16","dailyInterestRate":"0.000042","annualInterestRate":"0.01533","discountRate":"0.6"}
        #                 ]
        #             }
        #         ]
        #     }
        #
        timestamp = self.safe_integer(response, 'requestTime')
        data = self.safe_value(response, 'data', [])
        first = self.safe_value(data, 0, {})
        first['timestamp'] = timestamp
        return self.parse_borrow_rate(first, currency)

    def parse_borrow_rate(self, info, currency: Currency = None):
        #
        #     {
        #         "coin": "BTC",
        #         "leverage": "3",
        #         "transferable": True,
        #         "borrowable": True,
        #         "dailyInterestRate": "0.00007",
        #         "annualInterestRate": "0.02555",
        #         "maxBorrowableAmount": "26",
        #         "vipList": [
        #             {"level":"0","limit":"26","dailyInterestRate":"0.00007","annualInterestRate":"0.02555","discountRate":"1"},
        #             {"level":"1","limit":"26.78","dailyInterestRate":"0.0000679","annualInterestRate":"0.0247835","discountRate":"0.97"},
        #             {"level":"2","limit":"28.08","dailyInterestRate":"0.0000644","annualInterestRate":"0.023506","discountRate":"0.92"},
        #             {"level":"3","limit":"30.16","dailyInterestRate":"0.0000602","annualInterestRate":"0.021973","discountRate":"0.86"},
        #             {"level":"4","limit":"34.58","dailyInterestRate":"0.0000525","annualInterestRate":"0.0191625","discountRate":"0.75"},
        #             {"level":"5","limit":"43.16","dailyInterestRate":"0.000042","annualInterestRate":"0.01533","discountRate":"0.6"}
        #         ]
        #     }
        #
        currencyId = self.safe_string(info, 'coin')
        timestamp = self.safe_integer(info, 'timestamp')
        return {
            'currency': self.safe_currency_code(currencyId, currency),
            'rate': self.safe_number(info, 'dailyInterestRate'),
            'period': 86400000,  # 1-Day
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'info': info,
        }

    def fetch_borrow_interest(self, code: Str = None, symbol: Str = None, since: Int = None, limit: Int = None, params={}):
        """
        fetch the interest owed by the user for borrowing currency for margin trading
        :see: https://www.bitget.com/api-doc/margin/cross/record/Get-Cross-Interest-Records
        :see: https://www.bitget.com/api-doc/margin/isolated/record/Get-Isolated-Interest-Records
        :param str [code]: unified currency code
        :param str [symbol]: unified market symbol when fetching interest in isolated markets
        :param int [since]: the earliest time in ms to fetch borrow interest for
        :param int [limit]: the maximum number of structures to retrieve
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :param boolean [params.paginate]: default False, when True will automatically paginate by calling self endpoint multiple times. See in the docs all the [available parameters](https://github.com/ccxt/ccxt/wiki/Manual#pagination-params)
        :returns dict[]: a list of `borrow interest structures <https://docs.ccxt.com/#/?id=borrow-interest-structure>`
        """
        self.load_markets()
        paginate = False
        paginate, params = self.handle_option_and_params(params, 'fetchBorrowInterest', 'paginate')
        if paginate:
            return self.fetch_paginated_call_cursor('fetchBorrowInterest', symbol, since, limit, params, 'minId', 'idLessThan')
        market = None
        if symbol is not None:
            market = self.market(symbol)
        request: dict = {}
        currency = None
        if code is not None:
            currency = self.currency(code)
            request['coin'] = currency['id']
        if since is not None:
            request['startTime'] = since
        else:
            request['startTime'] = self.milliseconds() - 7776000000
        if limit is not None:
            request['limit'] = limit
        response = None
        marginMode = None
        marginMode, params = self.handle_margin_mode_and_params('fetchBorrowInterest', params, 'cross')
        if marginMode == 'isolated':
            if symbol is None:
                raise ArgumentsRequired(self.id + ' fetchBorrowInterest() requires a symbol argument')
            request['symbol'] = market['id']
            response = self.privateMarginGetV2MarginIsolatedInterestHistory(self.extend(request, params))
        elif marginMode == 'cross':
            response = self.privateMarginGetV2MarginCrossedInterestHistory(self.extend(request, params))
        #
        # isolated
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1700879935189,
        #         "data": {
        #             "resultList": [
        #                 {
        #                     "interestId": "1112125304879067137",
        #                     "interestCoin": "USDT",
        #                     "dailyInterestRate": "0.00041095",
        #                     "loanCoin": "USDT",
        #                     "interestAmount": "0.0000685",
        #                     "interstType": "first",
        #                     "symbol": "BTCUSDT",
        #                     "cTime": "1700877255648",
        #                     "uTime": "1700877255648"
        #                 },
        #             ],
        #             "maxId": "1112125304879067137",
        #             "minId": "1100138015672119298"
        #         }
        #     }
        #
        # cross
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1700879597044,
        #         "data": {
        #             "resultList": [
        #                 {
        #                     "interestId": "1112122013642272769",
        #                     "interestCoin": "USDT",
        #                     "dailyInterestRate": "0.00041",
        #                     "loanCoin": "USDT",
        #                     "interestAmount": "0.00006834",
        #                     "interstType": "first",
        #                     "cTime": "1700876470957",
        #                     "uTime": "1700876470957"
        #                 },
        #             ],
        #             "maxId": "1112122013642272769",
        #             "minId": "1096917004629716993"
        #         }
        #     }
        #
        data = self.safe_value(response, 'data', {})
        rows = self.safe_value(data, 'resultList', [])
        interest = self.parse_borrow_interests(rows, market)
        return self.filter_by_currency_since_limit(interest, code, since, limit)

    def parse_borrow_interest(self, info: dict, market: Market = None):
        #
        # isolated
        #
        #     {
        #         "interestId": "1112125304879067137",
        #         "interestCoin": "USDT",
        #         "dailyInterestRate": "0.00041095",
        #         "loanCoin": "USDT",
        #         "interestAmount": "0.0000685",
        #         "interstType": "first",
        #         "symbol": "BTCUSDT",
        #         "cTime": "1700877255648",
        #         "uTime": "1700877255648"
        #     }
        #
        # cross
        #
        #     {
        #         "interestId": "1112122013642272769",
        #         "interestCoin": "USDT",
        #         "dailyInterestRate": "0.00041",
        #         "loanCoin": "USDT",
        #         "interestAmount": "0.00006834",
        #         "interstType": "first",
        #         "cTime": "1700876470957",
        #         "uTime": "1700876470957"
        #     }
        #
        marketId = self.safe_string(info, 'symbol')
        market = self.safe_market(marketId, market)
        marginMode = 'isolated' if (marketId is not None) else 'cross'
        timestamp = self.safe_integer(info, 'cTime')
        return {
            'symbol': self.safe_string(market, 'symbol'),
            'marginMode': marginMode,
            'currency': self.safe_currency_code(self.safe_string(info, 'interestCoin')),
            'interest': self.safe_number(info, 'interestAmount'),
            'interestRate': self.safe_number(info, 'dailyInterestRate'),
            'amountBorrowed': None,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'info': info,
        }

    def close_position(self, symbol: str, side: OrderSide = None, params={}) -> Order:
        """
        closes an open position for a market
        :see: https://www.bitget.com/api-doc/contract/trade/Flash-Close-Position
        :param str symbol: unified CCXT market symbol
        :param str [side]: one-way mode: 'buy' or 'sell', hedge-mode: 'long' or 'short'
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict: An `order structure <https://docs.ccxt.com/#/?id=order-structure>`
        """
        self.load_markets()
        sandboxMode = self.safe_bool(self.options, 'sandboxMode', False)
        market = None
        if sandboxMode:
            sandboxSymbol = self.convert_symbol_for_sandbox(symbol)
            market = self.market(sandboxSymbol)
        else:
            market = self.market(symbol)
        productType = None
        productType, params = self.handle_product_type_and_params(market, params)
        request: dict = {
            'symbol': market['id'],
            'productType': productType,
        }
        if side is not None:
            request['holdSide'] = side
        response = self.privateMixPostV2MixOrderClosePositions(self.extend(request, params))
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1702975017017,
        #         "data": {
        #             "successList": [
        #                 {
        #                     "orderId": "1120923953904893955",
        #                     "clientOid": "1120923953904893956"
        #                 }
        #             ],
        #             "failureList": [],
        #             "result": False
        #         }
        #     }
        #
        data = self.safe_value(response, 'data', {})
        order = self.safe_list(data, 'successList', [])
        return self.parse_order(order[0], market)

    def close_all_positions(self, params={}) -> List[Position]:
        """
        closes all open positions for a market type
        :see: https://www.bitget.com/api-doc/contract/trade/Flash-Close-Position
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :param str [params.productType]: 'USDT-FUTURES', 'USDC-FUTURES', 'COIN-FUTURES', 'SUSDT-FUTURES', 'SUSDC-FUTURES' or 'SCOIN-FUTURES'
        :returns dict[]: A list of `position structures <https://docs.ccxt.com/#/?id=position-structure>`
        """
        self.load_markets()
        productType = None
        productType, params = self.handle_product_type_and_params(None, params)
        request: dict = {
            'productType': productType,
        }
        response = self.privateMixPostV2MixOrderClosePositions(self.extend(request, params))
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1702975017017,
        #         "data": {
        #             "successList": [
        #                 {
        #                     "orderId": "1120923953904893955",
        #                     "clientOid": "1120923953904893956"
        #                 }
        #             ],
        #             "failureList": [],
        #             "result": False
        #         }
        #     }
        #
        data = self.safe_value(response, 'data', {})
        orderInfo = self.safe_list(data, 'successList', [])
        return self.parse_positions(orderInfo, None, params)

    def fetch_margin_mode(self, symbol: str, params={}) -> MarginMode:
        """
        fetches the margin mode of a trading pair
        :see: https://www.bitget.com/api-doc/contract/account/Get-Single-Account
        :param str symbol: unified symbol of the market to fetch the margin mode for
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict: a `margin mode structure <https://docs.ccxt.com/#/?id=margin-mode-structure>`
        """
        self.load_markets()
        sandboxMode = self.safe_bool(self.options, 'sandboxMode', False)
        market = None
        if sandboxMode:
            sandboxSymbol = self.convert_symbol_for_sandbox(symbol)
            market = self.market(sandboxSymbol)
        else:
            market = self.market(symbol)
        productType = None
        productType, params = self.handle_product_type_and_params(market, params)
        request: dict = {
            'symbol': market['id'],
            'marginCoin': market['settleId'],
            'productType': productType,
        }
        response = self.privateMixGetV2MixAccountAccount(self.extend(request, params))
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1709791216652,
        #         "data": {
        #             "marginCoin": "USDT",
        #             "locked": "0",
        #             "available": "19.88811074",
        #             "crossedMaxAvailable": "19.88811074",
        #             "isolatedMaxAvailable": "19.88811074",
        #             "maxTransferOut": "19.88811074",
        #             "accountEquity": "19.88811074",
        #             "usdtEquity": "19.888110749166",
        #             "btcEquity": "0.000302183391",
        #             "crossedRiskRate": "0",
        #             "crossedMarginLeverage": 20,
        #             "isolatedLongLever": 20,
        #             "isolatedShortLever": 20,
        #             "marginMode": "crossed",
        #             "posMode": "hedge_mode",
        #             "unrealizedPL": "0",
        #             "coupon": "0",
        #             "crossedUnrealizedPL": "0",
        #             "isolatedUnrealizedPL": ""
        #         }
        #     }
        #
        data = self.safe_dict(response, 'data', {})
        return self.parse_margin_mode(data, market)

    def parse_margin_mode(self, marginMode: dict, market=None) -> MarginMode:
        marginType = self.safe_string(marginMode, 'marginMode')
        marginType = 'cross' if (marginType == 'crossed') else marginType
        return {
            'info': marginMode,
            'symbol': market['symbol'],
            'marginMode': marginType,
        }

    def fetch_positions_history(self, symbols: Strings = None, since: Int = None, limit: Int = None, params={}) -> List[Position]:
        """
        fetches historical positions
        :see: https://www.bitget.com/api-doc/contract/position/Get-History-Position
        :param str[] [symbols]: unified contract symbols
        :param int [since]: timestamp in ms of the earliest position to fetch, default=3 months ago, max range for params["until"] - since is 3 months
        :param int [limit]: the maximum amount of records to fetch, default=20, max=100
        :param dict params: extra parameters specific to the exchange api endpoint
        :param int [params.until]: timestamp in ms of the latest position to fetch, max range for params["until"] - since is 3 months
         *
         * EXCHANGE SPECIFIC PARAMETERS
        :param str [params.productType]: USDT-FUTURES(default), COIN-FUTURES, USDC-FUTURES, SUSDT-FUTURES, SCOIN-FUTURES, or SUSDC-FUTURES
        :returns dict[]: a list of `position structures <https://docs.ccxt.com/#/?id=position-structure>`
        """
        self.load_markets()
        until = self.safe_integer(params, 'until')
        params = self.omit(params, 'until')
        request: dict = {}
        if symbols is not None:
            symbolsLength = len(symbols)
            if symbolsLength > 0:
                market = self.market(symbols[0])
                request['symbol'] = market['id']
        if since is not None:
            request['startTime'] = since
        if limit is not None:
            request['limit'] = limit
        if until is not None:
            request['endTime'] = until
        response = self.privateMixGetV2MixPositionHistoryPosition(self.extend(request, params))
        #
        #    {
        #        code: '00000',
        #        msg: 'success',
        #        requestTime: '1712794148791',
        #        data: {
        #            list: [
        #                {
        #                    symbol: 'XRPUSDT',
        #                    marginCoin: 'USDT',
        #                    holdSide: 'long',
        #                    openAvgPrice: '0.64967',
        #                    closeAvgPrice: '0.58799',
        #                    marginMode: 'isolated',
        #                    openTotalPos: '10',
        #                    closeTotalPos: '10',
        #                    pnl: '-0.62976205',
        #                    netProfit: '-0.65356802',
        #                    totalFunding: '-0.01638',
        #                    openFee: '-0.00389802',
        #                    closeFee: '-0.00352794',
        #                    ctime: '1709590322199',
        #                    utime: '1709667583395'
        #                },
        #                ...
        #            ]
        #        }
        #    }
        #
        data = self.safe_dict(response, 'data')
        responseList = self.safe_list(data, 'list')
        positions = self.parse_positions(responseList, symbols, params)
        return self.filter_by_since_limit(positions, since, limit)

    def fetch_convert_quote(self, fromCode: str, toCode: str, amount: Num = None, params={}) -> Conversion:
        """
        fetch a quote for converting from one currency to another
        :see: https://www.bitget.com/api-doc/common/convert/Get-Quoted-Price
        :param str fromCode: the currency that you want to sell and convert from
        :param str toCode: the currency that you want to buy and convert into
        :param float [amount]: how much you want to trade in units of the from currency
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict: a `conversion structure <https://docs.ccxt.com/#/?id=conversion-structure>`
        """
        self.load_markets()
        request: dict = {
            'fromCoin': fromCode,
            'toCoin': toCode,
            'fromCoinSize': self.number_to_string(amount),
        }
        response = self.privateConvertGetV2ConvertQuotedPrice(self.extend(request, params))
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1712121940158,
        #         "data": {
        #             "fromCoin": "USDT",
        #             "fromCoinSize": "5",
        #             "cnvtPrice": "0.9993007892377704",
        #             "toCoin": "USDC",
        #             "toCoinSize": "4.99650394",
        #             "traceId": "1159288930228187140",
        #             "fee": "0"
        #         }
        #     }
        #
        data = self.safe_dict(response, 'data', {})
        fromCurrencyId = self.safe_string(data, 'fromCoin', fromCode)
        fromCurrency = self.currency(fromCurrencyId)
        toCurrencyId = self.safe_string(data, 'toCoin', toCode)
        toCurrency = self.currency(toCurrencyId)
        return self.parse_conversion(data, fromCurrency, toCurrency)

    def create_convert_trade(self, id: str, fromCode: str, toCode: str, amount: Num = None, params={}) -> Conversion:
        """
        convert from one currency to another
        :see: https://www.bitget.com/api-doc/common/convert/Trade
        :param str id: the id of the trade that you want to make
        :param str fromCode: the currency that you want to sell and convert from
        :param str toCode: the currency that you want to buy and convert into
        :param float amount: how much you want to trade in units of the from currency
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :param str params['price']: the price of the conversion, obtained from fetchConvertQuote()
        :param str params['toAmount']: the amount you want to trade in units of the toCurrency, obtained from fetchConvertQuote()
        :returns dict: a `conversion structure <https://docs.ccxt.com/#/?id=conversion-structure>`
        """
        self.load_markets()
        price = self.safe_string_2(params, 'price', 'cnvtPrice')
        if price is None:
            raise ArgumentsRequired(self.id + ' createConvertTrade() requires a price parameter')
        toAmount = self.safe_string_2(params, 'toAmount', 'toCoinSize')
        if toAmount is None:
            raise ArgumentsRequired(self.id + ' createConvertTrade() requires a toAmount parameter')
        params = self.omit(params, ['price', 'toAmount'])
        request: dict = {
            'traceId': id,
            'fromCoin': fromCode,
            'toCoin': toCode,
            'fromCoinSize': self.number_to_string(amount),
            'toCoinSize': toAmount,
            'cnvtPrice': price,
        }
        response = self.privateConvertPostV2ConvertTrade(self.extend(request, params))
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1712123746203,
        #         "data": {
        #             "cnvtPrice": "0.99940076",
        #             "toCoin": "USDC",
        #             "toCoinSize": "4.99700379",
        #             "ts": "1712123746217"
        #         }
        #     }
        #
        data = self.safe_dict(response, 'data', {})
        toCurrencyId = self.safe_string(data, 'toCoin', toCode)
        toCurrency = self.currency(toCurrencyId)
        return self.parse_conversion(data, None, toCurrency)

    def fetch_convert_trade_history(self, code: Str = None, since: Int = None, limit: Int = None, params={}) -> List[Conversion]:
        """
        fetch the users history of conversion trades
        :see: https://www.bitget.com/api-doc/common/convert/Get-Convert-Record
        :param str [code]: the unified currency code
        :param int [since]: the earliest time in ms to fetch conversions for
        :param int [limit]: the maximum number of conversion structures to retrieve
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict[]: a list of `conversion structures <https://docs.ccxt.com/#/?id=conversion-structure>`
        """
        self.load_markets()
        request: dict = {}
        msInDay = 86400000
        now = self.milliseconds()
        if since is not None:
            request['startTime'] = since
        else:
            request['startTime'] = now - msInDay
        endTime = self.safe_string_2(params, 'endTime', 'until')
        if endTime is not None:
            request['endTime'] = endTime
        else:
            request['endTime'] = now
        if limit is not None:
            request['limit'] = limit
        params = self.omit(params, 'until')
        response = self.privateConvertGetV2ConvertConvertRecord(self.extend(request, params))
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1712124371799,
        #         "data": {
        #             "dataList": [
        #                 {
        #                     "id": "1159296505255219205",
        #                     "fromCoin": "USDT",
        #                     "fromCoinSize": "5",
        #                     "cnvtPrice": "0.99940076",
        #                     "toCoin": "USDC",
        #                     "toCoinSize": "4.99700379",
        #                     "ts": "1712123746217",
        #                     "fee": "0"
        #                 }
        #             ],
        #             "endId": "1159296505255219205"
        #         }
        #     }
        #
        data = self.safe_dict(response, 'data', {})
        dataList = self.safe_list(data, 'dataList', [])
        return self.parse_conversions(dataList, code, 'fromCoin', 'toCoin', since, limit)

    def parse_conversion(self, conversion: dict, fromCurrency: Currency = None, toCurrency: Currency = None) -> Conversion:
        #
        # fetchConvertQuote
        #
        #     {
        #         "fromCoin": "USDT",
        #         "fromCoinSize": "5",
        #         "cnvtPrice": "0.9993007892377704",
        #         "toCoin": "USDC",
        #         "toCoinSize": "4.99650394",
        #         "traceId": "1159288930228187140",
        #         "fee": "0"
        #     }
        #
        # createConvertTrade
        #
        #     {
        #         "cnvtPrice": "0.99940076",
        #         "toCoin": "USDC",
        #         "toCoinSize": "4.99700379",
        #         "ts": "1712123746217"
        #     }
        #
        # fetchConvertTradeHistory
        #
        #     {
        #         "id": "1159296505255219205",
        #         "fromCoin": "USDT",
        #         "fromCoinSize": "5",
        #         "cnvtPrice": "0.99940076",
        #         "toCoin": "USDC",
        #         "toCoinSize": "4.99700379",
        #         "ts": "1712123746217",
        #         "fee": "0"
        #     }
        #
        timestamp = self.safe_integer(conversion, 'ts')
        fromCoin = self.safe_string(conversion, 'fromCoin')
        fromCode = self.safe_currency_code(fromCoin, fromCurrency)
        to = self.safe_string(conversion, 'toCoin')
        toCode = self.safe_currency_code(to, toCurrency)
        return {
            'info': conversion,
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
            'id': self.safe_string_2(conversion, 'id', 'traceId'),
            'fromCurrency': fromCode,
            'fromAmount': self.safe_number(conversion, 'fromCoinSize'),
            'toCurrency': toCode,
            'toAmount': self.safe_number(conversion, 'toCoinSize'),
            'price': self.safe_number(conversion, 'cnvtPrice'),
            'fee': self.safe_number(conversion, 'fee'),
        }

    def fetch_convert_currencies(self, params={}) -> Currencies:
        """
        fetches all available currencies that can be converted
        :see: https://www.bitget.com/api-doc/common/convert/Get-Convert-Currencies
        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict: an associative dictionary of currencies
        """
        self.load_markets()
        response = self.privateConvertGetV2ConvertCurrencies(params)
        #
        #     {
        #         "code": "00000",
        #         "msg": "success",
        #         "requestTime": 1712121755897,
        #         "data": [
        #             {
        #                 "coin": "BTC",
        #                 "available": "0.00009850",
        #                 "maxAmount": "0.756266",
        #                 "minAmount": "0.00001"
        #             },
        #         ]
        #     }
        #
        result: dict = {}
        data = self.safe_list(response, 'data', [])
        for i in range(0, len(data)):
            entry = data[i]
            id = self.safe_string(entry, 'coin')
            code = self.safe_currency_code(id)
            result[code] = {
                'info': entry,
                'id': id,
                'code': code,
                'networks': None,
                'type': None,
                'name': None,
                'active': None,
                'deposit': None,
                'withdraw': self.safe_number(entry, 'available'),
                'fee': None,
                'precision': None,
                'limits': {
                    'amount': {
                        'min': self.safe_number(entry, 'minAmount'),
                        'max': self.safe_number(entry, 'maxAmount'),
                    },
                    'withdraw': {
                        'min': None,
                        'max': None,
                    },
                    'deposit': {
                        'min': None,
                        'max': None,
                    },
                },
                'created': None,
            }
        return result

    def handle_errors(self, code: int, reason: str, url: str, method: str, headers: dict, body: str, response, requestHeaders, requestBody):
        if not response:
            return None  # fallback to default error handler
        #
        # spot
        #
        #     {"code":"00000","msg":"success","requestTime":1713294492511,"data":[...]}"
        #
        #     {"status":"fail","err_code":"01001","err_msg":"系统异常，请稍后重试"}
        #     {"status":"error","ts":1595594160149,"err_code":"invalid-parameter","err_msg":"invalid size, valid range: [1,2000]"}
        #     {"status":"error","ts":1595684716042,"err_code":"invalid-parameter","err_msg":"illegal sign invalid"}
        #     {"status":"error","ts":1595700216275,"err_code":"bad-request","err_msg":"your balance is low!"}
        #     {"status":"error","ts":1595700344504,"err_code":"invalid-parameter","err_msg":"invalid type"}
        #     {"status":"error","ts":1595703343035,"err_code":"bad-request","err_msg":"order cancel fail"}
        #     {"status":"error","ts":1595704360508,"err_code":"invalid-parameter","err_msg":"accesskey not null"}
        #     {"status":"error","ts":1595704490084,"err_code":"invalid-parameter","err_msg":"permissions not right"}
        #     {"status":"error","ts":1595711862763,"err_code":"system exception","err_msg":"system exception"}
        #     {"status":"error","ts":1595730308979,"err_code":"bad-request","err_msg":"20003"}
        #
        # swap
        #
        #     {"code":"40015","msg":"","requestTime":1595698564931,"data":null}
        #     {"code":"40017","msg":"Order id must not be blank","requestTime":1595702477835,"data":null}
        #     {"code":"40017","msg":"Order Type must not be blank","requestTime":1595698516162,"data":null}
        #     {"code":"40301","msg":"","requestTime":1595667662503,"data":null}
        #     {"code":"40017","msg":"Contract code must not be blank","requestTime":1595703151651,"data":null}
        #     {"code":"40108","msg":"","requestTime":1595885064600,"data":null}
        #     {"order_id":"513468410013679613","client_oid":null,"symbol":"ethusd","result":false,"err_code":"order_no_exist_error","err_msg":"订单不存在！"}
        #
        message = self.safe_string_2(response, 'err_msg', 'msg')
        feedback = self.id + ' ' + body
        nonEmptyMessage = ((message is not None) and (message != '') and (message != 'success'))
        if nonEmptyMessage:
            self.throw_exactly_matched_exception(self.exceptions['exact'], message, feedback)
            self.throw_broadly_matched_exception(self.exceptions['broad'], message, feedback)
        errorCode = self.safe_string_2(response, 'code', 'err_code')
        nonZeroErrorCode = (errorCode is not None) and (errorCode != '00000')
        if nonZeroErrorCode:
            self.throw_exactly_matched_exception(self.exceptions['exact'], errorCode, feedback)
        if nonZeroErrorCode or nonEmptyMessage:
            raise ExchangeError(feedback)  # unknown message
        return None

    def nonce(self):
        return self.milliseconds() - self.options['timeDifference']

    def sign(self, path, api=[], method='GET', params={}, headers=None, body=None):
        signed = api[0] == 'private'
        endpoint = api[1]
        pathPart = '/api'
        request = '/' + self.implode_params(path, params)
        payload = pathPart + request
        url = self.implode_hostname(self.urls['api'][endpoint]) + payload
        query = self.omit(params, self.extract_params(path))
        if not signed and (method == 'GET'):
            keys = list(query.keys())
            keysLength = len(keys)
            if keysLength > 0:
                url = url + '?' + self.urlencode(query)
        if signed:
            self.check_required_credentials()
            timestamp = str(self.nonce())
            auth = timestamp + method + payload
            if method == 'POST':
                body = self.json(params)
                auth += body
            else:
                if params:
                    queryInner = '?' + self.urlencode(self.keysort(params))
                    # check  #21169 pr
                    if queryInner.find('%24') > -1:
                        queryInner = queryInner.replace('%24', '$')
                    url += queryInner
                    auth += queryInner
            signature = self.hmac(self.encode(auth), self.encode(self.secret), hashlib.sha256, 'base64')
            broker = self.safe_string(self.options, 'broker')
            headers = {
                'ACCESS-KEY': self.apiKey,
                'ACCESS-SIGN': signature,
                'ACCESS-TIMESTAMP': timestamp,
                'ACCESS-PASSPHRASE': self.password,
                'X-CHANNEL-API-CODE': broker,
            }
            if method == 'POST':
                headers['Content-Type'] = 'application/json'
        return {'url': url, 'method': method, 'body': body, 'headers': headers}