import requests, csv, time
from math import floor

def left(symbol):
    return symbol.split("/")[0]


def right(symbol):
    return symbol.split("/")[1]


def readFile(coinCode) -> list:
    with open(f"./data/{coinCode}-USDT.csv", 'r') as file_csv:
        allData = csv.DictReader(file_csv)
        allData = list(allData)

    return allData


def time_frame_to_s(time_frame):
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


def time_frame_to_ms(time_frame):
    """Calcule le bon nombre de ms pour une time_frame donnée"""
    secAmount = time_frame_to_s(time_frame)
    if secAmount == None:
        return None
    else:
        return secAmount * 1000


def ping_test(url="https://www.google.com", timeout=3):
    try:
        response = requests.get(url, timeout=timeout)
        return True if response.status_code == 200 else False
    except (requests.ConnectionError, requests.Timeout):
        return False


def binarySearch(data, value, key=None):
    a = 0
    b = len(data)-1
    while a != b:
        mid = (a+b)//2
        if key == None:
            if data[mid] == value:
                return mid
            elif data[mid] > value:
                b = mid
            else:
                a = mid + 1

        else:
            if data[mid][key] == value:
                return mid
            if data[mid][key] > value:
                b = mid
            else:
                a = mid + 1
    
    return a


def read_symbols():
    with open('data/symbols', 'r') as file:
        symbols = [line.strip() for line in file]
    return symbols


def wait_next_frame(timeLoop=5):
    """Wait for next time frame comparing to world time"""
    actual = time.time() % (60 * timeLoop)
    time.sleep(60 * timeLoop - actual)