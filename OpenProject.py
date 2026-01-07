import os, time, sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from rich import box
import shutil
import Config

console = Console()
PROJECTS_DIR = os.path.expanduser("~/mf2_projects")

def get_projects():
    if not os.path.exists(PROJECTS_DIR): os.makedirs(PROJECTS_DIR)
    return [d for d in os.listdir(PROJECTS_DIR) if os.path.isdir(os.path.join(PROJECTS_DIR, d))]

def delete_project(name):
    path = os.path.join(PROJECTS_DIR, name)
    console.print(f"[bold red]⚠ УДАЛЕНИЕ:[/]{name}")
    if Prompt.ask("Введите 'del' для подтверждения") == "del":
        shutil.rmtree(path)
        console.print("[green]Удалено успешно.[/]")
        time.sleep(1)
        return True
    return False

def run():
    while True:
        console.clear()
        theme = Config.get_theme()
        
        console.print(Panel(
            Text("📂 PROJECT EXPLORER", justify="center", style="bold white"),
            style=f"white on {theme['secondary']}",
            box=box.SQUARE
        ))

        projects = get_projects()
        if not projects:
            console.print("\n[dim]Проектов нет.[/]")
            Prompt.ask("Enter для возврата")
            break

        table = Table(expand=True, box=box.ROUNDED, border_style=theme['secondary'])
        table.add_column("ID", justify="center", style=theme['primary'], width=4)
        table.add_column("Project Name")
        table.add_column("Status", justify="right")

        for idx, name in enumerate(projects, 1):
            table.add_row(str(idx), name, "[dim]Folder[/]")

        console.print(table)
        console.print(f"\n[bold {theme['primary']}]0[/] ⬅ Назад | [bold {theme['error']}]00[/] 🚪 Выход")
        
        choice = Prompt.ask("\nSelect ID")

        if choice == "00": sys.exit()
        if choice == "0": break

        if choice.isdigit() and 1 <= int(choice) <= len(projects):
            selected = projects[int(choice)-1]
            
            # ВЕРНУЛОСЬ ПОДМЕНЮ
            while True:
                console.clear()
                console.print(Panel(f"Project: [bold cyan]{selected}[/]"))
                console.print("[1] 📂 Open (Открыть)")
                console.print("[2] 🗑  Delete (Удалить)")
                console.print("[0] ⬅ Back (Назад)")
                
                act = Prompt.ask("Action", choices=["1", "2", "0"])
                if act == "1":
                    import MainProject
                    res = MainProject.run(selected)
                    if res == "HOME": return # Use return instead of break to go back to MainApp
                    break 
                elif act == "2":
                    if delete_project(selected): break
                elif act == "0":
                    break