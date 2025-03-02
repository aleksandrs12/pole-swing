prices = {
    0: [200, 50],
    1: [100, 125],
    2: [25, 300],
    3: [25, 200]
}

c1 = 2150
c2 = 1200

k = c1 / c2

for n in range(0, 4):
    prices[n][1] = prices[n][1] * k
    print(prices[n], prices[n][0] - prices[n][1])