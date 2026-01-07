import os
import json
from Resources import THEMES, LANGUAGES

CONFIG_FILE = os.path.expanduser("~/mmff/settings.json")

# Дефолтные настройки
DEFAULT_CONFIG = {
    "language": "RU",
    "theme": "Default"
}

def load_config():
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG
    
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except:
        return DEFAULT_CONFIG

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def get_text(key):
    cfg = load_config()
    lang_code = cfg.get("language", "RU")
    return LANGUAGES[lang_code].get(key, key)

def get_theme():
    cfg = load_config()
    theme_name = cfg.get("theme", "Default")
    return THEMES.get(theme_name, THEMES["Default"])

# Глобальный объект для быстрого доступа
current_config = load_config()
