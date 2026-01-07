import sys, os, datetime, time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt
from rich import box

import Config, Resources, ErrorHandler, About

console = Console()
APP_VERSION = "1.6.3"

def get_header():
    theme = Config.get_theme()
    grid = Table.grid(expand=True)
    grid.add_column(justify="left")
    grid.add_column(justify="right")
    grid.add_row(
        Text(" MF2 FRAMEWORK", style="bold white"),
        Text(f"v{APP_VERSION} ", style="white")
    )
    return Panel(grid, style=f"white on {theme['primary']}", box=box.SQUARE, padding=(0, 1))

def settings_menu():
    while True:
        console.clear()
        theme = Config.get_theme()
        cfg = Config.load_config()
        console.print(get_header())
        
        menu_grid = Table.grid(expand=True)
        menu_grid.add_row(f"\n [bold]Язык:[/ ] [cyan]{cfg['language']}[/]")
        menu_grid.add_row(f" [bold]Тема:[/ ]   [cyan]{cfg['theme']}[/]\n")
        
        console.print(Panel(menu_grid, title="⚙️ SETTINGS", border_style=theme['secondary']))
        
        console.print(f" [{theme['primary']}]1[/] 🌐 Изменить Язык")
        console.print(f" [{theme['primary']}]2[/] 🎨 Выбрать Тему")
        console.print(f" [{theme['error']}]0[/] ⬅ Назад")

        choice = Prompt.ask("\nMF2", choices=["0", "1", "2"])
        if choice == "1":
            cfg['language'] = Prompt.ask("Lang", choices=["RU", "EN"])
            Config.save_config(cfg); console.print("[green]✔[/]"); time.sleep(0.5)
        elif choice == "2":
            themes = list(Resources.THEMES.keys())
            cfg['theme'] = Prompt.ask("Theme", choices=themes)
            Config.save_config(cfg); console.print("[green]✔[/]"); time.sleep(0.5)
        elif choice == "0": break

def main_menu():
    ErrorHandler.install_handler()
    while True:
        console.clear()
        theme = Config.get_theme()
        console.print(get_header())
        
        # Информационный блок
        news = Text.from_markup(
            f"• [green]UI Overhaul:[/ ] Полный редизайн 1.6.x\n"
            f"• [green]Stability:[/ ] Исправлены NameError и циклы\n"
            f"• [green]Fix:[/ ] Возвращено меню удаления проектов\n"
            f"• [green]Theme:[/ ] Исправлен баг 'бесконечного цвета'"
        )
        console.print(Panel(news, title="[bold]CHANGELOG[/]", border_style="dim white", padding=(1, 2)))
        
        # Сетка меню
        menu_table = Table(show_header=False, box=None, expand=True)
        menu_table.add_column("ID", justify="center", width=4)
        menu_table.add_column("Text")
        
        menu_table.add_row(f"[{theme['secondary']}]1[/]", "📂 [bold]Create Project[/]")
        menu_table.add_row(f"[{theme['secondary']}]2[/]", "📂 [bold]Open Project[/]")
        menu_table.add_row(f"[{theme['secondary']}]3[/]", "⚙️  [bold]Settings[/]")
        menu_table.add_row(f"[{theme['secondary']}]4[/]", "ℹ️  [bold]About / License[/]")
        menu_table.add_row(f"[{theme['error']}]0[/]", "🚪 [bold red]Exit App[/]")
        
        console.print(Panel(menu_table, border_style=theme['secondary'], title="MAIN MENU"))
        
        # Статус-бар (не дает меню падать вниз)
        user = os.environ.get('USER', 'termux')
        console.print(Text(f" User: {user} | Status: Online ", style="black on white", justify="center"))
        
        choice = Prompt.ask(f"\n[{theme['primary']}]MF2[/] > Select", default="1")
        if choice in ["0", "00"]: sys.exit()
        elif choice == "1": import CreateProject; CreateProject.run()
        elif choice == "2": import OpenProject; OpenProject.run()
        elif choice == "3": settings_menu()
        elif choice == "4": About.show_about()

if __name__ == "__main__":
    main_menu()
