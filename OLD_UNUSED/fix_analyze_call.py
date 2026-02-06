with open('handlers.py', 'r') as f:
    content = f.read()

# Zamień wywołanie analyze_pair_full
old_call = """        analysis = await central_analyzer.analyze_pair_full(
            exchange=exchange,
            symbol=symbol,
            timeframe=timeframe,
            context=context
        )"""

new_call = """        analysis = await central_analyzer.analyze_pair_full(
            symbol=symbol,
            exchange=exchange,
            timeframe=timeframe,
            context=context
        )"""

content = content.replace(old_call, new_call)

with open('handlers.py', 'w') as f:
    f.write(content)

print("✅ Naprawiono kolejność parametrów!")

