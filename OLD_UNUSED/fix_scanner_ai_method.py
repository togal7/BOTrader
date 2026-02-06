with open('alert_scanner.py', 'r') as f:
    content = f.read()

print("=== FIXING AI TRADER METHOD NAME ===\n")

# Sprawdź co jest używane
if 'analyze_pair_full' in content:
    # Zamień na analyze_pair jeśli taka metoda istnieje
    content = content.replace(
        'await ai_trader.analyze_pair_full(',
        'await ai_trader.analyze_pair('
    )
    print("✅ Changed analyze_pair_full → analyze_pair")

with open('alert_scanner.py', 'w') as f:
    f.write(content)

