import os
import glob

replacements = [
    ('BOTrader', 'BOTrader'),
    ('Bot BOTrader', 'BOTrader'),
    ('BOTrader Bot', 'BOTrader'),
]

py_files = glob.glob('*.py')
total_changes = 0

for filepath in py_files:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        file_changes = 0
        
        for old, new in replacements:
            count = content.count(old)
            if count > 0:
                content = content.replace(old, new)
                file_changes += count
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ {filepath}: {file_changes} zmian")
            total_changes += file_changes
    
    except Exception as e:
        print(f"⚠️ {filepath}: {e}")

print(f"\n✅ TOTAL: {total_changes} zmian w {len(py_files)} plikach")

