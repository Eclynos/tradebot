import re

result_flat = 0
result_reinvested = 1
trades_done = 0
buy_prices = {}

with open("trade_logs.log", "r") as f:
    for line in f:
        try:
            if line[26] == "B":
                match = re.search(r'(\w+/\w+)', line)
                match_price = re.search(r'at (\d+\.\d+|\d+e-\d+)', line)
                if match and match_price:
                    buy_prices[match.group(1)] = match_price.group(1)
                else:
                    raise ValueError("Error of re")
            elif line[26] == "S":
                match = re.search(r'(\w+/\w+)', line)
                match_price = re.search(r'at (\d+\.\d+|\d+e-\d+)', line)
                if match and match_price:
                    trades_done += 1
                    last_price = float(buy_prices[match.group(1)])
                    new_price = float(match_price.group(1))
                    percentage_difference = (new_price - last_price) / last_price / 4
                    result_flat += percentage_difference
                    result_reinvested *= 1+percentage_difference
                    del buy_prices[match.group(1)]
                else:
                    raise ValueError("Error of re")
            else:
                raise ValueError(f"Missmatch letter:{line[26]}")
        except Exception as e:
            print(e)

result_flat /= trades_done

print(f"Nombre de trades effectués:{trades_done}")
print(f"Pourcentage de gain flat sur la période testée: {result_flat*100}%")
print(f"Pourcentage de gain en réinvestissant sur la période testée: {result_reinvested*100-100}%")