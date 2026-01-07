import os
import shutil
import sys
import time
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()
PROJECTS_DIR = os.path.expanduser("~/mf2_projects")

def get_projects():
    if not os.path.exists(PROJECTS_DIR): os.makedirs(PROJECTS_DIR)
    projects = [d for d in os.listdir(PROJECTS_DIR) if os.path.isdir(os.path.join(PROJECTS_DIR, d))]
    projects.sort()
    return projects

def delete_project(project_name):
    project_path = os.path.join(PROJECTS_DIR, project_name)
    console.print(f"[bold red]WARN:[/ ] Удалить [white]{project_name}[/]?")
    if Prompt.ask("Напишите 'del' для подтверждения", default="") == "del":
        try:
            shutil.rmtree(project_path)
            console.print("[green]✅ Удалено[/]")
            time.sleep(0.5)
            return True
        except Exception as e:
            console.print(f"[red]Ошибка при удалении: {e}[/]")
            input("Enter...")
            return False
    console.print("[yellow]Удаление отменено.[/]")
    time.sleep(1)
    return False

def run():
    while True:
        console.clear()
        console.print(Panel("[bold cyan]📂 EXPLORER[/]", border_style="cyan"))
        
        projects = get_projects()
        
        for idx, name in enumerate(projects, 1):
            console.print(f" {idx}. {name}")
        
        console.print("\n [0]  ⬅ Назад в Главное Меню")
        console.print(" [00] 🚪 Exit")
        
        choice_str = Prompt.ask("\nSelect", default="0")
        
        if choice_str == "0": return
        if choice_str == "00": 
            console.print("[bold red]Bye![/]")
            sys.exit()
        
        if choice_str.isdigit():
            idx = int(choice_str)
            if 1 <= idx <= len(projects):
                selected = projects[idx - 1]
                
                # Мини-меню перед открытием
                while True:
                    console.clear()
                    console.print(f"[bold cyan]Selected: {selected}[/]")
                    console.print(" [1] Open")
                    console.print(" [2] Delete")
                    console.print(" [0] Cancel")
                    
                    act = Prompt.ask("Action", choices=["1", "2", "0", "00"], default="0")
                    
                    if act == "1":
                        import MainProject
                        res = MainProject.run(selected)
                        # Если нажали "0" в MainProject, вернемся сюда (в список)
                        # Если нажали "00", sys.exit() сработает внутри MainProject, сюда даже не дойдет
                        if res == "BACK": break 
                    elif act == "2":
                        if delete_project(selected): break
                    elif act == "0":
                        break
                    elif act == "00":
                        console.print("[bold red]Bye![/]")
                        sys.exit()
        else:
            console.print("[red]Неверный ввод[/]")
            time.sleep(1)
