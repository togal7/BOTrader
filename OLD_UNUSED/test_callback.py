import sys
sys.path.insert(0, '/bots/BOTrader')

from database import db

# Pobierz user
user_id = 6169603983  # Twój user_id
user = db.get_user(user_id)

print(f"User: {user_id}")
print(f"Has cache: {'cached_scan_results' in user}")

if 'cached_scan_results' in user:
    cached = user['cached_scan_results']
    print(f"Cache length: {len(cached)}")
    print(f"First entry: {cached[0] if cached else 'Empty'}")
else:
    print("❌ NO CACHE IN USER!")

