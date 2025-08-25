# Task 2: Stock Portfolio Tracker

# Hardcoded stock prices
stock_prices = {
    "APPLE": 180,
    "TESLA": 250,
    "MICROSOFT": 310,
    "GOOGLE": 140,
    "AMAZON": 130,
    "SAMSUNG":143
}

portfolio = {}
total_value = 0

print("📊 Stock Portfolio Tracker")
print("Available stocks:", ", ".join(stock_prices.keys()))

while True:
    stock = input("Enter stock symbol (or 'done' to finish): ").upper()
    if stock == "DONE":
        break
    if stock not in stock_prices:
        print("⚠️ Stock not available. Try again.")
        continue

    qty = int(input(f"Enter quantity of {stock}: "))
    portfolio[stock] = portfolio.get(stock, 0) + qty

# Calculate total investment
for stock, qty in portfolio.items():
    value = qty * stock_prices[stock]
    total_value += value
    print(f"{stock}: {qty} shares × ${stock_prices[stock]} = ${value}")

print("\n💰 Total Investment Value: $", total_value)

# (Optional) Save to file
with open("portfolio.txt", "w") as f:
    for stock, qty in portfolio.items():
        f.write(f"{stock}: {qty} shares × ${stock_prices[stock]} = ${qty * stock_prices[stock]}\n")
    f.write(f"\nTotal Investment: ${total_value}\n")

print("📂 Portfolio saved to portfolio.txt")
