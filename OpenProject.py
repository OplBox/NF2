import os, time, sys, shutil
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from rich import box
import Config

console = Console()
PROJECTS_DIR = os.path.expanduser("~/mf2_projects")

def run():
    while True:
        console.clear()
        theme = Config.get_theme()
        
        # Шапка в стиле IDE
        head = Table.grid(expand=True)
        head.add_row(Text(" 📂 PROJECT EXPLORER", style="bold white"), Text("Search: * ", style="white"))
        console.print(Panel(head, style=f"white on {theme['secondary']}", box=box.SQUARE))

        if not os.path.exists(PROJECTS_DIR): os.makedirs(PROJECTS_DIR)
        projects = [d for d in os.listdir(PROJECTS_DIR) if os.path.isdir(os.path.join(PROJECTS_DIR, d))]
        
        if not projects:
            console.print(Panel("[dim]Папка проектов пуста. Создайте проект в главном меню.[/]", border_style="yellow"))
            Prompt.ask("\nНажмите Enter")
            break

        table = Table(expand=True, box=box.ROUNDED, border_style=theme['secondary'])
        table.add_column("ID", style=theme['primary'], justify="center", width=4)
        table.add_column("Название папки")
        table.add_column("Статус", justify="right")

        for idx, name in enumerate(projects, 1):
            table.add_row(str(idx), name, "[green]Folder[/]")

        console.print(table)
        console.print(f"\n [bold {theme['primary']}]0[/] ⬅ Назад | [bold {theme['error']}]00[/] 🚪 Выход")
        
        choice = Prompt.ask("\nSelect ID")
        if choice == "00": sys.exit()
        if choice == "0": break

        if choice.isdigit() and 1 <= int(choice) <= len(projects):
            selected = projects[int(choice)-1]
            
            # Подменю действий
            while True:
                console.clear()
                console.print(Panel(f"Выбран проект: [bold cyan]{selected}[/]", border_style=theme['primary']))
                console.print(f" [{theme['primary']}]1[/] 📂 Открыть (Open)")
                console.print(f" [{theme['primary']}]2[/] 🗑  Удалить (Delete)")
                console.print(" [0] ⬅ Назад")
                
                act = Prompt.ask("\nAction", choices=["0", "1", "2"])
                if act == "1":
                    import MainProject
                    res = MainProject.run(selected)
                    if res == "HOME": return # Use return instead of break to go back to MainApp
                    break 
                elif act == "2":
                    if Prompt.ask("Напишите 'del' для удаления") == "del":
                        shutil.rmtree(os.path.join(PROJECTS_DIR, selected))
                        break
                elif act == "0": break