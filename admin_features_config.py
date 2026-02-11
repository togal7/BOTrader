"""
Admin Features Config - kontrolki widoczności funkcji
Zapisuje stan w pliku JSON
"""
import json
import os

CONFIG_FILE = 'admin_features.json'

# Domyślne wartości
DEFAULTS = {
    'subscription_enabled': True,
    'referral_enabled': True,
}

def load_features():
    """Wczytaj config z pliku"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                data = json.load(f)
                # Uzupełnij brakujące klucze domyślnymi
                for k, v in DEFAULTS.items():
                    if k not in data:
                        data[k] = v
                return data
        except:
            pass
    return DEFAULTS.copy()

def save_features(features):
    """Zapisz config do pliku"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(features, f, indent=2)

def get_all_features():
    """Pobierz wszystkie ustawienia"""
    return load_features()

def get_feature(name):
    """Pobierz wartość konkretnej funkcji"""
    features = load_features()
    return features.get(name, DEFAULTS.get(name, True))

def toggle_feature(name):
    """Przełącz funkcję ON/OFF - zwróć nowy stan"""
    features = load_features()
    current = features.get(name, DEFAULTS.get(name, True))
    features[name] = not current
    save_features(features)
    return features[name]

def set_feature(name, value):
    """Ustaw konkretną wartość"""
    features = load_features()
    features[name] = value
    save_features(features)
    return value
