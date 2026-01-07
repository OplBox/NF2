import sys
import time
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text

# Наши модули
import Config
import Resources

console = Console()
APP_VERSION = "1.0.0" # Rel.Beta.Demo (1.0.0)

def settings_menu():
    """Меню настроек Языка и Темы"""
    while True:
        console.clear()
        cfg = Config.load_config()
        theme = Config.get_theme()
        
        console.print(Panel(f"[bold]SETTINGS[/]", border_style=theme['border']))
        
        console.print(f"Текущий язык: [{theme['secondary']}]{cfg['language']}[/]")
        console.print(f"Текущая тема: [{theme['secondary']}]{cfg['theme']}[/]\n")
        
        console.print("[1] 🌐 Change Language (RU/EN)")
        console.print("[2] 🎨 Change Theme")
        console.print("[0] ⬅ Back")
        
        choice = Prompt.ask("\nAction", choices=["0", "1", "2"])
        
        if choice == "1":
            new_lang = Prompt.ask("Select Language", choices=["RU", "EN"], default="RU")
            cfg['language'] = new_lang
            Config.save_config(cfg)
            console.print("[green]Saved![/]")
            time.sleep(0.5)
            
        elif choice == "2":
            # Показываем список тем
            themes_list = list(Resources.THEMES.keys())
            console.print(f"Available: {', '.join(themes_list)}")
            new_theme = Prompt.ask("Select Theme", choices=themes_list, default="Default")
            cfg['theme'] = new_theme
            Config.save_config(cfg)
            console.print("[green]Saved![/]")
            time.sleep(0.5)
            
        elif choice == "0":
            break

def show_banner():
    console.clear()
    theme = Config.get_theme()
    
    title = Text("Minecraft Mods For Fabric (MF2)", style=theme['primary'])
    subtitle = Text(f"v{APP_VERSION} | Release", style="italic white")
    
    welcome_text = Config.get_text("welcome")
    
    console.print(Panel(
        f"\n[{theme['secondary']}]{welcome_text}[/]\n"
        f"System: Termux\n",
        title=title,
        subtitle=subtitle,
        border_style=theme['border'],
        padding=(1, 2)
    ))

def main_menu():
    while True:
        show_banner()
        theme = Config.get_theme()
        
        # Берем тексты из конфига
        t_create = Config.get_text("menu_create")
        t_open = Config.get_text("menu_open")
        t_settings = Config.get_text("menu_settings")
        t_exit = Config.get_text("menu_exit")
        
        console.print(f"[1] 📂 {t_create}")
        console.print(f"[2] 📂 {t_open}")
        console.print(f"[3] ⚙️  {t_settings}")
        console.print(f"[0] 🚪 {t_exit}")
        console.print(f"[{theme['border']}]────────────────────────────────────────[/]")
        
        choice_str = Prompt.ask(Config.get_text("select"), default="1")

        if choice_str == "0" or choice_str == "00":
            console.print(f"[{theme['error']}]{Config.get_text('exit_msg')}[/]")
            sys.exit()

        if choice_str == "1":
            import CreateProject
            # Можно добавить перезагрузку модуля для применения темы, но пока так
            CreateProject.run()
        elif choice_str == "2":
            import OpenProject
            OpenProject.run()
        elif choice_str == "3":
            settings_menu()

if __name__ == "__main__":
    # Если запускаем напрямую MainApp, всё равно ловим ошибки
    import ErrorHandler
    ErrorHandler.install_handler()
    main_menu()
