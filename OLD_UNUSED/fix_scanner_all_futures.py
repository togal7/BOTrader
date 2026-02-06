with open('handlers.py', 'r') as f:
    content = f.read()

print("=== SCANNING ALL FUTURES ===\n")

# Zmień [:50] na wszystkie
old_line = "        for symbol in list(futures_symbols)[:50]:"
new_line = "        for symbol in list(futures_symbols):  # Scan ALL futures"

if old_line in content:
    content = content.replace(old_line, new_line)
    print("✅ Changed from [:50] to ALL futures")
else:
    # Może jeszcze nie ma futures_symbols
    if "for symbol in list(symbols)[:50]:" in content:
        content = content.replace(
            "for symbol in list(symbols)[:50]:",
            "# Filter ONLY futures\n        futures_symbols = [s for s in symbols if ':USDT' in s]\n        logger.info(f'Scanning {len(futures_symbols)} FUTURES')\n        \n        for symbol in futures_symbols:"
        )
        print("✅ Added futures filter + scan ALL")

with open('handlers.py', 'w') as f:
    f.write(content)

