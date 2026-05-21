# Crypto Price Tracker

Track cryptocurrency prices from the terminal with custom alerts.

## Features
- Real-time prices from CoinGecko
- 24h change indicators
- Custom price alerts (above/below thresholds)
- Configurable update interval

## Usage
```bash
python tracker.py                    # Track default coins (BTC, ETH, SOL, ADA)
python tracker.py --coins bitcoin ethereum  # Track specific coins
python tracker.py --once             # Single fetch and exit
python tracker.py --interval 30      # Update every 30 seconds
```

## Alerts
Edit `alerts.json` to set price alerts:
```json
[
    {"coin": "bitcoin", "direction": "above", "price": 100000},
    {"coin": "ethereum", "direction": "below", "price": 2000}
]
```
