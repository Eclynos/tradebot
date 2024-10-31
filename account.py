import ccxt.pro as ccxt

class Account:
    def __init__(self, key_file) -> None:
        with open(key_file, 'r') as file:
            self.access_key = file.readline().strip()
            self.secret_key = file.readline().strip()
            self.passphrase = file.readline().strip()
        self.exchange = None
        
        
    async def connect(self):
        """Connect account with api keys to python"""
        try:
            self.exchange = ccxt.bitget({ # etablie la connexion au compte
                'apiKey': self.access_key,
                'secret': self.secret_key,
                'password': self.passphrase,
                'enableRateLimit': True,
                'options': {
                    'defaultType': 'swap',
                }
            })
        
            self.exchange.verbose = False # pour le debug si True
            print("Connected")

        except Exception as e:
            print(f"Failed connecting\n{e}")
        
        
    async def disconnect(self): # à faire à la fin de l'utilisation du compte, à la fin du code
        """Disconnect linked account"""
        try:
            await self.exchange.close()
            print("Disconnected")
        except Exception as e:
            print(f"Failed disconnecting\n{e}")