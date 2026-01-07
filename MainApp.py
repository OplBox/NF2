import sys
import os
import datetime
from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt
from rich.align import Align
from rich import box # ИСПРАВЛЕНО

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
APP_VERSION = "1.6.3" # ОБНОВЛЕНО
BUILD_DATE = "Jan 2026"

def get_header():
    theme = Config.get_theme()
    grid = Table.grid(expand=True)
    grid.add_column(justify="left", ratio=1)
    grid.add_column(justify="right")
    
    title = Text("MF2 FRAMEWORK", style=f"bold white")
    ver = Text(f"v{APP_VERSION} [{BUILD_DATE}]", style="white")
    
    grid.add_row(title, ver)
    return Panel(grid, style=f"white on {theme['primary']}", box=box.SQUARE)

def get_menu_table():
    theme = Config.get_theme()
    table = Table(show_header=False, box=None, expand=True)
    table.add_column("Icon", width=4, justify="center")
    table.add_column("Title")
    
    table.add_row(f"[{theme['secondary']}]1[/]", "[bold]Create New Project[/]\n[dim]Создать новый мод с нуля")
    table.add_row("", "") 
    table.add_row(f"[{theme['secondary']}]2[/]", "[bold]Open Project[/]\n[dim]Открыть рабочий стол проекта")
    table.add_row("", "")
    table.add_row(f"[{theme['secondary']}]3[/]", "[bold]Settings[/]\n[dim]Темы, Язык, Настройки")
    table.add_row("", "")
    table.add_row(f"[{theme['error']}]0[/]", "[red]Exit Framework")
    
    return Panel(table, title="[bold]MAIN MENU[/]", border_style=theme['secondary'], padding=(1, 2))

def get_status_bar():
    theme = Config.get_theme()
    user = os.environ.get('USER', 'termux')
    time_now = datetime.datetime.now().strftime("%H:%M")
    return Text(f" User: {user} | Time: {time_now} | System: Online ", style="black on white", justify="center")

def main_menu():
    if hasattr(ErrorHandler, 'install_handler'):
        ErrorHandler.install_handler()

    while True:
        console.clear()
        theme = Config.get_theme()
        
        console.print(get_header())
        
        # ИСПРАВЛЕН БАГ ЦВЕТОВ (Закрыты теги [/])
        news_content = f"""
[bold cyan]What's New in {APP_VERSION}:[/]

• [green]UI Fix:[/][white] Исправлены NameError и импорты[/]
• [green]Core:[/][white] Стабильный билд 1.21.11[/]
• [green]Build:[/][white] Улучшена проверка Loader 0.18.4[/]
• [green]Theme:[/][white] Добавлен предпросмотр стилей[/]"""
        
        news_panel = Panel(news_content, title="[bold]CHANGELOG[/]", border_style="dim white", height=10)
        console.print(news_panel)
        console.print(get_menu_table())
        console.print(get_status_bar())
        
        choice_str = Prompt.ask(f"\n[{theme['primary']}]MF2[/] > Select", default="1")

        if choice_str == "0" or choice_str == "00":
            console.print(f"[bold red]Shutting down...[/]")
            sys.exit()

        if choice_str == "1":
            import CreateProject
            CreateProject.run()
        elif choice_str == "2":
            import OpenProject
            OpenProject.run()
        elif choice_str == "3":
            # Тут вызываем settings_menu, если она у тебя в коде есть
            try:
                from MainApp import settings_menu
                settings_menu()
            except:
                console.print("[yellow]Settings menu loading...[/]")
                time.sleep(0.5)

if __name__ == "__main__":
    main_menu()