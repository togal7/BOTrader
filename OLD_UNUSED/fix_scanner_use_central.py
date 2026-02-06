with open('alert_scanner.py', 'r') as f:
    content = f.read()

print("=== FIXING SCANNER TO USE CENTRAL ANALYZER ===\n")

# 1. Zmień import
old_import = "from ai_trader import ai_trader"
new_import = "from central_ai_analyzer import central_analyzer"

content = content.replace(old_import, new_import)
print("✅ Changed import")

# 2. Zmień wywołanie
old_call = "await ai_trader.analyze_pair("
new_call = "await central_analyzer.analyze_pair_full("

content = content.replace(old_call, new_call)
print("✅ Changed method call")

with open('alert_scanner.py', 'w') as f:
    f.write(content)

print("\n✅ Fixed!")

