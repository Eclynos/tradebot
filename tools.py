import requests, json, csv

class Tools:
    def __init__(self) -> None:
        self.codeToIDDico = {}
        with open('./data/codeToID.json','r') as json_File:
            self.codeToIDDico = json.load(json_File)

    def readFile(self, coinCode) -> list:
        with open(f"./data/{coinCode}-USDT.csv", 'r') as file_csv:
            allData = csv.DictReader(file_csv)
            allData = list(allData)

        return allData

    def time_frame_to_s(self, time_frame):
        """Calcule le bon nombre de s pour une time_frame donnée"""
        unit = time_frame[-1]
        amount = int(time_frame[:-1])
        if unit == 'm':
            return amount * 60
        elif unit == 'h':
            return amount * 60 * 60
        elif unit == 'd':
            return amount * 24 * 60 * 60
        else:
            print("Mauvais time_frame")


    def time_frame_to_ms(self, time_frame):
        """Calcule le bon nombre de ms pour une time_frame donnée"""
        secAmount = self.time_frame_to_s(time_frame)
        if secAmount==None:
            return None
        else:
            return secAmount * 1000


    def ping_test(self, url="https://www.google.com", timeout=3):
        try:
            response = requests.get(url, timeout=timeout)
            return True if response.status_code == 200 else False
        except (requests.ConnectionError, requests.Timeout):
            return False
