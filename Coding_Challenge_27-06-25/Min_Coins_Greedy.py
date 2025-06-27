def minimize_coins(amount):
    denominations = [500, 200, 100, 50, 20, 10, 5, 2, 1]
    result = []

    for coin in denominations:
        while amount >= coin:
            amount -= coin
            result.append(coin)

    print("Minimum coins needed:")
    print(result)
    print("Total coins used:", len(result))

# Example usage
amount = int(input("Enter the amount: "))
minimize_coins(amount)
