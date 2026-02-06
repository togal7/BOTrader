with open('handlers.py', 'r') as f:
    content = f.read()

print("STEP 1: Changing menu callbacks\n")

# Zamień callback_data w przyciskach
replacements = [
    ("callback_data='scan_gainers'", "callback_data='scan_select_gainers'"),
    ("callback_data='scan_losers'", "callback_data='scan_select_losers'"),
    ("callback_data='scan_rsi_oversold'", "callback_data='scan_select_rsi_oversold'"),
    ("callback_data='scan_rsi_overbought'", "callback_data='scan_select_rsi_overbought'"),
    ("callback_data='scan_volume'", "callback_data='scan_select_volume'"),
]

for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        print(f"✅ {old} → {new}")

with open('handlers.py', 'w') as f:
    f.write(content)

print("\n✅ Step 1 complete")

