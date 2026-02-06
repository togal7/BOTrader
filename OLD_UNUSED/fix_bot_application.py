with open('bot.py', 'r') as f:
    content = f.read()

print("Fixing application reference...")

# Znajdź main() function
import re

# application.run_polling() jest poza main() - musi być w środku
# Usuń błędne wywołanie poza funkcją
lines = content.split('\n')
new_lines = []
skip_next = False

for i, line in enumerate(lines):
    # Usuń application.run_polling() poza main()
    if 'application.run_polling(' in line and 'def main():' not in '\n'.join(lines[max(0,i-20):i]):
        print(f"Removing line {i}: {line}")
        continue
    
    new_lines.append(line)

content = '\n'.join(new_lines)

with open('bot.py', 'w') as f:
    f.write(content)

print("✅ Fixed!")

