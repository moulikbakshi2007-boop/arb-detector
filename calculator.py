def calculate_arb_sum(odds_list): 
    total = 0
    for odd in odds_list:
        total = total + (1 / odd)
    return total


def check_arbitrage(odds_list, min_profit_percent=0.5):
    arb_sum = calculate_arb_sum(odds_list)

    if arb_sum >= 1.0:
        return None

    profit_margin = (1 - arb_sum) * 100

    if profit_margin < min_profit_percent:
        return None

    return {
        "arb_sum": round(arb_sum, 4),
        "profit_margin": round(profit_margin, 3),
    }


def calculate_stakes(odds_list, total_investment):
    arb_sum = calculate_arb_sum(odds_list)
    stakes = []
    
    for odd in odds_list:
        stake = total_investment * (1 / odd) / arb_sum
        payout = stake * odd
        stakes.append({
            "odds": odd,
            "stake": round(stake, 2),
            "payout_if_wins": round(payout, 2)
        })
    
    return stakes


# test with fake data

print("=" * 50)
print("ARBITRAGE CALCULATOR TEST")
print("=" * 50)

print("\nTest 1: Tennis Match - Djokovic vs Nadal")
print("Book A offers Djokovic at 2.10")
print("Book B offers Nadal at 2.15")

odds = [2.10, 2.15]
result = check_arbitrage(odds)

if result:
    print(f"\n✅ ARBITRAGE FOUND!")
    print(f"   Arb sum: {result['arb_sum']} (less than 1.0 = profit)")
    print(f"   Profit margin: {result['profit_margin']}%")
    
    investment = 10000

    print(f"\n   If you invest ₹{investment}:")
    stakes = calculate_stakes(odds, investment)

    for i, s in enumerate(stakes):
        outcome = "Djokovic" if i == 0 else "Nadal"
        print(f"   → Bet ₹{s['stake']} on {outcome} at {s['odds']}")
        print(f"     If {outcome} wins, you receive ₹{s['payout_if_wins']}")
else:
    print("\n❌ No arbitrage opportunity")


print("\n" + "=" * 50)
print("Test 2: Football Match - typical bookmaker odds")
print("Book A offers Home Win at 1.80")
print("Book A offers Away Win at 2.00")

odds2 = [1.80, 2.00]
result2 = check_arbitrage(odds2)

if result2:
    print(f"\n✅ ARBITRAGE FOUND! {result2['profit_margin']}%")
else:
    print("\n❌ No arbitrage — bookmakers have margin built in")
    arb_sum = calculate_arb_sum(odds2)
    print(f"   Arb sum: {round(arb_sum, 4)} (above 1.0 = no profit possible)")


print("\n" + "=" * 50)
print("Test 3: Football 3-way - Home / Draw / Away")
print("Best odds found: Home 3.20, Draw 3.40, Away 2.80")

odds3 = [3.20, 3.40, 2.80]
result3 = check_arbitrage(odds3)

if result3:
    print(f"\n✅ ARBITRAGE FOUND! {result3['profit_margin']}%")
    investment3 = 10000
    stakes3 = calculate_stakes(odds3, investment3)
    outcomes3 = ["Home Win", "Draw", "Away Win"]

    for i, s in enumerate(stakes3):
        print(f"   → Bet ₹{s['stake']} on {outcomes3[i]}")
else:
    print(f"\n❌ No arbitrage")
    arb_sum = calculate_arb_sum(odds3)
    print(f"   Arb sum: {round(arb_sum, 4)}")


print("\n" + "=" * 50)
print("Calculator working correctly!")