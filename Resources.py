from rich import box

# Стили рамок
BOX_STYLE = box.ROUNDED

# Цветовые схемы
THEMES = {
    "Default": {"primary": "green", "secondary": "cyan", "warning": "yellow", "error": "red", "border": "green"},
    "Cyberpunk": {"primary": "bold magenta", "secondary": "bold cyan", "warning": "bold yellow", "error": "bold red", "border": "magenta"},
    "Matrix": {"primary": "green", "secondary": "bold green", "warning": "white", "error": "red", "border": "green"},
    "Ocean": {"primary": "blue", "secondary": "cyan", "warning": "magenta", "error": "red", "border": "blue"}
}

# Переводы
LANGUAGES = {
    "RU": {
        "welcome": "Добро пожаловать, Разработчик!",
        "select": "Выберите действие",
        "menu_create": "Создать новый мод",
        "menu_open": "Открыть проводник",
        "menu_settings": "Настройки системы",
        "menu_exit": "Выход из MF2"
    },
    "EN": {
        "welcome": "Welcome, Developer!",
        "select": "Select action",
        "menu_create": "Create New Mod",
        "menu_open": "Open Explorer",
        "menu_settings": "Settings",
        "menu_exit": "Exit Framework"
    }
}