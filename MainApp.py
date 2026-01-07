import sys
import os
import datetime
import time  # ИСПРАВЛЕНО
from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt
from rich.align import Align
from rich import box

# Наши модули
try:
    import Config
    import Resources
    import ErrorHandler
except ImportError:
    # Заглушка, если модули еще не созданы
    class Config:
        @staticmethod
        def get_theme(): return {"primary": "green", "secondary": "cyan", "border": "green", "warning": "yellow", "error": "red"}
        @staticmethod
        def get_text(key): return key # Просто возвращаем ключ, если нет перевода
    class Resources:
        # Для совместимости, если BOX_STYLE еще не определен
        THEMES = {"Default": {"primary": "green", "secondary": "cyan", "border": "green"}}
        BOX_STYLE = box.ROUNDED

console = Console()
APP_VERSION = "1.6.3"
BUILD_DATE = "Jan 2026"

def settings_menu():
    """Интерактивное меню настроек"""
    while True:
        console.clear()
        theme = Config.get_theme()
        cfg = Config.load_config()
        
        console.print(Panel(
            Text("⚙️ SETTINGS CONTROL CENTER", justify="center", style="bold white"),
            style=f"white on {theme['primary']}",
            box=box.SQUARE
        ))

        console.print(f"\n[bold]Язык:[/] [cyan]{cfg['language']}[/]")
        console.print(f"[bold]Тема:[/]   [cyan]{cfg['theme']}[/]\n")

        console.print("[1] 🌐 Изменить Язык (RU/EN)")
        console.print("[2] 🎨 Выбрать Тему (Галерея)")
        console.print("[0] ⬅ Назад")

        choice = Prompt.ask("\nAction", choices=["0", "1", "2"])

        if choice == "1":
            new_lang = Prompt.ask("Выберите язык", choices=["RU", "EN"])
            cfg['language'] = new_lang
            Config.save_config(cfg)
            console.print("[green]✔ Применено![/]")
            time.sleep(0.5)
        elif choice == "2":
            # Тут можно вызвать галерею из Resources
            themes_list = list(Resources.THEMES.keys())
            new_theme = Prompt.ask("Выберите тему", choices=themes_list)
            cfg['theme'] = new_theme
            Config.save_config(cfg)
            console.print(f"[green]✔ Тема {new_theme} активна![/]")
            time.sleep(0.5)
        elif choice == "0":
            break

def get_header():
    theme = Config.get_theme()
    grid = Table.grid(expand=True)
    grid.add_column(justify="left", ratio=1)
    grid.add_column(justify="right")
    grid.add_row(
        Text("MF2 FRAMEWORK", style="bold white"),
        Text(f"v{APP_VERSION} [{BUILD_DATE}]", style="white")
    )
    return Panel(grid, style=f"white on {theme['primary']}", box=box.SQUARE)

def main_menu():
    if hasattr(ErrorHandler, 'install_handler'):
        ErrorHandler.install_handler()

    while True:
        console.clear()
        theme = Config.get_theme()
        console.print(get_header())
        
        news_content = f"[bold cyan]What's New in {APP_VERSION}:[/]\n• [green]UI Overhaul:[/] Полный редизайн 1.6.x\n• [green]Stability:[/] Исправлены NameError и циклы\n• [green]Fix:[/] Возвращено меню удаления проектов\n• [green]Theme:[/] Исправлен баг \"бесконечного цвета\""
        
        console.print(Panel(news_content, title="[bold]CHANGELOG[/]", border_style="dim white", height=9))
        
        table = Table(show_header=False, box=None, expand=True)
        table.add_row(f"[{theme['secondary']}]1[/]", "📂 [bold]Create Project[/]")
        table.add_row(f"[{theme['secondary']}]2[/]", "📂 [bold]Open Project[/]")
        table.add_row(f"[{theme['secondary']}]3[/]", "⚙️  [bold]Settings[/]")
        table.add_row(f"[{theme['error']}]0[/]", "🚪 [bold red]Exit App[/]")
        
        console.print(Panel(table, border_style=theme['secondary']))
        
        choice_str = Prompt.ask(f"\n[{theme['primary']}]MF2[/] > Select", default="1")

        if choice_str == "0" or choice_str == "00":
            sys.exit()
        elif choice_str == "1":
            import CreateProject
            CreateProject.run()
        elif choice_str == "2":
            import OpenProject
            OpenProject.run()
        elif choice_str == "3":
            # Тут вызываем settings_menu, если она у тебя в коде есть
            try:
                # from MainApp import settings_menu # Removed cyclic import
                settings_menu()
            except Exception as e:
                console.print(f"[red]Error loading settings: {e}[/]")
                time.sleep(1)

if __name__ == "__main__":
    main_menu()
