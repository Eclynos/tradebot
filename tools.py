import requests, json, csv
import pandas as pd


def left(symbol):
    return symbol.split("/")[0]


def right(symbol):
    return symbol.split("/")[1]


class Tools:
    def __init__(self) -> None:
        pass
    
    
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
        elif unit == 'w':
            return amount * 7 * 24 * 60 * 60
        elif unit == 'M':
            return int(amount * 30.5 * 24 * 60 * 60)
        elif unit == 'y':
            return int(amount * 365.25 * 24 * 60 * 60)
        else:
            print("Mauvais time_frame")


    def time_frame_to_ms(self, time_frame):
        """Calcule le bon nombre de ms pour une time_frame donnée"""
        secAmount = self.time_frame_to_s(time_frame)
        if secAmount == None:
            return None
        else:
            return secAmount * 1000


    def ping_test(self, url="https://www.google.com", timeout=3):
        try:
            response = requests.get(url, timeout=timeout)
            return True if response.status_code == 200 else False
        except (requests.ConnectionError, requests.Timeout):
            return False


    def binarySearch(self, data, value, key=None):
        a= 0
        b= len(data)-1
        while a != b:
            mid = (a+b)//2
            if key == None:
                if data[mid] == value:
                    return mid
                elif data[mid] > value:
                    b = mid
                else:
                    a = mid+1

            else:
                if data[mid][key] == value:
                    return mid
                if data[mid][key] > value:
                    b = mid
                else:
                    a=mid+1
        
        return a

# remplacer la class tools par une liste de fonctions à importer