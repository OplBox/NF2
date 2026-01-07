import os, time, sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text # ИСПРАВЛЕНО
from rich import box
import Config

console = Console()
PROJECTS_DIR = os.path.expanduser("~/mf2_projects")

def run():
    while True:
        console.clear()
        theme = Config.get_theme()
        
        # Теперь Text определен!
        console.print(Panel(
            Text("📂 PROJECT EXPLORER", justify="center", style="bold white"),
            style=f"white on {theme['secondary']}",
            box=box.SQUARE
        ))

        if not os.path.exists(PROJECTS_DIR): os.makedirs(PROJECTS_DIR)
        projects = [d for d in os.listdir(PROJECTS_DIR) if os.path.isdir(os.path.join(PROJECTS_DIR, d))]
        
        if not projects:
            console.print("\n[dim]У вас пока нет созданных проектов.[/]")
            Prompt.ask("\nНажмите Enter, чтобы вернуться")
            break

        table = Table(expand=True, box=box.ROUNDED, border_style=theme['secondary'])
        table.add_column("ID", style=theme['primary'], justify="center", width=4)
        table.add_column("Название проекта (Folder)", style="bold white")
        table.add_column("Путь", style="dim white")

        for idx, name in enumerate(projects, 1):
            table.add_row(str(idx), name, f"~/mf2_projects/{name}")

        console.print(table)
        console.print(f"\n[bold {theme['primary']}]0[/] ⬅ Назад | [bold {theme['error']}]00[/] 🚪 Выход")
        
        choice = Prompt.ask("\nВыберите ID проекта")

        if choice == "00": sys.exit()
        if choice == "0": break

        if choice.isdigit() and 1 <= int(choice) <= len(projects):
            selected = projects[int(choice)-1]
            import MainProject
            res = MainProject.run(selected)
            if res == "HOME": break