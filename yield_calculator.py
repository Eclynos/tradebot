import re

result_flat = 1
result_reinvested = 1
trades_done = 0
buy_prices = {}

with open("trade_logs.log", "r") as f:
    for line in f:
        try:
            if line[28] == "B":
                match = re.search(r'(\w+/\w+)', line)
                match_price = re.search(r'at (\d+\.\d+|\d+e-\d+)', line)
                if match and match_price:
                    buy_prices[match.group(1)]
                else:
                    raise ValueError("Error of re")
            elif line[28] == "S":
                match = re.search(r'(\w+/\w+)', line)
                match_price = re.search(r'at (\d+\.\d+|\d+e-\d+)', line)
                if match and match_price:
                    trades_done += 1
                    percentage_difference = (match_price.group(1) - buy_prices[match.group(1)]) / buy_prices[match.group(1)] * 100
                    result_flat += percentage_difference
                    result_reinvested *= percentage_difference
                    del buy_prices[match.group(1)]
                else:
                    raise ValueError("Error of re")
            else:
                raise ValueError("Missmatch letter")
        except Exception as e:
            print(e)

result_flat /= trades_done

print(f"Nombre de trades effectués:{trades_done}")
print(f"Pourcentage de gain flat sur la période testée: {result_flat}")
print(f"Pourcentage de gain en réinvestissant sur la période testée: {result_reinvested}")