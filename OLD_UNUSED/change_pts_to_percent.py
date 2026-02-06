with open('handlers.py', 'r') as f:
    content = f.read()

# Zamień wszystkie wystąpienia "pts" na "%~" w kafelkach
content = content.replace('}pts"', '}%~"')

# Dodaj też wyjaśnienie w tekście nad kafelkami
old_warning = '⚠️ pts = wstępna ocena. Kliknij aby zobaczyć pełną analizę!'
new_warning = '⚠️ %~ = wstępna ocena (pełna analiza po kliknięciu)'

content = content.replace(old_warning, new_warning)

with open('handlers.py', 'w') as f:
    f.write(content)

print("✅ Zmieniono pts → %~")

