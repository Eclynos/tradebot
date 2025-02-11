import requests, csv, time, itertools, sys
from math import ceil


def left(symbol):
    return symbol.split("/")[0]


def right(symbol):
    return symbol.split("/")[1]


def readFile(coinCode, exchange) -> list:
    """Lit les fichiers csv et retourne une liste de dictionnaires de bougie"""
    with open(f"./data/{coinCode}-USDT{"-USDT" if exchange == "bitget" else ""}.csv", 'r') as file_csv:
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


def ping_test(url="https://www.google.com", timeout=2):
    try:
        response = requests.get(url, timeout=timeout)
        return True if response.status_code == 200 else False
    except (requests.ConnectionError, requests.Timeout):
        return False


def binarySearch(data, value, key=None):
    """Effectue une recherche binaire dans une liste de données"""
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
    time.sleep(ceil(60 * timeLoop - actual))


def getDataIndex(time, start, end, data, launch_sample_size):
    """
    Trouve les indices de début et de fin correspondant à la période donnée
    dans la liste des bougies
    """
    start = time - time_frame_to_ms(start)
    end = time - time_frame_to_ms(end)
    if start < int(data[0]["date"]) + launch_sample_size * 300000:
        raise ValueError(f"Start date too old for coinData. start :{start} dataStart :{data[0]["date"]}")
    if end > int(data[-1]["date"]):
        raise ValueError(f"End date too young for coinData. end :{end} dataEnd :{data[-1]["date"]}")
    return int((start - int(data[0]["date"])) / 300000), int((end - int(data[0]["date"])) / 300000)


def AreAnyCandlesMissing(data):
    """
    Regarde si il y a des espaces dans la liste des bougies
    renvoie le nombre d'espace correspondant au nombre de bougies manquantes
    """
    startStamp = int(data[0]["date"])
    amount_missing = 0
    for i in range(len(data)):
        if int(data[i]["date"]) != startStamp + i * 300000:
            #print(f"A candle is missing at {startStamp + i * 300000}\nIndex : {i}")
            startStamp += 300000
            amount_missing += 1
    print(f"{amount_missing} candles are missing on this database")


def spinner(stop_event):
    """
    Affiche une jolie animation de chargement
    """
    global done
    for c in itertools.cycle(["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]):
        if stop_event.is_set():
            break
        sys.stdout.write(f"\r{c}")
        sys.stdout.flush()
        time.sleep(0.1)

def timeStampToIndex(data, timeStamp):
    """
    Renvoie l'indice de la case de data où l'entrée date est égale à timeStamp
    """
    tailleBougie = data[1]["date"] - data[0]["date"]
    return (timeStamp-data[0]["date"]) // tailleBougie