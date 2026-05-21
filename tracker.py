#!/usr/bin/env python3
"""Crypto price tracker with alert thresholds."""
import json
import time
import urllib.request

COINGECKO_API = "https://api.coingecko.com/api/v3/simple/price"
DEFAULT_COINS = ["bitcoin", "ethereum", "solana", "cardano"]

def fetch_prices(coins: list, vs: str = "usd") -> dict:
    ids = ",".join(coins)
    url = f"{COINGECKO_API}?ids={ids}&vs_currencies={vs}&include_24hr_change=true"
    req = urllib.request.Request(url, headers={"User-Agent": "crypto-tracker/1.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read())

def display_prices(prices: dict):
    print(f"\n{'Coin':<12} {'Price':>12} {'24h Change':>12}")
    print("-" * 40)
    for coin, data in prices.items():
        price = data.get("usd", 0)
        change = data.get("usd_24h_change", 0)
        arrow = "▲" if change >= 0 else "▼"
        print(f"{coin:<12} ${price:>10,.2f} {arrow} {abs(change):>8.2f}%")

def load_alerts(filepath: str = "alerts.json") -> list:
    try:
        with open(filepath) as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def check_alerts(prices: dict, alerts: list):
    for alert in alerts:
        coin = alert["coin"]
        if coin in prices:
            current = prices[coin]["usd"]
            if alert["direction"] == "above" and current > alert["price"]:
                print(f"\n ALERT: {coin} is above ${alert['price']} (current: ${current:,.2f})")
            elif alert["direction"] == "below" and current < alert["price"]:
                print(f"\n ALERT: {coin} is below ${alert['price']} (current: ${current:,.2f})")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Crypto price tracker")
    parser.add_argument("--coins", nargs="+", default=DEFAULT_COINS, help="Coins to track")
    parser.add_argument("--interval", type=int, default=60, help="Update interval in seconds")
    parser.add_argument("--once", action="store_true", help="Fetch once and exit")
    args = parser.parse_args()
    
    alerts = load_alerts()
    
    while True:
        try:
            prices = fetch_prices(args.coins)
            display_prices(prices)
            check_alerts(prices, alerts)
        except Exception as e:
            print(f"Error: {e}")
        
        if args.once:
            break
        print(f"\nNext update in {args.interval}s... (Ctrl+C to stop)")
        time.sleep(args.interval)

if __name__ == "__main__":
    main()
