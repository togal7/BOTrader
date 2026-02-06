with open('handlers.py', 'r') as f:
    content = f.read()

# Znajdź część z unique_users (linie 863-869)
import re
match = re.search(r'(# Usuń duplikaty po user_id.*?unique_users\.append\(u\))', content, re.DOTALL)

if match:
    print("=== FOUND unique_users logic ===")
    print(match.group(1))
    print()
    
# Pokaż całą pętlę
match2 = re.search(r'(seen_ids = set\(\).*?for u in unique_users\[:15\]:)', content, re.DOTALL)
if match2:
    print("=== FULL LOOP ===")
    print(match2.group(1))

