# Tradebot

Authors:
 * Nathael CARLIER
 * Nicolas ANGLADE

The goal of this project is to create a trading bot using ccxt Api request to manage bitget wallets.

## Requirements

Create a [venv](https://docs.python.org/3/library/venv.html), and install the following packages inside (with pip):
- ccxt
- numpy
- logging
- requests

Some tests, or best parameters calculators programms are using other libraries, that are not necessary to run the bot :
- multiprocessing
- torch

To collect old candles data we are using [Backtest tools](https://github.com/CryptoRobotFr/Backtest-Tools-V2).

## Installation

``` bash
git clone https://github.com/Eclynos/tradebot.git
```

## Execution

On a file write on 3 lines your access key, secret key and passphrase of an API account instance you created on Bitget. Then, set the settings changing settings.json file.

After that, you can launch loop.py on a parralel terminal. Don't forget to run it on a venv.