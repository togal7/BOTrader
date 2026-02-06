"""
Admin Features Configuration
Kontrolki włączania/wyłączania funkcji dla użytkowników
"""

import json
import os

FEATURES_FILE = 'features_config.json'

# Default config
DEFAULT_CONFIG = {
    'subscription_enabled': False,  # Wyłączone - bot w testach
    'referral_enabled': True,       # Włączone
    'payments_enabled': False       # Wyłączone - nie pobieramy opłat
}

def load_features_config():
    """Load features configuration"""
    if os.path.exists(FEATURES_FILE):
        with open(FEATURES_FILE, 'r') as f:
            return json.load(f)
    else:
        # Create default
        save_features_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG

def save_features_config(config):
    """Save features configuration"""
    with open(FEATURES_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def is_feature_enabled(feature_name):
    """Check if feature is enabled"""
    config = load_features_config()
    return config.get(feature_name, False)

def toggle_feature(feature_name):
    """Toggle feature on/off"""
    config = load_features_config()
    current = config.get(feature_name, False)
    config[feature_name] = not current
    save_features_config(config)
    return config[feature_name]

def get_all_features():
    """Get all features status"""
    return load_features_config()

