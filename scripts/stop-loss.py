purchase_price = 15.21
stop_loss_pct = 8.15

# Calculate stop loss price based on a 10% loss from purchase price
stop_loss_price = purchase_price - (purchase_price * stop_loss_pct / 100)

print(f"Sample stop-loss price: ${stop_loss_price:.2f}")
