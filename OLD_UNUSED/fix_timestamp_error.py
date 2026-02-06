with open('handlers.py', 'r') as f:
    content = f.read()

print("=== FIXING TIMESTAMP ERROR ===\n")

# Zamień wszystkie odwołania do timestamp na bezpieczne
content = content.replace(
    "timestamp = alert['timestamp']",
    "timestamp = alert.get('triggered_at', alert.get('timestamp', 'N/A'))"
)

# W show_alert_detail też napraw
old = "⏰ {alert.get('triggered_at', '')}"
new = "⏰ {alert.get('triggered_at', alert.get('timestamp', 'N/A'))}"
content = content.replace(old, new)

print("✅ Fixed timestamp references")

with open('handlers.py', 'w') as f:
    f.write(content)

