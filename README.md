
# Opal Purchase Listener

This script monitors incoming SOL payments to the Opal shop wallet:
- Small Opal: 0.02 SOL + 0.01 fee = 0.03~0.04 SOL
- Large Opal: 0.05 SOL + 0.01 fee = 0.06+ SOL

### To run:

```bash
pip install solana
python opal_listener.py
```

You will see console output when a user purchases either item.
