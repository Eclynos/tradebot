import requests, json

class Tools:
    def __init__(self) -> None:
        self.codeToIDDico = {}
        with open('./data/codeToID.json','r') as json_File:
            self.codeToIDDico = json.load(json_File)


    def getCoinData(self, coinCode : str, timeFrame : str) -> list:

        if timeFrame not in ("1D", "7D", "1M", "1Y", "All"):
            print("Invalid Time Frame")
            return {}

        r = requests.get(f'https://api.coinmarketcap.com/data-api/v3/cryptocurrency/detail/chart?id={self.codeToIDDico[coinCode]}&range={timeFrame}')
        try:
            r = r.json()
        except:
            return []
        
        r = r["data"]
        if "points" not in r.keys():
            print(f"ERROR [{coinCode}] :", r)
        r = r["points"]
        l = []
        for k in r.keys():
            l.append({"key" : k, "price" : r[k]["v"][0], "volume" : r[k]["v"][1], "mc" : r[k]["v"][2]})

        l.sort(key= lambda item : int(item["key"])) #normalement pas nécessaire mais on sait jamais

        return l
    

    def time_frame_to_ms(self, time_frame):
        """Calcule le bon nombre de ms pour une time_frame donnée"""
        unit = time_frame[-1]
        amount = int(time_frame[:-1])
        if unit == 'm':
            return amount * 60 * 1000
        elif unit == 'h':
            return amount * 60 * 60 * 1000
        elif unit == 'd':
            return amount * 24 * 60 * 60 * 1000
        else:
            print("Mauvais time_frame")


    def ping_test(url="http://www.google.com", timeout=3):
        try:
            response = requests.get(url, timeout=timeout)
            return True if response.status_code == 200 else False
        except (requests.ConnectionError, requests.Timeout):
            return False
