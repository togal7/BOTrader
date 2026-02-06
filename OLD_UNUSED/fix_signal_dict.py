with open('handlers.py', 'r') as f:
    content = f.read()

print("=== FIXING SIGNAL DICT ERROR ===\n")

# Znajdź problematyczną linię i napraw
old_code = """        # Format analysis result
        signal = analysis.get('signal', 'NEUTRAL')
        confidence = analysis.get('confidence', 0)
        rsi = analysis.get('rsi', 0)
        
        signal_emoji = {
            'LONG': '🟢',
            'SHORT': '🔴',
            'NEUTRAL': '⚪'
        }.get(signal, '⚪')"""

new_code = """        # Format analysis result
        signal_data = analysis.get('signal', 'NEUTRAL')
        
        # Signal może być dict lub string
        if isinstance(signal_data, dict):
            signal = signal_data.get('direction', 'NEUTRAL')
        else:
            signal = signal_data
        
        confidence = analysis.get('confidence', 0)
        rsi = analysis.get('rsi', 0)
        
        signal_emoji = {
            'LONG': '🟢',
            'SHORT': '🔴',
            'NEUTRAL': '⚪'
        }.get(signal, '⚪')"""

content = content.replace(old_code, new_code)
print("✅ Fixed signal handling")

with open('handlers.py', 'w') as f:
    f.write(content)

